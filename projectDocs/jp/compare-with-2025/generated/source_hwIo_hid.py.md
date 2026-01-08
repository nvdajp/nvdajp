# Diff for: `source\hwIo\hid.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\hwIo\hid.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\hwIo\hid.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\hwIo\\hid.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\hwIo\\hid.py"
index cfffb82..46ae41c 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\hwIo\\hid.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\hwIo\\hid.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2015-2018 NV Access Limited, Babbage B.V.
+# Copyright (C) 2015-2025 NV Access Limited, Babbage B.V.
 
 
 """Raw input/output for braille displays via HID
@@ -20,9 +20,13 @@
 from logHandler import log
 from .base import IoBase, _isDebug
 import hidpi
+import winBindings.hid
+from utils import _deprecate
 
 
-hidDll = ctypes.windll.hid
+__getattr__ = _deprecate.handleDeprecations(
+	_deprecate.MovedSymbol("hidDll", "winBindings.hid", "dll"),
+)
 
 
 class HidPError(RuntimeError):
@@ -58,11 +62,11 @@ def __init__(self, device, data):
 		super().__init__(device)
 
 	def getUsages(self, usagePage, linkCollection=0):
-		maxUsages = hidDll.HidP_MaxUsageListLength(self._reportType, hidpi.USAGE(usagePage), self._dev._pd)
+		maxUsages = winBindings.hid.HidP_MaxUsageListLength(self._reportType, usagePage, self._dev._pd)
 		numUsages = ctypes.c_long(maxUsages)
 		usageList = (hidpi.USAGE * maxUsages)()
 		check_HidP_status(
-			hidDll.HidP_GetUsages,
+			winBindings.hid.HidP_GetUsages,
 			self._reportType,
 			hidpi.USAGE(usagePage),
 			USHORT(linkCollection),
@@ -75,11 +79,11 @@ def getUsages(self, usagePage, linkCollection=0):
 		return usageList[0 : numUsages.value]
 
 	def getDataItems(self):
-		maxDataLength = hidDll.HidP_MaxDataListLength(self._reportType, self._dev._pd)
+		maxDataLength = winBindings.hid.HidP_MaxDataListLength(self._reportType, self._dev._pd)
 		numDataLength = ctypes.c_ulong(maxDataLength)
 		dataList = (hidpi.HIDP_DATA * maxDataLength)()
 		check_HidP_status(
-			hidDll.HidP_GetData,
+			winBindings.hid.HidP_GetData,
 			self._reportType,
 			dataList,
 			ctypes.byref(numDataLength),
@@ -106,11 +110,11 @@ def data(self):
 	def setUsageValueArray(self, usagePage, linkCollection, usage, data):
 		dataBuf = ctypes.c_buffer(data)
 		check_HidP_status(
-			hidDll.HidP_SetUsageValueArray,
+			winBindings.hid.HidP_SetUsageValueArray,
 			self._reportType,
-			hidpi.USAGE(usagePage),
-			ctypes.c_ushort(linkCollection),
-			hidpi.USAGE(usage),
+			usagePage,
+			linkCollection,
+			usage,
 			dataBuf,
 			len(dataBuf),
 			self._dev._pd,
@@ -159,7 +163,7 @@ def __init__(
 				log.debug("Open failed: %s" % ctypes.WinError())
 			raise ctypes.WinError()
 		pd = ctypes.c_void_p()
-		if not hidDll.HidD_GetPreparsedData(handle, byref(pd)):
+		if not winBindings.hid.HidD_GetPreparsedData(handle, byref(pd)):
 			raise ctypes.WinError()
 		self._pd = pd
 		caps = self.caps
@@ -193,26 +197,26 @@ def caps(self):
 		if hasattr(self, "_caps"):
 			return self._caps
 		caps = hidpi.HIDP_CAPS()
-		check_HidP_status(hidDll.HidP_GetCaps, self._pd, byref(caps))
+		check_HidP_status(winBindings.hid.HidP_GetCaps, self._pd, byref(caps))
 		self._caps = caps
 		return self._caps
 
 	@property
-	def inputButtonCaps(self) -> ctypes.Array[hidpi.HIDP_VALUE_CAPS]:
+	def inputButtonCaps(self) -> ctypes.Array[hidpi.HIDP_BUTTON_CAPS]:
 		if hasattr(self, "_inputButtonCaps"):
 			return self._inputButtonCaps
-		valueCapsList = (hidpi.HIDP_VALUE_CAPS * self.caps.NumberInputButtonCaps)()
-		numValueCaps = ctypes.c_long(self.caps.NumberInputButtonCaps)
-		if numValueCaps.value == 0:
-			return valueCapsList
+		buttonCapsList = (hidpi.HIDP_BUTTON_CAPS * self.caps.NumberInputButtonCaps)()
+		numButtonCaps = ctypes.c_ushort(self.caps.NumberInputButtonCaps)
+		if numButtonCaps.value == 0:
+			return buttonCapsList
 		check_HidP_status(
-			hidDll.HidP_GetButtonCaps,
+			winBindings.hid.HidP_GetButtonCaps,
 			hidpi.HIDP_REPORT_TYPE.INPUT,
-			ctypes.byref(valueCapsList),
-			ctypes.byref(numValueCaps),
+			buttonCapsList,
+			ctypes.byref(numButtonCaps),
 			self._pd,
 		)
-		self._inputButtonCaps = valueCapsList
+		self._inputButtonCaps = buttonCapsList
 		return self._inputButtonCaps
 
 	@property
@@ -220,13 +224,13 @@ def inputValueCaps(self) -> ctypes.Array[hidpi.HIDP_VALUE_CAPS]:
 		if hasattr(self, "_inputValueCaps"):
 			return self._inputValueCaps
 		valueCapsList = (hidpi.HIDP_VALUE_CAPS * self.caps.NumberInputValueCaps)()
-		numValueCaps = ctypes.c_long(self.caps.NumberInputValueCaps)
+		numValueCaps = ctypes.c_ushort(self.caps.NumberInputValueCaps)
 		if numValueCaps.value == 0:
 			return valueCapsList
 		check_HidP_status(
-			hidDll.HidP_GetValueCaps,
+			winBindings.hid.HidP_GetValueCaps,
 			hidpi.HIDP_REPORT_TYPE.INPUT,
-			ctypes.byref(valueCapsList),
+			valueCapsList,
 			ctypes.byref(numValueCaps),
 			self._pd,
 		)
@@ -238,13 +242,13 @@ def outputValueCaps(self) -> ctypes.Array[hidpi.HIDP_VALUE_CAPS]:
 		if hasattr(self, "_outputValueCaps"):
 			return self._outputValueCaps
 		valueCapsList = (hidpi.HIDP_VALUE_CAPS * self.caps.NumberOutputValueCaps)()
-		numValueCaps = ctypes.c_long(self.caps.NumberOutputValueCaps)
+		numValueCaps = ctypes.c_ushort(self.caps.NumberOutputValueCaps)
 		if numValueCaps.value == 0:
 			return valueCapsList
 		check_HidP_status(
-			hidDll.HidP_GetValueCaps,
+			winBindings.hid.HidP_GetValueCaps,
 			hidpi.HIDP_REPORT_TYPE.OUTPUT,
-			ctypes.byref(valueCapsList),
+			valueCapsList,
 			ctypes.byref(numValueCaps),
 			self._pd,
 		)
@@ -274,7 +278,7 @@ def getFeature(self, reportId: bytes) -> bytes:
 		@return: The report, including the report id.
 		"""
 		buf = ctypes.create_string_buffer(reportId, size=self._featureSize)
