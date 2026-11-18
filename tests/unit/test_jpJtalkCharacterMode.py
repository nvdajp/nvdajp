# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited, NVDA Japanese Team

"""Unit tests for nvdajp_jtalk CharacterModeCommand support (upstream #20831)."""

import unittest
from unittest.mock import patch

import config
from speech import speech as speechModule
from speech.commands import CharacterModeCommand
from speech.shortcutKeys import (
	_getKeyboardShortcutSpeech,
	shouldUseSpellingFunctionality,
)
from synthDrivers import nvdajp_jtalk


def _createPatchedJtalkSynth() -> nvdajp_jtalk.SynthDriver:
	"""Create an nvdajp_jtalk.SynthDriver without loading native DLLs."""
	with (
		patch.object(nvdajp_jtalk.jtalkDriver, "initialize"),
		patch.object(nvdajp_jtalk.jtalkDriver, "set_rate"),
	):
		return nvdajp_jtalk.SynthDriver()


class TestNvdajpJtalkCharacterMode(unittest.TestCase):
	"""Verify nvdajp_jtalk declares and handles CharacterModeCommand."""

	def test_supportedCommandsIncludesCharacterMode(self) -> None:
		self.assertIn(CharacterModeCommand, nvdajp_jtalk.SynthDriver.supportedCommands)

	def test_speakSetsCharacterModeAndKeepsSegmentsSeparate(self) -> None:
		synth = _createPatchedJtalkSynth()
		with patch.object(nvdajp_jtalk.jtalkDriver, "speak") as mockSpeak:
			synth.speak(
				[
					CharacterModeCommand(True),
					"1",
					CharacterModeCommand(False),
					" 2 of 4",
				],
			)

		self.assertEqual(mockSpeak.call_count, 2)
		firstCall, secondCall = mockSpeak.call_args_list
		self.assertEqual(firstCall.args[0], "1")
		self.assertTrue(firstCall.kwargs["voiceProperty_"].characterMode)
		self.assertEqual(secondCall.args[0], " 2 of 4")
		self.assertFalse(secondCall.kwargs["voiceProperty_"].characterMode)

	def test_speakResetsCharacterModeBetweenCalls(self) -> None:
		synth = _createPatchedJtalkSynth()
		with patch.object(nvdajp_jtalk.jtalkDriver, "speak") as mockSpeak:
			synth.speak([CharacterModeCommand(True), "a"])
			synth.speak(["b"])

		self.assertEqual(mockSpeak.call_count, 2)
		firstCall, secondCall = mockSpeak.call_args_list
		self.assertEqual(firstCall.args[0], "a")
		self.assertTrue(firstCall.kwargs["voiceProperty_"].characterMode)
		self.assertEqual(secondCall.args[0], "b")
		self.assertFalse(secondCall.kwargs["voiceProperty_"].characterMode)

	def test_shortcutKeysAndSpellingHonorSupportedCommands(self) -> None:
		synth = _createPatchedJtalkSynth()
		synth.initSettings()
		speechSection = config.conf["speech"][synth.name]
		prevValue = speechSection["useSpellingFunctionality"]
		try:
			with (
				patch("speech.shortcutKeys.getSynth", return_value=synth),
				patch.object(speechModule, "getSynth", return_value=synth),
			):
				speechSection["useSpellingFunctionality"] = True
				self.assertTrue(shouldUseSpellingFunctionality())
				self.assertEqual(
					_getKeyboardShortcutSpeech("Ctrl+1"),
					["Ctrl", "+", CharacterModeCommand(True), "1", CharacterModeCommand(False)],
				)
				spellingOn = list(speechModule.getSpellingSpeech("a"))
				self.assertIn(CharacterModeCommand(True), spellingOn)
				self.assertIn(CharacterModeCommand(False), spellingOn)

				speechSection["useSpellingFunctionality"] = False
				self.assertFalse(shouldUseSpellingFunctionality())
				self.assertEqual(
					_getKeyboardShortcutSpeech("Ctrl+1"),
					["Ctrl", "+", "1"],
				)
				spellingOff = list(speechModule.getSpellingSpeech("a"))
				self.assertNotIn(CharacterModeCommand(True), spellingOff)
				self.assertNotIn(CharacterModeCommand(False), spellingOff)
		finally:
			speechSection["useSpellingFunctionality"] = prevValue


if __name__ == "__main__":
	unittest.main()
