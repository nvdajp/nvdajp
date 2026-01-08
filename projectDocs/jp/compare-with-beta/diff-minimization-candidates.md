# 差分最小化候補リスト

**生成日時**: 2026-01-08 23:46:14

## 概要

このレポートは、projectDocs/jp/compare-with-beta/generated/ 内のMarkdownファイルを解析して、
JP PATCHマーカーがない差分を特定し、本家版の変更を適用する候補をリストアップしたものです。

### 統計

- **JP PATCHマーカーがない差分**: 14 ファイル
- **JP PATCHマーカーがある差分**: 48 ファイル（保持すべきJP固有の変更）

## 優先順位の説明

1. **優先度1**: 明らかなマージ漏れ（例: screenCurtain統合）
2. **優先度2**: 明らかなマージ漏れ（例: registry.pyのリファクタリング）
3. **優先度3**: コード変更（要確認）
4. **優先度4**: ログメッセージの更新
5. **優先度5**: Copyright更新（低優先度）
6. **優先度6**: その他の変更（要確認）

## 適用候補（優先順位順）

### 🔴 **最優先**: `tests\unit\test_visionEnhancementProviders\test_magnificationAPI.py`

- **優先度**: 1
- **理由**: 明らかなマージ漏れ: screenCurtain統合
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: screenCurtain_merge_missing

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_visionEnhancementProviders\\test_magnificationAPI.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_visionEnhancementProviders\\test_magnificationAPI.py"
index ec86c75..fe46b23 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_visionEnhancementProviders\\test_magnificationAPI.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_visionEnhancementProviders\\test_magnificationAPI.py"
@@ -7,17 +7,15 @@
 
 import unittest
 
-from screenCurtain._screenCurtain import TRANSFORM_BLACK
-from winBindings import magnification
-from winBindings.magnification import MAGCOLOREFFECT
+from visionEnhancementProviders.screenCurtain import Magnification, TRANSFORM_BLACK, MAGCOLOREFFECT
 
 
 class _Test_MagnificationAPI(unittest.TestCase):
 	def setUp(self):
-		self.assertTrue(magnification.MagInitialize())
+		self.assertTrue(Magnification.MagInitialize())
 
 	def tearDown(self):
-		self.assertTrue(magnification.MagUninitialize())
+		self.assertTrue(Magnification.MagUninitialize())
 
 
 class Test_ScreenCurtain(_Test_MagnificationAPI):
@@ -34,7 +32,7 @@ def _isIdentityMatrix(self, magTransformMatrix: MAGCOLOREFFECT) -> bool:
 
 	def setUp(self):
 		super().setUp()
-		resultEffect = magnification.MagGetFullscreenColorEffect()
+		resultEffect = Magnification.MagGetFullscreenColorEffect()
 		if not self._isIdentityMatrix(resultEffect):
 			# If the resultEffect is not the identity matrix, skip the test.
 			# This is because a full screen colour effect is already set external to testing.
@@ -45,9 +43,9 @@ def setUp(self):
 		return
 
 	def test_setAndConfirmBlackFullscreenColorEffect(self):
-		result = magnification.MagSetFullscreenColorEffect(TRANSFORM_BLACK)
+		result = Magnification.MagSetFullscreenColorEffect(TRANSFORM_BLACK)
 		self.assertTrue(result)
-		resultEffect = magnification.MagGetFullscreenColorEffect()
+		resultEffect = Magnification.MagGetFullscreenColorEffect()
 		for i in range(5):
 			for j in range(5):
 				with self.subTest(i=i, j=j):
@@ -60,9 +58,9 @@ def test_setAndConfirmBlackFullscreenColorEffect(self):
 
 class Test_Mouse(_Test_MagnificationAPI):
 	def test_MagShowSystemCursor(self):
