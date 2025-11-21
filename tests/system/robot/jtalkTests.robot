# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NVDA Japanese Team
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
*** Settings ***
Documentation	JTalk driver smoke tests (start with JTalk selected and ensure it loads)
Force Tags	NVDA	jtalk

Library	NvdaLib.py
Library	jtalkTests.py

Test Setup	default setup
Test Teardown	default teardown

*** Keywords ***
default setup
	start NVDA	standard-jtalk.ini

default teardown
	quit NVDA

*** Test Cases ***
JTalk Driver Available
	[Documentation]	Ensure JTalk is selected and loads without errors.
	JTalk Driver Available

JTalk Driver Can Speak
	[Documentation]	Request speech with JTalk selected and ensure no errors are logged.
	JTalk Driver Can Speak
