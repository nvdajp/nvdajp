# Diff for: `miscDepsJp\jptools\jtalkPredicTest.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\miscDepsJp\jptools\jtalkPredicTest.py`  
**Current**: `F:\nvda\gh\alphajp-260109\miscDepsJp\jptools\jtalkPredicTest.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtalkPredicTest.py" "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\jtalkPredicTest.py"
index e67676d..9e7a858 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtalkPredicTest.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\jtalkPredicTest.py"
@@ -1,16 +1,16 @@
 # jtalkPredicTest.py
 # -*- coding: utf-8 -*-
 
-import os
 import sys
+from pathlib import Path
 
 # Use source/synthDrivers/jtalk directly (files moved from miscDepsJp in Phase 1)
-script_dir = os.path.dirname(os.path.abspath(__file__))
+script_dir = Path(__file__).resolve().parent
 # script_dir -> miscDepsJp/jptools
 # ../.. -> repo root
-repo_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
-jtalk_dir = os.path.join(repo_root, "source", "synthDrivers", "jtalk")
-sys.path.insert(0, jtalk_dir)
+repo_root = (script_dir / ".." / "..").resolve()
+jtalk_dir = repo_root / "source" / "synthDrivers" / "jtalk"
+sys.path.insert(0, str(jtalk_dir))
 import jtalkPrepare  # type: ignore
 from _nvdajp_unicode import unicode_normalize  # type: ignore
 
@@ -87,10 +87,7 @@ def runTasks():
 		normalized = unicode_normalize(msg)
 		s = jtalkPrepare.convert(normalized)
 		if item[1] != s:
-            _print(
-                "input:%s normalized:%s result:%s expected:%s"
-                % (msg, normalized, s, item[1])
-            )
+			_print("input:%s normalized:%s result:%s expected:%s" % (msg, normalized, s, item[1]))
 			count += 1
 	return count
 

```