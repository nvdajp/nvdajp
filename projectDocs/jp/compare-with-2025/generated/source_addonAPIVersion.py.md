# Diff for: `source\addonAPIVersion.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\addonAPIVersion.py`  
**Current**: `F:\nvda\gh\alphajp\source\addonAPIVersion.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\addonAPIVersion.py" "b/F:\\nvda\\gh\\alphajp\\source\\addonAPIVersion.py"
index 678e70861f..805644bbdb 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\addonAPIVersion.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\addonAPIVersion.py"
@@ -1,14 +1,11 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2018-2023 NV Access Limited
+# Copyright (C) 2018-2025 NV Access Limited
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
 
 import buildVersion
 import re
-from typing import (
-	Tuple,
-)
 from logHandler import log
 
 """
@@ -16,7 +13,7 @@
 how the API has changed as well as the range of API versions supported by this build of NVDA
 """
 
-AddonApiVersionT = Tuple[int, int, int]
+AddonApiVersionT = tuple[int, int, int]
 
 CURRENT: AddonApiVersionT = (
 	buildVersion.version_year,
@@ -24,12 +21,13 @@
 	buildVersion.version_minor,
 )
 
-BACK_COMPAT_TO: AddonApiVersionT = (2025, 1, 0)
+BACK_COMPAT_TO: AddonApiVersionT = (2026, 1, 0)
 """
 As BACK_COMPAT_TO is incremented, the changed / removed parts / or reasoning should be added below.
 These only serve to act as a reminder, the changelog should be consulted for a comprehensive listing.
 EG: (x, y, z): Large changes to speech.py
 ---
+(2026, 1, 0): Upgrade to python 3.13 and migration to 64bit from 32bit
 (2025, 1, 0): HTML passed to browsableMessage is now sanitised, and various changes to the settings schema
 (2024, 1, 0): upgrade to python 3.11
 (2023, 1, 0): speech as str was dropped in favor of only SpeechCommand, and security changes.

```