# Diff for: `source\_remoteClient\secureDesktop.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\_remoteClient\secureDesktop.py`  
**Current**: `F:\nvda\gh\alphajp\source\_remoteClient\secureDesktop.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\secureDesktop.py" "b/F:\\nvda\\gh\\alphajp\\source\\_remoteClient\\secureDesktop.py"
index a52dc511e7..1a3993eb3d 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\secureDesktop.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\_remoteClient\\secureDesktop.py"
@@ -19,36 +19,19 @@
     to exchange connection information between sessions.
 """
 
-from enum import IntEnum
 import json
 import socket
 import threading
 import uuid
 from pathlib import Path
 from typing import Any, Optional
-from ctypes import (
-	POINTER,
-	FormatError,
-	GetLastError,
-	c_bool,
-	c_size_t,
-	sizeof,
-	windll,
-	c_wchar_p,
-	c_ushort,
-	create_unicode_buffer,
-	WINFUNCTYPE,
-	wstring_at,
-)
-from ctypes.wintypes import BOOL, DWORD, HANDLE, LPCVOID, LPCWSTR, LPVOID, WCHAR
-from serial.win32 import INVALID_HANDLE_VALUE
+from ctypes import create_unicode_buffer
 
 import shlobj
 from logHandler import log
 from winAPI.secureDesktop import post_secureDesktopStateChange
 from NVDAHelper import localLib
-from winKernel import closeHandle
-from winKernel import ERROR_ALREADY_EXISTS, SECURITY_ATTRIBUTES
+from winBindings import kernel32
 
 from . import bridge, server
 from .connectionInfo import ConnectionInfo, ConnectionMode
@@ -58,193 +41,6 @@
 from .transport import RelayTransport
 
 
-class PAGE(IntEnum):
-	"""
-	Specifies the page protection of a file mapping object.
-
-	.. note::
-		Possible values for the ``flProtect`` parameter of ``CreateFileMapping``.
-
-	.. seealso::
-		https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-createfilemappingw
-	"""
-
-	EXECUTE_READ = 0x20
-	"""Allows views to be mapped for read-only, copy-on-write, or execute access."""
-
-	EXECUTE_READWRITE = 0x40
-	"""Allows views to be mapped for read-only, copy-on-write, read/write, or execute access."""
-
-	EXECUTE_WRITECOPY = 0x80
-	"""Allows views to be mapped for read-only, copy-on-write, or execute access."""
-
-	READONLY = 0x02
-	"""Allows views to be mapped for read-only or copy-on-write access."""
-
-	READWRITE = 0x04
-	"""Allows views to be mapped for read-only, copy-on-write, or read/write access."""
-
-	WRITECOPY = 0x08
-	"""Allows views to be mapped for read-only or copy-on-write access."""
-
-
-class FILE_MAP(IntEnum):
-	"""
-	The type of access to a file mapping object, which determines the page protection of the pages.
-
-	.. seealso::
-		https://learn.microsoft.com/en-us/windows/win32/memory/file-mapping-security-and-access-rights
-	"""
-
-	WRITE = 0x0002
-	"""
-	A read/write view of the file is mapped.
-
-	.. note::
-		When used with ``MapViewOfFile``, ``WRITE`` and ``ALL_ACCESS`` are equivalent.
-	"""
-
-	READ = 0x0004
-	"""A read-only view of the file is mapped."""
-
-	ALL_ACCESS = 0x000F001F
-	"""
-	A read/write view of the file is mapped.
-
-	.. note::
-		When used with ``MapViewOfFile``, ``ALL_ACCESS`` and ``WRITE`` are equivalent.
-	"""
-
-
-class WAIT(IntEnum):
-	"""Indicates the result of a Wait function."""
-
-	OBJECT_0 = 0x00000000
-	"""The state of the specified object is signaled."""
-
-	TIMEOUT = 0x00000102
-	"""The time-out interval elapsed, and the object's state is nonsignaled."""
-
-	FAILED = 0xFFFFFFFF
-	"""The function has failed."""
-
-
-kernel32 = windll.kernel32
-CreateFileMapping = WINFUNCTYPE(HANDLE, HANDLE, POINTER(SECURITY_ATTRIBUTES), DWORD, DWORD, DWORD, LPCWSTR)(
-	("CreateFileMappingW", kernel32),
-	(
-		(1, "hFile"),
-		(1, "lpFileMappingAttributes"),
-		(1, "flProtect"),
-		(1, "dwMaximumSizeHigh"),
-		(1, "dwMaximumSizeLow"),
-		(1, "lpName"),
-	),
-)
-"""
-Creates or opens a named or unnamed file mapping object for a specified file.
-
-.. seealso::
-	https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-createfilemappingw
-"""
-
-MapViewOfFile = WINFUNCTYPE(LPVOID, HANDLE, DWORD, DWORD, DWORD, c_size_t)(
-	("MapViewOfFile", kernel32),
-	(
-		(1, "hFileMappingObject"),
-		(1, "dwDesiredAccess"),
-		(1, "dwFileOffsetHigh"),
-		(1, "dwFileOffsetLow"),
-		(1, "dwNumberOfBytesToMap"),
-	),
-)
-"""
-Maps a view of a file mapping into the address space of a calling process.
-
-.. seealso::
-	https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-mapviewoffile
-"""
-
-UnmapViewOfFile = WINFUNCTYPE(BOOL, LPCVOID)(
-	("UnmapViewOfFile", kernel32),
-	((1, "lpBaseAddress"),),
-)
-"""
-Unmaps a mapped view of a file from the calling process's address space.
-
-.. seealso::
-	https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-unmapviewoffile
-"""
-
-OpenFileMapping = WINFUNCTYPE(HANDLE, DWORD, BOOL, LPCWSTR)(
-	("OpenFileMappingW", kernel32),
-	(
-		(1, "dwDesiredAccess"),
-		(1, "bInheritHandle"),
-		(1, "lpName"),
-	),
-)
-"""
-Opens a named file mapping object.
-
-.. seealso::
-	https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-openfilemappingw
-"""
-
-
-CreateEvent = WINFUNCTYPE(HANDLE, LPVOID, BOOL, BOOL, LPCWSTR)(
-	("CreateEventW", kernel32),
-	(
-		(1, "lpEventAttributes"),
-		(1, "bManualReset"),
-		(1, "bInitialState"),
-		(1, "lpName"),
-	),
-)
-"""
-Creates or opens a named or unnamed event object.
-
-.. seealso::
-	https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createeventw
-"""
-
-WaitForSingleObject = WINFUNCTYPE(DWORD, HANDLE, DWORD)(
-	("WaitForSingleObject", kernel32),
-	(
-		(1, "hHandle"),
-		(1, "dwMilliseconds"),
-	),
-)
-"""
-Waits until the specified object is in the signaled state or the time-out interval elapses.
-
-.. seealso::
-	https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject
-"""
-
-SetEvent = WINFUNCTYPE(BOOL, HANDLE)(
-	("SetEvent", kernel32),
-	((1, "hEvent"),),
-)
-"""
-Sets the specified event object to the signaled state.
-
-.. seealso::
-
-"""
-
-ResetEvent = WINFUNCTYPE(BOOL, HANDLE)(
-	("ResetEvent", kernel32),
-	((1, "hEvent"),),
-)
-"""
-Sets the specified event object to the nonsignaled state.
-
-.. seealso::
-	https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-resetevent
-"""
-
-
 def getProgramDataTempPath() -> Path:
 	"""Get the system's program data temp directory path.
 
@@ -264,31 +60,16 @@ class SecureDesktopHandler:
 
 	SD_CONNECT_BLOCK_TIMEOUT: int = 1
 
-	_IPC_FILENAME = r"Local\NVDARemoteAccessSDHIPCFile"
-	"""IPC filename"""
-	_IPC_EVENTNAME = r"Local\NVDARemoteAccessSDHIPCEvent"
-	"""IPC write event name"""
-	_IPC_MAXLEN = 64
-	"""
-	Maximum length of IPC data, in characters.
-
-	36 chars for a UUID4, 5 chars for a port number, and plenty of slack for JSON syntax.
-
-	.. note::
-		Must be multiplied by the size of a character when allocating memory.
-	"""
-
-	def __init__(self):
+	def __init__(self, tempPath: Path = getProgramDataTempPath()) -> None:
 		"""Initialize secure desktop handler.
 
-		:raises RuntimeError: if the IPC event cannot be created or opened.
+		:param tempPath: Directory for IPC file storage
 		"""
-		self._mapFile: int | None = None
-		self._bufferAddress: int | None = None
-		self._ipcEventHandle = CreateEvent(None, False, False, self._IPC_EVENTNAME)
-		if self._ipcEventHandle is None:
-			raise RuntimeError(f"Unable to get handle to IPC event. {GetLastError()}: {FormatError()}")
-		log.debug("Initialized SecureDesktopHandler")
+		self.tempPath = tempPath
+		self.IPCPath: Path = self.tempPath / "NVDA"
+		self.IPCPath.mkdir(parents=True, exist_ok=True)
+		self.IPCFile = self.IPCPath / "remote.ipc"
+		log.debug("Initialized SecureDesktopHandler with IPC file: %s", self.IPCFile)
 
 		self._followerSession: Optional[FollowerSession] = None
 		self.sdServer: Optional[server.LocalRelayServer] = None
@@ -302,19 +83,11 @@ def terminate(self) -> None:
 		log.debug("Terminating SecureDesktopHandler")
 		post_secureDesktopStateChange.unregister(self._onSecureDesktopChange)
 		self.leaveSecureDesktop()
-		# The IPC event will be disposed of by the OS when all of its handles are closed.
-		if not closeHandle(self._ipcEventHandle):
-			log.debugWarning(f"Error closing handle to IPC event. {GetLastError()}: {FormatError()}")
-		# We shouldn't be in a situation where we have shared IPC data,
-		# but it's still good to check and clean it up if we do.
-		if self._bufferAddress is not None:
-			if not UnmapViewOfFile(self._bufferAddress):
-				log.debugWarning(f"Error unmapping IPC shared memory. {GetLastError()}: {FormatError()}")
-		if self._mapFile is not None:
-			if not closeHandle(self._mapFile):
-				log.debugWarning(
-					f"Error closing handle to IPC file mapping. {GetLastError()}: {FormatError()}",
-				)
+		try:
+			log.debug("Removing IPC file: %s", self.IPCFile)
+			self.IPCFile.unlink()
+		except FileNotFoundError:
+			log.debug("IPC file already removed")
 		log.info("Secure desktop cleanup completed")
 
 	@property
@@ -359,62 +132,15 @@ def enterSecureDesktop(self) -> None:
 		if self.followerSession is None or self.followerSession.transport is None:
 			log.warning("No follower session connected, not entering secure desktop.")
 			return
-		log.debug("Creating shared memory for IPC.")
-		mapFile = CreateFileMapping(
-			INVALID_HANDLE_VALUE,  # Shared memory
-			None,
-			PAGE.READWRITE,
-			0,  # High-order size
-			self._IPC_MAXLEN * sizeof(WCHAR),  # Low-order size
-			self._IPC_FILENAME,
-		)
-		if mapFile is None:
-			log.error(f"Error creating file mapping: {GetLastError()}: {FormatError()}")
-			return
-		if GetLastError() == ERROR_ALREADY_EXISTS:
-			log.debugWarning("Mapped file already exists")
-		bufferAddress = MapViewOfFile(
-			mapFile,
-			FILE_MAP.ALL_ACCESS,
-			0,
-			0,
-			self._IPC_MAXLEN * sizeof(WCHAR),
-		)
-		if bufferAddress is None:
-			log.error(f"Couldn't map view of file. {GetLastError()}: {FormatError()}")
-			if not closeHandle(mapFile):
-				log.debugWarning(
-					f"Error closing handle to IPC file mapping. {GetLastError()}: {FormatError()}",
-				)
-			return
-		buffer = (WCHAR * self._IPC_MAXLEN).from_address(bufferAddress)
+		if not self.tempPath.exists():
+			log.debug(f"Creating temp directory: {self.tempPath}")
+			self.tempPath.mkdir(parents=True, exist_ok=True)
+
 		channel = str(uuid.uuid4())
 		log.debug("Starting local relay server")
 		self.sdServer = server.LocalRelayServer(port=0, password=channel, bindHost="127.0.0.1")
 		port = self.sdServer.serverSocket.getsockname()[1]
 		log.info("Local relay server started on port %d", port)
-		try:
-			log.debug("Writing connection data to shared memory")
-			buffer.value = json.dumps([port, channel])
-			# Setting value checks if the array is long enough to contain the literal value,
-			# and will write a terminating null if there is space to do so.
-			# However, if the given string is exactly the length of the buffer,
-			# no null terminator will be written.
-			# If this happens, we cannot proceed,
-			# as the contents of the array are not a valid c string.
-			if buffer[-1] != "\x00":
-				raise ValueError("Insufficient length for null terminator.")
-		except ValueError:
-			log.exception("Failed to write IPC data.", exc_info=True)
-			if not UnmapViewOfFile(bufferAddress):
-				log.debugWarning(f"Error unmapping IPC shared memory. {GetLastError()}: {FormatError()}")
-			if not closeHandle(mapFile):
-				log.debugWarning(
-					f"Error closing handle to IPC file mapping. {GetLastError()}: {FormatError()}",
-				)
-			self.sdServer.close()
-			self.sdServer = None
-			return None
 
 		serverThread = threading.Thread(target=self.sdServer.run)
 		serverThread.daemon = True
@@ -439,10 +165,9 @@ def enterSecureDesktop(self) -> None:
 		relayThread.daemon = True
 		relayThread.start()
 
-		self._mapFile, self._bufferAddress = mapFile, bufferAddress
-		# Signal that it's now safe to read the IPC shared memory and connect
-		if not SetEvent(self._ipcEventHandle):
-			log.error(f"Failed to set IPC event. {GetLastError()}: {FormatError()}")
+		data = [port, channel]
+		log.debug(f"Writing connection data to IPC file: {self.IPCFile}")
+		self.IPCFile.write_text(json.dumps(data))
 		log.info("Secure desktop setup completed successfully")
 
 	def leaveSecureDesktop(self) -> None:
@@ -471,58 +196,21 @@ def leaveSecureDesktop(self) -> None:
 			)
 			self.followerSession.setDisplaySize()
 
-		# The IPC event won't have been reset if a secure desktop copy didn't wait for it.
-		# Even if it's not in the set state, resetting it is harmless.
-		if not ResetEvent(self._ipcEventHandle):
-			log.debugWarning(f"Failed to reset IPC event. {GetLastError()}: {FormatError()}")
-		if self._bufferAddress is not None:
-			if not UnmapViewOfFile(self._bufferAddress):
-				log.debugWarning(f"Failed to unmap IPC file. {GetLastError()}: {FormatError()}")
-			self._bufferAddress = None
-		if self._mapFile is not None:
-			if not closeHandle(self._mapFile):
-				log.debugWarning(
-					f"Failed to close handle to memory mapped IPC file. {GetLastError()}: {FormatError()}"
-				)
-			self._mapFile = None
+		try:
+			self.IPCFile.unlink()
+		except FileNotFoundError:
+			pass
 
 	def initializeSecureDesktop(self) -> Optional[ConnectionInfo]:
 		"""Initialize connection when starting in secure desktop.
 
 		:return: Connection information if successful, None on failure
 		"""
-		getModuleFileName = windll.kernel32.GetModuleFileNameW
-		getModuleFileName.argtypes = (HANDLE, c_wchar_p, DWORD)
-		getModuleFileName.restype = DWORD
-		localListeningSocketExists = localLib.localListeningSocketExists
-		localListeningSocketExists.argtypes = (c_ushort, c_wchar_p)
-		localListeningSocketExists.restype = c_bool
 		log.info("Initializing secure desktop connection")
-		# Even though we only need read access,
-		# Memory mapped files must all be mapped with the same permissions.
-		mapFile = OpenFileMapping(FILE_MAP.ALL_ACCESS, False, self._IPC_FILENAME)
-		if mapFile is None:
-			log.debug(f"Failed to open IPC file mapping. {GetLastError()}: {FormatError()}")
-			return None
-		bufferAddress = MapViewOfFile(mapFile, FILE_MAP.ALL_ACCESS, 0, 0, self._IPC_MAXLEN * sizeof(WCHAR))
-		if bufferAddress is None:
-			log.error(f"Failed to map IPC file mapping. {GetLastError()}: {FormatError()}")
-			if not closeHandle(mapFile):
-				log.debugWarning(f"Failed to close file mapping. {GetLastError()}: {FormatError()}")
-			return None
-		waitResult = WaitForSingleObject(self._ipcEventHandle, 2000)
-		if waitResult == WAIT.TIMEOUT:
-			log.error("Timed out while waiting for IPC data.")
-			return None
-		elif waitResult == WAIT.FAILED:
-			log.error(f"Failed to wait for event. {GetLastError()}: {FormatError()}")
-			return None
-		elif waitResult != WAIT.OBJECT_0:
-			log.error(f"Unknown return from WaitForSingleObject: {waitResult}")
-			return None
 		try:
-			log.debug("Reading connection data from IPC file mapping.")
-			data = json.loads(wstring_at(bufferAddress))
+			log.debug(f"Reading connection data from IPC file: {self.IPCFile}")
+			data = json.loads(self.IPCFile.read_text())
+			self.IPCFile.unlink()
 			port, channel = data
 
 			# Try opening a socket to make sure we have the appropriate permissions
@@ -531,8 +219,8 @@ def initializeSecureDesktop(self) -> Optional[ConnectionInfo]:
 
 			# Check that a socket is open on the right IP and port and with the same owning process image
 			processImageName = create_unicode_buffer(1024)
-			getModuleFileName(0, processImageName, 1024)
-			if not localListeningSocketExists(port, processImageName):
+			kernel32.GetModuleFileName(0, processImageName, 1024)
+			if not localLib.localListeningSocketExists(port, processImageName):
 				raise RuntimeError("Matching socket not open.")
 
 			log.info(f"Successfully established secure desktop connection on port {port}")
@@ -547,13 +235,6 @@ def initializeSecureDesktop(self) -> Optional[ConnectionInfo]:
 		except Exception:
 			log.warning("Failed to initialize secure desktop connection.", exc_info=True)
 			return None
-		finally:
-			if not UnmapViewOfFile(bufferAddress):
-				log.debugWarning(f"Failed to unmap view of IPC file. {GetLastError()}: {FormatError()}")
-			if not closeHandle(mapFile):
-				log.debugWarning(
-					f"Failed to close handle to IPC file mapping. {GetLastError()}: {FormatError()}",
-				)
 
 	def _onLeaderDisplayChange(self, **kwargs: Any) -> None:
 		"""Handle display size changes."""

```