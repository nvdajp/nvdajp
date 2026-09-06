# coding: UTF-8
# jtalk_dic.py
# Copyright (C) 2026 Takuya Nishimoto
# License: BSD 3-Clause. See LICENSE.
#
# MeCab + JTalk extended dictionary (NAIST-JDIC + nvdajp custom entries)
# adapter for translator2.
#
# The dictionary binaries (sys.dic, matrix.bin, char.bin, unk.dic, dicrc,
# DIC_VERSION) are NOT part of this source tree. They are built and published
# from the libkuraji-jtalk-dic repository as GitHub Release assets
# (jtalk-dic-v*.zip). This module downloads the zip for a pinned tag on
# demand, extracts it to a cache directory, and wraps a fugashi Tagger so it
# can be injected into translator2.initialize(analyzer=...).
#
# This is an OPTIONAL runtime path. The default libkuraji test suite uses
# a recorded fixture (mecabFixture.json) via ReplayAnalyzer and does not
# require MeCab, fugashi, or network access. Integration tests opt in via
# the LIBKURAJI_INTEGRATION=1 environment variable.

import hashlib
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import zipfile
from pathlib import Path
from collections.abc import Callable

# Pinned default release tag of libkuraji-jtalk-dic. Override with the
# LIBKURAJI_JTALK_DIC_TAG environment variable. Bump this when a new
# dictionary release is validated against the harness. Keep this in sync
# with miscDepsJp/jptools/jtalk-dic-version.txt (checked by
# tests/unit/test_jpDicPins.py).
DEFAULT_DIC_TAG = "v1.1.10"

# Owner/repo of the dictionary release.
DIC_REPO = "nishimotz/libkuraji-jtalk-dic"

# Asset name pattern for the dictionary zip. Must match release-dic.yml
# in libkuraji-jtalk-dic.
_DIC_ZIP_NAME = "jtalk-dic-{tag}.zip"
_DIC_ZIP_SHA_NAME = "jtalk-dic-{tag}.zip.sha256"
_DIC_TAG_RE = re.compile(r"^v\d+\.\d+\.\d+$")
_DOWNLOAD_TIMEOUT_SEC = 120


# Halfwidth-to-fullwidth conversion for the MeCab input pipeline.
#
# The JTalk extended dictionary (NAIST-JDIC + nvdajp custom entries) was
# built with fullwidth ASCII characters as its unknown-word (unk) class
# definitions, so MeCab must be fed fullwidth input to reproduce the
# analysis recorded in tests/mecabFixture.json. This is the text2mecab
# conversion originally written by Takuya Nishimoto for python-jtalk,
# re-licensed to BSD 3-Clause for libkuraji.
#
# The dedicated fullwidth block U+FF01..U+FF5E mirrors ASCII U+0021..U+007E
# one-to-one. The ASCII space (U+0020) maps to U+3000. Three characters
# have special targets that differ from the naive fullwidth mapping:
# - "-" (HYPHEN-MINUS) -> U+2212 MINUS SIGN
# - "~" (TILDE) -> U+301C WAVE DASH
# - "\" (REVERSE SOLIDUS) -> U+FFE5 FULLWIDTH YEN SIGN
# - U+FFFD REPLACEMENT CHARACTER -> fullwidth question mark
_HALF_TO_FULL: dict[str, str] = {}
for _c in range(0x21, 0x7F):  # '!' .. '~'
	_HALF_TO_FULL[chr(_c)] = chr(_c + 0xFEE0)
_HALF_TO_FULL[" "] = "\u3000"  # fullwidth space
_HALF_TO_FULL["-"] = "\u2212"  # MINUS SIGN
_HALF_TO_FULL["~"] = "\u301c"  # WAVE DASH
_HALF_TO_FULL["\\"] = "\uffe5"  # FULLWIDTH YEN SIGN
_HALF_TO_FULL["\ufffd"] = "\uff1f"  # fullwidth question mark
_HALF2FULL_TABLE = str.maketrans(_HALF_TO_FULL)


