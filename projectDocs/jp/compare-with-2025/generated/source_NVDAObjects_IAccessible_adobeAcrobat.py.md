# Diff for: `source\NVDAObjects\IAccessible\adobeAcrobat.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\IAccessible\adobeAcrobat.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\IAccessible\adobeAcrobat.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\IAccessible\\adobeAcrobat.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\adobeAcrobat.py"
index 5feb3b4..631fc36 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\IAccessible\\adobeAcrobat.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\adobeAcrobat.py"
@@ -175,7 +175,7 @@ def _getNodeMathMl(self, node: IPDDomElement) -> str:
 		answer += ">"
 		val = node.GetValue()
 		if val:
-			answer += val
+			answer += html.escape(val)
 		else:
 			for childNum in range(node.GetChildCount()):
 				try:

```