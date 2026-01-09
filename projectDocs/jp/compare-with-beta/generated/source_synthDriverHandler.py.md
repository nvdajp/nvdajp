# Diff for: `source\synthDriverHandler.py`

**Source**: `F:\nvda\gh\beta\source\synthDriverHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\synthDriverHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\synthDriverHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDriverHandler.py"
index ba66af5..843d18f 100644
--- "a/F:\\nvda\\gh\\beta\\source\\synthDriverHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDriverHandler.py"
@@ -487,7 +487,10 @@ def getSynthInstance(name, asDefault=False):
 
 # The synthDrivers that should be used by default.
 # The first that successfully initializes will be used when config is set to auto (I.e. new installs of NVDA).
-defaultSynthPriorityList = ["oneCore", "espeak", "silence"]
+# BEGIN JP PATCH
+# nvdajp: use nvdajp_jtalk as the default Japanese synthesizer instead of espeak
+defaultSynthPriorityList = ["oneCore", "nvdajp_jtalk", "silence"]
+# END JP PATCH
 
 
 def setSynth(name: Optional[str], isFallback: bool = False):

```