# Diff for: `source\NVDAObjects\window\excel.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\window\excel.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\window\excel.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\window\\excel.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\window\\excel.py"
index f177ea6..d05ed8b 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\window\\excel.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\window\\excel.py"
@@ -8,11 +8,12 @@
 import abc
 import ctypes
 import enum
-from typing import (
-	Any,
-	Optional,
-	Callable,
-)
+from winBindings import user32
+import winBindings.gdi32
+
+from typing import Any
+from collections.abc import Callable
+import warnings
 
 from comtypes import COMError, BSTR
 import comtypes.automation
@@ -44,6 +45,7 @@
 from displayModel import DisplayModelTextInfo
 import controlTypes
 from controlTypes import TextPosition, TextAlign, VerticalTextAlign
+from NVDAHelper.localLib import EXCEL_CELLINFO
 from . import Window
 from .. import NVDAObjectTextInfo
 import scriptHandler
@@ -136,7 +138,8 @@ def __getattr__(attrName: str) -> Any:
 			1: "default",
 		},
 	}
-	if attrName in _deprecatedConstantsMap and NVDAState._allowDeprecatedAPI():
+	if NVDAState._allowDeprecatedAPI():
+		if attrName in _deprecatedConstantsMap:
 			replacementSymbol = _deprecatedConstantsMap[attrName]
 			log.warning(
 				f"Importing {attrName} from here is deprecated. "
@@ -144,6 +147,13 @@ def __getattr__(attrName: str) -> Any:
 				stack_info=True,
 			)
 			return replacementSymbol
+		elif attrName == "ExcelCellInfo":
+			warnings.warn(
+				"NVDAObjects.window.excel.ExcelCellInfo is deprecated. Use NVDAHelper.localLib.EXCEL_CELLINFO instead.",
+				DeprecationWarning,
+				stacklevel=2,
+			)
+			return EXCEL_CELLINFO
 	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")
 
 
@@ -1171,8 +1181,11 @@ def script_changeActiveCell(self, gesture: inputCore.InputGesture) -> None:
 			"kb:control+shift+8",
 			"kb:control+pageUp",
 			"kb:control+pageDown",
+			# BEGIN JP PATCH
+			# nvdajp: restore Shift+Control+PageUp/Down key bindings for Excel cell navigation
 			"kb:shift+control+pageUp",
 			"kb:shift+control+pageDown",
+			# END JP PATCH
 			"kb:control+a",
 			"kb:control+v",
 			"kb:shift+f11",
@@ -1461,23 +1474,6 @@ class NvCellState(enum.IntEnum):
 }
 
 
-class ExcelCellInfo(ctypes.Structure):
-	_fields_ = [
-		("text", comtypes.BSTR),
-		("address", comtypes.BSTR),
-		("inputTitle", comtypes.BSTR),
-		("inputMessage", comtypes.BSTR),
-		("nvCellStates", ctypes.c_longlong),  # bitwise OR of the NvCellState enum values.
-		("rowNumber", ctypes.c_long),
-		("rowSpan", ctypes.c_long),
-		("columnNumber", ctypes.c_long),
-		("columnSpan", ctypes.c_long),
-		("outlineLevel", ctypes.c_long),
-		("comments", comtypes.BSTR),
-		("formula", comtypes.BSTR),
-	]
-
-
 class ExcelCellInfoQuickNavItem(browseMode.QuickNavItem):
 	def __init__(self, parentIterator, cellInfo):
 		self.excelCellInfo = cellInfo
@@ -1576,7 +1572,7 @@ def iterate(self):
 		if not collectionObject:
 			return
 		count = collectionObject.count
-		cellInfos = (ExcelCellInfo * count)()
+		cellInfos = (EXCEL_CELLINFO * count)()
 		numCellsFetched = ctypes.c_long()
 		address = collectionObject.address(True, True, xlA1, True)
 		NVDAHelper.localLib.nvdaInProcUtils_excel_getCellInfos(
@@ -1613,13 +1609,13 @@ def collectionFromWorksheet(self, worksheetObject):
 
 
 class ExcelCell(ExcelBase):
-	excelCellInfo: Optional[ExcelCellInfo]
+	excelCellInfo: EXCEL_CELLINFO | None
 	"""Type info for auto property: _get_excelCellInfo"""
 
-	def _get_excelCellInfo(self) -> Optional[ExcelCellInfo]:
+	def _get_excelCellInfo(self) -> EXCEL_CELLINFO | None:
 		if not self.appModule.helperLocalBindingHandle:
 			return None
-		ci = ExcelCellInfo()
+		ci = EXCEL_CELLINFO()
 		numCellsFetched = ctypes.c_long()
 		address = self.excelCellObject.address(True, True, xlA1, True)
 		res = NVDAHelper.localLib.nvdaInProcUtils_excel_getCellInfos(
@@ -2254,12 +2250,12 @@ def _getFormControlScreenCoordinates(self):
 		# bottom right cell's height in points
 		bottomRightCellHeight = bottomRightAddress.Height
 		self.excelApplicationObject = self.parent.excelWorksheetObject.Application
-		hDC = ctypes.windll.user32.GetDC(None)
+		hDC = user32.GetDC(None)
 		# pixels per inch along screen width
-		px = ctypes.windll.gdi32.GetDeviceCaps(hDC, LOGPIXELSX)
+		px = winBindings.gdi32.GetDeviceCaps(hDC, LOGPIXELSX)
 		# pixels per inch along screen height
-		py = ctypes.windll.gdi32.GetDeviceCaps(hDC, LOGPIXELSY)
-		ctypes.windll.user32.ReleaseDC(None, hDC)
+		py = winBindings.gdi32.GetDeviceCaps(hDC, LOGPIXELSY)
+		user32.ReleaseDC(None, hDC)
 		zoom = self.excelApplicationObject.ActiveWindow.Zoom
 		zoomRatio = zoom / 100
 		# Conversion from inches to Points, 1 inch=72points

```