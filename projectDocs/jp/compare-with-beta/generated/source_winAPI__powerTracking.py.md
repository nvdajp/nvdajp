# Diff for: `source\winAPI\_powerTracking.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winAPI\_powerTracking.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winAPI\_powerTracking.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winAPI\\_powerTracking.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winAPI\\_powerTracking.py"
index 26ada01..b697f01 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winAPI\\_powerTracking.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winAPI\\_powerTracking.py"
@@ -218,21 +218,6 @@ def _getBatteryInformation(systemPowerStatus: SystemPowerStatus) -> List[str]:
 	SECONDS_PER_MIN = 60
 	if systemPowerStatus.BatteryLifeTime != BATTERY_LIFE_TIME_UNKNOWN:
 		nHours = systemPowerStatus.BatteryLifeTime // SECONDS_PER_HOUR
-		nMinutes = (systemPowerStatus.BatteryLifeTime % SECONDS_PER_HOUR) // SECONDS_PER_MIN
-
-		# Skip if no time, as it likely means the status check is inaccurate
-		if systemPowerStatus.BatteryLifeTime == 0:
-			return text
-		if nHours == 0 and nMinutes == 0:
-			# Translators: Reported when battery time is less than 1 minute.
-			text.append(_("Less than 1 minute remaining"))
-			return text
-
-		hourText: str | None = None
-		minuteText: str | None = None
-
-		# Handle hours - only if greater than 0
-		if nHours > 0:
 		hourText = ngettext(
 			# Translators: This is the hour string part of the estimated remaining runtime of the laptop battery.
 			# E.g. if the full string is "1 hour and 34 minutes remaining", this string is "1 hour".
@@ -240,9 +225,7 @@ def _getBatteryInformation(systemPowerStatus: SystemPowerStatus) -> List[str]:
 			"{hours:d} hours",
 			nHours,
 		).format(hours=nHours)
-
-		# Handle minutes - only if greater than 0
-		if nMinutes > 0:
+		nMinutes = (systemPowerStatus.BatteryLifeTime % SECONDS_PER_HOUR) // SECONDS_PER_MIN
 		minuteText = ngettext(
 			# Translators: This is the minute string part of the estimated remaining runtime of the laptop battery.
 			# E.g. if the full string is "1 hour and 34 minutes remaining", this string is "34 minutes".
@@ -250,24 +233,9 @@ def _getBatteryInformation(systemPowerStatus: SystemPowerStatus) -> List[str]:
 			"{minutes:d} minutes",
 			nMinutes,
 		).format(minutes=nMinutes)
-
-		# Combine hours and minutes appropriately
-		if hourText is not None and minuteText is not None:
 		text.append(
 			# Translators: This is the main string for the estimated remaining runtime of the laptop battery.
 			# E.g. hourText is replaced by "1 hour" and minuteText by "34 minutes".
 			_("{hourText} and {minuteText} remaining").format(hourText=hourText, minuteText=minuteText),
 		)
-		elif hourText is not None:
-			text.append(
-				# Translators: Reported when only hours remaining for battery life.
-				# E.g. "2 hours remaining"
-				_("{hourText} remaining").format(hourText=hourText),
-			)
-		elif minuteText is not None:
-			text.append(
-				# Translators: Reported when only minutes remaining for battery life.
-				# E.g. "30 minutes remaining"
-				_("{minuteText} remaining").format(minuteText=minuteText),
-			)
 	return text

```