... (残り 8 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚪ **低優先度**: `tests\checkPot.py`

- **優先度**: 5
- **理由**: Copyright更新（低優先度）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: copyright_update

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\checkPot.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\checkPot.py"
index f04efd9..c67747c 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\checkPot.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\checkPot.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2017-2025 NV Access Limited, Ethan Holliger, Dinesh Kaushal, Leonard de Ruijter,
+# Copyright (C) 2017-2023 NV Access Limited, Ethan Holliger, Dinesh Kaushal, Leonard de Ruijter,
 # Joseph Lee, Julien Cochuyt, Łukasz Golonka, Cyrille Bougot
 # This file may be used under the terms of the GNU General Public License, version 2 or later.
 # For more details see: https://www.gnu.org/licenses/gpl-2.0.html
@@ -136,8 +136,8 @@ def checkPot(fileName):
 					# 	"keys are passed to the application"
 					msgid = ""
 					for line in pot:
-						if line.startswith("msgstr ") or line.startswith("msgid_plural"):
-							# This begins the translated or plural message, so msgid has ended.
+						if line.startswith("msgstr "):
+							# This begins the translated message, so msgid has ended.
 							break
 						msgid += getStringFromLine(line)
 				else:
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚪ **低優先度**: `tests\system\robot\vscodeTests.py`

- **優先度**: 5
- **理由**: Copyright更新（低優先度）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: copyright_update

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\system\\robot\\vscodeTests.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\robot\\vscodeTests.py"
index 4dc9157..c9ef115 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\system\\robot\\vscodeTests.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\robot\\vscodeTests.py"
@@ -1,205 +1,19 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2025 NV Access Limited, Bill Dengler
-# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
-# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
+# Copyright (C) 2025 Bill Dengler
+# This file is covered by the GNU General Public License.
+# See the file COPYING for more details.
+
 
 from robot.libraries.BuiltIn import BuiltIn
 from SystemTestSpy import _getLib
 import NvdaLib as _NvdaLib
-from typing import TYPE_CHECKING
-
-if TYPE_CHECKING:
-	from VSCodeLib import VSCodeLib
 
 _builtIn: BuiltIn = BuiltIn()
-_vscode: "VSCodeLib" = _getLib("VSCodeLib")
-
-_UNTITLED_FILE_FORMAT = "Untitled-{number}"
+_vscode = _getLib("VSCodeLib")
 
 
-def status_line_is_available():
-	"""Ensure NVDA+end does not report "no status line found"."""
+def vs_code_status_line_is_available():
+	"""Start Visual Studio Code and ensure NVDA+end does not report "no status line found"."""
 	_vscode.start_vscode()
 	speech = _NvdaLib.getSpeechAfterKey("NVDA+end")
 	_builtIn.should_not_contain(speech, "no status line found")
-
-
-def sidebar_toggle_announced():
-	"""Ensure control+b announces sidebar shown/hidden."""
-	_vscode.start_vscode()
-	speech = _NvdaLib.getSpeechAfterKey("control+b")
-	_builtIn.should_contain(speech, "Side Bar hidden")
-	speech = _NvdaLib.getSpeechAfterKey("control+b")
-	_builtIn.should_contain(speech, "Side Bar shown")
-
-
-def command_palette():
-	"""Ensure the command palette is announced when activated and can be navigated."""
-	_vscode.start_vscode()
... (残り 167 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚪ **低優先度**: `tests\unit\objectProvider.py`

- **優先度**: 5
- **理由**: Copyright更新（低優先度）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: copyright_update

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\objectProvider.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\objectProvider.py"
index 43e9382..9f2fa13 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\objectProvider.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\objectProvider.py"
@@ -1,22 +1,19 @@
+# tests/unit/objectProvider.py
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2017-2025 NV Access Limited, Babbage B.V.
-# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
-# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
+# This file is covered by the GNU General Public License.
+# See the file COPYING for more details.
+# Copyright (C) 2017 NV Access Limited, Babbage B.V.
 
 """Fake object provider implementation for testing of code which uses NVDAObjects."""
 
 from NVDAObjects import NVDAObject
 import controlTypes
-from typing import Any
 
 
 class PlaceholderNVDAObject(NVDAObject):
 	processID = None  # Must be implemented to instantiate.
 	windowThreadID = 0  # Must be implemented for inputCore tests
 
-	def _isEqual(self, other: Any) -> bool:
-		return False
-
 
 class NVDAObjectWithRole(PlaceholderNVDAObject):
 	"""An object that accepts a role as one of its construction parameters.
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `ci\scripts\mozillaSyms.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\ci\\scripts\\mozillaSyms.py" "b/F:\\nvda\\gh\\alphajp-260109\\ci\\scripts\\mozillaSyms.py"
index 763d254..ec6f391 100644
--- "a/F:\\nvda\\gh\\beta\\ci\\scripts\\mozillaSyms.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\ci\\scripts\\mozillaSyms.py"
@@ -13,10 +13,10 @@
 import requests
 
 SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
-REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
-DUMP_SYMS = os.path.join(REPO_ROOT, "dump_syms.exe")
-NVDA_SOURCE = os.path.join(REPO_ROOT, "source")
+DUMP_SYMS = os.path.join(os.path.dirname(SCRIPT_DIR), "miscDeps", "tools", "dump_syms.exe")
+NVDA_SOURCE = os.path.join(os.path.dirname(SCRIPT_DIR), "source")
 NVDA_LIB = os.path.join(NVDA_SOURCE, "lib")
+NVDA_LIB64 = os.path.join(NVDA_SOURCE, "lib64")
 ZIP_FILE = os.path.join(SCRIPT_DIR, "mozillaSyms.zip")
 URL = "https://symbols.mozilla.org/upload/"
 
@@ -28,10 +28,10 @@
 	"nvdaHelperRemote.dll",
 ]
 DLL_FILES = [
-	os.path.join(NVDA_LIB, arch, dll)
+	f
 	for dll in DLL_NAMES
-	# We need symbols for all supported architectures.
-	for arch in ("x86", "x64", "arm64", "arm64ec")
+	# We need both the 32 bit and 64 bit symbols.
+	for f in (os.path.join(NVDA_LIB, dll), os.path.join(NVDA_LIB64, dll))
 ]
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\_remoteClient\localMachine.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\localMachine.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\localMachine.py"
index 7e1f827..1e401b5 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\localMachine.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\localMachine.py"
@@ -98,24 +98,6 @@ class LocalMachine:
 	    - :mod:`transport` - Network transport layer
 	"""
 
-	_receivingBraille: bool
-	"""Internal storage for :attr:`receivingBraille`."""
-
-	@property
-	def receivingBraille(self) -> bool:
-		"""When True, braille output comes from remote"""
-		return self._receivingBraille
-
-	@receivingBraille.setter
-	def receivingBraille(self, val: bool):
-		self._receivingBraille = val
-		# Let the braille handler know that whether it's enabled has changed.
-		# This needs to be blocking,
-		# otherwise there is a race condition between
-		# our handling of `ui.message`,
-		# and the braille handler clearing the message buffer.
-		braille.handler._refreshEnabled(block=True)
-
 	def __init__(self) -> None:
 		"""Initialize the local machine controller.
 
@@ -124,24 +106,13 @@ def __init__(self) -> None:
 		self.isMuted: bool = False
 		"""When True, most remote commands will be ignored"""
 
-		self.receivingBraille = False
+		self.receivingBraille: bool = False
+		"""When True, braille output comes from remote"""
 
 		self._cachedSizes: list[int] | None = None
 		"""Cached braille display sizes from remote machines"""
 
-		self._showingLocalUiMessage: bool = False
-		"""Whether we're currently showing a `ui.message` while showing remote braille."""
-
-		self._oldReceivingBraille: bool = False
-		"""Cached value of `self.receivingBraille` for when we show a `ui.message`."""
-
-		self._lastCells: list[int] = []
-		"""Cached cells for display when we return from controling the local computer, or displaying a `ui.message`."""
-
 		braille.decide_enabled.register(self.handleDecideEnabled)
... (残り 88 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\speech\__init__.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\speech\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\speech\\__init__.py"
index 830b57b..d9a666a 100644
--- "a/F:\\nvda\\gh\\beta\\source\\speech\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\speech\\__init__.py"
@@ -35,7 +35,6 @@
 	getTextInfoSpeech,
 	IDT_BASE_FREQUENCY,
 	IDT_MAX_SPACES,
-	getIndentToneDuration,
 	isBlank,
 	LANGS_WITH_CONJUNCT_CHARS,
 	pauseSpeech,
@@ -115,7 +114,6 @@
 	"getTextInfoSpeech",
 	"IDT_BASE_FREQUENCY",
 	"IDT_MAX_SPACES",
-	"getIndentToneDuration",
 	"isBlank",
 	"LANGS_WITH_CONJUNCT_CHARS",
 	"pauseSpeech",
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `tests\system\libraries\NvdaLib.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\system\\libraries\\NvdaLib.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\NvdaLib.py"
index 7bae843..5d2697d 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\system\\libraries\\NvdaLib.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\NvdaLib.py"
@@ -100,12 +100,15 @@ def findInstalledNVDAPath(self) -> _Optional[str]:
 		NVDAFilePath = _pJoin(_expandvars("%PROGRAMFILES%"), "nvda", "nvda.exe")
 		legacyNVDAFilePath = _pJoin(_expandvars("%PROGRAMFILES%"), "NVDA", "nvda.exe")
 		exeErrorMsg = f"Unable to find installed NVDA exe. Paths tried: {NVDAFilePath}, {legacyNVDAFilePath}"
-		try:
-			opSys.file_should_exist(NVDAFilePath)
+		# Check if file exists before using file_should_exist to avoid early failure during import
+		import os
+		if os.path.isfile(NVDAFilePath):
 			return NVDAFilePath
-		except AssertionError:
-			# Older versions of NVDA (<=2020.4) install the exe in NVDA\nvda.exe
-			opSys.file_should_exist(legacyNVDAFilePath, exeErrorMsg)
+		elif os.path.isfile(legacyNVDAFilePath):
+			return legacyNVDAFilePath
+		else:
+			# If neither file exists, raise error with helpful message
+			opSys.file_should_exist(NVDAFilePath, exeErrorMsg)
 			return legacyNVDAFilePath
 
 	def ensureInstallerPathsExist(self):
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `tests\system\libraries\VSCodeLib.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\system\\libraries\\VSCodeLib.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\VSCodeLib.py"
index 8f18c92..7a42199 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\system\\libraries\\VSCodeLib.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\VSCodeLib.py"
@@ -55,24 +55,13 @@ def _findCodeLauncher() -> str:
 				return f'"{resolved}"'
 		raise AssertionError("Visual Studio Code launcher not found. Is it installed?")
 
-	def start_vscode(self, targetPath: str | None = None) -> _Window:
-		"""Start Visual Studio Code.
-
-		:param targetPath: The path to the folder or file to open, defaults to a temporary directory.
-		:return: The window object for the started Visual Studio Code instance
-		"""
+	def start_vscode(self) -> _Window:
 		launcher = self._findCodeLauncher()
 		if VSCodeLib._testTempDir is None:
 			VSCodeLib._testTempDir = _tempfile.mkdtemp(prefix="nvdatest")
 		userDataDir = _os.path.join(VSCodeLib._testTempDir, "vscodeUserData")
 		_os.makedirs(userDataDir, exist_ok=True)
 
-		if targetPath is None:
-			targetPath = _os.path.join(VSCodeLib._testTempDir, "testDirectory")
-
-		if not _os.path.exists(targetPath):
-			_os.makedirs(targetPath, exist_ok=True)
-
 		# Prepare user settings to suppress welcome/startup screen
 		userSettingsDir = _os.path.join(userDataDir, "User")
 		_os.makedirs(userSettingsDir, exist_ok=True)
@@ -108,7 +97,6 @@ def start_vscode(self, targetPath: str | None = None) -> _Window:
 			f"--skip-add-to-recently-opened "
 			f"-n "
 			f"--wait"
-			f' "{targetPath}"'
 		)
 		_builtIn.log(f"Starting Visual Studio Code: {cmd}", level="DEBUG")
 		VSCodeLib._processRFHandleForStart = _process.start_process(
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `tests\system\robot\automatedImageDescriptions.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\system\\robot\\automatedImageDescriptions.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\robot\\automatedImageDescriptions.py"
index bfbd6b3..965071e 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\system\\robot\\automatedImageDescriptions.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\robot\\automatedImageDescriptions.py"
@@ -37,7 +37,7 @@ def NVDA_Caption():
 
 	# locate graph to generate caption
 	spy.emulateKeyPress("g")
-	spy.emulateKeyPress("NVDA+g")
+	spy.emulateKeyPress("NVDA+windows+,")
 	spy.wait_for_specific_speech(
 		"visual desk access non-visual desktop access non-visual desktop access non-visual desktop access non-visual desktop access non-visual desktop access non-visual",
 	)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `tests\unit\test_braille\test_brailleDisplayDrivers.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_braille\\test_brailleDisplayDrivers.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_braille\\test_brailleDisplayDrivers.py"
index 2e2a9f8..eafe5b1 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_braille\\test_brailleDisplayDrivers.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_braille\\test_brailleDisplayDrivers.py"
@@ -5,6 +5,8 @@
 
 """Unit tests for braille display drivers."""
 
+import sysconfig
+import sys
 from brailleDisplayDrivers import seikantk
 import unittest
 import braille
@@ -178,6 +180,14 @@ def test_identifiers(self):
 					self.assertRegex(gesture, braille.BrailleDisplayGesture.ID_PARTS_REGEX)
 
 
+@unittest.skipUnless(
+	sysconfig.get_platform() == "win32",
+	"BRLTTY is only supported on 32-bit Windows",
+)
+@unittest.skipUnless(
+	sys.version_info.major == 3 and sys.version_info.minor == 11,
+	"Skipping brlapi tests unless Python 3.11",
+)
 class TestBRLTTY(unittest.TestCase):
 	"""Tests the integrity of the bundled brlapi module."""
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `tests\unit\test_braille\test_routing.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_braille\\test_routing.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_braille\\test_routing.py"
index 32fff42..6f38237 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_braille\\test_routing.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_braille\\test_routing.py"
@@ -48,6 +48,14 @@ def setUp(self):
 		api.setReviewPosition(caret)
 		braille.handler.handleReviewMove()
 
+	@unittest.skip(
+		"See projectDocs/jp/test-routing-failures.md for details. "
+		"Investigation revealed that even when ReviewCursorManagerRegion is reverted to upstream's "
+		"empty class implementation, these tests still fail in the nvdajp branch. This suggests "
+		"the issue may not be solely due to nvdajp-specific code, but could involve test "
+		"preconditions, environment differences, or other factors. These tests are temporarily "
+		"skipped pending further investigation."
+	)
 	def test_moveCaret_never_moveReviewAndActivate(self):
 		"""Test that routing action on a cell will move the review cursor when routing changes the position,
 		whereas it should activate the current position when the review cursor is already at that position.
@@ -78,6 +86,14 @@ def test_moveCaret_never_moveReviewAndActivate(self):
 		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
 		self.assertEqual(caret, self.caret)
 
+	@unittest.skip(
+		"See projectDocs/jp/test-routing-failures.md for details. "
+		"Investigation revealed that even when ReviewCursorManagerRegion is reverted to upstream's "
+		"empty class implementation, these tests still fail in the nvdajp branch. This suggests "
+		"the issue may not be solely due to nvdajp-specific code, but could involve test "
+		"preconditions, environment differences, or other factors. These tests are temporarily "
+		"skipped pending further investigation."
+	)
 	def test_moveCaret_never_instantActivate(self):
 		"""Test that routing action on a cell will activate the current position
 		when the review cursor is already at that position.
@@ -97,6 +113,14 @@ def test_moveCaret_never_instantActivate(self):
 		caret = self.cm.makeTextInfo(textInfos.POSITION_CARET)
 		self.assertEqual(caret, self.caret)
 
+	@unittest.skip(
+		"See projectDocs/jp/test-routing-failures.md for details. "
+		"Investigation revealed that even when ReviewCursorManagerRegion is reverted to upstream's "
+		"empty class implementation, these tests still fail in the nvdajp branch. This suggests "
+		"the issue may not be solely due to nvdajp-specific code, but could involve test "
+		"preconditions, environment differences, or other factors. These tests are temporarily "
+		"skipped pending further investigation."
+	)
 	def test_moveCaret_always_moveReviewAndActivate(self):
 		"""Test that routing action on a cell will move the review cursor when routing changes the position,
 		whereas it should activate the current position when the review cursor is already at that position.
@@ -127,6 +151,14 @@ def test_moveCaret_always_moveReviewAndActivate(self):
... (残り 14 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `tests\unit\test_remote\test_remoteClient.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_remote\\test_remoteClient.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_remote\\test_remoteClient.py"
index e5df9c4..ce524b7 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_remote\\test_remoteClient.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_remote\\test_remoteClient.py"
@@ -9,8 +9,6 @@
 from _remoteClient.connectionInfo import ConnectionInfo, ConnectionMode
 from _remoteClient.protocol import RemoteMessageType
 from gui.message import ReturnCode
-from keyboardHandler import KeyboardInputGesture
-from utils.security import post_sessionLockStateChanged
 
 
 # Fake implementations for testing
@@ -21,14 +19,6 @@ def __init__(self):
 	def terminate(self):
 		pass
 
-	def setClipboardText(self, *a, **k): ...
-	def speak(self, *a, **k): ...
-	def cancelSpeech(self, *a, **k): ...
-	def pauseSpeech(self, *a, **k): ...
-	def beep(self, *a, **k): ...
-	def playWave(self, *a, **k): ...
-	def display(self, *a, **k): ...
-
 
 class FakeMenu:
 	def __init__(self):
@@ -42,7 +32,6 @@ def Check(self, value):
 			self.checked = value
 
 	def handleConnected(self, *args, **kwargs): ...
-	def handleConnecting(self, *a, **k): ...
 
 
 class FakeTransport:
@@ -242,60 +231,6 @@ def test_disconnect(self):
 			self.client.disconnect()
 		fakeControl.close.assert_called_once()
 
-	def test_lockWhileSendingKeys(self):
-		# the `onConnectedAsLeader` method is decorated with `alwaysCallAfter`.
-		# This causes issues here, so unwrap it.
-		with patch(
-			"_remoteClient.client.RemoteClient.onConnectedAsLeader",
-			rcClient.RemoteClient.onConnectedAsLeader.__wrapped__,
-		):
-			connInfo = ConnectionInfo(
-				hostname="localhost",
-				mode=ConnectionMode.LEADER,
... (残り 47 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `tests\unit\test_winVersion.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_winVersion.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_winVersion.py"
index 4dbe9e9..47e80ce 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_winVersion.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_winVersion.py"
@@ -89,7 +89,7 @@ def test_winVerUnknownBuildToReleaseName(self):
 	def test_winVerProcessorArchitecture(self):
 		# See if processor architecture matches what Windows says.
 		# Use os.environ to guard against platform.machine() giving odd results.
-		actualArchitecture = os.environ["PROCESSOR_ARCHITECTURE"]
+		actualArchitecture = os.environ.get("PROCESSOR_ARCHITEW6432", os.environ["PROCESSOR_ARCHITECTURE"])
 		self.assertEqual(winVersion.getWinVer().processorArchitecture, actualArchitecture)
 
 	def test_winVerUnknownWin11BuildToReleaseName(self):
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

## 注意事項

1. **各変更を小さな単位で適用**: 一度に複数のファイルを変更しない
2. **各変更後に検証**: ビルド・型チェック・単体テストを実行
3. **問題があれば即座にロールバック**: Gitで簡単に戻せるように、各変更を個別のコミットにする
4. **JP PATCHマーカーがある差分は保持**: これらはJP固有の変更なので、本家版の変更を適用しない

## 次のステップ

1. 優先度1-2のファイルから順に確認・適用
2. 各ファイルについて：
   - 本家版のファイルを確認: `F:\nvda\gh\beta\tests\unit\test_winVersion.py`
   - 現在のファイルを確認: `source\tests\unit\test_winVersion.py`
   - 差分を確認: projectDocs/jp/compare-with-beta/generated/source_tests_unit_test_winVersion_py.md
   - 本家版の変更を適用
   - ビルド・型チェック・テストを実行
   - 問題なければコミット

## 参考

- 元の比較結果: `projectDocs/jp/compare-with-beta/summary.md`
- ファイル一覧: `projectDocs/jp/compare-with-beta/file-list.md`