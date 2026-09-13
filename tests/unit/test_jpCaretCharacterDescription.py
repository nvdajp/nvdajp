# -*- coding: UTF-8 -*-
# tests/unit/test_jpCaretCharacterDescription.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited, NVDA Japanese Team

"""Unit tests for characterDescriptionMode in speech.speakTextInfo.

When characterDescriptionMode is enabled, moving by character (reason=CARET,
unit=UNIT_CHARACTER) speaks the character description without prepending
character type attributes ("hiragana", "half shape", etc.).
Detailed descriptions with character types (useDetails=True) should only be used
when explicitly requested (e.g. review cursor repeatCount == 1).
"""

import unittest
from unittest.mock import patch

import config
import speech
import textInfos
from controlTypes import OutputReason

from .textProvider import BasicTextProvider


class TestCaretCharacterDescription(unittest.TestCase):
	def setUp(self):
		import speechDictHandler

		speechDictHandler.initialize()
		import synthDriverHandler

		assert synthDriverHandler.setSynth("silence")
		assert synthDriverHandler.getSynth()
		from speech import speechInitialize

		speechInitialize()

	def test_caretMoveDoesNotPassUseDetails(self):
		"""Moving caret by character with characterDescriptionMode on must not pass useDetails=True."""
		prevMode = config.conf["language"]["characterDescriptionMode"]
		config.conf["language"]["characterDescriptionMode"] = True
		try:
			obj = BasicTextProvider(text="あ", selection=(0, 0))
			info = obj.makeTextInfo(textInfos.POSITION_SELECTION)
			info.expand(textInfos.UNIT_CHARACTER)

			with patch.object(speech.speech, "speakSpelling") as mockSpeakSpelling:
				handled = speech.speakTextInfo(
					info,
					unit=textInfos.UNIT_CHARACTER,
					reason=OutputReason.CARET,
				)
				self.assertTrue(handled)
				mockSpeakSpelling.assert_called_once_with(
					"あ",
					useCharacterDescriptions=True,
				)
		finally:
			config.conf["language"]["characterDescriptionMode"] = prevMode

	def test_caretMoveWhenModeDisabledFallsThrough(self):
		"""When characterDescriptionMode is False, speakTextInfo falls through to default speech generation."""
		prevMode = config.conf["language"]["characterDescriptionMode"]
		config.conf["language"]["characterDescriptionMode"] = False
		try:
			obj = BasicTextProvider(text="あ", selection=(0, 0))
			info = obj.makeTextInfo(textInfos.POSITION_SELECTION)
			info.expand(textInfos.UNIT_CHARACTER)

			with patch.object(speech.speech, "speakSpelling") as mockSpeakSpelling:
				speech.speakTextInfo(
					info,
					unit=textInfos.UNIT_CHARACTER,
					reason=OutputReason.CARET,
				)
				mockSpeakSpelling.assert_not_called()
		finally:
			config.conf["language"]["characterDescriptionMode"] = prevMode


if __name__ == "__main__":
	unittest.main()
