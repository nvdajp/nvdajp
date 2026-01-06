# Diff for: `tests\unit\test_baseObject.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\tests\unit\test_baseObject.py`  
**Current**: `F:\nvda\gh\alphajp\tests\unit\test_baseObject.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_baseObject.py" "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\test_baseObject.py"
index 764a2302d0..2af2892ea2 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_baseObject.py"
+++ "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\test_baseObject.py"
@@ -5,7 +5,6 @@
 
 """Unit tests for the baseObject module, its classes and their derivatives."""
 
-import sys
 import unittest
 from baseObject import AutoPropertyObject
 from .objectProvider import PlaceholderNVDAObject
@@ -149,14 +148,7 @@ class TestAbstractAutoPropertyObjects(unittest.TestCase):
 
 	@staticmethod
 	def _get_regex(className: str) -> str:
-		if sys.version_info.major == 3 and sys.version_info.minor == 13:
 		return rf"^Can't instantiate abstract class {className} without an implementation for abstract method 'x'"
-		elif sys.version_info.major == 3 and sys.version_info.minor == 11:
-			return rf"^Can't instantiate abstract class {className} with abstract method x"
-		else:
-			raise RuntimeError(
-				f"Unsupported Python version for abstract property tests: {sys.version_info.major}.{sys.version_info.minor}",
-			)
 
 	def test_abstractProperty(self):
 		self.assertRaisesRegex(

```