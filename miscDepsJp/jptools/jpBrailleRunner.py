# -*- coding: utf-8 -*-
# jptools/jpBrailleRunner.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2013 Masataka.Shinke, Takuya Nishimoto
# h1: カナと記号のテスト
# h2: テキスト解析とマスあけのテスト

import datetime
import io
import optparse
import os
import sys
import timeit
from pathlib import Path

from harness import tests
from nabccHarness import tests as nabcc_tests

tests.extend(nabcc_tests)

open_file = lambda name, mode: open(name, mode, encoding="utf-8")

# Use __file__ to get the script's directory, which is more reliable than getcwd()
# jpBrailleRunner.py is in miscDepsJp/jptools
script_dir = Path(__file__).resolve().parent
# script_dir -> miscDepsJp/jptools
# ../.. -> repo root
repo_root = (script_dir / ".." / "..").resolve()
# Verify repo_root contains miscDepsJp
if not (repo_root / "miscDepsJp").exists():
	# Fallback: try going up one more level if current calculation is wrong
	repo_root = (script_dir / ".." / ".." / "..").resolve()
jtalk_dir = repo_root / "source" / "synthDrivers" / "jtalk"
# Use source/synthDrivers/jtalk directly (files moved from miscDepsJp in Phase 1)
# Remove any existing occurrence to ensure correct import path
jtalk_dir_str = str(jtalk_dir)
if jtalk_dir_str in sys.path:
	sys.path.remove(jtalk_dir_str)
sys.path.insert(0, jtalk_dir_str)
import jtalkDir  # type: ignore
import translator1  # type: ignore
import translator2  # type: ignore
import mecab as mecab_module  # type: ignore

dic_dir = jtalk_dir / "dic"
user_dics = jtalkDir.user_dics


def __write(file, s=""):
	file.write(s)


def __writeln(file, s=""):
	file.write(s + "\n")


output = None


def __print(s=""):
	global output
	# Write to mecab_debug.log file only (not to console)
	# This ensures MeCab logs are only stored in logfile, not printed to console
	try:
		# Calculate path to mecab_debug.log relative to repo root
		script_dir = Path(__file__).resolve().parent
		# script_dir -> miscDepsJp/jptools
		# ../.. -> repo root
		repo_root = (script_dir / ".." / "..").resolve()
		debug_log_path = repo_root / "source" / "synthDrivers" / "jtalk" / "mecab_debug.log"
		debug_log_path.parent.mkdir(parents=True, exist_ok=True)
		with open(debug_log_path, "a", encoding="utf-8", errors="replace") as f:
			f.write(str(s) + "\n")
			f.flush()
	except Exception:
		# Logging is best-effort only. Failures must not interfere with normal operation.
		pass
	# Also write to output buffer for test result collection (if output is set)
	if output is not None:
		try:
			output.write(str(s) + "\n")
		except Exception:
			# Output buffer writing is best-effort only.
			pass


def dot_numbers(s):
	ret = []
	for c in s:
		code = ord(c)
		if code == 0x20 or code == 0x2800:
			ret.append("0")
		elif 0x2801 <= code and code <= 0x28FF:
			ar = []
			if code & 0x01:
				ar.append("1")
			if code & 0x02:
				ar.append("2")
			if code & 0x04:
				ar.append("3")
			if code & 0x08:
				ar.append("4")
			if code & 0x10:
				ar.append("5")
			if code & 0x20:
				ar.append("6")
			if code & 0x40:
				ar.append("7")
			if code & 0x80:
				ar.append("8")
			ret.append("".join(ar))
	return " ".join(ret)


