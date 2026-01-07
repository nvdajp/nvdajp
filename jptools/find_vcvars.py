#!/usr/bin/env python3
"""
CLI wrapper for vs_utils.find_vcvars().
Used by vcsetup.cmd to find Visual Studio vcvars scripts.
"""

import sys
from pathlib import Path

# Add jptools to path
sys.path.insert(0, str(Path(__file__).parent))

from vs_utils import find_vcvars

if __name__ == "__main__":
	if len(sys.argv) < 2:
		arch = "x86"
	else:
		arch = sys.argv[1]

	result = find_vcvars(arch)
	if result:
		print(result)
		sys.exit(0)
	else:
		sys.exit(1)
