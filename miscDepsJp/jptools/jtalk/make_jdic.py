# coding: utf-8
# make_jdic.py
# Copyright (C) 2010-2013 Takuya Nishimoto (NVDA Japanese Team)

import os
import shutil
import subprocess
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

import custom_dic_maker
import eng_dic_maker
import tankan_dic_maker
from filter_jdic import filter_jdic


def _log_mode() -> str:
	mode = os.environ.get("JP_MECAB_LOG_MODE", "file").lower()
	if mode not in {"file", "console"}:
		mode = "file"
	return mode


@contextmanager
def _log_redirect(repo_root: Path, mode: str):
	if mode == "console":
		yield None, None
		return
	log_dir = repo_root / "output" / "_logs"
	log_dir.mkdir(parents=True, exist_ok=True)
	log_path = log_dir / "make_jdic.log"
	with (
		log_path.open("w", encoding="utf-8", errors="ignore") as fp,
		redirect_stdout(fp),
		redirect_stderr(fp),
	):
		yield log_path, fp


def mkdir_p(path_obj):
	"""Create directory and parents if needed."""
	Path(path_obj).mkdir(parents=True, exist_ok=True)


def _load_pos_id_patterns(pos_id_path: Path) -> list[list[str]]:
	"""Parse pos-id.def into a list of field-pattern lists.

	Each line is "<comma-separated POS pattern> <id>". A field pattern of "*"
	matches any value; otherwise the match is exact (pos-id.def of naist-jdic
	uses no alternation syntax). A pattern may have fewer fields than the
	feature; the remaining feature fields are unconstrained, mirroring
	RewritePattern::rewrite in mecab.
	"""
	patterns = []
	for line in pos_id_path.read_text(encoding="utf-8").splitlines():
		line = line.strip()
		if not line:
			continue
		pattern_str = line.rsplit(None, 1)[0]
		patterns.append(pattern_str.split(","))
	return patterns


def _pos_resolves(feature_fields: list[str], patterns: list[list[str]]) -> bool:
	for pat in patterns:
		if len(pat) > len(feature_fields):
			continue
		if all(p == "*" or p == f for p, f in zip(pat, feature_fields)):
			return True
	return False


def _validate_custom_pos(tempdir: Path, csv_names: list[str]) -> None:
	"""Fail the build when an nvdajp custom CSV row has a POS that pos-id.def
	cannot resolve.

	POSIDGenerator::id() returns -1 silently in that case (no log line), so the
	mecab-dict-index log scan cannot catch it; the token would be written with
	posid 65535. Only the nvdajp-generated CSVs are validated: naist-jdic.csv
	itself contains 12 rows (副詞,* / 名詞,非自立,*) that its own pos-id.def
	does not cover, which is an upstream data quirk we do not touch.
	"""
	patterns = _load_pos_id_patterns(tempdir / "pos-id.def")
	bad: list[str] = []
	for name in csv_names:
		for line in (tempdir / name).read_text(encoding="utf-8").splitlines():
			cols = line.split(",")
			# surface,lid,rid,cost,feature... (generated rows contain no quoted commas)
			if len(cols) < 5:
				continue
			if not _pos_resolves(cols[4:], patterns):
				bad.append(f"{name}: {line[:80]}")
	if bad:
		print(f"make_jdic: {len(bad)} custom CSV row(s) have a POS that pos-id.def cannot resolve:")
		for entry in bad[:20]:
			print(f"  {entry}")
		raise SystemExit(
			"make_jdic: dictionary build failed: unresolvable POS in custom CSV "
			"(POSIDGenerator would silently assign posid 65535)",
		)


def convert_file(src_file, src_enc, dest_file, dest_enc, apply_filter=False):
	print("converting %s to %s" % (src_file, dest_file))
	with open(src_file, "r", encoding=src_enc) as sf:
		with open(dest_file, "w", encoding=dest_enc) as df:
			while 1:
				s = sf.readline()
				if not s:
					break
				if apply_filter:
					s = s.rstrip()
					s = filter_jdic(s)
					if s:
						s += "\n"  # do not use os.linesep here
				df.write(s)


