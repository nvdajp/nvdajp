# Diff for: `miscDepsJp\jptools\jtusrdic\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\miscDepsJp\jptools\jtusrdic\__init__.py`  
**Current**: `F:\nvda\gh\alphajp\miscDepsJp\jptools\jtusrdic\__init__.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtusrdic\\__init__.py" "b/F:\\nvda\\gh\\alphajp\\miscDepsJp\\jptools\\jtusrdic\\__init__.py"
index b4625ee78d..8232dcbf37 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtusrdic\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp\\miscDepsJp\\jptools\\jtusrdic\\__init__.py"
@@ -10,35 +10,33 @@
 import addonHandler
 import globalVars
 from logHandler import log
-import os
 import sys
+from pathlib import Path
 
 # Use source/synthDrivers/jtalk directly (files moved from miscDepsJp in Phase 1)
-script_dir = os.path.dirname(os.path.abspath(__file__))
+script_dir = Path(__file__).resolve().parent
 # script_dir -> miscDepsJp/jptools/jtusrdic
 # ../../.. -> repo root
-repo_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
-jtalk_dir = os.path.join(repo_root, "source", "synthDrivers", "jtalk")
-if jtalk_dir not in sys.path:
-    sys.path.insert(0, jtalk_dir)
+repo_root = (script_dir / ".." / ".." / "..").resolve()
+jtalk_dir = repo_root / "source" / "synthDrivers" / "jtalk"
+jtalk_dir_str = str(jtalk_dir)
+if jtalk_dir_str not in sys.path:
+    sys.path.insert(0, jtalk_dir_str)
 import jtalkDir
-import codecs
-import sys
 
-impPath = os.path.abspath(os.path.dirname(__file__))
-sys.path.append(impPath)
+impPath = Path(__file__).resolve().parent
+sys.path.append(str(impPath))
 import plumbum
-from plumbum import local
 
 del sys.path[-1]
 
-_addonDir = os.path.join(os.path.dirname(__file__), "..", "..")
-_curAddon = addonHandler.Addon(_addonDir)
+_addonDir = (Path(__file__).parent / ".." / "..").resolve()
+_curAddon = addonHandler.Addon(str(_addonDir))
 _addonSummary = _curAddon.manifest["summary"]
 addonHandler.initTranslation()
 
 mecabDictIndex = plumbum.local[
-    os.path.join(os.path.dirname(__file__), "mecab-dict-index.exe")
+    str(Path(__file__).parent / "mecab-dict-index.exe")
 ]
 
 
@@ -48,8 +46,8 @@ def editUserDicSrc(self):
         for s in srcs:
             os.startfile(s)
     else:
-        fileName = os.path.join(jtalkDir.configDir, "jtusr.txt")
-        with codecs.open(fileName, "w", "utf_8", errors="replace") as f:
+        fileName = str(Path(jtalkDir.configDir) / "jtusr.txt")
+        with open(fileName, "w", encoding="utf-8", errors="replace") as f:
             f.writelines(
                 ["足手纏い,,,,名詞,形容動詞語幹,*,*,*,*,足手纏い,アシデマトイ,アシデマトイ,4/6,C1,アシデ マトイ\n"]
             )
@@ -64,9 +62,7 @@ def compileUserDic(self):
         gui.messageBox(_("No source found."), _("Done"), wx.OK)
         return
     for s in srcs:
-        u = os.path.join(
-            jtalkDir.configDir, os.path.basename(s).replace(".txt", ".dic")
-        )
+        u = str(Path(jtalkDir.configDir) / Path(s).name.replace(".txt", ".dic"))
         log.info("user_dic %s to %s" % (s, u))
         # mecab-dict-index.exe -d ..\source\synthDrivers\jtalk\dic -u jtusr.dic -f utf-8 -t utf-8 jtusr.txt
         ret = mecabDictIndex[

```