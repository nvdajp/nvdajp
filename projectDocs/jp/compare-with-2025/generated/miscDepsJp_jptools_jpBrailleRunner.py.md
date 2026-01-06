# Diff for: `miscDepsJp\jptools\jpBrailleRunner.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\miscDepsJp\jptools\jpBrailleRunner.py`  
**Current**: `F:\nvda\gh\alphajp\miscDepsJp\jptools\jpBrailleRunner.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jpBrailleRunner.py" "b/F:\\nvda\\gh\\alphajp\\miscDepsJp\\jptools\\jpBrailleRunner.py"
index ec73b788e9..e5c5d04e67 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jpBrailleRunner.py"
+++ "b/F:\\nvda\\gh\\alphajp\\miscDepsJp\\jptools\\jpBrailleRunner.py"
@@ -13,38 +13,38 @@
 import os
 import sys
 import timeit
+from pathlib import Path
 
 from harness import tests
 from nabccHarness import tests as nabcc_tests
 
 tests.extend(nabcc_tests)
 
-from os import getcwd
-
 open_file = lambda name, mode: open(name, mode, encoding="utf-8")
 
 # Use __file__ to get the script's directory, which is more reliable than getcwd()
 # jpBrailleRunner.py is in miscDepsJp/jptools
-script_dir = os.path.dirname(os.path.abspath(__file__))
+script_dir = Path(__file__).resolve().parent
 # script_dir -> miscDepsJp/jptools
 # ../.. -> repo root
-repo_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
+repo_root = (script_dir / ".." / "..").resolve()
 # Verify repo_root contains miscDepsJp
-if not os.path.exists(os.path.join(repo_root, "miscDepsJp")):
+if not (repo_root / "miscDepsJp").exists():
     # Fallback: try going up one more level if current calculation is wrong
-    repo_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
-jtalk_dir = os.path.join(repo_root, "source", "synthDrivers", "jtalk")
+    repo_root = (script_dir / ".." / ".." / "..").resolve()
+jtalk_dir = repo_root / "source" / "synthDrivers" / "jtalk"
 # Use source/synthDrivers/jtalk directly (files moved from miscDepsJp in Phase 1)
 # Remove any existing occurrence to ensure correct import path
-if jtalk_dir in sys.path:
-    sys.path.remove(jtalk_dir)
-sys.path.insert(0, jtalk_dir)
+jtalk_dir_str = str(jtalk_dir)
+if jtalk_dir_str in sys.path:
+    sys.path.remove(jtalk_dir_str)
+sys.path.insert(0, jtalk_dir_str)
 import jtalkDir  # type: ignore
 import translator1  # type: ignore
 import translator2  # type: ignore
 import mecab as mecab_module  # type: ignore
 
-dic_dir = os.path.join(jtalk_dir, "dic")
+dic_dir = jtalk_dir / "dic"
 user_dics = jtalkDir.user_dics
 
 
@@ -61,19 +61,29 @@ def __writeln(file, s=""):
 
 def __print(s=""):
     global output
-    # Also output to console for x64 smoke test debugging
-    # PYTHONUTF8=1 is set in checkJtalkArch.ps1, so print() should handle Unicode correctly
+    # Write to mecab_debug.log file only (not to console)
+    # This ensures MeCab logs are only stored in logfile, not printed to console
     try:
-        print(s, flush=True)
-    except (UnicodeEncodeError, UnicodeDecodeError):
-        # Fallback for environments without PYTHONUTF8=1
+        # Calculate path to mecab_debug.log relative to repo root
+        script_dir = Path(__file__).resolve().parent
+        # script_dir -> miscDepsJp/jptools
+        # ../.. -> repo root
+        repo_root = (script_dir / ".." / "..").resolve()
+        debug_log_path = repo_root / "source" / "synthDrivers" / "jtalk" / "mecab_debug.log"
+        debug_log_path.parent.mkdir(parents=True, exist_ok=True)
+        with open(debug_log_path, "a", encoding="utf-8", errors="replace") as f:
+            f.write(str(s) + "\n")
+            f.flush()
+    except Exception:
+        # Logging is best-effort only. Failures must not interfere with normal operation.
+        pass
+    # Also write to output buffer for test result collection (if output is set)
+    if output is not None:
         try:
-            sys.stdout.buffer.write((s + "\n").encode('utf-8', errors='replace'))
-            sys.stdout.buffer.flush()
+            output.write(str(s) + "\n")
         except Exception:
-            # If all else fails, silently skip console output
+            # Output buffer writing is best-effort only.
             pass
-    output.write(s + "\n")
 
 
 def dot_numbers(s):
@@ -133,7 +143,10 @@ def pass1():
                         f.write("correct_inpos1: " + correct_inpos1 + "\n")
                     f.write("result_inpos1: " + result_inpos1 + "\n")
                     if "comment" in t:
-                        f.write("comment: " + t["comment"] + "\n")
+                        if isinstance(t["comment"], str):
+                            f.write("comment: " + t["comment"] + "\n")
+                        else:
+                            f.write("comment: " + ", ".join(t["comment"]) + "\n")
                     f.write("\n")
         print("h1: %d error(s). see %s" % (count, outfile))
     return (count, outfile)
@@ -143,17 +156,17 @@ def pass2(verboseMode=False):
     global output
     outfile = "__h2output.txt"
     with open_file(outfile, "w") as f:
-        libmecab_path = os.path.join(jtalk_dir, "libmecab.dll")
+        libmecab_path = jtalk_dir / "libmecab.dll"
         f.write(f"jtalk_dir: {jtalk_dir}\n")
-        f.write(f"libmecab.dll exists: {os.path.exists(libmecab_path)} ({libmecab_path})\n")
-        f.write(f"dic_dir exists: {os.path.isdir(dic_dir)} ({dic_dir})\n")
+        f.write(f"libmecab.dll exists: {libmecab_path.exists()} ({libmecab_path})\n")
+        f.write(f"dic_dir exists: {dic_dir.is_dir()} ({dic_dir})\n")
         f.write("user_dics: %s\n" % (", ".join(user_dics) if user_dics else "<none>"))
         f.write("\n")
 
         dll_dir_handle = None
         if hasattr(os, "add_dll_directory"):
             try:
-                dll_dir_handle = os.add_dll_directory(jtalk_dir)
+                dll_dir_handle = os.add_dll_directory(str(jtalk_dir))
                 f.write("add_dll_directory: OK\n")
             except OSError as e:
                 f.write(f"WARNING: add_dll_directory failed for {jtalk_dir}: {e}\n")
@@ -161,7 +174,7 @@ def pass2(verboseMode=False):
         output = io.StringIO()
         # jtalk_dir points to miscDepsJp/source/synthDrivers/jtalk/ where libmecab.dll is located
         try:
-            translator2.initialize(__print, jtalk_dir, dic_dir, user_dics)
+            translator2.initialize(__print, str(jtalk_dir), str(dic_dir), user_dics)
         except OSError as e:
             log = output.getvalue()
             output.close()
@@ -188,13 +201,24 @@ def pass2(verboseMode=False):
             f.write("This will cause access violations. Aborting.\n")
             raise RuntimeError(msg)
         count = 0
-        for t in tests:
+        error_summary = {
+            "result_mismatch": 0,
+            "inpos2_mismatch": 0,
+            "inpos_mismatch": 0,
+            "outpos_mismatch": 0,
+        }
+        for idx, t in enumerate(tests):
             if "input" not in t:
                 continue
             nabcc = False
             if t.get("mode") == "NABCC":
                 nabcc = True
             if "text" in t:
+                # Log current test context before translation for crash forensics.
+                f.write(f"Running test index {idx}\n")
+                f.write(f"text: {t['text']!r}\n")
+                f.write(f"input: {t.get('input')!r}\n")
+                f.flush()
                 output = io.StringIO()
                 result, pat, inpos1, inpos2 = translator2.translateWithInPos2(
                     t["text"], logwrite=__print, nabcc=nabcc
@@ -233,15 +257,28 @@ def pass2(verboseMode=False):
                 result_outpos = ",".join(["%d" % n for n in outpos])
                 # output
                 isError = False
-                if (
-                    result != t["input"]
-                    or (correct_inpos2 and result_inpos2 != correct_inpos2)
-                    or (correct_inpos and result_inpos != correct_inpos)
-                    or (correct_outpos and result_outpos != correct_outpos)
-                ):
+                error_types = []
+                if result != t["input"]:
+                    isError = True
+                    error_types.append("result_mismatch")
+                    error_summary["result_mismatch"] += 1
+                if correct_inpos2 and result_inpos2 != correct_inpos2:
+                    isError = True
+                    error_types.append("inpos2_mismatch")
+                    error_summary["inpos2_mismatch"] += 1
+                if correct_inpos and result_inpos != correct_inpos:
+                    isError = True
+                    error_types.append("inpos_mismatch")
+                    error_summary["inpos_mismatch"] += 1
+                if correct_outpos and result_outpos != correct_outpos:
                     isError = True
+                    error_types.append("outpos_mismatch")
+                    error_summary["outpos_mismatch"] += 1
+                if isError:
                     count += 1
                 if isError or verboseMode:
+                    if isError:
+                        f.write(f"=== ERROR #{count}: {', '.join(error_types)} ===\n")
                     f.write("text   : " + t["text"] + "\n")
                     f.write("correct: " + t["input"] + "\n")
                     f.write("result : " + result + "\n")
@@ -259,11 +296,44 @@ def pass2(verboseMode=False):
                     f.write("res_in : " + result_inpos + "\n")
                     f.write("res_out: " + result_outpos + "\n")
                     if "comment" in t and t["comment"]:
-                        f.write("comment: " + t["comment"] + "\n")
+                        if isinstance(t["comment"], str):
+                            f.write("comment: " + t["comment"] + "\n")
+                        else:
+                            f.write("comment: " + ", ".join(t["comment"]) + "\n")
                     f.write("\n")
                     f.write(log)
                     f.write("\n")
-        print("h2: %d error(s). see %s" % (count, outfile))
+        # Write error summary
+        if count > 0:
+            f.write("=" * 60 + "\n")
+            f.write("ERROR SUMMARY\n")
+            f.write("=" * 60 + "\n")
+            f.write(f"Total errors: {count}\n")
+            if error_summary["result_mismatch"] > 0:
+                f.write(f"  - Result mismatch: {error_summary['result_mismatch']}\n")
+            if error_summary["inpos2_mismatch"] > 0:
+                f.write(f"  - inpos2 mismatch: {error_summary['inpos2_mismatch']}\n")
+            if error_summary["inpos_mismatch"] > 0:
+                f.write(f"  - inpos mismatch: {error_summary['inpos_mismatch']}\n")
+            if error_summary["outpos_mismatch"] > 0:
+                f.write(f"  - outpos mismatch: {error_summary['outpos_mismatch']}\n")
+            f.write("=" * 60 + "\n")
+        outfile_path = Path(outfile).resolve()
+        if count > 0:
+            print(f"h2: {count} error(s) found. Details written to: {outfile_path}")
+            print("    Error breakdown: ", end="")
+            parts = []
+            if error_summary["result_mismatch"] > 0:
+                parts.append(f"result={error_summary['result_mismatch']}")
+            if error_summary["inpos2_mismatch"] > 0:
+                parts.append(f"inpos2={error_summary['inpos2_mismatch']}")
+            if error_summary["inpos_mismatch"] > 0:
+                parts.append(f"inpos={error_summary['inpos_mismatch']}")
+            if error_summary["outpos_mismatch"] > 0:
+                parts.append(f"outpos={error_summary['outpos_mismatch']}")
+            print(", ".join(parts))
+        else:
+            print(f"h2: All tests passed. Output written to: {outfile_path}")
     return (count, outfile)
 
 
@@ -312,7 +382,7 @@ def make_doc():
             if "mode" in t:
                 __writeln(f, "- モード: " + t["mode"])
             if "comment" in t:
-                if type(t["comment"]) == str:
+                if isinstance(t["comment"], str):
                     __writeln(f, "- コメント: " + t["comment"])
                 else:
                     __writeln(f, "- コメント: ")
@@ -367,15 +437,15 @@ def make_doc():
     )
     (options, args) = parser.parse_args()
 
-    if options.make_doc == True:
+    if options.make_doc:
         make_doc()
-    elif options.pass1_only == True:
+    elif options.pass1_only:
         t = timeit.Timer(stmt=pass1)
         print(t.timeit(number=options.number))
-    elif options.pass2_only == True:
+    elif options.pass2_only:
         t = timeit.Timer(stmt=pass2)
         print(t.timeit(number=options.number))
-    elif options.verbose == True:
+    elif options.verbose:
         pass2(verboseMode=True)
     else:
         pass1()

```