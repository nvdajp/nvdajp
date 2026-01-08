# Diff for: `miscDepsJp\jptools\jtalk\tankan_dic_maker.py`

**Source**: `F:\nvda\gh\alphajp-251219\miscDepsJp\jptools\jtalk\tankan_dic_maker.py`  
**Current**: `F:\nvda\gh\alphajp-260109\miscDepsJp\jptools\jtalk\tankan_dic_maker.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtalk\\tankan_dic_maker.py" "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\jtalk\\tankan_dic_maker.py"
index db8f518..90bd27b 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtalk\\tankan_dic_maker.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\jtalk\\tankan_dic_maker.py"
@@ -10,9 +10,8 @@
 open_file = lambda name, mode, encoding: open(name, mode, encoding=encoding)
 
 
-import os
 import re
-from os import path
+from pathlib import Path
 
 
 def contains_hankaku_katakana(k):
@@ -61,12 +60,19 @@ def read_characters_file(cs_file):
 
 
 def make_dic(CODE, CS_FILE, THISDIR):
+	# Accept both str and Path objects for compatibility
+	if isinstance(CS_FILE, Path):
+		CS_FILE = str(CS_FILE)
+	if isinstance(THISDIR, Path):
+		THISDIR = Path(THISDIR)
+	else:
+		THISDIR = Path(THISDIR)
 	char_dic = read_characters_file(CS_FILE)
 	print("char_dic %d" % len(char_dic))
 	import csv
 
 	jdic_tankan = {}
-    reader = csv.reader(open_file(path.join(THISDIR, "naist-jdic.csv"), "r", "euc-jp"))
+	reader = csv.reader(open_file(str(THISDIR / "naist-jdic.csv"), "r", "euc-jp"))
 	for row in reader:
 		hyousou = row[0]
 		if len(hyousou) == 1:
@@ -75,7 +81,7 @@ def make_dic(CODE, CS_FILE, THISDIR):
 			if hyousou == "聾":
 				continue
 			jdic_tankan[hyousou] = row
-    with open_file(path.join(THISDIR, OUT_FILE), "w", CODE) as file:
+	with open_file(str(THISDIR / OUT_FILE), "w", CODE) as file:
 		for k, v in char_dic.items():
 			if contains_hankaku_katakana(k):
 				continue

```