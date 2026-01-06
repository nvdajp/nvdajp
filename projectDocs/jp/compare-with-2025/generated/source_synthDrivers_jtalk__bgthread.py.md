# Diff for: `source\synthDrivers\jtalk\_bgthread.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\synthDrivers\jtalk\_bgthread.py`  
**Current**: `F:\nvda\gh\alphajp\source\synthDrivers\jtalk\_bgthread.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\_bgthread.py" "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\jtalk\\_bgthread.py"
index 89cc4dd6c9..0d10c395aa 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\_bgthread.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\jtalk\\_bgthread.py"
@@ -16,7 +16,6 @@
 import queue as Queue
 
 
-
 bgThread = None
 bgQueue = None
 isSpeaking = False
@@ -35,7 +34,7 @@ def run(self):
 				break
 			try:
 				func(*args, **kwargs)
-            except:
+			except Exception:
 				log.error("Error running function from queue", exc_info=True)
 			finally:
 				isSpeaking = False

```