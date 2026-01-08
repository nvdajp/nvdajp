# Diff for: `source\winKernel.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\winKernel.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winKernel.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winKernel.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winKernel.py"
index 96d574d..c634743 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winKernel.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winKernel.py"
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
+from ctypes.wintypes import BOOL, DWORD, HANDLE, LARGE_INTEGER, LCID, LPVOID
 from typing import (
 	TYPE_CHECKING,
-	Any,
 	Optional,
 	Union,
 )
@@ -26,24 +25,54 @@
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
+import winBindings.advapi32
+import winBindings.kernel32
+from winBindings.kernel32 import (
+	FILETIME as _FILETIME,
+	PTIMERAPCROUTINE as _PTIMERAPCROUTINE,
+	SYSTEMTIME as _SYSTEMTIME,
+	TIME_ZONE_INFORMATION as _TIME_ZONE_INFORMATION,
+)
+from utils import _deprecate
+
+
+__getattr__ = _deprecate.handleDeprecations(
+	_deprecate.MovedSymbol("kernel32", "winBindings.kernel32", "dll"),
+	_deprecate.MovedSymbol(
+		"SYSTEM_POWER_STATUS",
+		"winBindings.kernel32",
+	),
+	_deprecate.MovedSymbol(
+		"FILETIME",
+		"winBindings.kernel32",
+	),
+	_deprecate.MovedSymbol(
+		"SYSTEMTIME",
+		"winBindings.kernel32",
+	),
+	_deprecate.MovedSymbol(
+		"TIME_ZONE_INFORMATION",
+		"winBindings.kernel32",
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
+	_deprecate.MovedSymbol(
+		"PAPCFUNC ",
+		"winBindings.kernel32",
+	),
+	_deprecate.MovedSymbol("advapi32", "winBindings.advapi32", "dll"),
 )
-		return SystemPowerStatus
-	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")
-
 
-kernel32 = ctypes.windll.kernel32
-advapi32 = windll.advapi32
 
 # Constants
 INFINITE = 0xFFFFFFFF
@@ -84,7 +113,7 @@ def __getattr__(attrName: str) -> Any:
 
 
 def GetStdHandle(handleID):
-	h = kernel32.GetStdHandle(handleID)
+	h = winBindings.kernel32.GetStdHandle(handleID)
 	if h == 0:
 		raise WinError()
 	return h
@@ -107,7 +136,7 @@ def CreateFile(
 	flags,
 	templateFile,
 ):
-	res = kernel32.CreateFileW(
+	res = winBindings.kernel32.CreateFile(
 		fileName,
 		desiredAccess,
 		shareMode,
@@ -122,7 +151,7 @@ def CreateFile(
 
 
 def createEvent(eventAttributes=None, manualReset=False, initialState=False, name=None):
-	res = kernel32.CreateEventW(eventAttributes, manualReset, initialState, name)
+	res = winBindings.kernel32.CreateEvent(eventAttributes, manualReset, initialState, name)
 	if res == 0:
 		raise ctypes.WinError()
 	return res
@@ -142,36 +171,40 @@ def createWaitableTimer(securityAttributes=None, manualReset=False, name=None):
 	@param name: Defaults to C{None}, the timer object is created without a name.
 	@type name: str
 	"""
-	res = kernel32.CreateWaitableTimerW(securityAttributes, manualReset, name)
+	res = winBindings.kernel32.CreateWaitableTimer(securityAttributes, manualReset, name)
 	if res == 0:
 		raise ctypes.WinError()
 	return res
 
 
-def setWaitableTimer(handle, dueTime, period=0, completionRoutine=None, arg=None, resume=False):
+def setWaitableTimer(
+	handle: int,
+	dueTime: int,
+	period: int = 0,
+	completionRoutine: _PTIMERAPCROUTINE | None = None,
+	arg: int | None = None,
+	resume: bool = False,
+):
 	"""Wrapper to the kernel32 SETWaitableTimer function.
-	Consult https://msdn.microsoft.com/en-us/library/windows/desktop/ms686289.aspx for Microsoft's documentation.
-	@param handle: A handle to the timer object.
-	@type handle: int
-	@param dueTime: Relative time (in miliseconds).
+
+	Consult https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-setwaitabletimer for Microsoft's documentation.
+
+	:param handle: A handle to the timer object.
+	:param dueTime: Relative time (in milliseconds).
 		Note that the original function requires relative time to be supplied as a negative nanoseconds value.
-	@type dueTime: int
-	@param period: Defaults to 0, timer is only executed once.
-		Value should be supplied in miliseconds.
-	@type period: int
-	@param completionRoutine: The function to be executed when the timer elapses.
-	@type completionRoutine: L{PAPCFUNC}
-	@param arg: Defaults to C{None}; a pointer to a structure that is passed to the completion routine.
-	@type arg: L{ctypes.c_void_p}
-	@param resume: Defaults to C{False}; the system is not restored.
-		If this parameter is TRUE, restores a system in suspended power conservation mode
-		when the timer state is set to signaled.
-	@type resume: bool
+	:param period: Defaults to 0, timer is only executed once.
+		Value should be supplied in milliseconds.
+	:param completionRoutine: An optional function to be executed when the timer elapses.
+	:param arg: A pointer to a structure that is passed to the completion routine, defaults to ``None``. .
+	:param resume: Whether to restore a system in suspended power conservation mode when the timer state is set to signaled, defaults to ``False``.
+		If the system does not support a restore, the call succeeds, but ``GetLastError`` returns ``ERROR_NOT_SUPPORTED``.
 	"""
-	res = kernel32.SetWaitableTimer(
+	if completionRoutine is None:
+		completionRoutine = _PTIMERAPCROUTINE(0)
+	res = winBindings.kernel32.SetWaitableTimer(
 		handle,
 		# due time is in 100 nanosecond intervals, relative time should be negated.
-		byref(LARGE_INTEGER(dueTime * -10000)),
+		LARGE_INTEGER(dueTime * -10000),
 		period,
 		completionRoutine,
 		arg,
@@ -182,23 +215,28 @@ def setWaitableTimer(handle, dueTime, period=0, completionRoutine=None, arg=None
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
-	return kernel32.GetSystemPowerStatus(ctypes.byref(sps))
+	return winBindings.kernel32.GetSystemPowerStatus(ctypes.byref(sps))
 
 
 def getThreadLocale():
-	return kernel32.GetThreadLocale()
+	return winBindings.kernel32.GetThreadLocale()
 
 
 ERROR_INVALID_FUNCTION = 0x1
+ERROR_ACCESS_DENIED = 0x5
 ERROR_INVALID_HANDLE = 0x6
 
 
@@ -206,14 +244,14 @@ def getThreadLocale():
 def suspendWow64Redirection():
 	"""Context manager which disables Wow64 redirection for a section of code and re-enables it afterwards"""
 	oldValue = LPVOID()
-	res = kernel32.Wow64DisableWow64FsRedirection(byref(oldValue))
+	res = winBindings.kernel32.Wow64DisableWow64FsRedirection(byref(oldValue))
 	if res == 0:
 		# Disabling redirection failed.
 		# This can occur if we're running on 32-bit Windows (no Wow64 redirection)
 		# or as a 64-bit process on 64-bit Windows (Wow64 redirection not applicable)
 		# In this case failure is expected and there is no reason to raise an exception.
 		# Inspect last error code to determine reason for the failure.
-		errorCode = kernel32.GetLastError()
+		errorCode = winBindings.kernel32.GetLastError()
 		if errorCode == ERROR_INVALID_FUNCTION:  # Redirection not supported or not applicable.
 			redirectionDisabled = False
 		else:
@@ -224,63 +262,31 @@ def suspendWow64Redirection():
 		yield
 	finally:
 		if redirectionDisabled:
-			if kernel32.Wow64RevertWow64FsRedirection(oldValue) == 0:
+			if winBindings.kernel32.Wow64RevertWow64FsRedirection(oldValue) == 0:
 				raise WinError()
 
 
-class SYSTEMTIME(ctypes.Structure):
-	_fields_ = (
-		("wYear", WORD),
-		("wMonth", WORD),
-		("wDayOfWeek", WORD),
-		("wDay", WORD),
-		("wHour", WORD),
-		("wMinute", WORD),
-		("wSecond", WORD),
-		("wMilliseconds", WORD),
-	)
-
-
-class FILETIME(Structure):
-	_fields_ = (
-		("dwLowDateTime", DWORD),
-		("dwHighDateTime", DWORD),
-	)
-
-
-class TIME_ZONE_INFORMATION(Structure):
-	_fields_ = (
-		("Bias", ctypes.wintypes.LONG),
-		("StandardName", ctypes.wintypes.WCHAR * 32),
-		("StandardDate", SYSTEMTIME),
-		("StandardBias", ctypes.wintypes.LONG),
-		("DaylightName", ctypes.wintypes.WCHAR * 32),
-		("DaylightDate", SYSTEMTIME),
-		("DaylightBias", ctypes.wintypes.LONG),
-	)
-
-
-def time_tToFileTime(time_tToConvert: float) -> FILETIME:
+def time_tToFileTime(time_tToConvert: float) -> _FILETIME:
 	"""Converts time_t as returned from `time.time` to a FILETIME structure.
 	Based on a code snipped from:
 	https://docs.microsoft.com/en-us/windows/win32/sysinfo/converting-a-time-t-value-to-a-file-time
 	"""
-	timeAsFileTime = FILETIME()
+	timeAsFileTime = _FILETIME()
 	res = (int(time_tToConvert) * 10000000) + 116444736000000000
 	timeAsFileTime.dwLowDateTime = res
 	timeAsFileTime.dwHighDateTime = res >> 32
 	return timeAsFileTime
 
 
-def FileTimeToSystemTime(lpFileTime: FILETIME, lpSystemTime: SYSTEMTIME) -> None:
-	if kernel32.FileTimeToSystemTime(byref(lpFileTime), byref(lpSystemTime)) == 0:
+def FileTimeToSystemTime(lpFileTime: _FILETIME, lpSystemTime: _SYSTEMTIME) -> None:
+	if winBindings.kernel32.FileTimeToSystemTime(byref(lpFileTime), byref(lpSystemTime)) == 0:
 		raise WinError()
 
 
 def SystemTimeToTzSpecificLocalTime(
-	lpTimeZoneInformation: Union[TIME_ZONE_INFORMATION, None],
-	lpUniversalTime: SYSTEMTIME,
-	lpLocalTime: SYSTEMTIME,
+	timeZoneInformation: Union[_TIME_ZONE_INFORMATION, None],
+	lpUniversalTime: _SYSTEMTIME,
+	lpLocalTime: _SYSTEMTIME,
 ) -> None:
 	"""Wrapper for `SystemTimeToTzSpecificLocalTime` from kernel32.
 	:param lpTimeZoneInformation: Either TIME_ZONE_INFORMATION containing info about the desired time zone
@@ -289,10 +295,12 @@ def SystemTimeToTzSpecificLocalTime(
 	: param lpLocalTime: A SYSTEMTIME structure in which time converted to the desired time zone would be placed.
 	:raises WinError
 	"""
-	if lpTimeZoneInformation is not None:
-		lpTimeZoneInformation = byref(lpTimeZoneInformation)
+	if timeZoneInformation is not None:
+		lpTimeZoneInformation = byref(timeZoneInformation)
+	else:
+		lpTimeZoneInformation = None
 	if (
-		kernel32.SystemTimeToTzSpecificLocalTime(
+		winBindings.kernel32.SystemTimeToTzSpecificLocalTime(
 			lpTimeZoneInformation,
 			byref(lpUniversalTime),
 			byref(lpLocalTime),
@@ -304,56 +312,58 @@ def SystemTimeToTzSpecificLocalTime(
 
 def GetDateFormatEx(Locale, dwFlags, date, lpFormat):
 	if date is not None:
-		date = SYSTEMTIME(date.year, date.month, 0, date.day, date.hour, date.minute, date.second, 0)
+		date = _SYSTEMTIME(date.year, date.month, 0, date.day, date.hour, date.minute, date.second, 0)
 		lpDate = byref(date)
 	else:
 		lpDate = None
-	bufferLength = kernel32.GetDateFormatEx(Locale, dwFlags, lpDate, lpFormat, None, 0, None)
+	bufferLength = winBindings.kernel32.GetDateFormatEx(Locale, dwFlags, lpDate, lpFormat, None, 0, None)
 	buf = ctypes.create_unicode_buffer("", bufferLength)
-	kernel32.GetDateFormatEx(Locale, dwFlags, lpDate, lpFormat, buf, bufferLength, None)
+	winBindings.kernel32.GetDateFormatEx(Locale, dwFlags, lpDate, lpFormat, buf, bufferLength, None)
 	return buf.value
 
 
 def GetTimeFormatEx(Locale, dwFlags, date, lpFormat):
+	if dwFlags is None:
+		dwFlags = 0
 	if date is not None:
-		date = SYSTEMTIME(date.year, date.month, 0, date.day, date.hour, date.minute, date.second, 0)
+		date = _SYSTEMTIME(date.year, date.month, 0, date.day, date.hour, date.minute, date.second, 0)
 		lpTime = byref(date)
 	else:
 		lpTime = None
-	bufferLength = kernel32.GetTimeFormatEx(Locale, dwFlags, lpTime, lpFormat, None, 0)
+	bufferLength = winBindings.kernel32.GetTimeFormatEx(Locale, dwFlags, lpTime, lpFormat, None, 0)
 	buf = ctypes.create_unicode_buffer("", bufferLength)
-	kernel32.GetTimeFormatEx(Locale, dwFlags, lpTime, lpFormat, buf, bufferLength)
+	winBindings.kernel32.GetTimeFormatEx(Locale, dwFlags, lpTime, lpFormat, buf, bufferLength)
 	return buf.value
 
 
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
 
 
 def waitForSingleObjectEx(handle, timeout, alertable):
-	res = kernel32.WaitForSingleObjectEx(handle, timeout, alertable)
+	res = winBindings.kernel32.WaitForSingleObjectEx(handle, timeout, alertable)
 	if res == WAIT_FAILED:
 		raise ctypes.WinError()
 	return res
@@ -363,20 +373,20 @@ def waitForSingleObjectEx(handle, timeout, alertable):
 
 
 def SetProcessShutdownParameters(level, flags):
-	res = kernel32.SetProcessShutdownParameters(level, flags)
+	res = winBindings.kernel32.SetProcessShutdownParameters(level, flags)
 	if res == 0:
 		raise ctypes.WinError()
 
 
 def GetExitCodeProcess(process):
 	exitCode = ctypes.wintypes.DWORD()
-	if not kernel32.GetExitCodeProcess(process, ctypes.byref(exitCode)):
+	if not winBindings.kernel32.GetExitCodeProcess(process, ctypes.byref(exitCode)):
 		raise ctypes.WinError()
 	return exitCode.value
 
 
 def TerminateProcess(process, exitCode):
-	if not kernel32.TerminateProcess(process, exitCode):
+	if not winBindings.kernel32.TerminateProcess(process, exitCode):
 		raise ctypes.WinError()
 
 
@@ -390,7 +400,7 @@ def TerminateProcess(process, exitCode):
 
 
 def GetDriveType(rootPathName):
-	return kernel32.GetDriveTypeW(rootPathName)
+	return winBindings.kernel32.GetDriveType(rootPathName)
 
 
 class SECURITY_ATTRIBUTES(Structure):
@@ -408,7 +418,7 @@ def CreatePipe(pipeAttributes, size):
 	read = ctypes.wintypes.HANDLE()
 	write = ctypes.wintypes.HANDLE()
 	if (
-		kernel32.CreatePipe(
+		winBindings.kernel32.CreatePipe(
 			ctypes.byref(read),
 			ctypes.byref(write),
 			byref(pipeAttributes) if pipeAttributes else None,
@@ -420,44 +430,6 @@ def CreatePipe(pipeAttributes, size):
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
@@ -472,7 +444,7 @@ def CreateProcessAsUser(
 	processInformation,
 ):
 	if (
-		advapi32.CreateProcessAsUserW(
+		winBindings.advapi32.CreateProcessAsUser(
 			token,
 			applicationName,
 			commandLine,
@@ -491,12 +463,12 @@ def CreateProcessAsUser(
 
 
 def GetCurrentProcess():
-	return kernel32.GetCurrentProcess()
+	return winBindings.kernel32.GetCurrentProcess()
 
 
 def OpenProcessToken(ProcessHandle, DesiredAccess):
 	token = HANDLE()
-	if advapi32.OpenProcessToken(ProcessHandle, DesiredAccess, byref(token)) == 0:
+	if winBindings.advapi32.OpenProcessToken(ProcessHandle, DesiredAccess, byref(token)) == 0:
 		raise WinError()
 	return token.value
 
@@ -514,7 +486,7 @@ def DuplicateHandle(
 ):
 	targetHandle = HANDLE()
 	if (
-		kernel32.DuplicateHandle(
+		winBindings.kernel32.DuplicateHandle(
 			sourceProcessHandle,
 			sourceHandle,
 			targetProcessHandle,
@@ -529,7 +501,6 @@ def DuplicateHandle(
 	return targetHandle.value
 
 
-PAPCFUNC = ctypes.WINFUNCTYPE(None, ctypes.wintypes.ULONG)
 THREAD_SET_CONTEXT = 16
 
 GMEM_MOVEABLE = 2
@@ -554,7 +525,7 @@ def __init__(self, h, autoFree=True):
 
 	def __del__(self):
 		if self and self._autoFree:
-			windll.kernel32.GlobalFree(self)
+			winBindings.kernel32.GlobalFree(self)
 
 	@classmethod
 	def alloc(cls, flags, size):
@@ -563,7 +534,7 @@ def alloc(cls, flags, size):
 		providing it as an instance of this class.
 		This method Takes the same arguments as GlobalAlloc.
 		"""
-		h = windll.kernel32.GlobalAlloc(flags, size)
+		h = winBindings.kernel32.GlobalAlloc(flags, size)
 		return cls(h)
 
 	@contextlib.contextmanager
@@ -575,9 +546,9 @@ def lock(self):
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
@@ -597,7 +568,7 @@ def forget(self):
 
 def moveFileEx(lpExistingFileName: str, lpNewFileName: str, dwFlags: int):
 	# If MoveFileExW fails, Windows will raise appropriate errors.
-	if not kernel32.MoveFileExW(lpExistingFileName, lpNewFileName, dwFlags):
+	if not winBindings.kernel32.MoveFileEx(lpExistingFileName, lpNewFileName, dwFlags):
 		raise ctypes.WinError()
 
 
@@ -606,11 +577,9 @@ def moveFileEx(lpExistingFileName: str, lpNewFileName: str, dwFlags: int):
 ES_DISPLAY_REQUIRED = 0x2
 ES_SYSTEM_REQUIRED = 0x1
 
-kernel32.SetThreadExecutionState.restype = ctypes.wintypes.DWORD
-
 
 def SetThreadExecutionState(esFlags):
-	res = kernel32.SetThreadExecutionState(esFlags)
+	res = winBindings.kernel32.SetThreadExecutionState(esFlags)
 	if not res:
 		raise WinError()
 	return res
@@ -621,14 +590,14 @@ def LCIDToLocaleName(windowsLCID: LCID) -> Optional[str]:
 	from logHandler import log
 
 	dwFlags = 0
-	bufferLength = kernel32.LCIDToLocaleName(windowsLCID, None, 0, dwFlags)
+	bufferLength = winBindings.kernel32.LCIDToLocaleName(windowsLCID, None, 0, dwFlags)
 	if bufferLength == 0:
 		# This means that there was an error fetching the LCID.
 		# As the buffer is empty, this indicates that the windowsLCID is invalid.
 		log.debugWarning(f"Invalid LCID {windowsLCID}")
 		return None
 	buffer = ctypes.create_unicode_buffer("", bufferLength)
-	bufferLength = kernel32.LCIDToLocaleName(windowsLCID, buffer, bufferLength, dwFlags)
+	bufferLength = winBindings.kernel32.LCIDToLocaleName(windowsLCID, buffer, bufferLength, dwFlags)
 	if bufferLength == 0:
 		# This means that there was an error fetching the LCID.
 		# As we have already checked if the LCID is valid by receiveing a non-zero buffer length,

```