# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2022 NV Access Limited, Łukasz Golonka, Leonard de Ruijter, Babbage B.V.,
# Aleksey Sadovoy, Peter Vágner
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""global variables module
@var foregroundObject: holds the current foreground object. The object for the last foreground event received.
@var focusObject: holds the current focus object
@var mouseObject: holds the object that is at the position of the mouse pointer
@var mouseOldX: the last x coordinate of the mouse pointer before its current position
@type oldMouseX: int
@var mouseOldY: the last y coordinate of the mouse pointer before its current position
@type oldMouseY: int
@var navigatorObject: holds the current navigator object
"""

import argparse
import os
import typing

if typing.TYPE_CHECKING:
	import documentBase  # noqa: F401 used for type checking only
	import NVDAObjects  # noqa: F401 used for type checking only


class DefaultAppArgs(argparse.Namespace):
	quit: bool = False
	check_running: bool = False
	logFileName: typing.Optional[os.PathLike] = ""
	logLevel: int = 0
	configPath: typing.Optional[os.PathLike] = None
	language: str = "en"
	minimal: bool = False
	secure: bool = False
	"""
	When this is True, NVDA is running in secure mode.
	This is set to True when NVDA starts with the --secure parameter.
	This is also set to True when NVDA is running on a secure screen
	(systemUtils._isSecureDesktop() returns True)
	and the serviceDebug parameter is not set.

	For more information, refer to devDocs/technicalDesignOverview.md 'Logging in secure mode'
	and the following userGuide sections:
	 - SystemWideParameters (information on the serviceDebug parameter)
	 - SecureMode and SecureScreens
	"""
	disableAddons: bool = False
	debugLogging: bool = False
	noLogging: bool = False
	changeScreenReaderFlag: bool = True
	install: bool = False
	installSilent: bool = False
	createPortable: bool = False
	createPortableSilent: bool = False
	portablePath: typing.Optional[os.PathLike] = None
	launcher: bool = False
	enableStartOnLogon: typing.Optional[bool] = None
	copyPortableConfig: bool = False
	easeOfAccess: bool = False


startTime=0
desktopObject: typing.Optional['NVDAObjects.NVDAObject'] = None
foregroundObject: typing.Optional['NVDAObjects.NVDAObject'] = None
focusObject: typing.Optional['NVDAObjects.NVDAObject'] = None
focusAncestors: typing.List['NVDAObjects.NVDAObject'] = []
focusDifferenceLevel=None
mouseObject: typing.Optional['NVDAObjects.NVDAObject'] = None
mouseOldX=None
mouseOldY=None
navigatorObject: typing.Optional['NVDAObjects.NVDAObject'] = None
reviewPosition=None
reviewPositionObj: typing.Optional["documentBase.TextContainerObject"] = None
lastProgressValue=0
appArgs = DefaultAppArgs()
unknownAppArgs: typing.List[str] = []
settingsRing = None
speechDictionaryProcessing=True
exitCode=0

appPid: int = 0
"""The process ID of NVDA itself.
"""

_allowDeprecatedAPI: bool = True
"""
Used for marking code as deprecated.
This should never be False in released code.

Making this False may be useful for testing if code is compliant without using deprecated APIs.
Note that deprecated code may be imported at runtime,
and as such, this value cannot be changed at runtime to test compliance.
"""
