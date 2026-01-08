# Diff for: `source\hwIo\ioThread.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\hwIo\ioThread.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\hwIo\ioThread.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\hwIo\\ioThread.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\hwIo\\ioThread.py"
index 18015ef..fbcc13f 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\hwIo\\ioThread.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\hwIo\\ioThread.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2016-2023 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau,
+# Copyright (C) 2016-2025 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau,
 # Leonard de Ruijter
 
 import ctypes
@@ -14,14 +14,15 @@
 from extensionPoints.util import AnnotatableWeakref, BoundMethodWeakref
 from inspect import ismethod
 from logHandler import getFormattedStacksForAllThreads
+import winBindings.kernel32
+from utils import _deprecate
 
 
-LPOVERLAPPED_COMPLETION_ROUTINE = ctypes.WINFUNCTYPE(
-	None,
-	ctypes.wintypes.DWORD,
-	ctypes.wintypes.DWORD,
-	LPOVERLAPPED,
+__getattr__ = _deprecate.handleDeprecations(
+	_deprecate.MovedSymbol("LPOVERLAPPED_COMPLETION_ROUTINE", "winBindings.kernel32"),
 )
+
+
 ApcT = typing.Callable[[int], None]
 ApcIdT = int
 OverlappedStructAddressT = int
@@ -78,7 +79,7 @@ def __init__(self):
 			daemon=True,
 		)
 
-	@winKernel.PAPCFUNC
+	@winBindings.kernel32.PAPCFUNC
 	def _internalApc(param: ApcIdT):
 		threadinst = threading.current_thread()
 		if not isinstance(threadinst, IoThread):
@@ -107,7 +108,7 @@ def _internalApc(param: ApcIdT):
 				exc_info=True,
 			)
 
-	@LPOVERLAPPED_COMPLETION_ROUTINE
+	@winBindings.kernel32.LPOVERLAPPED_COMPLETION_ROUTINE
 	def _internalCompletionRoutine(
 		error: int,
 		numberOfBytes: int,
@@ -140,7 +141,7 @@ def _internalCompletionRoutine(
 
 	def start(self):
 		super().start()
-		self.handle = ctypes.windll.kernel32.OpenThread(winKernel.THREAD_SET_CONTEXT, False, self.ident)
+		self.handle = winBindings.kernel32.OpenThread(winKernel.THREAD_SET_CONTEXT, False, self.ident)
 
 	def _registerToCallAsApc(
 		self,
@@ -183,7 +184,7 @@ def queueAsApc(
 		@param param: The parameter passed to the APC when called.
 		"""
 		internalParam = self._registerToCallAsApc(func, param)
-		ctypes.windll.kernel32.QueueUserAPC(self._internalApc, self.handle, internalParam)
+		winBindings.kernel32.QueueUserAPC(self._internalApc, self.handle, internalParam)
 
 	def setWaitableTimer(
 		self,
@@ -206,7 +207,7 @@ def setWaitableTimer(
 		winKernel.setWaitableTimer(
 			handle,
 			dueTime,
-			completionRoutine=self._internalApc,
+			completionRoutine=ctypes.cast(self._internalApc, winBindings.kernel32.PTIMERAPCROUTINE),
 			arg=internalParam,
 		)
 
@@ -261,7 +262,7 @@ def fakeApc(param):
 	def run(self):
 		try:
 			while True:
-				ctypes.windll.kernel32.SleepEx(winKernel.INFINITE, True)
+				winBindings.kernel32.SleepEx(winKernel.INFINITE, True)
 				if self.exit:
 					break
 		except Exception:

```