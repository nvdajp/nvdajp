# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# Copyright (C) 2026 NV Access Limited, Tobias Heath
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file:
# https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the UIAHandler hung-window guard, UIA unit conversion, and bulk attribute fetcher."""

from unittest import TestCase
from unittest.mock import Mock, patch

from comtypes import COMError

import textInfos
import winUser
from UIAHandler import NVDAUnitsToUIAUnits, getUIAUnitFromNVDAUnit, utils
from UIAHandler.utils import BulkUIATextRangeAttributeValueFetcher


def _makeCOMError() -> COMError:
	# Mirrors the error seen when an unresponsive application's element is accessed:
	# (-2147220991, 'An event was unable to invoke any of the subscribers', ...)
	return COMError(
		-2147220991,
		"An event was unable to invoke any of the subscribers",
		(None, None, None, 0, None),
	)


class _FakeElement:
	"""Stand-in for an IUIAutomationElement event sender."""

	def __init__(self, cachedHandle: int = 0, raiseOnCached: bool = False) -> None:
		self._cachedHandle = cachedHandle
		self._raiseOnCached = raiseOnCached

	@property
	def cachedNativeWindowHandle(self) -> int:
		if self._raiseOnCached:
			raise _makeCOMError()
		return self._cachedHandle

	@property
	def currentNativeWindowHandle(self):
		raise AssertionError(
			"The hung-window guard must never read a live (current) property, "
			"as that is exactly the call that hangs on an unresponsive application.",
		)


class Test_getCachedWindowHandleFromEvent(TestCase):
	def test_returnsHandle(self):
		self.assertEqual(
			utils._getCachedWindowHandleFromEvent(_FakeElement(cachedHandle=1234)),
			1234,
		)

	def test_noHandleReturnsNone(self):
		self.assertIsNone(utils._getCachedWindowHandleFromEvent(_FakeElement(cachedHandle=0)))

	def test_comErrorReturnsNone(self):
		# Must swallow the COMError rather than propagate, and must not fall back
		# to the live property (which _FakeElement asserts against).
		self.assertIsNone(utils._getCachedWindowHandleFromEvent(_FakeElement(raiseOnCached=True)))


class Test_shouldSkipEventForHungWindow(TestCase):
	def test_noWindowHandleIsNotSkipped(self):
		with patch.object(winUser, "isHungAppWindow", side_effect=AssertionError("must not be called")):
			self.assertFalse(utils._shouldSkipEventForHungWindow(_FakeElement(cachedHandle=0)))

	def test_hungWindowIsSkipped(self):
		with patch.object(winUser, "isHungAppWindow", return_value=True):
			self.assertTrue(utils._shouldSkipEventForHungWindow(_FakeElement(cachedHandle=1)))

	def test_respondingWindowIsNotSkipped(self):
		with patch.object(winUser, "isHungAppWindow", return_value=False):
			self.assertFalse(utils._shouldSkipEventForHungWindow(_FakeElement(cachedHandle=1)))

	def test_guardNeverRaises(self):
		with patch.object(winUser, "isHungAppWindow", side_effect=RuntimeError("boom")):
			# A failure inside the guard itself must never escape into the COM handler.
			self.assertFalse(utils._shouldSkipEventForHungWindow(_FakeElement(cachedHandle=1)))


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
