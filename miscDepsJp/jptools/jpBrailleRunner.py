# -*- coding: utf-8 -*-
# jptools/jpBrailleRunner.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2013 Masataka.Shinke, Takuya Nishimoto
# translator2: MeCab・マスあけ・引用符範囲（パイプライン1番目）
# translator1: カナと記号のテスト（パイプライン3番目）。2番目は translator_louis

import datetime
import io
import optparse
import os
import sys
import timeit
from pathlib import Path

from harness import tests
from nabccHarness import tests as nabcc_tests
from eng2Harness import eng2_tests

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
import translator1  # type: ignore
import translator2  # type: ignore
import mecab as mecab_module  # type: ignore

import build_userdic

dic_dir = jtalk_dir / "dic"
# Build jtusr.dic against the current sys.dic and load it, instead of the
# cwd-dependent glob in jtalkDir (the harness has no task that needs the
# user dictionary; loading it here verifies it does not change results).
user_dics = build_userdic.ensure_user_dic()


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


def run_translator1():
	"""translator1（カナ→点字）のテスト。パイプラインでは3番目に実行される。"""
	global output
	outfile = "__translator1output.txt"
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
		print("translator1: %d error(s). see %s" % (count, outfile))
	return (count, outfile)


def run_translator2(verboseMode=False):
	"""translator2（MeCab・マスあけ・引用符範囲）のテスト。パイプラインでは1番目に実行される。"""
	global output
	outfile = "__translator2output.txt"
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
						error_details_parts.append(
							f"inpos2: expected '{correct_inpos2}', got '{result_inpos2}'",
						)
					if "inpos_mismatch" in error_types:
						error_details_parts.append(f"inpos: expected '{correct_inpos}', got '{result_inpos}'")
					if "outpos_mismatch" in error_types:
						error_details_parts.append(
							f"outpos: expected '{correct_outpos}', got '{result_outpos}'",
						)
					error_details = " | ".join(error_details_parts)

					# Output GitHub Actions error annotation
					# Escape special characters in error message for GitHub Actions
					error_msg = (
						f"Test #{count} ({', '.join(error_types)}): text='{t['text']}' | {error_details}"
					)
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
			print(f"\ntranslator2: {count} error(s) found. Details written to: {outfile_path}")
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
			print(f"\ntranslator2: All tests passed. Output written to: {outfile_path}")
	return (count, outfile)


def run_eng2_grade1():
	"""eng2Harness の1級点字を検証。原文 → translator2 → translator1 の結果と output を比較。"""
	global output
	outfile = "__eng2output.txt"
	with open_file(outfile, "w") as f:
		# translator2 の初期化（MeCab が必要）
		dll_dir_handle = None
		if hasattr(os, "add_dll_directory"):
			try:
				dll_dir_handle = os.add_dll_directory(str(jtalk_dir))
			except OSError:
				pass
		try:
			output = io.StringIO()
			try:
				translator2.initialize(__print, str(jtalk_dir), str(dic_dir), user_dics)
			except OSError as e:
				f.write("ERROR: MeCab DLL load failed: %s\n" % e)
				return (1, outfile)
			finally:
				output.close()
		finally:
			if dll_dir_handle is not None:
				dll_dir_handle.close()

		if mecab_module.libmc is None or mecab_module.mecab is None:
			f.write("ERROR: MeCab not initialized. Run test_translator2 first or check environment.\n")
			return (1, outfile)

		count = 0
		for idx, t in enumerate(eng2_tests):
			if "note" in t and "text" not in t:
				continue
			if "output" not in t or "text" not in t:
				continue
			# 既知の失敗・未実装: _output があるケースは 1 級検証をスキップ（スキップ規約）
			if "_output" in t:
				continue
			output = io.StringIO()
			try:
				result, pat, inpos1, inpos2 = translator2.translateWithInPos2(
					t["text"], logwrite=__print, nabcc=False, use_foreign_quotes=True,
				)
			except Exception as e:
				count += 1
				f.write("ERROR #%d: text=%r exception=%s\n\n" % (idx, t["text"], e))
				continue
			finally:
				output.close()
			braille_result, _ = translator1.translateWithInPos(result, nabcc=False)
			if braille_result != t["output"]:
				count += 1
				f.write("text   : %s\n" % t["text"])
				f.write("correct: %s\n" % t["output"])
				f.write("result : %s\n" % braille_result)
				if "comment" in t:
					f.write(
						"comment: %s\n"
						% (t["comment"] if isinstance(t["comment"], str) else ", ".join(t["comment"])),
					)
				f.write("\n")
		print("eng2_grade1: %d error(s). see %s" % (count, outfile))
	return (count, outfile)


