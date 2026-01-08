# Diff for: `source\appModuleHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\appModuleHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\appModuleHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModuleHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModuleHandler.py"
index 935f3e9..85b52b5 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModuleHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModuleHandler.py"
@@ -16,13 +16,13 @@
 import sys
 from types import ModuleType
 from typing import (
-	Any,
 	Dict,
 	List,
 	Optional,
 	Tuple,
 )
 
+import winBindings.kernel32
 import winVersion
 import importlib
 import importlib.util
@@ -32,7 +32,6 @@
 import baseObject
 from logHandler import log
 import NVDAHelper
-import NVDAState
 import winKernel
 import config
 import NVDAObjects  # Catches errors before loading default appModule
@@ -43,7 +42,31 @@
 from fileUtils import getFileVersionInfo
 import globalVars
 from systemUtils import getCurrentProcessLogonSessionId, getProcessLogonSessionId
+from oleacc import GetProcessHandleFromHwnd as _getProcessHandleFromHwnd
+from winUser import (
+	findTopLevelWindow as _findTopLevelWindow,
+	getWindowThreadProcessID as _getWindowThreadProcessID,
+)
 from comInterfaces import UIAutomationClient as UIA
+import winBindings.rpcrt4
+from utils import _deprecate
+
+
+__getattr__ = _deprecate.handleDeprecations(
+	_deprecate.MovedSymbol(
+		"processEntry32W",
+		"winBindings.kernel32",
+	),
+	_deprecate.MovedSymbol(
+		"_PROCESS_MACHINE_INFORMATION",
+		"winBindings.kernel32",
+	),
+	_deprecate.MovedSymbol(
+		"NVDAProcessID",
+		"globalVars",
+		"appPid",
+	),
+)
 
 
 # Dictionary of processID:appModule pairs used to hold the currently running modules
@@ -63,47 +86,6 @@
 """
 
 
-class processEntry32W(ctypes.Structure):
-	"""See https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/ns-tlhelp32-processentry32w"""
-
-	_fields_ = [
-		("dwSize", ctypes.wintypes.DWORD),
-		("cntUsage", ctypes.wintypes.DWORD),
-		("th32ProcessID", ctypes.wintypes.DWORD),
-		("th32DefaultHeapID", ctypes.wintypes.PULONG),
-		("th32ModuleID", ctypes.wintypes.DWORD),
-		("cntThreads", ctypes.wintypes.DWORD),
-		("th32ParentProcessID", ctypes.wintypes.DWORD),
-		("pcPriClassBase", ctypes.c_long),
-		("dwFlags", ctypes.wintypes.DWORD),
-		("szExeFile", ctypes.c_wchar * 260),
-	]
-
-
-class _PROCESS_MACHINE_INFORMATION(ctypes.Structure):
-	_fields_ = [
-		("ProcessMachine", ctypes.wintypes.USHORT),
-		("Res0", ctypes.wintypes.USHORT),
-		("MachineAttributes", ctypes.wintypes.DWORD),
-	]
-
-
-def __getattr__(attrName: str) -> Any:
-	"""Module level `__getattr__` used to preserve backward compatibility.
-	The module level variable `NVDAProcessID` is deprecated
-	and usages should be replaced with `globalVars.appPid`.
-	We cannot simply assign the value from `globalVars` to the old attribute
-	since add-ons are initialized before `appModuleHandler`
-	and when `appModuleHandler` was not yet initialized the variable was set to `None`.
-	"""
-	if attrName == "NVDAProcessID" and NVDAState._allowDeprecatedAPI():
-		log.warning("appModuleHandler.NVDAProcessID is deprecated, use globalVars.appPid instead.")
-		if initialize._alreadyInitialized:
-			return globalVars.appPid
-		return None
-	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")
-
-
 def registerExecutableWithAppModule(executableName: str, appModName: str) -> None:
 	"""Registers appModule to be used for a given executable."""
 	_executableNamesToAppModsAddons[executableName] = appModName
@@ -175,17 +157,17 @@ def getAppNameFromProcessID(processID: int, includeExt: bool = False) -> str:
 	"""
 	if processID == globalVars.appPid:
 		return "nvda.exe" if includeExt else "nvda"
