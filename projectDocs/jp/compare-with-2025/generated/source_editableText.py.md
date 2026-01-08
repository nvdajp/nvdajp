# Diff for: `source\editableText.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\editableText.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\editableText.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\editableText.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\editableText.py"
index fbccf79..b246e38 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\editableText.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\editableText.py"
@@ -214,7 +214,8 @@ def script_caret_newLine(self, gesture):
 		bookmark = info.bookmark
 		gesture.send()
 		caretMoved, newInfo = self._hasCaretMoved(bookmark)
-		# nvdajp begin
+		# BEGIN JP PATCH
+		# nvdajp: announce new line
 		from NVDAHelper import lastCompAttr
 
 		if (
@@ -224,10 +225,11 @@ def script_caret_newLine(self, gesture):
 			and config.conf["language"]["jpAnnounceNewLine"]
 		):
 			import queueHandler
+			from gui import _
 
 			# Translators: new line of editable text
 			queueHandler.queueFunction(queueHandler.eventQueue, speech.speakMessage, _("new line"))
-		# nvdajp end
+		# END JP PATCH
 		if not caretMoved or not newInfo:
 			return
 		# newInfo.copy should be good enough here, but in MS Word we get strange results.

```