def _to_mecab_text(text: str) -> str:
	"""Normalize text the way the JTalk dictionary expects.

	NFKC-normalize (which folds compatibility characters down to their
	halfwidth ASCII form), then widen ASCII to the fullwidth block the
	dictionary's unk classes were built against.
	"""
	text = unicodedata.normalize("NFKC", text)
	return text.translate(_HALF2FULL_TABLE)


def _env_truthy(name: str) -> bool:
	v = os.environ.get(name, "").strip().lower()
	return v in ("1", "true", "yes", "on")


def _validate_dic_tag(tag: str) -> str:
	tag = tag.strip()
	if not _DIC_TAG_RE.fullmatch(tag):
		raise ValueError(f"invalid dictionary release tag: {tag!r}")
	return tag


def get_dic_tag() -> str:
	"""Return the dictionary release tag to use."""
	raw = os.environ.get("LIBKURAJI_JTALK_DIC_TAG", DEFAULT_DIC_TAG).strip()
	return _validate_dic_tag(raw or DEFAULT_DIC_TAG)


def get_cache_dir() -> Path:
	"""Return the cache directory used to store downloaded dictionaries.

	Override with LIBKURAJI_JTALK_DIC_DIR (points directly at an already
	extracted dictionary directory, skipping download entirely).
	"""
	override = os.environ.get("LIBKURAJI_JTALK_DIC_DIR", "").strip()
	if override:
		return Path(override)
	base = os.environ.get("LIBKURAJI_CACHE_DIR", "").strip()
	if base:
		return Path(base) / "libkuraji-jtalk-dic"
	# ~/.cache/libkuraji-jtalk-dic on POSIX, %LOCALAPPDATA% on Windows.
	if sys.platform == "win32":
		local = os.environ.get("LOCALAPPDATA")
		if local:
			return Path(local) / "libkuraji-jtalk-dic"
	return Path.home() / ".cache" / "libkuraji-jtalk-dic"


def _gh_available() -> bool:
	return shutil.which("gh") is not None


def _parse_sha256_digest(content: str) -> str:
	line = content.strip().splitlines()[0]
	return line.split()[0].lower()


def _verify_zip_sha256(zip_path: Path, expected_digest: str) -> None:
	digest = hashlib.sha256()
	with zip_path.open("rb") as f:
		for chunk in iter(lambda: f.read(65536), b""):
			digest.update(chunk)
	actual = digest.hexdigest().lower()
	expected = expected_digest.lower()
	if actual != expected:
		raise RuntimeError(f"SHA-256 mismatch for {zip_path.name}: expected {expected}, got {actual}")


def _safe_extract_zip(zf: zipfile.ZipFile, dest: Path) -> None:
	dest_resolved = dest.resolve()
	for member in zf.namelist():
		target = (dest / member).resolve()
		if not target.is_relative_to(dest_resolved):
			raise RuntimeError(f"unsafe zip member path: {member!r}")
	zf.extractall(dest)


def _log_subprocess_output(
	logwrite: Callable[[str], None] | None,
	prefix: str,
	data: bytes | None,
) -> None:
	if not logwrite or not data:
		return
	text = data.decode("utf-8", errors="replace").strip()
	if text:
		logwrite(f"{prefix}: {text}")


