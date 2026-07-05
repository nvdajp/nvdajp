# -*- coding: UTF-8 -*-
# tests/unit/test_jpSpeechCrlfCharacter.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited, NVDA Japanese Team

"""Unit tests for speaking a CRLF pair as a single newline character.

Scintilla controls (Notepad++ etc.) treat CRLF as one caret position,
so the character unit at a line break yields the two-character text
"\\r\\n". Without the JP patch in speech.getTextInfoSpeech this fell
through to the plain text path and was announced as "blank".
See nvdajp issue #113.
"""

import unittest

import textInfos
from controlTypes import OutputReason

from .textProvider import BasicTextInfo, BasicTextProvider


class CrlfTextInfo(BasicTextInfo):
	"""Mimics Scintilla: a CRLF pair is a single character unit."""

	def _getCharacterOffsets(self, offset):
		storyText = self._getStoryText()
		if storyText[offset : offset + 2] == "\r\n":
			return [offset, offset + 2]
		return super()._getCharacterOffsets(offset)


class CrlfTextProvider(BasicTextProvider):
	def makeTextInfo(self, position):
		ti = super().makeTextInfo(position)
		ti.__class__ = CrlfTextInfo
		return ti


class TestCrlfCharacterSpeech(unittest.TestCase):
	def setUp(self):
		import speechDictHandler

		speechDictHandler.initialize()  # setting the synth depends on dictionary["voice"]
		import synthDriverHandler

		assert synthDriverHandler.setSynth("silence")
		assert synthDriverHandler.getSynth()
		from speech import speechInitialize

		speechInitialize()

	def _getCharacterSpeech(self, text: str, offset: int) -> str:
		from speech.speech import getTextInfoSpeech

		obj = CrlfTextProvider(text=text, selection=(offset, offset))
		info = obj.makeTextInfo(textInfos.POSITION_SELECTION)
		info.expand(textInfos.UNIT_CHARACTER)
		sequences = list(
			getTextInfoSpeech(
				info,
				unit=textInfos.UNIT_CHARACTER,
				reason=OutputReason.CARET,
			),
		)
		return " ".join(item for seq in sequences for item in seq if isinstance(item, str))

	def test_crlfPairSpokenAsNewline(self):
		"""The two-character "\\r\\n" unit must be spoken like a newline, not as blank."""
		spoken = self._getCharacterSpeech("a\r\nb", 1)
		self.assertNotIn("blank", spoken)
		self.assertIn("line feed", spoken)

	def test_lfOnlySpokenAsNewline(self):
		"""Regression guard: a single "\\n" character keeps its symbol reading."""
		spoken = self._getCharacterSpeech("a\nb", 1)
		self.assertNotIn("blank", spoken)
		self.assertIn("line feed", spoken)

	def test_normalCharacterUnaffected(self):
		spoken = self._getCharacterSpeech("a\r\nb", 0)
		self.assertIn("a", spoken)
		self.assertNotIn("line feed", spoken)
