# Diff for: `source\NVDAObjects\window\winword.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\window\winword.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\window\winword.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\window\\winword.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\window\\winword.py"
index b61ffd7..10bd66d 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\window\\winword.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\window\\winword.py"
@@ -1,8 +1,8 @@
 # A part of NonVisual Desktop Access (NVDA)
 # Copyright (C) 2006-2025 NV Access Limited, Manish Agrawal, Derek Riemer, Babbage B.V., Cyrille Bougot,
 # Leonard de Ruijter
-# This file is covered by the GNU General Public License.
-# See the file COPYING for more details.
+# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
+# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
 
 
 import ctypes
@@ -14,7 +14,6 @@
 	Self,
 	TYPE_CHECKING,
 )
-
 from comtypes import COMError, GUID, BSTR
 import comtypes.client
 import comtypes.automation
@@ -28,6 +27,7 @@
 import NVDAHelper
 import XMLFormatting
 from logHandler import log
+from winBindings import user32
 import winUser
 import oleacc
 import speech
@@ -471,7 +471,7 @@ class WinWordColor(IntEnum):
 
 winwordWindowIid = GUID("{00020962-0000-0000-C000-000000000046}")
 
-wm_winword_expandToLine = ctypes.windll.user32.RegisterWindowMessageW("wm_winword_expandToLine")
+wm_winword_expandToLine = user32.RegisterWindowMessage("wm_winword_expandToLine")
 
 NVDAUnitsToWordUnits = {
 	textInfos.UNIT_CHARACTER: wdCharacter,
@@ -634,6 +634,36 @@ def label(self):
 		return _("spelling: {text}").format(text=text)
 
 
+class WordDocumentReferenceQuickNavItem(WordDocumentCollectionQuickNavItem):
+	def rangeFromCollectionItem(
+		self,
+		item: comtypes.client.lazybind.Dispatch,
+	) -> comtypes.client.lazybind.Dispatch:
+		return item.reference
+
+
+class WordDocumentFootnoteQuickNavItem(WordDocumentReferenceQuickNavItem):
+	@property
+	def label(self) -> str:
+		number = self.collectionItem.index
+		text = self.collectionItem.range.text
+		# Translators: The label shown for a footnote reference in the NVDA Elements List dialog in Microsoft Word.
+		# {number} will be replaced with the footnote number.
+		# {text} will be replaced with the text in the footnote.
+		return _("footnote reference {number}: {text}").format(number=number, text=text)
+
+
+class WordDocumentEndnoteQuickNavItem(WordDocumentReferenceQuickNavItem):
+	@property
+	def label(self) -> str:
+		number = self.collectionItem.index
+		text = self.collectionItem.range.text
+		# Translators: The label shown for a endnote reference in the NVDA Elements List dialog in Microsoft Word.
+		# {number} will be replaced with the endnote number.
+		# {text} will be replaced with the text in the footnote.
+		return _("endnote reference {number}: {text}").format(number=number, text=text)
+
+
 class WinWordCollectionQuicknavIterator(object):
 	"""
 	Allows iterating over an MS Word collection (e.g. HyperLinks) emitting L{QuickNavItem} objects.
@@ -752,6 +782,23 @@ def collectionFromRange(self, rangeObj):
 		return rangeObj.spellingErrors
 
 
+class FootnoteWinWordCollectionQuicknavIterator(WinWordCollectionQuicknavIterator):
+	quickNavItemClass = WordDocumentFootnoteQuickNavItem
+
+	def collectionFromRange(
+		self,
+		rangeObj: comtypes.client.lazybind.Dispatch,
+	) -> comtypes.client.lazybind.Dispatch:
+		return rangeObj.footnotes
+
+
+class EndnoteWinWordCollectionQuicknavIterator(WinWordCollectionQuicknavIterator):
+	quickNavItemClass = WordDocumentEndnoteQuickNavItem
+
+	def collectionFromRange(self, rangeObj):
+		return rangeObj.endnotes
+
+
 class GraphicWinWordCollectionQuicknavIterator(WinWordCollectionQuicknavIterator):
 	def collectionFromRange(self, rangeObj):
 		return rangeObj.inlineShapes
@@ -1522,6 +1569,22 @@ def _iterNodesByType(self, nodeType, direction="next", pos=None):
 				rangeObj,
 				includeCurrent,
 			).iterate()
+		elif nodeType == "reference":
+			footnotes = FootnoteWinWordCollectionQuicknavIterator(
+				nodeType,
+				self,
+				direction,
+				rangeObj,
+				includeCurrent,
+			).iterate()
+			endnotes = EndnoteWinWordCollectionQuicknavIterator(
+				nodeType,
+				self,
+				direction,
+				rangeObj,
+				includeCurrent,
+			).iterate()
+			return browseMode.mergeQuickNavItemIterators([footnotes, endnotes], direction)
 		elif nodeType == "graphic":
 			return GraphicWinWordCollectionQuicknavIterator(
 				nodeType,
@@ -2160,4 +2223,7 @@ class ElementsListDialog(browseMode.ElementsListDialog):
 		# Translators: The label of a radio button to select the type of element
 		# in the browse mode Elements List dialog.
 		("error", _("&Errors")),
+		# Translators: The label of a radio button to select the type of element
+		# in the browse mode Elements List dialog.
+		("reference", _("&References")),
 	)

```