def _download_assets(
	tag: str,
	cache: Path,
	zip_name: str,
	sha_name: str,
	logwrite: Callable[[str], None] | None = None,
) -> None:
	zip_path = cache / zip_name
	sha_path = cache / sha_name
	downloaded = False
	if _gh_available():
		try:
			result = subprocess.run(
				[
					"gh",
					"release",
					"download",
					tag,
					"--repo",
					DIC_REPO,
					"--pattern",
					zip_name,
					"--pattern",
					sha_name,
					"--dir",
					str(cache),
					"--clobber",
				],
				check=True,
				capture_output=True,
			)
			downloaded = True
			_log_subprocess_output(logwrite, "gh download stdout", result.stdout)
		except subprocess.CalledProcessError as exc:
			if logwrite:
				logwrite(f"gh download failed (exit {exc.returncode}); falling back to GitHub REST API")
			_log_subprocess_output(logwrite, "gh download stdout", exc.stdout)
			_log_subprocess_output(logwrite, "gh download stderr", exc.stderr)
		except FileNotFoundError:
			if logwrite:
				logwrite("gh CLI not found; falling back to GitHub REST API")

	if not downloaded:
		_download_asset_via_rest(tag, zip_name, zip_path)
		_download_asset_via_rest(tag, sha_name, sha_path)

	if not sha_path.exists():
		raise RuntimeError(f"SHA-256 sidecar not found for {zip_name}")
	expected_digest = _parse_sha256_digest(sha_path.read_text(encoding="utf-8"))
	_verify_zip_sha256(zip_path, expected_digest)


def download_dic(
	tag: str | None = None,
	force: bool = False,
	logwrite: Callable[[str], None] | None = None,
) -> Path:
	"""Download and extract the dictionary zip for the given release tag.

	Returns the path to the extracted dictionary directory (the one
	containing sys.dic). Uses the gh CLI if available, otherwise falls
	back to the GitHub REST API via urllib.
	"""
	tag = _validate_dic_tag(tag or get_dic_tag())
	cache = get_cache_dir()
	# When LIBKURAJI_JTALK_DIC_DIR points directly at a dictionary dir,
	# cache == that dir and we must not try to "extract" into it.
	if os.environ.get("LIBKURAJI_JTALK_DIC_DIR", "").strip():
		if (cache / "sys.dic").exists():
			return cache
		raise FileNotFoundError(f"LIBKURAJI_JTALK_DIC_DIR={cache} does not contain sys.dic")

	extracted = cache / tag
	if (extracted / "sys.dic").exists() and not force:
		return extracted

	cache.mkdir(parents=True, exist_ok=True)
	zip_name = _DIC_ZIP_NAME.format(tag=tag)
	sha_name = _DIC_ZIP_SHA_NAME.format(tag=tag)
	zip_path = cache / zip_name

	if not zip_path.exists() or force:
		_download_assets(tag, cache, zip_name, sha_name, logwrite=logwrite)
	else:
		sha_path = cache / sha_name
		if not sha_path.exists():
			_download_asset_via_rest(tag, sha_name, sha_path)
		expected_digest = _parse_sha256_digest(sha_path.read_text(encoding="utf-8"))
		_verify_zip_sha256(zip_path, expected_digest)

	with zipfile.ZipFile(zip_path) as zf:
		_safe_extract_zip(zf, extracted)

	dicrc_path = extracted / "dicrc"
	if dicrc_path.exists():
		try:
			content = dicrc_path.read_bytes()
			lf_content = content.replace(b"\r\n", b"\n")
			if lf_content != content:
				dicrc_path.write_bytes(lf_content)
		except Exception:
			pass

	if not (extracted / "sys.dic").exists():
		raise RuntimeError(f"sys.dic not found in extracted {zip_name}; archive layout changed?")
	return extracted


def _download_asset_via_rest(tag: str, asset_name: str, dest: Path) -> None:
	import json
	import urllib.parse
	import urllib.request

	tag_quoted = urllib.parse.quote(tag, safe="")
	url = f"https://api.github.com/repos/{DIC_REPO}/releases/tags/{tag_quoted}"
	with urllib.request.urlopen(url, timeout=_DOWNLOAD_TIMEOUT_SEC) as r:
		release = json.loads(r.read().decode("utf-8"))
	asset_url = None
	for a in release.get("assets", []):
		if a.get("name") == asset_name:
			asset_url = a.get("browser_download_url")
			break
	if not asset_url:
		raise RuntimeError(f"asset {asset_name} not found in release {tag}")
	with urllib.request.urlopen(asset_url, timeout=_DOWNLOAD_TIMEOUT_SEC) as r, dest.open("wb") as f:
		shutil.copyfileobj(r, f)