-	FSnapshotHandle = winKernel.kernel32.CreateToolhelp32Snapshot(2, 0)
-	FProcessEntry32 = processEntry32W()
-	FProcessEntry32.dwSize = ctypes.sizeof(processEntry32W)
-	ContinueLoop = winKernel.kernel32.Process32FirstW(FSnapshotHandle, ctypes.byref(FProcessEntry32))
+	FSnapshotHandle = winBindings.kernel32.CreateToolhelp32Snapshot(2, 0)
+	FProcessEntry32 = winBindings.kernel32.PROCESSENTRY32W()
+	FProcessEntry32.dwSize = ctypes.sizeof(FProcessEntry32)
+	ContinueLoop = winBindings.kernel32.Process32First(FSnapshotHandle, ctypes.byref(FProcessEntry32))
 	appName = str()
 	while ContinueLoop:
 		if FProcessEntry32.th32ProcessID == processID:
 			appName = FProcessEntry32.szExeFile
 			break
-		ContinueLoop = winKernel.kernel32.Process32NextW(FSnapshotHandle, ctypes.byref(FProcessEntry32))
-	winKernel.kernel32.CloseHandle(FSnapshotHandle)
+		ContinueLoop = winBindings.kernel32.Process32Next(FSnapshotHandle, ctypes.byref(FProcessEntry32))
+	winBindings.kernel32.CloseHandle(FSnapshotHandle)
 	if not includeExt:
 		appName = os.path.splitext(appName)[0].lower()
 	if not appName:
@@ -200,15 +182,63 @@ def getAppNameFromProcessID(processID: int, includeExt: bool = False) -> str:
 	return appName
 
 
+def getProcessHandleFromProcessId(processId: int, fallBackToTopLevelWindowEnumeration: bool = True) -> int:
+	"""
+	Get a process handle for the given process ID.
+
+	This function attempts to open a process handle using the Windows API. If the direct
+	approach fails and fallback is enabled, it will attempt to find a top-level window
+	belonging to the process and derive the process handle from that window.
+
+	:param processId: The ID of the process for which to obtain a handle
+	:param fallBackToTopLevelWindowEnumeration: Whether to attempt window enumeration
+		as a fallback method if direct process opening fails. Defaults to True
+	:return: A handle to the process, or 0 if no handle could be obtained
+	"""
+	processHandle: int = 0
+	try:
+		if not (
+			processHandle := winKernel.openProcess(
+				winKernel.SYNCHRONIZE | winKernel.PROCESS_QUERY_INFORMATION,
+				False,
+				processId,
+			)
+		):
+			raise ctypes.WinError()
+	except WindowsError:
+		log.debugWarning(f"Unable to open process for processId {processId}", exc_info=True)
+	else:
+		return processHandle
+
+	if fallBackToTopLevelWindowEnumeration:
+		try:
+			if not (
+				foundWindowHandle := _findTopLevelWindow(
+					lambda hwnd: _getWindowThreadProcessID(hwnd)[0] == processId,
+				)
+			):
+				raise RuntimeError(f"No window handle found for process {processId} to create process handle")
+			if not (processHandle := _getProcessHandleFromHwnd(foundWindowHandle)):
+				raise ctypes.WinError()
+		except (WindowsError, RuntimeError):
+			log.debugWarning(
+				f"Unable to get process handle for process {processId} using window enumeration "
+				"and subsequently getting process handle from that window",
+				exc_info=True,
+			)
+
+	return processHandle
+
+
 def getAppModuleForNVDAObject(obj: NVDAObjects.NVDAObject) -> AppModule:
 	if not isinstance(obj, NVDAObjects.NVDAObject):
 		return
 	mod = getAppModuleFromProcessID(obj.processID)
