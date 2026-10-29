# _nvdajp_unicode.py (compatibility shim over the vendored libkuraji)
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
#
# The implementation now lives in libkuraji (source/libkuraji,
# vendored from https://github.com/nishimotz/libkuraji, BSD 3-Clause).

import sys
from pathlib import Path

try:
	from libkuraji.unicodeutil import unicode_normalize, nfkc_normalize_with_map
except ImportError:
	sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
	from libkuraji.unicodeutil import unicode_normalize, nfkc_normalize_with_map

__all__ = ["nfkc_normalize_with_map", "unicode_normalize"]
