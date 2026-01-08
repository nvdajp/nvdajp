# Diff for: `source\config\profileUpgradeSteps.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\config\profileUpgradeSteps.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\config\profileUpgradeSteps.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\config\\profileUpgradeSteps.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\profileUpgradeSteps.py"
index fbc35e3..8c4a22e 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\config\\profileUpgradeSteps.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\profileUpgradeSteps.py"
@@ -24,6 +24,7 @@
 	OutputMode,
 	ReportCellBorders,
 	ReportLineIndentation,
+	ReportSpellingErrors,
 	ReportTableHeaders,
 	ShowMessages,
 	TetherTo,
@@ -597,3 +598,40 @@ def upgradeConfigFrom_17_to_18(profile: ConfigObj) -> None:
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
+
+
+def upgradeConfigFrom_19_to_20(profile: ConfigObj):
+	"""Move Screen Curtain settings from vision to root."""
+	try:
+		# We must copy the old settings,
+		# otherwise configobj will write the new settings as a subsection of the last root section in the config
+		profile["screenCurtain"] = profile["vision"]["screenCurtain"].copy()
+	except KeyError:
+		log.debug("No vision enhancement provider-based Screen Curtain settings exist. No action taken.")
+		return
+	del profile["vision"]["screenCurtain"]
+	log.debug("Moved Screen Curtain settings from ['vision']['screenCurtain'] to ['screenCurtain'].")

```