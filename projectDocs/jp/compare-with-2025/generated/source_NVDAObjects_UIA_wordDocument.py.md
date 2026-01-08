# Diff for: `source\NVDAObjects\UIA\wordDocument.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\UIA\wordDocument.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\UIA\wordDocument.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\UIA\\wordDocument.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\UIA\\wordDocument.py"
index 3083a84..c160ddf 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\UIA\\wordDocument.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\UIA\\wordDocument.py"
@@ -1,7 +1,7 @@
-# This file is covered by the GNU General Public License.
 # A part of NonVisual Desktop Access (NVDA)
-# See the file COPYING for more details.
-# Copyright (C) 2016-2025 NV Access Limited, Joseph Lee, Jakub Lukowicz, Cyrille Bougot
+# Copyright (C) 2016-2025 NV Access Limited, Joseph Lee, Jakub Lukowicz, Cyrille Bougot, Leonard de Ruijter
+# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
+# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
 
 from typing import (
 	Optional,
@@ -74,6 +74,9 @@ class ElementsListDialog(browseMode.ElementsListDialog):
 		# Translators: The label of a radio button to select the type of element
 		# in the browse mode Elements List dialog.
 		("error", _("&Errors")),
+		# Translators: The label of a radio button to select the type of element
+		# in the browse mode Elements List dialog.
+		("reference", _("&References")),
 	)
 
 
@@ -99,6 +102,55 @@ def label(self):
 			return _("track change: {text}").format(text=text)
 
 
