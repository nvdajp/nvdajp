# Diff for: `source\gui\settingsDialogs.py`

**Source**: `F:\nvda\gh\beta\source\gui\settingsDialogs.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\settingsDialogs.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\settingsDialogs.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\settingsDialogs.py"
index 399e99c..12a8f2b 100644
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
@@ -2948,27 +3070,14 @@ def makeSettings(self, settingsSizer: wx.BoxSizer) -> None:
 
 		# Translators: label for combobox to specify which braille code to use
 		brailleMathCodeText = pgettext("math", "Braille math code for refreshable displays")
-		availableBrailleCodes: list[str] = preferences.getBrailleCodes()
-		autoBrailleCode = preferences.getAutoBrailleCode(availableBrailleCodes)
-		# Translators: An option in Math settings to select a braille code automatically,
-		# according to NVDA's language.
-		autoDisplay = pgettext("math", "Automatic ({name})").format(name=autoBrailleCode)
-		self._brailleCodeIds: list[str] = ["Auto"]
-		brailleMathCodeOptions: list[str] = [autoDisplay]
-		self._brailleCodeIds.extend(availableBrailleCodes)
-		brailleMathCodeOptions.extend(availableBrailleCodes)
+		brailleMathCodeOptions: list[str] = preferences.getBrailleCodes()
 		self.brailleMathCodeList = navGroup.addLabeledControl(
 			brailleMathCodeText,
 			wx.Choice,
 			choices=brailleMathCodeOptions,
 		)
 		self.bindHelpEvent("MathBrailleCode", self.brailleMathCodeList)
-		currentBrailleCode = config.conf["math"]["braille"]["brailleCode"]
-		try:
-			selectionIndex = self._brailleCodeIds.index(currentBrailleCode)
-		except ValueError:
-			selectionIndex = 0
-		self.brailleMathCodeList.SetSelection(selectionIndex)
+		self.brailleMathCodeList.SetStringSelection(config.conf["math"]["braille"]["brailleCode"])
 
 		# Translators: label for combobox to specify how braille dots should be modified when navigating/selecting subexprs
 		brailleHighlightsText = pgettext("math", "Highlight the current navigation node with dots 7 and 8")
@@ -3056,8 +3165,7 @@ def onSave(self):
 			BrailleNavHighlightOption,
 			self.brailleHighlightsList.GetSelection(),
 		)
-		selectedBrailleIndex = self.brailleMathCodeList.GetSelection()
-		mathConf["braille"]["brailleCode"] = self._brailleCodeIds[selectedBrailleIndex]
+		mathConf["braille"]["brailleCode"] = self.brailleMathCodeList.GetStringSelection()
 		mcPrefs: MathCATUserPreferences = MathCATUserPreferences.fromNVDAConfig()
 		mcPrefs.save()
 
@@ -5948,7 +6056,13 @@ class PrivacyAndSecuritySettingsPanel(SettingsPanel):
 	def makeSettings(self, sizer: wx.BoxSizer):
 		sHelper = guiHelper.BoxSizerHelper(self, sizer=sizer)
 
+		# BEGIN JP PATCH (Fix KeyError: 'screenCurtain')
+		from visionEnhancementProviders.screenCurtain import ScreenCurtainProvider, WarnOnLoadDialog, warnOnLoadCheckBoxText
 		self._screenCurtainConfig = config.conf["screenCurtain"]
+		screenCurtainId = ScreenCurtainProvider.getSettings().getId()
+		screenCurtainProviderInfo = vision.handler.getProviderInfo(screenCurtainId)
+		screenCurtainInstance = vision.handler.getProviderInstance(screenCurtainProviderInfo)
+		# END JP PATCH
 		# Translators: Name for a feature that disables output to the screen,
 		# making it black.
 		screenCurtainSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=_("Screen Curtain"))
@@ -5963,22 +6077,31 @@ def makeSettings(self, sizer: wx.BoxSizer):
 				label=_("Make screen black (immediate effect)"),
 			),
 		)
+		# BEGIN JP PATCH (Fix screenCurtain.screenCurtain reference)
 		self._screenCurtainEnabledCheckbox.SetValue(
-			screenCurtain.screenCurtain is not None and screenCurtain.screenCurtain.enabled,
+			screenCurtainInstance is not None and screenCurtainInstance.enabled,
 		)
 		self._screenCurtainEnabledCheckbox.Bind(wx.EVT_CHECKBOX, self._ensureScreenCurtainEnableState)
-		self._screenCurtainEnabledCheckbox.Enable(screenCurtain.screenCurtain is not None)
+		self._screenCurtainEnabledCheckbox.Enable(screenCurtainInstance is not None)
+		# END JP PATCH
 		self.bindHelpEvent("ScreenCurtainEnable", self._screenCurtainEnabledCheckbox)
 
 		self._screenCurtainWarnOnLoadCheckbox = screenCurtainGroup.addItem(
 			wx.CheckBox(
 				screenCurtainBox,
-				label=screenCurtain._screenCurtain.WARN_ON_LOAD_CHECKBOX_TEXT,
+				# BEGIN JP PATCH (Fix screenCurtain._screenCurtain reference)
+				label=warnOnLoadCheckBoxText,
+				# END JP PATCH
 			),
 		)
 		self._screenCurtainWarnOnLoadCheckbox.SetValue(self._screenCurtainConfig["warnOnLoad"])
 		self.bindHelpEvent("ScreenCurtainWarnOnLoad", self._screenCurtainWarnOnLoadCheckbox)
 
+		# BEGIN JP PATCH (Store provider info and instance for later use)
+		self._screenCurtainProviderInfo = screenCurtainProviderInfo
+		self._screenCurtainInstance = screenCurtainInstance
+		# END JP PATCH
+
 		self._screenCurtainPlayToggleSoundsCheckbox = screenCurtainGroup.addItem(
 			wx.CheckBox(
 				screenCurtainBox,
@@ -6054,11 +6177,14 @@ def _ocrActive(self) -> bool:
 		"""
 		# Import late to avoid circular import
 		from contentRecog.recogUi import RefreshableRecogResultNVDAObject
+		# BEGIN JP PATCH (Fix screenCurtain._screenCurtain reference)
+		from screenCurtain._screenCurtain import UNAVAILABLE_WHEN_RECOGNISING_CONTENT_MESSAGE
+		# END JP PATCH
 
 		focusObj = api.getFocusObject()
 		if isinstance(focusObj, RefreshableRecogResultNVDAObject) and focusObj.recognizer.allowAutoRefresh:
 			ui.message(
-				screenCurtain._screenCurtain.UNAVAILABLE_WHEN_RECOGNISING_CONTENT_MESSAGE,
+				UNAVAILABLE_WHEN_RECOGNISING_CONTENT_MESSAGE,
 				speechPriority=speech.priorities.Spri.NOW,
 			)
 			return True
@@ -6066,36 +6192,48 @@ def _ocrActive(self) -> bool:
 
 	def _ensureScreenCurtainEnableState(self, evt: wx.CommandEvent):
 		"""Ensures that toggling the Screen Curtain checkbox toggles the Screen Curtain."""
+		# BEGIN JP PATCH (Fix screenCurtain.screenCurtain reference)
+		import speech
+		import ui
+		screenCurtainInstance = vision.handler.getProviderInstance(self._screenCurtainProviderInfo)
+		# END JP PATCH
 		shouldBeEnabled = evt.IsChecked()
-		if screenCurtain.screenCurtain is None:
+		if screenCurtainInstance is None:
 			self._screenCurtainEnabledCheckbox.SetValue(False)
 			return
-		currentlyEnabled = screenCurtain.screenCurtain.enabled
+		currentlyEnabled = screenCurtainInstance.enabled
 		if shouldBeEnabled and not currentlyEnabled:
 			confirmed = self._confirmEnableScreenCurtainWithUser()
 			if not confirmed or self._ocrActive():
 				self._screenCurtainEnabledCheckbox.SetValue(False)
 			else:
 				try:
-					screenCurtain.screenCurtain.enable()
+					vision.handler.initializeProvider(self._screenCurtainProviderInfo)
 				except Exception:
-					log.error("Error enabling Screen Curtain.", exc_info=True)
+					# BEGIN JP PATCH (Fix screenCurtain._screenCurtain reference)
+					from screenCurtain._screenCurtain import ERROR_ENABLING_MESSAGE
+					# END JP PATCH
+					import logHandler
+					logHandler.log.error("Error enabling Screen Curtain.", exc_info=True)
 					ui.message(
-						screenCurtain._screenCurtain.ERROR_ENABLING_MESSAGE,
+						ERROR_ENABLING_MESSAGE,
 						speechPriority=speech.priorities.Spri.NOW,
 					)
 					self._screenCurtainEnabledCheckbox.SetValue(False)
 		elif not shouldBeEnabled and currentlyEnabled:
-			screenCurtain.screenCurtain.disable()
+			vision.handler.terminateProvider(self._screenCurtainProviderInfo)
 
 	def _confirmEnableScreenCurtainWithUser(self) -> bool:
 		"""Confirm with the user before enabling Screen Curtain, if configured to do so.
 
 		:return: ``True`` if the Screen Curtain should be enabled; ``False`` otherwise.
 		"""
+		# BEGIN JP PATCH (Fix screenCurtain._screenCurtain reference)
+		from visionEnhancementProviders.screenCurtain import ScreenCurtainProvider, WarnOnLoadDialog
+		# END JP PATCH
 		if not self._screenCurtainConfig["warnOnLoad"]:
 			return True
-		with screenCurtain._screenCurtain.WarnOnLoadDialog(
+		with WarnOnLoadDialog(
 			screenCurtainSettingsStorage=self._screenCurtainConfig,
 			parent=self,
 		) as dlg:
@@ -6118,6 +6256,9 @@ class NVDASettingsDialog(MultiCategorySettingsDialog):
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