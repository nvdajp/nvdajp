# -*- coding: UTF-8 -*-
# tests/unit/test_jpMecabSetFeature.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited, NVDA Japanese Team

"""Unit tests for the MeCab feature buffer bound (source/synthDrivers/jtalk/mecab.py).

Each feature slot is a fixed FELEN-byte heap buffer allocated via malloc.
Mecab_setFeature must refuse to write a longer feature instead of
overflowing the heap (security fix).
"""

import unittest

from synthDrivers.jtalk.mecab import (
	FELEN,
	Mecab_getFeature,
	Mecab_setFeature,
	NonblockingMecabFeatures,
)


class TestMecabSetFeatureBound(unittest.TestCase):
	"""Mecab_setFeature must never write beyond a FELEN-byte slot."""

	def setUp(self):
		self.mf = NonblockingMecabFeatures()

	def tearDown(self):
		# Buffers are freed by NonblockingMecabFeatures.__del__.
		del self.mf

	def test_small_feature_roundtrip(self):
		Mecab_setFeature(self.mf, 0, "あいう,名詞,一般")
		self.assertEqual(Mecab_getFeature(self.mf, 0), "あいう,名詞,一般")

	def test_max_length_feature_accepted(self):
		# FELEN - 1 bytes of data plus the terminating NUL exactly fill
		# the slot: 1998 bytes of fullwidth katakana + 1 ASCII byte.
		s = "あ" * ((FELEN - 2) // 3) + "x"
		self.assertEqual(len(s.encode("utf-8")), FELEN - 1)
		Mecab_setFeature(self.mf, 0, s)
		self.assertEqual(len(Mecab_getFeature(self.mf, 0).encode("utf-8")), FELEN - 1)

	def test_overlong_feature_rejected(self):
		with self.assertRaises(ValueError):
			Mecab_setFeature(self.mf, 0, "x" * FELEN)

	def test_overlong_multibyte_feature_rejected(self):
		# 700 fullwidth katakana characters encode to 2100 UTF-8 bytes.
		s = "ア" * 700
		self.assertGreaterEqual(len(s.encode("utf-8")), FELEN)
		with self.assertRaises(ValueError):
			Mecab_setFeature(self.mf, 0, s)


if __name__ == "__main__":
	unittest.main()
