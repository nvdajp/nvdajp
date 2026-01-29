# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited, Peter Vágner, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import importlib
import fnmatch
import shutil
from glob import glob
from pathlib import Path
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--dest-dir", default="dist")
args = parser.parse_args()

# Resolve relative to this script so overlay works regardless of cwd
_scriptDir = Path(__file__).resolve().parent
nvdaSourceDir = _scriptDir / ".." / ".." / "source"
nvdaSourceDir = nvdaSourceDir.resolve()
runtimeSourceDir = nvdaSourceDir / "_bridge" / "runtimes" / "synthDriverHost"
runtimeName = "synthDriverHost"
runtimeDestDir = args.dest_dir

# Minimal speech overlay for synthDriverHost32: nvwave only needs SpeechSequence and BreakCommand.
# Full speech.__init__ pulls in excluded modules and breaks py2exe analyze. Create overlay so
# "from speech import SpeechSequence" resolves to this minimal package (speech.types + speech.commands).
_speechOverlayDir = runtimeSourceDir / "speech"
_speechOverlayDir.mkdir(parents=True, exist_ok=True)
(_speechOverlayDir / "__init__.py").write_text(
	"# Minimal speech package for synthDriverHost runtime; nvwave only needs these.\n"
	"from speech.types import SpeechSequence, SequenceItemT\n"
	"from speech.commands import BreakCommand\n"
	"__all__ = [\"SpeechSequence\", \"SequenceItemT\", \"BreakCommand\"]\n",
	encoding="utf-8",
)
for _name in ("types", "commands"):
	shutil.copy2(
		nvdaSourceDir / "speech" / f"{_name}.py",
		_speechOverlayDir / f"{_name}.py",
	)

sys.path.insert(0, str(nvdaSourceDir))

import gettext  # noqa: E402
from buildVersion import (  # noqa: E402
	formatBuildVersionString,
	name,
	publisher,
	version,
)

gettext.install("nvda")

# versionInfo names must be imported after Gettext
# Suppress E402 (module level import not at top of file)
from versionInfo import (  # noqa: E402
	copyright as NVDAcopyright,  # copyright is a reserved python keyword
	description,
)


from py2exe import freeze  # noqa: E402
from py2exe.dllfinder import DllFinder  # noqa: E402

RT_MANIFEST = 24
manifestTemplateFilePath = nvdaSourceDir / "manifest.template.xml"
_manifestTemplate = manifestTemplateFilePath.read_text(encoding="utf-8")


def _genManifestTemplate(shouldHaveUIAccess: bool) -> tuple[int, int, bytes]:
	return (
		RT_MANIFEST,
		1,
		(_manifestTemplate % {"uiAccess": shouldHaveUIAccess}).encode("utf-8"),
	)


# py2exe's idea of whether a dll is a system dll appears to be wrong sometimes, so monkey patch it.
orig_determine_dll_type = DllFinder.determine_dll_type


def determine_dll_type(self, imagename):
	dll = Path(imagename).name.lower()
	if dll.startswith("api-ms-win-") or dll in ("powrprof.dll", "mpr.dll", "crypt32.dll"):
		# These are definitely system dlls available on all systems and must be excluded.
		# Including them can cause serious problems when a binary build is run on a different version of Windows.
		return None
	return orig_determine_dll_type(self, imagename)


DllFinder.determine_dll_type = determine_dll_type


def getRecursiveDataFiles(dest: str, source: Path, excludes: tuple = ()) -> list[tuple[str, list[str]]]:
	rulesList: list[tuple[str, list[str]]] = []
	for path in source.iterdir():
		if path.is_file() and not any(fnmatch.fnmatch(path.name, exclude) for exclude in excludes):
			rulesList.append((dest, [str(path)]))
	for path in source.iterdir():
		if path.is_dir() and not path.name.startswith("."):
			rulesList.extend(
				getRecursiveDataFiles(
					str(Path(dest) / path.name),
					path,
					excludes=excludes,
				),
			)
	return rulesList


sys.path.insert(0, str(runtimeSourceDir))