def pass1():
	global output
	outfile = "__h1output.txt"
	with open_file(outfile, "w") as f:
		count = 0
		for t in tests:
			nabcc = False
			if t.get("mode") == "NABCC":
				nabcc = True
			if "output" in t:
				result, inpos1 = translator1.translateWithInPos(t["input"], nabcc=nabcc)
				if "inpos1" in t:
					correct_inpos1 = ",".join(["%d" % n for n in t["inpos1"]])
				else:
					correct_inpos1 = None
				result_inpos1 = ",".join(["%d" % n for n in inpos1])
				if (
					result != t["output"]
					or (correct_inpos1 and result_inpos1 != correct_inpos1)
					or (len(result) != len(inpos1))
				):
					count += 1
					f.write("input: " + t["input"] + "\n")
					f.write("result: " + result + "\n")
					f.write("correct: " + t["output"] + "\n")
					if correct_inpos1:
						f.write("correct_inpos1: " + correct_inpos1 + "\n")
					f.write("result_inpos1: " + result_inpos1 + "\n")
					if "comment" in t:
						if isinstance(t["comment"], str):
							f.write("comment: " + t["comment"] + "\n")
						else:
							f.write("comment: " + ", ".join(t["comment"]) + "\n")
					f.write("\n")
		print("h1: %d error(s). see %s" % (count, outfile))
	return (count, outfile)


