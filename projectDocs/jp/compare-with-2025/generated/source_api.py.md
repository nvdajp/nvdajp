# Diff for: `source\api.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\api.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\api.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\api.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\api.py"
index d29342b..22e4cf9 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\api.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\api.py"
@@ -1,6 +1,6 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2022 NV Access Limited, James Teh, Michael Curran, Peter Vagner, Derek Riemer,
-# Davy Kager, Babbage B.V., Leonard de Ruijter, Joseph Lee, Accessolutions, Julien Cochuyt
+# Copyright (C) 2006-2025 NV Access Limited, James Teh, Michael Curran, Peter Vagner, Derek Riemer,
+# Davy Kager, Babbage B.V., Leonard de Ruijter, Joseph Lee, Accessolutions, Julien Cochuyt, hwf1324
 # This file may be used under the terms of the GNU General Public License, version 2 or later.
 # For more details see: https://www.gnu.org/licenses/gpl-2.0.html
 
@@ -130,17 +130,16 @@ def setFocusObject(obj: NVDAObjects.NVDAObject) -> bool:  # noqa: C901
 				origAncestors = oldFocusLine[0 : index + 1]
 				# make sure to cache the last old ancestor as a parent on the first new ancestor so as not to leave a broken parent cache
 				if ancestors and origAncestors:
-					# ancestors[0].container=origAncestors[-1]
-					# nvdajp begin
+					# BEGIN JP PATCH
+					# nvdajp ti33778 ti35974
+					# work around ATOK and braille display
+					# reverting nvaccess ticket 3873 4145
 					if braille.handler.display.name == "noBraille":
 						# merged nvaccess master
 						ancestors[0].container = origAncestors[-1]
 					else:
-						# nvdajp ti33778 ti35974
-						# work around ATOK and braille display
-						# reverting nvaccess ticket 3873 4145
 						ancestors[0].parent = origAncestors[-1]
-					# nvdajp end
+					# END JP PATCH
 				origAncestors.extend(ancestors)
 				ancestors = origAncestors
 				focusDifferenceLevel = index + 1
@@ -151,13 +150,13 @@ def setFocusObject(obj: NVDAObjects.NVDAObject) -> bool:  # noqa: C901
 			break
 		# We're moving backwards along the ancestor chain, so add this to the start of the list.
 		ancestors.insert(0, tempObj)
-		# container=tempObj.container
-		# tempObj.container=container # Cache the parent.
-		# tempObj=container
+		# BEGIN JP PATCH
+		# nvdajp: Keep hasattr check for safety
 		if hasattr(tempObj, "container"):
 			container = tempObj.container
 			tempObj.container = container  # Cache the parent.
 		tempObj = container if hasattr(tempObj, "container") else None
+		# END JP PATCH
 	# Remove the final new ancestor as this will be the new focus object
 	del ancestors[-1]
 	# #5467: Ensure that the appModule of the real focus is included in the newAppModule list for profile switching
@@ -514,6 +513,20 @@ def isNVDAObject(obj: Any) -> bool:
 	return isinstance(obj, NVDAObjects.NVDAObject)
 
 
+fakeNVDAObjectClasses: set[type[NVDAObjects.NVDAObject]] = set()
+"""
+A collection used to register fake NVDAObject classes.
+
+These classes are treated as virtual NVDAObjects, and may not correspond to actual controls.
+For instance, content recognition results.
+"""
+
+
+def isFakeNVDAObject(obj: Any) -> bool:
+	"""Returns whether the supplied object is a fake :class:`NVDAObjects.NVDAObject`."""
+	return isinstance(obj, tuple(fakeNVDAObjectClasses))
+
+
 def isCursorManager(obj: Any) -> bool:
 	"""Returns whether the supplied object is a L{cursorManager.CursorManager}"""
 	return isinstance(obj, cursorManager.CursorManager)

```