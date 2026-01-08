# Diff for: `source\watchdog.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\watchdog.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\watchdog.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\watchdog.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\watchdog.py"
index 5410fdc..c9f55be 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\watchdog.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\watchdog.py"
@@ -1,10 +1,9 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2008-2024 NV Access Limited, Cyrille Bougot
+# Copyright (C) 2008-2025 NV Access Limited, Cyrille Bougot
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
 import sys
-import os
 import time
 from time import perf_counter as _timer
 import threading
@@ -12,15 +11,21 @@
 	Any,
 )
 import inspect
-from ctypes import windll, oledll
 import ctypes.wintypes
-import msvcrt
 import comtypes
+import globalVars
+import winBindings.ole32
+import winBindings.dbgHelp
+import winBindings.kernel32
 import winUser
 import winKernel
 from logHandler import log
 import logHandler
-import globalVars
+from utils._crashHandler import (
+	CRASH_STATS,
+	crashHandler,
+	loadRecentCrashTimestamps,
+)
 import core
 import exceptions
 import NVDAHelper
@@ -62,7 +67,7 @@ def __getattr__(attrName: str) -> Any:
 isAttemptingRecovery: bool = False
 _coreIsAsleep = False
 
-_coreDeadTimer = windll.kernel32.CreateWaitableTimerW(None, True, None)
+_coreDeadTimer = winBindings.kernel32.CreateWaitableTimer(None, True, None)
 _suspended = False
 _watcherThread = None
 _cancelCallEvent = None
@@ -73,11 +78,11 @@ def alive():
 	global _coreIsAsleep
 	_coreIsAsleep = False
 	# Stop cancelling calls.
-	windll.kernel32.ResetEvent(_cancelCallEvent)
+	winBindings.kernel32.ResetEvent(_cancelCallEvent)
 	# Set the timer so the watcher will take action in MIN_CORE_ALIVE_TIMEOUT
 	# if this function or asleep() isn't called.
 	SECOND_TO_100_NANOSECOND = 10**7  # nanosecond is 10^9, 10^7 is hundreds of nanoseconds
