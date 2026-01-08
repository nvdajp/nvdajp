# Diff for: `source\IAccessibleHandler\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\IAccessibleHandler\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\IAccessibleHandler\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\IAccessibleHandler\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\IAccessibleHandler\\__init__.py"
index 8e7e93b..44405be 100644
--- "a/F:\\nvda\\gh\\beta\\source\\IAccessibleHandler\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\IAccessibleHandler\\__init__.py"
@@ -369,11 +369,10 @@ def accessibleObjectFromPoint(x, y):
 	return normalizeIAccessible(pacc, child), child
 
 
-def windowFromAccessibleObject(ia) -> int:
+def windowFromAccessibleObject(ia):
 	try:
 		return oleacc.WindowFromAccessibleObject(ia)
-	except WindowsError:
-		log.debugWarning("windowFromAccessibleObject failed", exc_info=True)
+	except:  # noqa: E722 Bare except
 		return 0
 
 
@@ -602,15 +601,20 @@ def winEventToNVDAEvent(  # noqa: C901
 	return (NVDAEventName, obj)
 
 
-def processGenericWinEvent(eventID: int, window: int, objectID: int, childID: int) -> bool:
+def processGenericWinEvent(eventID, window, objectID, childID):
 	"""Converts the win event to an NVDA event,
 	Checks to see if this NVDAObject  equals the current focus.
 	If all goes well, then the event is queued and we return True
-	:param eventID: a win event ID (type)
-	:param window: a win event's window handle
-	:param objectID: a win event's object ID
-	:param childID: a win event's child ID
-	:return: True if the event was processed, False otherwise.
+	@param eventID: a win event ID (type)
+	@type eventID: integer
+	@param window: a win event's window handle
+	@type window: integer
+	@param objectID: a win event's object ID
+	@type objectID: integer
+	@param childID: a win event's child ID
+	@type childID: integer
+	@returns: True if the event was processed, False otherwise.
+	@rtype: boolean
 	"""
 	if isMSAADebugLoggingEnabled():
 		log.debug(
@@ -676,15 +680,19 @@ def processGenericWinEvent(eventID: int, window: int, objectID: int, childID: in
 	return True
 
 
-def processFocusWinEvent(window: int, objectID: int, childID: int, force: bool = False) -> bool:
+def processFocusWinEvent(window, objectID, childID, force=False):
 	"""checks to see if the focus win event is not the same as the existing focus,
 	then converts the win event to an NVDA event (instantiating an NVDA Object) then calls
 	processFocusNVDAEvent. If all is ok it returns True.
-	:param window: a win event's window handle
-	:param objectID: a win event's object ID
-	:param childID: a win event's child ID
-	:param force: If True, the shouldAllowIAccessibleFocusEvent property of the object is ignored.
-	:return: True if the focus is valid and was handled, False otherwise.
+	@type window: integer
+	@param objectID: a win event's object ID
+	@type objectID: integer
+	@param childID: a win event's child ID
+	@type childID: integer
+	@param force: If True, the shouldAllowIAccessibleFocusEvent property of the object is ignored.
+	@type force: boolean
+	@returns: True if the focus is valid and was handled, False otherwise.
+	@rtype: boolean
 	"""
 	if isMSAADebugLoggingEnabled():
 		log.debug(
@@ -770,7 +778,7 @@ def processFocusNVDAEvent(obj, force=False):
 	return True
 
 
-def processDesktopSwitchWinEvent(window: int, objectID: int, childID: int) -> None:
+def processDesktopSwitchWinEvent(window, objectID, childID):
 	from winAPI.secureDesktop import _handleSecureDesktopChange
 
 	if isMSAADebugLoggingEnabled():
@@ -778,12 +786,12 @@ def processDesktopSwitchWinEvent(window: int, objectID: int, childID: int) -> No
 			f"Processing desktopSwitch winEvent: {getWinEventLogInfo(window, objectID, childID)}",
 		)
 	hDesk = user32.OpenInputDesktop(0, False, 0)
-	if hDesk is not None:
+	if hDesk != 0:
 		user32.CloseDesktop(hDesk)
 		core.callLater(200, _handleUserDesktop)
 	else:
-		# When hDesk == None, the active desktop has changed.
-		# This usually means the secure desktop has been launched,
+		# When hDesk == 0, the active desktop has changed.
+		# This is usually means the secure desktop has been launched,
 		# but the new desktop can also be a secondary desktop created through the Windows API.
 		# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createdesktopa
 		# This secondary desktop has some bugs, and as such is not properly supported (#14395).
@@ -1018,9 +1026,7 @@ def pumpAll():  # noqa: C901
 		alwaysAllowedObjects.append((focus.event_windowHandle, focus.event_objectID, focus.event_childID))
 
 	# Receive all the winEvents from the limiter for this cycle
-	winEvents: list[tuple[int, int, int, int]] = internalWinEventHandler.winEventLimiter.flushEvents(
-		alwaysAllowedObjects,
-	)
+	winEvents = internalWinEventHandler.winEventLimiter.flushEvents(alwaysAllowedObjects)
 
 	for winEvent in winEvents:
 		isEventOnCaret = winEvent[2] == winUser.OBJID_CARET

```