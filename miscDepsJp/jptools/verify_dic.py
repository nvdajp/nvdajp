# -*- coding: utf-8 -*-
# miscDepsJp/jptools/verify_dic.py
# Verifies that the MeCab dictionary includes custom entries (e.g. 一人→ヒトリ).
# Used by verifyJtalkDictionary.ps1 for CI and local validation.

import os
import sys
from pathlib import Path

# Resolve repo root and jtalk paths (verify_dic.py is in miscDepsJp/jptools)
script_dir = Path(__file__).resolve().parent
repo_root = (script_dir / ".." / "..").resolve()
if not (repo_root / "source").exists():
	repo_root = (script_dir / ".." / ".." / "..").resolve()

jtalk_dir = repo_root / "source" / "synthDrivers" / "jtalk"
dic_dir = jtalk_dir / "dic"

# Add jtalk to path for imports
sys.path.insert(0, str(jtalk_dir))

# Verification cases: (input_text, expected_output)
# CI: sanity only (translator2 normalizations + minimal custom-dic signal).
# Local/certBuild: strict custom-dictionary coverage before release smoke tests.
CASES_BASIC = [
	("一人", "ヒトリ"),
	("二人", "フタリ"),
	("おはようございます", "オハヨー ゴザイマス"),
]

CASES_STRICT = [
	("二百十日", "2ヒャク トオカ"),
	("ごめんください", "ゴメン クダサイ"),
	("寄付行為", "キフ コーイ"),
	("晴れ所により一時雨", "ハレ トコロニ ヨリ イチジ アメ"),
	("行っていらっしゃい", "イッテ イラッシャイ"),
]


def _cases_for_run() -> list[tuple[str, str]]:
	mode = os.environ.get("JP_VERIFY_DIC_MODE", "").strip().lower()
	if mode == "basic":
		return list(CASES_BASIC)
	if mode == "strict":
		return CASES_BASIC + CASES_STRICT
	# Default: basic on GHA (chcp/console env differs); strict locally.
	if os.environ.get("GITHUB_ACTIONS") == "true":
		return list(CASES_BASIC)
	return CASES_BASIC + CASES_STRICT


def verify() -> int:
	"""Run verification. Returns 0 on success, 1 on failure."""
	cases = _cases_for_run()
	mode_label = "basic" if len(cases) == len(CASES_BASIC) else "strict"
	print(f"verify_dic: mode={mode_label}, cases={len(cases)}")
	# Fail fast if dictionary is missing (e.g. jtalkSync did not run or failed)
	if not (dic_dir / "sys.dic").exists():
		print(
			f"ERROR: Dictionary not found at {dic_dir} (sys.dic missing). Run scons jtalkSync first.",
			file=sys.stderr,
		)
		return 1

	import jtalkDir  # noqa: E402
	import translator2  # noqa: E402

	dll_handle = None
	if hasattr(os, "add_dll_directory"):
		try:
			dll_handle = os.add_dll_directory(str(jtalk_dir))
		except OSError as e:
			print(f"ERROR: add_dll_directory failed: {e}", file=sys.stderr)
			return 1

	try:
		translator2.initialize(lambda s: None, str(jtalk_dir), str(dic_dir), jtalkDir.user_dics)
		failed = 0
		for text, expected in cases:
			result, _, _, _ = translator2.translateWithInPos2(
				text, logwrite=lambda s: None, nabcc=False,
			)
			if result != expected:
				print(
					f"FAIL: {text!r} -> expected {expected!r}, got {result!r}",
					file=sys.stderr,
				)
				failed += 1
			else:
				print(f"OK: {text!r} -> {result!r}")
		return 1 if failed else 0
	except Exception as e:
		import traceback

		print(f"ERROR: MeCab initialization or translation failed: {e}", file=sys.stderr)
		traceback.print_exc(file=sys.stderr)
		return 1
	finally:
		if dll_handle is not None:
			dll_handle.close()


if __name__ == "__main__":
	sys.exit(verify())
