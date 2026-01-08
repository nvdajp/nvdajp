# Diff for: `source\wincon.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\wincon.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\wincon.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\wincon.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\wincon.py"
index 67fc251..1f49bad 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\wincon.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\wincon.py"
@@ -1,51 +1,60 @@
-from ctypes import *  # noqa: F403
-from ctypes.wintypes import *  # noqa: F403
+# A part of NonVisual Desktop Access (NVDA)
+# Copyright (C) 2006-2025 NV Access Limited
+# This file is covered by the GNU General Public License.
+# See the file COPYING for more details.
+
+
+from ctypes import (
+	byref,
+	cast,
+	WinError,
+	create_unicode_buffer,
+	c_char,
+	c_void_p,
+)
+from ctypes.wintypes import DWORD
+import winBindings.kernel32
+from winBindings.kernel32 import (
+	COORD as _COORD,
+	CONSOLE_SCREEN_BUFFER_INFO as _CONSOLE_SCREEN_BUFFER_INFO,
+	CONSOLE_SELECTION_INFO as _CONSOLE_SELECTION_INFO,
+	CHAR_INFO as _CHAR_INFO,
+)
 import textUtils
+from utils import _deprecate
 
 """
 Lower level utility functions and constants for NVDA's
 legacy Windows console support, for situations where UIA isn't available.
 """
 
-CONSOLE_REAL_OUTPUT_HANDLE = -2
-
-
-class COORD(Structure):  # noqa: F405
-	_fields_ = [
-		("x", c_short),  # noqa: F405
-		("y", c_short),  # noqa: F405
-	]
-
-
-class CONSOLE_SCREEN_BUFFER_INFO(Structure):  # noqa: F405
-	_fields_ = [
-		("dwSize", COORD),
-		("dwCursorPosition", COORD),
-		("wAttributes", WORD),  # noqa: F405
-		("srWindow", SMALL_RECT),  # noqa: F405
-		("dwMaximumWindowSize", COORD),
-	]
-
-
-class CONSOLE_SELECTION_INFO(Structure):  # noqa: F405
-	_fields_ = [
-		("dwFlags", DWORD),  # noqa: F405
-		("dwSelectionAnchor", COORD),
-		("srSelection", SMALL_RECT),  # noqa: F405
-	]
 
+__getattr__ = _deprecate.handleDeprecations(
+	_deprecate.MovedSymbol(
+		"COORD",
+		"winBindings.kernel32",
+	),
+	_deprecate.MovedSymbol(
+		"CONSOLE_SCREEN_BUFFER_INFO",
+		"winBindings.kernel32",
+	),
+	_deprecate.MovedSymbol(
+		"CONSOLE_SELECTION_INFO",
+		"winBindings.kernel32",
+	),
+	_deprecate.MovedSymbol(
+		"CHAR_INFO",
+		"winBindings.kernel32",
+	),
+	_deprecate.MovedSymbol(
+		"PHANDLER_ROUTINE",
+		"winBindings.kernel32",
+	),
+)
 
-class CHAR_INFO(Structure):  # noqa: F405
-	_fields_ = [
-		(
-			"Char",
-			c_wchar,  # noqa: F405
-		),  # union of char and wchar_t isn't needed since we deal only with unicode  # noqa: F405
-		("Attributes", WORD),  # noqa: F405
-	]
 
+CONSOLE_REAL_OUTPUT_HANDLE = -2
 
-PHANDLER_ROUTINE = WINFUNCTYPE(BOOL, DWORD)  # noqa: F405
 
 CTRL_C_EVENT = 0
 CTRL_BREAK_EVENT = 1
@@ -59,73 +68,82 @@ class CHAR_INFO(Structure):  # noqa: F405
 
 
 def GetConsoleSelectionInfo():
-	info = CONSOLE_SELECTION_INFO()
-	if windll.kernel32.GetConsoleSelectionInfo(byref(info)) == 0:  # noqa: F405
-		raise WinError()  # noqa: F405
+	info = _CONSOLE_SELECTION_INFO()
+	if winBindings.kernel32.GetConsoleSelectionInfo(byref(info)) == 0:
+		raise WinError()
 	return info
 
 
 def ReadConsoleOutputCharacter(handle, length, x, y):
