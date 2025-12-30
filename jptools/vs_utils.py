"""
Visual Studio utility functions for JP builds.
Provides shared logic for finding Visual Studio installation paths.
Uses vswhere (preferred) with fallback to direct path search.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Literal

# VS 2022 edition search order (most common first)
VS2022_EDITIONS = ["BuildTools", "Community", "Professional", "Enterprise"]

VS2022_BASE_PATH = Path(r"C:\Program Files\Microsoft Visual Studio\2022")

# vswhere.exe location
VSWHERE_PATH = Path(r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe")


def find_vcvarsall_with_vswhere() -> str | None:
	"""Find vcvarsall.bat using vswhere (preferred method).

	Prioritizes Visual Studio 2022 over Visual Studio 2025.

	Returns:
		Absolute path to vcvarsall.bat if found, None otherwise.
	"""
	if not VSWHERE_PATH.exists():
		return None

	pattern = r"VC\Auxiliary\Build\vcvarsall.bat"

	# Try Visual Studio 2022 first (version [17.0,18.0))
	for version_range in ["[17.0,18.0)", "*"]:
		try:
			args = [
				str(VSWHERE_PATH),
				"-latest",
				"-products", "*",
				"-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
				"-find", pattern,
				"-format", "value",
			]
			if version_range != "*":
				args.insert(2, "-version")
				args.insert(3, version_range)

			result = subprocess.check_output(
				args,
				text=True,
				errors="ignore",
			).strip()

			if result and Path(result).exists():
				return result
		except Exception:
			pass

	return None


def find_vcvars_with_vswhere(arch: Literal["x86", "x64"] = "x86") -> str | None:
	"""Find vcvars script using vswhere (preferred method).

	Prioritizes Visual Studio 2022 over Visual Studio 2025.

	Args:
		arch: Target architecture ("x86" or "x64"). Defaults to "x86".

	Returns:
		Absolute path to vcvars script if found, None otherwise.
	"""
	if not VSWHERE_PATH.exists():
		return None

	script_name = "vcvars32.bat" if arch == "x86" else "vcvars64.bat"
	pattern = rf"VC\Auxiliary\Build\{script_name}"

	# Try Visual Studio 2022 first (version [17.0,18.0))
	for version_range in ["[17.0,18.0)", "*"]:
		try:
			args = [
				str(VSWHERE_PATH),
				"-latest",
				"-products", "*",
				"-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
				"-find", pattern,
				"-format", "value",
			]
			if version_range != "*":
				args.insert(2, "-version")
				args.insert(3, version_range)

			result = subprocess.check_output(
				args,
				text=True,
				errors="ignore",
			).strip()

			if result and Path(result).exists():
				return result
		except Exception:
			pass

	return None


def find_vcvarsall() -> str | None:
	"""Find vcvarsall.bat in Visual Studio install locations.

	First tries vswhere (preferred), then falls back to direct path search.

	Returns:
		Absolute path to vcvarsall.bat if found, None otherwise.

	Search order: BuildTools, Community, Professional, Enterprise.
	"""
	# Try vswhere first (preferred method, consistent with nonCertBuild.py)
	result = find_vcvarsall_with_vswhere()
	if result:
		return result

	# Fallback to direct path search (for environments without vswhere)
	for edition in VS2022_EDITIONS:
		path = VS2022_BASE_PATH / edition / "VC" / "Auxiliary" / "Build" / "vcvarsall.bat"
		if path.exists():
			return str(path)
	return None


def find_vcvars(arch: Literal["x86", "x64"] = "x86") -> str | None:
	"""Find vcvars32.bat or vcvars64.bat in Visual Studio install locations.

	First tries vswhere (preferred), then falls back to direct path search.

	Args:
		arch: Target architecture ("x86" or "x64"). Defaults to "x86".

	Returns:
		Absolute path to vcvars script if found, None otherwise.

	Search order: BuildTools, Community, Professional, Enterprise.
	"""
	# Try vswhere first (preferred method, consistent with nonCertBuild.py)
	result = find_vcvars_with_vswhere(arch)
	if result:
		return result

	# Fallback to direct path search (for environments without vswhere)
	script_name = "vcvars32.bat" if arch == "x86" else "vcvars64.bat"

	for edition in VS2022_EDITIONS:
		path = VS2022_BASE_PATH / edition / "VC" / "Auxiliary" / "Build" / script_name
		if path.exists():
			return str(path)
	return None


def get_editions() -> list[str]:
	"""Get list of Visual Studio 2022 editions in search order.

	Returns:
		List of edition names: ["BuildTools", "Community", "Professional", "Enterprise"]
	"""
	return VS2022_EDITIONS.copy()
