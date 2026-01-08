# Diff for: `tests\unit\test_braille\test_brailleDisplayDrivers.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\tests\unit\test_braille\test_brailleDisplayDrivers.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\unit\test_braille\test_brailleDisplayDrivers.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_braille\\test_brailleDisplayDrivers.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_braille\\test_brailleDisplayDrivers.py"
index 2e2a9f8..eafe5b1 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_braille\\test_brailleDisplayDrivers.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_braille\\test_brailleDisplayDrivers.py"
@@ -5,6 +5,8 @@
 
 """Unit tests for braille display drivers."""
 
+import sysconfig
+import sys
 from brailleDisplayDrivers import seikantk
 import unittest
 import braille
@@ -178,6 +180,14 @@ def test_identifiers(self):
 					self.assertRegex(gesture, braille.BrailleDisplayGesture.ID_PARTS_REGEX)
 
 
+@unittest.skipUnless(
+	sysconfig.get_platform() == "win32",
+	"BRLTTY is only supported on 32-bit Windows",
+)
+@unittest.skipUnless(
+	sys.version_info.major == 3 and sys.version_info.minor == 11,
+	"Skipping brlapi tests unless Python 3.11",
+)
 class TestBRLTTY(unittest.TestCase):
 	"""Tests the integrity of the bundled brlapi module."""
 

```