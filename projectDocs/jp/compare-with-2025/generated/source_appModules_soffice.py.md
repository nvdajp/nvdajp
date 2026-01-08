# Diff for: `source\appModules\soffice.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\appModules\soffice.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\appModules\soffice.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModules\\soffice.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\soffice.py"
index 0bcd15f..2c6ded0 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModules\\soffice.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\soffice.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
-# This file is covered by the GNU General Public License.
-# See the file COPYING for more details.
 # Copyright (C) 2006-2025 NV Access Limited, Bill Dengler, Leonard de Ruijter, Cyrille Bougot
+# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
+# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
 
 from typing import (
 	Optional,
@@ -18,7 +18,7 @@
 from controlTypes import TextPosition
 import textInfos
 import colors
-from compoundDocuments import CompoundDocument, TreeCompoundTextInfo
+from compoundDocuments import CompoundDocument, TreeCompoundTextInfo, CompoundTextLeafTextInfo
 from NVDAObjects import NVDAObject
 from NVDAObjects.IAccessible import IAccessible, IA2TextTextInfo
 from NVDAObjects.behaviors import EditableText
@@ -55,7 +55,7 @@ def get_id(obj: NVDAObject) -> str | None:
 		return obj.IA2Attributes.get("id")
 
 
-class SymphonyTextInfo(IA2TextTextInfo):
+class SymphonyTextInfo(IA2TextTextInfo, CompoundTextLeafTextInfo):
 	# C901 '_getFormatFieldFromLegacyAttributesString' is too complex
 	# Note: when working on _getFormatFieldFromLegacyAttributesString, look for opportunities to simplify
 	# and move logic out into smaller helper functions.
@@ -237,6 +237,7 @@ def _getLineOffsets(self, offset):
 		if offset == 0 and start == 0 and end == 0:
 			# HACK: Symphony doesn't expose any characters at all on empty lines, but this means we don't ever fetch the list item prefix in this case.
 			# Fake a character so that the list item prefix will be spoken on empty lines.
+			# Note: Observations in LibreOffice revealed that this might no longer be necessary.
 			return (0, 1)
 		return start, end
 

```