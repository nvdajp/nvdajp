# Diff for: `source\synthDrivers\jtalk\_bgthread.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\synthDrivers\jtalk\_bgthread.py`  
**Current**: `F:\nvda\gh\alphajp\source\synthDrivers\jtalk\_bgthread.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\_bgthread.py" "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\jtalk\\_bgthread.py"
index 89cc4dd6c9..ee865ac6a2 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\_bgthread.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\jtalk\\_bgthread.py"
@@ -16,7 +16,6 @@
 import queue as Queue
 
 
-
 bgThread = None
 bgQueue = None
 isSpeaking = False
@@ -29,13 +28,14 @@ def __init__(self):
 
 	def run(self):
 		global isSpeaking
+		assert bgQueue is not None  # Type narrowing for type checkers
 		while True:
 			func, args, kwargs = bgQueue.get()
 			if not func:
 				break
 			try:
 				func(*args, **kwargs)
-            except:
+			except Exception:
 				log.error("Error running function from queue", exc_info=True)
 			finally:
 				isSpeaking = False
@@ -44,6 +44,7 @@ def run(self):
 
 def execWhenDone(func, *args, **kwargs):
 	global bgQueue
+	assert bgQueue is not None  # Type narrowing for type checkers
 	# This can't be a kwarg in the function definition because it will consume the first non-keywor dargument which is meant for func.
 	mustBeAsync = kwargs.pop("mustBeAsync", False)
 	if mustBeAsync or bgQueue.unfinished_tasks != 0:
@@ -63,6 +64,8 @@ def initialize():
 
 def terminate():
 	global bgThread, bgQueue
+	assert bgQueue is not None  # Type narrowing for type checkers
+	assert bgThread is not None  # Type narrowing for type checkers
 	bgQueue.put((None, None, None))
 	bgThread.join()
 	bgThread = None

```