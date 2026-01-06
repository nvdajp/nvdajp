# Diff for: `source\gui\nvdaControls.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\gui\nvdaControls.py`  
**Current**: `F:\nvda\gh\alphajp\source\gui\nvdaControls.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\nvdaControls.py" "b/F:\\nvda\\gh\\alphajp\\source\\gui\\nvdaControls.py"
index 4adf94df0d..bd3524ee98 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\nvdaControls.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\gui\\nvdaControls.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2016-2024 NV Access Limited, Derek Riemer, Cyrille Bougot, Luke Davis, Leonard de Ruijter
+# Copyright (C) 2016-2025 NV Access Limited, Derek Riemer, Cyrille Bougot, Luke Davis, Leonard de Ruijter
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -23,6 +23,7 @@
 	FlagValueEnum as FeatureFlagEnumT,
 )
 import gui.message
+from winBindings import user32
 from .dpiScalingHelper import DpiScalingHelperMixin
 from . import (
 	guiHelper,
@@ -406,7 +407,7 @@ def SetValue(self, i):
 		# HACK: Win events don't seem to be sent for certain explicitly set values,
 		# so send our own win event.
 		# This will cause duplicates in some cases, but NVDA will filter them out.
-		winUser.user32.NotifyWinEvent(
+		user32.NotifyWinEvent(
 			winUser.EVENT_OBJECT_VALUECHANGE,
 			self.Handle,
 			winUser.OBJID_CLIENT,

```