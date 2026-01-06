# Diff for: `source\fonts\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\fonts\__init__.py`  
**Current**: `F:\nvda\gh\alphajp\source\fonts\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\fonts\\__init__.py" "b/F:\\nvda\\gh\\alphajp\\source\\fonts\\__init__.py"
index ab38fa927b..1511e2f78a 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\fonts\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\fonts\\__init__.py"
@@ -3,13 +3,14 @@
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 from typing import List
-
 import globalVars
 from logHandler import log
 import os
-from ctypes import WinDLL
 
-gdi32 = WinDLL("gdi32.dll")
+import winBindings.gdi32
+from utils import _deprecate
+
+
 """
 Loads custom fonts for use in NVDA.
 """
@@ -39,7 +40,7 @@ def addFonts(_fontSearchPath) -> List[str]:
 def _addFontResource(fontPath: str) -> int:
 	# from wingdi.h
 	FR_PRIVATE = 0x10
-	res = gdi32.AddFontResourceExW(
+	res = winBindings.gdi32.AddFontResourceEx(
 		fontPath,
 		# Only this process can use the font.
 		# The system will take care of unloading the font when the process ends.
@@ -62,3 +63,8 @@ def importFonts():
 
 	log.debug("Loading fonts.")
 	_imported = addFonts(fontsDir)
+
+
+__getattr__ = _deprecate.handleDeprecations(
+	_deprecate.MovedSymbol("gdi32", "winBindings.gdi32", "dll"),
+)

```