# Diff for: `source\IAccessibleHandler\orderedWinEventLimiter.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\IAccessibleHandler\orderedWinEventLimiter.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\IAccessibleHandler\orderedWinEventLimiter.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\IAccessibleHandler\\orderedWinEventLimiter.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\IAccessibleHandler\\orderedWinEventLimiter.py"
index d58fb5a..2e6575d 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\IAccessibleHandler\\orderedWinEventLimiter.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\IAccessibleHandler\\orderedWinEventLimiter.py"
@@ -50,12 +50,12 @@ def addEvent(
 		threadID: int,
 	) -> bool:
 		"""Adds a winEvent to the limiter.
-		@param eventID: the winEvent type
-		@param window: the window handle of the winEvent
-		@param objectID: the objectID of the winEvent
-		@param childID: the childID of the winEvent
-		@param threadID: the threadID of the winEvent
-		@return: C{True} if the event was added, C{False} if it was discarded.
+		:param eventID: the winEvent type
+		:param window: the window handle of the winEvent
+		:param objectID: the objectID of the winEvent
+		:param childID: the childID of the winEvent
+		:param threadID: the threadID of the winEvent
+		:return: C{True} if the event was added, C{False} if it was discarded.
 		"""
 		if eventID == winUser.EVENT_OBJECT_FOCUS:
 			if objectID in (winUser.OBJID_SYSMENU, winUser.OBJID_MENU) and childID == 0:
@@ -83,13 +83,13 @@ def addEvent(
 	def flushEvents(
 		self,
 		alwaysAllowedObjects: Optional[List[IAccessibleObjectIdentifierType]] = None,
-	) -> List:
+	) -> list[tuple[int, int, int, int]]:
 		"""Returns a list of winEvents that have been added.
 		Due to limiting, it will not necessarily be all the winEvents that were originally added.
 		They are definitely guaranteed to be in the correct order though.
 		winEvents for objects listed in alwaysAllowedObjects will always be emitted,
 		Even if the winEvent limit for that thread has been exceeded.
-		@return Tuple[eventID,window,objectID,childID]
+		:return: a list of tuples with eventID,window,objectID,childID
 		"""
 		if self._lastMenuEvent is not None:
 			heapq.heappush(self._eventHeap, self._lastMenuEvent)

```