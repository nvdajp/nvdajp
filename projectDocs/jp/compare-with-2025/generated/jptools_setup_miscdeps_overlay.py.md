# Diff for: `jptools\setup_miscdeps_overlay.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\jptools\setup_miscdeps_overlay.py`  
**Current**: `F:\nvda\gh\alphajp\jptools\setup_miscdeps_overlay.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\setup_miscdeps_overlay.py" "b/F:\\nvda\\gh\\alphajp\\jptools\\setup_miscdeps_overlay.py"
index 7fa9cb01e9..1dfc8f21f0 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\setup_miscdeps_overlay.py"
+++ "b/F:\\nvda\\gh\\alphajp\\jptools\\setup_miscdeps_overlay.py"
@@ -4,40 +4,44 @@
 
 
 def overlay_copy(src: Path, dst: Path) -> None:
-    for root, dirs, files in os.walk(src):
-        r = Path(root)
-        rel = r.relative_to(src)
-        target_dir = dst / rel
-        target_dir.mkdir(parents=True, exist_ok=True)
-        for f in files:
-            s = r / f
-            d = target_dir / f
-            try:
-                # If destination exists and is identical, skip copy
-                if d.exists() and d.stat().st_mtime >= s.stat().st_mtime and d.stat().st_size == s.stat().st_size:
-                    continue
-                shutil.copy2(s, d)
-            except (PermissionError, OSError) as e:
-                # If file is locked or permission denied, log warning and continue
-                # This can happen when comInterfaces generates files that are still in use
-                print(f"Warning: Could not copy {s} to {d}: {e}")
-                print("  Skipping this file (may be locked by another process)")
-                continue
+	for root, dirs, files in os.walk(src):
+		r = Path(root)
+		rel = r.relative_to(src)
+		target_dir = dst / rel
+		target_dir.mkdir(parents=True, exist_ok=True)
+		for f in files:
+			s = r / f
+			d = target_dir / f
+			try:
+				# If destination exists and is identical, skip copy
+				if (
+					d.exists()
+					and d.stat().st_mtime >= s.stat().st_mtime
+					and d.stat().st_size == s.stat().st_size
+				):
+					continue
+				shutil.copy2(s, d)
+			except (PermissionError, OSError) as e:
+				# If file is locked or permission denied, log warning and continue
+				# This can happen when comInterfaces generates files that are still in use
+				print(f"Warning: Could not copy {s} to {d}: {e}")
+				print("  Skipping this file (may be locked by another process)")
+				continue
 
 
 def main() -> int:
-    # This script is intended to be run from repoRoot/miscDepsJp
-    cwd = Path.cwd()
-    src = cwd / "source"
-    # Destination is the repository root 'source' directory
-    dst = cwd.parent / "source"
+	# This script is intended to be run from repoRoot/miscDepsJp
+	cwd = Path.cwd()
+	src = cwd / "source"
+	# Destination is the repository root 'source' directory
+	dst = cwd.parent / "source"
 
-    # Copy all files under miscDepsJp/source as-is into repo source.
-    # Any content policy (e.g. not placing espeak-data here) is enforced at repo level.
+	# Copy all files under miscDepsJp/source as-is into repo source.
+	# Any content policy (e.g. not placing espeak-data here) is enforced at repo level.
 
-    overlay_copy(src, dst)
-    return 0
+	overlay_copy(src, dst)
+	return 0
 
 
 if __name__ == "__main__":
-    raise SystemExit(main())
+	raise SystemExit(main())

```