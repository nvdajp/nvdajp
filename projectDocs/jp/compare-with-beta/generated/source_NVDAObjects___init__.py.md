# Diff for: `source\NVDAObjects\__init__.py`

**Source**: `F:\nvda\gh\beta\source\NVDAObjects\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\__init__.py"
index 660a6ae..c4a89f5 100644
--- "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\__init__.py"
@@ -514,8 +514,11 @@ def _get_roleTextBraille(self):
 		which will override the standard label for this object's role property as well as the value of roleText.
 		By default, NVDA falls back to using roleText.
 		"""
-		if self.landmark and self.landmark in braille.landmarkLabels:
-			return f"{braille.roleLabels[controlTypes.Role.LANDMARK]} {braille.landmarkLabels[self.landmark]}"
+		# BEGIN JP PATCH
+		# nvdajp: use getRoleLabel and getLandmarkLabel functions for JP-specific braille processing
+		if self.landmark and self.landmark in braille.getLandmarkLabels():
+			return f"{braille.getRoleLabel(controlTypes.Role.LANDMARK)} {braille.getLandmarkLabel(self.landmark)}"
+		# END JP PATCH
 		return self.roleText
 
 	#: Typing information for auto property _get_value

```