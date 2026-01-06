# Diff for: `source\NVDAObjects\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\__init__.py`  
**Current**: `F:\nvda\gh\alphajp\source\NVDAObjects\__init__.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\__init__.py" "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\__init__.py"
index 4a974e6eb0..660a6ae795 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\__init__.py"
@@ -514,8 +514,8 @@ def _get_roleTextBraille(self):
 		which will override the standard label for this object's role property as well as the value of roleText.
 		By default, NVDA falls back to using roleText.
 		"""
-		if self.landmark and self.landmark in braille.getLandmarkLabels():
-			return f"{braille.getRoleLabel(controlTypes.Role.LANDMARK)} {braille.getLandmarkLabel(self.landmark)}"
+		if self.landmark and self.landmark in braille.landmarkLabels:
+			return f"{braille.roleLabels[controlTypes.Role.LANDMARK]} {braille.landmarkLabels[self.landmark]}"
 		return self.roleText
 
 	#: Typing information for auto property _get_value

```