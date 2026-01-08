# Diff for: `jptools\jpDicTest.py`

**Source**: `F:\nvda\gh\alphajp-251219\jptools\jpDicTest.py`  
**Current**: `F:\nvda\gh\alphajp-260109\jptools\jpDicTest.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\jpDicTest.py" "b/F:\\nvda\\gh\\alphajp-260109\\jptools\\jpDicTest.py"
index c6d7f69..c0a4de3 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\jpDicTest.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\jptools\\jpDicTest.py"
@@ -10,17 +10,18 @@
 
 import unittest
 import sys
-import os
+from pathlib import Path
 
-sys.path.append(r"..\source")
-sys.path.append(r"..\miscdeps\python")
+script_dir = Path(__file__).parent
+sys.path.append(str(script_dir.parent / "source"))
+sys.path.append(str(script_dir.parent / "miscdeps" / "python"))
 
-import languageHandler
+import languageHandler  # noqa: E402
 
 # Initialize globalVars before importing modules that depend on it.
 import globalVars  # noqa: E402
 
-appDir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
+appDir = str(Path(__file__).parent.parent.resolve())
 globalVars.appDir = appDir
 
 import gettext  # noqa: E402
@@ -80,7 +81,9 @@ def __init__(self):
 
 languageHandler.setLanguage("ja")
 
-gettext.translation("nvda", localedir=r"..\source\locale", languages=["ja"]).install()
+gettext.translation(
+	"nvda", localedir=str(script_dir.parent / "source" / "locale"), languages=["ja"]
+).install()
 
 
 class JpUtilsTestCase(unittest.TestCase):

```