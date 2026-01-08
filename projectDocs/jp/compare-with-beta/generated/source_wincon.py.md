# Diff for: `source\wincon.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\wincon.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\wincon.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\wincon.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\wincon.py"
index 1f49bad..7ce1ab7 100644
--- "a/F:\\nvda\\gh\\beta\\source\\wincon.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\wincon.py"
@@ -6,13 +6,10 @@
 
 from ctypes import (
 	byref,
-	cast,
 	WinError,
-	create_unicode_buffer,
-	c_char,
-	c_void_p,
+	create_string_buffer,
+	c_int,
 )
-from ctypes.wintypes import DWORD
 import winBindings.kernel32
 from winBindings.kernel32 import (
 	COORD as _COORD,
@@ -69,14 +66,15 @@
 
 def GetConsoleSelectionInfo():
 	info = _CONSOLE_SELECTION_INFO()
-	if winBindings.kernel32.GetConsoleSelectionInfo(byref(info)) == 0:
-		raise WinError()
+	if winBindings.kernel32.GetConsoleSelectionInfo(byref(info)) == 0:  # noqa: F405
+		raise WinError()  # noqa: F405
 	return info
 
 
 def ReadConsoleOutputCharacter(handle, length, x, y):
-	buf = create_unicode_buffer(length)
-	numCharsRead = DWORD()
+	# Use a string buffer, as from an unicode buffer, we can't get the raw data.
+	buf = create_string_buffer(length * 2)  # noqa: F405
+	numCharsRead = c_int()  # noqa: F405
 	if (
 		winBindings.kernel32.ReadConsoleOutputCharacter(
 			handle,
@@ -84,16 +82,12 @@ def ReadConsoleOutputCharacter(handle, length, x, y):
 			length,
 			_COORD(x, y),
 			byref(numCharsRead),
-		)
+		)  # noqa: F405
 		== 0
-	):
-		raise WinError()
-	numRawBytes = numCharsRead.value * 2
-	rawBuf = (c_char * numRawBytes).from_address(
-		cast(buf, c_void_p).value or 0,
-	)
+	):  # noqa: F405
+		raise WinError()  # noqa: F405
 	return textUtils.getTextFromRawBytes(
-		rawBuf.raw,
+		buf.raw,
 		numChars=numCharsRead.value,
 		encoding=textUtils.WCHAR_ENCODING,
 	)
@@ -104,46 +98,46 @@ def ReadConsoleOutput(handle, length, rect):
 	buf = BufType()
 	# rect=SMALL_RECT(x, y, x+length-1, y)
 	if (
-		winBindings.kernel32.ReadConsoleOutput(
+		winBindings.kernel32.ReadConsoleOutput(  # noqa: F405
 			handle,
 			buf,
 			_COORD(rect.Right - rect.Left + 1, rect.Bottom - rect.Top + 1),
 			_COORD(0, 0),
-			byref(rect),
+			byref(rect),  # noqa: F405
 		)
 		== 0
-	):
-		raise WinError()
+	):  # noqa: F405
+		raise WinError()  # noqa: F405
 	return buf
 
 
 def GetConsoleScreenBufferInfo(handle):
 	info = _CONSOLE_SCREEN_BUFFER_INFO()
-	if winBindings.kernel32.GetConsoleScreenBufferInfo(handle, byref(info)) == 0:
-		raise WinError()
+	if winBindings.kernel32.GetConsoleScreenBufferInfo(handle, byref(info)) == 0:  # noqa: F405
+		raise WinError()  # noqa: F405
 	return info
 
 
 def FreeConsole():
-	if winBindings.kernel32.FreeConsole() == 0:
-		raise WinError()
+	if winBindings.kernel32.FreeConsole() == 0:  # noqa: F405
+		raise WinError()  # noqa: F405
 
 
 def AttachConsole(processID):
-	if winBindings.kernel32.AttachConsole(processID) == 0:
-		raise WinError()
+	if winBindings.kernel32.AttachConsole(processID) == 0:  # noqa: F405
+		raise WinError()  # noqa: F405
 
 
 def GetConsoleWindow():
-	return winBindings.kernel32.GetConsoleWindow()
+	return winBindings.kernel32.GetConsoleWindow()  # noqa: F405
 
 
 def GetConsoleProcessList(maxProcessCount):
-	processList = (DWORD * maxProcessCount)()
-	num = winBindings.kernel32.GetConsoleProcessList(processList, maxProcessCount)
+	processList = (c_int * maxProcessCount)()  # noqa: F405
+	num = winBindings.kernel32.GetConsoleProcessList(processList, maxProcessCount)  # noqa: F405
 	return processList[0:num]
 
 
 def SetConsoleCtrlHandler(handler, add):
-	if winBindings.kernel32.SetConsoleCtrlHandler(handler, add) == 0:
-		raise WinError()
+	if winBindings.kernel32.SetConsoleCtrlHandler(handler, add) == 0:  # noqa: F405
+		raise WinError()  # noqa: F405

```