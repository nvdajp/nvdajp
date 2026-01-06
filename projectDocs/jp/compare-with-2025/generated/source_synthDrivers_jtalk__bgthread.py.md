# Diff for: `source\synthDrivers\jtalk\_bgthread.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\synthDrivers\jtalk\_bgthread.py`  
**Current**: `F:\nvda\gh\alphajp\source\synthDrivers\jtalk\_bgthread.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\_bgthread.py" "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\jtalk\\_bgthread.py"
index 89cc4dd6c9..ee865ac6a2 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\_bgthread.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\jtalk\\_bgthread.py"
@@ -16,54 +16,57 @@
 import queue as Queue
 
 
-
 bgThread = None
 bgQueue = None
 isSpeaking = False
 
 
 class BgThread(threading.Thread):
-    def __init__(self):
-        threading.Thread.__init__(self)
-        self.setDaemon(True)
+	def __init__(self):
+		threading.Thread.__init__(self)
+		self.setDaemon(True)
 
-    def run(self):
-        global isSpeaking
-        while True:
-            func, args, kwargs = bgQueue.get()
-            if not func:
-                break
-            try:
-                func(*args, **kwargs)
-            except:
-                log.error("Error running function from queue", exc_info=True)
-            finally:
-                isSpeaking = False
-                bgQueue.task_done()
+	def run(self):
+		global isSpeaking
+		assert bgQueue is not None  # Type narrowing for type checkers
+		while True:
+			func, args, kwargs = bgQueue.get()
+			if not func:
+				break
+			try:
+				func(*args, **kwargs)
+			except Exception:
+				log.error("Error running function from queue", exc_info=True)
+			finally:
+				isSpeaking = False
+				bgQueue.task_done()
 
 
 def execWhenDone(func, *args, **kwargs):
-    global bgQueue
-    # This can't be a kwarg in the function definition because it will consume the first non-keywor dargument which is meant for func.
-    mustBeAsync = kwargs.pop("mustBeAsync", False)
-    if mustBeAsync or bgQueue.unfinished_tasks != 0:
-        # Either this operation must be asynchronous or There is still an operation in progress.
-        # Therefore, run this asynchronously in the background thread.
-        bgQueue.put((func, args, kwargs))
-    else:
-        func(*args, **kwargs)
+	global bgQueue
+	assert bgQueue is not None  # Type narrowing for type checkers
+	# This can't be a kwarg in the function definition because it will consume the first non-keywor dargument which is meant for func.
+	mustBeAsync = kwargs.pop("mustBeAsync", False)
+	if mustBeAsync or bgQueue.unfinished_tasks != 0:
+		# Either this operation must be asynchronous or There is still an operation in progress.
+		# Therefore, run this asynchronously in the background thread.
+		bgQueue.put((func, args, kwargs))
+	else:
+		func(*args, **kwargs)
 
 
 def initialize():
-    global bgThread, bgQueue
-    bgQueue = Queue.Queue()
-    bgThread = BgThread()
-    bgThread.start()
+	global bgThread, bgQueue
+	bgQueue = Queue.Queue()
+	bgThread = BgThread()
+	bgThread.start()
 
 
 def terminate():
-    global bgThread, bgQueue
-    bgQueue.put((None, None, None))
-    bgThread.join()
-    bgThread = None
-    bgQueue = None
+	global bgThread, bgQueue
+	assert bgQueue is not None  # Type narrowing for type checkers
+	assert bgThread is not None  # Type narrowing for type checkers
+	bgQueue.put((None, None, None))
+	bgThread.join()
+	bgThread = None
+	bgQueue = None

```