+def getReferenceFromPosition(position: "WordDocumentTextInfo") -> UIA | None:
+	"""
+	Fetches reference (footnote/endnote) for the reference located at the given position in a word document.
+	:param position: a TextInfo representing the span of the reference in the word document.
+	:return: The reference NVDAObject, if any
+	"""
+	val = position._rangeObj.getAttributeValue(UIAHandler.UIA_AnnotationObjectsAttributeId)
+	if not val:
+		return None
+	try:
+		UIAElementArray = val.QueryInterface(UIAHandler.IUIAutomationElementArray)
+	except COMError:
+		return None
+	for index in range(UIAElementArray.length):
+		UIAElement = UIAElementArray.getElement(index)
+		UIAElement = UIAElement.buildUpdatedCache(UIAHandler.handler.baseCacheRequest)
+		typeID = UIAElement.GetCurrentPropertyValue(UIAHandler.UIA_AnnotationAnnotationTypeIdPropertyId)
+		# Use Annotation Type Footnote or Endnote if available
+		if typeID in (UIAHandler.UIA.AnnotationType_Footnote, UIAHandler.UIA.AnnotationType_Endnote):
+			return UIA(UIAElement=UIAElement)
+	return None
+
+
+class ReferenceUIATextInfoQuickNavItem(TextAttribUIATextInfoQuickNavItem):
+	attribID = UIAHandler.UIA_AnnotationTypesAttributeId
+	wantedAttribValues = {UIAHandler.AnnotationType_Footnote, UIAHandler.AnnotationType_Endnote}
+
+	@property
+	def label(self) -> str:
+		obj = getReferenceFromPosition(self.textInfo)
+		if obj:
+			text = obj.UIATextPattern.DocumentRange.GetText(-1).strip()
+			match obj.UIAElement.GetCurrentPropertyValue(UIAHandler.UIA_AnnotationAnnotationTypeIdPropertyId):
+				case UIAHandler.UIA.AnnotationType_Footnote:
+					# Translators: The label shown for a footnote in the NVDA Elements List dialog in Microsoft Word.
+					# {text} will be replaced with the text of the footnote.
+					return _("footnote reference: {text}").format(text=text)
+				case UIAHandler.UIA.AnnotationType_Endnote:
+					# Translators: The label shown for an endnote in the NVDA Elements List dialog in Microsoft Word.
+					# {text} will be replaced with the text of the endnote.
+					return _("endnote reference: {text}").format(text=text)
+				case _:
+					log.error("Unknown reference annotation type")
+			name = self.textInfo._rangeObj.GetEnclosingElement().CurrentName
+			# Translators: The label shown for a reference in the NVDA Elements List dialog in Microsoft Word.
+			# {name} will be replaced with the name of the reference.
+			return _("reference: {name}").format(name=name)
+
+
 def getCommentInfoFromPosition(position):
 	"""
 	Fetches information about the comment located at the given position in a word document.
@@ -223,7 +275,13 @@ def _getTextWithFields_text(self, textRange, formatConfig, UIAFormatUnits=None):
 	def _get_controlFieldNVDAObjectClass(self):
 		return WordDocumentNode
 
-	def _getControlFieldForUIAObject(self, obj, isEmbedded=False, startOfNode=False, endOfNode=False):
+	def _getControlFieldForUIAObject(
+		self,
+		obj: "WordDocumentNode",
+		isEmbedded=False,
+		startOfNode=False,
+		endOfNode=False,
+	):
 		# Ignore strange editable text fields surrounding most inner fields (links, table cells etc)
 		automationId = obj.UIAAutomationId
 		field = super(WordDocumentTextInfo, self)._getControlFieldForUIAObject(
@@ -354,10 +412,10 @@ def getTextWithFields(  # noqa: C901
 			return fields
 
 		# MS Word tries to produce speakable math content within equations.
-		# However, using mathPlayer with the exposed mathml property on the equation is much nicer.
+		# However, using math presentation providers with the exposed mathml property on the equation is much nicer.
 		# But, we therefore need to remove the inner math content if reading by line
 		if not formatConfig or not formatConfig.get("extraDetail"):
-			# We really only want to remove content if we can guarantee that mathPlayer is available.
+			# We really only want to remove content if we can guarantee that a math presentation provider is available.
 			if mathPres.speechProvider or mathPres.brailleProvider:
 				curLevel = 0
 				mathLevel = None
@@ -543,7 +601,7 @@ def _shouldSetFocusToObj(self, obj: NVDAObject) -> bool:
 		):
 			return False
 		elif obj.role == controlTypes.Role.MATH:
-			# Don't set focus to math equations otherwise they cannot be interacted  with mathPlayer.
+			# Don't set focus to math equations otherwise they cannot be interacted  with by math presentation providers.
 			return False
 		return super()._shouldSetFocusToObj(obj)
 
@@ -554,7 +612,7 @@ def shouldPassThrough(self, obj, reason=None):
 		):
 			return False
 		elif obj.role == controlTypes.Role.MATH:
-			# Don't  activate focus mode for math equations otherwise they cannot be interacted  with mathPlayer.
+			# Don't  activate focus mode for math equations otherwise they cannot be interacted  with by math presentation providers.
 			return False
 		return super(WordBrowseModeDocument, self).shouldPassThrough(obj, reason=reason)
 
@@ -587,6 +645,14 @@ def _iterNodesByType(self, nodeType, direction="next", pos=None):
 				direction=direction,
 			)
 			return browseMode.mergeQuickNavItemIterators([comments, revisions], direction)
+		elif nodeType == "reference":
+			return UIATextAttributeQuicknavIterator(
+				ReferenceUIATextInfoQuickNavItem,
+				nodeType,
+				self,
+				pos,
+				direction=direction,
+			)
 		return super(WordBrowseModeDocument, self)._iterNodesByType(nodeType, direction=direction, pos=pos)
 
 	ElementsListDialog = ElementsListDialog
@@ -616,7 +682,7 @@ def _get_role(self):
 		if self.mathMl:
 			return controlTypes.Role.MATH
 		role = super(WordDocumentNode, self).role
-		# Footnote / endnote elements currently have a role of unknown. Force them to editableText so that theyr text is presented correctly
+		# Some elements have a role of unknown. Force them to editableText so that their text is presented correctly
 		if role == controlTypes.Role.UNKNOWN:
 			role = controlTypes.Role.EDITABLETEXT
 		return role

```