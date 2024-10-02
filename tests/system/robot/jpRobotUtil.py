# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 Takuya Nishimoto
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import NvdaLib as _NvdaLib


def press_numpad2_4_times():
	spy = _NvdaLib.getSpyLib()
	for _ in range(4):
		spy.emulateKeyPress("numpad2")
	# TODO: wait for NVDA to finish speaking
	# "Character description mode disabled"
