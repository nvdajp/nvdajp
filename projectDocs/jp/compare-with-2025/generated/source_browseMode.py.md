# Diff for: `source\browseMode.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\browseMode.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\browseMode.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\browseMode.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\browseMode.py"
index d7549c8..3b2b479 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\browseMode.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\browseMode.py"
@@ -1,8 +1,8 @@
 # A part of NonVisual Desktop Access (NVDA)
 # Copyright (C) 2007-2025 NV Access Limited, Babbage B.V., James Teh, Leonard de Ruijter,
 # Thomas Stivers, Accessolutions, Julien Cochuyt, Cyrille Bougot
-# This file is covered by the GNU General Public License.
-# See the file COPYING for more details.
+# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
+# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
 
 from typing import (
 	Any,
@@ -1221,6 +1221,19 @@ def _get_disableAutoPassThrough(self):
 	# Translators: Message presented when the browse mode element is not found.
 	prevError=_("No previous different style text"),
 )
+qn(
+	"reference",
+	key=None,
+	# Translators: Input help message for a quick navigation command in browse mode.
+	nextDoc=_("moves to the next reference"),
+	# Translators: Message presented when the browse mode element is not found.
+	nextError=_("no next reference"),
+	# Translators: Input help message for a quick navigation command in browse mode.
+	prevDoc=_("moves to the previous reference"),
+	# Translators: Message presented when the browse mode element is not found.
+	prevError=_("no previous reference"),
+	readUnit=textInfos.UNIT_WORD,
+)
 del qn
 
 

```