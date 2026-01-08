# Diff for: `source\gui\addonStoreGui\controls\storeDialog.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\gui\addonStoreGui\controls\storeDialog.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\addonStoreGui\controls\storeDialog.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\addonStoreGui\\controls\\storeDialog.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\addonStoreGui\\controls\\storeDialog.py"
index 7283f2a..1c67707 100644
--- "a/F:\\nvda\\gh\\beta\\source\\gui\\addonStoreGui\\controls\\storeDialog.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\addonStoreGui\\controls\\storeDialog.py"
@@ -7,6 +7,9 @@
 import wx
 from wx.adv import BannerWindow
 
+from addonHandler import (
+	BUNDLE_EXTENSION,
+)
 from addonStore.dataManager import addonDataManager
 from addonStore.models.channel import Channel, _channelFilters
 from addonStore.models.status import (
@@ -14,7 +17,6 @@
 	_statusFilters,
 	_StatusFilterKey,
 )
-from config.registry import ADDON_BUNDLE_EXTENSION
 from core import callLater
 import globalVars
 import gui
@@ -416,7 +418,7 @@ def openExternalInstall(self, evt: wx.EVT_BUTTON):
 			# Translators: The message displayed in the dialog that
 			# allows you to choose an add-on package for installation.
 			message=pgettext("addonStore", "Choose Add-on Package File"),
-			wildcard=(fileTypeLabel + "|*.{ext}").format(ext=ADDON_BUNDLE_EXTENSION),
+			wildcard=(fileTypeLabel + "|*.{ext}").format(ext=BUNDLE_EXTENSION),
 			defaultDir="c:",
 			style=wx.FD_OPEN,
 		)

```