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
CASES = [
	("一人", "ヒトリ"),
	("二人", "フタリ"),
	("二百十日", "2ヒャク トオカ"),
	("ごめんください", "ゴメン クダサイ"),
	("おはようございます", "オハヨー ゴザイマス"),
]


def verify() -> int:
	"""Run verification. Returns 0 on success, 1 on failure."""
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
		for text, expected in CASES:
			result, _, _, _ = translator2.translateWithInPos2(
				text, logwrite=lambda s: None, nabcc=False
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
