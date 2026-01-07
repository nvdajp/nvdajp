# Diff for: `source\api.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\api.py`  
**Current**: `F:\nvda\gh\alphajp\source\api.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\api.py" "b/F:\\nvda\\gh\\alphajp\\source\\api.py"
index d29342ba2a..a11f1dc40c 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\api.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\api.py"
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

```