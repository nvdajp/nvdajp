# Diff for: `jptools\copy_jtalk_core_files.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\jptools\copy_jtalk_core_files.py`  
**Current**: `F:\nvda\gh\alphajp\jptools\copy_jtalk_core_files.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\copy_jtalk_core_files.py" "b/F:\\nvda\\gh\\alphajp\\jptools\\copy_jtalk_core_files.py"
index 8ea82a62c5..a9abe3fdd6 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\copy_jtalk_core_files.py"
+++ "b/F:\\nvda\\gh\\alphajp\\jptools\\copy_jtalk_core_files.py"
@@ -3,6 +3,7 @@
 
 This script replaces copy_jtalk_core_files.cmd and can be called from .cmd files.
 """
+
 import sys
 from pathlib import Path
 
@@ -11,12 +12,13 @@
 sys.path.insert(0, str(repo_root / "jptools"))
 
 try:
-    from scons_jp import _copy_jtalk_core_files
-    exit_code = _copy_jtalk_core_files(repo_root)
-    sys.exit(exit_code)
+	from scons_jp import _copy_jtalk_core_files
+
+	exit_code = _copy_jtalk_core_files(repo_root)
+	sys.exit(exit_code)
 except ImportError as e:
-    print(f"Error: Failed to import scons_jp: {e}", file=sys.stderr)
-    sys.exit(1)
+	print(f"Error: Failed to import scons_jp: {e}", file=sys.stderr)
+	sys.exit(1)
 except Exception as e:
-    print(f"Error: {e}", file=sys.stderr)
-    sys.exit(1)
+	print(f"Error: {e}", file=sys.stderr)
+	sys.exit(1)

```