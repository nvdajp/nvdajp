# Diff for: `source\globalCommands.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\globalCommands.py`  
**Current**: `F:\nvda\gh\alphajp\source\globalCommands.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\globalCommands.py" "b/F:\\nvda\\gh\\alphajp\\source\\globalCommands.py"
index 2aa2cab186..03c19d9573 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\globalCommands.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\globalCommands.py"
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
@@ -181,7 +182,9 @@ def toggleIntegerValue(
 	ui.message(msg)
 
 
+# BEGIN JP PATCH (character description mode)
 characterDescriptionMode = True
+# END JP PATCH
 
 
 class GlobalCommands(ScriptableObject):
@@ -278,11 +281,13 @@ def script_reportCurrentLine(self, gesture):
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
@@ -411,9 +416,11 @@ def script_reportCurrentSelection(self, gesture):
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
@@ -456,7 +463,6 @@ def script_dateTime(self, gesture):
 					None,
 					None,
 				)
-				text = jpUtils.modifyTimeText(text)
 		else:
 			text = winKernel.GetDateFormatEx(
 				winKernel.LOCALE_NAME_USER_DEFAULT,
@@ -799,19 +805,18 @@ def script_toggleReportStyle(self, gesture):
 
 	@script(
 		# Translators: Input help mode message for toggle report spelling errors command.
-		description=_("Toggles on and off the reporting of spelling errors"),
+		description=_("Cycles through options for how to report spelling errors"),
 		category=SCRCAT_DOCUMENTFORMATTING,
 	)
-	def script_toggleReportSpellingErrors(self, gesture):
-		if config.conf["documentFormatting"]["reportSpellingErrors"]:
-			# Translators: The message announced when toggling the report spelling errors document formatting setting.
-			state = _("report spelling errors off")
-			config.conf["documentFormatting"]["reportSpellingErrors"] = False
-		else:
-			# Translators: The message announced when toggling the report spelling errors document formatting setting.
-			state = _("report spelling errors on")
-			config.conf["documentFormatting"]["reportSpellingErrors"] = True
-		ui.message(state)
+	def script_toggleReportSpellingErrors(self, gesture: inputCore.InputGesture):
+		toggleIntegerValue(
+			configSection="documentFormatting",
+			configKey="reportSpellingErrors2",
+			enumClass=ReportSpellingErrors,
+			# Translators: Reported when the user cycles through the choices to report spelling errors.
+			# {mode} will be replaced with the mode; e.g. Off, Speech, Sound.
+			messageTemplate=_("Report spelling errors {mode}"),
+		)
 
 	@script(
 		# Translators: Input help mode message for toggle report pages command.
@@ -1422,11 +1427,13 @@ def script_navigatorObject_current(self, gesture: inputCore.InputGesture):
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
@@ -1861,11 +1868,13 @@ def script_review_currentLine(self, gesture: inputCore.InputGesture):
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
@@ -2067,7 +2076,7 @@ def script_review_currentWord(self, gesture: inputCore.InputGesture):
 			speech.spellTextInfo(
 				info,
 				useCharacterDescriptions=(scriptCount > 1),
-				useDetails=(scriptCount > 1 and characterDescriptionMode),
+				useDetails=(scriptCount > 1 and characterDescriptionMode),  # nvdajp
 			)
 
 	@script(
@@ -2186,7 +2195,7 @@ def script_review_previousCharacter(self, gesture: inputCore.InputGesture):
 		speakOnDemand=True,
 	)
 	def script_review_currentCharacter(self, gesture: inputCore.InputGesture):
-		global characterDescriptionMode
+		global characterDescriptionMode  # nvdajp
 		info = api.getReviewPosition().copy()
 		# This script is available on the lock screen via getSafeScripts, as such
 		# ensure the review position does not contain secure information
@@ -2200,12 +2209,17 @@ def script_review_currentCharacter(self, gesture: inputCore.InputGesture):
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
@@ -2230,7 +2244,9 @@ def script_review_currentCharacter(self, gesture: inputCore.InputGesture):
 					unit=textInfos.UNIT_CHARACTER,
 					reason=controlTypes.OutputReason.CARET,
 				)
+			# END JP PATCH
 		else:
+			# BEGIN JP PATCH (character description mode toggle)
 			if characterDescriptionMode:
 				# Translators: character description mode
 				ui.message(_("Character description mode disabled"))
@@ -2239,6 +2255,7 @@ def script_review_currentCharacter(self, gesture: inputCore.InputGesture):
 				# Translators: character description mode
 				ui.message(_("Character description mode enabled"))
 				characterDescriptionMode = True
+			# END JP PATCH
 
 	@script(
 		description=_(
@@ -2530,7 +2547,9 @@ def script_restart(self, gesture):
 	@script(
 		# Translators: Input help mode message for show NVDA menu command.
 		description=_("Shows the NVDA menu"),
+		# BEGIN JP PATCH
 		allowInSleepMode=True,
+		# END JP PATCH
 		gestures=("kb:NVDA+n", "ts:2finger_double_tap"),
 	)
 	@gui.blockAction.when(gui.blockAction.Context.MODAL_DIALOG_OPEN)
@@ -2578,7 +2597,7 @@ def _reportFormattingHelper(self, info, browseable=False):
 			"reportColor",
 			"reportStyle",
 			"reportAlignment",
-			"reportSpellingErrors",
+			"reportSpellingErrors2",
 			"reportLineIndentation",
 			"reportParagraphIndentation",
 			"reportLineSpacing",
@@ -2878,11 +2897,13 @@ def script_reportCurrentFocus(self, gesture: inputCore.InputGesture):
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
@@ -2967,9 +2988,11 @@ def script_spellStatusLine(self, gesture):
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
@@ -3116,9 +3139,11 @@ def script_title(self, gesture: inputCore.InputGesture):
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
 
@@ -3983,9 +4008,11 @@ def script_reportClipboardText(self, gesture):
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

```