# Diff for: `source\gui\settingsDialogs.py`

**Source**: `F:\nvda\gh\beta\source\gui\settingsDialogs.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\settingsDialogs.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\settingsDialogs.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\settingsDialogs.py"
index 399e99c..21348b4 100644
--- "a/F:\\nvda\\gh\\beta\\source\\gui\\settingsDialogs.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\settingsDialogs.py"
@@ -1145,6 +1145,128 @@ def onRestartNowButton(self, evt):
 		queueHandler.queueFunction(queueHandler.eventQueue, core.restart)
 
 
+# BEGIN JP PATCH (Japanese language settings panel)
+class LanguageSettingsPanel(SettingsPanel):
+	# Translators: This is the label for the language settings dialog.
+	title = _("Language Settings")
+
+	def makeSettings(self, settingsSizer):
+		settingsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
+		self.nconvAsNVDAModifierCheckBox = settingsSizerHelper.addItem(
+			# Translators: The label of a checkbox in language settings
+			wx.CheckBox(self, label=_("Use NonConvert as an NVDA modifier key"))
+		)
+		self.nconvAsNVDAModifierCheckBox.SetValue(config.conf["keyboard"]["useNonConvertAsNVDAModifierKey"])
+
+		self.convAsNVDAModifierCheckBox = settingsSizerHelper.addItem(
+			# Translators: The label of a checkbox in language settings
+			wx.CheckBox(self, label=_("Use Convert as an NVDA modifier key"))
+		)
+		self.convAsNVDAModifierCheckBox.SetValue(config.conf["keyboard"]["useConvertAsNVDAModifierKey"])
+
+		self.escAsNVDAModifierCheckBox = settingsSizerHelper.addItem(
+			# Translators: The label of a checkbox in language settings
+			wx.CheckBox(self, label=_("Use Escape as an NVDA modifier key"))
+		)
+		self.escAsNVDAModifierCheckBox.SetValue(config.conf["keyboard"]["useEscapeAsNVDAModifierKey"])
+
+		self.nvdajpImeBeepCheckBox = settingsSizerHelper.addItem(
+			# Translators: The label of a checkbox in language settings
+			wx.CheckBox(self, label=_("Beep for IME mode change"))
+		)
+		self.nvdajpImeBeepCheckBox.SetValue(config.conf["keyboard"]["nvdajpImeBeep"])
+
+		self.jpPhoneticReadingKanaCheckBox = settingsSizerHelper.addItem(
+			# Translators: The label of a checkbox in language settings
+			wx.CheckBox(self, label=_("Phonetic reading for Kana"))
+		)
+		self.jpPhoneticReadingKanaCheckBox.SetValue(config.conf["language"]["jpPhoneticReadingKana"])
+
+		self.jpPhoneticReadingLatinCheckBox = settingsSizerHelper.addItem(
+			# Translators: The label of a checkbox in language settings
+			wx.CheckBox(self, label=_("Phonetic reading for Latin"))
+		)
+		self.jpPhoneticReadingLatinCheckBox.SetValue(config.conf["language"]["jpPhoneticReadingLatin"])
+
+		self.jpKatakanaPitchChangeEdit = settingsSizerHelper.addLabeledControl(
+			# Translators: The label of a editbox in language settings
+			_("Katakana pitch change percentage"),
+			nvdaControls.SelectOnFocusSpinCtrl,
+			min=-100,
+			max=100,
+			initial=config.conf["language"]["jpKatakanaPitchChange"],
+		)
+
+		self.halfShapePitchChangeEdit = settingsSizerHelper.addLabeledControl(
+			# Translators: The label of a editbox in language settings
+			_("Half shape pitch change percentage"),
+			nvdaControls.SelectOnFocusSpinCtrl,
+			min=-100,
+			max=100,
+			initial=config.conf["language"]["halfShapePitchChange"],
+		)
+
+		self.announceCandidateNumberCheckBox = settingsSizerHelper.addItem(
+			# Translators: The label of a checkbox in language settings
+			wx.CheckBox(self, label=_("Announce candidate number"))
+		)
+		self.announceCandidateNumberCheckBox.SetValue(config.conf["language"]["announceCandidateNumber"])
+
+		self.nvdajpEnableKeyEventsCheckBox = settingsSizerHelper.addItem(
+			# Translators: The label of a checkbox in language settings
+			wx.CheckBox(self, label=_("Use IME support of nvdajp"))
+		)
+		self.nvdajpEnableKeyEventsCheckBox.SetValue(config.conf["keyboard"]["nvdajpEnableKeyEvents"])
+
+		self.jpAnsiEditCheckBox = settingsSizerHelper.addItem(
+			# Translators: The label of a checkbox in language settings
+			wx.CheckBox(self, label=_("Work around ANSI editbox"))
+		)
+		self.jpAnsiEditCheckBox.SetValue(config.conf["language"]["jpAnsiEditbox"])
+
+		self.jpAnnounceNewLineCheckBox = settingsSizerHelper.addItem(
+			# Translators: The label of a checkbox in language settings
+			wx.CheckBox(self, label=_("Announce new line in editable text"))
+		)
+		self.jpAnnounceNewLineCheckBox.SetValue(config.conf["language"]["jpAnnounceNewLine"])
+
+		self.openDocFileByMSHTACheckBox = settingsSizerHelper.addItem(
+			# Translators: The label of a checkbox in language settings
+			wx.CheckBox(self, label=_("Open document file by MSHTA"))
+		)
+		self.openDocFileByMSHTACheckBox.SetValue(config.conf["language"]["openDocFileByMSHTA"])
+
+		self.alwaysSpeakMathInEnglishCheckBox = settingsSizerHelper.addItem(
+			# Translators: The label of a checkbox in language settings
+			wx.CheckBox(self, label=_("Always speak math in English"))
+		)
+		self.alwaysSpeakMathInEnglishCheckBox.SetValue(config.conf["language"]["alwaysSpeakMathInEnglish"])
+
+	def onSave(self):
+		config.conf["keyboard"]["useNonConvertAsNVDAModifierKey"] = (
+			self.nconvAsNVDAModifierCheckBox.IsChecked()
+		)
+		config.conf["keyboard"]["useConvertAsNVDAModifierKey"] = self.convAsNVDAModifierCheckBox.IsChecked()
+		config.conf["keyboard"]["useEscapeAsNVDAModifierKey"] = self.escAsNVDAModifierCheckBox.IsChecked()
+		config.conf["language"]["jpPhoneticReadingKana"] = self.jpPhoneticReadingKanaCheckBox.IsChecked()
+		config.conf["language"]["jpPhoneticReadingLatin"] = self.jpPhoneticReadingLatinCheckBox.IsChecked()
+		config.conf["keyboard"]["nvdajpEnableKeyEvents"] = self.nvdajpEnableKeyEventsCheckBox.IsChecked()
+		config.conf["keyboard"]["nvdajpImeBeep"] = self.nvdajpImeBeepCheckBox.IsChecked()
+		config.conf["language"]["announceCandidateNumber"] = self.announceCandidateNumberCheckBox.IsChecked()
+		config.conf["language"]["jpAnsiEditbox"] = self.jpAnsiEditCheckBox.IsChecked()
+		config.conf["language"]["jpAnnounceNewLine"] = self.jpAnnounceNewLineCheckBox.IsChecked()
+		config.conf["language"]["openDocFileByMSHTA"] = self.openDocFileByMSHTACheckBox.IsChecked()
+		config.conf["language"]["alwaysSpeakMathInEnglish"] = (
+			self.alwaysSpeakMathInEnglishCheckBox.IsChecked()
+		)
+
+		config.conf["language"]["jpKatakanaPitchChange"] = self.jpKatakanaPitchChangeEdit.Value
+		config.conf["language"]["halfShapePitchChange"] = self.halfShapePitchChangeEdit.Value
+
+
+# END JP PATCH
+
+
 class SpeechSettingsPanel(SettingsPanel):
 	# Translators: This is the label for the speech panel
 	title = _("Speech")
@@ -6118,6 +6240,9 @@ class NVDASettingsDialog(MultiCategorySettingsDialog):
 	title = _("NVDA Settings")
 	categoryClasses = [
 		GeneralSettingsPanel,
+		# BEGIN JP PATCH (Japanese language settings panel)
+		LanguageSettingsPanel,
+		# END JP PATCH
 		SpeechSettingsPanel,
 		BrailleSettingsPanel,
 		AudioPanel,

```