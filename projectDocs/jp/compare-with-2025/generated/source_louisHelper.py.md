# Diff for: `source\louisHelper.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\louisHelper.py`  
**Current**: `F:\nvda\gh\alphajp\source\louisHelper.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\louisHelper.py" "b/F:\\nvda\\gh\\alphajp\\source\\louisHelper.py"
index 8edbc02901..a90d6b4299 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\louisHelper.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\louisHelper.py"
@@ -158,14 +158,17 @@ def translate(tableList, inbuf, typeform=None, cursorPos=None, mode=0):
 	except ModuleNotFoundError:
 		log.warning("Japanese translation module not found.")
 		jpTranslate = None
-	if jpTranslate and tableList[0].endswith("ja-jp-comp6.utb"):
+	if jpTranslate and tableList and len(tableList) > 0 and tableList[0].endswith("ja-jp-comp6.utb"):
 		log.debug(text)
 		nabcc = config.conf["braille"]["expandAtCursor"]
+		try:
 			braille, brailleToRawPos, rawToBraillePos, brailleCursorPos = jpTranslate(
 				text,
 				cursorPos=cursorPos or 0,
 				nabcc=nabcc,
 			)
+		except Exception as e:
+			raise
 	else:
 		braille, brailleToRawPos, rawToBraillePos, brailleCursorPos = louis.translate(
 			tableList,

```