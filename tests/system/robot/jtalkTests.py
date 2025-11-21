# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NVDA Japanese Team
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Logic for JTalk driver system tests."""

from pathlib import Path
import os
from robot.libraries.BuiltIn import BuiltIn

# relative import not used for 'systemTestUtils' because the folder is added to the path for 'libraries'
# imported methods start with underscore (_) so they don't get imported into robot files as keywords
from SystemTestSpy import (
	_getLib,
)

from AssertsLib import AssertsLib as _AssertsLib

import NvdaLib as _nvdaLib
from NvdaLib import NvdaLib as _nvdaRobotLib

_nvdaRobot: _nvdaRobotLib = _getLib("NvdaLib")
_builtIn: BuiltIn = BuiltIn()
_asserts: _AssertsLib = _getLib("AssertsLib")

_JTALK_SYNTH_ID = "nvdajp_jtalk"
_JTALK_ERROR_MARKERS = [
	"Error while importing SynthDriver nvdajp_jtalk",
	"ModuleNotFoundError: No module named 'synthDrivers.jtalk.jtalkCore'",
	"Error initializing JTalk",
]


def _get_profile_ini_path() -> Path:
	from NvdaLib import _locations

	return Path(_locations.profileDir) / "nvda.ini"


def _get_log_content() -> str:
	from NvdaLib import _locations

	log_path = _locations.logPath
	if os.path.exists(log_path):
		return Path(log_path).read_text(encoding="utf-8", errors="ignore")
	return ""


def _assert_jtalk_selected() -> None:
	ini_path = _get_profile_ini_path()
	if not ini_path.exists():
		raise AssertionError(f"nvda.ini not found at expected path: {ini_path}")
	ini_content = ini_path.read_text(encoding="utf-8", errors="ignore")
	if f"synth = {_JTALK_SYNTH_ID}" not in ini_content:
		raise AssertionError(
			f"JTalk is not selected in profile. Expected synth={_JTALK_SYNTH_ID}. "
			f"Profile path: {ini_path}"
		)


def _assert_no_jtalk_errors(log_content: str) -> None:
	for error_msg in _JTALK_ERROR_MARKERS:
		if error_msg in log_content:
			raise AssertionError(
				f"JTalk driver loading error found in log: {error_msg}"
			)


def JTalk_Driver_Available():
	"""Test that JTalk driver can be loaded without errors.
	
	This test checks that:
	1. Config selects JTalk
	2. No errors occur during driver initialization
	"""
	spy = _nvdaLib.getSpyLib()
	_assert_jtalk_selected()
	log_content = _get_log_content()
	_assert_no_jtalk_errors(log_content)
	_builtIn.log("JTalk driver loaded and selected without errors")


def JTalk_Driver_Can_Speak():
	"""Test that JTalk driver can produce speech output.
	
	This test:
	1. Confirms JTalk is selected and loaded
	2. Attempts to speak some text
	3. Verifies that no JTalk errors are logged after speaking
	"""
	spy = _nvdaLib.getSpyLib()
	_assert_jtalk_selected()

	# Request a simple utterance (title) to avoid external app dependencies.
	spy.emulateKeyPress("NVDA+t")
	spy.wait_for_speech_to_finish()

	after_log = _get_log_content()
	_assert_no_jtalk_errors(after_log)

	_builtIn.log("JTalk speech request completed without logged errors")

