# -*- coding: UTF-8 -*-
"""Build the JTalk user dictionary (jtusr.dic) for JP smoke tests.

jtusr.dic is built from jtusr.csv with the x64 mecab-dict-index.exe that
"scons jtalkSync" builds from the patched libopenjtalk mecab source.
The produced dictionary must be binary-compatible with the runtime
sys.dic (Dictionary::isCompatible checks version, charset and the
left/right context table sizes), so it is always rebuilt against the
current dictionary directory instead of being stored in the repository.

jtusr.csv entries must carry explicit context IDs and costs. Automatic
ID assignment (empty ID fields) requires a CRF model file which
naist-jdic does not provide. Entries use 0,0 (BOS/EOS) plus a cost,
the same convention as the custom entries built into sys.dic
(custom_dic_maker.py); migration to per-POS context IDs is tracked as
roadmap task 2.8. See projectDocs/jp/userdic.md.
"""

import subprocess
import sys
from pathlib import Path

_jptools_dir = Path(__file__).resolve().parent
_repo_root = (_jptools_dir / ".." / "..").resolve()

CSV_PATH = _jptools_dir / "jtusr.csv"
USER_DIC_PATH = _jptools_dir / "jtusr.dic"
MECAB_DICT_INDEX = _jptools_dir / "jtalk" / "libopenjtalk" / "mecab" / "src" / "mecab-dict-index.exe"
DIC_DIR = _repo_root / "source" / "synthDrivers" / "jtalk" / "dic"

# Cache for ensure_user_dic: None = not attempted yet, list = result.
_built = None


def _missing_prerequisites():
	problems = []
	if not MECAB_DICT_INDEX.exists():
		problems.append("missing %s (run: scons jtalkSync)" % MECAB_DICT_INDEX)
	if not (DIC_DIR / "sys.dic").exists():
		problems.append("missing %s (run: scons jtalkSync)" % (DIC_DIR / "sys.dic"))
	if not CSV_PATH.exists():
		problems.append("missing %s" % CSV_PATH)
	return problems


def build_user_dic():
	"""Build jtusr.dic from jtusr.csv against the current runtime dictionary.

	Returns the path to the built dictionary. Raises RuntimeError when a
	prerequisite is missing or the build fails.
	"""
	problems = _missing_prerequisites()
	if problems:
		raise RuntimeError("cannot build user dictionary: " + "; ".join(problems))
	result = subprocess.run(
		[
			str(MECAB_DICT_INDEX),
			"-d",
			str(DIC_DIR),
			"-u",
			str(USER_DIC_PATH),
			"-f",
			"utf-8",
			"-t",
			"utf-8",
			str(CSV_PATH),
		],
		capture_output=True,
		text=True,
		encoding="utf-8",
		errors="replace",
	)
	output = (result.stdout or "") + (result.stderr or "")
	# mecab-dict-index may not exit nonzero on CHECK_DIE failures (the Open
	# JTalk build disables exit in die()), so also require the success marker.
	if result.returncode != 0 or "done!" not in output or not USER_DIC_PATH.exists():
		raise RuntimeError(
			"mecab-dict-index failed to build %s (exit %d):\n%s" % (USER_DIC_PATH, result.returncode, output),
		)
	return USER_DIC_PATH


def ensure_user_dic(strict=False):
	"""Return a list of user dictionary paths for Mecab_initialize.

	Rebuilds jtusr.dic once per process so that it always matches the
	current sys.dic. When prerequisites are missing: raises if strict,
	otherwise prints a warning and returns an empty list so callers can
	run without a user dictionary.
	"""
	global _built
	if _built is not None:
		return list(_built)
	problems = _missing_prerequisites()
	if problems:
		if strict:
			raise RuntimeError("cannot build user dictionary: " + "; ".join(problems))
		print("build_userdic: user dictionary skipped: " + "; ".join(problems))
		_built = []
		return []
	build_user_dic()
	_built = [str(USER_DIC_PATH)]
	return list(_built)


if __name__ == "__main__":
	try:
		path = build_user_dic()
	except RuntimeError as e:
		print(str(e))
		sys.exit(1)
	print("built %s" % path)
