# -*- coding: UTF-8 -*-
# tests/unit/test_jpInputCompositionHookSafety.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited, NVDA Japanese Team

"""Unit tests for Japanese input composition hook safety (#775).

Ensures that isInInputComposition and isCompositionActive do not access parent
objects across threads when focus belongs to NVDA's own process, and gracefully
handles exceptions without crashing the low-level keyboard hook thread.
"""

import os
import unittest
from unittest.mock import MagicMock, PropertyMock, patch

from NVDAObjects import inputComposition


class TestInputCompositionHookSafety(unittest.TestCase):
	def test_isInInputComposition_nvdaProcess_returnsFalseWithoutAccessingParent(self):
		"""When focus belongs to NVDA's own process (e.g. HtmlMessageDialog),
		isInInputComposition must return False without evaluating focus.parent.
		"""
		mockFocus = MagicMock()
		mockFocus.processID = os.getpid()
		type(mockFocus).parent = PropertyMock(
			side_effect=AssertionError("focus.parent should not be accessed")
		)

		result = inputComposition.isInInputComposition(mockFocus)
		self.assertFalse(result)

	def test_isInInputComposition_handlesExceptionGracefully(self):
		"""When accessing focus.parent raises an OSError (such as access violation reading COM object),
		isInInputComposition must handle it gracefully and return False.
		"""
		mockFocus = MagicMock()
		mockFocus.processID = os.getpid() + 1
		type(mockFocus).parent = PropertyMock(
			side_effect=OSError("access violation reading 0x00000000000002A0")
		)

		result = inputComposition.isInInputComposition(mockFocus)
		self.assertFalse(result)

	def test_isCompositionActive_nvdaProcess_returnsFalseWithoutAccessingParent(self):
		"""When focus belongs to NVDA's own process, isCompositionActive must return False."""
		mockFocus = MagicMock()
		mockFocus.processID = os.getpid()
		type(mockFocus).parent = PropertyMock(
			side_effect=AssertionError("focus.parent should not be accessed")
		)

		with patch("NVDAHelper.lastCompString", ""), patch("api.getFocusObject", return_value=mockFocus):
			result = inputComposition.isCompositionActive()
			self.assertFalse(result)

	def test_isCompositionActive_handlesExceptionGracefully(self):
		"""When accessing focus.parent raises an OSError, isCompositionActive must return False."""
		mockFocus = MagicMock()
		mockFocus.processID = os.getpid() + 1
		type(mockFocus).parent = PropertyMock(
			side_effect=OSError("access violation reading 0x00000000000002A0")
		)

		with patch("NVDAHelper.lastCompString", ""), patch("api.getFocusObject", return_value=mockFocus):
			result = inputComposition.isCompositionActive()
			self.assertFalse(result)
