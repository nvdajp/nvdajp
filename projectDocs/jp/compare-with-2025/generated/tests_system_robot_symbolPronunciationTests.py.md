# Diff for: `tests\system\robot\symbolPronunciationTests.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\tests\system\robot\symbolPronunciationTests.py`  
**Current**: `F:\nvda\gh\alphajp\tests\system\robot\symbolPronunciationTests.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\system\\robot\\symbolPronunciationTests.py" "b/F:\\nvda\\gh\\alphajp\\tests\\system\\robot\\symbolPronunciationTests.py"
index eb57cf5453..960164099f 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\system\\robot\\symbolPronunciationTests.py"
+++ "b/F:\\nvda\\gh\\alphajp\\tests\\system\\robot\\symbolPronunciationTests.py"
@@ -42,7 +42,6 @@
 from AssertsLib import AssertsLib as _AssertsLib
 import NvdaLib as _NvdaLib
 from robot.libraries.BuiltIn import BuiltIn
-from jpRobotUtil import press_numpad2_4_times
 
 _builtIn: BuiltIn = BuiltIn()
 _notepad: _NotepadLib = _getLib("NotepadLib")
@@ -273,7 +272,6 @@ def test_moveByChar():
 	"""Move by character with symbol level 'none', then with symbol level 'all'."""
 	_notepad.prepareNotepad(_getMoveByCharTestSample())
 
-	press_numpad2_4_times()
 	# todo: Symbol level should not affect the output. Use same expected speech for both.
 	_doTest(
 		navKey=Move.REVIEW_CHAR,
@@ -341,7 +339,7 @@ def _testDelayedDescription(expectDescription: bool = True) -> None:
 	spoken = _NvdaLib.getSpeechAfterKey(Move.CARET_CHAR.value).split("\n")
 	if not spoken:
 		raise AssertionError("Nothing spoken after character press")
-	if expectDescription and spoken[0] not in _CHARACTER_DESCRIPTIONS:
+	if spoken[0] not in _CHARACTER_DESCRIPTIONS:
 		raise AssertionError(
 			f"First piece of speech not an expected character; got: '{spoken[0]}'",
 		)
@@ -367,7 +365,6 @@ def test_delayedDescriptions():
 	spy = _NvdaLib.getSpyLib()
 	spy.set_configValue(["speech", "delayedCharacterDescriptions"], True)
 
-	press_numpad2_4_times()
 	_testDelayedDescription()
 
 
@@ -599,24 +596,13 @@ def test_symbolInSpeechUI():
 	"""Replace a translation string to include a character that is can be substituted,
 	check if the 'speech UI' translation string the character substituted.
 	"""
-	_notepad.prepareNotepad(
-		(
-			"t"  # Character doesn't matter, we just want to invoke "Right" speech UI.
-		),
-	)
+	character = "t"  # Character doesn't matter, we just want to invoke "Right" speech UI.
+	_notepad.prepareNotepad(character)
 	_setConfig(SymLevel.ALL)
 	spy = _NvdaLib.getSpyLib()
 	expected = "shouldn't sub tick symbol"
 	spy.override_translationString(EndSpeech.RIGHT.value, expected)
 
-	# get to the end char
-	actual = _pressKeyAndCollectSpeech(Move.REVIEW_CHAR.value, numberOfTimes=1)
-	_builtIn.should_be_equal(
-		actual,
-		["blank"],
-		msg="actual vs expected. Unexpected speech when moving to final character.",
-	)
-
 	actual = _pressKeyAndCollectSpeech(Move.REVIEW_CHAR.value, numberOfTimes=1)
 	_builtIn.should_be_equal(
 		actual,
@@ -625,7 +611,7 @@ def test_symbolInSpeechUI():
 		[
 			# todo: 'tick' is a bug
 			"shouldn tick t sub tick symbol"  # intentionally concatenate strings
-			"\nblank",
+			f"\n{character}",
 		],
 		msg="actual vs expected. NVDA speech UI substitutes symbols",
 	)
@@ -635,7 +621,7 @@ def test_symbolInSpeechUI():
 	actual = _pressKeyAndCollectSpeech(Move.REVIEW_CHAR.value, numberOfTimes=1)
 	_builtIn.should_be_equal(
 		actual,
-		[f"{expected}\nblank"],
+		[f"{expected}\n{character}"],
 		msg="actual vs expected. NVDA speech UI substitutes symbols",
 	)
 

```