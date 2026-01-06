# Diff for: `jptools\pack_kgs_addon.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\jptools\pack_kgs_addon.py`  
**Current**: `F:\nvda\gh\alphajp\jptools\pack_kgs_addon.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\pack_kgs_addon.py" "b/F:\\nvda\\gh\\alphajp\\jptools\\pack_kgs_addon.py"
index f4887ef6b3..4872200c21 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\pack_kgs_addon.py"
+++ "b/F:\\nvda\\gh\\alphajp\\jptools\\pack_kgs_addon.py"
@@ -7,66 +7,72 @@
 
 
 def add_to_zip(zf: zipfile.ZipFile, path: Path, arc_prefix: str = "") -> None:
-    if path.is_file():
-        zf.write(path, os.path.join(arc_prefix, path.name))
-        return
-    for root, _, files in os.walk(path):
-        root_p = Path(root)
-        for fn in files:
-            fp = root_p / fn
-            rel = fp.relative_to(path)
-            zf.write(fp, os.path.join(arc_prefix, rel.as_posix()))
+	if path.is_file():
+		zf.write(path, os.path.join(arc_prefix, path.name))
+		return
+	for root, _, files in os.walk(path):
+		root_p = Path(root)
+		for fn in files:
+			fp = root_p / fn
+			rel = fp.relative_to(path)
+			zf.write(fp, os.path.join(arc_prefix, rel.as_posix()))
 
 
 def main() -> int:
-    parser = argparse.ArgumentParser(description="Pack KGS braille addon without 7z")
-    parser.add_argument("--version", default=os.environ.get("VERSION") or os.environ.get("KGSVERSION"))
-    args = parser.parse_args()
+	parser = argparse.ArgumentParser(description="Pack KGS braille addon without 7z")
+	parser.add_argument("--version", default=os.environ.get("VERSION") or os.environ.get("KGSVERSION"))
+	args = parser.parse_args()
 
-    repo_root = Path(__file__).resolve().parents[1]
-    source_dir = repo_root / "source"
-    jptools_dir = repo_root / "jptools"
-    manifest_path = source_dir / "manifest.ini"
+	repo_root = Path(__file__).resolve().parents[1]
+	source_dir = repo_root / "source"
+	jptools_dir = repo_root / "jptools"
+	manifest_path = source_dir / "manifest.ini"
 
-    version = args.version
-    if not version:
-        from datetime import datetime
+	version = args.version
+	if not version:
+		from datetime import datetime
 
-        version = datetime.now().strftime("%y%m%d")
+		version = datetime.now().strftime("%y%m%d")
 
-    # Generate manifest.ini using the existing helper to stay consistent
-    try:
-        subprocess.check_call([
-            sys.executable,
-            str(jptools_dir / "kgs_manifest.py"),
-            version,
-            str(manifest_path),
-        ])
-    except subprocess.CalledProcessError as e:
-        print(f"Failed to generate manifest.ini: {e}", file=sys.stderr)
-        return e.returncode
+	# Generate manifest.ini using the existing helper to stay consistent
+	try:
+		subprocess.check_call(
+			[
+				sys.executable,
+				str(jptools_dir / "kgs_manifest.py"),
+				version,
+				str(manifest_path),
+			]
+		)
+	except subprocess.CalledProcessError as e:
+		print(f"Failed to generate manifest.ini: {e}", file=sys.stderr)
+		return e.returncode
 
-    out_zip = jptools_dir / f"kgsbraille-{version}.nvda-addon"
-    try:
-        with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
-            # manifest
-            zf.write(manifest_path, "manifest.ini")
-            # files
-            zf.write(source_dir / "brailleDisplayDrivers" / "kgs.py", "brailleDisplayDrivers/kgs.py")
-            zf.write(source_dir / "brailleDisplayDrivers" / "brailleMemo.py", "brailleDisplayDrivers/brailleMemo.py")
-            zf.write(source_dir / "brailleDisplayDrivers" / "DirectBM.dll", "brailleDisplayDrivers/DirectBM.dll")
-    finally:
-        # Clean up the generated manifest
-        try:
-            if manifest_path.exists():
-                manifest_path.unlink()
-        except Exception:
-            pass
+	out_zip = jptools_dir / f"kgsbraille-{version}.nvda-addon"
+	try:
+		with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
+			# manifest
+			zf.write(manifest_path, "manifest.ini")
+			# files
+			zf.write(source_dir / "brailleDisplayDrivers" / "kgs.py", "brailleDisplayDrivers/kgs.py")
+			zf.write(
+				source_dir / "brailleDisplayDrivers" / "brailleMemo.py",
+				"brailleDisplayDrivers/brailleMemo.py",
+			)
+			zf.write(
+				source_dir / "brailleDisplayDrivers" / "DirectBM.dll", "brailleDisplayDrivers/DirectBM.dll"
+			)
+	finally:
+		# Clean up the generated manifest
+		try:
+			if manifest_path.exists():
+				manifest_path.unlink()
+		except Exception:
+			pass
 
-    print(str(out_zip))
-    return 0
+	print(str(out_zip))
+	return 0
 
 
 if __name__ == "__main__":
-    raise SystemExit(main())
-
+	raise SystemExit(main())

```