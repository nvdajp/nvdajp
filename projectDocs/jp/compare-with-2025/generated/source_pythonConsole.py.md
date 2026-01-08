# Diff for: `source\pythonConsole.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\pythonConsole.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\pythonConsole.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\pythonConsole.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\pythonConsole.py"
index c650646..5bee38c 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\pythonConsole.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\pythonConsole.py"
@@ -1,4 +1,3 @@
-# pythonConsole.py
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
@@ -74,8 +73,6 @@ def attr_matches(self, text: str) -> list[str]:
 		This causes serious issues for baseObject.Getter descriptors
 		when a getter raises NotImplementedError, for example (#15872).
 		"""
-		import re
-
 		m = re.match(r"(\w+(\.\w+)*)\.(\w*)", text)
 		if not m:
 			return []

```