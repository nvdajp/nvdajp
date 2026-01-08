# Diff for: `miscDepsJp\jptools\jtusrdic\jtalkDir.py`

**Source**: `F:\nvda\gh\alphajp-251219\miscDepsJp\jptools\jtusrdic\jtalkDir.py`  
**Current**: `F:\nvda\gh\alphajp-260109\miscDepsJp\jptools\jtusrdic\jtalkDir.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtusrdic\\jtalkDir.py" "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\jtusrdic\\jtalkDir.py"
index 1221e50..b3759b9 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtusrdic\\jtalkDir.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\jtusrdic\\jtalkDir.py"
@@ -3,51 +3,37 @@
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
-import os
 import sys
 from glob import glob
 import tempfile
-import codecs
-
-jtalk_dir = os.path.normpath(
-    os.path.join(
-        os.path.dirname(__file__),
-        "..",
-        "..",
-        "..",
-        "..",
-        "..",
-        "synthDrivers",
-        "jtalk",
-    )
-)
+from pathlib import Path
+
+jtalk_dir = (Path(__file__).parent / ".." / ".." / ".." / ".." / ".." / "synthDrivers" / "jtalk").resolve()
 if hasattr(sys, "frozen"):
-    d = os.path.join(os.getcwd(), "synthDrivers", "jtalk")
-    if os.path.isdir(d):
+	d = Path.cwd() / "synthDrivers" / "jtalk"
+	if d.is_dir():
 		jtalk_dir = d
 
-dic_dir = os.path.join(jtalk_dir, "dic")
+dic_dir = jtalk_dir / "dic"
 
-configDir = os.getcwd()
+configDir = Path.cwd()
 try:
 	import globalVars
 
-    configDir = os.path.abspath(globalVars.appArgs.configPath)
-except:
+	configDir = Path(globalVars.appArgs.configPath).resolve()
+except Exception:
 	pass
 
-tempDir = tempfile.mkdtemp()
+tempDir = Path(tempfile.mkdtemp())
 
 
 def user_dic_srcs():
 	user_dics = []
-    for u in [os.path.normpath(d) for d in glob(os.path.join(configDir, "jtusr*.txt"))]:
-        d = os.path.join(tempDir, os.path.basename(u))
-        file_reader = codecs.open(u, "r", "utf-8-sig")
-        file_writer = codecs.open(d, "w", "utf-8")
+	for u in [Path(d).resolve() for d in glob(str(configDir / "jtusr*.txt"))]:
+		d = tempDir / u.name
+		with open(str(u), "r", encoding="utf-8-sig") as file_reader:
+			with open(str(d), "w", encoding="utf-8") as file_writer:
 				for line in file_reader:
 					file_writer.write(line)
-        file_writer.close()
-        file_reader.close()
-        user_dics.append(d)
+		user_dics.append(str(d))
 	return user_dics

```