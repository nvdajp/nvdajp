# Diff for: `source\languageHandler.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\languageHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\languageHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\languageHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\languageHandler.py"
index 53d45ba..8e6ef0e 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\languageHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\languageHandler.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2007-2023 NV access Limited, Joseph Lee, Łukasz Golonka, Cyrille Bougot
+# Copyright (C) 2007-2025 NV access Limited, Joseph Lee, Łukasz Golonka, Cyrille Bougot
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -18,6 +18,7 @@
 import enum
 import globalVars
 from logHandler import log
+import winBindings.kernel32
 import winKernel
 from typing import (
 	FrozenSet,
@@ -114,7 +115,7 @@ def localeNameToWindowsLCID(localeName: str) -> int:
 	# Windows Vista (NT 6.0) and later is able to convert locale names to LCIDs.
 	# Because NVDA supports Windows 7 (NT 6.1) SP1 and later, just use it directly.
 	localeName = normalizeLocaleForWin32(localeName)
-	LCID = ctypes.windll.kernel32.LocaleNameToLCID(localeName, 0)
+	LCID = winBindings.kernel32.LocaleNameToLCID(localeName, 0)
 	# #6259: In Windows 10, LOCALE_CUSTOM_UNSPECIFIED is returned for any locale name unknown to Windows.
 	# This was observed for Aragonese ("an").
 	# See https://msdn.microsoft.com/en-us/library/system.globalization.cultureinfo.lcid(v=vs.110).aspx.
@@ -154,11 +155,11 @@ def getLanguageDescription(language: str) -> Optional[str]:
 		buf = ctypes.create_unicode_buffer(1024)
 		# If the original locale didn't have country info (was just language) then make sure we just get language from Windows
 		if "_" not in language:
-			res = ctypes.windll.kernel32.GetLocaleInfoW(LCID, LOCALE.SLANGDISPLAYNAME, buf, 1024)
+			res = winBindings.kernel32.GetLocaleInfo(LCID, LOCALE.SLANGDISPLAYNAME, buf, 1024)
 		else:
 			res = 0
 		if res == 0:
-			res = ctypes.windll.kernel32.GetLocaleInfoW(LCID, LOCALE.SLANGUAGE, buf, 1024)
+			res = winBindings.kernel32.GetLocaleInfo(LCID, LOCALE.SLANGUAGE, buf, 1024)
 		desc = buf.value
 	if not desc:
 		# Some hard-coded descriptions where we know the language fails on various configurations.
@@ -176,10 +177,10 @@ def englishLanguageNameFromNVDALocale(localeName: str) -> Optional[str]:
 	"""Returns either English name of the given language  using `GetLocaleInfoEx` or None
 	if the given locale is not known to Windows."""
 	localeName = normalizeLocaleForWin32(localeName)
-	buffLength = winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE.SENGLISHLANGUAGENAME, None, 0)
+	buffLength = winBindings.kernel32.GetLocaleInfoEx(localeName, LOCALE.SENGLISHLANGUAGENAME, None, 0)
 	if buffLength:
 		buf = ctypes.create_unicode_buffer(buffLength)
-		winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE.SENGLISHLANGUAGENAME, buf, buffLength)
+		winBindings.kernel32.GetLocaleInfoEx(localeName, LOCALE.SENGLISHLANGUAGENAME, buf, buffLength)
 		langName = buf.value
 		if "Unknown" in langName:
 			# Windows 10 returns 'Unknown' for locales not known to Windows
@@ -209,10 +210,10 @@ def englishCountryNameFromNVDALocale(localeName: str) -> Optional[str]:
 	"""Returns either English name of the given country using GetLocaleInfoEx or None
 	if the given locale is not known to Windows."""
 	localeName = normalizeLocaleForWin32(localeName)
-	buffLength = winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE.SENGLISHCOUNTRYNAME, None, 0)
+	buffLength = winBindings.kernel32.GetLocaleInfoEx(localeName, LOCALE.SENGLISHCOUNTRYNAME, None, 0)
 	if buffLength:
 		buf = ctypes.create_unicode_buffer(buffLength)
-		winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE.SENGLISHCOUNTRYNAME, buf, buffLength)
+		winBindings.kernel32.GetLocaleInfoEx(localeName, LOCALE.SENGLISHCOUNTRYNAME, buf, buffLength)
 		if "Unknown" in buf.value:
 			# Windows 10 returns 'Unknown region' for locales not known to Windows
 			# even though documentation states that in case of an unknown locale 0 is returned.
@@ -236,15 +237,15 @@ def ansiCodePageFromNVDALocale(localeName: str) -> Optional[str]:
 	# before attempting to retrieve code page.
 	if not englishCountryNameFromNVDALocale(localeName):
 		return None
-	buffLength = winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE.IDEFAULTANSICODEPAGE, None, 0)
+	buffLength = winBindings.kernel32.GetLocaleInfoEx(localeName, LOCALE.IDEFAULTANSICODEPAGE, None, 0)
 	if buffLength:
 		buf = ctypes.create_unicode_buffer(buffLength)
-		winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE.IDEFAULTANSICODEPAGE, buf, buffLength)
+		winBindings.kernel32.GetLocaleInfoEx(localeName, LOCALE.IDEFAULTANSICODEPAGE, buf, buffLength)
 		codePage = buf.value
 		if codePage == CP_ACP:
 			# Some locales such as Hindi are Unicode only i.e. they don't have specific ANSI code page.
 			# In such case code page should be set to the default ANSI code page of the system.
-			codePage = str(winKernel.kernel32.GetACP())
+			codePage = str(winBindings.kernel32.GetACP())
 		return codePage
 	return None
 
@@ -302,7 +303,7 @@ def getWindowsLanguage():
 	"""
 	Fetches the locale name of the user's configured language in Windows.
 	"""
-	windowsLCID = ctypes.windll.kernel32.GetUserDefaultUILanguage()
+	windowsLCID = winBindings.kernel32.GetUserDefaultUILanguage()
 	localeName = windowsLCIDToLocaleName(windowsLCID)
 	if localeName:
 		localeName = normalizeLanguage(localeName)
@@ -340,7 +341,7 @@ def setLanguage(lang: str) -> None:
 		localeName = lang
 		# Set the windows locale for this thread (NVDA core) to this locale.
 		LCID = localeNameToWindowsLCID(lang)
-		if winKernel.kernel32.SetThreadLocale(LCID) == 0:
+		if winBindings.kernel32.SetThreadLocale(LCID) == 0:
 			log.debugWarning(f"couldn't set windows thread locale to {lang}")
 
 	trans, validatedLocalName = _createGettextTranslation(localeName)
@@ -464,7 +465,7 @@ def useImperialMeasurements() -> bool:
 	"""
 	bufLength = 2
 	buf = ctypes.create_unicode_buffer(bufLength)
-	if not winKernel.kernel32.GetLocaleInfoEx(None, LOCALE.IMEASURE, buf, bufLength):
+	if not winBindings.kernel32.GetLocaleInfoEx(None, LOCALE.IMEASURE, buf, bufLength):
 		raise RuntimeError("LOCALE.IMEASURE not supported")
 	return buf.value == "1"
 

```