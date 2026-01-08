# Diff for: `source\NVDAObjects\UIA\wordDocument.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\NVDAObjects\UIA\wordDocument.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\UIA\wordDocument.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\UIA\\wordDocument.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\UIA\\wordDocument.py"
index c160ddf..f5603d8 100644
--- "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\UIA\\wordDocument.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\UIA\\wordDocument.py"
@@ -412,10 +412,10 @@ def getTextWithFields(  # noqa: C901
 			return fields
 
 		# MS Word tries to produce speakable math content within equations.
-		# However, using math presentation providers with the exposed mathml property on the equation is much nicer.
+		# However, using mathPlayer with the exposed mathml property on the equation is much nicer.
 		# But, we therefore need to remove the inner math content if reading by line
 		if not formatConfig or not formatConfig.get("extraDetail"):
-			# We really only want to remove content if we can guarantee that a math presentation provider is available.
+			# We really only want to remove content if we can guarantee that mathPlayer is available.
 			if mathPres.speechProvider or mathPres.brailleProvider:
 				curLevel = 0
 				mathLevel = None
@@ -601,7 +601,7 @@ def _shouldSetFocusToObj(self, obj: NVDAObject) -> bool:
 		):
 			return False
 		elif obj.role == controlTypes.Role.MATH:
-			# Don't set focus to math equations otherwise they cannot be interacted  with by math presentation providers.
+			# Don't set focus to math equations otherwise they cannot be interacted  with mathPlayer.
 			return False
 		return super()._shouldSetFocusToObj(obj)
 
@@ -612,7 +612,7 @@ def shouldPassThrough(self, obj, reason=None):
 		):
 			return False
 		elif obj.role == controlTypes.Role.MATH:
-			# Don't  activate focus mode for math equations otherwise they cannot be interacted  with by math presentation providers.
+			# Don't  activate focus mode for math equations otherwise they cannot be interacted  with mathPlayer.
 			return False
 		return super(WordBrowseModeDocument, self).shouldPassThrough(obj, reason=reason)
 

```