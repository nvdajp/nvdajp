# Diff for: `source\globalCommands.py`

**Source**: `F:\nvda\gh\beta\source\globalCommands.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\globalCommands.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\globalCommands.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\globalCommands.py"
index 432b35c..7ca2771 100644
--- "a/F:\\nvda\\gh\\beta\\source\\globalCommands.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\globalCommands.py"
@@ -64,6 +64,7 @@
 import characterProcessing
 from baseObject import ScriptableObject
 import core
+import jpUtils  # nvdajp
 from winAPI._powerTracking import reportCurrentBatteryStatus
 import winVersion
 from base64 import b16encode
@@ -184,6 +185,11 @@ def toggleIntegerValue(
 	ui.message(msg)
 
 
+# BEGIN JP PATCH (character description mode)
+characterDescriptionMode = True
+# END JP PATCH
+
+
 class GlobalCommands(ScriptableObject):
 	"""Commands that are available at all times, regardless of the current focus."""
 
@@ -278,7 +284,13 @@ def script_reportCurrentLine(self, gesture):
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
@@ -407,7 +419,11 @@ def script_reportCurrentSelection(self, gesture):
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
@@ -1435,7 +1451,13 @@ def script_navigatorObject_current(self, gesture: inputCore.InputGesture):
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
@@ -1870,7 +1892,13 @@ def script_review_currentLine(self, gesture: inputCore.InputGesture):
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
@@ -2069,7 +2097,11 @@ def script_review_currentWord(self, gesture: inputCore.InputGesture):
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
@@ -2187,6 +2219,7 @@ def script_review_previousCharacter(self, gesture: inputCore.InputGesture):
 		speakOnDemand=True,
 	)
 	def script_review_currentCharacter(self, gesture: inputCore.InputGesture):
+		global characterDescriptionMode  # nvdajp
 		info = api.getReviewPosition().copy()
 		# This script is available on the lock screen via getSafeScripts, as such
 		# ensure the review position does not contain secure information
@@ -2200,15 +2233,28 @@ def script_review_currentCharacter(self, gesture: inputCore.InputGesture):
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
@@ -2222,6 +2268,18 @@ def script_review_currentCharacter(self, gesture: inputCore.InputGesture):
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
@@ -2513,6 +2571,9 @@ def script_restart(self, gesture):
 	@script(
 		# Translators: Input help mode message for show NVDA menu command.
 		description=_("Shows the NVDA menu"),
+		# BEGIN JP PATCH
+		allowInSleepMode=True,
+		# END JP PATCH
 		gestures=("kb:NVDA+n", "ts:2finger_double_tap"),
 	)
 	@gui.blockAction.when(gui.blockAction.Context.MODAL_DIALOG_OPEN)
@@ -2860,7 +2921,13 @@ def script_reportCurrentFocus(self, gesture: inputCore.InputGesture):
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
@@ -2945,7 +3012,11 @@ def script_spellStatusLine(self, gesture):
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
@@ -3109,7 +3180,11 @@ def script_title(self, gesture: inputCore.InputGesture):
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
 
@@ -3992,7 +4067,11 @@ def script_reportClipboardText(self, gesture):
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

```