# -*- coding: UTF-8 -*-
# tests/unit/test_jpDicPins.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited, NVDA Japanese Team

"""Unit tests for the JTalk dictionary version pins.

The dictionary release is pinned in two places:

- build time: miscDepsJp/jptools/jtalk-dic-version.txt (consumed by
  jptools/scons_jp.py to bundle the prebuilt dictionary),
- runtime: DEFAULT_DIC_TAG in source/libkuraji/jtalk_dic.py (used by
  make_analyzer when the bundled dictionary is missing).

They must point at the same release, otherwise the bundled dictionary and
the auto-downloaded one can produce different MeCab morpheme boundaries.
"""

import re
import unittest
from pathlib import Path

from libkuraji.jtalk_dic import DEFAULT_DIC_TAG

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DIC_VERSION_FILE = _REPO_ROOT / "miscDepsJp" / "jptools" / "jtalk-dic-version.txt"


class TestJtalkDicPinParity(unittest.TestCase):
	"""DEFAULT_DIC_TAG and jtalk-dic-version.txt must reference the same tag."""

	def test_runtimeDefaultTagMatchesBuildPin(self):
		pinText = _DIC_VERSION_FILE.read_text(encoding="utf-8")
		match = re.search(r"^tag=(\S+)", pinText, flags=re.MULTILINE)
		self.assertIsNotNone(match, f"tag= line not found in {_DIC_VERSION_FILE}")
		buildTag = match.group(1)
		self.assertEqual(
			DEFAULT_DIC_TAG,
			buildTag,
			msg=(
				f"source/libkuraji/jtalk_dic.py DEFAULT_DIC_TAG ({DEFAULT_DIC_TAG}) does not "
				f"match miscDepsJp/jptools/jtalk-dic-version.txt ({buildTag}); "
				"bump both together in the same PR."
			),
		)


class TestJtalkDicTagFormat(unittest.TestCase):
	"""DEFAULT_DIC_TAG must be a well-formed release tag."""

	def test_defaultTagMatchesTagPattern(self):
		# _DIC_TAG_RE in jtalk_dic.py is private; assert the same shape here.
		pattern = re.compile(r"^v\d+\.\d+\.\d+$")
		self.assertRegex(DEFAULT_DIC_TAG, pattern)


if __name__ == "__main__":
	unittest.main()