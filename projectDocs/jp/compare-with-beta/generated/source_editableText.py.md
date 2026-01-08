# Diff for: `source\editableText.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\editableText.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\editableText.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\editableText.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\editableText.py"
index 3ca4718..b246e38 100644
--- "a/F:\\nvda\\gh\\beta\\source\\editableText.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\editableText.py"
@@ -214,6 +214,22 @@ def script_caret_newLine(self, gesture):
 		bookmark = info.bookmark
 		gesture.send()
 		caretMoved, newInfo = self._hasCaretMoved(bookmark)
+		# BEGIN JP PATCH
+		# nvdajp: announce new line
+		from NVDAHelper import lastCompAttr
+
+		if (
+			caretMoved
+			and (not lastCompAttr)
+			and config.conf["keyboard"]["speakTypedCharacters"]
+			and config.conf["language"]["jpAnnounceNewLine"]
+		):
+			import queueHandler
+			from gui import _
+
+			# Translators: new line of editable text
+			queueHandler.queueFunction(queueHandler.eventQueue, speech.speakMessage, _("new line"))
+		# END JP PATCH
 		if not caretMoved or not newInfo:
 			return
 		# newInfo.copy should be good enough here, but in MS Word we get strange results.

```