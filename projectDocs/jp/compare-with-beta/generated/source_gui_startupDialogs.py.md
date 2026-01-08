# Diff for: `source\gui\startupDialogs.py`

**Source**: `F:\nvda\gh\beta\source\gui\startupDialogs.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\startupDialogs.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\startupDialogs.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\startupDialogs.py"
index 123bd57..39145bf 100644
--- "a/F:\\nvda\\gh\\beta\\source\\gui\\startupDialogs.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\startupDialogs.py"
@@ -75,6 +75,24 @@ def __init__(self, parent):
 			self.kbdList.SetSelection(index)
 		except (ValueError, KeyError):
 			log.error("Could not set Keyboard layout list to current layout", exc_info=True)
+		# BEGIN JP PATCH (Japanese keyboard modifier keys)
+		# Translators: The label of a checkbox in the Welcome dialog.
+		nconvAsNVDAModifierText = _("Use NonConvert as an NVDA modifier key")
+		self.nconvAsNVDAModifierCheckBox = sHelper.addItem(
+			wx.CheckBox(optionsBox, label=nconvAsNVDAModifierText)
+		)
+		self.nconvAsNVDAModifierCheckBox.SetValue(config.conf["keyboard"]["useNonConvertAsNVDAModifierKey"])
+		# Translators: The label of a checkbox in the Welcome dialog.
+		convAsNVDAModifierText = _("Use Convert as an NVDA modifier key")
+		self.convAsNVDAModifierCheckBox = sHelper.addItem(
+			wx.CheckBox(optionsBox, label=convAsNVDAModifierText)
+		)
+		self.convAsNVDAModifierCheckBox.SetValue(config.conf["keyboard"]["useConvertAsNVDAModifierKey"])
+		# Translators: The label of a checkbox in the Welcome dialog.
+		escAsNVDAModifierText = _("Use Escape as an NVDA modifier key")
+		self.escAsNVDAModifierCheckBox = sHelper.addItem(wx.CheckBox(optionsBox, label=escAsNVDAModifierText))
+		self.escAsNVDAModifierCheckBox.SetValue(config.conf["keyboard"]["useEscapeAsNVDAModifierKey"])
+		# END JP PATCH
 		# Translators: The label of a checkbox in the Welcome dialog.
 		capsAsNVDAModifierText = _("&Use CapsLock as an NVDA modifier key")
 		self.capsAsNVDAModifierCheckBox = sHelper.addItem(
@@ -130,6 +148,13 @@ def onOk(self, evt):
 			)
 		else:
 			config.conf["keyboard"]["NVDAModifierKeys"] = NVDAKeysVal
+		# BEGIN JP PATCH (Japanese keyboard modifier keys)
+		config.conf["keyboard"]["useNonConvertAsNVDAModifierKey"] = (
+			self.nconvAsNVDAModifierCheckBox.IsChecked()
+		)
+		config.conf["keyboard"]["useConvertAsNVDAModifierKey"] = self.convAsNVDAModifierCheckBox.IsChecked()
+		config.conf["keyboard"]["useEscapeAsNVDAModifierKey"] = self.escAsNVDAModifierCheckBox.IsChecked()
+		# END JP PATCH
 		if self.startAfterLogonCheckBox.Enabled:
 			config.setStartAfterLogon(self.startAfterLogonCheckBox.Value)
 		config.conf["general"]["showWelcomeDialogAtStartup"] = (
@@ -286,6 +311,10 @@ def __init__(self, parent):
 			"Please refer to the User Guide for a current list of all data collected.\n\n"
 			"Do you wish to allow NV Access to periodically collect this data in order to improve NVDA?",
 		)
+		# BEGIN JP PATCH (Replace "NV Access" with "NVDA Japanese Team")
+		# Translators: 'NV Access' should be replaced with 'NVDA Japanese Team'
+		message = message.replace("NV Access", _("NVDA Japanese Team"))
+		# END JP PATCH
 		sText = sHelper.addItem(wx.StaticText(self, label=message))
 		# the wx.Window must be constructed before we can get the handle.
 		import windowUtils

```