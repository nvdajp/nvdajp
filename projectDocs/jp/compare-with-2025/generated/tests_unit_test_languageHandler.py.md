# Diff for: `tests\unit\test_languageHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\tests\unit\test_languageHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\unit\test_languageHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_languageHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_languageHandler.py"
index 20121c3..d4f0220 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_languageHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_languageHandler.py"
@@ -1,16 +1,16 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2017-2022 NV Access Limited, Łukasz Golonka
+# Copyright (C) 2017-2025 NV Access Limited, Łukasz Golonka
 
 """Unit tests for the languageHandler module."""
 
 import unittest
+import winBindings.kernel32
 import languageHandler
 from languageHandler import LCID_NONE, LCIDS_TO_TRANSLATED_LOCALES
 from localesData import LANG_NAMES_TO_LOCALIZED_DESCS
 import locale
-import ctypes
 
 
 def generateUnsupportedWindowsLocales():
@@ -77,7 +77,10 @@ def test_localeNormalizationForWin32(self):
 class Test_GetLocaleInfoEx_Wrappers(unittest.TestCase):
 	"""Set of tests for wrappers around `GetLocaleInfoEx` from `languageHandler`"""
 
-	POSSIBLE_CODE_PAGES_FOR_UNICODE_ONLY_LOCALES = {str(ctypes.windll.kernel32.GetACP()), "65001"}
+	POSSIBLE_CODE_PAGES_FOR_UNICODE_ONLY_LOCALES = {
+		str(winBindings.kernel32.GetACP()),
+		"65001",
+	}
 
 	def test_ValidEnglishLangNamesAreReturned(self):
 		"""Smoke tests `languageHandler.englishLanguageNameFromNVDALocale` with some known locale names"""
@@ -245,8 +248,8 @@ def tearDown(self):
 	def __init__(self, *args, **kwargs):
 		self._prevLang = languageHandler.getLanguage()
 
-		ctypes.windll.kernel32.SetThreadLocale(0)
-		defaultThreadLocale = ctypes.windll.kernel32.GetThreadLocale()
+		winBindings.kernel32.SetThreadLocale(0)
+		defaultThreadLocale = winBindings.kernel32.GetThreadLocale()
 		self._defaultThreadLocaleName = languageHandler.windowsLCIDToLocaleName(
 			defaultThreadLocale,
 		)
@@ -272,7 +275,7 @@ def test_NVDASupportedLanguages_LanguageIsSetCorrectly(self):
 				self.assertEqual(languageHandler.getLanguage(), localeName)
 
 				# check Windows thread is set
-				threadLocale = ctypes.windll.kernel32.GetThreadLocale()
+				threadLocale = winBindings.kernel32.GetThreadLocale()
 				threadLocaleName = languageHandler.windowsLCIDToLocaleName(threadLocale)
 				threadLocaleLang = threadLocaleName.split("_")[0]
 				if localeName in UNSUPPORTED_WIN_LANGUAGES:

```