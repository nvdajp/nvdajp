# Diff for: `source\UIAHandler\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\UIAHandler\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\UIAHandler\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\UIAHandler\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\UIAHandler\\__init__.py"
index 3cd2567..b11e5f0 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\UIAHandler\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\UIAHandler\\__init__.py"
@@ -3,12 +3,9 @@
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
-from typing import Optional
 import ctypes
 import ctypes.wintypes
 from ctypes import (
-	oledll,
-	windll,
 	POINTER,
 	CFUNCTYPE,  # noqa: F401
 	c_voidp,  # noqa: F401
@@ -37,11 +34,15 @@
 import appModuleHandler
 import controlTypes
 import globalVars
+from winBindings import user32
+import winBindings.ole32
+import winBindings.kernel32
 import winKernel
 import winUser
 import winVersion
 import eventHandler
 from logHandler import log
+import winBindings.uiAutomationCore
 from . import utils
 from comInterfaces import UIAutomationClient as UIA
 
@@ -250,8 +251,6 @@
 
 localEventHandlerGroupUIAEventIds = set()
 
-autoSelectDetectionAvailable = False
-if winVersion.getWinVer() >= winVersion.WIN10:
 UIAEventIdsToNVDAEventNames.update(
 	{
 		UIA.UIA_Text_TextSelectionChangedEventId: "caret",
@@ -262,7 +261,6 @@
 		UIA.UIA_Text_TextSelectionChangedEventId,
 	},
 )
-	autoSelectDetectionAvailable = True
 
 globalEventHandlerGroupUIAEventIds = set(UIAEventIdsToNVDAEventNames) - localEventHandlerGroupUIAEventIds
 
@@ -457,7 +455,7 @@ def terminate(self):
 
 		# Terminate the MTA thread
 		MTAThreadHandle = ctypes.wintypes.HANDLE(
-			windll.kernel32.OpenThread(
+			winBindings.kernel32.OpenThread(
 				winKernel.SYNCHRONIZE,
 				False,
 				self.MTAThread.ident,
@@ -465,14 +463,14 @@ def terminate(self):
 		)
 		self.MTAThreadQueue.put_nowait(None)
 		# Wait for the MTA thread to die (while still message pumping)
-		if windll.user32.MsgWaitForMultipleObjects(1, byref(MTAThreadHandle), False, 200, 0) != 0:
+		if user32.MsgWaitForMultipleObjects(1, byref(MTAThreadHandle), False, 200, 0) != 0:
 			log.debugWarning("Timeout or error while waiting for UIAHandler MTA thread")
-		windll.kernel32.CloseHandle(MTAThreadHandle)
+		winBindings.kernel32.CloseHandle(MTAThreadHandle)
 		del self.MTAThread
 
 	def MTAThreadFunc(self):
 		try:
-			oledll.ole32.CoInitializeEx(None, comtypes.COINIT_MULTITHREADED)
+			winBindings.ole32.CoInitializeEx(None, comtypes.COINIT_MULTITHREADED)
 			self.clientObject = CoCreateInstance(
 				UIA.CUIAutomation8._reg_clsid_,
 				# Minimum interface is IUIAutomation3 (Windows 8.1).
@@ -536,7 +534,7 @@ def MTAThreadFunc(self):
 			if config.conf["UIA"]["enhancedEventProcessing"]:
 				handler = self._rateLimitedEventHandler = POINTER(IUnknown)()
 				NVDAHelper.localLib.rateLimitedUIAEventHandler_create(
-					self._com_pointers_[IUnknown._iid_],
+					self.QueryInterface(IUnknown),
 					byref(self._rateLimitedEventHandler),
 				)
 			else:
@@ -594,7 +592,7 @@ def _registerGlobalEventHandlers(self, handler: "UIAHandler"):
 				self.baseCacheRequest,
 				handler,
 			)
-		if not utils._shouldSelectivelyRegister() and winVersion.getWinVer() >= winVersion.WIN10:
+		if not utils._shouldSelectivelyRegister():
 			# #14067: Due to poor performance, textChange requires special handling
 			self.globalEventHandlerGroup.AddAutomationEventHandler(
 				UIA.UIA_Text_TextChangedEventId,
@@ -1220,7 +1218,7 @@ def _isUIAWindowHelper(self, hwnd: int, isDebug=False) -> bool:  # noqa: C901
 						return False
 					parentHwnd = winUser.getAncestor(parentHwnd, winUser.GA_PARENT)
 		# Ask the window if it supports UIA natively
-		res = windll.UIAutomationCore.UiaHasServerSideProvider(hwnd)
+		res = winBindings.uiAutomationCore.UiaHasServerSideProvider(hwnd)
 		if res:
 			if isDebug:
 				log.debug("window has UIA server side provider")
@@ -1512,7 +1510,7 @@ def isNativeUIAElement(self, UIAElement):
 		return False
 
 
-handler: Optional[UIAHandler] = None
+handler: UIAHandler | None = None
 
 
 def initialize():

```