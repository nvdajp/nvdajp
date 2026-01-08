# Diff for: `source\gui\configProfiles.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\gui\configProfiles.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\configProfiles.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\configProfiles.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\configProfiles.py"
index d29ce69..8e33c8b 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\configProfiles.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\configProfiles.py"
@@ -4,11 +4,11 @@
 # See the file COPYING for more details.
 
 import wx
+import NVDAState
 import config
 import api
 import gui
 from logHandler import log
-import globalVars
 from . import guiHelper
 import gui.contextHelp
 
@@ -110,7 +110,7 @@ def __init__(self, parent):
 		self.Bind(wx.EVT_BUTTON, self.onClose, id=wx.ID_CLOSE)
 		self.EscapeId = wx.ID_CLOSE
 
-		if globalVars.appArgs.secure:
+		if not NVDAState.shouldWriteToDisk():
 			for item in newButton, triggersButton, self.renameButton, self.deleteButton:
 				item.Disable()
 		self.onProfileListChoice(None)
@@ -242,7 +242,7 @@ def onProfileListChoice(self, evt):
 			label = _("Manual activate")
 		self.changeStateButton.Label = label
 		self.changeStateButton.Enabled = enable
-		if globalVars.appArgs.secure:
+		if not NVDAState.shouldWriteToDisk():
 			return
 		self.deleteButton.Enabled = enable
 		self.renameButton.Enabled = enable

```