# translator_louis 単体テスト用: 英文 → liblouis en-ueb-g2.ctb の期待値（引用符なし）
# UEB G2: 大文字符 ⠠、縮約（world→⠸⠺ 等）は liblouis の実際の出力に合わせる
TRANSLATOR_LOUIS_CASES = [
	{"text": "and", "ueb_g2": "⠯"},
	{"text": "the", "ueb_g2": "⠮"},
	{"text": "Hello world", "ueb_g2": "⠠⠓⠑⠇⠇⠕ ⠸⠺"},  # 大文字符 + world 縮約
	{"text": "what's new", "ueb_g2": "⠱⠁⠞⠄⠎ ⠝⠑⠺"},
	{"text": "tea room", "ueb_g2": "⠞⠑⠁ ⠗⠕⠕⠍"},
	{"text": "correct, and", "ueb_g2": "⠉⠕⠗⠗⠑⠉⠞⠂ ⠯"},
]


def run_translator_louis():
	"""translator_louis 単体: liblouis en-ueb-g2.ctb で英文を UEB Grade 2 に変換し期待値と比較。
	louis が未ビルドの場合はスキップ（0 件で成功）。"""
	outfile = "__translator_louis_output.txt"
	try:
		from translator_louis_runner import translate_english_ueb_g2, is_louis_available
	except ImportError:
		with open_file(outfile, "w") as f:
			f.write("translator_louis_runner not found\n")
		print("translator_louis: skipped (runner not found)")
		return (0, outfile)
	if not is_louis_available():
		with open_file(outfile, "w") as f:
			f.write("louis not available (scons source required for source/louis/tables and liblouis.dll)\n")
		print("translator_louis: skipped (louis not available, run scons source)")
		return (0, outfile)
	count = 0
	with open_file(outfile, "w") as f:
		for t in TRANSLATOR_LOUIS_CASES:
			text = t["text"]
			expected = t["ueb_g2"]
			result = translate_english_ueb_g2(text)
			if result is None:
				count += 1
				f.write("text: %r -> translate failed\n" % text)
				continue
			if result != expected:
				count += 1
				f.write("text   : %s\n" % text)
				f.write("correct: %s\n" % expected)
				f.write("result : %s\n" % result)
				f.write("\n")
	if count > 0:
		print("translator_louis: %d error(s). see %s" % (count, outfile))
	else:
		print("translator_louis: all %d passed." % len(TRANSLATOR_LOUIS_CASES))
	return (count, outfile)