-	# #14403: some apps report process handle of 0, causing process information and other functions to fail.
+	# #14403: For some apps it is not possible to get a process handle,
+	# causing process information and other functions to fail.
 	if mod.processHandle == 0:
-		# Sometimes process handle for the NVDA object may not be defined, more so when running tests.
 		try:
-			mod.processHandle = obj.processHandle
+			mod.processHandle = _getProcessHandleFromHwnd(obj.windowHandle)
 		except AttributeError:
 			pass
 	return mod
@@ -481,11 +511,7 @@ def __init__(self, processID, appName=None):
 		if appName is None:
 			appName = getAppNameFromProcessID(processID)
 		self.appName = appName
-		self.processHandle = winKernel.openProcess(
-			winKernel.SYNCHRONIZE | winKernel.PROCESS_QUERY_INFORMATION,
-			False,
-			processID,
-		)
+		self.processHandle = getProcessHandleFromProcessId(processID)
 		self.helperLocalBindingHandle: Optional[ctypes.c_long] = None
 		"""RPC binding handle pointing to the RPC server for this process"""
 
@@ -498,7 +524,7 @@ def _get_processExecutablePath(self) -> str:
 		# Create the buffer to get the executable name
 		exeFileName = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
 		length = ctypes.wintypes.DWORD(ctypes.wintypes.MAX_PATH)
