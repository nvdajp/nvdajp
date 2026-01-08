# Diff for: `source\NVDAObjects\IAccessible\mscandui.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\IAccessible\mscandui.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\IAccessible\mscandui.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\IAccessible\\mscandui.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\mscandui.py"
index b711251..51a3981 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\IAccessible\\mscandui.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\mscandui.py"
@@ -78,15 +78,19 @@ def _get_states(self):
 	def event_stateChange(self):
 		if controlTypes.State.SELECTED in self.states:
 			reportSelectedCandidate(self)
-			# nvdajp
+			# BEGIN JP PATCH
+			# nvdajp: notify candidate comment for Microsoft IME
 			if not config.conf["inputComposition"]["announceSelectedCandidate"]:
 				return
 			import wx
 
 			wx.CallLater(1000, notifyCandidateComment, self)
+			# END JP PATCH
 
 
 def notifyCandidateComment(item):
+	# BEGIN JP PATCH
+	# nvdajp: function to notify Microsoft IME candidate comment
 	import windowUtils
 	import NVDAObjects.IAccessible
 	import winUser
@@ -120,6 +124,7 @@ def notifyCandidateComment(item):
 			msg += s
 	if msg:
 		ui.message(msg)
+	# END JP PATCH
 
 
 class MSCandUI21_candidateMenuItem(BaseCandidateItem):

```