def run_eng2_ueb_g2():
	"""eng2Harness の UEB 2級点字を検証。原文 → translator2(louis) → translator1 の結果と ueb_g2 を比較。
	louis が未ビルドの場合はスキップ（0 件で成功）。"""
	global output
	outfile = "__eng2_ueb_g2_output.txt"
	try:
		from translator_louis_runner import get_louis_translate_for_pipeline, is_louis_available
	except ImportError:
		with open_file(outfile, "w") as f:
			f.write("translator_louis_runner not found\n")
		print("eng2_ueb_g2: skipped (runner not found)")
		return (0, outfile)
	if not is_louis_available():
		with open_file(outfile, "w") as f:
			f.write("louis not available (scons source required)\n")
		print("eng2_ueb_g2: skipped (louis not available)")
		return (0, outfile)
	louisTranslate, louisTableList = get_louis_translate_for_pipeline()
	if louisTranslate is None or not louisTableList:
		print("eng2_ueb_g2: skipped (louis not available)")
		return (0, outfile)

	with open_file(outfile, "w") as f:
		dll_dir_handle = None
		if hasattr(os, "add_dll_directory"):
			try:
				dll_dir_handle = os.add_dll_directory(str(jtalk_dir))
			except OSError:
				pass
		try:
			output = io.StringIO()
			try:
				translator2.initialize(__print, str(jtalk_dir), str(dic_dir), user_dics)
			except OSError as e:
				f.write("ERROR: MeCab DLL load failed: %s\n" % e)
				return (1, outfile)
			finally:
				output.close()
		finally:
			if dll_dir_handle is not None:
				dll_dir_handle.close()

		if mecab_module.libmc is None or mecab_module.mecab is None:
			f.write("ERROR: MeCab not initialized.\n")
			return (1, outfile)

		count = 0
		for idx, t in enumerate(eng2_tests):
			if "note" in t and "text" not in t:
				continue
			if "ueb_g2" not in t or "text" not in t:
				continue
			if "_ueb_g2" in t:
				continue
			output = io.StringIO()
			try:
				outbuf, result, inpos1, inpos2 = translator2.translateWithInPos2(
					t["text"],
					logwrite=__print,
					nabcc=False,
					louisTranslate=louisTranslate,
					louisTableList=louisTableList,
					use_foreign_quotes=True,
				)
			except Exception as e:
				count += 1
				f.write("ERROR #%d: text=%r exception=%s\n\n" % (idx, t["text"], e))
				continue
			finally:
				output.close()
			# result は既に translator1 通過済みの最終点字
			inpos, outpos_ = translator2.mergePositionMap(inpos1, inpos2, len(result), len(t["text"]))
			outpos = translator2.makeOutPos(inpos, len(t["text"]), len(result))
			is_error = False
			if result != t["ueb_g2"]:
				is_error = True
			if "ueb_g2_inpos2" in t:
				correct_inpos2 = ",".join("%d" % n for n in t["ueb_g2_inpos2"])
				result_inpos2 = ",".join("%d" % n for n in inpos2)
				if result_inpos2 != correct_inpos2:
					is_error = True
			if "ueb_g2_inpos" in t:
				correct_inpos = ",".join("%d" % n for n in t["ueb_g2_inpos"])
				result_inpos = ",".join("%d" % n for n in inpos)
				if result_inpos != correct_inpos:
					is_error = True
			if "ueb_g2_outpos" in t:
				correct_outpos = ",".join("%d" % n for n in t["ueb_g2_outpos"])
				result_outpos = ",".join("%d" % n for n in outpos)
				if result_outpos != correct_outpos:
					is_error = True
			if is_error:
				count += 1
				f.write("text   : %s\n" % t["text"])
				if result != t["ueb_g2"]:
					f.write("correct: %s\n" % t["ueb_g2"])
					f.write("result : %s\n" % result)
				if "ueb_g2_inpos2" in t and ",".join("%d" % n for n in inpos2) != ",".join("%d" % n for n in t["ueb_g2_inpos2"]):
					f.write("correct_inpos2: %s\n" % ",".join("%d" % n for n in t["ueb_g2_inpos2"]))
					f.write("result_inpos2: %s\n" % ",".join("%d" % n for n in inpos2))
				if "ueb_g2_inpos" in t and ",".join("%d" % n for n in inpos) != ",".join("%d" % n for n in t["ueb_g2_inpos"]):
					f.write("correct_inpos: %s\n" % ",".join("%d" % n for n in t["ueb_g2_inpos"]))
					f.write("result_inpos: %s\n" % ",".join("%d" % n for n in inpos))
				if "ueb_g2_outpos" in t and ",".join("%d" % n for n in outpos) != ",".join("%d" % n for n in t["ueb_g2_outpos"]):
					f.write("correct_outpos: %s\n" % ",".join("%d" % n for n in t["ueb_g2_outpos"]))
					f.write("result_outpos: %s\n" % ",".join("%d" % n for n in outpos))
				if "comment" in t:
					f.write(
						"comment: %s\n"
						% (t["comment"] if isinstance(t["comment"], str) else ", ".join(t["comment"])),
					)
				f.write("\n")
		print("eng2_ueb_g2: %d error(s). see %s" % (count, outfile))
	return (count, outfile)


