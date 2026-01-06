# Diff for: `jptools\pack_controller_client.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\jptools\pack_controller_client.py`  
**Current**: `F:\nvda\gh\alphajp\jptools\pack_controller_client.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\pack_controller_client.py" "b/F:\\nvda\\gh\\alphajp\\jptools\\pack_controller_client.py"
index 42609de42d..d885b2925c 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\pack_controller_client.py"
+++ "b/F:\\nvda\\gh\\alphajp\\jptools\\pack_controller_client.py"
@@ -5,59 +5,71 @@
 
 
 def add_path(zipf: ZipFile, base_dir: Path, path: Path) -> None:
-    if path.is_dir():
-        for p in path.rglob('*'):
-            if p.is_file():
-                arcname = p.relative_to(base_dir).as_posix()
-                zipf.write(p, arcname)
-    else:
-        arcname = path.relative_to(base_dir).as_posix()
-        zipf.write(path, arcname)
+	if path.is_dir():
+		for p in path.rglob("*"):
+			if p.is_file():
+				arcname = p.relative_to(base_dir).as_posix()
+				zipf.write(p, arcname)
+	else:
+		arcname = path.relative_to(base_dir).as_posix()
+		zipf.write(path, arcname)
 
 
 def main() -> int:
-    parser = argparse.ArgumentParser(description="Pack NVDA controller client (no 7z)")
-    parser.add_argument('--version', default=os.environ.get('VERSION'), required=False,
-                        help='Version string used for output filename if --output is not given')
-    parser.add_argument('--client-root', default=None,
-                        help='Path to nvdajpClient root (defaults to jptools/nvdajpClient)')
-    parser.add_argument('--output', default=None,
-                        help='Output zip path (defaults to output/nvda_<version>_controllerClientJp.zip)')
-    args = parser.parse_args()
-
-    script_dir = Path(__file__).resolve().parent
-    repo_root = script_dir.parent
-    client_root = Path(args.client_root) if args.client_root else (script_dir / 'nvdajpClient')
-    client_root = client_root.resolve()
-
-    if not client_root.exists():
-        raise SystemExit(f"client root not found: {client_root}")
-
-    if args.output:
-        out_path = Path(args.output)
-    else:
-        version = args.version or 'local'
-        out_path = repo_root / 'output' / f'nvda_{version}_controllerClientJp.zip'
-
-    out_path.parent.mkdir(parents=True, exist_ok=True)
-
-    targets = [
-        'arm64', 'examples', 'x64', 'x86',
-        'license.txt', 'readme.html', 'readmejp.txt',
-    ]
-
-    with ZipFile(out_path, 'w', compression=ZIP_DEFLATED) as zf:
-        for t in targets:
-            p = (client_root / t)
-            if not p.exists():
-                # Skip missing optional targets silently to mirror prior behavior
-                continue
-            add_path(zf, client_root, p)
-
-    print(out_path)
-    return 0
-
-
-if __name__ == '__main__':
-    raise SystemExit(main())
+	parser = argparse.ArgumentParser(description="Pack NVDA controller client (no 7z)")
+	parser.add_argument(
+		"--version",
+		default=os.environ.get("VERSION"),
+		required=False,
+		help="Version string used for output filename if --output is not given",
+	)
+	parser.add_argument(
+		"--client-root", default=None, help="Path to nvdajpClient root (defaults to jptools/nvdajpClient)"
+	)
+	parser.add_argument(
+		"--output",
+		default=None,
+		help="Output zip path (defaults to output/nvda_<version>_controllerClientJp.zip)",
+	)
+	args = parser.parse_args()
 
+	script_dir = Path(__file__).resolve().parent
+	repo_root = script_dir.parent
+	client_root = Path(args.client_root) if args.client_root else (script_dir / "nvdajpClient")
+	client_root = client_root.resolve()
+
+	if not client_root.exists():
+		raise SystemExit(f"client root not found: {client_root}")
+
+	if args.output:
+		out_path = Path(args.output)
+	else:
+		version = args.version or "local"
+		out_path = repo_root / "output" / f"nvda_{version}_controllerClientJp.zip"
+
+	out_path.parent.mkdir(parents=True, exist_ok=True)
+
+	targets = [
+		"arm64",
+		"examples",
+		"x64",
+		"x86",
+		"license.txt",
+		"readme.html",
+		"readmejp.txt",
+	]
+
+	with ZipFile(out_path, "w", compression=ZIP_DEFLATED) as zf:
+		for t in targets:
+			p = client_root / t
+			if not p.exists():
+				# Skip missing optional targets silently to mirror prior behavior
+				continue
+			add_path(zf, client_root, p)
+
+	print(out_path)
+	return 0
+
+
+if __name__ == "__main__":
+	raise SystemExit(main())

```