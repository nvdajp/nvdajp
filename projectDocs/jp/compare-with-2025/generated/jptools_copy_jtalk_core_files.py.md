# Diff for: `jptools\copy_jtalk_core_files.py`

**Source**: `F:\nvda\gh\alphajp-251219\jptools\copy_jtalk_core_files.py`  
**Current**: `F:\nvda\gh\alphajp-260109\jptools\copy_jtalk_core_files.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\copy_jtalk_core_files.py" "b/F:\\nvda\\gh\\alphajp-260109\\jptools\\copy_jtalk_core_files.py"
index 8ea82a6..a9abe3f 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\copy_jtalk_core_files.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\jptools\\copy_jtalk_core_files.py"
@@ -3,6 +3,7 @@
 
 This script replaces copy_jtalk_core_files.cmd and can be called from .cmd files.
 """
+
 import sys
 from pathlib import Path
 
@@ -12,6 +13,7 @@
 
 try:
 	from scons_jp import _copy_jtalk_core_files
+
 	exit_code = _copy_jtalk_core_files(repo_root)
 	sys.exit(exit_code)
 except ImportError as e:

```