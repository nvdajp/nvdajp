# Diff for: `source\compoundDocuments.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\compoundDocuments.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\compoundDocuments.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\compoundDocuments.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\compoundDocuments.py"
index c2fe19e..1e24efb 100644
--- "a/F:\\nvda\\gh\\beta\\source\\compoundDocuments.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\compoundDocuments.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2010-2025 NV Access Limited, Bram Duvigneau, Leonard de Ruijter
-# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
-# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
+# This file is covered by the GNU General Public License.
+# See the file COPYING for more details.
+# Copyright (C) 2010-2024 NV Access Limited, Bram Duvigneau
 
 from typing import (
 	Optional,
@@ -12,7 +12,6 @@
 import textUtils
 import winUser
 import textInfos
-import textInfos.offsets
 import controlTypes
 import eventHandler
 from NVDAObjects import NVDAObject
@@ -504,15 +503,6 @@ def _get_boundingRects(self):
 		return rects
 
 
-class CompoundTextLeafTextInfo(textInfos.offsets.OffsetsTextInfo):
-	"""A mixin class for leafs within a CompoundTextInfo that utilize offsets.
-	It ensures that moving past the end of the object is only allowed for certain units.
-	"""
-
-	def allowMoveToUnitOffsetPastEnd(self, unit: str) -> bool:
-		return unit in (textInfos.UNIT_CHARACTER, textInfos.UNIT_WORD) or not self.obj.flowsTo
-
-
 class CompoundDocument(EditableText, DocumentTreeInterceptor):
 	TextInfo = TreeCompoundTextInfo
 

```