def _main():
	# MECAB_DICT_INDEX と OUTDIR は libopenjtalk/mecab-naist-jdic/_temp が基準
	jtdir = Path(__file__).resolve().parent
	engdic = jtdir / "bep-eng.dic"
	cs_file = jtdir / "characters-ja.dic"

	thisdir = jtdir / "libopenjtalk" / "mecab-naist-jdic"
	# Build output directly under source/ to avoid extra copy in jtalkSync.
	repo_root = (jtdir / ".." / ".." / "..").resolve()
	outdir = repo_root / "source" / "synthDrivers" / "jtalk" / "dic"
	tempdir = thisdir / "_temp"
	mecab_dict_index = thisdir.parent / "mecab" / "src" / "mecab-dict-index.exe"
	code = "utf-8"  # cp932

	mode = _log_mode()
	with _log_redirect(repo_root, mode) as (log_path, log_fp):
		mkdir_p(outdir)
		mkdir_p(tempdir)

		eng_dic_maker.make_dic(engdic, code, thisdir)
		tankan_dic_maker.make_dic(code, cs_file, thisdir)
		custom_dic_maker.make_dic(code, thisdir)

		files = [
			"dicrc",
			"nvdajp-eng-dic.csv",
			"nvdajp-tankan-dic.csv",
			"nvdajp-custom-dic.csv",
		]

		euc_files = [
			"char.def",
			"feature.def",
			"left-id.def",
			"matrix.def",
			"pos-id.def",
			"rewrite.def",
			"right-id.def",
			"unk.def",
		]

		jdic_file = "naist-jdic.csv"

		for f in files:
			src_path = thisdir / f
			print(f"copy {src_path} to {tempdir}")
			shutil.copy(str(src_path), str(tempdir))

		for f in euc_files:
			convert_file(str(thisdir / f), "euc-jp", str(tempdir / f), code)

		convert_file(
			str(thisdir / jdic_file),
			"euc-jp",
			str(tempdir / jdic_file),
			code,
			apply_filter=True,
		)

		_validate_custom_pos(
			tempdir,
			["nvdajp-eng-dic.csv", "nvdajp-tankan-dic.csv", "nvdajp-custom-dic.csv"],
		)

		print(f"{tempdir} {[str(mecab_dict_index), '-d', '.', '-o', str(outdir), '-f', code, '-c', code]}")
		# Capture output so we can scan it: mecab-dict-index never exits nonzero
		# on CHECK_DIE failures (the Open JTalk build disables exit in die()), so
		# errors like "cannot find LEFT-ID" would otherwise produce a corrupt,
		# non-reproducible sys.dic that only fails much later in smoke tests.
		result = subprocess.run(
			[str(mecab_dict_index), "-d", ".", "-o", str(outdir), "-f", code, "-c", code],
			cwd=str(tempdir),
			check=True,
			capture_output=True,
			text=True,
			encoding="utf-8",
			errors="replace",
		)
		tool_output = (result.stdout or "") + (result.stderr or "")
		# In file mode stdout is redirected to make_jdic.log; in console mode this
		# prints to the console, matching the previous behavior in both modes.
		print(tool_output)
		fatal_markers = [
			"cannot find LEFT-ID",
			"cannot find RIGHT-ID",
			"invalid ids are found",
			"may be broken",
			"rewrite failed",
			"no such file or directory",
			"format error",
			"not a number",
		]
		fatal_lines = [
			line for line in tool_output.splitlines() if any(m in line for m in fatal_markers)
		]
		if fatal_lines:
			print(f"make_jdic: mecab-dict-index reported {len(fatal_lines)} fatal error line(s):")
			for line in fatal_lines[:20]:
				print(f"  {line}")
			raise SystemExit(
				"make_jdic: dictionary build failed: mecab-dict-index reported errors "
				"(it does not exit nonzero on its own; see log for details)",
			)

		dicrc_src = thisdir / "dicrc"
		print(f"copy {dicrc_src} to {outdir}")
		shutil.copy(str(dicrc_src), str(outdir))
		# Runtime input and dictionary are UTF-8 (mecab-dict-index -f/-c utf-8). The template
		# dicrc still says EUC-JP; align config-charset so MeCab loads params consistently with
		# UTF-8 sys.dic (avoids CI vs local segmentation drift for custom entries).
		dicrc_dst = outdir / "dicrc"
		try:
			rc_text = dicrc_dst.read_text(encoding="utf-8")
			rc_text = rc_text.replace("config-charset = EUC-JP", "config-charset = UTF-8")
			rc_text = rc_text.replace("config-charset=sjis", "config-charset = UTF-8")
			dicrc_dst.write_text(rc_text, encoding="utf-8")
		except OSError as e:
			print(f"WARNING: could not patch dicrc for UTF-8: {e}")
		dic_version_file = outdir / "DIC_VERSION"
		print(f"dic version file: {dic_version_file}")
		version = f"nvdajp-jtalk-dic ({code}) {datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
		print(version)
		dic_version_file.write_text(version + os.linesep, encoding="utf-8")

	if mode == "file" and log_path:
		print(f"make_jdic: output suppressed; see {log_path}")


if __name__ == "__main__":
	_main()
