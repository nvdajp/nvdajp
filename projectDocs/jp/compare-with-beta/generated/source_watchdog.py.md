# Diff for: `source\watchdog.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\watchdog.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\watchdog.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\watchdog.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\watchdog.py"
index c9f55be..bf47358 100644
--- "a/F:\\nvda\\gh\\beta\\source\\watchdog.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\watchdog.py"
@@ -4,6 +4,7 @@
 # See the file COPYING for more details.
 
 import sys
+import os
 import time
 from time import perf_counter as _timer
 import threading
@@ -13,19 +14,15 @@
 import inspect
 import ctypes.wintypes
 import comtypes
-import globalVars
 import winBindings.ole32
 import winBindings.dbgHelp
 import winBindings.kernel32
+from winBindings.kernel32 import UnhandledExceptionFilter
 import winUser
 import winKernel
 from logHandler import log
 import logHandler
-from utils._crashHandler import (
-	CRASH_STATS,
-	crashHandler,
-	loadRecentCrashTimestamps,
-)
+import globalVars
 import core
 import exceptions
 import NVDAHelper
@@ -239,6 +236,30 @@ def _recoverAttempt():
 		pass
 
 
+@UnhandledExceptionFilter
+def _crashHandler(exceptionInfo):
+	threadId = winBindings.kernel32.GetCurrentThreadId()
+	# An exception might have been set for this thread.
+	# Clear it so that it doesn't get raised in this function.
+	ctypes.pythonapi.PyThreadState_SetAsyncExc(threadId, None)
+
+	# Write a minidump.
+	dumpPath = os.path.join(os.path.dirname(globalVars.appArgs.logFileName), "nvda_crash.dmp")
+	if not NVDAHelper.localLib.writeCrashDump(dumpPath, exceptionInfo):
+		log.critical("NVDA crashed! Error writing minidump", exc_info=True)
+	else:
+		log.critical("NVDA crashed! Minidump written to %s" % dumpPath)
+
+	# Log Python stacks for every thread.
+	stacks = logHandler.getFormattedStacksForAllThreads()
+	log.info(f"Listing stacks for Python threads:\n{stacks}")
+
+	log.info("Restarting due to crash")
+	# if NVDA has crashed we cannot rely on the queue handler to start the new NVDA instance
+	core.restartUnsafely()
+	return 1  # EXCEPTION_EXECUTE_HANDLER
+
+
 @ctypes.WINFUNCTYPE(None)
 def _notifySendMessageCancelled():
 	caller = inspect.currentframe().f_back
@@ -260,19 +281,8 @@ def initialize():
 	if isRunning:
 		raise RuntimeError("already running")
 	isRunning = True
-	if not globalVars.appArgs.secure:
-		now = time.time()
-		recentCrashes = loadRecentCrashTimestamps(now)
-		if len(recentCrashes) >= CRASH_STATS.maxCount:
-			log.error(
-				f"Crash loop detected ({len(recentCrashes)} crashes in {CRASH_STATS.timeout:.0f} seconds). "
-				"Automatic crash recovery will remain disabled until the loop clears.",
-			)
-		else:
-			# Catch application crashes if the handler is enabled.
-			winBindings.kernel32.SetUnhandledExceptionFilter(crashHandler)
-	else:
-		log.debug("Not enabling crash recovery as NVDA is running in secure mode.")
+	# Catch application crashes.
+	winBindings.kernel32.SetUnhandledExceptionFilter(_crashHandler)
 	winBindings.ole32.CoEnableCallCancellation(None)
 	# Cache cancelCallEvent.
 	_cancelCallEvent = ctypes.wintypes.HANDLE.in_dll(

```