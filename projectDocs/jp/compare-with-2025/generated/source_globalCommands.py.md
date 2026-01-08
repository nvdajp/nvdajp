# Diff for: `source\globalCommands.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\globalCommands.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\globalCommands.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\globalCommands.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\globalCommands.py"
index 2aa2cab..4f6be3e 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\globalCommands.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\globalCommands.py"
@@ -7,7 +7,6 @@
 # Julien Cochuyt, Jakub Lukowicz, Bill Dengler, Cyrille Bougot, Rob Meredith, Luke Davis,
 # Burman's Computer and Education Ltd, Cary-rowen.
 
-import jpUtils
 import itertools
 from typing import (
 	Optional,
@@ -46,6 +45,7 @@
 	BrailleMode,
 	OutputMode,
 	TypingEcho,
+	ReportSpellingErrors,
 )
 from config.featureFlag import FeatureFlag
 from config.featureFlagEnums import BoolFlag
@@ -64,6 +64,7 @@
 import characterProcessing
 from baseObject import ScriptableObject
 import core
+import jpUtils  # nvdajp
 from winAPI._powerTracking import reportCurrentBatteryStatus
 import winVersion
 from base64 import b16encode
@@ -73,6 +74,7 @@
 import synthDriverHandler
 from utils.displayString import DisplayStringEnum
 import _remoteClient
+import _localCaptioner
 
 #: Script category for text review commands.
 # Translators: The name of a category of NVDA commands.
@@ -125,6 +127,9 @@
 #: Script category for Remote Access commands.
 # Translators: The name of a category of NVDA commands.
 SCRCAT_REMOTE = pgettext("remote", "Remote Access")
+#: Script category for image description commands.
+# Translators: The name of a category of NVDA commands.
+SCRCAT_IMAGE_DESC = pgettext("imageDesc", "Image Descriptions")
 
 # Translators: Reported when there are no settings to configure in synth settings ring
 # (example: when there is no setting for language).
@@ -181,7 +186,9 @@ def toggleIntegerValue(
 	ui.message(msg)
 
 
+# BEGIN JP PATCH (character description mode)
 characterDescriptionMode = True
+# END JP PATCH
 
 
 class GlobalCommands(ScriptableObject):
@@ -278,11 +285,13 @@ def script_reportCurrentLine(self, gesture):
 		if scriptCount == 0:
 			speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)
 		else:
+			# BEGIN JP PATCH (character description mode)
 			speech.spellTextInfo(
 				info,
 				useCharacterDescriptions=scriptCount > 1,
 				useDetails=characterDescriptionMode if scriptCount > 1 else False,
 			)
+			# END JP PATCH
 
 	@script(
 		# Translators: Input help mode message for left mouse click command.
@@ -411,9 +420,11 @@ def script_reportCurrentSelection(self, gesture):
 				return
 
 			elif len(info.text) < speech.speech.MAX_LENGTH_FOR_SELECTION_REPORTING:
+				# BEGIN JP PATCH (character description mode)
 				speech.speakSpelling(
 					info.text, useCharacterDescriptions=scriptCount > 1, useDetails=scriptCount > 1
 				)
+				# END JP PATCH
 			else:
 				speech.speakTextSelected(info.text)
 				braille.handler.message(selectMessage)
@@ -456,7 +467,6 @@ def script_dateTime(self, gesture):
 					None,
 					None,
 				)
