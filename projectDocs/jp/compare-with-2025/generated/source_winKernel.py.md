# Diff for: `source\winKernel.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\winKernel.py`  
**Current**: `F:\nvda\gh\alphajp\source\winKernel.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winKernel.py" "b/F:\\nvda\\gh\\alphajp\\source\\winKernel.py"
index 96d574d37c..ca4cb09784 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winKernel.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\winKernel.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2022 NV Access Limited, Rui Batista, Aleksey Sadovoy, Peter Vagner,
+# Copyright (C) 2006-2025 NV Access Limited, Rui Batista, Aleksey Sadovoy, Peter Vagner,
 # Mozilla Corporation, Babbage B.V., Joseph Lee, Łukasz Golonka
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
@@ -13,11 +13,10 @@
 import contextlib
 import ctypes
 import ctypes.wintypes
-from ctypes import byref, c_byte, POINTER, sizeof, Structure, windll, WinError
-from ctypes.wintypes import BOOL, DWORD, HANDLE, LARGE_INTEGER, LCID, LPWSTR, LPVOID, WORD
+from ctypes import byref, sizeof, Structure, WinError
+from ctypes.wintypes import BOOL, DWORD, HANDLE, LARGE_INTEGER, LCID, LPVOID, WORD
 from typing import (
 	TYPE_CHECKING,
-	Any,
 	Optional,
 	Union,
 )
@@ -26,24 +25,34 @@
 	from winAPI._powerTracking import SystemPowerStatus
 
 
-def __getattr__(attrName: str) -> Any:
-	"""Module level `__getattr__` used to preserve backward compatibility."""
-	import NVDAState
-
-	if attrName == "SYSTEM_POWER_STATUS" and NVDAState._allowDeprecatedAPI():
-		from logHandler import log
-		from winAPI._powerTracking import SystemPowerStatus
-
-		log.warning(
-			"winKernel.SYSTEM_POWER_STATUS is deprecated, "
-			"use winAPI._powerTracking.SystemPowerStatus instead.",
-		)
-		return SystemPowerStatus
-	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")
+import winBindings.advapi32
+import winBindings.kernel32
+from utils import _deprecate
+
+
+__getattr__ = _deprecate.handleDeprecations(
+	_deprecate.MovedSymbol(
+		"SYSTEM_POWER_STATUS",
+		"winAPI._powerTracking",
+		"SystemPowerStatus",
+	),
+	_deprecate.MovedSymbol(
+		"STARTUPINFO",
+		"winBindings.advapi32",
+	),
+	_deprecate.MovedSymbol(
+		"STARTUPINFOW",
+		"winBindings.advapi32",
+	),
+	_deprecate.MovedSymbol(
+		"PROCESS_INFORMATION",
+		"winBindings.advapi32",
+	),
+	_deprecate.MovedSymbol("advapi32", "winBindings.advapi32", "dll"),
+)
 
 
 kernel32 = ctypes.windll.kernel32
-advapi32 = windll.advapi32
 
 # Constants
 INFINITE = 0xFFFFFFFF
@@ -182,12 +191,16 @@ def setWaitableTimer(handle, dueTime, period=0, completionRoutine=None, arg=None
 	return True
 
 
-def openProcess(*args):
-	return kernel32.OpenProcess(*args)
+def openProcess(*args) -> int:
+	try:
+		return winBindings.kernel32.OpenProcess(*args) or 0
+	except Exception:
+		# Compatibility: error should just be a handle of 0.
+		return 0
 
 
 def closeHandle(*args):
-	return kernel32.CloseHandle(*args)
+	return winBindings.kernel32.CloseHandle(*args)
 
 
 def GetSystemPowerStatus(sps: "SystemPowerStatus") -> int:
@@ -327,26 +340,26 @@ def GetTimeFormatEx(Locale, dwFlags, date, lpFormat):
 
 
 def virtualAllocEx(*args):
-	res = kernel32.VirtualAllocEx(*args)
+	res = winBindings.kernel32.VirtualAllocEx(*args)
 	if res == 0:
 		raise WinError()
 	return res
 
 
 def virtualFreeEx(*args):
-	return kernel32.VirtualFreeEx(*args)
+	return winBindings.kernel32.VirtualFreeEx(*args)
 
 
 def readProcessMemory(*args):
-	return kernel32.ReadProcessMemory(*args)
+	return winBindings.kernel32.ReadProcessMemory(*args)
 
 
 def writeProcessMemory(*args):
-	return kernel32.WriteProcessMemory(*args)
+	return winBindings.kernel32.WriteProcessMemory(*args)
 
 
 def waitForSingleObject(handle, timeout):
-	res = kernel32.WaitForSingleObject(handle, timeout)
+	res = winBindings.kernel32.WaitForSingleObject(handle, timeout)
 	if res == WAIT_FAILED:
 		raise ctypes.WinError()
 	return res
@@ -420,44 +433,6 @@ def CreatePipe(pipeAttributes, size):
 	return read.value, write.value
 
 
-class STARTUPINFOW(Structure):
-	_fields_ = (
-		("cb", DWORD),
-		("lpReserved", LPWSTR),
-		("lpDesktop", LPWSTR),
-		("lpTitle", LPWSTR),
-		("dwX", DWORD),
-		("dwY", DWORD),
-		("dwXSize", DWORD),
-		("dwYSize", DWORD),
-		("dwXCountChars", DWORD),
-		("dwYCountChars", DWORD),
-		("dwFillAttribute", DWORD),
-		("dwFlags", DWORD),
-		("wShowWindow", WORD),
-		("cbReserved2", WORD),
-		("lpReserved2", POINTER(c_byte)),
-		("hSTDInput", HANDLE),
-		("hSTDOutput", HANDLE),
-		("hSTDError", HANDLE),
-	)
-
-	def __init__(self, **kwargs):
-		super(STARTUPINFOW, self).__init__(cb=sizeof(self), **kwargs)
-
-
-STARTUPINFO = STARTUPINFOW
-
-
-class PROCESS_INFORMATION(Structure):
-	_fields_ = (
-		("hProcess", HANDLE),
-		("hThread", HANDLE),
-		("dwProcessID", DWORD),
-		("dwThreadID", DWORD),
-	)
-
-
 def CreateProcessAsUser(
 	token,
 	applicationName,
@@ -472,7 +447,7 @@ def CreateProcessAsUser(
 	processInformation,
 ):
 	if (
-		advapi32.CreateProcessAsUserW(
+		winBindings.advapi32.CreateProcessAsUser(
 			token,
 			applicationName,
 			commandLine,
@@ -496,7 +471,7 @@ def GetCurrentProcess():
 
 def OpenProcessToken(ProcessHandle, DesiredAccess):
 	token = HANDLE()
-	if advapi32.OpenProcessToken(ProcessHandle, DesiredAccess, byref(token)) == 0:
+	if winBindings.advapi32.OpenProcessToken(ProcessHandle, DesiredAccess, byref(token)) == 0:
 		raise WinError()
 	return token.value
 
@@ -514,7 +489,7 @@ def DuplicateHandle(
 ):
 	targetHandle = HANDLE()
 	if (
-		kernel32.DuplicateHandle(
+		winBindings.kernel32.DuplicateHandle(
 			sourceProcessHandle,
 			sourceHandle,
 			targetProcessHandle,
@@ -554,7 +529,7 @@ def __init__(self, h, autoFree=True):
 
 	def __del__(self):
 		if self and self._autoFree:
-			windll.kernel32.GlobalFree(self)
+			winBindings.kernel32.GlobalFree(self)
 
 	@classmethod
 	def alloc(cls, flags, size):
@@ -563,7 +538,7 @@ def alloc(cls, flags, size):
 		providing it as an instance of this class.
 		This method Takes the same arguments as GlobalAlloc.
 		"""
-		h = windll.kernel32.GlobalAlloc(flags, size)
+		h = winBindings.kernel32.GlobalAlloc(flags, size)
 		return cls(h)
 
 	@contextlib.contextmanager
@@ -575,9 +550,9 @@ def lock(self):
 		When the body completes, GlobalUnlock is automatically called.
 		"""
 		try:
-			yield windll.kernel32.GlobalLock(self)
+			yield winBindings.kernel32.GlobalLock(self)
 		finally:
-			windll.kernel32.GlobalUnlock(self)
+			winBindings.kernel32.GlobalUnlock(self)
 
 	def forget(self):
 		"""

```