-	# Use a string buffer, as from an unicode buffer, we can't get the raw data.
-	buf = create_string_buffer(length * 2)  # noqa: F405
-	numCharsRead = c_int()  # noqa: F405
+	buf = create_unicode_buffer(length)
+	numCharsRead = DWORD()
 	if (
-		windll.kernel32.ReadConsoleOutputCharacterW(handle, buf, length, COORD(x, y), byref(numCharsRead))  # noqa: F405
+		winBindings.kernel32.ReadConsoleOutputCharacter(
+			handle,
+			buf,
+			length,
+			_COORD(x, y),
+			byref(numCharsRead),
+		)
 		== 0
-	):  # noqa: F405
-		raise WinError()  # noqa: F405
+	):
+		raise WinError()
+	numRawBytes = numCharsRead.value * 2
+	rawBuf = (c_char * numRawBytes).from_address(
+		cast(buf, c_void_p).value or 0,
+	)
 	return textUtils.getTextFromRawBytes(
-		buf.raw,
+		rawBuf.raw,
 		numChars=numCharsRead.value,
 		encoding=textUtils.WCHAR_ENCODING,
 	)
 
 
 def ReadConsoleOutput(handle, length, rect):
-	BufType = CHAR_INFO * length
+	BufType = _CHAR_INFO * length
 	buf = BufType()
 	# rect=SMALL_RECT(x, y, x+length-1, y)
 	if (
-		windll.kernel32.ReadConsoleOutputW(  # noqa: F405
+		winBindings.kernel32.ReadConsoleOutput(
 			handle,
 			buf,
-			COORD(rect.Right - rect.Left + 1, rect.Bottom - rect.Top + 1),
-			COORD(0, 0),
-			byref(rect),  # noqa: F405
+			_COORD(rect.Right - rect.Left + 1, rect.Bottom - rect.Top + 1),
+			_COORD(0, 0),
+			byref(rect),
 		)
 		== 0
-	):  # noqa: F405
-		raise WinError()  # noqa: F405
+	):
+		raise WinError()
 	return buf
 
 
 def GetConsoleScreenBufferInfo(handle):
-	info = CONSOLE_SCREEN_BUFFER_INFO()
-	if windll.kernel32.GetConsoleScreenBufferInfo(handle, byref(info)) == 0:  # noqa: F405
-		raise WinError()  # noqa: F405
+	info = _CONSOLE_SCREEN_BUFFER_INFO()
+	if winBindings.kernel32.GetConsoleScreenBufferInfo(handle, byref(info)) == 0:
+		raise WinError()
 	return info
 
 
 def FreeConsole():
-	if windll.kernel32.FreeConsole() == 0:  # noqa: F405
-		raise WinError()  # noqa: F405
+	if winBindings.kernel32.FreeConsole() == 0:
+		raise WinError()
 
 
 def AttachConsole(processID):
-	if windll.kernel32.AttachConsole(processID) == 0:  # noqa: F405
-		raise WinError()  # noqa: F405
+	if winBindings.kernel32.AttachConsole(processID) == 0:
+		raise WinError()
 
 
 def GetConsoleWindow():
-	return windll.kernel32.GetConsoleWindow()  # noqa: F405
+	return winBindings.kernel32.GetConsoleWindow()
 
 
 def GetConsoleProcessList(maxProcessCount):
-	processList = (c_int * maxProcessCount)()  # noqa: F405
-	num = windll.kernel32.GetConsoleProcessList(processList, maxProcessCount)  # noqa: F405
+	processList = (DWORD * maxProcessCount)()
+	num = winBindings.kernel32.GetConsoleProcessList(processList, maxProcessCount)
 	return processList[0:num]
 
 
 def SetConsoleCtrlHandler(handler, add):
-	if windll.kernel32.SetConsoleCtrlHandler(handler, add) == 0:  # noqa: F405
-		raise WinError()  # noqa: F405
+	if winBindings.kernel32.SetConsoleCtrlHandler(handler, add) == 0:
+		raise WinError()

```