-		if not hidDll.HidD_GetFeature(self._file, buf, self._featureSize):
+		if not winBindings.hid.HidD_GetFeature(self._file, buf, self._featureSize):
 			if _isDebug():
 				log.debug(
 					"Get feature %r failed: %s" % (reportId, ctypes.WinError()),
@@ -292,7 +296,7 @@ def setFeature(self, report: bytes) -> None:
 		bufSize = ctypes.sizeof(buf)
 		if _isDebug():
 			log.debug("Set feature: %r" % report)
-		result = hidDll.HidD_SetFeature(
+		result = winBindings.hid.HidD_SetFeature(
 			self._file,
 			buf,
 			bufSize,
@@ -312,7 +316,7 @@ def setOutputReport(self, report: bytes) -> None:
 		bufSize = ctypes.sizeof(buf)
 		if _isDebug():
 			log.debug("Set output report: %r" % report)
-		result = hidDll.HidD_SetOutputReport(
+		result = winBindings.hid.HidD_SetOutputReport(
 			self._writeFile,
 			buf,
 			bufSize,
@@ -329,5 +333,5 @@ def close(self):
 		super(Hid, self).close()
 		winKernel.closeHandle(self._file)
 		self._file = None
-		hidDll.HidD_FreePreparsedData(self._pd)
+		winBindings.hid.HidD_FreePreparsedData(self._pd)
 		self._isClosed = True

```