-	windll.kernel32.SetWaitableTimer(
+	winBindings.kernel32.SetWaitableTimer(
 		_coreDeadTimer,
 		ctypes.byref(
 			ctypes.wintypes.LARGE_INTEGER(
@@ -93,7 +98,7 @@ def alive():
 			),
 		),
 		0,
-		None,
+		winBindings.kernel32.PTIMERAPCROUTINE(0),
 		None,
 		False,
 	)
@@ -106,7 +111,7 @@ def asleep():
 	alive()
 	# CancelWaitableTimer does not reset the signaled state; if it was signaled, it remains signaled.
 	# However, alive() calls SetWaitableTimer, which resets the timer to unsignaled.
-	windll.kernel32.CancelWaitableTimer(_coreDeadTimer)
+	winBindings.kernel32.CancelWaitableTimer(_coreDeadTimer)
 	_coreIsAsleep = True
 
 
@@ -178,7 +183,7 @@ def waitForFreezeRecovery(waitedSince: float):
 
 	# Cancel calls until the core is alive.
 	# This event will be reset by alive().
-	windll.kernel32.SetEvent(_cancelCallEvent)
+	winBindings.kernel32.SetEvent(_cancelCallEvent)
 
 	# Some calls have to be killed individually.
 	while not _isAlive():
@@ -229,62 +234,11 @@ def _shouldRecoverAfterMinTimeout():
 
 def _recoverAttempt():
 	try:
-		oledll.ole32.CoCancelCall(core.mainThreadId, 0)
+		winBindings.ole32.CoCancelCall(core.mainThreadId, 0)
 	except:  # noqa: E722
 		pass
 
 
-class MINIDUMP_EXCEPTION_INFORMATION(ctypes.Structure):
-	_fields_ = (
-		("ThreadId", ctypes.wintypes.DWORD),
-		("ExceptionPointers", ctypes.c_void_p),
-		("ClientPointers", ctypes.wintypes.BOOL),
-	)
-
-
-@ctypes.WINFUNCTYPE(ctypes.wintypes.LONG, ctypes.c_void_p)
-def _crashHandler(exceptionInfo):
-	threadId = ctypes.windll.kernel32.GetCurrentThreadId()
-	# An exception might have been set for this thread.
-	# Clear it so that it doesn't get raised in this function.
-	ctypes.pythonapi.PyThreadState_SetAsyncExc(threadId, None)
-
-	# Write a minidump.
-	dumpPath = os.path.join(os.path.dirname(globalVars.appArgs.logFileName), "nvda_crash.dmp")
-	try:
-		# Though we aren't using pythonic functions to write to the dump file,
-		# open it in binary mode as opening it in text mode (the default) doesn't make sense.
-		with open(dumpPath, "wb") as mdf:
-			mdExc = MINIDUMP_EXCEPTION_INFORMATION(
-				ThreadId=threadId,
-				ExceptionPointers=exceptionInfo,
-				ClientPointers=False,
-			)
-			if not ctypes.windll.DbgHelp.MiniDumpWriteDump(
-				winKernel.kernel32.GetCurrentProcess(),
-				globalVars.appPid,
-				msvcrt.get_osfhandle(mdf.fileno()),
-				0,  # MiniDumpNormal
-				ctypes.byref(mdExc),
-				None,
-				None,
-			):
-				raise ctypes.WinError()
-	except:  # noqa: E722
-		log.critical("NVDA crashed! Error writing minidump", exc_info=True)
-	else:
-		log.critical("NVDA crashed! Minidump written to %s" % dumpPath)
-
-	# Log Python stacks for every thread.
-	stacks = logHandler.getFormattedStacksForAllThreads()
-	log.info(f"Listing stacks for Python threads:\n{stacks}")
-
-	log.info("Restarting due to crash")
-	# if NVDA has crashed we cannot rely on the queue handler to start the new NVDA instance
-	core.restartUnsafely()
-	return 1  # EXCEPTION_EXECUTE_HANDLER
-
-
 @ctypes.WINFUNCTYPE(None)
 def _notifySendMessageCancelled():
 	caller = inspect.currentframe().f_back
@@ -306,17 +260,28 @@ def initialize():
 	if isRunning:
 		raise RuntimeError("already running")
 	isRunning = True
-	# Catch application crashes.
-	windll.kernel32.SetUnhandledExceptionFilter(_crashHandler)
-	oledll.ole32.CoEnableCallCancellation(None)
+	if not globalVars.appArgs.secure:
+		now = time.time()
+		recentCrashes = loadRecentCrashTimestamps(now)
+		if len(recentCrashes) >= CRASH_STATS.maxCount:
+			log.error(
+				f"Crash loop detected ({len(recentCrashes)} crashes in {CRASH_STATS.timeout:.0f} seconds). "
+				"Automatic crash recovery will remain disabled until the loop clears.",
+			)
+		else:
+			# Catch application crashes if the handler is enabled.
+			winBindings.kernel32.SetUnhandledExceptionFilter(crashHandler)
+	else:
+		log.debug("Not enabling crash recovery as NVDA is running in secure mode.")
+	winBindings.ole32.CoEnableCallCancellation(None)
 	# Cache cancelCallEvent.
 	_cancelCallEvent = ctypes.wintypes.HANDLE.in_dll(
-		NVDAHelper.localLib,
+		NVDAHelper.localLib.dll,
 		"cancelCallEvent",
 	)
 	# Handle cancelled SendMessage calls.
 	NVDAHelper._setDllFuncPointer(
-		NVDAHelper.localLib,
+		NVDAHelper.localLib.dll,
 		"_notifySendMessageCancelled",
 		_notifySendMessageCancelled,
 	)
@@ -335,13 +300,13 @@ def terminate():
 	if not isRunning:
 		return
 	isRunning = False
-	oledll.ole32.CoDisableCallCancellation(None)
+	winBindings.ole32.CoDisableCallCancellation(None)
 	# Wake up the watcher so it knows to finish.
-	windll.kernel32.SetWaitableTimer(
+	winBindings.kernel32.SetWaitableTimer(
 		_coreDeadTimer,
 		ctypes.byref(ctypes.wintypes.LARGE_INTEGER(0)),
 		0,
-		None,
+		winBindings.kernel32.PTIMERAPCROUTINE(0),
 		None,
 		False,
 	)
@@ -371,7 +336,7 @@ def __init__(self):
 		super(CancellableCallThread, self).__init__()
 		self.daemon = True
 		self._executeEvent = threading.Event()
-		self._executionDoneEvent = ctypes.windll.kernel32.CreateEventW(None, False, False, None)
+		self._executionDoneEvent = winBindings.kernel32.CreateEvent(None, False, False, None)
 		self.isUsable = True
 
 	def execute(self, func, *args, pumpMessages=True, **kwargs):
@@ -394,7 +359,7 @@ def execute(self, func, *args, pumpMessages=True, **kwargs):
 		)
 		waitIndex = ctypes.wintypes.DWORD()
 		if pumpMessages:
-			oledll.ole32.CoWaitForMultipleHandles(
+			winBindings.ole32.CoWaitForMultipleHandles(
 				0,
 				winKernel.INFINITE,
 				2,
@@ -402,7 +367,7 @@ def execute(self, func, *args, pumpMessages=True, **kwargs):
 				ctypes.byref(waitIndex),
 			)
 		else:
-			waitIndex.value = windll.kernel32.WaitForMultipleObjects(
+			waitIndex.value = winBindings.kernel32.WaitForMultipleObjects(
 				2,
 				waitHandles,
 				False,
@@ -431,8 +396,8 @@ def run(self):
 				self._result = self._func(*self._args, **self._kwargs)
 			except Exception as e:
 				self._exc_info = e
-			ctypes.windll.kernel32.SetEvent(self._executionDoneEvent)
-		ctypes.windll.kernel32.CloseHandle(self._executionDoneEvent)
+			winBindings.kernel32.SetEvent(self._executionDoneEvent)
+		winBindings.kernel32.CloseHandle(self._executionDoneEvent)
 
 
 cancellableCallThread = None
@@ -467,12 +432,12 @@ def cancellableSendMessage(hwnd, msg, wParam, lParam, flags=0, timeout=60000):
 	The call will still be cancelled if appropriate even if the specified timeout has not yet been reached.
 	@raise CallCancelled: If the call was cancelled.
 	"""
-	result = ctypes.wintypes.DWORD()
+	result = NVDAHelper.localLib.DWORD_PTR()
 	NVDAHelper.localLib.cancellableSendMessageTimeout(
 		hwnd,
 		msg,
-		wParam,
-		lParam,
+		wParam or 0,
+		lParam or 0,
 		flags,
 		timeout,
 		ctypes.byref(result),

```