# Diff for: `source\watchdog.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\watchdog.py`  
**Current**: `F:\nvda\gh\alphajp\source\watchdog.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\watchdog.py" "b/F:\\nvda\\gh\\alphajp\\source\\watchdog.py"
index 5410fdc55c..1ce81eca79 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\watchdog.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\watchdog.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2008-2024 NV Access Limited, Cyrille Bougot
+# Copyright (C) 2008-2025 NV Access Limited, Cyrille Bougot
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -12,10 +12,13 @@
 	Any,
 )
 import inspect
-from ctypes import windll, oledll
+from ctypes import windll
 import ctypes.wintypes
-import msvcrt
 import comtypes
+import winBindings.ole32
+import winBindings.dbgHelp
+import winBindings.kernel32
+from winBindings.kernel32 import UnhandledExceptionFilter
 import winUser
 import winKernel
 from logHandler import log
@@ -229,20 +232,12 @@ def _shouldRecoverAfterMinTimeout():
 
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
+@UnhandledExceptionFilter
 def _crashHandler(exceptionInfo):
 	threadId = ctypes.windll.kernel32.GetCurrentThreadId()
 	# An exception might have been set for this thread.
@@ -251,26 +246,7 @@ def _crashHandler(exceptionInfo):
 
 	# Write a minidump.
 	dumpPath = os.path.join(os.path.dirname(globalVars.appArgs.logFileName), "nvda_crash.dmp")
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
+	if not NVDAHelper.localLib.writeCrashDump(dumpPath, exceptionInfo):
 		log.critical("NVDA crashed! Error writing minidump", exc_info=True)
 	else:
 		log.critical("NVDA crashed! Minidump written to %s" % dumpPath)
@@ -307,16 +283,16 @@ def initialize():
 		raise RuntimeError("already running")
 	isRunning = True
 	# Catch application crashes.
-	windll.kernel32.SetUnhandledExceptionFilter(_crashHandler)
-	oledll.ole32.CoEnableCallCancellation(None)
+	winBindings.kernel32.SetUnhandledExceptionFilter(_crashHandler)
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
@@ -335,7 +311,7 @@ def terminate():
 	if not isRunning:
 		return
 	isRunning = False
-	oledll.ole32.CoDisableCallCancellation(None)
+	winBindings.ole32.CoDisableCallCancellation(None)
 	# Wake up the watcher so it knows to finish.
 	windll.kernel32.SetWaitableTimer(
 		_coreDeadTimer,
@@ -394,7 +370,7 @@ def execute(self, func, *args, pumpMessages=True, **kwargs):
 		)
 		waitIndex = ctypes.wintypes.DWORD()
 		if pumpMessages:
-			oledll.ole32.CoWaitForMultipleHandles(
+			winBindings.ole32.CoWaitForMultipleHandles(
 				0,
 				winKernel.INFINITE,
 				2,
@@ -432,7 +408,7 @@ def run(self):
 			except Exception as e:
 				self._exc_info = e
 			ctypes.windll.kernel32.SetEvent(self._executionDoneEvent)
-		ctypes.windll.kernel32.CloseHandle(self._executionDoneEvent)
+		winBindings.kernel32.CloseHandle(self._executionDoneEvent)
 
 
 cancellableCallThread = None
@@ -467,12 +443,12 @@ def cancellableSendMessage(hwnd, msg, wParam, lParam, flags=0, timeout=60000):
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