def pass2(verboseMode=False):
	global output
	outfile = "__h2output.txt"
	with open_file(outfile, "w") as f:
		# Display environment info (GitHub Actions compatible)
		print("::group::Test Environment")
		try:
			import ctypes

			code_page_acp = ctypes.windll.kernel32.GetACP()
			print(f"  Code page (GetACP): {code_page_acp}")
		except Exception:
			print("  Code page (GetACP): <unavailable>")
		try:
			import subprocess
			import locale

			# Get console code page (chcp output is in console encoding, not UTF-8)
			# Use GetACP() result if available, otherwise try chcp with proper encoding
			try:
				chcp_result = subprocess.run(
					["chcp"],
					capture_output=True,
					text=False,  # Get bytes first
					shell=True,
				)
				# Try to decode with console encoding (usually cp932 on Japanese Windows)
				console_encoding = locale.getpreferredencoding()
				if chcp_result.stdout:
					chcp_output = chcp_result.stdout.decode(console_encoding, errors="replace").strip()
				else:
					chcp_output = "<unavailable>"
			except Exception:
				# Fallback: use GetACP() result if chcp fails
				chcp_output = f"{code_page_acp} (from GetACP)"
			print(f"  chcp: {chcp_output}")
		except Exception:
			print("  chcp: <unavailable>")
		print(f"  jtalk_dir: {jtalk_dir}")
		print(f"  dic_dir: {dic_dir}")
		print("::endgroup::")

		libmecab_path = jtalk_dir / "libmecab.dll"
		f.write(f"jtalk_dir: {jtalk_dir}\n")
		f.write(f"libmecab.dll exists: {libmecab_path.exists()} ({libmecab_path})\n")
		f.write(f"dic_dir exists: {dic_dir.is_dir()} ({dic_dir})\n")
		f.write("user_dics: %s\n" % (", ".join(user_dics) if user_dics else "<none>"))
		f.write("\n")

		dll_dir_handle = None
		if hasattr(os, "add_dll_directory"):
			try:
				dll_dir_handle = os.add_dll_directory(str(jtalk_dir))
				f.write("add_dll_directory: OK\n")
			except OSError as e:
				f.write(f"WARNING: add_dll_directory failed for {jtalk_dir}: {e}\n")

		output = io.StringIO()
		# jtalk_dir points to miscDepsJp/source/synthDrivers/jtalk/ where libmecab.dll is located
		try:
			translator2.initialize(__print, str(jtalk_dir), str(dic_dir), user_dics)
		except OSError as e:
			log = output.getvalue()
			output.close()
			f.write(log)
			f.write("\n")
			f.write(f"ERROR: Failed to load MeCab DLL: {e}\n")
			f.write(f"Expected libmecab.dll at: {libmecab_path}\n")
			raise RuntimeError(f"MeCab DLL load failed: {e}") from e
		finally:
			if dll_dir_handle is not None:
				dll_dir_handle.close()

		log = output.getvalue()
		output.close()
		f.write(log)
		f.write("\n")
		# Verify MeCab initialization
		if mecab_module.libmc is None or mecab_module.mecab is None:
			msg = "MeCab initialization failed: libmc=%s, mecab=%s" % (
				mecab_module.libmc,
				mecab_module.mecab,
			)
			f.write(msg + "\n")
			f.write("This will cause access violations. Aborting.\n")
			raise RuntimeError(msg)
		count = 0
		error_summary = {
			"result_mismatch": 0,
			"inpos2_mismatch": 0,
			"inpos_mismatch": 0,
			"outpos_mismatch": 0,
		}
		for idx, t in enumerate(tests):
			if "input" not in t:
				continue
			nabcc = False
			if t.get("mode") == "NABCC":
				nabcc = True
			if "text" in t:
				# Log current test context before translation for crash forensics.
				f.write(f"Running test index {idx}\n")
				f.write(f"text: {t['text']!r}\n")
				f.write(f"input: {t.get('input')!r}\n")
				f.flush()
				output = io.StringIO()
				result, pat, inpos1, inpos2 = translator2.translateWithInPos2(
					t["text"],
					logwrite=__print,
					nabcc=nabcc,
				)
				log = output.getvalue()
				output.close()
				# inpos2
				if "inpos2" in t:
					correct_inpos2 = ",".join(["%d" % n for n in t["inpos2"]])
				else:
					correct_inpos2 = None
				# inpos1
				if "inpos1" in t:
					correct_inpos1 = ",".join(["%d" % n for n in t["inpos1"]])
				else:
					correct_inpos1 = None
				# merged inpos
				inpos, outpos_ = translator2.mergePositionMap(inpos1, inpos2, len(pat), len(t["text"]))
				# outpos
				outpos = translator2.makeOutPos(inpos, len(t["text"]), len(pat))

				if "inpos" in t:
					correct_inpos = ",".join(["%d" % n for n in t["inpos"]])
				else:
					correct_inpos = None
				if "outpos" in t:
					correct_outpos = ",".join(["%d" % n for n in t["outpos"]])
				else:
					correct_outpos = None
				# result
				result_inpos2 = ",".join(["%d" % n for n in inpos2])
				result_inpos1 = ",".join(["%d" % n for n in inpos1])
				result_inpos = ",".join(["%d" % n for n in inpos])
				result_outpos = ",".join(["%d" % n for n in outpos])
				# output
				isError = False
				error_types = []
				if result != t["input"]:
					isError = True
					error_types.append("result_mismatch")
					error_summary["result_mismatch"] += 1
				if correct_inpos2 and result_inpos2 != correct_inpos2:
					isError = True
					error_types.append("inpos2_mismatch")
					error_summary["inpos2_mismatch"] += 1
				if correct_inpos and result_inpos != correct_inpos:
					isError = True
					error_types.append("inpos_mismatch")
					error_summary["inpos_mismatch"] += 1
				if correct_outpos and result_outpos != correct_outpos:
					isError = True
					error_types.append("outpos_mismatch")
					error_summary["outpos_mismatch"] += 1
				if isError:
					count += 1
					# Build error details for console output and GitHub Actions annotation
					error_details_parts = []
					if "result_mismatch" in error_types:
						error_details_parts.append(f"result: expected '{t['input']}', got '{result}'")
					if "inpos2_mismatch" in error_types:
						error_details_parts.append(f"inpos2: expected '{correct_inpos2}', got '{result_inpos2}'")
					if "inpos_mismatch" in error_types:
						error_details_parts.append(f"inpos: expected '{correct_inpos}', got '{result_inpos}'")
					if "outpos_mismatch" in error_types:
						error_details_parts.append(f"outpos: expected '{correct_outpos}', got '{result_outpos}'")
					error_details = " | ".join(error_details_parts)

					# Output GitHub Actions error annotation
					# Escape special characters in error message for GitHub Actions
					error_msg = f"Test #{count} ({', '.join(error_types)}): text='{t['text']}' | {error_details}"
					# Replace newlines and other special chars that might break annotation
					error_msg_escaped = error_msg.replace("\n", " ").replace("\r", " ")
					print(f"::error file={outfile}::{error_msg_escaped}")

					# Output detailed error to console for immediate visibility
					print(f"\n=== ERROR #{count}: {', '.join(error_types)} ===")
					print(f"text   : {t['text']}")
					print(f"correct: {t['input']}")
					print(f"result : {result}")
					print(f"pat    : {pat}")
					if correct_inpos2:
						print(f"cor_in2: {correct_inpos2}")
					if correct_inpos1:
						print(f"cor_in1: {correct_inpos1}")
					if correct_inpos:
						print(f"cor_in : {correct_inpos}")
					if correct_outpos:
						print(f"cor_out: {correct_outpos}")
					print(f"res_in2: {result_inpos2}")
					print(f"res_in1: {result_inpos1}")
					print(f"res_in : {result_inpos}")
					print(f"res_out: {result_outpos}")
					if "comment" in t and t["comment"]:
						if isinstance(t["comment"], str):
							print(f"comment: {t['comment']}")
						else:
							print(f"comment: {', '.join(t['comment'])}")
					print()  # Empty line for readability
				if isError or verboseMode:
					if isError:
						f.write(f"=== ERROR #{count}: {', '.join(error_types)} ===\n")
					f.write("text   : " + t["text"] + "\n")
					f.write("correct: " + t["input"] + "\n")
					f.write("result : " + result + "\n")
					f.write("pat    : " + pat + "\n")
					if correct_inpos2:
						f.write("cor_in2: " + correct_inpos2 + "\n")
					if correct_inpos1:
						f.write("cor_in1: " + correct_inpos1 + "\n")
					if correct_inpos:
						f.write("cor_in : " + correct_inpos + "\n")
					if correct_outpos:
						f.write("cor_out: " + correct_outpos + "\n")
					f.write("res_in2: " + result_inpos2 + "\n")
					f.write("res_in1: " + result_inpos1 + "\n")
					f.write("res_in : " + result_inpos + "\n")
					f.write("res_out: " + result_outpos + "\n")
					if "comment" in t and t["comment"]:
						if isinstance(t["comment"], str):
							f.write("comment: " + t["comment"] + "\n")
						else:
							f.write("comment: " + ", ".join(t["comment"]) + "\n")
					f.write("\n")
					f.write(log)
					f.write("\n")
		# Write error summary
		if count > 0:
			f.write("=" * 60 + "\n")
			f.write("ERROR SUMMARY\n")
			f.write("=" * 60 + "\n")
			f.write(f"Total errors: {count}\n")
			if error_summary["result_mismatch"] > 0:
				f.write(f"  - Result mismatch: {error_summary['result_mismatch']}\n")
			if error_summary["inpos2_mismatch"] > 0:
				f.write(f"  - inpos2 mismatch: {error_summary['inpos2_mismatch']}\n")
			if error_summary["inpos_mismatch"] > 0:
				f.write(f"  - inpos mismatch: {error_summary['inpos_mismatch']}\n")
			if error_summary["outpos_mismatch"] > 0:
				f.write(f"  - outpos mismatch: {error_summary['outpos_mismatch']}\n")
			f.write("=" * 60 + "\n")

			# Output error summary to console for immediate visibility
			print("\n" + "=" * 60)
			print("ERROR SUMMARY")
			print("=" * 60)
			print(f"Total errors: {count}")
			if error_summary["result_mismatch"] > 0:
				print(f"  - Result mismatch: {error_summary['result_mismatch']}")
			if error_summary["inpos2_mismatch"] > 0:
				print(f"  - inpos2 mismatch: {error_summary['inpos2_mismatch']}")
			if error_summary["inpos_mismatch"] > 0:
				print(f"  - inpos mismatch: {error_summary['inpos_mismatch']}")
			if error_summary["outpos_mismatch"] > 0:
				print(f"  - outpos mismatch: {error_summary['outpos_mismatch']}")
			print("=" * 60)
		outfile_path = Path(outfile).resolve()
		if count > 0:
			print(f"\nh2: {count} error(s) found. Details written to: {outfile_path}")
			print("    Error breakdown: ", end="")
			parts = []
			if error_summary["result_mismatch"] > 0:
				parts.append(f"result={error_summary['result_mismatch']}")
			if error_summary["inpos2_mismatch"] > 0:
				parts.append(f"inpos2={error_summary['inpos2_mismatch']}")
			if error_summary["inpos_mismatch"] > 0:
				parts.append(f"inpos={error_summary['inpos_mismatch']}")
			if error_summary["outpos_mismatch"] > 0:
				parts.append(f"outpos={error_summary['outpos_mismatch']}")
			print(", ".join(parts))
		else:
			print(f"\nh2: All tests passed. Output written to: {outfile_path}")
	return (count, outfile)


