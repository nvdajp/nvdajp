# Diff for: `miscDepsJp\jptools\jtalk\roma_dic_maker.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\miscDepsJp\jptools\jtalk\roma_dic_maker.py`  
**Current**: `F:\nvda\gh\alphajp\miscDepsJp\jptools\jtalk\roma_dic_maker.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtalk\\roma_dic_maker.py" "b/F:\\nvda\\gh\\alphajp\\miscDepsJp\\jptools\\jtalk\\roma_dic_maker.py"
index 3357c8d105..daf4590ee5 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtalk\\roma_dic_maker.py"
+++ "b/F:\\nvda\\gh\\alphajp\\miscDepsJp\\jptools\\jtalk\\roma_dic_maker.py"
@@ -4,7 +4,7 @@
 
 OUT_FILE = "nvdajp-roma-dic.csv"
 
-from os import path
+from pathlib import Path
 
 from alpha2mb import alpha2mb
 
@@ -341,10 +341,15 @@ def isGoodEntry(s):
 
 
 def make_dic(CODE, THISDIR):
+    # Accept both str and Path objects for compatibility
+    if isinstance(THISDIR, Path):
+        THISDIR = Path(THISDIR)
+    else:
+        THISDIR = Path(THISDIR)
     hin0 = "名詞"
     hin1 = "固有名詞"
     hin2 = "一般"
-    with open(path.join(THISDIR, OUT_FILE), "w") as file:
+    with open(str(THISDIR / OUT_FILE), "w") as file:
         ## romadic
         cost = 500.0
         step = 0.5

```