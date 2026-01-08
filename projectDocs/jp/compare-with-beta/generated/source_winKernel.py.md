# Diff for: `source\winKernel.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winKernel.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winKernel.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winKernel.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winKernel.py"
index c634743..e31eacf 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winKernel.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winKernel.py"
@@ -29,7 +29,6 @@
 import winBindings.kernel32
 from winBindings.kernel32 import (
 	FILETIME as _FILETIME,
-	PTIMERAPCROUTINE as _PTIMERAPCROUTINE,
 	SYSTEMTIME as _SYSTEMTIME,
 	TIME_ZONE_INFORMATION as _TIME_ZONE_INFORMATION,
 )
@@ -177,34 +176,30 @@ def createWaitableTimer(securityAttributes=None, manualReset=False, name=None):
 	return res
 
 
-def setWaitableTimer(
-	handle: int,
-	dueTime: int,
-	period: int = 0,
-	completionRoutine: _PTIMERAPCROUTINE | None = None,
-	arg: int | None = None,
-	resume: bool = False,
-):
+def setWaitableTimer(handle, dueTime, period=0, completionRoutine=None, arg=None, resume=False):
 	"""Wrapper to the kernel32 SETWaitableTimer function.
-
-	Consult https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-setwaitabletimer for Microsoft's documentation.
-
-	:param handle: A handle to the timer object.
-	:param dueTime: Relative time (in milliseconds).
+	Consult https://msdn.microsoft.com/en-us/library/windows/desktop/ms686289.aspx for Microsoft's documentation.
+	@param handle: A handle to the timer object.
+	@type handle: int
+	@param dueTime: Relative time (in miliseconds).
 		Note that the original function requires relative time to be supplied as a negative nanoseconds value.
-	:param period: Defaults to 0, timer is only executed once.
-		Value should be supplied in milliseconds.
-	:param completionRoutine: An optional function to be executed when the timer elapses.
-	:param arg: A pointer to a structure that is passed to the completion routine, defaults to ``None``. .
-	:param resume: Whether to restore a system in suspended power conservation mode when the timer state is set to signaled, defaults to ``False``.
-		If the system does not support a restore, the call succeeds, but ``GetLastError`` returns ``ERROR_NOT_SUPPORTED``.
+	@type dueTime: int
+	@param period: Defaults to 0, timer is only executed once.
+		Value should be supplied in miliseconds.
+	@type period: int
+	@param completionRoutine: The function to be executed when the timer elapses.
+	@type completionRoutine: L{PAPCFUNC}
+	@param arg: Defaults to C{None}; a pointer to a structure that is passed to the completion routine.
+	@type arg: L{ctypes.c_void_p}
+	@param resume: Defaults to C{False}; the system is not restored.
+		If this parameter is TRUE, restores a system in suspended power conservation mode
+		when the timer state is set to signaled.
+	@type resume: bool
 	"""
-	if completionRoutine is None:
-		completionRoutine = _PTIMERAPCROUTINE(0)
 	res = winBindings.kernel32.SetWaitableTimer(
 		handle,
 		# due time is in 100 nanosecond intervals, relative time should be negated.
-		LARGE_INTEGER(dueTime * -10000),
+		byref(LARGE_INTEGER(dueTime * -10000)),
 		period,
 		completionRoutine,
 		arg,
@@ -236,7 +231,6 @@ def getThreadLocale():
 
 
 ERROR_INVALID_FUNCTION = 0x1
-ERROR_ACCESS_DENIED = 0x5
 ERROR_INVALID_HANDLE = 0x6
 
 
@@ -323,8 +317,6 @@ def GetDateFormatEx(Locale, dwFlags, date, lpFormat):
 
 
 def GetTimeFormatEx(Locale, dwFlags, date, lpFormat):
-	if dwFlags is None:
-		dwFlags = 0
 	if date is not None:
 		date = _SYSTEMTIME(date.year, date.month, 0, date.day, date.hour, date.minute, date.second, 0)
 		lpTime = byref(date)

```