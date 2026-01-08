# Diff for: `tests\system\libraries\ChromeLib.py`

**Source**: `F:\nvda\gh\beta\tests\system\libraries\ChromeLib.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\system\libraries\ChromeLib.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\system\\libraries\\ChromeLib.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\ChromeLib.py"
index fc52c59..0c8881e 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\system\\libraries\\ChromeLib.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\ChromeLib.py"
@@ -178,19 +178,22 @@ def _waitForStartMarker(self) -> bool:
 		"""
 		spy = _NvdaLib.getSpyLib()
 		spy.wait_for_speech_to_finish()
-		expectedAddressBarSpeech = "Address and search bar"
+		# BEGIN JP PATCH (Support both English and Japanese UI language)
+		expectedAddressBarSpeechOptions = ["Address and search bar", "アドレス検索バー"]
+		# END JP PATCH
+		# Original: expectedAddressBarSpeech = "Address and search bar"
 		moveToAddressBarSpeech = _NvdaLib.getSpeechAfterKey("nvda+tab")  # report current focus.
-		if expectedAddressBarSpeech not in moveToAddressBarSpeech:
+		if not any(option in moveToAddressBarSpeech for option in expectedAddressBarSpeechOptions):
 			moveToAddressBarSpeech = _NvdaLib.getSpeechAfterKey(
 				"alt+d",
 			)  # focus the address bar, chrome shortcut
-			if expectedAddressBarSpeech not in moveToAddressBarSpeech:
+			if not any(option in moveToAddressBarSpeech for option in expectedAddressBarSpeechOptions):
 				# The "Ask Google about this page" button is sometimes spoken,
 				# which clobbers the expected output
 				moveToAddressBarSpeech = _NvdaLib.getSpeechAfterKey("nvda+tab")  # report current focus.
-				if expectedAddressBarSpeech not in moveToAddressBarSpeech:
+				if not any(option in moveToAddressBarSpeech for option in expectedAddressBarSpeechOptions):
 					builtIn.log(
-						f"Didn't read '{expectedAddressBarSpeech}' after alt+d, instead got: {moveToAddressBarSpeech}",
+						f"Didn't read any of {expectedAddressBarSpeechOptions} after alt+d, instead got: {moveToAddressBarSpeech}",
 					)
 					return False
 

```