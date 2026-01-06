# Diff for: `tests\unit\objectProvider.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\tests\unit\objectProvider.py`  
**Current**: `F:\nvda\gh\alphajp\tests\unit\objectProvider.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\objectProvider.py" "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\objectProvider.py"
index c7a0101a9d..9f2fa13f6d 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\objectProvider.py"
+++ "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\objectProvider.py"
@@ -12,7 +12,7 @@
 
 class PlaceholderNVDAObject(NVDAObject):
 	processID = None  # Must be implemented to instantiate.
-	windowThreadID = None  # Must be implemented for inputCore tests
+	windowThreadID = 0  # Must be implemented for inputCore tests
 
 
 class NVDAObjectWithRole(PlaceholderNVDAObject):

```