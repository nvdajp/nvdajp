"""
Visual Studio utility functions for JP builds.
Provides shared logic for finding Visual Studio installation paths.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

# VS 2022 edition search order (most common first)
VS2022_EDITIONS = ["BuildTools", "Community", "Professional", "Enterprise"]

VS2022_BASE_PATH = Path(r"C:\Program Files\Microsoft Visual Studio\2022")


def find_vcvarsall() -> str | None:
	"""Find vcvarsall.bat in Visual Studio 2022 install locations.
	
	Returns:
		Absolute path to vcvarsall.bat if found, None otherwise.
		
	Search order: BuildTools, Community, Professional, Enterprise.
	"""
	for edition in VS2022_EDITIONS:
		path = VS2022_BASE_PATH / edition / "VC" / "Auxiliary" / "Build" / "vcvarsall.bat"
		if path.exists():
			return str(path)
	return None


def find_vcvars(arch: Literal["x86", "x64"] = "x86") -> str | None:
	"""Find vcvars32.bat or vcvars64.bat in Visual Studio 2022 install locations.
	
	Args:
		arch: Target architecture ("x86" or "x64"). Defaults to "x86".
		
	Returns:
		Absolute path to vcvars script if found, None otherwise.
		
	Search order: BuildTools, Community, Professional, Enterprise.
	"""
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
