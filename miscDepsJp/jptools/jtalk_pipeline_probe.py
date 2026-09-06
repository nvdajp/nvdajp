# -*- coding: utf-8 -*-
"""Probe JTalk pipeline outputs for regression investigation.

Usage:
  uv run --python .venv\\Scripts\\python.exe python -m miscDepsJp.jptools.jtalk_pipeline_probe
  uv run --python .venv\\Scripts\\python.exe python -m miscDepsJp.jptools.jtalk_pipeline_probe "一人" "二人"
"""

from __future__ import annotations

import json
import os
import sys
from ctypes import string_at
from pathlib import Path


def _resolve_repo_root() -> Path:
	repo_root = os.environ.get("REPO_ROOT")
	if repo_root:
		p = Path(repo_root).resolve()
		if (p / "miscDepsJp").exists():
			return p
	script_dir = Path(__file__).resolve().parent
	return (script_dir / ".." / "..").resolve()


REPO_ROOT = _resolve_repo_root()
JTALK_DIR = REPO_ROOT / "source" / "synthDrivers" / "jtalk"

if str(JTALK_DIR) in sys.path:
	sys.path.remove(str(JTALK_DIR))
sys.path.insert(0, str(JTALK_DIR))

import jtalkPrepare  # type: ignore
import jtalkCore  # type: ignore
from jtalkCore import (  # type: ignore
	libjt_initialize,
	libjt_load,
	libjt_set_alpha,
	libjt_set_beta,
	libjt_synthesis,
	libjt_refresh,
)
from mecab import (  # type: ignore
	Mecab_initialize,
	Mecab_analysis,
	Mecab_correctFeatures,
	Mecab_utf8_to_cp932,
	MecabFeatures,
)
from text2mecab import text2mecab  # type: ignore


DEFAULT_TEXTS = [
	"一人",
	"二人",
	"二百十日",
	"ごめんください",
	"おはようございます",
	"寄付行為",
	"アクセント記号",
]
_is_initialized = False


def _decode_feature(raw: bytes) -> str:
	for enc in ("utf-8", "cp932", "mbcs"):
		try:
			return raw.decode(enc)
		except UnicodeDecodeError:
			continue
	return raw.decode("utf-8", errors="replace")


def _iter_features(mf: MecabFeatures, limit: int = 8) -> list[str]:
	from ctypes import string_at

	items: list[str] = []
	for i in range(min(mf.size, limit)):
		items.append(_decode_feature(string_at(mf.feature[i])))
	return items


def _probe_one(text: str, feature_limit: int = 8) -> dict:
	prepared = jtalkPrepare.convert(text)
	src = text2mecab(prepared)
	mf = MecabFeatures()
	Mecab_analysis(src, mf)
	Mecab_correctFeatures(mf)
	feature_head = _iter_features(mf, limit=feature_limit)
	token_count = mf.size
	max_feature_len = max(
		(len(string_at(mf.feature[i])) for i in range(mf.size)),
		default=0,
	)
	Mecab_utf8_to_cp932(mf)
	buf = libjt_synthesis(mf.feature, mf.size, fperiod_=240)
	libjt_refresh()
	return {
		"text": text,
		"prepared": prepared,
		"tokenCount": token_count,
		"featureHead": feature_head,
		"maxFeatureLen": max_feature_len,
		"waveBytes": len(buf) if buf else 0,
		"hasWave": bool(buf),
	}


def initialize() -> None:
	global _is_initialized
	if _is_initialized:
		return
	if hasattr(os, "add_dll_directory"):
		try:
			os.add_dll_directory(str(JTALK_DIR))
		except OSError:
			pass
	libjt_initialize(JTALK_DIR / "libopenjtalk.dll")
	libjt_load(JTALK_DIR / "tohokuf01" / "tohoku-f01-neutral.htsvoice")
	libjt_set_alpha(0.54)
	libjt_set_beta(0.00)
	Mecab_initialize(None, str(JTALK_DIR), str(JTALK_DIR / "dic"))
	_is_initialized = True


def probe_text(text: str, feature_limit: int = 8) -> dict:
	initialize()
	return _probe_one(text, feature_limit=feature_limit)


def probe_digit_compound(text: str = "12") -> dict:
	"""Check njd_set_digit merges ASCII digits into compound readings.

	While Mecab_utf8_to_cp932 runs before libjt_synthesis, njd_set_digit must stay
	compiled as CHARSET_SHIFT_JIS. UTF-8 rule tables against CP932 node strings
	fail strcmp and leave digit-by-digit readings (イチ+ニ instead of ジュウニ).
	"""
	from ctypes import string_at

	initialize()
	assert jtalkCore.libjt is not None
	prepared = jtalkPrepare.convert(text)
	src = text2mecab(prepared)
	mf = MecabFeatures()
	Mecab_analysis(src, mf)
	Mecab_correctFeatures(mf)
	mecab_token_count = mf.size
	Mecab_utf8_to_cp932(mf)
	libjt = jtalkCore.libjt
	njd = jtalkCore.njd
	jpcommon = jtalkCore.jpcommon
	libjt.mecab2njd(njd, mf.feature, mf.size)
	libjt.njd_set_pronunciation(njd)
	libjt.njd_set_digit(njd)
	libjt.njd2jpcommon(jpcommon, njd)
	libjt.JPCommon_make_label(jpcommon)
	label_count = libjt.JPCommon_get_label_size(jpcommon)
	label_feature = libjt.JPCommon_get_label_feature(jpcommon)
	labels = "".join(
		string_at(label_feature[i]).decode("ascii", errors="replace")
		for i in range(label_count)
	)
	libjt_refresh()
	labels_lower = labels.lower()
	# Merged twelve: ju-mora path. Digit-by-digit: i+ch (イチ) mora path.
	digit_merged = ("j+u" in labels_lower or "j-u" in labels_lower) and (
		"i+ch" not in labels_lower and "i-ch" not in labels_lower
	)
	return {
		"text": text,
		"mecabTokenCount": mecab_token_count,
		"labelCount": label_count,
		"hasWave": label_count > 2,
		"digitMerged": digit_merged,
		"labelsSnippet": labels[:400],
	}


def main() -> int:
	initialize()

	texts = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_TEXTS
	for text in texts:
		print(json.dumps(_probe_one(text), ensure_ascii=False))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
