# Diff for: `source\gui\startupDialogs.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\gui\startupDialogs.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\startupDialogs.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\startupDialogs.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\startupDialogs.py"
index 47f6c78..39145bf 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\startupDialogs.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\startupDialogs.py"
@@ -1,4 +1,3 @@
-# -*- coding: UTF-8 -*-
 # A part of NonVisual Desktop Access (NVDA)
 # Copyright (C) 2006-2025 NV Access Limited, Łukasz Golonka, Cyrille Bougot
 # This file may be used under the terms of the GNU General Public License, version 2 or later.
@@ -18,7 +17,7 @@
 import gui.guiHelper
 import keyboardHandler
 from logHandler import log
-import versionInfo
+import buildVersion
 
 
 class WelcomeDialog(
@@ -76,7 +75,7 @@ def __init__(self, parent):
 			self.kbdList.SetSelection(index)
 		except (ValueError, KeyError):
 			log.error("Could not set Keyboard layout list to current layout", exc_info=True)
-		# nvdajp
+		# BEGIN JP PATCH (Japanese keyboard modifier keys)
 		# Translators: The label of a checkbox in the Welcome dialog.
 		nconvAsNVDAModifierText = _("Use NonConvert as an NVDA modifier key")
 		self.nconvAsNVDAModifierCheckBox = sHelper.addItem(
@@ -93,7 +92,7 @@ def __init__(self, parent):
 		escAsNVDAModifierText = _("Use Escape as an NVDA modifier key")
 		self.escAsNVDAModifierCheckBox = sHelper.addItem(wx.CheckBox(optionsBox, label=escAsNVDAModifierText))
 		self.escAsNVDAModifierCheckBox.SetValue(config.conf["keyboard"]["useEscapeAsNVDAModifierKey"])
-		# nvdajp done
+		# END JP PATCH
 		# Translators: The label of a checkbox in the Welcome dialog.
 		capsAsNVDAModifierText = _("&Use CapsLock as an NVDA modifier key")
 		self.capsAsNVDAModifierCheckBox = sHelper.addItem(
@@ -149,11 +148,13 @@ def onOk(self, evt):
 			)
 		else:
 			config.conf["keyboard"]["NVDAModifierKeys"] = NVDAKeysVal
+		# BEGIN JP PATCH (Japanese keyboard modifier keys)
 		config.conf["keyboard"]["useNonConvertAsNVDAModifierKey"] = (
 			self.nconvAsNVDAModifierCheckBox.IsChecked()
-		)  # nvdajp
+		)
 		config.conf["keyboard"]["useConvertAsNVDAModifierKey"] = self.convAsNVDAModifierCheckBox.IsChecked()
 		config.conf["keyboard"]["useEscapeAsNVDAModifierKey"] = self.escAsNVDAModifierCheckBox.IsChecked()
+		# END JP PATCH
 		if self.startAfterLogonCheckBox.Enabled:
 			config.setStartAfterLogon(self.startAfterLogonCheckBox.Value)
 		config.conf["general"]["showWelcomeDialogAtStartup"] = (
@@ -200,7 +201,7 @@ class LauncherDialog(
 	def __init__(self, parent: wx.Window | None):
 		super().__init__(
 			parent,
-			title=f"{versionInfo.name} {_('Launcher')}",
+			title=f"{buildVersion.name} {_('Launcher')}",
 		)
 
 		mainSizer = wx.BoxSizer(wx.VERTICAL)
@@ -310,8 +311,10 @@ def __init__(self, parent):
 			"Please refer to the User Guide for a current list of all data collected.\n\n"
 			"Do you wish to allow NV Access to periodically collect this data in order to improve NVDA?",
 		)
+		# BEGIN JP PATCH (Replace "NV Access" with "NVDA Japanese Team")
 		# Translators: 'NV Access' should be replaced with 'NVDA Japanese Team'
 		message = message.replace("NV Access", _("NVDA Japanese Team"))
+		# END JP PATCH
 		sText = sHelper.addItem(wx.StaticText(self, label=message))
 		# the wx.Window must be constructed before we can get the handle.
 		import windowUtils

```