freeze(
	version_info={
		"version": formatBuildVersionString(),
		"description": description,
		"product_name": name,
		"product_version": version,
		"copyright": NVDAcopyright,
		"company_name": publisher,
	},
	console=[
		{
			"script": str(runtimeSourceDir / "main.pyw"),
			"dest_base": f"nvda_{runtimeName}",
			"icon_resources": [(1, str(nvdaSourceDir / "images" / "nvda.ico"))],
			"other_resources": [_genManifestTemplate(shouldHaveUIAccess=False)],
			"version_info": {
				"version": formatBuildVersionString(),
				"description": "32 bit NVDA synthDriver host runtime",
				"product_name": "NVDA",
				"product_version": version,
				"copyright": NVDAcopyright,
				"company_name": publisher,
			},
		},
	],
	options={
		"verbose": 2,
		# Removes assertions for builds.
		# https://docs.python.org/3.13/tutorial/modules.html#compiled-python-files
		"optimize": 1,
		"bundle_files": 3,
		"dist_dir": runtimeDestDir,
		"excludes": [
			"_localCaptioner",
			"_remoteClient",
			"addonHandler",
			"addonStore",
			"appModules",
			"audio",
			"brailleDisplayDrivers",
			"brailleTables",
			"COMRegistrationFixes",
			"documentNavigation",
			"contentRegoc",
			"controlTypes",
			"globalPlugins",
			"gui",
			"hwIo",
			"IAccessibleHandler",
			"louis",
			"mathPres",
			"NVDAHelper",
			"NVDAObjects",
			"screenCurtain",
			"textInfos",
			"textUtils",
			"UIAHandler",
			"virtualBuffers",
			"vision",
			"visionEnhancementProviders",
			"wx",
			"addonAPIVersion",
			"annotation",
			"api",
			"appModuleHandler",
			"aria",
			"bdDetect",
			"braille",
			"brailleInput",
			"browseMode",
			"characterProcessing",
			"compoundDocuments",
			"cursorManager",
			"diffHandler",
			"displayModel",
			"documentBase",
			"easeOfAccess",
			"editableText",
			"eventHandler",
			"globalCommands",
			"globalPluginHandler",
			"hwPortUtils",
			"inputCore",
			"installer",
			"JABHandler",
			"keyboardHandler",
			"keyLabels",
			"locationHelper",
			"louisHelper",
			"mathType",
			"mouseHandler",
			"oleacc",
			"pythonConsole",
			"queueHandler",
			"review",
			"screenBitmap",
			"screenExplorer",
			"scriptHandler",
			"speechViewer",
			"tableUtils",
			"tones",
			"touchhandler",
			"touchTracker",
			"treeInterceptorHandler",
			"ui",
			"updateCheck",
			"vkCodes",
			"watchdog",
			"wincon",
			"winConsoleHandler",
			"windowUtils",
			"winInputHook",
			"xmlFormatting",
			"tkinter",
			"serial.loopback_connection",
			"serial.rfc2217",
			"serial.serialcli",
			"serial.serialjava",
			"serial.serialposix",
			"serial.socket_connection",
			# netbios (from pywin32) is optionally used by Python3's uuid module.
			# This is not needed.
			# We also need to exclude win32wnet explicitly.
			"netbios",
			"win32wnet",
			# winxptheme is optionally used by wx.lib.agw.aui.
			# We don't need this.
			"winxptheme",
			# multiprocessing isn't going to work in a frozen environment
			"multiprocessing",
			"concurrent.futures.process",
			# Tomli is part of Python 3.11+ as Tomlib, but is imported as tomli by cryptography, which causes an infinite loop in py2exe
			"tomli",
		],
		"packages": [
			"winBindings",
			"speech",
			"synthDrivers",
		],
		"includes": [
			"win32event",
			"win32file",
			"win32pipe",
			"audioDucking",
			"comtypes.stream",
		],
	},
	data_files=[
		(".", glob("*.dll") + glob("*.manifest")),
	]
	+ getRecursiveDataFiles(
		"synthDrivers",
		runtimeSourceDir / "synthDrivers",
		excludes=tuple(f"*{ext}" for ext in importlib.machinery.all_suffixes())
		+ (
			"*.exp",
			"*.lib",
			"*.pdb",
		),
	),
)
