# Diff for: `source\controlTypes\state.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\controlTypes\state.py`  
**Current**: `F:\nvda\gh\alphajp\source\controlTypes\state.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\controlTypes\\state.py" "b/F:\\nvda\\gh\\alphajp\\source\\controlTypes\\state.py"
index 9a2a02ddce..337675621d 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\controlTypes\\state.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\controlTypes\\state.py"
@@ -103,6 +103,7 @@ def negativeDisplayString(self) -> str:
 	HASPOPUP_LIST = setBit(49)
 	HASPOPUP_TREE = setBit(50)
 	INTERNAL_LINK = setBit(51)
+	MULTISELECTABLE = setBit(52)
 
 
 STATES_SORTED = frozenset([State.SORTED, State.SORTED_ASCENDING, State.SORTED_DESCENDING])
@@ -210,6 +211,9 @@ def negativeDisplayString(self) -> str:
 	# Translators: Presented when a link destination points to the page containing the link.
 	# For example, links of a table of contents of a document with different sections.
 	State.INTERNAL_LINK: _("same page"),
+	# Translators: Presented when the control allows multiple selected objects.
+	# For example, a list box that allows selecting multiple items.
+	State.MULTISELECTABLE: _("multi-select"),
 }
 
 

```