def run_eng2_us_g2():
	"""eng2Harness の US 2級点字を検証。原文 → translator2(louis en-us-g2) → translator1 の結果と us_g2 を比較。
	louis が未ビルドの場合はスキップ（0 件で成功）。"""
	global output
	outfile = "__eng2_us_g2_output.txt"
	try:
		from translator_louis_runner import get_louis_translate_for_pipeline, is_louis_available
	except ImportError:
		with open_file(outfile, "w") as f:
			f.write("translator_louis_runner not found\n")
		print("eng2_us_g2: skipped (runner not found)")
		return (0, outfile)
	if not is_louis_available():
		with open_file(outfile, "w") as f:
			f.write("louis not available (scons source required)\n")
		print("eng2_us_g2: skipped (louis not available)")
		return (0, outfile)
	louisTranslate, louisTableList = get_louis_translate_for_pipeline("us")
	if louisTranslate is None or not louisTableList:
		print("eng2_us_g2: skipped (louis not available)")
		return (0, outfile)

	with open_file(outfile, "w") as f:
		dll_dir_handle = None
		if hasattr(os, "add_dll_directory"):
			try:
				dll_dir_handle = os.add_dll_directory(str(jtalk_dir))
			except OSError:
				pass
		try:
			output = io.StringIO()
			try:
				translator2.initialize(__print, str(jtalk_dir), str(dic_dir), user_dics)
			except OSError as e:
				f.write("ERROR: MeCab DLL load failed: %s\n" % e)
				return (1, outfile)
			finally:
				output.close()
		finally:
			if dll_dir_handle is not None:
				dll_dir_handle.close()

		if mecab_module.libmc is None or mecab_module.mecab is None:
			f.write("ERROR: MeCab not initialized.\n")
			return (1, outfile)

		count = 0
		for idx, t in enumerate(eng2_tests):
			if "note" in t and "text" not in t:
				continue
			if "us_g2" not in t or "text" not in t:
				continue
			if "_us_g2" in t:
				continue
			output = io.StringIO()
			try:
				outbuf, result, inpos1, inpos2 = translator2.translateWithInPos2(
					t["text"],
					logwrite=__print,
					nabcc=False,
					louisTranslate=louisTranslate,
					louisTableList=louisTableList,
					use_foreign_quotes=True,
				)
			except Exception as e:
				count += 1
				f.write("ERROR #%d: text=%r exception=%s\n\n" % (idx, t["text"], e))
				continue
			finally:
				output.close()
			inpos, outpos_ = translator2.mergePositionMap(inpos1, inpos2, len(result), len(t["text"]))
			outpos = translator2.makeOutPos(inpos, len(t["text"]), len(result))
			is_error = False
			if result != t["us_g2"]:
				is_error = True
			if "us_g2_inpos2" in t:
				correct_inpos2 = ",".join("%d" % n for n in t["us_g2_inpos2"])
				result_inpos2 = ",".join("%d" % n for n in inpos2)
				if result_inpos2 != correct_inpos2:
					is_error = True
			if "us_g2_inpos" in t:
				correct_inpos = ",".join("%d" % n for n in t["us_g2_inpos"])
				result_inpos = ",".join("%d" % n for n in inpos)
				if result_inpos != correct_inpos:
					is_error = True
			if "us_g2_outpos" in t:
				correct_outpos = ",".join("%d" % n for n in t["us_g2_outpos"])
				result_outpos = ",".join("%d" % n for n in outpos)
				if result_outpos != correct_outpos:
					is_error = True
			if is_error:
				count += 1
				f.write("text   : %s\n" % t["text"])
				if result != t["us_g2"]:
					f.write("correct: %s\n" % t["us_g2"])
					f.write("result : %s\n" % result)
				if "us_g2_inpos2" in t and ",".join("%d" % n for n in inpos2) != ",".join("%d" % n for n in t["us_g2_inpos2"]):
					f.write("correct_inpos2: %s\n" % ",".join("%d" % n for n in t["us_g2_inpos2"]))
					f.write("result_inpos2: %s\n" % ",".join("%d" % n for n in inpos2))
				if "us_g2_inpos" in t and ",".join("%d" % n for n in inpos) != ",".join("%d" % n for n in t["us_g2_inpos"]):
					f.write("correct_inpos: %s\n" % ",".join("%d" % n for n in t["us_g2_inpos"]))
					f.write("result_inpos: %s\n" % ",".join("%d" % n for n in inpos))
				if "us_g2_outpos" in t and ",".join("%d" % n for n in outpos) != ",".join("%d" % n for n in t["us_g2_outpos"]):
					f.write("correct_outpos: %s\n" % ",".join("%d" % n for n in t["us_g2_outpos"]))
					f.write("result_outpos: %s\n" % ",".join("%d" % n for n in outpos))
				if "comment" in t:
					f.write(
						"comment: %s\n"
						% (t["comment"] if isinstance(t["comment"], str) else ", ".join(t["comment"])),
					)
				f.write("\n")
		print("eng2_us_g2: %d error(s). see %s" % (count, outfile))
	return (count, outfile)


