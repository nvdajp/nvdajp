# Diff for: `source\synthDrivers\jtalk\jtalkDir.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\synthDrivers\jtalk\jtalkDir.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\synthDrivers\jtalk\jtalkDir.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\jtalkDir.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDrivers\\jtalk\\jtalkDir.py"
index e967022..f035ba7 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\jtalkDir.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDrivers\\jtalk\\jtalkDir.py"
@@ -3,44 +3,39 @@
 # speech engine nvdajp_jtalk
 # Copyright (C) 2010-2014 Takuya Nishimoto (nishimotz.com)
 
-import os
 import sys
 from glob import glob
 import tempfile
 import shutil
-from os import getcwd
+from pathlib import Path
 
 
-jtalk_dir = os.path.dirname(__file__)
+jtalk_dir = Path(__file__).parent
 if hasattr(sys, "frozen"):
-    d = os.path.join(getcwd(), "synthDrivers", "jtalk")
-    if os.path.isdir(d):
+	d = Path.cwd() / "synthDrivers" / "jtalk"
+	if d.is_dir():
 		jtalk_dir = d
 
-configDir = getcwd()
+configDir = Path.cwd()
 try:
 	import globalVars  # type: ignore
 
 	if globalVars.appArgs.configPath:
-        configDir = globalVars.appArgs.configPath
-    d = os.path.join(
-        globalVars.appArgs.configPath, "addons", "nvdajp_jtalk", "synthDrivers", "jtalk"
-    )
-    if os.path.isdir(d):
+		configDir = Path(globalVars.appArgs.configPath)
+		d = Path(globalVars.appArgs.configPath) / "addons" / "nvdajp_jtalk" / "synthDrivers" / "jtalk"
+		if d.is_dir():
 			jtalk_dir = d
-except:
+except Exception:
 	pass
 
-dic_dir = os.path.join(jtalk_dir, "dic")
+dic_dir = jtalk_dir / "dic"
 
-user_dics_org = [
-    os.path.normpath(d) for d in glob(os.path.join(configDir, "jtusr.dic"))
-]
+user_dics_org = [Path(d).resolve() for d in glob(str(configDir / "jtusr.dic"))]
 
-tempDir = tempfile.mkdtemp()
+tempDir = Path(tempfile.mkdtemp())
 user_dics = []
 for u in user_dics_org:
-    b = os.path.basename(u)
-    d = os.path.join(tempDir, b)
-    shutil.copyfile(u, d)
-    user_dics.append(d)
+	b = u.name
+	d = tempDir / b
+	shutil.copyfile(str(u), str(d))
+	user_dics.append(str(d))

```