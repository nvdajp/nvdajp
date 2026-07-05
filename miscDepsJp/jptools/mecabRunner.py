# mecabRunner.py
# -*- coding: utf-8 -*-
# Japanese text processor test module
# by Takuya Nishimoto

import sys
from pathlib import Path

import build_userdic
from mecabHarness import tasks

# Use source/synthDrivers/jtalk directly (files moved from miscDepsJp in Phase 1)
script_dir = Path(__file__).resolve().parent
# script_dir -> miscDepsJp/jptools
# ../.. -> repo root
repo_root = (script_dir / ".." / "..").resolve()
jt_dir = repo_root / "source" / "synthDrivers" / "jtalk"
sys.path.insert(0, str(jt_dir))
from _nvdajp_unicode import unicode_normalize  # type: ignore
from mecab import *  # type: ignore

dic = jt_dir / "dic"


def __print(s):
	# Write to mecab_debug.log file only (not to console)
	# This ensures MeCab logs are only stored in logfile, not printed to console
	try:
		debug_log_path = (
			Path(__file__).parent.parent.parent / "source" / "synthDrivers" / "jtalk" / "mecab_debug.log"
		)
		debug_log_path.parent.mkdir(parents=True, exist_ok=True)
		with open(debug_log_path, "a", encoding="utf-8", errors="replace") as f:
			f.write(str(s) + "\n")
			f.flush()
	except Exception:
		# Logging is best-effort only. Failures must not interfere with normal operation.
		pass


def _truncate_debug_log():
	# mecab_debug.log is opened in append mode everywhere; truncate it once
	# per test process so CI failures are not diagnosed against log lines
	# left over from a previous run. This runs at import time, before any
	# test executes: doing it in runTasks() would be too late, as MecabTests
	# runs last in unittest class order (JpBrailleTests -> Jtalk* -> MecabTests)
	# and truncating there would wipe braille/jtalk debug log lines before CI
	# could collect them.
	try:
		debug_log_path = jt_dir / "mecab_debug.log"
		debug_log_path.write_text("", encoding="utf-8")
	except Exception:
		pass


_truncate_debug_log()


_buffer = ""


def clear_morph_buffer():
	global _buffer
	_buffer = ""


def print_morph_buffer():
	__print(_buffer)


def __print_dummy(s):
	global _buffer
	_buffer += s + "\n"


def Mecab_get_reading(mf, CODE_=CODE):  # type: ignore
	reading = ""
	braille = ""
	for pos in range(0, mf.size):
		ar = Mecab_getFeature(mf, pos, CODE_=CODE_).split(",")
		rd = ""
		if len(ar) > 9:
			rd = ar[9].replace("\u3000", " ")
		elif ar[0] != "ー":
			rd = unicode_normalize(ar[0])
		reading += rd
		if len(ar) > 12:
			braille += ar[12] + r"/"
		else:
			braille += rd + r"/"
	return (reading, braille.rstrip(r" /"))


def get_reading(msg):
	s = text2mecab(msg)
	# Hold the MeCab lock explicitly instead of via MecabFeatures, whose
	# release depends on __del__ (GC timing): a traceback keeping the object
	# alive after a failure would deadlock every following test case.
	with lock:
		mf = NonblockingMecabFeatures()
		Mecab_analysis(s, mf, logwrite_=__print)
		Mecab_print(mf, logwrite_=__print_dummy)
		Mecab_correctFeatures(mf)
		Mecab_print(mf, logwrite_=__print_dummy)
		Mecab_print(mf)
		reading = Mecab_get_reading(mf)
		mf = None
	return reading


# Sample word from jtusr.csv: 12 characters, analyzed as several
# morphemes by the base dictionary and as a single morpheme when the
# user dictionary is loaded.
USER_DIC_TEST_TEXT = "次世代型点字ピンディスプレイ"


def analyze(msg):
	"""Return (morpheme count, reading, braille) for msg with the current dictionaries."""
	s = text2mecab(msg)
	with lock:
		mf = NonblockingMecabFeatures()
		Mecab_analysis(s, mf, logwrite_=__print)
		Mecab_correctFeatures(mf)
		size = mf.size
		reading, braille = Mecab_get_reading(mf)
		mf = None
	return size, reading, braille


def probeUserDic():
	"""Analyze USER_DIC_TEST_TEXT with and without the user dictionary.

	Builds jtusr.dic first (strict: raises when the x64 mecab-dict-index.exe
	or the runtime dictionary is missing). Returns a dict with "base" and
	"user" keys, each holding the analyze() tuple.
	"""
	dics = build_userdic.ensure_user_dic(strict=True)
	__print(f"probeUserDic: initializing MeCab without user dictionaries: {jt_dir}, {dic}")
	Mecab_initialize(__print, str(jt_dir), str(dic))
	base = analyze(USER_DIC_TEST_TEXT)
	__print(f"probeUserDic: initializing MeCab with user dictionaries: {dics}")
	Mecab_initialize(__print, str(jt_dir), str(dic), dics)
	user = analyze(USER_DIC_TEST_TEXT)
	return {"base": base, "user": user}


def runTasks(enableUserDic=False):
	# Mecab_initialize rebuilds the process-global tagger when the requested
	# dictionary configuration differs from the current one. In jpSmokeTests,
	# test_translator2 (user_dics) runs before this class (MecabTests is last),
	# so runTasks(False) must switch back to the base dictionary explicitly.
	if enableUserDic:
		# All harness tasks must also pass with the user dictionary loaded;
		# the user dictionary is required here (strict) so that a broken or
		# missing jtusr.dic cannot silently degrade this run to the base
		# dictionary. Whether the entry is actually selected is verified by
		# probeUserDic().
		user_dics = build_userdic.ensure_user_dic(strict=True)
		user_dics_str = ", ".join(map(str, user_dics)) if user_dics else "None"
		__print(f"Initializing MeCab with user dictionaries: {jt_dir}, {dic}, {user_dics_str}")
		Mecab_initialize(__print, str(jt_dir), str(dic), user_dics)
	else:
		__print(f"Initializing MeCab: {jt_dir}, {dic}")
		Mecab_initialize(__print, str(jt_dir), str(dic))
	count = 0
	for i in tasks:
		if isinstance(i, dict):
			if "braille" in i:
				if "speech" in i:
					item = [i["text"], i["speech"], i["braille"]]
				else:
					s = i["braille"].replace(" ", "").replace("/", "")
					item = [i["text"], s, i["braille"]]
			elif "input" in i:
				if "speech" in i:
					item = [i["text"], i["speech"], i["input"]]
				else:
					s = i["input"].replace(" ", "").replace("/", "")
					item = [i["text"], s, i["input"]]
			elif "text" in i and "speech" in i:
				item = [i["text"], i["speech"]]
			else:
				continue
		else:
			item = i
		clear_morph_buffer()
		result = get_reading(item[0])
		if item[1] is not None and item[1] and result[0] != item[1]:
			__print("input:    " + item[0])
			__print("reading expected: " + item[1])
			__print("reading result:   " + result[0])
			print_morph_buffer()
			count += 1
		if len(item) > 2 and item[2] and result[1] != item[2]:
			__print("input:            " + item[0])
			__print("braille expected: " + item[2])
			__print("braille result:   " + result[1])
			print_morph_buffer()
			count += 1

	return count


if __name__ == "__main__":
	runTasks(enableUserDic=True)
