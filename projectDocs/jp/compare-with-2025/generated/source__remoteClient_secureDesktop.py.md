# Diff for: `source\_remoteClient\secureDesktop.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\_remoteClient\secureDesktop.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\_remoteClient\secureDesktop.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\secureDesktop.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\secureDesktop.py"
index a52dc51..a7ae635 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\secureDesktop.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\secureDesktop.py"
@@ -30,12 +30,9 @@
 	POINTER,
 	FormatError,
 	GetLastError,
-	c_bool,
 	c_size_t,
 	sizeof,
 	windll,
-	c_wchar_p,
-	c_ushort,
 	create_unicode_buffer,
 	WINFUNCTYPE,
 	wstring_at,
@@ -47,6 +44,7 @@
 from logHandler import log
 from winAPI.secureDesktop import post_secureDesktopStateChange
 from NVDAHelper import localLib
+from winBindings import kernel32 as _kernel32
 from winKernel import closeHandle
 from winKernel import ERROR_ALREADY_EXISTS, SECURITY_ATTRIBUTES
 
@@ -482,7 +480,7 @@ def leaveSecureDesktop(self) -> None:
 		if self._mapFile is not None:
 			if not closeHandle(self._mapFile):
 				log.debugWarning(
-					f"Failed to close handle to memory mapped IPC file. {GetLastError()}: {FormatError()}"
+					"Failed to close handle to memory mapped IPC file. {GetLastError()}: {FormatError()}",
 				)
 			self._mapFile = None
 
@@ -491,12 +489,6 @@ def initializeSecureDesktop(self) -> Optional[ConnectionInfo]:
 
 		:return: Connection information if successful, None on failure
 		"""
-		getModuleFileName = windll.kernel32.GetModuleFileNameW
-		getModuleFileName.argtypes = (HANDLE, c_wchar_p, DWORD)
-		getModuleFileName.restype = DWORD
-		localListeningSocketExists = localLib.localListeningSocketExists
-		localListeningSocketExists.argtypes = (c_ushort, c_wchar_p)
-		localListeningSocketExists.restype = c_bool
 		log.info("Initializing secure desktop connection")
 		# Even though we only need read access,
 		# Memory mapped files must all be mapped with the same permissions.
@@ -531,8 +523,8 @@ def initializeSecureDesktop(self) -> Optional[ConnectionInfo]:
 
 			# Check that a socket is open on the right IP and port and with the same owning process image
 			processImageName = create_unicode_buffer(1024)
-			getModuleFileName(0, processImageName, 1024)
-			if not localListeningSocketExists(port, processImageName):
+			_kernel32.GetModuleFileName(0, processImageName, 1024)
+			if not localLib.localListeningSocketExists(port, processImageName):
 				raise RuntimeError("Matching socket not open.")
 
 			log.info(f"Successfully established secure desktop connection on port {port}")

```