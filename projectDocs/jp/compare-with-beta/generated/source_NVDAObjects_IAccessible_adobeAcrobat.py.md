# Diff for: `source\NVDAObjects\IAccessible\adobeAcrobat.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\NVDAObjects\IAccessible\adobeAcrobat.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\IAccessible\adobeAcrobat.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\IAccessible\\adobeAcrobat.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\adobeAcrobat.py"
index 631fc36..5feb3b4 100644
--- "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\IAccessible\\adobeAcrobat.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\adobeAcrobat.py"
@@ -175,7 +175,7 @@ def _getNodeMathMl(self, node: IPDDomElement) -> str:
 		answer += ">"
 		val = node.GetValue()
 		if val:
-			answer += html.escape(val)
+			answer += val
 		else:
 			for childNum in range(node.GetChildCount()):
 				try:

```