# nvaccess beta マージコンフリクト詳細記録（2025-11）

このファイルは、nvaccess/beta を日本語版にマージする際に発生したコンフリクトの詳細を記録したものです。

## メタ情報

- **マージ元**: nvaccess/beta
- **マージ先（ベース）**: betajp
- **記録日時**: 2025-11-06 00:01:02
- **上流コミット**: ac309fe35f (Update user_docs/en/changes.xliff)
- **ベースコミット**: 210eb36f50 (cherry certbuild refactor (#569))

## コンフリクトファイル一覧
### 1. .github/ISSUE_TEMPLATE/bug_report.md

**状態**: コンフリクトマーカーが見つかりません（未解決または自動マージ済み）

### 2. .github/ISSUE_TEMPLATE/feature_request.md

**状態**: コンフリクトマーカーが見つかりません（未解決または自動マージ済み）

### 3. .github/workflows/testAndPublish.yml

**コンフリクト数**: 22

**コンフリクト開始行**: 6, 38, 140, 355, 370, 426, 461, 493, 513, 531, 570, 633, 714, 724, 747, 785, 798, 809, 827, 854, 875, 886

**最初のコンフリクト周辺（行 1 - 56）**:

````n1:name: CI/CD Japanese Version
2:
3:on:
4:  push:
5:    branches:
6:<<<<<<< HEAD <- JP側
7:      - 'betajp'
8:      - 'releasejp'
9:  pull_request:
10:    branches:
11:      - 'alphajp**'
12:      - 'betajp**'
13:      - 'releasejp**'
14:======= <- 分岐点
15:      - master
16:      - beta
17:      - rc
18:      - 'try-**'
19:    tags:
20:      - 'release-**'
21:
22:  pull_request:
23:    branches:
24:      - master
25:      - beta
26:      - rc
27:      - 'try-**'
28:
29:>>>>>>> nvaccess/beta <- 上流側
30:  workflow_dispatch:
31:
32:env:
33:  PY_PYTHON: 3.11-32
34:  RELEASE: 1
35:  PUBLISHER: nvdajp
36:  # Cache details about available MSVC tooling for subsequent SCons invocations
37:  SCONS_CACHE_MSVC_CONFIG: ".scons_msvc_cache.json"
38:<<<<<<< HEAD <- JP側
39:
40:jobs:
41:  typeCheck:
42:    name: Static type analysis (pyright)
43:    runs-on: windows-2025
44:    steps:
45:    - name: Checkout repository
46:      uses: actions/checkout@v4
47:      with:
48:        submodules: true
49:
50:    - name: Set up Python 3.11 x86
51:      uses: actions/setup-python@v5
52:      with:
53:        python-version: '3.11.9'
54:        architecture: 'x86'
55:
56:    - name: Install uv
````n
---

### 4. .python-versions

**コンフリクト数**: 1

**コンフリクト開始行**: 1

**最初のコンフリクト周辺（行 1 - 5）**:

````n1:<<<<<<< HEAD <- JP側
2:cpython-3.11.9-windows-x86-none
3:======= <- 分岐点
4:cpython-3.13.9-windows-x86_64-none
5:>>>>>>> nvaccess/beta <- 上流側
````n
---

### 5. miscDeps

**コンフリクト数**: 1

**コンフリクト開始行**: 

---

### 6. nvdaHelper/archBuild_sconscript

**コンフリクト数**: 1

**コンフリクト開始行**: 267

**最初のコンフリクト周辺（行 262 - 279）**:

````n262:	remoteLoaderProgram = env.SConscript("remoteLoader/sconscript")
263:	if signExec:
264:		env.AddPostAction(remoteLoaderProgram, [signExec])
265:	env.Install(libInstallDir, remoteLoaderProgram)
266:
267:<<<<<<< HEAD <- JP側
268:if TARGET_ARCH == "x86":
269:	espeakLib, sonicLib = thirdPartyEnv.SConscript("espeak/sconscript")
270:	if signExec:
271:		thirdPartyEnv.AddPostAction(espeakLib, signExec)
272:		thirdPartyEnv.AddPostAction(sonicLib, signExec)
273:======= <- 分岐点
274:if isNVDACoreArch:
275:	thirdPartyEnv.SConscript("espeak/sconscript")
276:>>>>>>> nvaccess/beta <- 上流側
277:	thirdPartyEnv.SConscript("liblouis/sconscript")
278:	thirdPartyEnv.SConscript("javaAccessBridge/sconscript")
279:	thirdPartyEnv.SConscript("uwp/sconscript")
````n
---

### 7. runlint.bat

**コンフリクト数**: 1

**コンフリクト開始行**: 12

**最初のコンフリクト周辺（行 7 - 35）**:

````n7:
8:set ruffCheckArgs=
9:set ruffFormatArgs=
10:set ruffExcludeArgs=--exclude=include,source/comInterfaces,miscDepsJp,miscDeps/python/ftdi2.py,source/NVDAObjects/UIA/__init__.py
11:if "%1" NEQ "" set ruffCheckArgs=--output-file=%1/PR-lint.xml --output-format=junit
12:<<<<<<< HEAD <- JP側
13:if "%1" NEQ "" set ruffFormatArgs=--diff > %1/lint-diff.diff
14:call uv run --group lint --directory "%here%" ruff check --fix %ruffExcludeArgs% %ruffCheckArgs%
15:if ERRORLEVEL 1 exit /b %ERRORLEVEL%
16:call uv run --group lint --directory "%here%" ruff format %ruffExcludeArgs% %ruffFormatArgs%
17:======= <- 分岐点
18:if "%1" NEQ "" set ruffFormatArgs=--diff
19:call uv run --group lint --directory "%here%" ruff check --fix %ruffCheckArgs%
20:if ERRORLEVEL 1 exit /b %ERRORLEVEL%
21:if "%1" NEQ "" (
22:    call uv run --group lint --directory "%here%" ruff format %ruffFormatArgs% > %1/lint-diff.diff
23:) else (
24:    call uv run --group lint --directory "%here%" ruff format %ruffFormatArgs%
25:)
26:>>>>>>> nvaccess/beta <- 上流側
27:if ERRORLEVEL 1 exit /b %ERRORLEVEL%
28:
29:rem Run pyright for type checking
30:if "%1" NEQ "" (
31:    call uv run --group lint --directory "%here%" pyright > %1/pyright-output.txt
32:) else (
33:    call uv run --group lint --directory "%here%" pyright
34:)
35:if ERRORLEVEL 1 exit /b %ERRORLEVEL%
````n
---

### 8. source/NVDAHelper/__init__.py

**コンフリクト数**: 1

**コンフリクト開始行**: 7

**最初のコンフリクト周辺（行 2 - 57）**:

````n2:# Copyright (C) 2008-2025 NV Access Limited, Peter Vagner, Davy Kager, Mozilla Corporation, Google LLC,
3:# Leonard de Ruijter
4:# This file is covered by the GNU General Public License.
5:# See the file COPYING for more details.
6:
7:<<<<<<< HEAD:source/NVDAHelper.py <- JP側
8:from typing import Optional, Tuple
9:======= <- 分岐点
10:from ctypes.wintypes import (
11:	HANDLE,
12:	HKEY,
13:)
14:>>>>>>> nvaccess/beta:source/NVDAHelper/__init__.py <- 上流側
15:import typing
16:import os
17:import winreg
18:import msvcrt
19:
20:from ctypes import (
21:	CDLL,
22:	POINTER,
23:	WINFUNCTYPE,
24:	WinError,
25:	byref,
26:	c_bool,
27:	c_int,
28:	c_long,
29:	c_ulong,
30:	c_void_p,
31:	c_wchar_p,
32:	c_wchar,
33:	cast,
34:	create_unicode_buffer,
35:	windll,
36:	wstring_at,
37:)
38:
39:from winBindings import user32
40:import winBindings.oleaut32
41:import winBindings.kernel32
42:import winBindings.advapi32
43:import winBindings.rpcrt4
44:import winBindings.shlwapi
45:import globalVars
46:from NVDAState import ReadPaths
47:
48:from . import localLib
49:import winVersion
50:import winKernel
51:import config
52:import winUser
53:import eventHandler
54:import queueHandler
55:import api
56:from logHandler import log
57:from utils.security import isLockScreenModeActive
````n
---

### 9. source/_remoteClient/secureDesktop.py

**コンフリクト数**: 1

**コンフリクト開始行**: 483

**最初のコンフリクト周辺（行 478 - 533）**:

````n478:				log.debugWarning(f"Failed to unmap IPC file. {GetLastError()}: {FormatError()}")
479:			self._bufferAddress = None
480:		if self._mapFile is not None:
481:			if not closeHandle(self._mapFile):
482:				log.debugWarning(
483:<<<<<<< HEAD <- JP側
484:					f"Failed to close handle to memory mapped IPC file. {GetLastError()}: {FormatError()}"
485:======= <- 分岐点
486:					"Failed to close handle to memory mapped IPC file. {GetLastError()}: {FormatError()}",
487:>>>>>>> nvaccess/beta <- 上流側
488:				)
489:			self._mapFile = None
490:
491:	def initializeSecureDesktop(self) -> Optional[ConnectionInfo]:
492:		"""Initialize connection when starting in secure desktop.
493:
494:		:return: Connection information if successful, None on failure
495:		"""
496:		log.info("Initializing secure desktop connection")
497:		# Even though we only need read access,
498:		# Memory mapped files must all be mapped with the same permissions.
499:		mapFile = OpenFileMapping(FILE_MAP.ALL_ACCESS, False, self._IPC_FILENAME)
500:		if mapFile is None:
501:			log.debug(f"Failed to open IPC file mapping. {GetLastError()}: {FormatError()}")
502:			return None
503:		bufferAddress = MapViewOfFile(mapFile, FILE_MAP.ALL_ACCESS, 0, 0, self._IPC_MAXLEN * sizeof(WCHAR))
504:		if bufferAddress is None:
505:			log.error(f"Failed to map IPC file mapping. {GetLastError()}: {FormatError()}")
506:			if not closeHandle(mapFile):
507:				log.debugWarning(f"Failed to close file mapping. {GetLastError()}: {FormatError()}")
508:			return None
509:		waitResult = WaitForSingleObject(self._ipcEventHandle, 2000)
510:		if waitResult == WAIT.TIMEOUT:
511:			log.error("Timed out while waiting for IPC data.")
512:			return None
513:		elif waitResult == WAIT.FAILED:
514:			log.error(f"Failed to wait for event. {GetLastError()}: {FormatError()}")
515:			return None
516:		elif waitResult != WAIT.OBJECT_0:
517:			log.error(f"Unknown return from WaitForSingleObject: {waitResult}")
518:			return None
519:		try:
520:			log.debug("Reading connection data from IPC file mapping.")
521:			data = json.loads(wstring_at(bufferAddress))
522:			port, channel = data
523:
524:			# Try opening a socket to make sure we have the appropriate permissions
525:			testSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
526:			testSocket.close()
527:
528:			# Check that a socket is open on the right IP and port and with the same owning process image
529:			processImageName = create_unicode_buffer(1024)
530:			_kernel32.GetModuleFileName(0, processImageName, 1024)
531:			if not localLib.localListeningSocketExists(port, processImageName):
532:				raise RuntimeError("Matching socket not open.")
533:
````n
---

### 10. source/braille.py

**コンフリクト数**: 2

**コンフリクト開始行**: 802, 886

**最初のコンフリクト周辺（行 797 - 852）**:

````n797:			level = None
798:		elif role == controlTypes.Role.LINK and states and controlTypes.State.VISITED in states:
799:			states = states.copy()
800:			states.discard(controlTypes.State.VISITED)
801:			# Translators: Displayed in braille for a link which has been visited.
802:<<<<<<< HEAD <- JP側
803:			roleText = _nvdajp("vlnk")
804:======= <- 分岐点
805:			roleText = _("vlnk")
806:		elif role == controlTypes.Role.LIST:
807:			if (
808:				states
809:				and controlTypes.State.MULTISELECTABLE in states
810:				and config.conf["presentation"]["reportMultiSelect"]
811:			):
812:				# Collapse the list role and multiselectable state into a single role text.
813:				# Note that for other cases where this state is found, regular processing with
814:				# controlTypes.processAndLabelStates will discard the state if necessary.
815:				states = states.copy()
816:				states.discard(controlTypes.State.MULTISELECTABLE)
817:				# Translators: Displayed in braille for a multi select list.
818:				roleText = _("mslst")
819:			else:
820:				roleText = roleLabels.get(role, role.displayString)
821:			if childControlCount:
822:				roleText += childControlCount
823:				childControlCount = None
824:
825:>>>>>>> nvaccess/beta <- 上流側
826:		elif (
827:			name or cellCoordsText or rowNumber or columnNumber
828:		) and role in controlTypes.silentRolesOnFocus:
829:			roleText = None
830:		else:
831:			roleText = getRoleLabel(role, role.displayString)
832:	elif role is None:
833:		role = propertyValues.get("_role")
834:	# nvdajp begin
835:	if (
836:		config.conf["keyboard"]["nvdajpEnableKeyEvents"]
837:		and isComposition
838:		and role == controlTypes.Role.EDITABLETEXT
839:	):
840:		roleText = None
841:	# nvdajp end
842:	value = propertyValues.get("value")
843:	if value and role not in controlTypes.silentValuesForRoles:
844:		textList.append(value)
845:	if states is not None:
846:		textList.extend(
847:			controlTypes.processAndLabelStates(
848:				role,
849:				states,
850:				controlTypes.OutputReason.FOCUS,
851:				states,
852:				None,
````n
---

### 11. source/gui/__init__.py

**コンフリクト数**: 1

**コンフリクト開始行**: 113

**最初のコンフリクト周辺（行 108 - 163）**:

````n108:	subprocess.Popen([MSHTA_PATH, hta_file_path])
109:
110:
111:### Constants
112:NVDA_PATH = globalVars.appDir
113:<<<<<<< HEAD <- JP側
114:# ICON_PATH=os.path.join(NVDA_PATH, "images", "nvda.ico")
115:ICON_PATH = os.path.join(NVDA_PATH, "images", "nvdajp3.ico")
116:# DONATE_URL = f"{versionInfo.url}/donate/"
117:DONATE_URL = "https://www.nvda.jp/donate.html"
118:======= <- 分岐点
119:ICON_PATH = os.path.join(NVDA_PATH, "images", "nvda.ico")
120:DONATE_URL = f"{buildVersion.url}/donate/"
121:>>>>>>> nvaccess/beta <- 上流側
122:
123:### Globals
124:mainFrame: "MainFrame | None" = None
125:"""Set by initialize. Should be used as the parent for "top level" dialogs.
126:"""
127:
128:
129:def __getattr__(attrName: str) -> Any:
130:	"""Module level `__getattr__` used to preserve backward compatibility."""
131:	from gui.settingsDialogs import AutoSettingsMixin, SettingsPanel
132:
133:	if attrName == "AutoSettingsMixin" and NVDAState._allowDeprecatedAPI():
134:		log.warning(
135:			"Importing AutoSettingsMixin from here is deprecated. "
136:			"Import AutoSettingsMixin from gui.settingsDialogs instead. ",
137:			# Include stack info so testers can report warning to add-on author.
138:			stack_info=True,
139:		)
140:		return AutoSettingsMixin
141:	if attrName == "SettingsPanel" and NVDAState._allowDeprecatedAPI():
142:		log.warning(
143:			"Importing SettingsPanel from here is deprecated. "
144:			"Import SettingsPanel from gui.settingsDialogs instead. ",
145:			# Include stack info so testers can report warning to add-on author.
146:			stack_info=True,
147:		)
148:		return SettingsPanel
149:	if attrName == "ExecAndPump" and NVDAState._allowDeprecatedAPI():
150:		log.warning(
151:			"Importing ExecAndPump from here is deprecated. Import ExecAndPump from systemUtils instead. ",
152:			# Include stack info so testers can report warning to add-on author.
153:			stack_info=True,
154:		)
155:		import systemUtils
156:
157:		return systemUtils.ExecAndPump
158:	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")
159:
160:
161:class MainFrame(wx.Frame):
162:	"""A hidden window, intended to act as the parent to all dialogs."""
163:
````n
---

### 12. source/installer.py

**コンフリクト数**: 1

**コンフリクト開始行**: 276

**最初のコンフリクト周辺（行 271 - 326）**:

````n271:	"""
272:	Constructs a dictionary that is written to the registry for NVDA to show up
273:	in the Windows "Apps and Features" overview.
274:	"""
275:	return dict(
276:<<<<<<< HEAD <- JP側
277:		DisplayName=f"{versionInfo.name} {versionInfo.version}",
278:		DisplayVersion=versionInfo.version_detailed,
279:		DisplayIcon=os.path.join(installDir, "images", "nvdajp3.ico"),
280:======= <- 分岐点
281:		DisplayName=f"{buildVersion.name} {buildVersion.version}",
282:		DisplayVersion=buildVersion.version_detailed,
283:		DisplayIcon=os.path.join(installDir, "images", "nvda.ico"),
284:>>>>>>> nvaccess/beta <- 上流側
285:		# EstimatedSize is in KiB
286:		EstimatedSize=getDirectorySize(installDir) // 1024,
287:		InstallDir=installDir,
288:		Publisher=buildVersion.publisher,
289:		UninstallDirectory=installDir,
290:		UninstallString=os.path.join(installDir, "uninstall.exe"),
291:		URLInfoAbout=buildVersion.url,
292:	)
293:
294:
295:def getDirectorySize(path: str) -> int:
296:	"""Calculates the size of a directory in bytes."""
297:	total = 0
298:	with os.scandir(path) as iterator:
299:		for entry in iterator:
300:			if entry.is_file():
301:				total += entry.stat().st_size
302:			elif entry.is_dir():
303:				total += getDirectorySize(entry.path)
304:	return total
305:
306:
307:def registerInstallation(
308:	installDir: str,
309:	startMenuFolder: str,
310:	shouldCreateDesktopShortcut: bool,
311:	startOnLogonScreen: bool,
312:	configInLocalAppData: bool = False,
313:) -> None:
314:	calculatedUninstallerRegInfo = getUninstallerRegInfo(installDir)
315:	log.debug(f"Estimated install size: {calculatedUninstallerRegInfo.get('EstimatedSize')} KiB")
316:	with winreg.CreateKeyEx(
317:		winreg.HKEY_LOCAL_MACHINE,
318:		RegistryKey.INSTALLED_COPY.value,
319:		0,
320:		winreg.KEY_WRITE,
321:	) as k:
322:		for name, value in calculatedUninstallerRegInfo.items():
323:			if isinstance(value, int):
324:				regType = winreg.REG_DWORD
325:			elif isinstance(value, str):
326:				regType = winreg.REG_SZ
````n
---

### 13. source/locale/ja/LC_MESSAGES/nvda.po

**コンフリクト数**: 38

**コンフリクト開始行**: 1, 397, 1983, 4560, 11305, 11815, 12009, 12019, 13295, 13422, 13761, 14530, 15487, 16818, 19822, 20798, 21054, 21383, 21425, 21489, 21582, 22263, 23219, 23852, 23910, 24565, 29393, 29800, 31323, 31639, 33248, 33261, 34238, 36882, 37089, 37145, 37157, 37168

**最初のコンフリクト周辺（行 1 - 51）**:

````n1:<<<<<<< HEAD <- JP側
2:msgid ""
3:msgstr ""
4:"Project-Id-Version: nvda\n"
5:"Report-Msgid-Bugs-To: \n"
6:"POT-Creation-Date: 2025-09-05 06:01+0000\n"
7:"PO-Revision-Date: 2025-09-08 00:44\n"
8:"Last-Translator: \n"
9:"Language-Team: Japanese\n"
10:"Language: ja_JP\n"
11:"MIME-Version: 1.0\n"
12:"Content-Type: text/plain; charset=UTF-8\n"
13:"Content-Transfer-Encoding: 8bit\n"
14:"Plural-Forms: nplurals=1; plural=0;\n"
15:"X-Crowdin-Project: nvda\n"
16:"X-Crowdin-Project-ID: 598017\n"
17:"X-Crowdin-Language: ja\n"
18:"X-Crowdin-File: nvda.pot\n"
19:"X-Crowdin-File-ID: 2\n"
20:
21:# nvdajp from here
22:
23:#: source\gui\__init__.py
24:msgid "NVDA Japanese Team"
25:msgstr "NVDA日本語チーム"
26:
27:#: keyLabels.py:139
28:msgid "IME non convert"
29:msgstr "無変換"
30:
31:#: keyLabels.py:141
32:msgid "IME convert"
33:msgstr "変換"
34:
35:#: keyLabels.py:143
36:msgid "pause"
37:msgstr "ポーズ"
38:
39:#: gui\settingsDialogs.py:497
40:msgid "Phonetic reading for Kana"
41:msgstr "かな文字をフォネティック読み"
42:
43:#: gui\settingsDialogs.py:494
44:msgid "Phonetic reading for Latin"
45:msgstr "アルファベットをフォネティック読み"
46:
47:#: gui\settingsDialogs.py:549
48:msgid "Use IME support of nvdajp"
49:msgstr "日本語版の文字入力拡張"
50:
51:#: gui\settingsDialogs.py:552
````n
---

### 14. source/synthDriverHandler.py

**コンフリクト数**: 1

**コンフリクト開始行**: 486

**最初のコンフリクト周辺（行 481 - 536）**:

````n481:	return newSynth
482:
483:
484:# The synthDrivers that should be used by default.
485:# The first that successfully initializes will be used when config is set to auto (I.e. new installs of NVDA).
486:<<<<<<< HEAD <- JP側
487:defaultSynthPriorityList = ["nvdajp_jtalk", "espeak", "silence"]
488:if winVersion.getWinVer() >= winVersion.WIN10:
489:	# Default to OneCore on Windows 10 and above
490:	defaultSynthPriorityList.insert(0, "oneCore")
491:======= <- 分岐点
492:defaultSynthPriorityList = ["oneCore", "espeak", "silence"]
493:>>>>>>> nvaccess/beta <- 上流側
494:
495:
496:def setSynth(name: Optional[str], isFallback: bool = False):
497:	from synthDrivers.silence import SynthDriver as SilenceSynthDriver
498:
499:	asDefault = False
500:	global _curSynth, _audioOutputDevice
501:	if name is None:
502:		_curSynth.cancel()
503:		_curSynth.terminate()
504:		_curSynth = None
505:		return True
506:	if name == "auto":
507:		asDefault = True
508:		name = defaultSynthPriorityList[0]
509:	if _curSynth:
510:		_curSynth.cancel()
511:		_curSynth.terminate()
512:		prevSynthName = _curSynth.name
513:		_curSynth = None
514:	else:
515:		prevSynthName = None
516:	try:
517:		_curSynth = getSynthInstance(name, asDefault)
518:	except:  # noqa: E722 # Legacy bare except
519:		log.error(f"setSynth failed for {name}", exc_info=True)
520:
521:	if _curSynth is not None:
522:		_audioOutputDevice = config.conf["audio"]["outputDevice"]
523:		if not isFallback:
524:			config.conf["speech"]["synth"] = name
525:		log.info(f"Loaded synthDriver {_curSynth.name}")
526:		synthChanged.notify(synth=_curSynth, audioOutputDevice=_audioOutputDevice, isFallback=isFallback)
527:		return True
528:	# As there was an error loading this synth:
529:	elif prevSynthName and not prevSynthName == SilenceSynthDriver.name:
530:		# Don't fall back to silence if speech is expected
531:		log.info(f"Falling back to previous synthDriver {prevSynthName}")
532:		# There was a previous synthesizer, so switch back to that one.
533:		setSynth(prevSynthName, isFallback=True)
534:	else:
535:		# There was no previous synth, so fallback to the next available default synthesizer
536:		# that has not been tried yet.
````n
---

### 15. tests/system/libraries/SystemTestSpy/configManager.py

**コンフリクト数**: 1

**コンフリクト開始行**: 131

**最初のコンフリクト周辺（行 126 - 181）**:

````n126:	"""Cleans up the profile directory
127:	@todo: this could have an option to preserve the profile for debugging purposes.
128:	@param stagingDir: Where the profile was constructed
129:	"""
130:	builtIn.log("Cleaning up NVDA profile", level="DEBUG")
131:<<<<<<< HEAD <- JP側
132:	# Best-effort ensure NVDA is not running to release nvda.log handles.
133:	try:
134:		process.run_process(
135:			"taskkill /IM nvda.exe /T /F",
136:			shell=True,
137:		)
138:	except Exception:
139:		pass
140:	# Retry removal to avoid transient file locks (e.g. nvda.log)
141:	profilePath = _pJoin(stagingDir, "nvdaProfile")
142:	lastErr: Exception | None = None
143:	for _ in range(10):
144:		try:
145:			opSys.remove_directory(
146:				profilePath,
147:				recursive=True,
148:			)
149:			return
150:		except Exception as e:
151:			lastErr = e
152:			time.sleep(0.5)
153:	# If still failing after retries, raise the last error
154:	if lastErr:
155:		raise lastErr
156:======= <- 分岐点
157:	opSys.remove_directory(
158:		_pJoin(stagingDir, "nvdaProfile"),
159:		recursive=True,
160:	)
161:
162:
163:def _configModels(modelsDirectory: str) -> None:
164:	from .mockModels import MockVisionEncoderDecoderGenerator
165:
166:	generator = MockVisionEncoderDecoderGenerator(randomSeed=8)
167:	generator.generateAllFiles(modelsDirectory)
168:
169:
170:def _shouldGenerateMockModel(iniPath: str) -> bool:
171:	# Read original lines
172:	with open(iniPath, "r", encoding="utf-8") as f:
173:		lines = f.readlines()
174:
175:	for line in lines:
176:		# Detect section headers
177:		stripLine = line.strip()
178:		if stripLine.startswith("[") and stripLine.endswith("]"):
179:			hasCaptionSection = stripLine.lower() == "[automatedimagedescriptions]"
180:			if hasCaptionSection:
181:				return True
````n
---

### 16. tests/unit/test_brailleTables.py

**コンフリクト数**: 1

**コンフリクト開始行**: 23

**最初のコンフリクト周辺（行 18 - 73）**:

````n18:
19:	def test_tableExistence(self):
20:		"""Tests whether all defined tables exist."""
21:		tables = brailleTables.listTables()
22:		for table in tables:
23:<<<<<<< HEAD <- JP側
24:			tables_dir = brailleTables.TABLES_DIR
25:			if table.displayName in (
26:				"Japanese 6 dot computer braille",
27:				"Japanese 6 dot with UEB grade 2",
28:				"Japanese 6 dot with English (U.S.) grade 2",
29:				"Japanese 6 dot kanji braille",
30:			):
31:				tables_dir = brailleTables.TABLES_DIR_JP
32:			self.assertTrue(
33:				os.path.isfile(os.path.join(tables_dir, table.fileName)),
34:				msg="{table} table not found".format(table=table.displayName),
35:			)
36:======= <- 分岐点
37:			with self.subTest(table=table.fileName):
38:				self.assertTrue(
39:					os.path.isfile(os.path.join(brailleTables.TABLES_DIR, table.fileName)),
40:					msg="{table} table not found".format(table=table.displayName),
41:				)
42:>>>>>>> nvaccess/beta <- 上流側
43:
44:	def test_renamedTableExistence(self):
45:		"""Tests whether all defined renamed tables are part of the actual list of tables."""
46:		tableNames = [table.fileName for table in brailleTables.listTables()]
47:		for name in brailleTables.RENAMED_TABLES.values():
48:			with self.subTest(name=name):
49:				self.assertIn(name, tableNames)
50:
51:
52:class TestTranslate(unittest.TestCase):
53:	"""Ensures that all tables can be used for translation."""
54:
55:	def test_translate(self):
56:		"""Tests whether all tables can be used for translation."""
57:		tables = brailleTables.listTables()
58:		for table in tables:
59:			if not table.output:
60:				continue
61:			with self.subTest(table=table.fileName):
62:				try:
63:					louisHelper.translate([table.fileName, "braille-patterns.cti"], "test")
64:				except Exception as e:
65:					self.fail(f"Translation failed for {table.displayName}: {e}")
66:
67:	def test_backtranslate(self):
68:		"""Tests whether all tables can be used for back-translation."""
69:		tables = brailleTables.listTables()
70:		for table in tables:
71:			if not table.input:
72:				continue
73:			with self.subTest(table=table.fileName):
````n
---

### 17. uv.lock

**コンフリクト数**: 14

**コンフリクト開始行**: 3, 105, 129, 237, 394, 442, 548, 755, 828, 952, 981, 1260, 1352, 1368

**最初のコンフリクト周辺（行 1 - 53）**:

````n1:version = 1
2:revision = 3
3:<<<<<<< HEAD <- JP側
4:requires-python = "==3.11.*"
5:======= <- 分岐点
6:requires-python = "==3.13.*"
7:>>>>>>> nvaccess/beta <- 上流側
8:resolution-markers = [
9:    "sys_platform == 'win32'",
10:]
11:supported-markers = [
12:    "sys_platform == 'win32'",
13:]
14:
15:[manifest]
16:members = [
17:    "nvda",
18:    "nvda-misc-deps",
19:]
20:
21:[[package]]
22:name = "alabaster"
23:version = "1.0.0"
24:source = { registry = "https://pypi.org/simple" }
25:sdist = { url = "https://files.pythonhosted.org/packages/a6/f8/d9c74d0daf3f742840fd818d69cfae176fa332022fd44e3469487d5a9420/alabaster-1.0.0.tar.gz", hash = "sha256:c00dca57bca26fa62a6d7d0a9fcce65f3e026e9bfe33e9c538fd3fbb2144fd9e", size = 24210, upload-time = "2024-07-26T18:15:03.762Z" }
26:wheels = [
27:    { url = "https://files.pythonhosted.org/packages/7e/b3/6b4067be973ae96ba0d615946e314c5ae35f9f993eca561b356540bb0c2b/alabaster-1.0.0-py3-none-any.whl", hash = "sha256:fc6786402dc3fcb2de3cabd5fe455a2db534b371124f1f21de8731783dec828b", size = 13929, upload-time = "2024-07-26T18:15:02.05Z" },
28:]
29:
30:[[package]]
31:name = "appdirs"
32:version = "1.4.4"
33:source = { registry = "https://pypi.org/simple" }
34:sdist = { url = "https://files.pythonhosted.org/packages/d7/d8/05696357e0311f5b5c316d7b95f46c669dd9c15aaeecbb48c7d0aeb88c40/appdirs-1.4.4.tar.gz", hash = "sha256:7d5d0167b2b1ba821647616af46a749d1c653740dd0d2415100fe26e27afdf41", size = 13470, upload-time = "2020-05-11T07:59:51.037Z" }
35:wheels = [
36:    { url = "https://files.pythonhosted.org/packages/3b/00/2344469e2084fb287c2e0b57b72910309874c3245463acd6cf5e3db69324/appdirs-1.4.4-py2.py3-none-any.whl", hash = "sha256:a841dacd6b99318a741b166adb07e19ee71a274450e68237b4650ca1055ab128", size = 9566, upload-time = "2020-05-11T07:59:49.499Z" },
37:]
38:
39:[[package]]
40:name = "attrs"
41:version = "23.2.0"
42:source = { registry = "https://pypi.org/simple" }
43:sdist = { url = "https://files.pythonhosted.org/packages/e3/fc/f800d51204003fa8ae392c4e8278f256206e7a919b708eef054f5f4b650d/attrs-23.2.0.tar.gz", hash = "sha256:935dc3b529c262f6cf76e50877d35a4bd3c1de194fd41f47a2b7ae8f19971f30", size = 780820, upload-time = "2023-12-31T06:30:32.926Z" }
44:wheels = [
45:    { url = "https://files.pythonhosted.org/packages/e0/44/827b2a91a5816512fcaf3cc4ebc465ccd5d598c45cefa6703fcf4a79018f/attrs-23.2.0-py3-none-any.whl", hash = "sha256:99b87a485a5820b23b879f04c2305b44b951b502fd64be915879d77a7e8fc6f1", size = 60752, upload-time = "2023-12-31T06:30:30.772Z" },
46:]
47:
48:[[package]]
49:name = "babel"
50:version = "2.17.0"
51:source = { registry = "https://pypi.org/simple" }
52:sdist = { url = "https://files.pythonhosted.org/packages/7d/6b/d52e42361e1aa00709585ecc30b3f9684b3ab62530771402248b1b1d6240/babel-2.17.0.tar.gz", hash = "sha256:0c54cffb19f690cdcc52a3b50bcbf71e07a808d1c80d549f2459b9d2cf0afb9d", size = 9951852, upload-time = "2025-02-01T15:17:41.026Z" }
53:wheels = [
````n
---


## 解決方針メモ

各ファイルの解決方針は projectDocs/jp/merge-issues-beta-2025-11.md を参照してください。

## 次のステップ

1. 各コンフリクトを projectDocs/jp/merge-issues-beta-2025-11.md の解決方針に従って解決
2. uv.lock はコンフリクト解決後に 'uv lock --upgrade' で再生成
3. source/locale/ja/LC_MESSAGES/nvda.po は msgmerge で上流 pot に追随
4. 解決後、ビルドとテストを実行して確認

