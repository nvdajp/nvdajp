# Diff for: `source\controlTypes\processAndLabelStates.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\controlTypes\processAndLabelStates.py`  
**Current**: `F:\nvda\gh\alphajp\source\controlTypes\processAndLabelStates.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\controlTypes\\processAndLabelStates.py" "b/F:\\nvda\\gh\\alphajp\\source\\controlTypes\\processAndLabelStates.py"
index 45755c5320..8bb5b50870 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\controlTypes\\processAndLabelStates.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\controlTypes\\processAndLabelStates.py"
@@ -73,6 +73,9 @@ def _processPositiveStates(
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