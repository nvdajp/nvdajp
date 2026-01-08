# Diff for: `source\config\profileUpgradeSteps.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\config\profileUpgradeSteps.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\config\profileUpgradeSteps.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\config\\profileUpgradeSteps.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\profileUpgradeSteps.py"
index 8c4a22e..d19a848 100644
--- "a/F:\\nvda\\gh\\beta\\source\\config\\profileUpgradeSteps.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\profileUpgradeSteps.py"
@@ -622,16 +622,3 @@ def upgradeConfigFrom_18_to_19(profile: ConfigObj):
 		f"Converted '{key}' with value {oldValue} to '{newKey}' with value {newValue}"
 		f" ({ReportSpellingErrors(newValue).name}). The old key '{key}' has been deleted.",
 	)
-
-
-def upgradeConfigFrom_19_to_20(profile: ConfigObj):
-	"""Move Screen Curtain settings from vision to root."""
-	try:
-		# We must copy the old settings,
-		# otherwise configobj will write the new settings as a subsection of the last root section in the config
-		profile["screenCurtain"] = profile["vision"]["screenCurtain"].copy()
-	except KeyError:
-		log.debug("No vision enhancement provider-based Screen Curtain settings exist. No action taken.")
-		return
-	del profile["vision"]["screenCurtain"]
-	log.debug("Moved Screen Curtain settings from ['vision']['screenCurtain'] to ['screenCurtain'].")

```