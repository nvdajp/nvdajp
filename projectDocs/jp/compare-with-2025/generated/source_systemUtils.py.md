# Diff for: `source\systemUtils.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\systemUtils.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\systemUtils.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\systemUtils.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\systemUtils.py"
index 6b7b5e2..cb8156d 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\systemUtils.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\systemUtils.py"
@@ -15,19 +15,17 @@
 	byref,
 	create_unicode_buffer,
 	sizeof,
-	windll,
 )
+import ctypes.wintypes
 from typing import (
 	Generic,
 	Optional,
-)
-from typing_extensions import (
-	# Uses `TypeVar` from `typing_extensions`, to be able to specify default type.
-	# This should be changed to use version from `typing`
-	# when updating to version of Python supporting PEP 696.
 	TypeVar,
 )
 
+import winBindings.advapi32
+import winBindings.kernel32
+import winBindings.shell32
 import winKernel
 import winreg
 import shellapi
@@ -36,6 +34,7 @@
 import shlobj
 from logHandler import log
 from NVDAState import WritePaths
+from winBindings import advapi32, user32
 
 
 @functools.lru_cache(maxsize=1)
@@ -69,14 +68,14 @@ def openDefaultConfigurationDirectory():
 
 def hasUiAccess():
 	token = ctypes.wintypes.HANDLE()