-		if not ctypes.windll.Kernel32.QueryFullProcessImageNameW(
+		if not winBindings.kernel32.QueryFullProcessImageName(
 			self.processHandle,
 			0,
 			exeFileName,
@@ -521,10 +547,10 @@ def _getImmersivePackageInfo(self):
 		# Some apps such as File Explorer says it is an immersive process but error 15700 is shown.
 		# Others such as Store version of Office are not truly hosted apps but are distributed via Store.
 		length = ctypes.c_uint()
-		ctypes.windll.kernel32.GetPackageFullName(self.processHandle, ctypes.byref(length), None)
+		winBindings.kernel32.GetPackageFullName(self.processHandle, ctypes.byref(length), None)
 		packageFullName = ctypes.create_unicode_buffer(length.value)
 		if (
-			ctypes.windll.kernel32.GetPackageFullName(
+			winBindings.kernel32.GetPackageFullName(
 				self.processHandle,
 				ctypes.byref(length),
 				packageFullName,
@@ -578,9 +604,17 @@ def __repr__(self):
 	def _get_appModuleName(self):
 		return self.__class__.__module__.split(".")[-1]
 
+	_liveForEver: bool = False
+	"""
+	Set to true when NVDA cannot get enough permissions to successfully verify if the process is dead.
+	E.g. Security software such as 1Password which blocks the SYNCHRONIZE access right.
+	"""
+
 	isAlive: bool
 
 	def _get_isAlive(self) -> bool:
+		if self._liveForEver:
+			return True
 		try:
 			return bool(winKernel.waitForSingleObject(self.processHandle, 0))
 		except OSError as e:
@@ -590,6 +624,16 @@ def _get_isAlive(self) -> bool:
 					f"Process handle {self.processHandle} for {self} is invalid, assuming process is dead.",
 				)
 				return False
+			elif e.winerror == winKernel.ERROR_ACCESS_DENIED:
+				# Although we opened the process asking for the SYNCHRONIZE access right,
+				# The process is refusing us the permission when waiting on the handle.
+				# This may be a protected process like 1Password.
+				# Currently there is no alternative way to check if the process is dead, so we must assume it stays alive for ever.
+				log.debugWarning(
+					f"Access denied waiting on Process handle {self.processHandle} for {self}, cannot verify dead, marking as living for ever.",
+				)
+				self._liveForEver = True
+				return True
 			raise
 
 	def terminate(self):
@@ -601,9 +645,9 @@ def terminate(self):
 		if getattr(self, "_helperPreventDisconnect", False):
 			return
 		if self._inprocRegistrationHandle:
-			ctypes.windll.rpcrt4.RpcSsDestroyClientContext(ctypes.byref(self._inprocRegistrationHandle))
+			winBindings.rpcrt4.RpcSsDestroyClientContext(ctypes.byref(self._inprocRegistrationHandle))
 		if self.helperLocalBindingHandle:
-			ctypes.windll.rpcrt4.RpcBindingFree(ctypes.byref(self.helperLocalBindingHandle))
+			winBindings.rpcrt4.RpcBindingFree(ctypes.byref(self.helperLocalBindingHandle))
 
 	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
 		"""Choose NVDAObject overlay classes for a given NVDAObject.
@@ -625,7 +669,7 @@ def _get_appPath(self):
 		"""
 		size = ctypes.wintypes.DWORD(ctypes.wintypes.MAX_PATH)
 		path = ctypes.create_unicode_buffer(size.value)
-		winKernel.kernel32.QueryFullProcessImageNameW(self.processHandle, 0, path, ctypes.byref(size))
+		winBindings.kernel32.QueryFullProcessImageName(self.processHandle, 0, path, ctypes.byref(size))
 		self.appPath = path.value if path else None
 		return self.appPath
 
@@ -641,7 +685,7 @@ def _get_is64BitProcess(self) -> bool:
 			# We need IsWow64Process2 to detect WOW64 on ARM64.
 			processMachine = ctypes.wintypes.USHORT()
 			if (
-				ctypes.windll.kernel32.IsWow64Process2(
+				winBindings.kernel32.IsWow64Process2(
 					self.processHandle,
 					ctypes.byref(processMachine),
 					None,
@@ -656,7 +700,7 @@ def _get_is64BitProcess(self) -> bool:
 			# IsWow64Process2 is only supported on Windows 10 version 1511 and later.
 			# Fall back to IsWow64Process.
 			res = ctypes.wintypes.BOOL()
-			if ctypes.windll.kernel32.IsWow64Process(self.processHandle, ctypes.byref(res)) == 0:
+			if winBindings.kernel32.IsWow64Process(self.processHandle, ctypes.byref(res)) == 0:
 				self.is64BitProcess = False
 				return False
 			self.is64BitProcess = not res
@@ -714,15 +758,15 @@ def _get_appArchitecture(self) -> str:
 		}
 		# #14403: GetProcessInformation can be called from Windows 11 and later to obtain process machine.
 		if winVersion.getWinVer() >= winVersion.WIN11:
-			processMachineInfo = _PROCESS_MACHINE_INFORMATION()
+			processMachineInfo = winBindings.kernel32._PROCESS_MACHINE_INFORMATION()
 			# Constant comes from PROCESS_INFORMATION_CLASS enumeration.
 			ProcessMachineTypeInfo = 9
 			# Sometimes getProcessInformation may fail, so say "unknown".
-			if not ctypes.windll.kernel32.GetProcessInformation(
+			if not winBindings.kernel32.GetProcessInformation(
 				self.processHandle,
 				ProcessMachineTypeInfo,
 				ctypes.byref(processMachineInfo),
-				ctypes.sizeof(_PROCESS_MACHINE_INFORMATION),
+				ctypes.sizeof(processMachineInfo),
 			):
 				self.appArchitecture = "unknown"
 			else:
@@ -734,7 +778,7 @@ def _get_appArchitecture(self) -> str:
 			try:
 				# If a native app is running (such as x64 app on x64 machines), app architecture value is not set.
 				processMachine = ctypes.wintypes.USHORT()
-				ctypes.windll.kernel32.IsWow64Process2(self.processHandle, ctypes.byref(processMachine), None)
+				winBindings.kernel32.IsWow64Process2(self.processHandle, ctypes.byref(processMachine), None)
 				if not processMachine.value:
 					self.appArchitecture = winVersion.getWinVer().processorArchitecture
 				else:

```