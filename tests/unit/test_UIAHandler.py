# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file:
# https://github.com/nvaccess/nvda/blob/master/copying.txt

from unittest import TestCase
from unittest.mock import Mock, patch

from comtypes import COMError

import textInfos
from UIAHandler import NVDAUnitsToUIAUnits, getUIAUnitFromNVDAUnit
from UIAHandler.utils import BulkUIATextRangeAttributeValueFetcher


class Test_getUIAUnitFromNVDAUnit(TestCase):
	def test_mappedUnitReturnsUIAUnit(self):
		self.assertEqual(
			getUIAUnitFromNVDAUnit(textInfos.UNIT_WORD),
			NVDAUnitsToUIAUnits[textInfos.UNIT_WORD],
		)

	def test_unmappedUnitRaisesNotImplementedError(self):
		with self.assertRaises(NotImplementedError):
			getUIAUnitFromNVDAUnit(textInfos.UNIT_SENTENCE)


class TestBulkUIATextRangeAttributeValueFetcher(TestCase):
	"""Tests for the bulk UIA text range attribute value fetcher."""

	def _makeHandler(self):
		handler = Mock()
		handler.ReservedMixedAttributeValue = "mixed"
		handler.reservedNotSupportedValue = "not-supported"
		return handler

	def test_getAttributeValuesCOMErrorFallsBackToIndividualFetches(self):
		"""A COMError from GetAttributeValues should fall back to individual fetches."""
		textRange = Mock()
		textRange.GetAttributeValues.side_effect = COMError(-2147417851, "server fault", None)
		# Individual fetches succeed.
		textRange.getAttributeValue.side_effect = lambda ID: {1: "value1", 2: "value2"}[ID]
		with patch("UIAHandler.utils.UIAHandler.handler", self._makeHandler()):
			fetcher = BulkUIATextRangeAttributeValueFetcher(textRange, [1, 2])
			self.assertEqual(fetcher.getValue(1), "value1")
			self.assertEqual(fetcher.getValue(2), "value2")
		textRange.GetAttributeValues.assert_called_once()

	def test_getAttributeValuesSucceeds(self):
		"""A successful GetAttributeValues should be used directly."""
		textRange = Mock()
		textRange.GetAttributeValues.return_value = ["value1", "value2"]
		with patch("UIAHandler.utils.UIAHandler.handler", self._makeHandler()):
			fetcher = BulkUIATextRangeAttributeValueFetcher(textRange, [1, 2])
			self.assertEqual(fetcher.getValue(1), "value1")
			self.assertEqual(fetcher.getValue(2), "value2")
		textRange.getAttributeValue.assert_not_called()

	def test_getAttributeValuesCOMErrorIndividualFetchAlsoFails(self):
		"""If both bulk and individual fetches fail, reservedNotSupportedValue is returned."""
		textRange = Mock()
		textRange.GetAttributeValues.side_effect = COMError(-2147417851, "server fault", None)
		textRange.getAttributeValue.side_effect = COMError(-2147417851, "server fault", None)
		with patch("UIAHandler.utils.UIAHandler.handler", self._makeHandler()):
			fetcher = BulkUIATextRangeAttributeValueFetcher(textRange, [1, 2])
			self.assertEqual(fetcher.getValue(1), "not-supported")