class JTalkDicAnalyzer:
	"""Morphological analyzer backed by MeCab (via fugashi) and the
	JTalk extended dictionary.

	Implements the small contract expected by translator2.initialize():
	- is_ready() -> bool
	- analyze(text, logwrite=None) -> list[str]   (MeCab feature lines)

	The feature lines are returned in the CSV form translator2 expects
	(surface + 13+ comma-separated feature fields), matching the format
	emitted by the JTalk extended dictionary's braille-notation field.
	"""

	def __init__(self, dic_dir: Path, logwrite: Callable[[str], None] | None = None):
		self.dic_dir = Path(dic_dir)
		self._log = logwrite or (lambda s: None)
		self._tagger = None
		try:
			from fugashi import GenericTagger  # type: ignore
		except ImportError as e:
			raise ImportError(
				"fugashi is required for JTalkDicAnalyzer; install with `pip install -e .[integration]`",
			) from e
		# fugashi.Tagger (the Unidic variant) rejects dictionaries whose
		# feature field count doesn't match Unidic's schema, so we use the
		# GenericTagger which accepts any feature layout.
		#
		# fugashi wraps the user arg with a forced `-C` and runs it through
		# shlex.split, which mangles backslashes on Windows. Always pass
		# forward-slash paths, and give MeCab an explicit `-r <dicrc>` so it
		# doesn't fall back to the system default (`c:\mecab\mecabrc`).
		d = str(self.dic_dir).replace("\\", "/")
		arg = f"-r {d}/dicrc -d {d}"
		self._tagger = GenericTagger(arg)
		self._log(f"JTalkDicAnalyzer initialized with dic_dir={self.dic_dir}")

	def is_ready(self) -> bool:
		return self._tagger is not None and (self.dic_dir / "sys.dic").exists()

	def _reparse(self, text: str) -> list[str]:
		"""Re-parse a single character to fill missing readings.

		Used by correct_features (PATTERN 1/2) for unknown words whose
		reading is empty. The input is widened the same way as analyze().
		"""
		text = _to_mecab_text(text)
		out: list[str] = []
		for word in self._tagger(text):
			out.append(f"{word.surface},{word.feature_raw}")
		return out

	def analyze(self, text: str, logwrite: Callable[[str], None] | None = None) -> list[str]:
		if self._tagger is None:
			raise RuntimeError("JTalkDicAnalyzer: tagger not initialized")
		log = logwrite or self._log
		# The JTalk dictionary's unknown-word classes are defined for
		# fullwidth ASCII, so we widen the input before handing it to
		# MeCab. This matches the analysis recorded in mecabFixture.json.
		text = _to_mecab_text(text)
		# GenericTagger exposes `feature_raw` (CSV feature string) and
		# `surface`. translator2.mecab_to_morphs expects each line to start
		# with the surface, followed by the comma-separated feature fields,
		# matching the format recorded in mecabFixture.json.
		raw_lines: list[str] = []
		for word in self._tagger(text):
			surface = word.surface
			raw = word.feature_raw
			raw_lines.append(f"{surface},{raw}")
			log(f"mecab: {raw_lines[-1]}")
		# Post-process (correct) the features to match the reference
		# analysis. The correction may re-parse individual characters to
		# fill missing readings for unknown words.
		from .mecab_correct import correct_features

		return correct_features(raw_lines, reparse=self._reparse)


def make_analyzer(
	tag: str | None = None,
	logwrite: Callable[[str], None] | None = None,
) -> JTalkDicAnalyzer:
	"""Convenience: download (if needed) and return a ready analyzer.

	Requires LIBKURAJI_INTEGRATION=1 to be set; otherwise raises so that
	accidental calls in the default test path fail loudly.
	"""
	if not _env_truthy("LIBKURAJI_INTEGRATION"):
		raise RuntimeError("JTalk dictionary integration is opt-in; set LIBKURAJI_INTEGRATION=1 to enable.")
	dic_dir = download_dic(tag, logwrite=logwrite)
	return JTalkDicAnalyzer(dic_dir, logwrite=logwrite)
