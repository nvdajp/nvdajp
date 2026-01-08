# Diff for: `source\winBindings\winmm.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\winmm.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\winmm.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\winmm.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\winmm.py"
index f0d814f..9bcbf23 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\winmm.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\winmm.py"
@@ -6,7 +6,6 @@
 """Functions exported by winmm.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	c_size_t,
 	windll,
 	c_long,
@@ -24,7 +23,7 @@
 dll = windll.winmm
 
 
-waveOutGetNumDevs = WINFUNCTYPE(None)(("waveOutGetNumDevs", dll))
+waveOutGetNumDevs = dll.waveOutGetNumDevs
 """
 Retrieves the number of waveform-audio output devices present in the system.
 
@@ -34,7 +33,7 @@
 waveOutGetNumDevs.restype = UINT
 waveOutGetNumDevs.argtypes = ()
 
-waveOutMessage = WINFUNCTYPE(None)(("waveOutMessage", dll))
+waveOutMessage = dll.waveOutMessage
 """
 Sends a message to the given waveform-audio output device.
 

```