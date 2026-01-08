# Diff for: `source\winAPI\constants.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\winAPI\constants.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winAPI\constants.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winAPI\\constants.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winAPI\\constants.py"
index 41e60a3..e748a49 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winAPI\\constants.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winAPI\\constants.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2022-2024 NV Access Limited
+# Copyright (C) 2022-2025 NV Access Limited
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -31,5 +31,9 @@ class SystemErrorCodes(enum.IntEnum):
 	SHARING_VIOLATION = 0x20
 	"""The process cannot access the file because it is being used by another process."""
 	INVALID_PARAMETER = 0x57
+	INSUFFICIENT_BUFFER = 0x7A
+	"""The data area passed to a system call is too small."""
 	MOD_NOT_FOUND = 0x7E
+	NO_MORE_ITEMS = 0x103
+	"""No more data is available."""
 	CANCELLED = 0x4C7

```