def make_doc():
	outfile = "__jpBrailleHarness.md"
	timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
	with open_file(outfile, "w") as f:
		__writeln(
			f,
			"""
# NVDA 日本語版 点訳テストケース """
			+ timestamp,
		)
		count = 0
		for t in tests:
			# 'note' はテストケースではなく説明の記述
			if "note" in t:
				note = t["note"]
				# "==== 見出し ====" => "##### 見出し"
				# "=== 見出し ===" => "#### 見出し"
				# "== 見出し ==" => "### 見出し"
				# "+ 見出し +" => "## 見出し"
				if note.startswith("====") and note.endswith("===="):
					note = "##### " + note[4:-4]
				elif note.startswith("===") and note.endswith("==="):
					note = "#### " + note[3:-3]
				elif note.startswith("==") and note.endswith("=="):
					note = "### " + note[2:-2]
				elif note.startswith("+") and note.endswith("+"):
					note = "## " + note[1:-1]
				__writeln(f)
				__writeln(f, note)
				__writeln(f)
				continue
			count += 1
			__writeln(f, "###### 番号: %d" % count)

			if "text" in t:
				__writeln(f, "- 日本語: " + t["text"].replace("　", "□").replace(" ", "□"))
			if "input" in t:
				__writeln(f, "- カナ表記: " + t["input"].replace(" ", "□"))
			if "output" in t:
				__writeln(f, "- 点字: " + t["output"].replace(" ", "□"))
			if "output" in t:
				__writeln(f, "- ドット番号: " + dot_numbers(t["output"]))
			if "mode" in t:
				__writeln(f, "- モード: " + t["mode"])
			if "comment" in t:
				if isinstance(t["comment"], str):
					__writeln(f, "- コメント: " + t["comment"])
				else:
					__writeln(f, "- コメント: ")
					for c in t["comment"]:
						__writeln(f, "  - " + c)
					__writeln(f, "  -")
			__writeln(f, "")


if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option(
		"-1",
		"--pass1only",
		action="store_true",
		dest="pass1_only",
		default="False",
		help="pass1 only timeit",
	)
	parser.add_option(
		"-2",
		"--pass2only",
		action="store_true",
		dest="pass2_only",
		default="False",
		help="pass2 only timeit",
	)
	parser.add_option(
		"-v",
		"--verbose",
		action="store_true",
		dest="verbose",
		default="False",
		help="pass2 with verbose mode",
	)
	parser.add_option(
		"-m",
		"--makedoc",
		action="store_true",
		dest="make_doc",
		default="False",
		help="make t2t document of harness",
	)
	parser.add_option(
		"-n",
		"--number",
		action="store",
		dest="number",
		type="int",
		default=1,
		help="number for timeit",
	)
	(options, args) = parser.parse_args()

	if options.make_doc:
		make_doc()
	elif options.pass1_only:
		t = timeit.Timer(stmt=pass1)
		print(t.timeit(number=options.number))
	elif options.pass2_only:
		t = timeit.Timer(stmt=pass2)
		print(t.timeit(number=options.number))
	elif options.verbose:
		pass2(verboseMode=True)
	else:
		pass1()
		pass2()
