# Diff for: `source\NVDAObjects\window\edit.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\window\edit.py`  
**Current**: `F:\nvda\gh\alphajp\source\NVDAObjects\window\edit.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\window\\edit.py" "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\window\\edit.py"
index 6029f5b384..a334597133 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\window\\edit.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\window\\edit.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2023 NV Access Limited, Babbage B.V., Cyrille Bougot, Leonard de Ruijter
+# Copyright (C) 2006-2025 NV Access Limited, Babbage B.V., Cyrille Bougot, Leonard de Ruijter
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -9,17 +9,15 @@
 	Union,
 )
 
-import comtypes.client
 import ctypes
-from comtypes import COMError
-import oleTypes
+from comtypes import BSTR, COMError
 import colors
-import NVDAHelper
 import eventHandler
 import comInterfaces.tom
 from logHandler import log
 import languageHandler
 import config
+import winBindings.oleacc
 import winKernel
 import api
 import winUser
@@ -34,6 +32,8 @@
 import watchdog
 import locationHelper
 import textUtils
+import NVDAHelper.localLib
+
 
 selOffsetsAtLastCaretEvent = None
 
@@ -466,7 +466,7 @@ def _setCaretOffset(self, offset):
 
 	def _getStoryText(self):
 		if controlTypes.State.PROTECTED in self.obj.states:
-			return "*" * (self._getStoryLength() - 1)
+			return "*" * self._getStoryLength()
 		return self.obj.windowText
 
 	def _getStoryLength(self):
@@ -501,18 +501,12 @@ def _getStoryLength(self):
 				)
 			finally:
 				winKernel.virtualFreeEx(processHandle, internalInfo, 0, winKernel.MEM_RELEASE)
-			# Py3 review: investigation with Python 2 NVDA revealed that
-			# adding 1 to this creates an off by one error.
-			# Tested using Wordpad, enforcing EditTextInfo as the textInfo implementation.
-			return textLen + 1
+			return textLen
 		else:
 			# ForWM_GETTEXTLENGTH documentation, see
 			# https://docs.microsoft.com/en-us/windows/desktop/winmsg/wm-gettextlength
 			# It determines the length, in characters, of the text associated with a window.
-			# Py3 review: investigation with Python 2 NVDA revealed that
-			# adding 1 to this created an off by one error.
-			# Tested using Notepad
-			return watchdog.cancellableSendMessage(self.obj.windowHandle, winUser.WM_GETTEXTLENGTH, 0, 0) + 1
+			return watchdog.cancellableSendMessage(self.obj.windowHandle, winUser.WM_GETTEXTLENGTH, 0, 0)
 
 	def _getLineCount(self):
 		return self.obj.windowTextLineCount
@@ -624,42 +618,11 @@ def _getLineNumFromOffset(self, offset):
 		else:
 			return watchdog.cancellableSendMessage(self.obj.windowHandle, winUser.EM_LINEFROMCHAR, offset, 0)
 
-	def _needsWorkAroundEncoding(self):
-		return config.conf["language"]["jpAnsiEditbox"] and (not self.obj.isWindowUnicode)
-
-	def _startEndInBytesToStartEndInUnicodeChars(self, start, end):
-		# start/end in bytes to start/end in unicode chars
-		story_text = self._getStoryText()
-		start_new = end_new = -1
-		bytepos = 0
-		for charpos, ch in enumerate(story_text):
-			cb = len(ch.encode("mbcs", "replace"))
-			if bytepos == start:
-				start_new = charpos
-			if bytepos == end:
-				end_new = charpos
-				break
-			bytepos += cb
-		if end_new == -1:
-			end_new = len(story_text)
-		return (start_new, end_new)
-
 	def _getLineOffsets(self, offset):
-		if self._needsWorkAroundEncoding():
-			# offset in unicode chars to offset in bytes
-			s = self._getStoryText()[0:offset]
-			offset = len(s.encode("mbcs", "replace"))
 		lineNum = self._getLineNumFromOffset(offset)
 		start = watchdog.cancellableSendMessage(self.obj.windowHandle, winUser.EM_LINEINDEX, lineNum, 0)
 		length = watchdog.cancellableSendMessage(self.obj.windowHandle, winUser.EM_LINELENGTH, offset, 0)
 		end = start + length
-		if self._needsWorkAroundEncoding():
-			start_new, end_new = self._startEndInBytesToStartEndInUnicodeChars(start, end)
-			log.debug(
-				"offset %d lineNum %d start %d length %d end %d start_new %d end_new %d"
-				% (offset, lineNum, start, length, end, start_new, end_new)
-			)
-			return (start_new, end_new)
 		# If we just seem to get invalid line info, calculate manually
 		if (
 			start <= 0
@@ -833,7 +796,7 @@ def _getEmbeddedObjectLabel(self, embedRangeObj):
 		label = None
 		try:
 			o = embedRangeObj.GetEmbeddedObject()
-		except comtypes.COMError:
+		except COMError:
 			o = None
 		if not o:
 			return None
@@ -842,7 +805,7 @@ def _getEmbeddedObjectLabel(self, embedRangeObj):
 
 		try:
 			label = o.QueryInterface(oleacc.IAccessible).accName(0)
-		except comtypes.COMError:
+		except COMError:
 			pass
 		if label:
 			return label
@@ -865,23 +828,25 @@ def _getEmbeddedObjectLabel(self, embedRangeObj):
 		if label and not label.isspace():
 			return label
 		# Windows Live Mail exposes the label via the embedded object's data (IDataObject)
+		text = BSTR()
 		try:
-			dataObj = o.QueryInterface(oleTypes.IDataObject)
-		except comtypes.COMError:
-			dataObj = None
-		if dataObj:
-			text = comtypes.BSTR()
-			NVDAHelper.localLib.getOleClipboardText(dataObj, ctypes.byref(text))
+			NVDAHelper.localLib.getOleClipboardText(o, ctypes.byref(text))
+		except WindowsError:
+			pass
+		else:
 			label = text.value
 		if label:
 			return label
-		# As a final fallback (e.g. could not get display  model text for Outlook Express), use the embedded object's user type (e.g. "recipient").
+		# As a final fallback (e.g. could not get display model text for Outlook Express), use the embedded object's user type (e.g. "recipient").
+		userType = BSTR()
 		try:
-			oleObj = o.QueryInterface(oleTypes.IOleObject)
-			label = oleObj.GetUserType(1)
-		except comtypes.COMError:
+			NVDAHelper.localLib.getOleUserType(o, 0, ctypes.byref(userType))
+		except WindowsError:
 			pass
-		return label
+		else:
+			label = userType.value
+		if label:
+			return label
 
 	def _getTextAtRange(self, rangeObj):
 		embedRangeObj = None
@@ -1087,7 +1052,7 @@ def _get_ITextDocumentObject(self):
 		if not hasattr(self, "_ITextDocumentObject"):
 			try:
 				ptr = ctypes.POINTER(comInterfaces.tom.ITextDocument)()
-				ctypes.windll.oleacc.AccessibleObjectFromWindow(
+				winBindings.oleacc.AccessibleObjectFromWindow(
 					self.windowHandle,
 					-16,
 					ctypes.byref(ptr._iid_),

```