-	ctypes.windll.advapi32.OpenProcessToken(
-		ctypes.windll.kernel32.GetCurrentProcess(),
+	advapi32.OpenProcessToken(
+		winBindings.kernel32.GetCurrentProcess(),
 		winKernel.MAXIMUM_ALLOWED,
 		ctypes.byref(token),
 	)
 	try:
 		val = ctypes.wintypes.DWORD()
-		ctypes.windll.advapi32.GetTokenInformation(
+		winBindings.advapi32.GetTokenInformation(
 			token,
 			TokenUIAccess,
 			ctypes.byref(val),
@@ -85,7 +84,7 @@ def hasUiAccess():
 		)
 		return bool(val.value)
 	finally:
-		ctypes.windll.kernel32.CloseHandle(token)
+		winBindings.kernel32.CloseHandle(token)
 
 
 #: Value from the TOKEN_INFORMATION_CLASS enumeration:
@@ -120,7 +119,7 @@ def getProcessLogonSessionId(processHandle: int) -> int:
 	* CloseHandle: To close the token handle.
 	"""
 	token = ctypes.wintypes.HANDLE()
-	if not ctypes.windll.advapi32.OpenProcessToken(
+	if not advapi32.OpenProcessToken(
 		processHandle,
 		winKernel.MAXIMUM_ALLOWED,
 		ctypes.byref(token),
@@ -128,7 +127,7 @@ def getProcessLogonSessionId(processHandle: int) -> int:
 		raise ctypes.WinError()
 	try:
 		val = TokenOrigin()
-		if not ctypes.windll.advapi32.GetTokenInformation(
+		if not winBindings.advapi32.GetTokenInformation(
 			token,
 			TOKEN_ORIGIN,
 			ctypes.byref(val),
@@ -138,7 +137,7 @@ def getProcessLogonSessionId(processHandle: int) -> int:
 			raise ctypes.WinError()
 		return val.originatingLogonSession
 	finally:
-		ctypes.windll.kernel32.CloseHandle(token)
+		winBindings.kernel32.CloseHandle(token)
 
 
 @functools.lru_cache(maxsize=1)
@@ -153,7 +152,7 @@ def execElevated(path, params=None, wait=False, handleAlreadyElevated=False):
 		params = subprocess.list2cmdline(params)
 	sei = shellapi.SHELLEXECUTEINFO(lpFile=path, lpParameters=params, nShow=winUser.SW_HIDE)
 	# IsUserAnAdmin is apparently deprecated so may not work above Windows 8
-	if not handleAlreadyElevated or not ctypes.windll.shell32.IsUserAnAdmin():
+	if not handleAlreadyElevated or not winBindings.shell32.IsUserAnAdmin():
 		sei.lpVerb = "runas"
 	if wait:
 		sei.fMask = shellapi.SEE_MASK_NOCLOSEPROCESS
@@ -162,10 +161,10 @@ def execElevated(path, params=None, wait=False, handleAlreadyElevated=False):
 		try:
 			h = ctypes.wintypes.HANDLE(sei.hProcess)
 			msg = ctypes.wintypes.MSG()
-			while ctypes.windll.user32.MsgWaitForMultipleObjects(1, ctypes.byref(h), False, -1, 255) == 1:
-				while ctypes.windll.user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1):
-					ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
-					ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
+			while user32.MsgWaitForMultipleObjects(1, ctypes.byref(h), False, -1, 255) == 1:
+				while user32.PeekMessage(ctypes.byref(msg), None, 0, 0, 1):
+					user32.TranslateMessage(ctypes.byref(msg))
+					user32.DispatchMessage(ctypes.byref(msg))
 			return winKernel.GetExitCodeProcess(sei.hProcess)
 		finally:
 			winKernel.closeHandle(sei.hProcess)
@@ -174,9 +173,11 @@ def execElevated(path, params=None, wait=False, handleAlreadyElevated=False):
 @functools.lru_cache(maxsize=1)
 def _getDesktopName() -> str:
 	UOI_NAME = 2  # The name of the object, as a string
-	desktop = windll.user32.GetThreadDesktop(windll.kernel32.GetCurrentThreadId())
+	desktop = user32.GetThreadDesktop(
+		winBindings.kernel32.GetCurrentThreadId(),
+	)
 	name = create_unicode_buffer(256)
-	windll.user32.GetUserObjectInformationW(
+	user32.GetUserObjectInformation(
 		desktop,
 		UOI_NAME,
 		byref(name),
@@ -231,13 +232,17 @@ def __init__(self, func: Callable[..., _execAndPumpResT], *args, **kwargs) -> No
 		self.threadExc: Exception | None = None
 		self.start()
 		time.sleep(0.1)
-		threadHandle = ctypes.c_int()
-		threadHandle.value = winKernel.kernel32.OpenThread(0x100000, False, self.ident)
+		# BEGIN JP PATCH
+		threadHandle = ctypes.wintypes.HANDLE()
+		threadHandle.value = winBindings.kernel32.OpenThread(0x100000, False, self.ident)
+		if not threadHandle.value:
+			raise ctypes.WinError()
 		msg = ctypes.wintypes.MSG()
-		while winUser.user32.MsgWaitForMultipleObjects(1, ctypes.byref(threadHandle), False, -1, 255) == 1:
-			while winUser.user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1):
-				winUser.user32.TranslateMessage(ctypes.byref(msg))
-				winUser.user32.DispatchMessageW(ctypes.byref(msg))
+		while user32.MsgWaitForMultipleObjects(1, ctypes.byref(threadHandle), False, -1, 255) == 1:
+			while user32.PeekMessage(ctypes.byref(msg), None, 0, 0, 1):
+				user32.TranslateMessage(ctypes.byref(msg))
+				user32.DispatchMessage(ctypes.byref(msg))
+		# END JP PATCH
 		if self.threadExc:
 			raise self.threadExc
 
@@ -261,7 +266,7 @@ def preventSystemIdle(preventDisplayTurningOff: bool | None = None, persistent:
 		import config
 
 		preventDisplayTurningOff = config.conf["general"]["preventDisplayTurningOff"]
-	windll.kernel32.SetThreadExecutionState(
+	winBindings.kernel32.SetThreadExecutionState(
 		winKernel.ES_SYSTEM_REQUIRED
 		| (winKernel.ES_DISPLAY_REQUIRED if preventDisplayTurningOff else 0)
 		| (winKernel.ES_CONTINUOUS if persistent else 0),
@@ -270,4 +275,4 @@ def preventSystemIdle(preventDisplayTurningOff: bool | None = None, persistent:
 
 def resetThreadExecutionState() -> None:
 	"""Reset the thread execution state to the default."""
-	windll.kernel32.SetThreadExecutionState(winKernel.ES_CONTINUOUS)
+	winBindings.kernel32.SetThreadExecutionState(winKernel.ES_CONTINUOUS)

```