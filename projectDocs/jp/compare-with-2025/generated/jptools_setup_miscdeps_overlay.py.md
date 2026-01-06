# Diff for: `jptools\setup_miscdeps_overlay.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\jptools\setup_miscdeps_overlay.py`  
**Current**: `F:\nvda\gh\alphajp\jptools\setup_miscdeps_overlay.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\setup_miscdeps_overlay.py" "b/F:\\nvda\\gh\\alphajp\\jptools\\setup_miscdeps_overlay.py"
index 7fa9cb01e9..1dfc8f21f0 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\setup_miscdeps_overlay.py"
+++ "b/F:\\nvda\\gh\\alphajp\\jptools\\setup_miscdeps_overlay.py"
@@ -14,7 +14,11 @@ def overlay_copy(src: Path, dst: Path) -> None:
 			d = target_dir / f
 			try:
 				# If destination exists and is identical, skip copy
-                if d.exists() and d.stat().st_mtime >= s.stat().st_mtime and d.stat().st_size == s.stat().st_size:
+				if (
+					d.exists()
+					and d.stat().st_mtime >= s.stat().st_mtime
+					and d.stat().st_size == s.stat().st_size
+				):
 					continue
 				shutil.copy2(s, d)
 			except (PermissionError, OSError) as e:

```