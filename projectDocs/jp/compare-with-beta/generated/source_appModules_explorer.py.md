# Diff for: `source\appModules\explorer.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\appModules\explorer.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\appModules\explorer.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\appModules\\explorer.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\explorer.py"
index 7f71607..4888034 100644
--- "a/F:\\nvda\\gh\\beta\\source\\appModules\\explorer.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\explorer.py"
@@ -45,6 +45,21 @@ def _get_container(self):
 			return super(MultitaskingViewFrameListItem, self).container
 
 
+# Support for Win8 start screen search suggestions.
+class SuggestionListItem(UIA):
+	def event_UIA_elementSelected(self):
+		speech.cancelSpeech()
+		if api.setNavigatorObject(self, isFocus=True):
+			self.reportFocus()
+			super().event_UIA_elementSelected()
+
+
+# Windows 8 hack: Class to disable incorrect focus on windows 8 search box
+# (containing the already correctly focused edit field)
+class SearchBoxClient(IAccessible):
+	shouldAllowIAccessibleFocusEvent = False
+
+
 # Class for menu items  for Windows Places and Frequently used Programs (in start menu)
 # Also used for desktop items
 class SysListView32EmittingDuplicateFocusEvents(IAccessible):
@@ -149,6 +164,47 @@ def event_show(self):
 			super().event_show()
 
 
+class GridTileElement(UIA):
+	role = controlTypes.Role.TABLECELL
+
+	def _get_description(self):
+		name = self.name
+		descriptionStrings = []
+		for child in self.children:
+			description = child.basicText
+			if not description or description == name:
+				continue
+			descriptionStrings.append(description)
+		return " ".join(descriptionStrings)
+		return description
+
+
+class GridListTileElement(UIA):
+	role = controlTypes.Role.TABLECELL
+	description = None
+
+
+class GridGroup(UIA):
+	"""A group in the Windows 8 Start Menu."""
+
+	presentationType = UIA.presType_content
+
+	# Normally the name is the first tile which is rather redundant
+	# However some groups have custom header text which should be read instead
+	def _get_name(self):
+		child = self.firstChild
+		if isinstance(child, UIA):
+			if child.UIAAutomationId == "GridListGroupHeader":
+				return child.name
+
+
+class ImmersiveLauncher(UIA):
+	# When the Windows 8 start screen opens, focus correctly goes to the first tile,
+	# but then incorrectly back to the root of the window.
+	# Ignore focus events on this object.
+	shouldAllowUIAFocusEvent = False
+
+
 class StartButton(IAccessible):
 	"""For Windows 8.1 and 10 Start buttons to be recognized as proper buttons
 	and to suppress selection announcement."""
@@ -213,6 +269,14 @@ def chooseNVDAObjectOverlayClasses(self, obj, clsList):  # NOQA: C901
 		windowClass = obj.windowClassName
 		role = obj.role
 
+		if (
+			windowClass in ("Search Box", "UniversalSearchBand")
+			and role == controlTypes.Role.PANE
+			and isinstance(obj, IAccessible)
+		):
+			clsList.insert(0, SearchBoxClient)
+			return  # Optimization: return early to avoid comparing class names and roles that will never match.
+
 		if windowClass == "ToolbarWindow32":
 			if role != controlTypes.Role.POPUPMENU:
 				try:
@@ -262,8 +326,18 @@ def chooseNVDAObjectOverlayClasses(self, obj, clsList):  # NOQA: C901
 
 		if isinstance(obj, UIA):
 			uiaClassName = obj.UIAElement.cachedClassName
+			if uiaClassName == "GridTileElement":
+				clsList.insert(0, GridTileElement)
+			elif uiaClassName == "GridListTileElement":
+				clsList.insert(0, GridListTileElement)
+			elif uiaClassName == "GridGroup":
+				clsList.insert(0, GridGroup)
+			elif uiaClassName == "ImmersiveLauncher" and role == controlTypes.Role.PANE:
+				clsList.insert(0, ImmersiveLauncher)
+			elif uiaClassName == "ListViewItem" and obj.UIAAutomationId.startswith("Suggestion_"):
+				clsList.insert(0, SuggestionListItem)
 			# Multitasking view frame window
-			if (
+			elif (
 				# Windows 10 and earlier
 				(uiaClassName == "MultitaskingViewFrame" and role == controlTypes.Role.WINDOW)
 				# Windows 11 where a pane window receives focus when switching tasks

```