# Diff for: `tests\unit\test_visionEnhancementProviders\test_magnificationAPI.py`

**Source**: `F:\nvda\gh\beta\tests\unit\test_visionEnhancementProviders\test_magnificationAPI.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\unit\test_visionEnhancementProviders\test_magnificationAPI.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_visionEnhancementProviders\\test_magnificationAPI.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_visionEnhancementProviders\\test_magnificationAPI.py"
index ec86c75..fe46b23 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_visionEnhancementProviders\\test_magnificationAPI.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_visionEnhancementProviders\\test_magnificationAPI.py"
@@ -7,17 +7,15 @@
 
 import unittest
 
-from screenCurtain._screenCurtain import TRANSFORM_BLACK
-from winBindings import magnification
-from winBindings.magnification import MAGCOLOREFFECT
+from visionEnhancementProviders.screenCurtain import Magnification, TRANSFORM_BLACK, MAGCOLOREFFECT
 
 
 class _Test_MagnificationAPI(unittest.TestCase):
 	def setUp(self):
-		self.assertTrue(magnification.MagInitialize())
+		self.assertTrue(Magnification.MagInitialize())
 
 	def tearDown(self):
-		self.assertTrue(magnification.MagUninitialize())
+		self.assertTrue(Magnification.MagUninitialize())
 
 
 class Test_ScreenCurtain(_Test_MagnificationAPI):
@@ -34,7 +32,7 @@ def _isIdentityMatrix(self, magTransformMatrix: MAGCOLOREFFECT) -> bool:
 
 	def setUp(self):
 		super().setUp()
-		resultEffect = magnification.MagGetFullscreenColorEffect()
+		resultEffect = Magnification.MagGetFullscreenColorEffect()
 		if not self._isIdentityMatrix(resultEffect):
 			# If the resultEffect is not the identity matrix, skip the test.
 			# This is because a full screen colour effect is already set external to testing.
@@ -45,9 +43,9 @@ def setUp(self):
 		return
 
 	def test_setAndConfirmBlackFullscreenColorEffect(self):
-		result = magnification.MagSetFullscreenColorEffect(TRANSFORM_BLACK)
+		result = Magnification.MagSetFullscreenColorEffect(TRANSFORM_BLACK)
 		self.assertTrue(result)
-		resultEffect = magnification.MagGetFullscreenColorEffect()
+		resultEffect = Magnification.MagGetFullscreenColorEffect()
 		for i in range(5):
 			for j in range(5):
 				with self.subTest(i=i, j=j):
@@ -60,9 +58,9 @@ def test_setAndConfirmBlackFullscreenColorEffect(self):
 
 class Test_Mouse(_Test_MagnificationAPI):
 	def test_MagShowSystemCursor(self):
-		result = magnification.MagShowSystemCursor(True)
+		result = Magnification.MagShowSystemCursor(True)
 		self.assertTrue(result)
 
 	def test_MagHideSystemCursor(self):
-		result = magnification.MagShowSystemCursor(False)
+		result = Magnification.MagShowSystemCursor(False)
 		self.assertTrue(result)

```