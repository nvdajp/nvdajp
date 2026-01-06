# Diff for: `tests\unit\test_textUtils.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\tests\unit\test_textUtils.py`  
**Current**: `F:\nvda\gh\alphajp\tests\unit\test_textUtils.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_textUtils.py" "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\test_textUtils.py"
index 3229be415d..6993ac7d96 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_textUtils.py"
+++ "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\test_textUtils.py"
@@ -1,13 +1,14 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2019-2024 NV Access Limited, Babbage B.V., Leonard de Ruijter
+# Copyright (C) 2019-2025 NV Access Limited, Babbage B.V., Leonard de Ruijter
 
 """Unit tests for the textUtils module."""
 
 import unittest
 
 from textUtils import UnicodeNormalizationOffsetConverter, WideStringOffsetConverter
+from textUtils.uniscribe import splitAtCharacterBoundaries
 
 FACE_PALM = "\U0001f926"  # 🤦
 SMILE = "\U0001f60a"  # 😊
@@ -358,3 +359,86 @@ def test_normalizedOffsetsMixedIJ(self):
 		self.assertSequenceEqual(converter.computedStrToEncodedOffsets, expectedStrToEncoded)
 		expectedEncodedToStr = (0, 0, 1, 2, 3, 3, 4, 5, 6, 6)
 		self.assertSequenceEqual(converter.computedEncodedToStrOffsets, expectedEncodedToStr)
+
+
+class TestUniscribeSplitAtCharacterBoundaries(unittest.TestCase):
+	"""Several tests for the splitAtCharacterBoundaries function."""
+
+	def _testHelper(self, input: str, expected: list[str]) -> None:
+		self.assertSequenceEqual(list(splitAtCharacterBoundaries(input)), expected)
+
+	def test_emptyString(self):
+		self._testHelper("", [])
+
+	def test_singleBasicCharacter(self):
+		self._testHelper("a", ["a"])
+
+	def test_multipleBasicCharacters(self):
+		text = "Hello"
+		self._testHelper(text, list(text))
+
+	def test_longSentence(self):
+		text = "This is a longer sentence, with punctuation!"
+		self._testHelper(text, list(text))
+
+	def test_emojis(self):
+		text = "😊🤦👍"
+		self._testHelper(text, list(text))
+
+	def test_compositeCharacters(self):
+		self._testHelper("áéĳ", ["á", "é", "ĳ"])
+
+	def test_singleAcute(self):
+		self._testHelper("\u0301", ["\u0301"])
+
+	def test_acuteWithSpaceBefore(self):
+		# The acute is bound to the space
+		self._testHelper(" \u0301", [" \u0301"])
+
+	def test_acuteWithSpaceAfter(self):
+		self._testHelper("\u0301 ", ["\u0301", " "])
+
+	def test_sentenceWithComposites(self):
+		text = "Één eigenwĳze geïnteresseerde ĳsbeer"
+		expected = [
+			"É",
+			"é",
+			"n",
+			" ",
+			"e",
+			"i",
+			"g",
+			"e",
+			"n",
+			"w",
+			"ĳ",
+			"z",
+			"e",
+			" ",
+			"g",
+			"e",
+			"ï",
+			"n",
+			"t",
+			"e",
+			"r",
+			"e",
+			"s",
+			"s",
+			"e",
+			"e",
+			"r",
+			"d",
+			"e",
+			" ",
+			"ĳ",
+			"s",
+			"b",
+			"e",
+			"e",
+			"r",
+		]
+		self._testHelper(text, expected)
+
+	def test_hebrew(self):
+		self._testHelper("בְּרֵאשִׁית", ["בְּ", "רֵ", "א", "שִׁ", "י", "ת"])

```