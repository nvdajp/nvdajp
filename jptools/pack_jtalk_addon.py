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
	parser = argparse.ArgumentParser(description="Pack nvdajp jtalk addon without 7z")
	parser.add_argument("--nowdate", default=os.environ.get("VERSION") or os.environ.get("NOWDATE"))
	args = parser.parse_args()

	repo_root = Path(__file__).resolve().parents[1]
	source_dir = repo_root / "source"
	jptools_dir = repo_root / "jptools"
	manifest_path = source_dir / "manifest.ini"

	nowdate = args.nowdate
	if not nowdate:
		# Fallback to yymmdd style if not provided
		from datetime import datetime

		nowdate = datetime.now().strftime("%y%m%d")

	# Generate manifest.ini using the existing helper to stay consistent
	try:
		subprocess.check_call(
			[
				sys.executable,
				str(jptools_dir / "jtalk_manifest.py"),
				nowdate,
				str(manifest_path),
			],
		)
	except subprocess.CalledProcessError as e:
		print(f"Failed to generate manifest.ini: {e}", file=sys.stderr)
		return e.returncode

	out_zip = jptools_dir / f"nvdajp-jtalk-{nowdate}.nvda-addon"
	synth_dir = source_dir / "synthDrivers"
	try:
		with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
			# manifest
			zf.write(manifest_path, "manifest.ini")
			# top-level nvdajp*.py in synthDrivers
			for p in synth_dir.glob("nvdajp*.py"):
				zf.write(p, f"synthDrivers/{p.name}")
			# jtalk subdirectory
			jtalk_dir = synth_dir / "jtalk"
			add_to_zip(zf, jtalk_dir, arc_prefix="synthDrivers/jtalk")
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
