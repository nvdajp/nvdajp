# Diff for: `tests\unit\test_braille\test_brailleDisplayDrivers.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\tests\unit\test_braille\test_brailleDisplayDrivers.py`  
**Current**: `F:\nvda\gh\alphajp\tests\unit\test_braille\test_brailleDisplayDrivers.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_braille\\test_brailleDisplayDrivers.py" "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\test_braille\\test_brailleDisplayDrivers.py"
index ed21b25a37..eafe5b11a7 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_braille\\test_brailleDisplayDrivers.py"
+++ "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\test_braille\\test_brailleDisplayDrivers.py"
@@ -5,6 +5,7 @@
 
 """Unit tests for braille display drivers."""
 
+import sysconfig
 import sys
 from brailleDisplayDrivers import seikantk
 import unittest
@@ -179,13 +180,17 @@ def test_identifiers(self):
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
 
-	@unittest.skipUnless(
-		sys.version_info.major == 3 and sys.version_info.minor == 11,
-		"Skipping brlapi tests unless Python 3.11",
-	)
 	def test_brlapi(self):
 		try:
 			# SUpress Flake8 F401 imported but unused, as we're testing the import

```