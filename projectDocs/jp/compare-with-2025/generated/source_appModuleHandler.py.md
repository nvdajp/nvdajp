# Diff for: `source\appModuleHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\appModuleHandler.py`  
**Current**: `F:\nvda\gh\alphajp\source\appModuleHandler.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModuleHandler.py" "b/F:\\nvda\\gh\\alphajp\\source\\appModuleHandler.py"
index 935f3e9d56..077d68d9ad 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModuleHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\appModuleHandler.py"
@@ -43,7 +43,13 @@
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
 
 
 # Dictionary of processID:appModule pairs used to hold the currently running modules
@@ -200,15 +206,63 @@ def getAppNameFromProcessID(processID: int, includeExt: bool = False) -> str:
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
@@ -481,11 +535,7 @@ def __init__(self, processID, appName=None):
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
 
@@ -601,9 +651,9 @@ def terminate(self):
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

```