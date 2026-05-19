# -*- coding: UTF-8 -*-
# tests/unit/test_jpAnsiEditbox.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited, NVDA Japanese Team

"""Unit tests for jpAnsiEditbox workaround in NVDAObjects.window.edit."""

import os
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import winUser
from NVDAObjects.window import edit


@unittest.skipUnless(sys.platform == "win32", "jpAnsiEditbox uses Windows mbcs encoding")
class TestJpAnsiEditboxMbcs(unittest.TestCase):
	@unittest.skipIf(
		os.environ.get("GITHUB_ACTIONS") == "true",
		"mbcs byte lengths differ from Japanese Windows on GitHub Actions runners; run locally",
	)
	def test_byte_to_unicode_offsets(self):
		# 'a'(1 byte) + 'あ'(2 bytes in typical Japanese mbcs) + 'b'(1 byte)
		story = "aあb"
		ti = object.__new__(edit.EditTextInfo)
		start, end = ti._startEndInBytesToStartEndInUnicodeChars(story, 1, 3)
		self.assertEqual((start, end), (1, 2))


class TestJpAnsiEditboxGetLineOffsets(unittest.TestCase):
	def test_get_line_offsets_fetches_story_text_once_when_workaround_enabled(self):
		ti = object.__new__(edit.EditTextInfo)
		ti.obj = SimpleNamespace(windowHandle=100)

		story_calls = {"count": 0}
		story = "abcあいう\n"

		def _get_story_text():
			story_calls["count"] += 1
			return story

		ti._needsWorkAroundEncoding = lambda: True
		ti._getStoryText = _get_story_text
		ti._getLineNumFromOffset = lambda offset: 0
		ti._startEndInBytesToStartEndInUnicodeChars = lambda st, s, e: (0, 3)
		ti._getLineCount = lambda: 1
		ti._getStoryLength = lambda: len(story)

		def send_message(hwnd, msg, w_param, l_param):
			if msg == winUser.EM_LINEINDEX:
				return 0
			if msg == winUser.EM_LINELENGTH:
				return 3
			raise AssertionError(f"Unexpected message: {msg}")

		with patch("NVDAObjects.window.edit.watchdog.cancellableSendMessage", side_effect=send_message):
			result = edit.EditTextInfo._getLineOffsets(ti, 2)

		self.assertEqual(result, (0, 3))
		self.assertEqual(story_calls["count"], 1)

	def test_get_line_offsets_without_workaround(self):
		ti = object.__new__(edit.EditTextInfo)
		ti.obj = SimpleNamespace(windowHandle=100)

		ti._needsWorkAroundEncoding = lambda: False

		def line_num_from_offset(o: int) -> int:
			# Line 0 is characters 0..4; offset 5+ belongs to the next line (stops extension loop).
			return 0 if o < 5 else 1

		ti._getLineNumFromOffset = line_num_from_offset
		ti._getLineCount = lambda: 1
		ti._getStoryLength = lambda: 10

		def send_message(hwnd, msg, w_param, l_param):
			if msg == winUser.EM_LINEINDEX:
				return 0
			if msg == winUser.EM_LINELENGTH:
				return 5
			raise AssertionError(f"Unexpected message: {msg}")

		with patch("NVDAObjects.window.edit.watchdog.cancellableSendMessage", side_effect=send_message):
			result = edit.EditTextInfo._getLineOffsets(ti, 2)

		self.assertEqual(result, (0, 5))
