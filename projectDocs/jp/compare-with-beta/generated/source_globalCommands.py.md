# Diff for: `source\globalCommands.py`

**Source**: `F:\nvda\gh\beta\source\globalCommands.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\globalCommands.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\globalCommands.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\globalCommands.py"
index 432b35c..4f6be3e 100644
--- "a/F:\\nvda\\gh\\beta\\source\\globalCommands.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\globalCommands.py"
@@ -64,9 +64,11 @@
 import characterProcessing
 from baseObject import ScriptableObject
 import core
+import jpUtils  # nvdajp
 from winAPI._powerTracking import reportCurrentBatteryStatus
 import winVersion
 from base64 import b16encode
+import vision
 from utils.security import objectBelowLockScreenAndWindowsIsLocked
 import audio
 import synthDriverHandler
@@ -184,6 +186,11 @@ def toggleIntegerValue(
 	ui.message(msg)
 
 
+# BEGIN JP PATCH (character description mode)
+characterDescriptionMode = True
+# END JP PATCH
+
+
 class GlobalCommands(ScriptableObject):
 	"""Commands that are available at all times, regardless of the current focus."""
 
@@ -278,7 +285,13 @@ def script_reportCurrentLine(self, gesture):
 		if scriptCount == 0:
 			speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)
 		else:
-			speech.spellTextInfo(info, useCharacterDescriptions=scriptCount > 1)
+			# BEGIN JP PATCH (character description mode)
+			speech.spellTextInfo(
+				info,
+				useCharacterDescriptions=scriptCount > 1,
+				useDetails=characterDescriptionMode if scriptCount > 1 else False,
+			)
+			# END JP PATCH
 
 	@script(
 		# Translators: Input help mode message for left mouse click command.
@@ -407,7 +420,11 @@ def script_reportCurrentSelection(self, gesture):
 				return
 
 			elif len(info.text) < speech.speech.MAX_LENGTH_FOR_SELECTION_REPORTING:
-				speech.speakSpelling(info.text, useCharacterDescriptions=scriptCount > 1)
+				# BEGIN JP PATCH (character description mode)
+				speech.speakSpelling(
+					info.text, useCharacterDescriptions=scriptCount > 1, useDetails=scriptCount > 1
+				)
+				# END JP PATCH
 			else:
 				speech.speakTextSelected(info.text)
 				braille.handler.message(selectMessage)
@@ -1435,7 +1452,13 @@ def script_navigatorObject_current(self, gesture: inputCore.InputGesture):
 			text = " ".join(textList)
 			if len(text) > 0 and not text.isspace():
 				if scriptHandler.getLastScriptRepeatCount() == 1:
-					speech.speakSpelling(text)
+					# BEGIN JP PATCH (character description mode)
+					speech.speakSpelling(
+						text,
+						useCharacterDescriptions=characterDescriptionMode,
+						useDetails=characterDescriptionMode,
+					)
+					# END JP PATCH
 				else:
 					api.copyToClip(text, notify=True)
 		else:
@@ -1870,7 +1893,13 @@ def script_review_currentLine(self, gesture: inputCore.InputGesture):
 		if scriptCount == 0:
 			speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)
 		else:
-			speech.spellTextInfo(info, useCharacterDescriptions=scriptCount > 1)
+			# BEGIN JP PATCH (character description mode)
+			speech.spellTextInfo(
+				info,
+				useCharacterDescriptions=scriptCount > 1,
+				useDetails=characterDescriptionMode if scriptCount > 1 else False,
+			)
+			# END JP PATCH
 
 	@script(
 		description=_(
@@ -2069,7 +2098,11 @@ def script_review_currentWord(self, gesture: inputCore.InputGesture):
 		if scriptCount == 0:
 			speech.speakTextInfo(info, reason=controlTypes.OutputReason.CARET, unit=textInfos.UNIT_WORD)
 		else:
-			speech.spellTextInfo(info, useCharacterDescriptions=scriptCount > 1)
+			speech.spellTextInfo(
+				info,
+				useCharacterDescriptions=(scriptCount > 1),
+				useDetails=(scriptCount > 1 and characterDescriptionMode),  # nvdajp
+			)
 
 	@script(
 		description=_(
@@ -2187,6 +2220,7 @@ def script_review_previousCharacter(self, gesture: inputCore.InputGesture):
 		speakOnDemand=True,
 	)
 	def script_review_currentCharacter(self, gesture: inputCore.InputGesture):
+		global characterDescriptionMode  # nvdajp
 		info = api.getReviewPosition().copy()
 		# This script is available on the lock screen via getSafeScripts, as such
 		# ensure the review position does not contain secure information
@@ -2200,15 +2234,28 @@ def script_review_currentCharacter(self, gesture: inputCore.InputGesture):
 		braille.handler.handleReviewMove(shouldAutoTether=True)
 		scriptCount = scriptHandler.getLastScriptRepeatCount()
 		if scriptCount == 0:
-			speech.speakTextInfo(info, unit=textInfos.UNIT_CHARACTER, reason=controlTypes.OutputReason.CARET)
+			# BEGIN JP PATCH (character description mode)
+			speech.spellTextInfo(info, useCharacterDescriptions=characterDescriptionMode)
+			braille.handler.message(jpUtils.getDescriptionForBraille(info.text))
+			# END JP PATCH
 		elif scriptCount == 1:
-			speech.spellTextInfo(info, useCharacterDescriptions=True)
-		else:
+			# BEGIN JP PATCH (character description mode)
+			speech.spellTextInfo(info, useCharacterDescriptions=True, useDetails=True)
+			braille.handler.message(jpUtils.getDescriptionForBraille(info.text))
+			# END JP PATCH
+		elif scriptCount == 2:
+			# BEGIN JP PATCH (character description mode)
 			try:
 				cList = [ord(c) for c in info.text]
 			except TypeError:
-				c = None
-			if cList:
+				cList = None
+			if cList and jpUtils.isJa():
+				for c in cList:
+					s = jpUtils.code2kana(c)
+					o = "%d u+%s" % (c, s)
+					speech.speakMessage(o)
+				braille.handler.message("  ".join("%d %s" % (c, jpUtils.code2hex(c)) for c in cList))
+			elif cList:
 				for c in cList:
 					speech.speakMessage("%d," % c)
 					# Report hex along with decimal only when there is one character; else, it's confusing.
@@ -2222,6 +2269,18 @@ def script_review_currentCharacter(self, gesture: inputCore.InputGesture):
 					unit=textInfos.UNIT_CHARACTER,
 					reason=controlTypes.OutputReason.CARET,
 				)
+			# END JP PATCH
+		else:
+			# BEGIN JP PATCH (character description mode toggle)
+			if characterDescriptionMode:
+				# Translators: character description mode
+				ui.message(_("Character description mode disabled"))
+				characterDescriptionMode = False
+			else:
+				# Translators: character description mode
+				ui.message(_("Character description mode enabled"))
+				characterDescriptionMode = True
+			# END JP PATCH
 
 	@script(
 		description=_(
@@ -2513,6 +2572,9 @@ def script_restart(self, gesture):
 	@script(
 		# Translators: Input help mode message for show NVDA menu command.
 		description=_("Shows the NVDA menu"),
+		# BEGIN JP PATCH
+		allowInSleepMode=True,
+		# END JP PATCH
 		gestures=("kb:NVDA+n", "ts:2finger_double_tap"),
 	)
 	@gui.blockAction.when(gui.blockAction.Context.MODAL_DIALOG_OPEN)
@@ -2860,7 +2922,13 @@ def script_reportCurrentFocus(self, gesture: inputCore.InputGesture):
 			text = " ".join(s for s in speechList if isinstance(s, str))
 			braille.handler.message(text)
 		else:
-			speech.speakSpelling(focusObject.name, useCharacterDescriptions=repeatCount > 1)
+			# BEGIN JP PATCH (character description mode)
+			speech.speakSpelling(
+				focusObject.name,
+				useCharacterDescriptions=repeatCount > 1 and characterDescriptionMode,
+				useDetails=repeatCount > 1 and characterDescriptionMode,
+			)
+			# END JP PATCH
 
 	@staticmethod
 	def _getStatusBarText(setReviewCursor: bool = False) -> Optional[str]:
@@ -2945,7 +3013,11 @@ def script_spellStatusLine(self, gesture):
 			# Translators: Reported when status line exist, but is empty.
 			ui.message(_("no status bar information"))
 		else:
-			speech.speakSpelling(text)
+			# BEGIN JP PATCH (character description mode)
+			speech.speakSpelling(
+				text, useCharacterDescriptions=characterDescriptionMode, useDetails=characterDescriptionMode
+			)
+			# END JP PATCH
 
 	@script(
 		description=_(
@@ -3109,7 +3181,11 @@ def script_title(self, gesture: inputCore.InputGesture):
 		if repeatCount == 0:
 			ui.message(title)
 		elif repeatCount == 1:
-			speech.speakSpelling(title)
+			# BEGIN JP PATCH (character description mode)
+			speech.speakSpelling(
+				title, useCharacterDescriptions=characterDescriptionMode, useDetails=characterDescriptionMode
+			)
+			# END JP PATCH
 		else:
 			api.copyToClip(title, notify=True)
 
@@ -3992,7 +4068,11 @@ def script_reportClipboardText(self, gesture):
 			if repeatCount == 0:
 				ui.message(text)
 			else:
-				speech.speakSpelling(text, useCharacterDescriptions=repeatCount > 1)
+				# BEGIN JP PATCH (character description mode)
+				speech.speakSpelling(
+					text, useCharacterDescriptions=repeatCount > 1, useDetails=repeatCount > 1
+				)
+				# END JP PATCH
 		else:
 			ui.message(
 				ngettext(
@@ -4704,9 +4784,11 @@ def script_recognizeWithUwpOcr(self, gesture):
 			# Translators: Reported when Windows OCR is not available.
 			ui.message(_("Windows OCR not available"))
 			return
-		from screenCurtain import screenCurtain
+		from visionEnhancementProviders.screenCurtain import ScreenCurtainProvider
 
-		isScreenCurtainRunning = screenCurtain is not None and screenCurtain.enabled
+		screenCurtainId = ScreenCurtainProvider.getSettings().getId()
+		screenCurtainProviderInfo = vision.handler.getProviderInfo(screenCurtainId)
+		isScreenCurtainRunning = bool(vision.handler.getProviderInstance(screenCurtainProviderInfo))
 		if isScreenCurtainRunning:
 			# Translators: Reported when screen curtain is enabled.
 			ui.message(_("Please disable screen curtain before using Windows OCR."))
@@ -4810,8 +4892,8 @@ def script_speech_cycleUnicodeNormalization(self, gesture: inputCore.InputGestur
 		ui.message(msg)
 
 	_tempEnableScreenCurtain = True
-	_waitingOnScreenCurtainWarningDialog: wx.Dialog | None = None
-	_toggleScreenCurtainMessage: str | None = None
+	_waitingOnScreenCurtainWarningDialog: Optional[wx.Dialog] = None
+	_toggleScreenCurtainMessage: Optional[str] = None
 
 	@script(
 		description=_(
@@ -4824,20 +4906,19 @@ def script_speech_cycleUnicodeNormalization(self, gesture: inputCore.InputGestur
 		category=SCRCAT_VISION,
 		gesture="kb:NVDA+control+escape",
 	)
-	def script_toggleScreenCurtain(self, gesture: inputCore.InputGesture) -> None:
-		import screenCurtain
-
-		if screenCurtain.screenCurtain is None:
-			# Screen curtain has not been initialized.
-			# Translators: Reported when the screen curtain is not available.
-			ui.message(_("Screen curtain not available"), speechPriority=speech.priorities.Spri.NOW)
-			return
-
+	def script_toggleScreenCurtain(self, gesture):
 		scriptCount = scriptHandler.getLastScriptRepeatCount()
 		if scriptCount == 0:  # first call should reset last message
 			self._toggleScreenCurtainMessage = None
-		alreadyRunning = screenCurtain.screenCurtain.enabled
+
+		from visionEnhancementProviders.screenCurtain import ScreenCurtainProvider
+
+		screenCurtainId = ScreenCurtainProvider.getSettings().getId()
+		screenCurtainProviderInfo = vision.handler.getProviderInfo(screenCurtainId)
+		alreadyRunning = bool(vision.handler.getProviderInstance(screenCurtainProviderInfo))
+
 		GlobalCommands._tempEnableScreenCurtain = scriptCount == 0
+
 		if self._waitingOnScreenCurtainWarningDialog:
 			# Already in the process of enabling the screen curtain, exit early.
 			# Ensure that the dialog is in the foreground, and read it again.
@@ -4878,7 +4959,7 @@ def script_toggleScreenCurtain(self, gesture: inputCore.InputGesture) -> None:
 			# Translators: Reported when the screen curtain is disabled.
 			message = _("Screen curtain disabled")
 			try:
-				screenCurtain.screenCurtain.disable()
+				vision.handler.terminateProvider(screenCurtainProviderInfo)
 			except Exception:
 				# If the screen curtain was enabled, we do not expect exceptions.
 				log.error("Screen curtain termination error", exc_info=True)
@@ -4891,6 +4972,13 @@ def script_toggleScreenCurtain(self, gesture: inputCore.InputGesture) -> None:
 		elif (  # enable it
 			scriptCount in (0, 1)  # 1 press (temp enable) or 2 presses (enable)
 		):
+			# Check if screen curtain is available, exit early if not.
+			if not screenCurtainProviderInfo.providerClass.canStart():
+				# Translators: Reported when the screen curtain is not available.
+				message = _("Screen curtain not available")
+				self._toggleScreenCurtainMessage = message
+				ui.message(message, speechPriority=speech.priorities.Spri.NOW)
+				return
 
 			def _enableScreenCurtain(doEnable: bool = True):
 				self._waitingOnScreenCurtainWarningDialog = None
@@ -4906,9 +4994,12 @@ def _enableScreenCurtain(doEnable: bool = True):
 
 				try:
 					if alreadyRunning:
-						screenCurtain.screenCurtain.settings["enabled"] = True
+						screenCurtainProviderInfo.providerClass.enableInConfig(True)
 					else:
-						screenCurtain.screenCurtain.enable(persist=not tempEnable)
+						vision.handler.initializeProvider(
+							screenCurtainProviderInfo,
+							temporary=tempEnable,
+						)
 				except Exception:
 					log.error("Screen curtain initialization error", exc_info=True)
 					enableMessage = screenCurtain._screenCurtain.ERROR_ENABLING_MESSAGE
@@ -4917,11 +5008,14 @@ def _enableScreenCurtain(doEnable: bool = True):
 					ui.message(enableMessage, speechPriority=speech.priorities.Spri.NOW)
 
 			#  Show warning if necessary and do enable.
-			settingsStorage = screenCurtain.screenCurtain.settings
-			if settingsStorage["warnOnLoad"]:
-				dlg = screenCurtain._screenCurtain.WarnOnLoadDialog(
+			settingsStorage = ScreenCurtainProvider.getSettings()
+			if settingsStorage.warnOnLoad:
+				from visionEnhancementProviders.screenCurtain import WarnOnLoadDialog
+
+				parent = gui.mainFrame
+				dlg = WarnOnLoadDialog(
 					screenCurtainSettingsStorage=settingsStorage,
-					parent=gui.mainFrame,
+					parent=parent,
 				)
 				self._waitingOnScreenCurtainWarningDialog = dlg
 				gui.runScriptModalDialog(
@@ -4940,10 +5034,9 @@ def _enableScreenCurtain(doEnable: bool = True):
 					isinstance(focusObj, RefreshableRecogResultNVDAObject)
 					and focusObj.recognizer.allowAutoRefresh
 				):
-					ui.message(
-						screenCurtain._screenCurtain.UNAVAILABLE_WHEN_RECOGNISING_CONTENT_MESSAGE,
-						speechPriority=speech.priorities.Spri.NOW,
-					)
+					# Translators: Warning message when trying to enable the screen curtain when OCR is active.
+					warningMessage = _("Could not enable screen curtain when performing content recognition")
+					ui.message(warningMessage, speechPriority=speech.priorities.Spri.NOW)
 					return
 				_enableScreenCurtain()
 
@@ -5110,26 +5203,21 @@ def script_sendSAS(self, gesture: "inputCore.InputGesture"):
 		_remoteClient._remoteClient.sendSAS()
 
 	@script(
-		description=pgettext(
-			"imageDesc",
 		# Translators: Description for the image caption script
-			"Get an AI-generated image description of the navigator object.",
-		),
+		description=pgettext("imageDesc", "Get an AI generated image description"),
 		category=SCRCAT_IMAGE_DESC,
-		gesture="kb:NVDA+g",
+		gesture="kb:NVDA+windows+,",
 	)
 	@gui.blockAction.when(gui.blockAction.Context.SCREEN_CURTAIN)
 	def script_runCaption(self, gesture: "inputCore.InputGesture"):
 		_localCaptioner._localCaptioner.runCaption(gesture)
 
 	@script(
-		description=pgettext(
-			"imageDesc",
 		# Translators: Description for the toggle image captioning script
-			"Load or unload the image captioner",
-		),
+		description=pgettext("imageDesc", "Toggle image captioning"),
 		category=SCRCAT_IMAGE_DESC,
 	)
+	@gui.blockAction.when(gui.blockAction.Context.SCREEN_CURTAIN)
 	def script_toggleImageCaptioning(self, gesture: "inputCore.InputGesture"):
 		_localCaptioner._localCaptioner.toggleImageCaptioning(gesture)
 

```