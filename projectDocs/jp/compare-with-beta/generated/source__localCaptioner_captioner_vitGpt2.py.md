# Diff for: `source\_localCaptioner\captioner\vitGpt2.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\_localCaptioner\captioner\vitGpt2.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\_localCaptioner\captioner\vitGpt2.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_localCaptioner\\captioner\\vitGpt2.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_localCaptioner\\captioner\\vitGpt2.py"
index 47af56c..6224c3a 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_localCaptioner\\captioner\\vitGpt2.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_localCaptioner\\captioner\\vitGpt2.py"
@@ -86,10 +86,7 @@ def __init__(
 		try:
 			self.encoderSession = ort.InferenceSession(encoderPath, sess_options=sessionOptions)
 			self.decoderSession = ort.InferenceSession(decoderPath, sess_options=sessionOptions)
-		except (
-			ort.capi.onnxruntime_pybind11_state.InvalidProtobuf,
-			ort.capi.onnxruntime_pybind11_state.NoSuchFile,
-		) as e:
+		except ort.capi.onnxruntime_pybind11_state.InvalidProtobuf as e:
 			raise FileNotFoundError(
 				"model file incomplete"
 				f" Please check whether the file is complete or re-download. Original error: {e}",
@@ -145,7 +142,7 @@ def _loadVocab(self, vocabPath: str) -> dict[int, str]:
 
 			# Convert to id -> token format
 			vocab = {v: k for k, v in vocabData.items()}
-			log.debug(f"Successfully loaded vocabulary with {len(vocab)} tokens")
+			log.info(f"Successfully loaded vocabulary with {len(vocab)} tokens")
 			return vocab
 
 		except FileNotFoundError:

```