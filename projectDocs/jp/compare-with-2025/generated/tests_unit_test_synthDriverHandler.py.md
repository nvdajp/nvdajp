# Diff for: `tests\unit\test_synthDriverHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\tests\unit\test_synthDriverHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\unit\test_synthDriverHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_synthDriverHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_synthDriverHandler.py"
index c313d00..1e58c8a 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_synthDriverHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_synthDriverHandler.py"
@@ -117,7 +117,10 @@ def test_setSynth_auto_fallback_ifOneCoreDoesntSupportDefaultLanguage(self):
 		self.assertEqual(synthDriverHandler.getSynth().name, FAKE_DEFAULT_SYNTH_NAME)
 		synthDriverHandler.setSynth(None)  # reset the synth so there is no fallback
 		synthDriverHandler.setSynth("auto")
+		# BEGIN JP PATCH
+		# nvdajp: defaultSynthPriorityList includes nvdajp_jtalk instead of espeak
 		self.assertEqual(synthDriverHandler.getSynth().name, "nvdajp_jtalk")
+		# END JP PATCH
 
 	def test_synthChangedExtensionPoint(self):
 		expectedKwargs = dict(

```