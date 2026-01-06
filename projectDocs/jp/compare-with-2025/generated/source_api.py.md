# Diff for: `source\api.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\api.py`  
**Current**: `F:\nvda\gh\alphajp\source\api.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\api.py" "b/F:\\nvda\\gh\\alphajp\\source\\api.py"
index d29342ba2a..939aac949c 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\api.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\api.py"
@@ -98,7 +98,7 @@ def setFocusObject(obj: NVDAObjects.NVDAObject) -> bool:  # noqa: C901
 	# add the old focus to the old focus ancestors, but only if its not None (is none at NVDA initialization)
 	if globalVars.focusObject:
 		oldFocusLine.append(globalVars.focusObject)
-	oldAppModules = [o.appModule for o in oldFocusLine if o and getattr(o, "appModule", None)]
+	oldAppModules = [o.appModule for o in oldFocusLine if o and o.appModule]
 	appModuleHandler.cleanup()
 	ancestors = []
 	tempObj = obj
@@ -130,17 +130,7 @@ def setFocusObject(obj: NVDAObjects.NVDAObject) -> bool:  # noqa: C901
 				origAncestors = oldFocusLine[0 : index + 1]
 				# make sure to cache the last old ancestor as a parent on the first new ancestor so as not to leave a broken parent cache
 				if ancestors and origAncestors:
-					# ancestors[0].container=origAncestors[-1]
-					# nvdajp begin
-					if braille.handler.display.name == "noBraille":
-						# merged nvaccess master
-						ancestors[0].container = origAncestors[-1]
-					else:
-						# nvdajp ti33778 ti35974
-						# work around ATOK and braille display
-						# reverting nvaccess ticket 3873 4145
-						ancestors[0].parent = origAncestors[-1]
-					# nvdajp end
+					ancestors[0].container = origAncestors[-1]
 				origAncestors.extend(ancestors)
 				ancestors = origAncestors
 				focusDifferenceLevel = index + 1
@@ -151,18 +141,14 @@ def setFocusObject(obj: NVDAObjects.NVDAObject) -> bool:  # noqa: C901
 			break
 		# We're moving backwards along the ancestor chain, so add this to the start of the list.
 		ancestors.insert(0, tempObj)
-		# container=tempObj.container
-		# tempObj.container=container # Cache the parent.
-		# tempObj=container
-		if hasattr(tempObj, "container"):
-			container = tempObj.container
-			tempObj.container = container  # Cache the parent.
-		tempObj = container if hasattr(tempObj, "container") else None
+		container = tempObj.container
+		tempObj.container = container  # Cache the parent.
+		tempObj = container
 	# Remove the final new ancestor as this will be the new focus object
 	del ancestors[-1]
 	# #5467: Ensure that the appModule of the real focus is included in the newAppModule list for profile switching
 	# Rather than an original focus ancestor which happened to match the new focus.
-	newAppModules = [o.appModule for o in ancestors if o and getattr(o, "appModule", None)]
+	newAppModules = [o.appModule for o in ancestors if o and o.appModule]
 	if obj.appModule:
 		newAppModules.append(obj.appModule)
 	try:

```