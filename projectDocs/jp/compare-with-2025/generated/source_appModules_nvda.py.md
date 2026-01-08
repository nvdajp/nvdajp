# Diff for: `source\appModules\nvda.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\appModules\nvda.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\appModules\nvda.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModules\\nvda.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\nvda.py"
index cb5c61e..723de9f 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModules\\nvda.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\nvda.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2008-2024 NV Access Limited, James Teh, Michael Curran, Leonard de Ruijter, Reef Turner,
+# Copyright (C) 2008-2025 NV Access Limited, James Teh, Michael Curran, Leonard de Ruijter, Reef Turner,
 # Julien Cochuyt
 # This file may be used under the terms of the GNU General Public License, version 2 or later.
 # For more details see: https://www.gnu.org/licenses/gpl-2.0.html
@@ -9,8 +9,8 @@
 
 import appModuleHandler
 import api
+import buildVersion
 import controlTypes
-import versionInfo
 from NVDAObjects.IAccessible import IAccessible
 from baseObject import ScriptableObject
 import gui
@@ -199,7 +199,7 @@ def event_NVDAObject_init(self, obj):
 		# It seems that context menus always get the name "context" and this cannot be overridden.
 		# Fudge the name of the NVDA system tray menu to make it more friendly.
 		if self.isNvdaMenu(obj):
-			obj.name = versionInfo.name
+			obj.name = buildVersion.name
 
 	def event_gainFocus(self, obj, nextHandler):
 		if obj.role == controlTypes.Role.UNKNOWN and controlTypes.State.INVISIBLE in obj.states:

```