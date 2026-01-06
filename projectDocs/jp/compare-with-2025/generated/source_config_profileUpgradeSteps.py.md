# Diff for: `source\config\profileUpgradeSteps.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\config\profileUpgradeSteps.py`  
**Current**: `F:\nvda\gh\alphajp\source\config\profileUpgradeSteps.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\config\\profileUpgradeSteps.py" "b/F:\\nvda\\gh\\alphajp\\source\\config\\profileUpgradeSteps.py"
index fbc35e379b..d19a848a1f 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\config\\profileUpgradeSteps.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\config\\profileUpgradeSteps.py"
@@ -24,6 +24,7 @@
 	OutputMode,
 	ReportCellBorders,
 	ReportLineIndentation,
+	ReportSpellingErrors,
 	ReportTableHeaders,
 	ShowMessages,
 	TetherTo,
@@ -597,3 +598,27 @@ def upgradeConfigFrom_17_to_18(profile: ConfigObj) -> None:
 			"dotPad added to braille display auto detection excluded displays due to generic USB PID/VID. "
 			f"List is now: {excludedDisplays}",
 		)
+
+
+def upgradeConfigFrom_18_to_19(profile: ConfigObj):
+	"""Convert report spelling errors configurations from boolean to integer values."""
+
+	section = "documentFormatting"
+	key = "reportSpellingErrors"
+	newKey = "reportSpellingErrors2"
+	try:
+		oldValue: bool = profile[section].as_bool(key)
+	except KeyError:
+		log.debug(f"'{key}' not present in config, no action taken.")
+		return
+	except ValueError:
+		log.error(f"'{key}' is not a boolean, got {profile[section][key]!r}. No action taken.")
+		return
+
+	newValue = ReportSpellingErrors.SPEECH.value if oldValue else ReportSpellingErrors.OFF.value
+	profile[section][newKey] = newValue
+	del profile[section][key]
+	log.debug(
+		f"Converted '{key}' with value {oldValue} to '{newKey}' with value {newValue}"
+		f" ({ReportSpellingErrors(newValue).name}). The old key '{key}' has been deleted.",
+	)

```