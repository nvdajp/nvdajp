# Diff for: `miscDepsJp\include\python-jtalk\jtalkRunner.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\miscDepsJp\include\python-jtalk\jtalkRunner.py`  
**Current**: `F:\nvda\gh\alphajp-260109\miscDepsJp\include\python-jtalk\jtalkRunner.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\include\\python-jtalk\\jtalkRunner.py" "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\include\\python-jtalk\\jtalkRunner.py"
index 4adb48c..bf4bb86 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\include\\python-jtalk\\jtalkRunner.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\include\\python-jtalk\\jtalkRunner.py"
@@ -13,57 +13,87 @@
 import time
 import wave
 from os import getcwd
+from pathlib import Path
 
 try:
     import pyaudio
-except:
+except Exception:
     pyaudio = None  # type: ignore
 # import cProfile
 # import pstats
 # Calculate repo root (miscDepsJp's parent) and use miscDepsJp/source/synthDrivers/jtalk
 # Long-term approach: Use REPO_ROOT environment variable to avoid depending on miscDepsJp folder structure
 repo_root = os.environ.get('REPO_ROOT')
-if repo_root and os.path.isdir(repo_root):
-    repo_root = os.path.abspath(repo_root)
+if repo_root:
+    repo_root_path = Path(repo_root)
+    if repo_root_path.is_dir():
+        repo_root_path = repo_root_path.resolve()
         # Verify repo_root contains miscDepsJp (sanity check)
-    if not os.path.exists(os.path.join(repo_root, "miscDepsJp")):
+        if not (repo_root_path / "miscDepsJp").exists():
+            repo_root = None
+        else:
+            repo_root = str(repo_root_path)
+    else:
+        repo_root = None
+else:
     repo_root = None
 
 # Fallback 1: Try to get repo root from PYTHONPATH environment variable
 if repo_root is None:
     pythonpath = os.environ.get('PYTHONPATH', '')
     if pythonpath:
-        for path in pythonpath.split(os.pathsep):
-            if path and os.path.isdir(path):
+        for path_str in pythonpath.split(os.pathsep):
+            if path_str:
+                path = Path(path_str)
+                if path.is_dir():
                     # Check if this path contains miscDepsJp/include/python-jtalk
-                if path.endswith("miscDepsJp/include/python-jtalk") or path.endswith("miscDepsJp\\include\\python-jtalk"):
+                    if path_str.endswith("miscDepsJp/include/python-jtalk") or path_str.endswith("miscDepsJp\\include\\python-jtalk"):
                         # Go up two levels: miscDepsJp/include/python-jtalk -> miscDepsJp -> repo root
-                    candidate = os.path.dirname(os.path.dirname(path))
-                    if os.path.exists(os.path.join(candidate, "miscDepsJp")):
-                        repo_root = os.path.dirname(candidate)
+                        candidate = path.parent.parent
+                        if (candidate / "miscDepsJp").exists():
+                            repo_root = str(candidate.parent)
                             break
 
 # Fallback 2: Use __file__-based calculation (depends on miscDepsJp folder structure)
-if repo_root is None or not os.path.exists(os.path.join(repo_root, "miscDepsJp")):
-    script_dir = os.path.dirname(os.path.abspath(__file__))
+if repo_root is None:
+    script_dir = Path(__file__).resolve().parent
     # script_dir -> miscDepsJp/include/python-jtalk
     # ../.. -> miscDepsJp
     # ../.. -> repo root
-    repo_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
-jtalk_dir = JT_DIR = os.path.join(repo_root, "source", "synthDrivers", "jtalk")
+    repo_root_path = (script_dir / ".." / ".." / "..").resolve()
+    if (repo_root_path / "miscDepsJp").exists():
+        repo_root = str(repo_root_path)
+    else:
+        repo_root = None
+
+if repo_root is None:
+    raise RuntimeError("Could not determine repo root")
+
+repo_root_path = Path(repo_root)
+jtalk_dir = JT_DIR = repo_root_path / "source" / "synthDrivers" / "jtalk"
+JT_DIR_str = str(JT_DIR)
 # Use source/synthDrivers/jtalk directly (files moved from miscDepsJp in Phase 1)
 # Remove any existing occurrence to ensure correct import path
-if JT_DIR in sys.path:
-    sys.path.remove(JT_DIR)
-sys.path.insert(0, JT_DIR)
+if JT_DIR_str in sys.path:
+    sys.path.remove(JT_DIR_str)
+sys.path.insert(0, JT_DIR_str)
 import jtalkPrepare  # type: ignore
 from jtalkCore import *  # type: ignore
+from mecab import (  # type: ignore
+    Mecab_initialize,
+    Mecab_analysis,
+    Mecab_print,
+    Mecab_correctFeatures,
+    Mecab_utf8_to_cp932,
+    MecabFeatures,
+)
+from text2mecab import text2mecab  # type: ignore
 
-JT_DLL = os.path.abspath(os.path.join(JT_DIR, "libopenjtalk.dll"))
+JT_DLL = (JT_DIR / "libopenjtalk.dll").resolve()
 # Ensure DLL directory is in search path
 if hasattr(os, "add_dll_directory"):
     try:
-        os.add_dll_directory(JT_DIR)
+        os.add_dll_directory(JT_DIR_str)
     except OSError:
         pass  # Ignore if already added or fails
 
@@ -77,7 +107,7 @@
         "lf0_base": 5.0,
         "pitch_bias": 0,
         "speaker_attenuation": 1.0,
-        "htsvoice": os.path.join(jtalk_dir, "m001", "m001.htsvoice"),
+        "htsvoice": str(jtalk_dir / "m001" / "m001.htsvoice"),
         "alpha": 0.55,
         "beta": 0.00,
         "espeak_variant": "max",
@@ -92,7 +122,7 @@
         "pitch_bias": -25,
         "inflection_bias": -10,
         "speaker_attenuation": 0.8,
-        "htsvoice": os.path.join(jtalk_dir, "mei", "mei_happy.htsvoice"),
+        "htsvoice": str(jtalk_dir / "mei" / "mei_happy.htsvoice"),
         "alpha": 0.60,  # 0.55,
         "beta": 0.00,
         "espeak_variant": "f1",
@@ -106,7 +136,7 @@
         "lf0_base": 5.0,
         "pitch_bias": 0,
         "speaker_attenuation": 1.0,
-        "htsvoice": os.path.join(jtalk_dir, "lite", "voice.htsvoice"),
+        "htsvoice": str(jtalk_dir / "lite" / "voice.htsvoice"),
         "alpha": 0.42,
         "beta": 0.00,
         "espeak_variant": "max",
@@ -121,7 +151,7 @@
         "pitch_bias": 0,
         "inflection_bias": 0,
         "speaker_attenuation": 0.8,
-        "htsvoice": os.path.join(jtalk_dir, "tohokuf01", "tohoku-f01-neutral.htsvoice"),
+        "htsvoice": str(jtalk_dir / "tohokuf01" / "tohoku-f01-neutral.htsvoice"),
         "alpha": 0.54,
         "beta": 0.00,
         "espeak_variant": "f1",
@@ -152,6 +182,23 @@ def pa_play(data, samp_rate=16000):
 
 
 def __print(s):
+    # Write to mecab_debug.log file only (not to console)
+    # This ensures MeCab logs are only stored in logfile, not printed to console
+    try:
+        # Calculate path to mecab_debug.log relative to repo root
+        if repo_root:
+            debug_log_path = Path(repo_root) / "source" / "synthDrivers" / "jtalk" / "mecab_debug.log"
+        else:
+            # Fallback: use current directory
+            debug_log_path = Path("source") / "synthDrivers" / "jtalk" / "mecab_debug.log"
+        debug_log_path.parent.mkdir(parents=True, exist_ok=True)
+        with open(debug_log_path, "a", encoding="utf-8", errors="replace") as f:
+            f.write(str(s) + "\n")
+            f.flush()
+    except Exception:
+        # Logging is best-effort only. Failures must not interfere with normal operation.
+        pass
+    # Note: do_print flag is kept for backward compatibility, but MeCab logs are always written to file
     if do_print:
         print(s.encode("cp932", "ignore"))
 
@@ -247,7 +294,7 @@ def main(do_play=False, do_write=True, do_log=False):
     # libjt_set_beta(0.40)
     # libjt_set_gv_interpolation_weight(0, 0, 2)
     # libjt_set_gv_interpolation_weight(0, 1, 2)
-    Mecab_initialize(__print, JT_DIR, os.path.join(JT_DIR, "dic"))
+    Mecab_initialize(__print, JT_DIR_str, str(JT_DIR / "dic"))
 
     msgs = [
         "welcome to nvda",

```