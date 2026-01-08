# Diff for: `source\winAPI\_powerTracking.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\winAPI\_powerTracking.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winAPI\_powerTracking.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winAPI\\_powerTracking.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winAPI\\_powerTracking.py"
index 8fa7ea0..26ada01 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winAPI\\_powerTracking.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winAPI\\_powerTracking.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2022 NV Access Limited, Rui Batista, Cyrille Bougot
+# Copyright (C) 2022-2025 NV Access Limited, Rui Batista, Cyrille Bougot
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -11,6 +11,7 @@
 The power status can also be reported using script_say_battery_status.
 """
 
+from __future__ import annotations
 import ctypes
 from enum import (
 	Enum,
@@ -26,6 +27,8 @@
 
 from logHandler import log
 import ui
+import winBindings.kernel32
+from winBindings.kernel32 import SYSTEM_POWER_STATUS as SystemPowerStatus
 import winKernel
 
 
@@ -83,18 +86,6 @@ class PowerState(IntFlag):
 	AC_ONLINE = 0x1
 	UNKNOWN = 0xFF
 
-
-class SystemPowerStatus(ctypes.Structure):
-	# https://docs.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-system_power_status
-	_fields_ = [
-		("ACLineStatus", ctypes.c_byte),
-		("BatteryFlag", ctypes.c_byte),
-		("BatteryLifePercent", ctypes.c_byte),
-		("Reserved1", ctypes.c_byte),
-		("BatteryLifeTime", ctypes.wintypes.DWORD),
-		("BatteryFullLiveTime", ctypes.wintypes.DWORD),
-	]
-
 	BatteryFlag: BatteryFlag
 	ACLineStatus: PowerState
 	BatteryLifePercent: int
@@ -112,7 +103,7 @@ def initialize():
 	we fetch the initial power state manually.
 	"""
 	global _powerState
-	systemPowerStatus = SystemPowerStatus()
+	systemPowerStatus = winBindings.kernel32.SYSTEM_POWER_STATUS()
 	if (
 		not winKernel.GetSystemPowerStatus(systemPowerStatus)
 		or systemPowerStatus.BatteryFlag == BatteryFlag.UNKNOWN
@@ -227,6 +218,21 @@ def _getBatteryInformation(systemPowerStatus: SystemPowerStatus) -> List[str]:
 	SECONDS_PER_MIN = 60
 	if systemPowerStatus.BatteryLifeTime != BATTERY_LIFE_TIME_UNKNOWN:
 		nHours = systemPowerStatus.BatteryLifeTime // SECONDS_PER_HOUR
+		nMinutes = (systemPowerStatus.BatteryLifeTime % SECONDS_PER_HOUR) // SECONDS_PER_MIN
+
+		# Skip if no time, as it likely means the status check is inaccurate
+		if systemPowerStatus.BatteryLifeTime == 0:
+			return text
+		if nHours == 0 and nMinutes == 0:
+			# Translators: Reported when battery time is less than 1 minute.
+			text.append(_("Less than 1 minute remaining"))
+			return text
+
+		hourText: str | None = None
+		minuteText: str | None = None
+
+		# Handle hours - only if greater than 0
+		if nHours > 0:
 			hourText = ngettext(
 				# Translators: This is the hour string part of the estimated remaining runtime of the laptop battery.
 				# E.g. if the full string is "1 hour and 34 minutes remaining", this string is "1 hour".
@@ -234,7 +240,9 @@ def _getBatteryInformation(systemPowerStatus: SystemPowerStatus) -> List[str]:
 				"{hours:d} hours",
 				nHours,
 			).format(hours=nHours)
-		nMinutes = (systemPowerStatus.BatteryLifeTime % SECONDS_PER_HOUR) // SECONDS_PER_MIN
+
+		# Handle minutes - only if greater than 0
+		if nMinutes > 0:
 			minuteText = ngettext(
 				# Translators: This is the minute string part of the estimated remaining runtime of the laptop battery.
 				# E.g. if the full string is "1 hour and 34 minutes remaining", this string is "34 minutes".
@@ -242,9 +250,24 @@ def _getBatteryInformation(systemPowerStatus: SystemPowerStatus) -> List[str]:
 				"{minutes:d} minutes",
 				nMinutes,
 			).format(minutes=nMinutes)
+
+		# Combine hours and minutes appropriately
+		if hourText is not None and minuteText is not None:
 			text.append(
 				# Translators: This is the main string for the estimated remaining runtime of the laptop battery.
 				# E.g. hourText is replaced by "1 hour" and minuteText by "34 minutes".
 				_("{hourText} and {minuteText} remaining").format(hourText=hourText, minuteText=minuteText),
 			)
+		elif hourText is not None:
+			text.append(
+				# Translators: Reported when only hours remaining for battery life.
+				# E.g. "2 hours remaining"
+				_("{hourText} remaining").format(hourText=hourText),
+			)
+		elif minuteText is not None:
+			text.append(
+				# Translators: Reported when only minutes remaining for battery life.
+				# E.g. "30 minutes remaining"
+				_("{minuteText} remaining").format(minuteText=minuteText),
+			)
 	return text

```