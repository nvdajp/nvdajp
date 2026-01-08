# Diff for: `source\controlTypes\processAndLabelStates.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\controlTypes\processAndLabelStates.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\controlTypes\processAndLabelStates.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\controlTypes\\processAndLabelStates.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\controlTypes\\processAndLabelStates.py"
index 79a5b2a..8bb5b50 100644
--- "a/F:\\nvda\\gh\\beta\\source\\controlTypes\\processAndLabelStates.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\controlTypes\\processAndLabelStates.py"
@@ -5,27 +5,25 @@
 
 from typing import Dict, List, Optional, Set
 
-import config
-
-from .outputReason import OutputReason
 from .role import Role, clickableRoles
-from .state import STATES_LINK_TYPE, STATES_SORTED, State
+from .state import State, STATES_SORTED, STATES_LINK_TYPE
+from .outputReason import OutputReason
 
 
 def _processPositiveStates(
 	role: Role,
-	states: set[State],
+	states: Set[State],
 	reason: OutputReason,
-	positiveStates: set[State] | None = None,
-) -> set[State]:
+	positiveStates: Optional[Set[State]] = None,
+) -> Set[State]:
 	"""Processes the states for an object and returns the positive states to output for a specified reason.
 	For example, if C{State.CHECKED} is in the returned states, it means that the processed object is checked.
-	:param role: The role of the object to process states for (e.g. C{Role.CHECKBOX}).
-	:param states: The raw states for an object to process.
-	:param reason: The reason to process the states (e.g. C{OutputReason.FOCUS}).
-	:param positiveStates: Used for C{OutputReason.CHANGE}, specifies states changed from negative to
+	@param role: The role of the object to process states for (e.g. C{Role.CHECKBOX}).
+	@param states: The raw states for an object to process.
+	@param reason: The reason to process the states (e.g. C{OutputReason.FOCUS}).
+	@param positiveStates: Used for C{OutputReason.CHANGE}, specifies states changed from negative to
 	positive.
-	:return: The processed positive states.
+	@return: The processed positive states.
 	"""
 	positiveStates = positiveStates.copy() if positiveStates is not None else states.copy()
 	# The user never cares about certain states.
@@ -35,15 +33,6 @@ def _processPositiveStates(
 		positiveStates.discard(State.VISITED)
 		positiveStates.discard(State.INTERNAL_LINK)
 	positiveStates.discard(State.SELECTABLE)
-	if not config.conf["presentation"]["reportMultiSelect"] or role in (
-		Role.LISTITEM,
-		Role.TREEVIEWITEM,
-		Role.MENUITEM,
-		Role.TABLEROW,
-		Role.TABLECELL,
-		Role.CHECKBOX,
-	):
-		positiveStates.discard(State.MULTISELECTABLE)
 	positiveStates.discard(State.FOCUSABLE)
 	positiveStates.discard(State.CHECKABLE)
 	if State.DRAGGING in positiveStates:
@@ -52,6 +41,8 @@ def _processPositiveStates(
 	if role == Role.COMBOBOX:
 		# Combo boxes inherently have a popup, so don't report it.
 		positiveStates.discard(State.HASPOPUP)
+	import config
+
 	if not config.conf["documentFormatting"]["reportClickable"] or role in clickableRoles:
 		# This control is clearly clickable according to its role,
 		# or reporting clickable just isn't useful,
@@ -82,6 +73,9 @@ def _processPositiveStates(
 			and State.SELECTABLE in states
 		):
 			positiveStates.discard(State.SELECTED)
+			positiveStates.discard(State.MULTISELECTABLE)
+		elif not config.conf["presentation"]["reportMultiSelect"]:
+			positiveStates.discard(State.MULTISELECTABLE)
 	if role not in (Role.EDITABLETEXT, Role.CHECKBOX):
 		positiveStates.discard(State.READONLY)
 	if role == Role.CHECKBOX:

```