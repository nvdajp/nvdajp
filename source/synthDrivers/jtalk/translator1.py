# coding: UTF-8
# translator1.py (compatibility shim over the vendored libkuraji)
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2026 Masataka Shinke, Takuya Nishimoto
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
#
# The kana-to-braille stage now lives in libkuraji (source/libkuraji,
# vendored from https://github.com/nishimotz/libkuraji, BSD 3-Clause)
# as a clean-room reimplementation; this module keeps the historical
# NVDAJP entry point.

import sys
from pathlib import Path

try:
	from libkuraji.kana import translate_with_pos, translateWithInPos
except ImportError:
	sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
	from libkuraji.kana import translate_with_pos, translateWithInPos

__all__ = ["translate_with_pos", "translateWithInPos"]
