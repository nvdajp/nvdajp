# -*- coding: utf-8 -*-
# jptools/syncLibkuraji.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 Takuya Nishimoto
#
# Sync the vendored libkuraji package (source/libkuraji) from a local
# clone of https://github.com/nishimotz/libkuraji (BSD 3-Clause).
# libkuraji is the upstream: make changes there, run its test suite,
# then run this script and commit the result here.
#
# Usage: python miscDepsJp/jptools/syncLibkuraji.py [path-to-libkuraji]

import shutil
import subprocess
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]


def main():
	if len(sys.argv) > 1:
		src_root = Path(sys.argv[1])
	else:
		src_root = repo_root.parent / "libkuraji"
	pkg_src = src_root / "src" / "libkuraji"
	if not (pkg_src / "kana.py").exists():
		print(f"libkuraji package not found under {pkg_src}", file=sys.stderr)
		return 1

	dest = repo_root / "source" / "libkuraji"
	if dest.exists():
		shutil.rmtree(dest)
	dest.mkdir(parents=True)
	copied = []
	for py in sorted(pkg_src.glob("*.py")):
		shutil.copy2(py, dest / py.name)
		copied.append(py.name)
	shutil.copy2(src_root / "LICENSE", dest / "LICENSE")

	try:
		commit = subprocess.run(
			["git", "-C", str(src_root), "rev-parse", "HEAD"],
			capture_output=True,
			text=True,
			check=True,
		).stdout.strip()
	except Exception:
		commit = "unknown"
	(dest / "PROVENANCE.md").write_text(
		"# Vendored copy of libkuraji\n\n"
		"- Upstream: https://github.com/nishimotz/libkuraji (BSD 3-Clause)\n"
		f"- Commit: {commit}\n"
		"- Do not edit here; change upstream and re-run "
		"`python miscDepsJp/jptools/syncLibkuraji.py`.\n",
		encoding="utf-8",
		newline="\n",
	)
	print(f"synced {', '.join(copied)} from {src_root} (commit {commit[:10]}) -> {dest}")
	return 0


if __name__ == "__main__":
	sys.exit(main())
