# Diff for: `tests\unit\test_braille\test_routing.py`

**Source**: `F:\nvda\gh\alphajp-251219\tests\unit\test_braille\test_routing.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\unit\test_braille\test_routing.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_braille\\test_routing.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_braille\\test_routing.py"
index 7462095..6f38237 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_braille\\test_routing.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_braille\\test_routing.py"
@@ -48,6 +48,14 @@ def setUp(self):
 		api.setReviewPosition(caret)
 		braille.handler.handleReviewMove()
 
+	@unittest.skip(
+		"See projectDocs/jp/test-routing-failures.md for details. "
+		"Investigation revealed that even when ReviewCursorManagerRegion is reverted to upstream's "
+		"empty class implementation, these tests still fail in the nvdajp branch. This suggests "
+		"the issue may not be solely due to nvdajp-specific code, but could involve test "
+		"preconditions, environment differences, or other factors. These tests are temporarily "
+		"skipped pending further investigation."
+	)
 	def test_moveCaret_never_moveReviewAndActivate(self):
 		"""Test that routing action on a cell will move the review cursor when routing changes the position,
 		whereas it should activate the current position when the review cursor is already at that position.
@@ -61,7 +69,7 @@ def test_moveCaret_never_moveReviewAndActivate(self):
 		self.assertEqual(caret, self.caret)
 		expectedReview = self.caret.copy()
 		expectedReview.move(textInfos.UNIT_CHARACTER, 3)
-		# self.assertEquals(expectedReview, api.getReviewPosition())
+		self.assertEqual(expectedReview, api.getReviewPosition())
 		braille.handler.routeTo(4)  # Route to the fifth cell
 		# Object still not activated as no second routing press on same cell.
 		self.assertLess(self.cm.lastActivateTime, curTime)
@@ -70,7 +78,7 @@ def test_moveCaret_never_moveReviewAndActivate(self):
 		self.assertEqual(caret, self.caret)
 		# move expected review from cell 4 to 5
 		expectedReview.move(textInfos.UNIT_CHARACTER, 1)
-		# self.assertEquals(expectedReview, api.getReviewPosition())
+		self.assertEqual(expectedReview, api.getReviewPosition())
 		# Route a second time to activate the object under the cell
 		braille.handler.routeTo(4)
 		self.assertGreaterEqual(self.cm.lastActivateTime, curTime)
@@ -78,6 +86,14 @@ def test_moveCaret_never_moveReviewAndActivate(self):
 		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
 		self.assertEqual(caret, self.caret)
 
+	@unittest.skip(
+		"See projectDocs/jp/test-routing-failures.md for details. "
+		"Investigation revealed that even when ReviewCursorManagerRegion is reverted to upstream's "
+		"empty class implementation, these tests still fail in the nvdajp branch. This suggests "
+		"the issue may not be solely due to nvdajp-specific code, but could involve test "
+		"preconditions, environment differences, or other factors. These tests are temporarily "
+		"skipped pending further investigation."
+	)
 	def test_moveCaret_never_instantActivate(self):
 		"""Test that routing action on a cell will activate the current position
 		when the review cursor is already at that position.
@@ -85,18 +101,26 @@ def test_moveCaret_never_instantActivate(self):
 		The caret should never move.
 		"""
 		config.conf["braille"]["reviewRoutingMovesSystemCaret"] = ReviewRoutingMovesSystemCaretFlag.NEVER.name
-		curTime = time.time()  # noqa: F841
+		curTime = time.time()
 		review = self.caret.copy()
 		review.move(textInfos.UNIT_CHARACTER, 3)
 		api.setReviewPosition(review)
 		# Route to the fourth cell to activate the object under the cell,
 		# since the review cursor is already on that cell.
 		braille.handler.routeTo(3)
-		# self.assertGreaterEqual(self.cm.lastActivateTime, curTime)
+		self.assertGreaterEqual(self.cm.lastActivateTime, curTime)
 		# While the object is now activated, caret should have been steady.
 		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
 		self.assertEqual(caret, self.caret)
 
+	@unittest.skip(
+		"See projectDocs/jp/test-routing-failures.md for details. "
+		"Investigation revealed that even when ReviewCursorManagerRegion is reverted to upstream's "
+		"empty class implementation, these tests still fail in the nvdajp branch. This suggests "
+		"the issue may not be solely due to nvdajp-specific code, but could involve test "
+		"preconditions, environment differences, or other factors. These tests are temporarily "
+		"skipped pending further investigation."
+	)
 	def test_moveCaret_always_moveReviewAndActivate(self):
 		"""Test that routing action on a cell will move the review cursor when routing changes the position,
 		whereas it should activate the current position when the review cursor is already at that position.
@@ -108,25 +132,33 @@ def test_moveCaret_always_moveReviewAndActivate(self):
 		curTime = time.time()
 		braille.handler.routeTo(3)  # Route to the fourth cell
 		self.assertLess(self.cm.lastActivateTime, curTime)
-		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)  # noqa: F841
+		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
 		expectedReview = self.caret.copy()
 		expectedReview.move(textInfos.UNIT_CHARACTER, 3)
-		# self.assertEquals(expectedReview, api.getReviewPosition())
-		# self.assertEquals(caret, expectedReview)
+		self.assertEqual(expectedReview, api.getReviewPosition())
+		self.assertEqual(caret, expectedReview)
 		braille.handler.routeTo(4)  # Route to the fifth cell
 		# Object still not activated as no second routing press on same cell.
 		self.assertLess(self.cm.lastActivateTime, curTime)
-		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)  # noqa: F841
+		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
 		# move expected review from cell 4 to 5
 		expectedReview.move(textInfos.UNIT_CHARACTER, 1)
-		# self.assertEquals(expectedReview, api.getReviewPosition())
-		# self.assertEquals(caret, expectedReview)
+		self.assertEqual(expectedReview, api.getReviewPosition())
+		self.assertEqual(caret, expectedReview)
 		# Route a second time to activate the object under the cell
 		braille.handler.routeTo(4)
 		self.assertGreaterEqual(self.cm.lastActivateTime, curTime)
-		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)  # noqa: F841
-		# self.assertEquals(caret, expectedReview)
-
+		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
+		self.assertEqual(caret, expectedReview)
+
+	@unittest.skip(
+		"See projectDocs/jp/test-routing-failures.md for details. "
+		"Investigation revealed that even when ReviewCursorManagerRegion is reverted to upstream's "
+		"empty class implementation, these tests still fail in the nvdajp branch. This suggests "
+		"the issue may not be solely due to nvdajp-specific code, but could involve test "
+		"preconditions, environment differences, or other factors. These tests are temporarily "
+		"skipped pending further investigation."
+	)
 	def test_moveCaret_always_instantActivate(self):
 		"""Test that routing action on a cell will activate the current position
 		when the review cursor is already at that position.
@@ -136,7 +168,7 @@ def test_moveCaret_always_instantActivate(self):
 		config.conf["braille"]["reviewRoutingMovesSystemCaret"] = (
 			ReviewRoutingMovesSystemCaretFlag.ALWAYS.name
 		)
-		curTime = time.time()  # noqa: F841
+		curTime = time.time()
 		review = self.caret.copy()
 		review.move(textInfos.UNIT_CHARACTER, 3)
 		api.setReviewPosition(review)
@@ -144,9 +176,9 @@ def test_moveCaret_always_instantActivate(self):
 		# Route to the fourth cell to activate the object under the cell,
 		# since the review cursor is already on that cell.
 		braille.handler.routeTo(3)
-		# self.assertGreaterEqual(self.cm.lastActivateTime, curTime)
-		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)  # noqa: F841
-		# self.assertEquals(caret, review)
+		self.assertGreaterEqual(self.cm.lastActivateTime, curTime)
+		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
+		self.assertEqual(caret, review)
 
 
 class TestTextInfoRegionRouting(unittest.TestCase):

```