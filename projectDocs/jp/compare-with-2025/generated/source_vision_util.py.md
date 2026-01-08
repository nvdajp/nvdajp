# Diff for: `source\vision\util.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\vision\util.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\vision\util.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\vision\\util.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\vision\\util.py"
index 05b1a37..9644cc9 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\vision\\util.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\vision\\util.py"
@@ -2,7 +2,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.
+# Copyright (C) 2018-2025 NV Access Limited, Babbage B.V., hwf1324
 
 """Utility functions for vision enhancement providers."""
 
@@ -25,7 +25,11 @@ def getCaretRect(obj: Optional[TextContainerObject] = None) -> locationHelper.Re
 		obj = api.getCaretObject()
 	if api.isObjectInActiveTreeInterceptor(obj):
 		obj = obj.treeInterceptor
-	if api.isNVDAObject(obj):
+	if (
+		api.isNVDAObject(obj)
+		# Ignore fake NVDAObjects, as the caret rectangle may not be obtainable through the display model.
+		and not api.isFakeNVDAObject(obj)
+	):
 		# Import late to avoid circular import
 		import displayModel
 

```