# Diff for: `source\controlTypes\processAndLabelStates.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\controlTypes\processAndLabelStates.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\controlTypes\processAndLabelStates.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\controlTypes\\processAndLabelStates.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\controlTypes\\processAndLabelStates.py"
index 45755c5..79a5b2a 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\controlTypes\\processAndLabelStates.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\controlTypes\\processAndLabelStates.py"
@@ -5,25 +5,27 @@
 
 from typing import Dict, List, Optional, Set
 
-from .role import Role, clickableRoles
-from .state import State, STATES_SORTED, STATES_LINK_TYPE
+import config
+
 from .outputReason import OutputReason
+from .role import Role, clickableRoles
+from .state import STATES_LINK_TYPE, STATES_SORTED, State
 
 
 def _processPositiveStates(
 	role: Role,
-	states: Set[State],
+	states: set[State],
 	reason: OutputReason,
-	positiveStates: Optional[Set[State]] = None,
-) -> Set[State]:
+	positiveStates: set[State] | None = None,
+) -> set[State]:
 	"""Processes the states for an object and returns the positive states to output for a specified reason.
 	For example, if C{State.CHECKED} is in the returned states, it means that the processed object is checked.
-	@param role: The role of the object to process states for (e.g. C{Role.CHECKBOX}).
-	@param states: The raw states for an object to process.
-	@param reason: The reason to process the states (e.g. C{OutputReason.FOCUS}).
-	@param positiveStates: Used for C{OutputReason.CHANGE}, specifies states changed from negative to
+	:param role: The role of the object to process states for (e.g. C{Role.CHECKBOX}).
+	:param states: The raw states for an object to process.
+	:param reason: The reason to process the states (e.g. C{OutputReason.FOCUS}).
+	:param positiveStates: Used for C{OutputReason.CHANGE}, specifies states changed from negative to
 	positive.
-	@return: The processed positive states.
+	:return: The processed positive states.
 	"""
 	positiveStates = positiveStates.copy() if positiveStates is not None else states.copy()
 	# The user never cares about certain states.
@@ -33,6 +35,15 @@ def _processPositiveStates(
 		positiveStates.discard(State.VISITED)
 		positiveStates.discard(State.INTERNAL_LINK)
 	positiveStates.discard(State.SELECTABLE)
+	if not config.conf["presentation"]["reportMultiSelect"] or role in (
+		Role.LISTITEM,
+		Role.TREEVIEWITEM,
+		Role.MENUITEM,
+		Role.TABLEROW,
+		Role.TABLECELL,
+		Role.CHECKBOX,
+	):
+		positiveStates.discard(State.MULTISELECTABLE)
 	positiveStates.discard(State.FOCUSABLE)
 	positiveStates.discard(State.CHECKABLE)
 	if State.DRAGGING in positiveStates:
@@ -41,8 +52,6 @@ def _processPositiveStates(
 	if role == Role.COMBOBOX:
 		# Combo boxes inherently have a popup, so don't report it.
 		positiveStates.discard(State.HASPOPUP)
-	import config
-
 	if not config.conf["documentFormatting"]["reportClickable"] or role in clickableRoles:
 		# This control is clearly clickable according to its role,
 		# or reporting clickable just isn't useful,

```