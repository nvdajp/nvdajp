# Diff for: `tests\unit\objectProvider.py`

**Source**: `F:\nvda\gh\alphajp-251219\tests\unit\objectProvider.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\unit\objectProvider.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\objectProvider.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\objectProvider.py"
index c7a0101..9f2fa13 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\objectProvider.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\objectProvider.py"
@@ -12,7 +12,7 @@
 
 class PlaceholderNVDAObject(NVDAObject):
 	processID = None  # Must be implemented to instantiate.
-	windowThreadID = None  # Must be implemented for inputCore tests
+	windowThreadID = 0  # Must be implemented for inputCore tests
 
 
 class NVDAObjectWithRole(PlaceholderNVDAObject):

```