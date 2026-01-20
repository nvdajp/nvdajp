import argparse
import os
import subprocess
import sys
import zipfile
from pathlib import Path


def add_to_zip(zf: zipfile.ZipFile, path: Path, arc_prefix: str = "") -> None:
	if path.is_file():
		zf.write(path, os.path.join(arc_prefix, path.name))
		return
	for root, _, files in os.walk(path):
		root_p = Path(root)
		for fn in files:
			fp = root_p / fn
			rel = fp.relative_to(path)
			zf.write(fp, os.path.join(arc_prefix, rel.as_posix()))


def main() -> int:
	parser = argparse.ArgumentParser(description="Pack KGS braille addon without 7z")
	parser.add_argument("--version", default=os.environ.get("VERSION") or os.environ.get("KGSVERSION"))
	args = parser.parse_args()

	repo_root = Path(__file__).resolve().parents[1]
	source_dir = repo_root / "source"
	jptools_dir = repo_root / "jptools"
	manifest_path = source_dir / "manifest.ini"

	version = args.version
	if not version:
		from datetime import datetime

		version = datetime.now().strftime("%y%m%d")

	# Generate manifest.ini using the existing helper to stay consistent
	try:
		subprocess.check_call(
			[
				sys.executable,
				str(jptools_dir / "kgs_manifest.py"),
				version,
				str(manifest_path),
			],
		)
	except subprocess.CalledProcessError as e:
		print(f"Failed to generate manifest.ini: {e}", file=sys.stderr)
		return e.returncode

	out_zip = jptools_dir / f"kgsbraille-{version}.nvda-addon"
	try:
		with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
			# manifest
			zf.write(manifest_path, "manifest.ini")
			# files
			zf.write(source_dir / "brailleDisplayDrivers" / "kgs.py", "brailleDisplayDrivers/kgs.py")
			zf.write(
				source_dir / "brailleDisplayDrivers" / "brailleMemo.py",
				"brailleDisplayDrivers/brailleMemo.py",
			)
			zf.write(
				source_dir / "brailleDisplayDrivers" / "DirectBM.dll",
				"brailleDisplayDrivers/DirectBM.dll",
			)
	finally:
		# Clean up the generated manifest
		try:
			if manifest_path.exists():
				manifest_path.unlink()
		except Exception:
			pass

	print(str(out_zip))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
