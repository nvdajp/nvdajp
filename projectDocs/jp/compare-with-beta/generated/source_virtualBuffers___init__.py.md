# Diff for: `source\virtualBuffers\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\virtualBuffers\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\virtualBuffers\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\virtualBuffers\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\virtualBuffers\\__init__.py"
index 74e8f7c..97def79 100644
--- "a/F:\\nvda\\gh\\beta\\source\\virtualBuffers\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\virtualBuffers\\__init__.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2007-2025 NV Access Limited, Peter Vágner, Cyrille Bougot, Leonard de Ruijter
-# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
-# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
+# This file is covered by the GNU General Public License.
+# See the file COPYING for more details.
+# Copyright (C) 2007-2025 NV Access Limited, Peter Vágner, Cyrille Bougot
 
 import time
 import threading
@@ -149,9 +149,7 @@ def isChild(self, parent):
 
 
 class VirtualBufferTextInfo(browseMode.BrowseModeDocumentTextInfo, textInfos.offsets.OffsetsTextInfo):
-	def allowMoveToUnitOffsetPastEnd(self, unit: str) -> bool:
-		"""Virtual buffers have no insertion point, so no need to move past the end of text."""
-		return False
+	allowMoveToOffsetPastEnd = False  #: no need for end insertion point as vbuf is not editable.
 
 	def _getControlFieldAttribs(self, docHandle, id):
 		info = self.copy()

```