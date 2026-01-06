# Diff for: `source\synthDriverHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\synthDriverHandler.py`  
**Current**: `F:\nvda\gh\alphajp\source\synthDriverHandler.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDriverHandler.py" "b/F:\\nvda\\gh\\alphajp\\source\\synthDriverHandler.py"
index 351086fc4d..5f38b3ccfb 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDriverHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\synthDriverHandler.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2006-2024 NV Access Limited, Peter Vágner, Aleksey Sadovoy,
+# Copyright (C) 2006-2025 NV Access Limited, Peter Vágner, Aleksey Sadovoy,
 # Joseph Lee, Arnold Loubriat, Leonard de Ruijter
 
 import pkgutil
@@ -18,7 +18,6 @@
 from locale import strxfrm
 
 import config
-import winVersion
 import globalVars
 from logHandler import log
 from synthSettingsRing import SynthSettingsRing
@@ -484,10 +483,7 @@ def getSynthInstance(name, asDefault=False):
 
 # The synthDrivers that should be used by default.
 # The first that successfully initializes will be used when config is set to auto (I.e. new installs of NVDA).
-defaultSynthPriorityList = ["nvdajp_jtalk", "espeak", "silence"]
-if winVersion.getWinVer() >= winVersion.WIN10:
-	# Default to OneCore on Windows 10 and above
-	defaultSynthPriorityList.insert(0, "oneCore")
+defaultSynthPriorityList = ["oneCore", "espeak", "silence"]
 
 
 def setSynth(name: Optional[str], isFallback: bool = False):

```