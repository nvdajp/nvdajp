# Diff for: `source\NVDAObjects\IAccessible\mscandui.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\IAccessible\mscandui.py`  
**Current**: `F:\nvda\gh\alphajp\source\NVDAObjects\IAccessible\mscandui.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\IAccessible\\mscandui.py" "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\IAccessible\\mscandui.py"
index b711251954..5a155d3f3f 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\IAccessible\\mscandui.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\IAccessible\\mscandui.py"
@@ -78,48 +78,6 @@ def _get_states(self):
 	def event_stateChange(self):
 		if controlTypes.State.SELECTED in self.states:
 			reportSelectedCandidate(self)
-			# nvdajp
-			if not config.conf["inputComposition"]["announceSelectedCandidate"]:
-				return
-			import wx
-
-			wx.CallLater(1000, notifyCandidateComment, self)
-
-
-def notifyCandidateComment(item):
-	import windowUtils
-	import NVDAObjects.IAccessible
-	import winUser
-	import jpUtils
-
-	parent = api.getDesktopObject().windowHandle
-	try:
-		obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
-			windowUtils.findDescendantWindow(parent, className="mscandui40.comment", visible=True),
-			winUser.OBJID_CLIENT,
-			0,
-		)
-	except LookupError:
-		return
-	if not obj or not obj.firstChild or not obj.firstChild.children:
-		return
-	currDiscReading = item.name
-	msg = ""
-	isCurrItem = False
-	for o in obj.firstChild.children:
-		s = o.name
-		d = o.decodedAccDescription
-		if d == "Headword":
-			if currDiscReading == jpUtils.getDiscriminantReading(s):
-				isCurrItem = True
-			else:
-				isCurrItem = False
-		if d:
-			s = None
-		if s and isCurrItem:
-			msg += s
-	if msg:
-		ui.message(msg)
 
 
 class MSCandUI21_candidateMenuItem(BaseCandidateItem):

```