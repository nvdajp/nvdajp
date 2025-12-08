#!/usr/bin/env python3
"""Copy JTalk core files using Python function from scons_jp.

This script replaces copy_jtalk_core_files.cmd and can be called from .cmd files.
"""
import sys
from pathlib import Path

# Add jptools to path
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root / "jptools"))

try:
    from scons_jp import _copy_jtalk_core_files
    exit_code = _copy_jtalk_core_files(repo_root)
    sys.exit(exit_code)
except ImportError as e:
    print(f"Error: Failed to import scons_jp: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)

