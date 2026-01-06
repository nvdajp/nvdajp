# Diff for: `tests\system\libraries\ChromeLib.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\tests\system\libraries\ChromeLib.py`  
**Current**: `F:\nvda\gh\alphajp\tests\system\libraries\ChromeLib.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\system\\libraries\\ChromeLib.py" "b/F:\\nvda\\gh\\alphajp\\tests\\system\\libraries\\ChromeLib.py"
index 336e938a46..9320761e0c 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\system\\libraries\\ChromeLib.py"
+++ "b/F:\\nvda\\gh\\alphajp\\tests\\system\\libraries\\ChromeLib.py"
@@ -178,21 +178,20 @@ def _waitForStartMarker(self) -> bool:
 		"""
 		spy = _NvdaLib.getSpyLib()
 		spy.wait_for_speech_to_finish()
+		# BEGIN JP PATCH (Japanese UI language)
 		expectedAddressBarSpeech = "アドレス検索バー"
+		# END JP PATCH
+		# Original: expectedAddressBarSpeech = "Address and search bar"
 		moveToAddressBarSpeech = _NvdaLib.getSpeechAfterKey("nvda+tab")  # report current focus.
 		if expectedAddressBarSpeech not in moveToAddressBarSpeech:
 			moveToAddressBarSpeech = _NvdaLib.getSpeechAfterKey(
 				"alt+d",
 			)  # focus the address bar, chrome shortcut
 			if expectedAddressBarSpeech not in moveToAddressBarSpeech:
-				# The "Ask Google about this page" button is sometimes spoken,
-				# which clobbers the expected output
-				moveToAddressBarSpeech = _NvdaLib.getSpeechAfterKey("nvda+tab")  # report current focus.
-				if expectedAddressBarSpeech not in moveToAddressBarSpeech:
-					builtIn.log(
-						f"Didn't read '{expectedAddressBarSpeech}' after alt+d, instead got: {moveToAddressBarSpeech}",
-					)
-					return False
+				builtIn.log(
+					f"Didn't read '{expectedAddressBarSpeech}' after alt+d, instead got: {moveToAddressBarSpeech}",
+				)
+				return False
 
 		afterControlF6Speech = _NvdaLib.getSpeechAfterKey("control+F6")  # focus web content, chrome shortcut.
 		if ChromeLib._testCaseTitle not in afterControlF6Speech:
@@ -254,8 +253,6 @@ def prepareChrome(self, testCase: str, _alwaysDoToggleFocus: bool = False) -> No
 		patternSafeTitleString = applicationTitle.replace("(", ".").replace(")", ".")
 		chromeTitleSpeechPattern = re.compile(patternSafeTitleString)
 
-		spy.emulateKeyPress("alt+f")
-		spy.emulateKeyPress("escape")
 		if (
 			_alwaysDoToggleFocus  # may work around focus/foreground event missed issues for tests.
 			or not _chromeLib.canChromeTitleBeReported(chromeTitleSpeechPattern)

```