-				text = jpUtils.modifyTimeText(text)
 		else:
 			text = winKernel.GetDateFormatEx(
 				winKernel.LOCALE_NAME_USER_DEFAULT,
@@ -799,19 +809,39 @@ def script_toggleReportStyle(self, gesture):
 
 	@script(
 		# Translators: Input help mode message for toggle report spelling errors command.
-		description=_("Toggles on and off the reporting of spelling errors"),
+		description=_("Cycles through options for how to report spelling or grammar errors"),
+		category=SCRCAT_DOCUMENTFORMATTING,
+	)
+	def script_toggleReportSpellingErrors(self, gesture: inputCore.InputGesture):
+		currentValue = config.conf["documentFormatting"]["reportSpellingErrors2"]
+		newValue = ((currentValue + 1) % ReportSpellingErrors.BRAILLE) | (
+			currentValue & ReportSpellingErrors.BRAILLE
+		)
+		config.conf["documentFormatting"]["reportSpellingErrors2"] = newValue
+		ui.message(
+			# Translators: Reported when the user cycles through the choices to report spelling or grammar errors.
+			# {mode} will be replaced with the mode; e.g. Off, Speech, Sound, Speech and sound.
+			_("Report errors {mode}").format(
+				mode=ReportSpellingErrors(newValue & ~ReportSpellingErrors.BRAILLE).displayString,
+			),
+		)
+
+	@script(
+		# Translators: Input help mode message for command to toggle report spelling or grammar errors in braille.
+		description=_("Toggles reporting spelling or grammar errors in braille"),
 		category=SCRCAT_DOCUMENTFORMATTING,
 	)
-	def script_toggleReportSpellingErrors(self, gesture):
-		if config.conf["documentFormatting"]["reportSpellingErrors"]:
-			# Translators: The message announced when toggling the report spelling errors document formatting setting.
-			state = _("report spelling errors off")
-			config.conf["documentFormatting"]["reportSpellingErrors"] = False
+	def script_toggleReportSpellingErrorsInBraille(self, gesture: inputCore.InputGesture):
+		formatConfig = config.conf["documentFormatting"]["reportSpellingErrors2"]
+		config.conf["documentFormatting"]["reportSpellingErrors2"] = (
+			formatConfig ^ ReportSpellingErrors.BRAILLE
+		)
+		if config.conf["documentFormatting"]["reportSpellingErrors2"] & ReportSpellingErrors.BRAILLE:
+			# Translators: Message presented when turning on reporting spelling or grammar errors in braille.
+			ui.message(_("Report errors in braille on"))
 		else:
-			# Translators: The message announced when toggling the report spelling errors document formatting setting.
-			state = _("report spelling errors on")
-			config.conf["documentFormatting"]["reportSpellingErrors"] = True
-		ui.message(state)
+			# Translators: Message presented when turning off reporting spelling errors or grammar in braille.
+			ui.message(_("Report errors in braille off"))
 
 	@script(
 		# Translators: Input help mode message for toggle report pages command.
@@ -1422,11 +1452,13 @@ def script_navigatorObject_current(self, gesture: inputCore.InputGesture):
 			text = " ".join(textList)
 			if len(text) > 0 and not text.isspace():
 				if scriptHandler.getLastScriptRepeatCount() == 1:
+					# BEGIN JP PATCH (character description mode)
 					speech.speakSpelling(
 						text,
 						useCharacterDescriptions=characterDescriptionMode,
 						useDetails=characterDescriptionMode,
 					)
+					# END JP PATCH
 				else:
 					api.copyToClip(text, notify=True)
 		else:
@@ -1861,11 +1893,13 @@ def script_review_currentLine(self, gesture: inputCore.InputGesture):
 		if scriptCount == 0:
 			speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)
 		else:
+			# BEGIN JP PATCH (character description mode)
 			speech.spellTextInfo(
 				info,
 				useCharacterDescriptions=scriptCount > 1,
 				useDetails=characterDescriptionMode if scriptCount > 1 else False,
 			)
+			# END JP PATCH
 
 	@script(
 		description=_(
@@ -2067,7 +2101,7 @@ def script_review_currentWord(self, gesture: inputCore.InputGesture):
 			speech.spellTextInfo(
 				info,
 				useCharacterDescriptions=(scriptCount > 1),
-				useDetails=(scriptCount > 1 and characterDescriptionMode),
+				useDetails=(scriptCount > 1 and characterDescriptionMode),  # nvdajp
 			)
 
 	@script(
@@ -2186,7 +2220,7 @@ def script_review_previousCharacter(self, gesture: inputCore.InputGesture):
 		speakOnDemand=True,
 	)
 	def script_review_currentCharacter(self, gesture: inputCore.InputGesture):
-		global characterDescriptionMode
+		global characterDescriptionMode  # nvdajp
 		info = api.getReviewPosition().copy()
 		# This script is available on the lock screen via getSafeScripts, as such
 		# ensure the review position does not contain secure information
@@ -2200,12 +2234,17 @@ def script_review_currentCharacter(self, gesture: inputCore.InputGesture):
 		braille.handler.handleReviewMove(shouldAutoTether=True)
 		scriptCount = scriptHandler.getLastScriptRepeatCount()
 		if scriptCount == 0:
+			# BEGIN JP PATCH (character description mode)
 			speech.spellTextInfo(info, useCharacterDescriptions=characterDescriptionMode)
 			braille.handler.message(jpUtils.getDescriptionForBraille(info.text))
+			# END JP PATCH
 		elif scriptCount == 1:
+			# BEGIN JP PATCH (character description mode)
 			speech.spellTextInfo(info, useCharacterDescriptions=True, useDetails=True)
 			braille.handler.message(jpUtils.getDescriptionForBraille(info.text))
+			# END JP PATCH
 		elif scriptCount == 2:
+			# BEGIN JP PATCH (character description mode)
 			try:
 				cList = [ord(c) for c in info.text]
 			except TypeError:
@@ -2230,7 +2269,9 @@ def script_review_currentCharacter(self, gesture: inputCore.InputGesture):
 					unit=textInfos.UNIT_CHARACTER,
 					reason=controlTypes.OutputReason.CARET,
 				)
+			# END JP PATCH
 		else:
+			# BEGIN JP PATCH (character description mode toggle)
 			if characterDescriptionMode:
 				# Translators: character description mode
 				ui.message(_("Character description mode disabled"))
@@ -2239,6 +2280,7 @@ def script_review_currentCharacter(self, gesture: inputCore.InputGesture):
 				# Translators: character description mode
 				ui.message(_("Character description mode enabled"))
 				characterDescriptionMode = True
+			# END JP PATCH
 
 	@script(
 		description=_(
@@ -2530,7 +2572,9 @@ def script_restart(self, gesture):
 	@script(
 		# Translators: Input help mode message for show NVDA menu command.
 		description=_("Shows the NVDA menu"),
+		# BEGIN JP PATCH
 		allowInSleepMode=True,
+		# END JP PATCH
 		gestures=("kb:NVDA+n", "ts:2finger_double_tap"),
 	)
 	@gui.blockAction.when(gui.blockAction.Context.MODAL_DIALOG_OPEN)
@@ -2578,7 +2622,7 @@ def _reportFormattingHelper(self, info, browseable=False):
 			"reportColor",
 			"reportStyle",
 			"reportAlignment",
-			"reportSpellingErrors",
+			"reportSpellingErrors2",
 			"reportLineIndentation",
 			"reportParagraphIndentation",
 			"reportLineSpacing",
@@ -2878,11 +2922,13 @@ def script_reportCurrentFocus(self, gesture: inputCore.InputGesture):
 			text = " ".join(s for s in speechList if isinstance(s, str))
 			braille.handler.message(text)
 		else:
+			# BEGIN JP PATCH (character description mode)
 			speech.speakSpelling(
 				focusObject.name,
 				useCharacterDescriptions=repeatCount > 1 and characterDescriptionMode,
 				useDetails=repeatCount > 1 and characterDescriptionMode,
 			)
+			# END JP PATCH
 
 	@staticmethod
 	def _getStatusBarText(setReviewCursor: bool = False) -> Optional[str]:
@@ -2967,9 +3013,11 @@ def script_spellStatusLine(self, gesture):
 			# Translators: Reported when status line exist, but is empty.
 			ui.message(_("no status bar information"))
 		else:
+			# BEGIN JP PATCH (character description mode)
 			speech.speakSpelling(
 				text, useCharacterDescriptions=characterDescriptionMode, useDetails=characterDescriptionMode
 			)
+			# END JP PATCH
 
 	@script(
 		description=_(
@@ -3066,6 +3114,23 @@ def script_toggleMouseTracking(self, gesture):
 			config.conf["mouse"]["enableMouseTracking"] = True
 		ui.message(state)
 
+	@script(
+		# Translators: Input help mode message for toggle mouse audio coordinates command.
+		description=_("Toggles beeps that report mouse coordinates as the mouse moves"),
+		category=SCRCAT_MOUSE,
+	)
+	def script_toggleMouseAudioCoordinates(self, gesture: inputCore.InputGesture):
+		# Translators: Reported when mouse audio coordinates are toggled on.
+		enabledMsg = _("Mouse audio coordinates on")
+		# Translators: Reported when mouse audio coordinates are toggled off.
+		disabledMsg = _("Mouse audio coordinates off")
+		toggleBooleanValue(
+			configSection="mouse",
+			configKey="audioCoordinatesOnMouseMove",
+			enabledMsg=enabledMsg,
+			disabledMsg=disabledMsg,
+		)
+
 	@script(
 		# Translators: Input help mode message for toggle mouse text unit resolution command.
 		description=_("Toggles how much text will be spoken when the mouse moves"),
@@ -3116,9 +3181,11 @@ def script_title(self, gesture: inputCore.InputGesture):
 		if repeatCount == 0:
 			ui.message(title)
 		elif repeatCount == 1:
+			# BEGIN JP PATCH (character description mode)
 			speech.speakSpelling(
 				title, useCharacterDescriptions=characterDescriptionMode, useDetails=characterDescriptionMode
 			)
+			# END JP PATCH
 		else:
 			api.copyToClip(title, notify=True)
 
@@ -3412,6 +3479,15 @@ def script_activateBrailleSettingsDialog(self, gesture):
 	def script_activateAudioSettingsDialog(self, gesture):
 		wx.CallAfter(gui.mainFrame.onAudioSettingsCommand, None)
 
+	@script(
+		# Translators: Input help mode message for go to privacy and security settings command.
+		description=_("Shows NVDA's privacy and security settings"),
+		category=SCRCAT_CONFIG,
+	)
+	@gui.blockAction.when(gui.blockAction.Context.MODAL_DIALOG_OPEN)
+	def script_activatePrivacyAndSecuritySettings(self, gesture: inputCore.InputGesture) -> None:
+		wx.CallAfter(gui.mainFrame.onPrivacyAndSecuritySettingsCommand, None)
+
 	@script(
 		# Translators: Input help mode message for go to vision settings command.
 		description=_("Shows NVDA's vision settings"),
@@ -3498,6 +3574,15 @@ def script_activateDocumentFormattingDialog(self, gesture):
 	def script_activateRemoteAccessSettings(self, gesture: "inputCore.InputGesture"):
 		wx.CallAfter(gui.mainFrame.onRemoteAccessSettingsCommand, None)
 
+	@script(
+		# Translators: Input help mode message for go to local captioner settings command.
+		description=pgettext("imageDesc", "Shows the AI image descriptions settings"),
+		category=SCRCAT_CONFIG,
+	)
+	@gui.blockAction.when(gui.blockAction.Context.MODAL_DIALOG_OPEN)
+	def script_activateLocalCaptionerSettings(self, gesture: "inputCore.InputGesture"):
+		wx.CallAfter(gui.mainFrame.onLocalCaptionerSettingsCommand, None)
+
 	@script(
 		# Translators: Input help mode message for go to Add-on Store settings command.
 		description=_("Shows NVDA's Add-on Store settings"),
@@ -3983,9 +4068,11 @@ def script_reportClipboardText(self, gesture):
 			if repeatCount == 0:
 				ui.message(text)
 			else:
+				# BEGIN JP PATCH (character description mode)
 				speech.speakSpelling(
 					text, useCharacterDescriptions=repeatCount > 1, useDetails=repeatCount > 1
 				)
+				# END JP PATCH
 		else:
 			ui.message(
 				ngettext(
@@ -4915,8 +5002,7 @@ def _enableScreenCurtain(doEnable: bool = True):
 						)
 				except Exception:
 					log.error("Screen curtain initialization error", exc_info=True)
-					# Translators: Reported when the screen curtain could not be enabled.
-					enableMessage = _("Could not enable screen curtain")
+					enableMessage = screenCurtain._screenCurtain.ERROR_ENABLING_MESSAGE
 				finally:
 					self._toggleScreenCurtainMessage = enableMessage
 					ui.message(enableMessage, speechPriority=speech.priorities.Spri.NOW)
@@ -5116,6 +5202,25 @@ def script_sendKeys(self, gesture: "inputCore.InputGesture"):
 	def script_sendSAS(self, gesture: "inputCore.InputGesture"):
 		_remoteClient._remoteClient.sendSAS()
 
+	@script(
+		# Translators: Description for the image caption script
+		description=pgettext("imageDesc", "Get an AI generated image description"),
+		category=SCRCAT_IMAGE_DESC,
+		gesture="kb:NVDA+windows+,",
+	)
+	@gui.blockAction.when(gui.blockAction.Context.SCREEN_CURTAIN)
+	def script_runCaption(self, gesture: "inputCore.InputGesture"):
+		_localCaptioner._localCaptioner.runCaption(gesture)
+
+	@script(
+		# Translators: Description for the toggle image captioning script
+		description=pgettext("imageDesc", "Toggle image captioning"),
+		category=SCRCAT_IMAGE_DESC,
+	)
+	@gui.blockAction.when(gui.blockAction.Context.SCREEN_CURTAIN)
+	def script_toggleImageCaptioning(self, gesture: "inputCore.InputGesture"):
+		_localCaptioner._localCaptioner.toggleImageCaptioning(gesture)
+
 
 #: The single global commands instance.
 #: @type: L{GlobalCommands}

```