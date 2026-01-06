# Diff for: `source\gui\settingsDialogs.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\gui\settingsDialogs.py`  
**Current**: `F:\nvda\gh\alphajp\source\gui\settingsDialogs.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\settingsDialogs.py" "b/F:\\nvda\\gh\\alphajp\\source\\gui\\settingsDialogs.py"
index 73559b08b1..c36aacc009 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\settingsDialogs.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\gui\\settingsDialogs.py"
@@ -41,6 +41,7 @@
 	TetherTo,
 	ParagraphStartMarker,
 	ReportLineIndentation,
+	ReportSpellingErrors,
 	ReportTableHeaders,
 	ReportCellBorders,
 	OutputMode,
@@ -944,6 +945,7 @@ def makeSettings(self, settingsSizer):
 			if globalVars.appArgs.secure:
 				item.Disable()
 			settingsSizerHelper.addItem(item)
+			# BEGIN JP PATCH (Replace "NV Access" with "NVDA Japanese Team")
 			item = self.allowUsageStatsCheckBox = wx.CheckBox(
 				self,
 				# Translators: The label of a checkbox in general settings to toggle allowing of usage stats gathering
@@ -951,6 +953,7 @@ def makeSettings(self, settingsSizer):
 					"NV Access", _("NVDA Japanese Team")
 				),
 			)
+			# END JP PATCH
 			self.bindHelpEvent("GeneralSettingsGatherUsageStats", self.allowUsageStatsCheckBox)
 			item.Value = config.conf["update"]["allowUsageStats"]
 			if globalVars.appArgs.secure:
@@ -1181,6 +1184,7 @@ def onRestartNowButton(self, evt):
 		queueHandler.queueFunction(queueHandler.eventQueue, core.restart)
 
 
+# BEGIN JP PATCH (Japanese language settings panel)
 class LanguageSettingsPanel(SettingsPanel):
 	# Translators: This is the label for the language settings dialog.
 	title = _("Language Settings")
@@ -1297,6 +1301,7 @@ def onSave(self):
 
 		config.conf["language"]["jpKatakanaPitchChange"] = self.jpKatakanaPitchChangeEdit.Value
 		config.conf["language"]["halfShapePitchChange"] = self.halfShapePitchChangeEdit.Value
+# END JP PATCH
 
 
 class SpeechSettingsPanel(SettingsPanel):
@@ -2244,7 +2249,7 @@ def makeSettings(self, settingsSizer):
 		)
 		self.bindHelpEvent("KeyboardSettingsAlertForSpellingErrors", self.alertForSpellingErrorsCheckBox)
 		self.alertForSpellingErrorsCheckBox.SetValue(config.conf["keyboard"]["alertForSpellingErrors"])
-		if not config.conf["documentFormatting"]["reportSpellingErrors"]:
+		if not config.conf["documentFormatting"]["reportSpellingErrors2"]:
 			self.alertForSpellingErrorsCheckBox.Disable()
 
 		# Translators: This is the label for a checkbox in the
@@ -2598,6 +2603,15 @@ def makeSettings(self, settingsSizer):
 			config.conf["presentation"]["guessObjectPositionInformationWhenUnavailable"],
 		)
 
+		# Translators: This is the label for a checkbox in the
+		# object presentation settings panel.
+		reportMultiSelectText = _("Report when lists support &multiple selection")
+		self.reportMultiSelectCheckBox = sHelper.addItem(wx.CheckBox(self, label=reportMultiSelectText))
+		self.bindHelpEvent("ReportMultiSelect", self.reportMultiSelectCheckBox)
+		self.reportMultiSelectCheckBox.SetValue(
+			config.conf["presentation"]["reportMultiSelect"],
+		)
+
 		# Translators: This is the label for a checkbox in the
 		# object presentation settings panel.
 		descriptionText = _("Report object &descriptions")
@@ -2662,6 +2676,7 @@ def onSave(self):
 		config.conf["presentation"]["guessObjectPositionInformationWhenUnavailable"] = (
 			self.guessPositionInfoCheckBox.IsChecked()
 		)
+		config.conf["presentation"]["reportMultiSelect"] = self.reportMultiSelectCheckBox.IsChecked()
 		config.conf["presentation"]["reportObjectDescriptions"] = self.descriptionCheckBox.IsChecked()
 		config.conf["presentation"]["progressBarUpdates"]["progressBarOutputMode"] = self.progressLabels[
 			self.progressList.GetSelection()
@@ -2920,11 +2935,23 @@ def makeSettings(self, settingsSizer):
 		self.revisionsCheckBox = docInfoGroup.addItem(wx.CheckBox(docInfoBox, label=revisionsText))
 		self.revisionsCheckBox.SetValue(config.conf["documentFormatting"]["reportRevisions"])
 
-		# Translators: This is the label for a checkbox in the
-		# document formatting settings panel.
-		spellingErrorText = _("Spelling e&rrors")
-		self.spellingErrorsCheckBox = docInfoGroup.addItem(wx.CheckBox(docInfoBox, label=spellingErrorText))
-		self.spellingErrorsCheckBox.SetValue(config.conf["documentFormatting"]["reportSpellingErrors"])
+		self._spellingErrorsChecklist = docInfoGroup.addLabeledControl(
+			# Translators: This is the label for a checklist in the
+			# document formatting settings panel.
+			_("Spelling e&rrors"),
+			nvdaControls.CustomCheckListBox,
+			choices=[i.displayString for i in ReportSpellingErrors],
+		)
+		checkedItems = []
+		for i, mode in enumerate(ReportSpellingErrors):
+			if config.conf["documentFormatting"]["reportSpellingErrors2"] & mode.value:
+				checkedItems.append(i)
+		self._spellingErrorsChecklist.SetCheckedItems(checkedItems)
+		self._spellingErrorsChecklist.Select(0)
+		self.bindHelpEvent(
+			"reportSpellingErrors",
+			self._spellingErrorsChecklist,
+		)
 
 		# Translators: This is the label for a group of document formatting options in the
 		# document formatting settings panel
@@ -3147,7 +3174,11 @@ def onSave(self):
 		config.conf["documentFormatting"]["reportHighlight"] = self.highlightCheckBox.IsChecked()
 		config.conf["documentFormatting"]["reportAlignment"] = self.alignmentCheckBox.IsChecked()
 		config.conf["documentFormatting"]["reportStyle"] = self.styleCheckBox.IsChecked()
-		config.conf["documentFormatting"]["reportSpellingErrors"] = self.spellingErrorsCheckBox.IsChecked()
+		config.conf["documentFormatting"]["reportSpellingErrors2"] = sum(
+			mode.value
+			for (n, mode) in enumerate(ReportSpellingErrors)
+			if self._spellingErrorsChecklist.IsChecked(n)
+		)
 		config.conf["documentFormatting"]["reportPage"] = self.pageCheckBox.IsChecked()
 		config.conf["documentFormatting"]["reportLineNumber"] = self.lineNumberCheckBox.IsChecked()
 		config.conf["documentFormatting"]["reportLineIndentation"] = self.lineIndentationCombo.GetSelection()
@@ -4278,6 +4309,7 @@ def __init__(self, parent):
 			"garbageHandler",
 			"remoteClient",
 			"externalPythonDependencies",
+			"bdDetect",
 		]
 		# Translators: This is the label for a list in the
 		#  Advanced settings panel
@@ -4303,10 +4335,8 @@ def __init__(self, parent):
 		# Translators: Label for the Play a sound for logged errors combobox, in the Advanced settings panel.
 		label = _("Play a sound for logged e&rrors:")
 		playErrorSoundChoices = (
-			# # Translators: Label for a value in the Play a sound for logged errors combobox, in the Advanced settings.
-			# pgettext("advanced.playErrorSound", "Only in NVDA test versions"),
 			# Translators: Label for a value in the Play a sound for logged errors combobox, in the Advanced settings.
-			_("No"),
+			pgettext("advanced.playErrorSound", "Only in NVDA test versions"),
 			# Translators: Label for a value in the Play a sound for logged errors combobox, in the Advanced settings.
 			pgettext("advanced.playErrorSound", "Yes"),
 		)
@@ -5647,7 +5677,9 @@ class NVDASettingsDialog(MultiCategorySettingsDialog):
 	title = _("NVDA Settings")
 	categoryClasses = [
 		GeneralSettingsPanel,
+		# BEGIN JP PATCH (Japanese language settings panel)
 		LanguageSettingsPanel,
+		# END JP PATCH
 		SpeechSettingsPanel,
 		BrailleSettingsPanel,
 		AudioPanel,

```