# Diff for: `miscDepsJp\jptools\jtalk\eng_dic_maker.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\miscDepsJp\jptools\jtalk\eng_dic_maker.py`  
**Current**: `F:\nvda\gh\alphajp\miscDepsJp\jptools\jtalk\eng_dic_maker.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtalk\\eng_dic_maker.py" "b/F:\\nvda\\gh\\alphajp\\miscDepsJp\\jptools\\jtalk\\eng_dic_maker.py"
index c88e2936d0..2d095f2668 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtalk\\eng_dic_maker.py"
+++ "b/F:\\nvda\\gh\\alphajp\\miscDepsJp\\jptools\\jtalk\\eng_dic_maker.py"
@@ -12,12 +12,19 @@
 open_file = lambda name, mode, encoding: open(name, mode, encoding=encoding)
 
 
-from os import path
+from pathlib import Path
 
 from alpha2mb import alpha2mb
 
 
 def make_dic(IN_FILE, CODE, THISDIR):
+    # Accept both str and Path objects for compatibility
+    if isinstance(IN_FILE, Path):
+        IN_FILE = str(IN_FILE)
+    if isinstance(THISDIR, Path):
+        THISDIR = Path(THISDIR)
+    else:
+        THISDIR = Path(THISDIR)
     import re
 
     d = [
@@ -357,7 +364,7 @@ def make_dic(IN_FILE, CODE, THISDIR):
             d.append([a1, a2])
             k[a1] = True
     d.sort()
-    with open_file(path.join(THISDIR, OUT_FILE), "w", CODE) as file:
+    with open_file(str(THISDIR / OUT_FILE), "w", CODE) as file:
         for i in d:
             k = i[0]
             # skip such as SHE'LL

```