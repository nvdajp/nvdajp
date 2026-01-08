# Diff for: `tests\unit\objectProvider.py`

**Source**: `F:\nvda\gh\beta\tests\unit\objectProvider.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\unit\objectProvider.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\objectProvider.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\objectProvider.py"
index 43e9382..9f2fa13 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\objectProvider.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\objectProvider.py"
@@ -1,22 +1,19 @@
+# tests/unit/objectProvider.py
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2017-2025 NV Access Limited, Babbage B.V.
-# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
-# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
+# This file is covered by the GNU General Public License.
+# See the file COPYING for more details.
+# Copyright (C) 2017 NV Access Limited, Babbage B.V.
 
 """Fake object provider implementation for testing of code which uses NVDAObjects."""
 
 from NVDAObjects import NVDAObject
 import controlTypes
-from typing import Any
 
 
 class PlaceholderNVDAObject(NVDAObject):
 	processID = None  # Must be implemented to instantiate.
 	windowThreadID = 0  # Must be implemented for inputCore tests
 
-	def _isEqual(self, other: Any) -> bool:
-		return False
-
 
 class NVDAObjectWithRole(PlaceholderNVDAObject):
 	"""An object that accepts a role as one of its construction parameters.

```