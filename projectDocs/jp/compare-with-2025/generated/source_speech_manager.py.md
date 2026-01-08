# Diff for: `source\speech\manager.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\speech\manager.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\speech\manager.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\speech\\manager.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\speech\\manager.py"
index 71d4c4f..2f2507f 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\speech\\manager.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\speech\\manager.py"
@@ -495,7 +495,7 @@ def _checkForCancellations(self, utterance: SpeechSequence) -> bool:
 		utteranceIndex = self._getUtteranceIndex(utterance)
 		if utteranceIndex is None:
 			raise IndexError(
-				f"no utterance index({utteranceIndex}, cant save cancellable commands",
+				f"no utterance index({utterance}), can't save cancellable commands",
 			)
 		cancellableItems = list(
 			item for item in reversed(utterance) if isinstance(item, _CancellableSpeechCommand)

```