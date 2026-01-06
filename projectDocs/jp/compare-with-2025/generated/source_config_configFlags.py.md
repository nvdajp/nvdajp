# Diff for: `source\config\configFlags.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\config\configFlags.py`  
**Current**: `F:\nvda\gh\alphajp\source\config\configFlags.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\config\\configFlags.py" "b/F:\\nvda\\gh\\alphajp\\source\\config\\configFlags.py"
index 5b3d5bc863..dd1ce7aa69 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\config\\configFlags.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\config\\configFlags.py"
@@ -180,6 +180,39 @@ def _displayStringLabels(self):
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
+		}
+
+
 @unique
 class ReportTableHeaders(DisplayStringIntEnum):
 	"""Enumeration containing the possible config values to report table headers.

```