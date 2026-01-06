# Diff for: `source\synthDrivers\jtalk\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\synthDrivers\jtalk\__init__.py`  
**Current**: `F:\nvda\gh\alphajp\source\synthDrivers\jtalk\__init__.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\__init__.py" "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\jtalk\\__init__.py"
index 3ab3897efc..066bb1e46c 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\jtalk\\__init__.py"
@@ -2,6 +2,6 @@
 
 
 class SynthDriver(SynthDriver):  # type: ignore
-    @classmethod
-    def check(cls):
-        return False
+	@classmethod
+	def check(cls):
+		return False

```