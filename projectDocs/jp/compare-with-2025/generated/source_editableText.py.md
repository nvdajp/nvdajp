# Diff for: `source\editableText.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\editableText.py`  
**Current**: `F:\nvda\gh\alphajp\source\editableText.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\editableText.py" "b/F:\\nvda\\gh\\alphajp\\source\\editableText.py"
index fbccf79ec8..3ca47189cc 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\editableText.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\editableText.py"
@@ -214,20 +214,6 @@ def script_caret_newLine(self, gesture):
 		bookmark = info.bookmark
 		gesture.send()
 		caretMoved, newInfo = self._hasCaretMoved(bookmark)
-		# nvdajp begin
-		from NVDAHelper import lastCompAttr
-
-		if (
-			caretMoved
-			and (not lastCompAttr)
-			and config.conf["keyboard"]["speakTypedCharacters"]
-			and config.conf["language"]["jpAnnounceNewLine"]
-		):
-			import queueHandler
-
-			# Translators: new line of editable text
-			queueHandler.queueFunction(queueHandler.eventQueue, speech.speakMessage, _("new line"))
-		# nvdajp end
 		if not caretMoved or not newInfo:
 			return
 		# newInfo.copy should be good enough here, but in MS Word we get strange results.

```