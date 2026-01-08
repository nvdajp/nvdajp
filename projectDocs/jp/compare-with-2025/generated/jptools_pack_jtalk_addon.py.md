# Diff for: `jptools\pack_jtalk_addon.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\jptools\pack_jtalk_addon.py`  
**Current**: `F:\nvda\gh\alphajp-260109\jptools\pack_jtalk_addon.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\pack_jtalk_addon.py" "b/F:\\nvda\\gh\\alphajp-260109\\jptools\\pack_jtalk_addon.py"
index 93488f5..1079c22 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\pack_jtalk_addon.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\jptools\\pack_jtalk_addon.py"
@@ -37,12 +37,14 @@ def main() -> int:
 
 	# Generate manifest.ini using the existing helper to stay consistent
 	try:
-        subprocess.check_call([
+		subprocess.check_call(
+			[
 				sys.executable,
 				str(jptools_dir / "jtalk_manifest.py"),
 				nowdate,
 				str(manifest_path),
-        ])
+			]
+		)
 	except subprocess.CalledProcessError as e:
 		print(f"Failed to generate manifest.ini: {e}", file=sys.stderr)
 		return e.returncode
@@ -73,4 +75,3 @@ def main() -> int:
 
 if __name__ == "__main__":
 	raise SystemExit(main())
-

```