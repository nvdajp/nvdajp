# Diff for: `miscDepsJp\jptools\mecabRunner.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\miscDepsJp\jptools\mecabRunner.py`  
**Current**: `F:\nvda\gh\alphajp\miscDepsJp\jptools\mecabRunner.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\mecabRunner.py" "b/F:\\nvda\\gh\\alphajp\\miscDepsJp\\jptools\\mecabRunner.py"
index ad2c76e0d2..218b1bbb1d 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\mecabRunner.py"
+++ "b/F:\\nvda\\gh\\alphajp\\miscDepsJp\\jptools\\mecabRunner.py"
@@ -3,30 +3,39 @@
 # Japanese text processor test module
 # by Takuya Nishimoto
 
-import os
 import sys
-from os import getcwd
+from pathlib import Path
 
 from mecabHarness import tasks
 
 # Use source/synthDrivers/jtalk directly (files moved from miscDepsJp in Phase 1)
-script_dir = os.path.dirname(os.path.abspath(__file__))
+script_dir = Path(__file__).resolve().parent
 # script_dir -> miscDepsJp/jptools
 # ../.. -> repo root
-repo_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
-jt_dir = os.path.join(repo_root, "source", "synthDrivers", "jtalk")
-sys.path.insert(0, jt_dir)
+repo_root = (script_dir / ".." / "..").resolve()
+jt_dir = repo_root / "source" / "synthDrivers" / "jtalk"
+sys.path.insert(0, str(jt_dir))
 import jtalkDir  # type: ignore
 from _nvdajp_unicode import unicode_normalize  # type: ignore
 from mecab import *  # type: ignore
 
-dic = os.path.join(jt_dir, "dic")
+dic = jt_dir / "dic"
 user_dics_org = jtalkDir.user_dics_org
 user_dics = jtalkDir.user_dics
 
 
 def __print(s):
-    print(s)
+    # Write to mecab_debug.log file only (not to console)
+    # This ensures MeCab logs are only stored in logfile, not printed to console
+    try:
+        debug_log_path = Path(__file__).parent.parent.parent / "source" / "synthDrivers" / "jtalk" / "mecab_debug.log"
+        debug_log_path.parent.mkdir(parents=True, exist_ok=True)
+        with open(debug_log_path, "a", encoding="utf-8", errors="replace") as f:
+            f.write(str(s) + "\n")
+            f.flush()
+    except Exception:
+        # Logging is best-effort only. Failures must not interfere with normal operation.
+        pass
 
 
 _buffer = ""
@@ -79,11 +88,12 @@ def get_reading(msg):
 
 def runTasks(enableUserDic=False):
     if enableUserDic:
-        print(jt_dir, dic, user_dics)
-        Mecab_initialize(__print, jt_dir, dic, user_dics)
+        user_dics_str = ', '.join(map(str, user_dics)) if user_dics else 'None'
+        __print(f"Initializing MeCab with user dictionaries: {jt_dir}, {dic}, {user_dics_str}")
+        Mecab_initialize(__print, str(jt_dir), str(dic), user_dics)
     else:
-        print(jt_dir, dic)
-        Mecab_initialize(__print, jt_dir, dic)
+        __print(f"Initializing MeCab: {jt_dir}, {dic}")
+        Mecab_initialize(__print, str(jt_dir), str(dic))
     count = 0
     for i in tasks:
         if isinstance(i, dict):

```