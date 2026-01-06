# Diff for: `tests\unit\test_synthDriverHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\tests\unit\test_synthDriverHandler.py`  
**Current**: `F:\nvda\gh\alphajp\tests\unit\test_synthDriverHandler.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_synthDriverHandler.py" "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\test_synthDriverHandler.py"
index c313d00056..e345672fcd 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_synthDriverHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\test_synthDriverHandler.py"
@@ -117,7 +117,7 @@ def test_setSynth_auto_fallback_ifOneCoreDoesntSupportDefaultLanguage(self):
 		self.assertEqual(synthDriverHandler.getSynth().name, FAKE_DEFAULT_SYNTH_NAME)
 		synthDriverHandler.setSynth(None)  # reset the synth so there is no fallback
 		synthDriverHandler.setSynth("auto")
-		self.assertEqual(synthDriverHandler.getSynth().name, "nvdajp_jtalk")
+		self.assertEqual(synthDriverHandler.getSynth().name, "espeak")
 
 	def test_synthChangedExtensionPoint(self):
 		expectedKwargs = dict(

```