# Diff for: `tests\unit\contentRecog\test_contentRecog.py`

**Source**: `F:\nvda\gh\alphajp-251219\tests\unit\contentRecog\test_contentRecog.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\unit\contentRecog\test_contentRecog.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\contentRecog\\test_contentRecog.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\contentRecog\\test_contentRecog.py"
index b62ac14..3f355ef 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\contentRecog\\test_contentRecog.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\contentRecog\\test_contentRecog.py"
@@ -70,24 +70,27 @@ class TestLinesWordsResult(unittest.TestCase):
 		],
 	]
 	TOP = 0
-	BOTTOM = 23
-	WORD1_OFFSETS = (0, 6)
+	# BEGIN JP PATCH
+	# nvdajp: East Asian narrow characters don't have spaces between them
+	BOTTOM = 21
+	WORD1_OFFSETS = (0, 5)
 	WORD1_SECOND = 1
-	WORD1_LAST = 5
+	WORD1_LAST = 4
 	WORD1_RECT = RectLTWH(100, 200, 10, 20)
-	WORD2_START = 6
-	WORD2_OFFSETS = (6, 12)
+	WORD2_START = 5
+	WORD2_OFFSETS = (5, 11)
 	WORD2_RECT = RectLTWH(110, 200, 10, 20)
-	WORD3_OFFSETS = (12, 18)
-	WORD3_START = 12
+	WORD3_OFFSETS = (11, 16)
+	WORD3_START = 11
 	WORD3_RECT = RectLTWH(100, 220, 10, 20)
-	WORD4_OFFSETS = (18, 24)
+	WORD4_OFFSETS = (16, 22)
 	WORD4_RECT = RectLTWH(110, 220, 10, 20)
-	LINE1_OFFSETS = (0, 12)
+	LINE1_OFFSETS = (0, 11)
 	LINE1_SECOND = 1
-	LINE1_LAST = 11
-	LINE2_OFFSETS = (12, 24)
-	LINE2_START = 12
+	LINE1_LAST = 10
+	LINE2_OFFSETS = (11, 22)
+	LINE2_START = 11
+	# END JP PATCH
 
 	def setUp(self):
 		info = contentRecog.RecogImageInfo(0, 0, 1000, 2000, 1)
@@ -96,7 +99,10 @@ def setUp(self):
 		self.textInfo = self.result.makeTextInfo(self.fakeObj, textInfos.POSITION_FIRST)
 
 	def test_text(self):
+		# BEGIN JP PATCH
+		# nvdajp: East Asian narrow characters don't have spaces between them
 		self.assertEqual(self.result.text, "word1word2\nword3word4\n")
+		# END JP PATCH
 
 	def test_textLen(self):
 		self.assertEqual(self.result.textLen, len(self.result.text))

```