def run_eng2_nabcc_regression():
	"""nabcc+2級併用モードの回帰テスト。nabcc=True, louis, use_foreign_quotes=True で実行し、
	クラッシュせず正常終了することを検証。louis 未ビルド時はスキップ。"""
	global output
	outfile = "__eng2_nabcc_regression_output.txt"
	try:
		from translator_louis_runner import get_louis_translate_for_pipeline, is_louis_available
	except ImportError:
		with open_file(outfile, "w") as f:
			f.write("translator_louis_runner not found\n")
		print("eng2_nabcc_regression: skipped (runner not found)")
		return (0, outfile)
	if not is_louis_available():
		with open_file(outfile, "w") as f:
			f.write("louis not available (scons source required)\n")
		print("eng2_nabcc_regression: skipped (louis not available)")
		return (0, outfile)
	louisTranslate, louisTableList = get_louis_translate_for_pipeline()
	if louisTranslate is None or not louisTableList:
		print("eng2_nabcc_regression: skipped (louis not available)")
		return (0, outfile)

	MAX_CASES = 3  # 最小限の件数

	with open_file(outfile, "w") as f:
		dll_dir_handle = None
		if hasattr(os, "add_dll_directory"):
			try:
				dll_dir_handle = os.add_dll_directory(str(jtalk_dir))
			except OSError:
				pass
		try:
			output = io.StringIO()
			try:
				translator2.initialize(__print, str(jtalk_dir), str(dic_dir), user_dics)
			except OSError as e:
				f.write("ERROR: MeCab DLL load failed: %s\n" % e)
				return (1, outfile)
			finally:
				output.close()
		finally:
			if dll_dir_handle is not None:
				dll_dir_handle.close()

		if mecab_module.libmc is None or mecab_module.mecab is None:
			f.write("ERROR: MeCab not initialized.\n")
			return (1, outfile)

		count = 0
		cases_run = 0
		for idx, t in enumerate(eng2_tests):
			if cases_run >= MAX_CASES:
				break
			if "note" in t and "text" not in t:
				continue
			if "ueb_g2" not in t or "text" not in t:
				continue
			if "_ueb_g2" in t:
				continue
			output = io.StringIO()
			try:
				outbuf, result, inpos1, inpos2 = translator2.translateWithInPos2(
					t["text"],
					logwrite=__print,
					nabcc=True,
					louisTranslate=louisTranslate,
					louisTableList=louisTableList,
					use_foreign_quotes=True,
				)
			except Exception as e:
				count += 1
				f.write("ERROR #%d: text=%r exception=%s\n\n" % (idx, t["text"], e))
				cases_run += 1
				continue
			finally:
				output.close()
			cases_run += 1
			if not result or len(result) == 0:
				count += 1
				f.write("ERROR #%d: text=%r empty result\n\n" % (idx, t["text"]))
		print("eng2_nabcc_regression: %d error(s). see %s" % (count, outfile))
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
		"-2",
		"--translator2only",
		action="store_true",
		dest="translator2_only",
		default="False",
		help="translator2 only timeit",
	)
	parser.add_option(
		"-1",
		"--translator1only",
		action="store_true",
		dest="translator1_only",
		default="False",
		help="translator1 only timeit",
	)
	parser.add_option(
		"-v",
		"--verbose",
		action="store_true",
		dest="verbose",
		default="False",
		help="translator2 with verbose mode",
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
	elif options.translator2_only:
		t = timeit.Timer(stmt=run_translator2)
		print(t.timeit(number=options.number))
	elif options.translator1_only:
		t = timeit.Timer(stmt=run_translator1)
		print(t.timeit(number=options.number))
	elif options.verbose:
		run_translator2(verboseMode=True)
	else:
		run_translator2()
		run_translator1()
