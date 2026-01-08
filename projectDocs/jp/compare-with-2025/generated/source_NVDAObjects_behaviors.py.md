# Diff for: `source\NVDAObjects\behaviors.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\behaviors.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\behaviors.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\behaviors.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\behaviors.py"
index 0aa6eea..74ccab1 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\behaviors.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\behaviors.py"
@@ -2,7 +2,7 @@
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 # Copyright (C) 2006-2025 NV Access Limited, Peter Vágner, Joseph Lee, Bill Dengler,
-# Burman's Computer and Education Ltd, Cary-rowen
+# Burman's Computer and Education Ltd, Cary-rowen, Cyrille Bougot
 
 """Mix-in classes which provide common behaviour for particular types of controls across different APIs.
 Behaviors described in this mix-in include providing table navigation commands for certain table rows, terminal input and output support, announcing notifications and suggestion items and so on.
@@ -31,7 +31,10 @@
 import globalVars
 from typing import List, Union
 import diffHandler
-from config.configFlags import TypingEcho
+from config.configFlags import (
+	TypingEcho,
+	ReportSpellingErrors,
+)
 
 
 class ProgressBar(NVDAObject):
@@ -291,13 +294,14 @@ def _delayedDetection():
 			else:
 				# No error.
 				return
+			if speech.getState().speechMode not in [speech.SpeechMode.off, speech.SpeechMode.onDemand]:
 				nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", "textError.wav"))
 
 		core.callLater(50, _delayedDetection)
 
 	def event_typedCharacter(self, ch: str):
 		if (
-			config.conf["documentFormatting"]["reportSpellingErrors"]
+			config.conf["documentFormatting"]["reportSpellingErrors2"] != ReportSpellingErrors.OFF.value
 			and config.conf["keyboard"]["alertForSpellingErrors"]
 			and (
 				# Not alpha, apostrophe or control.
@@ -632,7 +636,8 @@ class KeyboardHandlerBasedTypedCharSupport(EnhancedTermTypedCharSupport):
 
 class CandidateItem(NVDAObject):
 	def getFormattedCandidateName(self, number, candidate):
-		# nvdajp begin
+		# BEGIN JP PATCH
+		# nvdajp: use discriminant reading for candidate names when nvdajpEnableKeyEvents is enabled
 		import jpUtils
 
 		if config.conf["keyboard"]["nvdajpEnableKeyEvents"]:
@@ -642,7 +647,7 @@ def getFormattedCandidateName(self, number, candidate):
 			if config.conf["language"]["announceCandidateNumber"]:
 				return _("{number} {candidate}").format(number=number, candidate=c)
 			return c
-		# nvdajp end
+		# END JP PATCH
 		if config.conf["inputComposition"]["alwaysIncludeShortCharacterDescriptionInCandidateName"]:
 			describedSymbols = []
 			for symbol in candidate:

```