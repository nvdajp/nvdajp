# Diff for: `jptools\pack_kgs_addon.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\jptools\pack_kgs_addon.py`  
**Current**: `F:\nvda\gh\alphajp\jptools\pack_kgs_addon.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\pack_kgs_addon.py" "b/F:\\nvda\\gh\\alphajp\\jptools\\pack_kgs_addon.py"
index f4887ef6b3..4872200c21 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\pack_kgs_addon.py"
+++ "b/F:\\nvda\\gh\\alphajp\\jptools\\pack_kgs_addon.py"
@@ -36,12 +36,14 @@ def main() -> int:
 
 	# Generate manifest.ini using the existing helper to stay consistent
 	try:
-        subprocess.check_call([
+		subprocess.check_call(
+			[
 				sys.executable,
 				str(jptools_dir / "kgs_manifest.py"),
 				version,
 				str(manifest_path),
-        ])
+			]
+		)
 	except subprocess.CalledProcessError as e:
 		print(f"Failed to generate manifest.ini: {e}", file=sys.stderr)
 		return e.returncode
@@ -53,8 +55,13 @@ def main() -> int:
 			zf.write(manifest_path, "manifest.ini")
 			# files
 			zf.write(source_dir / "brailleDisplayDrivers" / "kgs.py", "brailleDisplayDrivers/kgs.py")
-            zf.write(source_dir / "brailleDisplayDrivers" / "brailleMemo.py", "brailleDisplayDrivers/brailleMemo.py")
-            zf.write(source_dir / "brailleDisplayDrivers" / "DirectBM.dll", "brailleDisplayDrivers/DirectBM.dll")
+			zf.write(
+				source_dir / "brailleDisplayDrivers" / "brailleMemo.py",
+				"brailleDisplayDrivers/brailleMemo.py",
+			)
+			zf.write(
+				source_dir / "brailleDisplayDrivers" / "DirectBM.dll", "brailleDisplayDrivers/DirectBM.dll"
+			)
 	finally:
 		# Clean up the generated manifest
 		try:
@@ -69,4 +76,3 @@ def main() -> int:
 
 if __name__ == "__main__":
 	raise SystemExit(main())
-

```