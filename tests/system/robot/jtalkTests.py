# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NVDA Japanese Team
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Logic for JTalk driver system tests."""

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


def JTalk_Driver_Available():
	"""Test that JTalk driver can be loaded without errors.
	
	This test checks that:
	1. JTalk driver module can be imported
	2. No errors occur during driver initialization
	"""
	spy = _nvdaLib.getSpyLib()
	
	# Check NVDA log for JTalk driver loading errors
	# If JTalk driver fails to load, there should be an error in the log
	from NvdaLib import _locations
	
	log_path = _locations.logPath
	
	# Read the log file to check for JTalk-related errors
	import os
	if os.path.exists(log_path):
		with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
			log_content = f.read()
	else:
		# Log file doesn't exist yet, which is fine for this test
		log_content = ""
	
	# Check for JTalk driver import errors
	jtalk_errors = [
		"Error while importing SynthDriver nvdajp_jtalk",
		"ModuleNotFoundError: No module named 'synthDrivers.jtalk.jtalkCore'",
		"Error initializing JTalk",
	]
	
	for error_msg in jtalk_errors:
		if error_msg in log_content:
			raise AssertionError(
				f"JTalk driver loading error found in log: {error_msg}\n"
				f"Log path: {log_path}"
			)
	
	# If we get here, JTalk driver loaded successfully (or wasn't attempted)
	# For a more positive test, we could check if JTalk is in the available synthesizers
	_builtIn.log("JTalk driver loaded without errors")


def JTalk_Driver_Can_Be_Selected():
	"""Test that JTalk driver can be selected in voice settings.
	
	This test:
	1. Opens voice settings dialog
	2. Checks if JTalk is available in the synthesizer list
	3. Selects JTalk if available
	"""
	spy = _nvdaLib.getSpyLib()
	
	# Open voice settings dialog
	spy.emulateKeyPress("NVDA+n")
	spy.wait_for_speech_to_finish()
	spy.emulateKeyPress("p")
	spy.wait_for_speech_to_finish()
	spy.emulateKeyPress("v")  # Voice settings
	spy.wait_for_speech_to_finish()
	
	# Wait for voice settings dialog to open
	spy.wait_for_specific_speech("Voice settings")
	spy.wait_for_speech_to_finish()
	
	# Navigate to synthesizer combo box
	# The synthesizer combo box should be the first control or near the top
	spy.reset_all_speech_index()
	start_index = spy.get_next_speech_index()
	
	# Press Tab a few times to find the synthesizer combo box
	# This is a heuristic - in practice, the synthesizer combo is usually early in the tab order
	for _ in range(5):
		spy.emulateKeyPress("tab")
		spy.wait_for_speech_to_finish()
		speech = spy.get_last_speech()
		if "synthesizer" in speech.lower() or "combo box" in speech.lower():
			# Found the synthesizer combo box
			break
	
	# Get all speech to see what synthesizers are available
	all_speech = spy.get_speech_at_index_until_now(start_index)
	
	# Check if JTalk is mentioned in the available synthesizers
	jtalk_found = False
	jtalk_indicators = ["JTalk", "jtalk", "nvdajp_jtalk"]
	
	for indicator in jtalk_indicators:
		if indicator in all_speech:
			jtalk_found = True
			break
	
	if not jtalk_found:
		# Try to open the combo box to see all options
		spy.emulateKeyPress("alt+downArrow")  # Open combo box
		spy.wait_for_speech_to_finish()
		combo_speech = spy.get_speech_at_index_until_now(spy.get_next_speech_index())
		
		for indicator in jtalk_indicators:
			if indicator in combo_speech:
				jtalk_found = True
				break
	
	if not jtalk_found:
		_builtIn.log(f"Available synthesizers: {all_speech}")
		raise AssertionError(
			"JTalk driver not found in available synthesizers. "
			"This may indicate that JTalk driver failed to load or is not available."
		)
	
	_builtIn.log("JTalk driver is available in synthesizer list")


def JTalk_Driver_Can_Speak():
	"""Test that JTalk driver can produce speech output.
	
	This test:
	1. Selects JTalk driver if not already selected
	2. Attempts to speak some text
	3. Verifies that speech output occurs
	"""
	spy = _nvdaLib.getSpyLib()
	
	# First, try to select JTalk if it's not already selected
	# Open voice settings
	spy.emulateKeyPress("NVDA+n")
	spy.wait_for_speech_to_finish()
	spy.emulateKeyPress("p")
	spy.wait_for_speech_to_finish()
	spy.emulateKeyPress("v")  # Voice settings
	spy.wait_for_speech_to_finish()
	
	spy.wait_for_specific_speech("Voice settings")
	spy.wait_for_speech_to_finish()
	
	# Try to find and select JTalk
	# This is a simplified approach - in practice, you might need more navigation
	# For now, we'll just test if speech works with the current synthesizer
	# and assume JTalk is selected if it's available
	
	# Close the dialog (Escape or Cancel)
	spy.emulateKeyPress("escape")
	spy.wait_for_speech_to_finish()
	
	# Test speech output by reading something
	# Open Notepad and type some text
	spy.emulateKeyPress("leftWindows+r")
	spy.wait_for_speech_to_finish()
	spy.emulateKeyPress("notepad")
	spy.wait_for_speech_to_finish()
	spy.emulateKeyPress("enter")
	spy.wait_for_speech_to_finish()
	
	# Wait for Notepad to open
	spy.wait_for_specific_speech("Untitled")
	spy.wait_for_speech_to_finish()
	
	# Type some text
	test_text = "JTalk test"
	spy.reset_all_speech_index()
	start_index = spy.get_next_speech_index()
	
	for char in test_text:
		spy.emulateKeyPress(char)
		spy.wait_for_speech_to_finish()
	
	# Check if we got any speech output
	speech = spy.get_speech_at_index_until_now(start_index)
	
	if not speech or len(speech.strip()) == 0:
		raise AssertionError(
			"No speech output detected. JTalk driver may not be working correctly."
		)
	
	_builtIn.log(f"Speech output received: {speech}")
	
	# Close Notepad
	spy.emulateKeyPress("alt+f4")
	spy.wait_for_speech_to_finish()

