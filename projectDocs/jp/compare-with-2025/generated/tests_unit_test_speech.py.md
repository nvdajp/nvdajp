# Diff for: `tests\unit\test_speech.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\tests\unit\test_speech.py`  
**Current**: `F:\nvda\gh\alphajp\tests\unit\test_speech.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_speech.py" "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\test_speech.py"
index a50557f1c4..1c6b55a0ca 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_speech.py"
+++ "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\test_speech.py"
@@ -527,6 +527,53 @@ def test_decomposed_normalizeOnReport(self):
 		)
 		self.assertEqual(repr(list(output)), expected)
 
+	def test_decomposedBindingToSpace(self):
+		# Note, with this test string, no normalization occurs at all.
+		# Yet we need to test this explicitly because splitAtCharacterBoundaries treats
+		# space plus acute as one character.
+		text = " ́"
+		expected = repr(
+			[
+				"space",
+				EndUtteranceCommand(),
+				"́",
+				EndUtteranceCommand(),
+			],
+		)
+		output1 = _getSpellingSpeechWithoutCharMode(
+			text=text,
+			locale=None,
+			useCharacterDescriptions=False,
+			sayCapForCapitals=False,
+			capPitchChange=0,
+			beepForCapitals=False,
+			unicodeNormalization=False,
+			reportNormalizedForCharacterNavigation=False,
+		)
+		self.assertEqual(repr(list(output1)), expected)
+		output2 = _getSpellingSpeechWithoutCharMode(
+			text=text,
+			locale=None,
+			useCharacterDescriptions=False,
+			sayCapForCapitals=False,
+			capPitchChange=0,
+			beepForCapitals=False,
+			unicodeNormalization=True,
+			reportNormalizedForCharacterNavigation=False,
+		)
+		self.assertEqual(repr(list(output2)), expected)
+		output3 = _getSpellingSpeechWithoutCharMode(
+			text=text,
+			locale=None,
+			useCharacterDescriptions=False,
+			sayCapForCapitals=False,
+			capPitchChange=0,
+			beepForCapitals=False,
+			unicodeNormalization=True,
+			reportNormalizedForCharacterNavigation=True,
+		)
+		self.assertEqual(repr(list(output3)), expected)
+
 	def test_normalizedInSymbolDict_normalizeOff(self):
 		expected = repr(
 			[

```