# Diff for: `source\config\configFlags.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\config\configFlags.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\config\configFlags.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\config\\configFlags.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\configFlags.py"
index 5b3d5bc..0fa86af 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\config\\configFlags.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\configFlags.py"
@@ -13,6 +13,7 @@
 
 from typing import TYPE_CHECKING
 from enum import unique, verify, CONTINUOUS
+from logHandler import Logger
 from utils.displayString import (
 	DisplayStringFlag,
 	DisplayStringIntEnum,
@@ -180,6 +181,42 @@ def _displayStringLabels(self):
 		}
 
 
+@unique
+class ReportSpellingErrors(DisplayStringIntFlag):
+	"""IntFlag enumeration containing the possible config values to report spelling errors while reading.
+
+	Use ReportSpellingErrors.MEMBER.value to compare with the config;
+	the config stores a bitwise combination of zero, one or more of these values.
+	Use ReportSpellingErrors.MEMBER.displayString in the UI for a translatable description of this member.
+	"""
+
+	OFF = 0b0
+	SPEECH = 0b1
+	SOUND = 0b10
+	SPEECH_AND_SOUND = SPEECH | SOUND
+	BRAILLE = 0b100
+
+	@property
+	def _displayStringLabels(self) -> dict["ReportSpellingErrors", str]:
+		return {
+			# Translators: A value reported by the cycle script defining how spelling errors are reported.
+			ReportSpellingErrors.OFF: pgettext("reportSpellingErrorsSetting", "Off"),
+			# Translators: A value reported by the cycle script defining how spelling errors are reported, also used
+			# as choice in a checklist box in the document formatting dialog to report spelling errors with speech.
+			ReportSpellingErrors.SPEECH: pgettext("reportSpellingErrorsSetting", "Speech"),
+			# Translators: A value reported by the cycle script defining how spelling errors are reported, also used
+			# as choice in a checklist box in the document formatting dialog to report spelling errors with a sound.
+			ReportSpellingErrors.SOUND: pgettext("reportSpellingErrorsSetting", "Sound"),
+			ReportSpellingErrors.SPEECH_AND_SOUND: pgettext(
+				"reportSpellingErrorsSetting",
+				# Translators: A value reported by the cycle script defining how spelling errors are reported.
+				"Speech and sound",
+			),
+			# Translators: A value used as choice in a checklist box in the document formatting dialog to report spelling errors in braille.
+			ReportSpellingErrors.BRAILLE: pgettext("reportSpellingErrorsSetting", "Braille"),
+		}
+
+
 @unique
 class ReportTableHeaders(DisplayStringIntEnum):
 	"""Enumeration containing the possible config values to report table headers.
@@ -370,3 +407,32 @@ def _displayStringLabels(self):
 			# Translators: Use NVDA as the Remote control server
 			RemoteServerType.LOCAL: pgettext("remote", "Host locally"),
 		}
+
+
+class LoggingLevel(DisplayStringIntEnum):
+	"""Enumeration containing the possible logging levels.
+
+	Use LoggingLevel.MEMBER.value to compare with the config;
+	use LoggingLevel.MEMBER.displayString in the UI for a translatable description of this member.
+	"""
+
+	OFF = Logger.OFF
+	INFO = Logger.INFO
+	DEBUGWARNING = Logger.DEBUGWARNING
+	IO = Logger.IO
+	DEBUG = Logger.DEBUG
+
+	@property
+	def _displayStringLabels(self) -> dict[int, str]:
+		return {
+			# Translators: One of the log levels of NVDA (the disabled mode turns off logging completely).
+			self.OFF: _("disabled"),
+			# Translators: One of the log levels of NVDA (the info mode shows info as NVDA runs).
+			self.INFO: _("info"),
+			# Translators: One of the log levels of NVDA (the debug warning shows debugging messages and warnings as NVDA runs).
+			self.DEBUGWARNING: _("debug warning"),
+			# Translators: One of the log levels of NVDA (the input/output shows keyboard commands and/or braille commands as well as speech and/or braille output of NVDA).
+			self.IO: _("input/output"),
+			# Translators: One of the log levels of NVDA (the debug mode shows debug messages as NVDA runs).
+			self.DEBUG: _("debug"),
+		}

```