# Diff for: `source\hwIo\base.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\hwIo\base.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\hwIo\base.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\hwIo\\base.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\hwIo\\base.py"
index fb7eac1..0a34b27 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\hwIo\\base.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\hwIo\\base.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2015-2023 NV Access Limited, Babbage B.V., Leonard de Ruijter
+# Copyright (C) 2015-2025 NV Access Limited, Babbage B.V., Leonard de Ruijter
 
 
 """Raw input/output for braille displays via serial and HID.
@@ -28,6 +28,7 @@
 	CreateFile,
 	SetCommTimeouts,
 )
+import winBindings.kernel32
 import winKernel
 from logHandler import log
 import config
@@ -143,13 +144,13 @@ def write(self, data: bytes):
 			log.debug("Write: %r" % data)
 
 		size, data = self._prepareWriteBuffer(data)
-		if not ctypes.windll.kernel32.WriteFile(self._writeFile, data, size, None, byref(self._writeOl)):
+		if not winBindings.kernel32.WriteFile(self._writeFile, data, size, None, byref(self._writeOl)):
 			if ctypes.GetLastError() != ERROR_IO_PENDING:
 				if _isDebug():
 					log.debug("Write failed: %s" % ctypes.WinError())
 				raise ctypes.WinError()
 			byteData = DWORD()
-			ctypes.windll.kernel32.GetOverlappedResult(
+			winBindings.kernel32.GetOverlappedResult(
 				self._writeFile,
 				byref(self._writeOl),
 				byref(byteData),
@@ -162,9 +163,9 @@ def close(self):
 		self._onReceive = None
 		self._onReadError = None
 		if hasattr(self, "_file") and self._file is not INVALID_HANDLE_VALUE:
-			ctypes.windll.kernel32.CancelIoEx(self._file, byref(self._readOl))
+			winBindings.kernel32.CancelIoEx(self._file, byref(self._readOl))
 		if hasattr(self, "_writeFile") and self._writeFile not in (self._file, INVALID_HANDLE_VALUE):
-			ctypes.windll.kernel32.CancelIoEx(self._writeFile, byref(self._readOl))
+			winBindings.kernel32.CancelIoEx(self._writeFile, byref(self._readOl))
 		winKernel.closeHandle(self._recvEvt)
 
 	def __del__(self):
@@ -181,7 +182,7 @@ def _asyncRead(self, param: Optional[int] = None):
 		# Wait for _readSize bytes of data.
 		# _ioDone will call onReceive once it is received.
 		# onReceive can then optionally read additional bytes if it knows these are coming.
-		ctypes.windll.kernel32.ReadFileEx(
+		winBindings.kernel32.ReadFileEx(
 			self._file,
 			self._readBuf,
 			self._readSize,
@@ -201,7 +202,7 @@ def _ioDone(self, error, numberOfBytes: int, overlapped):
 				self._ioDone = None
 				return
 		self._notifyReceive(self._readBuf[:numberOfBytes])
-		winKernel.kernel32.SetEvent(self._recvEvt)
+		winBindings.kernel32.SetEvent(self._recvEvt)
 		self._asyncRead()
 
 	def _notifyReceive(self, data: bytes):

```