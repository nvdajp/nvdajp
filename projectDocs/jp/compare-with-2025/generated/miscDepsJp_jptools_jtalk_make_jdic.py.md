# Diff for: `miscDepsJp\jptools\jtalk\make_jdic.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\miscDepsJp\jptools\jtalk\make_jdic.py`  
**Current**: `F:\nvda\gh\alphajp-260109\miscDepsJp\jptools\jtalk\make_jdic.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtalk\\make_jdic.py" "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\jtalk\\make_jdic.py"
index 709f80e..9233135 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtalk\\make_jdic.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\jtalk\\make_jdic.py"
@@ -7,7 +7,6 @@
 import subprocess
 from contextlib import contextmanager, redirect_stderr, redirect_stdout
 from datetime import datetime, timezone
-from os import path
 from pathlib import Path
 
 import custom_dic_maker
@@ -31,12 +30,17 @@ def _log_redirect(repo_root: Path, mode: str):
 	log_dir = repo_root / "output" / "_logs"
 	log_dir.mkdir(parents=True, exist_ok=True)
 	log_path = log_dir / "make_jdic.log"
-    with log_path.open("w", encoding="utf-8", errors="ignore") as fp, redirect_stdout(fp), redirect_stderr(fp):
+	with (
+		log_path.open("w", encoding="utf-8", errors="ignore") as fp,
+		redirect_stdout(fp),
+		redirect_stderr(fp),
+	):
 		yield log_path, fp
 
 
-def mkdir_p(path):
-    os.makedirs(path, exist_ok=True)
+def mkdir_p(path_obj):
+	"""Create directory and parents if needed."""
+	Path(path_obj).mkdir(parents=True, exist_ok=True)
 
 
 def convert_file(src_file, src_enc, dest_file, dest_enc, apply_filter=False):
@@ -57,16 +61,16 @@ def convert_file(src_file, src_enc, dest_file, dest_enc, apply_filter=False):
 
 def _main():
 	# MECAB_DICT_INDEX と OUTDIR は libopenjtalk/mecab-naist-jdic/_temp が基準
-    jtdir = path.dirname(path.abspath(__file__))
-    engdic = path.normpath(path.join(jtdir, "bep-eng.dic"))
-    cs_file = path.normpath(path.join(jtdir, "characters-ja.dic"))
+	jtdir = Path(__file__).resolve().parent
+	engdic = jtdir / "bep-eng.dic"
+	cs_file = jtdir / "characters-ja.dic"
 
-    thisdir = path.normpath(path.join(jtdir, "libopenjtalk", "mecab-naist-jdic"))
+	thisdir = jtdir / "libopenjtalk" / "mecab-naist-jdic"
 	# Build output directly under source/ to avoid extra copy in jtalkSync.
-    repo_root = Path(path.normpath(path.join(jtdir, "..", "..", "..")))
-    outdir = path.normpath(path.join(repo_root, "source", "synthDrivers", "jtalk", "dic"))
-    tempdir = path.normpath(path.join(thisdir, "_temp"))
-    mecab_dict_index = path.normpath(path.join(thisdir, "..", "mecab", "src", "mecab-dict-index.exe"))
+	repo_root = (jtdir / ".." / ".." / "..").resolve()
+	outdir = repo_root / "source" / "synthDrivers" / "jtalk" / "dic"
+	tempdir = thisdir / "_temp"
+	mecab_dict_index = thisdir.parent / "mecab" / "src" / "mecab-dict-index.exe"
 	code = "utf-8"  # cp932
 
 	mode = _log_mode()
@@ -99,25 +103,26 @@ def _main():
 		jdic_file = "naist-jdic.csv"
 
 		for f in files:
-            print("copy %s to %s" % (path.join(thisdir, f), tempdir))
-            shutil.copy(path.join(thisdir, f), tempdir)
+			src_path = thisdir / f
+			print(f"copy {src_path} to {tempdir}")
+			shutil.copy(str(src_path), str(tempdir))
 
 		for f in euc_files:
-            convert_file(path.join(thisdir, f), "euc-jp", path.join(tempdir, f), code)
+			convert_file(str(thisdir / f), "euc-jp", str(tempdir / f), code)
 
 		convert_file(
-            path.join(thisdir, jdic_file),
+			str(thisdir / jdic_file),
 			"euc-jp",
-            path.join(tempdir, jdic_file),
+			str(tempdir / jdic_file),
 			code,
 			apply_filter=True,
 		)
 
-        print(tempdir, [mecab_dict_index, "-d", ".", "-o", outdir, "-f", code, "-c", code])
+		print(f"{tempdir} {[str(mecab_dict_index), '-d', '.', '-o', str(outdir), '-f', code, '-c', code]}")
 		# In console mode (log_fp is None), don't set stdout/stderr to preserve default console output
 		# In file mode (log_fp is set), redirect both stdout and stderr to the log file
 		run_kwargs = {
-            "cwd": tempdir,
+			"cwd": str(tempdir),
 			"text": True,
 			"check": True,
 		}
@@ -125,18 +130,18 @@ def _main():
 			run_kwargs["stdout"] = log_fp
 			run_kwargs["stderr"] = subprocess.STDOUT
 		subprocess.run(
-            [mecab_dict_index, "-d", ".", "-o", outdir, "-f", code, "-c", code],
+			[str(mecab_dict_index), "-d", ".", "-o", str(outdir), "-f", code, "-c", code],
 			**run_kwargs,
 		)
 
-        print("copy %s to %s" % (path.join(thisdir, "dicrc"), outdir))
-        shutil.copy(path.join(thisdir, "dicrc"), outdir)
-        dic_version_file = path.join(outdir, "DIC_VERSION")
-        print("dic version file: " + dic_version_file)
+		dicrc_src = thisdir / "dicrc"
+		print(f"copy {dicrc_src} to {outdir}")
+		shutil.copy(str(dicrc_src), str(outdir))
+		dic_version_file = outdir / "DIC_VERSION"
+		print(f"dic version file: {dic_version_file}")
 		version = f"nvdajp-jtalk-dic ({code}) {datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
 		print(version)
-        with open(dic_version_file, "w", encoding="utf-8") as f:
-            f.write(version + os.linesep)
+		dic_version_file.write_text(version + os.linesep, encoding="utf-8")
 
 	if mode == "file" and log_path:
 		print(f"make_jdic: output suppressed; see {log_path}")

```