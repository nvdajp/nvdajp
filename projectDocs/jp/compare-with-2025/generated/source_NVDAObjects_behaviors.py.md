# Diff for: `source\NVDAObjects\behaviors.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\behaviors.py`  
**Current**: `F:\nvda\gh\alphajp\source\NVDAObjects\behaviors.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\behaviors.py" "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\behaviors.py"
index 0aa6eea738..c92ec76137 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\behaviors.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\behaviors.py"
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
@@ -297,7 +300,7 @@ def _delayedDetection():
 
 	def event_typedCharacter(self, ch: str):
 		if (
-			config.conf["documentFormatting"]["reportSpellingErrors"]
+			config.conf["documentFormatting"]["reportSpellingErrors2"] != ReportSpellingErrors.OFF.value
 			and config.conf["keyboard"]["alertForSpellingErrors"]
 			and (
 				# Not alpha, apostrophe or control.
@@ -632,17 +635,6 @@ class KeyboardHandlerBasedTypedCharSupport(EnhancedTermTypedCharSupport):
 
 class CandidateItem(NVDAObject):
 	def getFormattedCandidateName(self, number, candidate):
-		# nvdajp begin
-		import jpUtils
-
-		if config.conf["keyboard"]["nvdajpEnableKeyEvents"]:
-			fb = braille.handler.displaySize > 0
-			c = jpUtils.getDiscriminantReading(candidate, forBraille=fb)
-			log.debug("{number} {candidate} {c}".format(number=number, candidate=candidate, c=c))
-			if config.conf["language"]["announceCandidateNumber"]:
-				return _("{number} {candidate}").format(number=number, candidate=c)
-			return c
-		# nvdajp end
 		if config.conf["inputComposition"]["alwaysIncludeShortCharacterDescriptionInCandidateName"]:
 			describedSymbols = []
 			for symbol in candidate:

```