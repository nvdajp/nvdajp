# 差分最小化候補リスト

**生成日時**: 2026-01-08 22:28:21

## 概要

このレポートは、projectDocs/jp/compare-with-beta/generated/ 内のMarkdownファイルを解析して、
JP PATCHマーカーがない差分を特定し、本家版の変更を適用する候補をリストアップしたものです。

### 統計

- **JP PATCHマーカーがない差分**: 98 ファイル
- **JP PATCHマーカーがある差分**: 37 ファイル（保持すべきJP固有の変更）

## 優先順位の説明

1. **優先度1**: 明らかなマージ漏れ（例: screenCurtain統合）
2. **優先度2**: 明らかなマージ漏れ（例: registry.pyのリファクタリング）
3. **優先度3**: コード変更（要確認）
4. **優先度4**: ログメッセージの更新
5. **優先度5**: Copyright更新（低優先度）
6. **優先度6**: その他の変更（要確認）

## 適用候補（優先順位順）

### 🔴 **最優先**: `source\config\__init__.py`

- **優先度**: 1
- **理由**: 明らかなマージ漏れ: screenCurtain統合
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: screenCurtain_merge_missing

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\config\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\__init__.py"
index 0fbd3cd..edc5c9f 100644
--- "a/F:\\nvda\\gh\\beta\\source\\config\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\__init__.py"
@@ -154,7 +154,7 @@ def isInstalledCopy() -> bool:
 		log.error("Unable to query isInstalledCopy registry key", exc_info=True)
 		return False
 
-	k.Close()
+	winreg.CloseKey(k)
 	try:
 		return os.stat(instDir) == os.stat(globalVars.appDir)
 	except (WindowsError, FileNotFoundError):
@@ -318,10 +318,10 @@ def setSystemConfigToCurrentConfig():
 			raise RuntimeError("Slave failure")
 
 
-def _setSystemConfig(fromPath, *, prefix=sys.prefix):
+def _setSystemConfig(fromPath):
 	import installer
 
-	toPath = os.path.join(prefix, "systemConfig")
+	toPath = os.path.join(sys.prefix, "systemConfig")
 	log.debug("Copying config to systemconfig dir: %s", toPath)
 	if os.path.isdir(toPath):
 		installer.tryRemoveFile(toPath)
@@ -418,7 +418,6 @@ class ConfigManager(object):
 		"remote",
 		"automatedImageDescriptions",
 		"math",
-		"screenCurtain",
 	}
 	"""
 	Sections that only apply to the base configuration;
@@ -668,8 +667,7 @@ def createProfile(self, name):
 		@type name: str
 		@raise ValueError: If a profile with this name already exists.
 		"""
-		if not NVDAState.shouldWriteToDisk():
-			log.debug("Not creating configuration profile, as shouldWriteToDisk returned False.")
+		if globalVars.appArgs.secure:
 			return
 		if not name:
 			raise ValueError("Missing name.")
@@ -690,8 +688,7 @@ def deleteProfile(self, name):
 		@type name: str
 		@raise LookupError: If the profile doesn't exist.
 		"""
-		if not NVDAState.shouldWriteToDisk():
-			log.debug("Not deleting profile, as shouldSaveToDisk returned False.")
... (残り 25 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### 🔴 **最優先**: `source\config\profileUpgradeSteps.py`

- **優先度**: 1
- **理由**: 明らかなマージ漏れ: screenCurtain統合
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: screenCurtain_merge_missing

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\config\\profileUpgradeSteps.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\profileUpgradeSteps.py"
index 8c4a22e..d19a848 100644
--- "a/F:\\nvda\\gh\\beta\\source\\config\\profileUpgradeSteps.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\profileUpgradeSteps.py"
@@ -622,16 +622,3 @@ def upgradeConfigFrom_18_to_19(profile: ConfigObj):
 		f"Converted '{key}' with value {oldValue} to '{newKey}' with value {newValue}"
 		f" ({ReportSpellingErrors(newValue).name}). The old key '{key}' has been deleted.",
 	)
-
-
-def upgradeConfigFrom_19_to_20(profile: ConfigObj):
-	"""Move Screen Curtain settings from vision to root."""
-	try:
-		# We must copy the old settings,
-		# otherwise configobj will write the new settings as a subsection of the last root section in the config
-		profile["screenCurtain"] = profile["vision"]["screenCurtain"].copy()
-	except KeyError:
-		log.debug("No vision enhancement provider-based Screen Curtain settings exist. No action taken.")
-		return
-	del profile["vision"]["screenCurtain"]
-	log.debug("Moved Screen Curtain settings from ['vision']['screenCurtain'] to ['screenCurtain'].")
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### 🔴 **最優先**: `source\core.py`

- **優先度**: 1
- **理由**: 明らかなマージ漏れ: screenCurtain統合
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: screenCurtain_merge_missing

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\core.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\core.py"
index 113b88a..33d62bc 100644
--- "a/F:\\nvda\\gh\\beta\\source\\core.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\core.py"
@@ -322,12 +322,9 @@ def resetConfiguration(factoryDefaults=False):
 	import hwIo
 	import tones
 	import audio
-	import screenCurtain
 
 	log.debug("Terminating vision")
 	vision.terminate()
-	log.debug("Terminating Screen Curtain")
-	screenCurtain.terminate()
 	log.debug("Terminating braille")
 	braille.terminate()
 	log.debug("Terminating brailleInput")
@@ -391,8 +388,6 @@ def resetConfiguration(factoryDefaults=False):
 	# Vision
 	log.debug("initializing vision")
 	vision.initialize()
-	log.debug("initializing Screen Curtain")
-	screenCurtain.initialize()
 	log.debug("Reloading user and locale input gesture maps")
 	inputCore.manager.loadUserGestureMap()
 	inputCore.manager.loadLocaleGestureMap()
@@ -791,7 +786,7 @@ def main():
 	speech.initialize()
 	import mathPres
 
-	log.debug("Initializing math presentation")
+	log.debug("Initializing MathPlayer")
 	mathPres.initialize()
 	timeSinceStart = time.time() - NVDAState.getStartTime()
 	if not globalVars.appArgs.minimal and timeSinceStart > 5:
@@ -815,12 +810,6 @@ def main():
 
 	log.debug("Initializing braille")
 	braille.initialize()
-
-	import screenCurtain
-
-	log.debug("Initializing Screen Curtain")
-	screenCurtain.initialize()
-
 	import vision
 
 	log.debug("Initializing vision")
@@ -1098,7 +1087,6 @@ def _doPostNvdaStartupAction():
 	_terminate(keyboardHandler, name="keyboard handler")
... (残り 6 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### 🔴 **最優先**: `source\gui\blockAction.py`

- **優先度**: 1
- **理由**: 明らかなマージ漏れ: screenCurtain統合
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: screenCurtain_merge_missing

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\blockAction.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\blockAction.py"
index 21fbe4a..78372d5 100644
--- "a/F:\\nvda\\gh\\beta\\source\\gui\\blockAction.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\blockAction.py"
@@ -42,9 +42,13 @@ def _isRemoteAccessDisabled() -> bool:
 def _isScreenCurtainEnabled() -> bool:
 	"""Whether screen curtain functionality is **enabled**."""
 	# Import late to avoid circular import
-	from screenCurtain import screenCurtain
+	import vision
+	from visionEnhancementProviders.screenCurtain import ScreenCurtainProvider
 
-	return screenCurtain is not None and screenCurtain.enabled
+	screenCurtainId = ScreenCurtainProvider.getSettings().getId()
+	screenCurtainProviderInfo = vision.handler.getProviderInfo(screenCurtainId)
+	isScreenCurtainRunning = bool(vision.handler.getProviderInstance(screenCurtainProviderInfo))
+	return isScreenCurtainRunning
 
 
 @dataclass
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### 🔴 **最優先**: `source\vision\visionHandler.py`

- **優先度**: 1
- **理由**: 明らかなマージ漏れ: screenCurtain統合
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: screenCurtain_merge_missing

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\vision\\visionHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\vision\\visionHandler.py"
index e3aa82d..b70d3f4 100644
--- "a/F:\\nvda\\gh\\beta\\source\\vision\\visionHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\vision\\visionHandler.py"
@@ -102,9 +102,11 @@ def postGuiInit(self) -> None:
 
 	def _getBuiltInProviderIds(self):
 		from visionEnhancementProviders.NVDAHighlighter import NVDAHighlighterSettings
+		from visionEnhancementProviders.screenCurtain import ScreenCurtainSettings
 
 		return [
 			NVDAHighlighterSettings.getId(),
+			ScreenCurtainSettings.getId(),
 		]
 
 	def _updateAllProvidersList(self):
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### 🔴 **最優先**: `source\visionEnhancementProviders\_exampleProvider_autoGui.py`

- **優先度**: 1
- **理由**: 明らかなマージ漏れ: screenCurtain統合
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: screenCurtain_merge_missing

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\visionEnhancementProviders\\_exampleProvider_autoGui.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\visionEnhancementProviders\\_exampleProvider_autoGui.py"
index df99fdc..806b875 100644
--- "a/F:\\nvda\\gh\\beta\\source\\visionEnhancementProviders\\_exampleProvider_autoGui.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\visionEnhancementProviders\\_exampleProvider_autoGui.py"
@@ -13,7 +13,7 @@
 """Example provider, which demonstrates using the automatically constructed GUI. Rename this file, removing
  the first underscore to test it with NVDA.
 
-For examples of overriding the GUI and using a custom implementation, see NVDAHighlighter.
+For examples of overriding the GUI and using a custom implementation, see NVDAHighlighter or ScreenCurtain.
 
 This example imagines that some settings are "always available", while the availability of others is unknown
 until "runtime".
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### 🔴 **最優先**: `source\winVersion.py`

- **優先度**: 1
- **理由**: 明らかなマージ漏れ: screenCurtain統合
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: screenCurtain_merge_missing

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winVersion.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winVersion.py"
index 140f0d6..797da41 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winVersion.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winVersion.py"
@@ -223,6 +223,22 @@ def isUwpOcrAvailable() -> bool:
 	return os.path.isdir(UWP_OCR_DATA_PATH)
 
 
+if NVDAState._allowDeprecatedAPI():
+
+	def isFullScreenMagnificationAvailable() -> bool:
+		"""
+		Technically this is always False. The Magnification API has been marked by MS as unsupported for
+		WOW64 applications such as NVDA. For our usages, support has been added since Windows 8, relying on our
+		testing our specific usage of the API with each Windows version since Windows 8
+		"""
+		log.debugWarning(
+			"Deprecated function called: winVersion.isFullScreenMagnificationAvailable, "
+			"use visionEnhancementProviders.screenCurtain.ScreenCurtainProvider.canStart instead.",
+			stack_info=True,
+		)
+		return True
+
+
 def __getattr__(attrName: str) -> Any:
 	"""Module level `__getattr__` used to preserve backward compatibility."""
 	if attrName == "WIN7" and NVDAState._allowDeprecatedAPI():
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### 🟠 **高優先度**: `source\_remoteClient\localMachine.py`

- **優先度**: 2
- **理由**: 明らかなマージ漏れ: registry.pyのリファクタリング
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: registry_refactor

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\localMachine.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\localMachine.py"
index 7e1f827..4221f3d 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\localMachine.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\localMachine.py"
@@ -20,7 +20,7 @@
 
 from enum import IntEnum, nonmember
 import os
-from typing import Any
+from typing import Any, Dict, List, Optional
 import winreg
 
 import winBindings.sas
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
 
-		self._cachedSizes: list[int] | None = None
+		self._cachedSizes: Optional[List[int]] = None
 		"""Cached braille display sizes from remote machines"""
 
... (残り 143 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### 🟠 **高優先度**: `source\_remoteClient\urlHandler.py`

- **優先度**: 2
- **理由**: 明らかなマージ漏れ: registry.pyのリファクタリング
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: registry_refactor

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\urlHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\urlHandler.py"
index 6b572ee..bd39535 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\urlHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\urlHandler.py"
@@ -25,7 +25,8 @@
 import sys
 import winreg
 
-from config.registry import RegistryKey, _deleteKeyAndSubkeys
+
+_REGISTRY_KEY_PATH: str = r"SOFTWARE\Classes\nvdaremote"
 
 
 def _createRegistryStructure(keyHandle: winreg.HKEYType, data: dict):
@@ -43,7 +44,7 @@ def _createRegistryStructure(keyHandle: winreg.HKEYType, data: dict):
 				try:
 					_createRegistryStructure(subkey, value)
 				finally:
-					subkey.Close()
+					winreg.CloseKey(subkey)
 			except WindowsError as e:
 				raise OSError(f"Failed to create registry subkey {name}: {e}")
 		else:
@@ -54,13 +55,42 @@ def _createRegistryStructure(keyHandle: winreg.HKEYType, data: dict):
 				raise OSError(f"Failed to set registry value {name}: {e}")
 
 
+def _deleteRegistryKeyRecursive(baseKey: int, subkeyPath: str):
+	"""Recursively deletes a registry key and all its subkeys.
+
+	:param baseKey: One of the HKEY_* constants from winreg
+	:param subkeyPath: Full registry path to the key to delete
+	:raises OSError: If deletion fails for reasons other than key not found
+	"""
+	try:
+		# Try to delete directly first
+		winreg.DeleteKey(baseKey, subkeyPath)
+	except WindowsError:
+		# If that fails, need to do recursive deletion
+		try:
+			with winreg.OpenKey(baseKey, subkeyPath, access=winreg.KEY_READ | winreg.KEY_WRITE) as key:
+				# Enumerate and delete all subkeys
+				while True:
+					try:
+						subkeyName = winreg.EnumKey(key, 0)
+						fullPath = f"{subkeyPath}\\{subkeyName}"
+						_deleteRegistryKeyRecursive(baseKey, fullPath)
+					except WindowsError:
+						break
+			# Now delete the key itself
... (残り 29 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### 🟠 **高優先度**: `source\config\registry.py`

- **優先度**: 2
- **理由**: 明らかなマージ漏れ: registry.pyのリファクタリング
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: registry_refactor

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\config\\registry.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\registry.py"
index 1ff385f..51eff3e 100644
--- "a/F:\\nvda\\gh\\beta\\source\\config\\registry.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\registry.py"
@@ -4,9 +4,6 @@
 # See the file COPYING for more details.
 
 from enum import Enum, nonmember
-import winreg
-
-from winBindings.advapi32 import RegDeleteTree
 
 
 EASE_OF_ACCESS_APP_KEY_NAME = "nvda_nvda_v1"
@@ -31,8 +28,6 @@ class RegistryKey(str, Enum):
 	NT_CURRENT_VERSION = rf"{_SOFTWARE}\Microsoft\Windows NT\CurrentVersion"
 	EASE_OF_ACCESS = rf"{NT_CURRENT_VERSION}\Accessibility"
 	EASE_OF_ACCESS_TEMP = rf"{NT_CURRENT_VERSION}\AccessibilityTemp"
-	# This should always be accessed with 64-bit view of the registry.
-	# TODO: remove winreg.KEY_WOW64_64KEY from usages when NVDA is 64-bit only.
 	EASE_OF_ACCESS_APP = rf"{EASE_OF_ACCESS}\ATs\{EASE_OF_ACCESS_APP_KEY_NAME}"
 	ADDON_PROG = rf"{_SOFTWARE}\Classes\{NVDA_ADDON_PROG_ID}"
 	ADDON_EXT = rf"{_SOFTWARE}\Classes\.{ADDON_BUNDLE_EXTENSION}"
@@ -62,14 +57,13 @@ class _RegistryKeyX86(str, Enum):  # type: ignore[reportUnusedClass]
 
 	_SOFTWARE = nonmember(r"SOFTWARE\WOW6432Node")
 	CURRENT_VERSION = rf"{_SOFTWARE}\Microsoft\Windows\CurrentVersion"
-
-
-def _deleteKeyAndSubkeys(key: int, subkey: str, access: int = 0) -> None:
-	"""Delete a registry key and all its subkeys using RegDeleteTree via winBindings.advapi32."""
-	with winreg.OpenKey(key, "", 0, winreg.KEY_WRITE | winreg.KEY_READ | access) as parent:
-		result = RegDeleteTree(
-			parent.handle,
-			subkey,
-		)
-	if result != 0:
-		raise WindowsError(result, f"RegDeleteTree failed for {subkey=}")
+	INSTALLED_COPY = rf"{CURRENT_VERSION}\Uninstall\NVDA"
+	RUN = rf"{CURRENT_VERSION}\Run"
+	NVDA = rf"{_SOFTWARE}\NVDA"
+	APP_PATH = rf"{CURRENT_VERSION}\App Paths\nvda.exe"
+	EXPLORER_ADVANCED = rf"{CURRENT_VERSION}\Explorer\Advanced"
+	SYSTEM_POLICIES = rf"{CURRENT_VERSION}\Policies\System"
+	NT_CURRENT_VERSION = rf"{_SOFTWARE}\Microsoft\Windows NT\CurrentVersion"
+	EASE_OF_ACCESS = rf"{NT_CURRENT_VERSION}\Accessibility"
+	EASE_OF_ACCESS_TEMP = rf"{NT_CURRENT_VERSION}\AccessibilityTemp"
+	EASE_OF_ACCESS_APP = rf"{EASE_OF_ACCESS}\ATs\{EASE_OF_ACCESS_APP_KEY_NAME}"
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### 🟠 **高優先度**: `source\winBindings\advapi32.py`

- **優先度**: 2
- **理由**: 明らかなマージ漏れ: registry.pyのリファクタリング
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: registry_refactor

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\advapi32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\advapi32.py"
index 383b27b..7082530 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\advapi32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\advapi32.py"
@@ -29,7 +29,6 @@
 __all__ = (
 	"OpenProcessToken",
 	"RegCloseKey",
-	"RegDeleteTree",
 	"RegOpenKeyEx",
 	"RegQueryValueEx",
 	"CreateProcessAsUser",
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚪ **低優先度**: `source\appModules\soffice.py`

- **優先度**: 5
- **理由**: Copyright更新（低優先度）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: copyright_update

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\appModules\\soffice.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\soffice.py"
index 2c6ded0..0bcd15f 100644
--- "a/F:\\nvda\\gh\\beta\\source\\appModules\\soffice.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\soffice.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
+# This file is covered by the GNU General Public License.
+# See the file COPYING for more details.
 # Copyright (C) 2006-2025 NV Access Limited, Bill Dengler, Leonard de Ruijter, Cyrille Bougot
-# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
-# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
 
 from typing import (
 	Optional,
@@ -18,7 +18,7 @@
 from controlTypes import TextPosition
 import textInfos
 import colors
-from compoundDocuments import CompoundDocument, TreeCompoundTextInfo, CompoundTextLeafTextInfo
+from compoundDocuments import CompoundDocument, TreeCompoundTextInfo
 from NVDAObjects import NVDAObject
 from NVDAObjects.IAccessible import IAccessible, IA2TextTextInfo
 from NVDAObjects.behaviors import EditableText
@@ -55,7 +55,7 @@ def get_id(obj: NVDAObject) -> str | None:
 		return obj.IA2Attributes.get("id")
 
 
-class SymphonyTextInfo(IA2TextTextInfo, CompoundTextLeafTextInfo):
+class SymphonyTextInfo(IA2TextTextInfo):
 	# C901 '_getFormatFieldFromLegacyAttributesString' is too complex
 	# Note: when working on _getFormatFieldFromLegacyAttributesString, look for opportunities to simplify
 	# and move logic out into smaller helper functions.
@@ -237,7 +237,6 @@ def _getLineOffsets(self, offset):
 		if offset == 0 and start == 0 and end == 0:
 			# HACK: Symphony doesn't expose any characters at all on empty lines, but this means we don't ever fetch the list item prefix in this case.
 			# Fake a character so that the list item prefix will be spoken on empty lines.
-			# Note: Observations in LibreOffice revealed that this might no longer be necessary.
 			return (0, 1)
 		return start, end
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚪ **低優先度**: `source\compoundDocuments.py`

- **優先度**: 5
- **理由**: Copyright更新（低優先度）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: copyright_update

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\compoundDocuments.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\compoundDocuments.py"
index c2fe19e..1e24efb 100644
--- "a/F:\\nvda\\gh\\beta\\source\\compoundDocuments.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\compoundDocuments.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2010-2025 NV Access Limited, Bram Duvigneau, Leonard de Ruijter
-# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
-# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
+# This file is covered by the GNU General Public License.
+# See the file COPYING for more details.
+# Copyright (C) 2010-2024 NV Access Limited, Bram Duvigneau
 
 from typing import (
 	Optional,
@@ -12,7 +12,6 @@
 import textUtils
 import winUser
 import textInfos
-import textInfos.offsets
 import controlTypes
 import eventHandler
 from NVDAObjects import NVDAObject
@@ -504,15 +503,6 @@ def _get_boundingRects(self):
 		return rects
 
 
-class CompoundTextLeafTextInfo(textInfos.offsets.OffsetsTextInfo):
-	"""A mixin class for leafs within a CompoundTextInfo that utilize offsets.
-	It ensures that moving past the end of the object is only allowed for certain units.
-	"""
-
-	def allowMoveToUnitOffsetPastEnd(self, unit: str) -> bool:
-		return unit in (textInfos.UNIT_CHARACTER, textInfos.UNIT_WORD) or not self.obj.flowsTo
-
-
 class CompoundDocument(EditableText, DocumentTreeInterceptor):
 	TextInfo = TreeCompoundTextInfo
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚪ **低優先度**: `source\contentRecog\recogUi.py`

- **優先度**: 5
- **理由**: Copyright更新（低優先度）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: copyright_update

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\contentRecog\\recogUi.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\contentRecog\\recogUi.py"
index 86042fa..5b8a608 100644
--- "a/F:\\nvda\\gh\\beta\\source\\contentRecog\\recogUi.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\contentRecog\\recogUi.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2017-2025 NV Access Limited, James Teh, Leonard de Ruijter, Cyrille Bougot, Cary-rowen, hwf1324
+# Copyright (C) 2017-2025 NV Access Limited, James Teh, Leonard de Ruijter, Cyrille Bougot
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -22,7 +22,6 @@
 import eventHandler
 import textInfos
 from logHandler import log
-from speech import sayAll
 import queueHandler
 import core
 from scriptHandler import script
@@ -46,7 +45,6 @@ class RecogResultNVDAObject(cursorManager.CursorManager, NVDAObjects.window.Wind
 
 	def __init__(self, result=None, obj=None):
 		self.parent = parent = api.getFocusObject()
-		self._shouldSayAllOnFirstFocus = False
 		self.result = result
 		if result:
 			self._selection = self.makeTextInfo(textInfos.POSITION_FIRST)
@@ -162,8 +160,6 @@ def _onFirstResult(self, result: Union[RecognitionResult, Exception]):
 		self._selection = self.makeTextInfo(textInfos.POSITION_FIRST)
 		# This method queues an event to the main thread.
 		self.setFocus()
-		if self.recognizer.autoSayAllOnResult:
-			self._shouldSayAllOnFirstFocus = True
 		if self.recognizer.allowAutoRefresh:
 			self._scheduleRecognize()
 
@@ -208,9 +204,6 @@ def _onResult(self, result: Union[RecognitionResult, Exception]):
 
 	def event_gainFocus(self):
 		super().event_gainFocus()
-		if self._shouldSayAllOnFirstFocus:
-			self._shouldSayAllOnFirstFocus = False
-			sayAll.SayAllHandler.readText(sayAll.CURSOR.CARET)
 		if self.recognizer.allowAutoRefresh:
 			# Make LiveText watch for and report new text.
 			self.startMonitoring()
@@ -226,8 +219,6 @@ def start(self):
 
 #: Keeps track of the recognition in progress, if any.
 _activeRecog = None
... (残り 5 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚪ **低優先度**: `source\contentRecog\uwpOcr.py`

- **優先度**: 5
- **理由**: Copyright更新（低優先度）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: copyright_update

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\contentRecog\\uwpOcr.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\contentRecog\\uwpOcr.py"
index 0610d5f..76b1f16 100644
--- "a/F:\\nvda\\gh\\beta\\source\\contentRecog\\uwpOcr.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\contentRecog\\uwpOcr.py"
@@ -1,16 +1,11 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2017-2025 NV Access Limited, Cary-rowen
+# Copyright (C) 2017-2021 NV Access Limited
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
 """Recognition of text using the UWP OCR engine included in Windows 10 and later."""
 
-from ctypes import (
-	cast,
-	POINTER,
-)
 import json
-from winBindings.gdi32 import RGBQUAD
 import NVDAHelper
 from NVDAHelper.localWin10 import (
 	uwpOcr_getLanguages,
@@ -91,10 +86,6 @@ def _get_allowAutoRefresh(cls) -> bool:
 	def _get_autoRefreshInterval(cls) -> int:
 		return config.conf["uwpOcr"]["autoRefreshInterval"]
 
-	@classmethod
-	def _get_autoSayAllOnResult(cls) -> bool:
-		return config.conf["uwpOcr"]["autoSayAllOnResult"]
-
 	def getResizeFactor(self, width, height):
 		# UWP OCR performs poorly with small images, so increase their size.
 		if width < 100 or height < 100:
@@ -133,15 +124,7 @@ def callback(result):
 		if not self._handle:
 			onResult(RuntimeError("UWP OCR initialization failed"))
 			return
-		uwpOcr_recognize(
-			self._handle,
-			# pixels, as fetched from screenBitmap.captureImage is a 2d array of RGBQUAD values.
-			# However uwpOcr_recognize expects a 1d array (pointer).
-			# These are identical in memory, so we can just cast.
-			cast(pixels, POINTER(RGBQUAD)),
-			imgInfo.recogWidth,
-			imgInfo.recogHeight,
-		)
+		uwpOcr_recognize(self._handle, pixels, imgInfo.recogWidth, imgInfo.recogHeight)
 
 	def cancel(self):
 		self._onResult = None
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚪ **低優先度**: `source\hidpi.py`

- **優先度**: 5
- **理由**: Copyright更新（低優先度）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: copyright_update

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\hidpi.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\hidpi.py"
index 3c6f728..5ac760e 100644
--- "a/F:\\nvda\\gh\\beta\\source\\hidpi.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\hidpi.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2021-2025 NV Access Limited
+# Copyright (C) 2021 NV Access Limited
 
 """
 Required types and defines from Windows SDK's hidpi.h
@@ -9,7 +9,7 @@
 """
 
 import enum
-from ctypes import Structure, Union, c_byte, c_long
+from ctypes import Structure, Union, c_byte
 from ctypes.wintypes import USHORT, BOOLEAN, ULONG, LONG
 
 
@@ -52,17 +52,6 @@ class HIDP_REPORT_TYPE(enum.IntEnum):
 	OUTPUT = 1
 	FEATURE = 2
 
-	@classmethod
-	def from_param(cls, obj):
-		"""
-		Used by ctypes for automatic parameter conversion when passing
-		HIDP_REPORT_TYPE values to C functions. Converts the enum or integer
-		to a c_long as required by the Windows API.
-		"""
-		if isinstance(obj, (cls, int)):
-			return c_long(obj)
-		raise TypeError(f"Expected {cls.__name__} or int, got {type(obj).__name__}")
-
 
 class _HIDP_DATA_U1(Union):
 	_fields_ = [
@@ -79,7 +68,7 @@ class HIDP_DATA(Structure):
 	]
 
 
-class _HIDP_VALUE_AND_BUTTON_CAPS_U1_RANGE(Structure):
+class _HIDP_VALUE_CAPS_U1_RANGE(Structure):
 	_fields_ = [
 		("UsageMin", USAGE),
 		("UsageMax", USAGE),
@@ -92,7 +81,7 @@ class _HIDP_VALUE_AND_BUTTON_CAPS_U1_RANGE(Structure):
... (残り 78 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚪ **低優先度**: `source\hwIo\hid.py`

- **優先度**: 5
- **理由**: Copyright更新（低優先度）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: copyright_update

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\hwIo\\hid.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\hwIo\\hid.py"
index 46ae41c..cfffb82 100644
--- "a/F:\\nvda\\gh\\beta\\source\\hwIo\\hid.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\hwIo\\hid.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2015-2025 NV Access Limited, Babbage B.V.
+# Copyright (C) 2015-2018 NV Access Limited, Babbage B.V.
 
 
 """Raw input/output for braille displays via HID
@@ -20,13 +20,9 @@
 from logHandler import log
 from .base import IoBase, _isDebug
 import hidpi
-import winBindings.hid
-from utils import _deprecate
 
 
-__getattr__ = _deprecate.handleDeprecations(
-	_deprecate.MovedSymbol("hidDll", "winBindings.hid", "dll"),
-)
+hidDll = ctypes.windll.hid
 
 
 class HidPError(RuntimeError):
@@ -62,11 +58,11 @@ def __init__(self, device, data):
 		super().__init__(device)
 
 	def getUsages(self, usagePage, linkCollection=0):
-		maxUsages = winBindings.hid.HidP_MaxUsageListLength(self._reportType, usagePage, self._dev._pd)
+		maxUsages = hidDll.HidP_MaxUsageListLength(self._reportType, hidpi.USAGE(usagePage), self._dev._pd)
 		numUsages = ctypes.c_long(maxUsages)
 		usageList = (hidpi.USAGE * maxUsages)()
 		check_HidP_status(
-			winBindings.hid.HidP_GetUsages,
+			hidDll.HidP_GetUsages,
 			self._reportType,
 			hidpi.USAGE(usagePage),
 			USHORT(linkCollection),
@@ -79,11 +75,11 @@ def getUsages(self, usagePage, linkCollection=0):
 		return usageList[0 : numUsages.value]
 
 	def getDataItems(self):
-		maxDataLength = winBindings.hid.HidP_MaxDataListLength(self._reportType, self._dev._pd)
+		maxDataLength = hidDll.HidP_MaxDataListLength(self._reportType, self._dev._pd)
 		numDataLength = ctypes.c_ulong(maxDataLength)
 		dataList = (hidpi.HIDP_DATA * maxDataLength)()
... (残り 136 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚪ **低優先度**: `source\textInfos\offsets.py`

- **優先度**: 5
- **理由**: Copyright更新（低優先度）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: copyright_update

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\textInfos\\offsets.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\textInfos\\offsets.py"
index 1def339..f9a6973 100644
--- "a/F:\\nvda\\gh\\beta\\source\\textInfos\\offsets.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\textInfos\\offsets.py"
@@ -1,14 +1,14 @@
+# textInfos/offsets.py
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2025 NV Access Limited, Babbage B.V., Leonard de Ruijter
-# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
-# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
+# This file is covered by the GNU General Public License.
+# See the file COPYING for more details.
+# Copyright (C) 2006-2024 NV Access Limited, Babbage B.V., Leonard de Ruijter
 
 from abc import abstractmethod
 import re
 import ctypes
 import unicodedata
 import NVDAHelper
-import NVDAState
 import config
 import textInfos
 import locationHelper
@@ -643,27 +643,11 @@ def unitCount(self, unit):
 		else:
 			raise NotImplementedError
 
-	def allowMoveToUnitOffsetPastEnd(self, unit: str) -> bool:
+	allowMoveToOffsetPastEnd = True
 	"""
-		This method indicates whether the `move` method is allowed to move one unit past the end of the text info.
-		For example, normally we should be able to move 1 past story length
-		to allow braille routing to move to an insertion point at the end. (#2096)
-		Furthermore, review cursor should be able to reach the last, empty line in some controls,
-		like Scintilla. (#18348)
-		:param unit: the TextInfo unit (e.g. character or word)
-		:return: Whether or not to allow movement past end for the specific unit.
+	We can move 1 past story length to allow braille routing to end insertion point. (#2096)
+	Furthermore, review cursor is able to reach the last, empty line in some controls, like Scintilla. (#18348)
 	"""
-		return True
-
-	if NVDAState._allowDeprecatedAPI():
-
-		def _get_allowMoveToOffsetPastEnd(self) -> bool:
-			log.warning(
-				"OffsetsTextInfo.allowMoveToOffsetPastEnd is deprecated. "
-				"Use the OffsetsTextInfo.allowMoveToUnitOffsetPastEnd method instead.",
-				stack_info=True,
-			)
... (残り 15 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚪ **低優先度**: `source\virtualBuffers\__init__.py`

- **優先度**: 5
- **理由**: Copyright更新（低優先度）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: copyright_update

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\virtualBuffers\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\virtualBuffers\\__init__.py"
index 74e8f7c..97def79 100644
--- "a/F:\\nvda\\gh\\beta\\source\\virtualBuffers\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\virtualBuffers\\__init__.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2007-2025 NV Access Limited, Peter Vágner, Cyrille Bougot, Leonard de Ruijter
-# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
-# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
+# This file is covered by the GNU General Public License.
+# See the file COPYING for more details.
+# Copyright (C) 2007-2025 NV Access Limited, Peter Vágner, Cyrille Bougot
 
 import time
 import threading
@@ -149,9 +149,7 @@ def isChild(self, parent):
 
 
 class VirtualBufferTextInfo(browseMode.BrowseModeDocumentTextInfo, textInfos.offsets.OffsetsTextInfo):
-	def allowMoveToUnitOffsetPastEnd(self, unit: str) -> bool:
-		"""Virtual buffers have no insertion point, so no need to move past the end of text."""
-		return False
+	allowMoveToOffsetPastEnd = False  #: no need for end insertion point as vbuf is not editable.
 
 	def _getControlFieldAttribs(self, docHandle, id):
 		info = self.copy()
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚪ **低優先度**: `source\vision\util.py`

- **優先度**: 5
- **理由**: Copyright更新（低優先度）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: copyright_update

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\vision\\util.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\vision\\util.py"
index 9644cc9..05b1a37 100644
--- "a/F:\\nvda\\gh\\beta\\source\\vision\\util.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\vision\\util.py"
@@ -2,7 +2,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2018-2025 NV Access Limited, Babbage B.V., hwf1324
+# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.
 
 """Utility functions for vision enhancement providers."""
 
@@ -25,11 +25,7 @@ def getCaretRect(obj: Optional[TextContainerObject] = None) -> locationHelper.Re
 		obj = api.getCaretObject()
 	if api.isObjectInActiveTreeInterceptor(obj):
 		obj = obj.treeInterceptor
-	if (
-		api.isNVDAObject(obj)
-		# Ignore fake NVDAObjects, as the caret rectangle may not be obtainable through the display model.
-		and not api.isFakeNVDAObject(obj)
-	):
+	if api.isNVDAObject(obj):
 		# Import late to avoid circular import
 		import displayModel
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚪ **低優先度**: `source\winConsoleHandler.py`

- **優先度**: 5
- **理由**: Copyright更新（低優先度）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: copyright_update

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winConsoleHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winConsoleHandler.py"
index 648c488..aff67ec 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winConsoleHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winConsoleHandler.py"
@@ -4,7 +4,6 @@
 # See the file COPYING for more details.
 # Copyright (C) 2009-2025 NV Access Limited, Babbage B.V.
 
-from ctypes.wintypes import SMALL_RECT
 import gui
 import winUser
 import winBindings.kernel32
@@ -157,15 +156,7 @@ def getConsoleVisibleLines():
 
 
 @winBindings.user32.WINEVENTPROC
-def consoleWinEventHook(
-	handle: int | None,
-	eventID: int,
-	window: int | None,
-	objectID: int,
-	childID: int,
-	threadID: int,
-	timestamp: int,
-) -> None:
+def consoleWinEventHook(handle, eventID, window, objectID, childID, threadID, timestamp):
 	from NVDAObjects.behaviors import KeyboardHandlerBasedTypedCharSupport
 
 	# We don't want to do anything with the event if the event is not for the window this console is in
@@ -273,7 +264,7 @@ def getTextWithFields(self, formatConfig: Optional[Dict] = None) -> textInfos.Te
 			formatConfig = config.conf["documentFormatting"]
 		left, top = self._consoleCoordFromOffset(self._startOffset)
 		right, bottom = self._consoleCoordFromOffset(self._endOffset - 1)
-		rect = SMALL_RECT(left, top, right, bottom)
+		rect = wincon.SMALL_RECT(left, top, right, bottom)
 		if bottom - top > 0:  # offsets span multiple lines
 			rect.Left = 0
 			rect.Right = self.consoleScreenBufferInfo.dwSize.x - 1
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\_localCaptioner\captioner\vitGpt2.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_localCaptioner\\captioner\\vitGpt2.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_localCaptioner\\captioner\\vitGpt2.py"
index 47af56c..6224c3a 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_localCaptioner\\captioner\\vitGpt2.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_localCaptioner\\captioner\\vitGpt2.py"
@@ -86,10 +86,7 @@ def __init__(
 		try:
 			self.encoderSession = ort.InferenceSession(encoderPath, sess_options=sessionOptions)
 			self.decoderSession = ort.InferenceSession(decoderPath, sess_options=sessionOptions)
-		except (
-			ort.capi.onnxruntime_pybind11_state.InvalidProtobuf,
-			ort.capi.onnxruntime_pybind11_state.NoSuchFile,
-		) as e:
+		except ort.capi.onnxruntime_pybind11_state.InvalidProtobuf as e:
 			raise FileNotFoundError(
 				"model file incomplete"
 				f" Please check whether the file is complete or re-download. Original error: {e}",
@@ -145,7 +142,7 @@ def _loadVocab(self, vocabPath: str) -> dict[int, str]:
 
 			# Convert to id -> token format
 			vocab = {v: k for k, v in vocabData.items()}
-			log.debug(f"Successfully loaded vocabulary with {len(vocab)} tokens")
+			log.info(f"Successfully loaded vocabulary with {len(vocab)} tokens")
 			return vocab
 
 		except FileNotFoundError:
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\_localCaptioner\imageDescriber.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_localCaptioner\\imageDescriber.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_localCaptioner\\imageDescriber.py"
index 1e19378..6a599da 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_localCaptioner\\imageDescriber.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_localCaptioner\\imageDescriber.py"
@@ -123,10 +123,8 @@ def _doCaption(self) -> None:
 		imageData = _screenshotNavigator()
 
 		if not self.isModelLoaded:
-			from gui._localCaptioner.messageDialogs import openEnableOnceDialog
-
-			# Ask to enable image desc only in this session, No configuration modifications
-			wx.CallAfter(openEnableOnceDialog)
+			# Translators: Message when image description is not enabled
+			ui.message(pgettext("imageDesc", "image description is not enabled"))
 			return
 
 		if self.captionThread is not None and self.captionThread.is_alive():
@@ -165,10 +163,9 @@ def _loadModel(self, localModelDirPath: str | None = None) -> None:
 			)
 		except FileNotFoundError:
 			self.isModelLoaded = False
-			from gui._localCaptioner.messageDialogs import ImageDescDownloader
+			from gui._localCaptioner.messageDialogs import openDownloadDialog
 
-			descDownloader = ImageDescDownloader()
-			wx.CallAfter(descDownloader.openDownloadDialog)
+			wx.CallAfter(openDownloadDialog)
 		except Exception:
 			self.isModelLoaded = False
 			# Translators: error message when fail to load model
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\_localCaptioner\modelDownloader.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_localCaptioner\\modelDownloader.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_localCaptioner\\modelDownloader.py"
index 476b91d..80e1a54 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_localCaptioner\\modelDownloader.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_localCaptioner\\modelDownloader.py"
@@ -136,8 +136,8 @@ def constructDownloadUrl(
 		model = modelName.strip("/")
 		ref = resolvePath.strip("/")
 		filePath = filePath.lstrip("/")
-
-		return f"{base}/{model}/{ref}/{filePath}"
+		url = f"{base}/{model}/{ref}/{filePath}"
+		return url
 
 	def _getRemoteFileSize(self, url: str) -> int:
 		"""
@@ -151,7 +151,7 @@ def _getRemoteFileSize(self, url: str) -> int:
 
 		try:
 			# Use HEAD request with automatic redirect following
-			response = self.session.head(url, timeout=10, allow_redirects=True)
+			response = self.session.head(url, timeout=30, allow_redirects=True)
 			response.raise_for_status()
 		except Exception as e:
 			if not self.cancelRequested:
@@ -163,7 +163,7 @@ def _getRemoteFileSize(self, url: str) -> int:
 
 		try:
 			# If HEAD doesn't work, try GET with range header to get just 1 byte
-			response = self.session.get(url, headers={"Range": "bytes=0-0"}, timeout=10, allow_redirects=True)
+			response = self.session.get(url, headers={"Range": "bytes=0-0"}, timeout=30, allow_redirects=True)
 		except Exception as e:
 			if not self.cancelRequested:
 				log.warning(f"Failed to get remote file size (GET) for {url}: {e}")
@@ -419,7 +419,6 @@ def _performSingleDownload(
 		try:
 			# Determine total file size
 			total = self._calculateTotalSize(response, resumePos)
-
 			if total > 0:
 				log.debug(f"Total file size: {total:,} bytes")
 
@@ -437,7 +436,8 @@ def _performSingleDownload(
 				return False, message
 
 			# Verify download integrity
-			return self._verifyDownloadIntegrity(localPath, fileName, total, progressCallback, threadId)
+			result = self._verifyDownloadIntegrity(localPath, fileName, total, progressCallback, threadId)
+			return result
 
 		finally:
... (残り 40 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\_remoteClient\client.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\client.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\client.py"
index 07b8b1c..4691a22 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\client.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\client.py"
@@ -19,7 +19,7 @@
 from keyboardHandler import KeyboardInputGesture, canModifiersPerformAction
 from logHandler import log
 from gui.guiHelper import alwaysCallAfter
-from utils.security import isRunningOnSecureDesktop, post_sessionLockStateChanged
+from utils.security import isRunningOnSecureDesktop
 from gui.message import MessageDialog, DefaultButton, ReturnCode, DialogType
 import scriptHandler
 import winUser
@@ -46,13 +46,11 @@ class RemoteClient:
 	followerSession: Optional[FollowerSession]
 	keyModifiers: Set[KeyModifier]
 	hostPendingModifiers: Set[KeyModifier]
-	hostPendingNonmodifier: KeyModifier | None
 	_connecting: bool
 	leaderTransport: Optional[RelayTransport]
 	followerTransport: Optional[RelayTransport]
 	localControlServer: Optional[server.LocalRelayServer]
 	sendingKeys: bool
-	sdHandler: SecureDesktopHandler | None
 
 	def __init__(
 		self,
@@ -60,7 +58,6 @@ def __init__(
 		log.info("Initializing NVDA Remote client")
 		self.keyModifiers = set()
 		self.hostPendingModifiers = set()
-		self.hostPendingNonmodifiers = None
 		self.localScripts = set()
 		self.localMachine = LocalMachine()
 		self.followerSession = None
@@ -74,13 +71,7 @@ def __init__(
 		self.followerTransport = None
 		self.localControlServer = None
 		self.sendingKeys = False
-		self._wasSendingKeysBeforeLock: bool = False
-		try:
 		self.sdHandler = SecureDesktopHandler()
-		except RuntimeError:
-			log.error("Failed to initialise the secure desktop handler.", exc_info=True)
-			self.sdHandler = None
-		else:
 		if isRunningOnSecureDesktop():
 			connection = self.sdHandler.initializeSecureDesktop()
 			if connection:
@@ -111,7 +102,6 @@ def performAutoconnect(self):
... (残り 87 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\_remoteClient\input.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\input.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\input.py"
index 4dcfdb9..678b084 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\input.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\input.py"
@@ -4,7 +4,8 @@
 # See the file COPYING for more details.
 
 import ctypes
-from enum import IntEnum
+from ctypes import POINTER, Structure, Union, c_long, c_ulong, wintypes
+from enum import IntEnum, IntFlag
 
 import api
 import baseObject
@@ -16,6 +17,23 @@
 from winBindings import user32
 
 
+class InputType(IntEnum):
+	"""Values permissible as the `type` field in an `INPUT` struct.
+
+	.. seealso::
+		https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input
+	"""
+
+	MOUSE = 0
+	"""The event is a mouse event. Use the mi structure of the union."""
+
+	KEYBOARD = 1
+	"""The event is a keyboard event. Use the ki structure of the union."""
+
+	HARDWARE = 2
+	"""The event is a hardware event. Use the hi structure of the union."""
+
+
 class VKMapType(IntEnum):
 	"""Type of mapping to be performed between virtual key code and virtual scan code.
 
@@ -27,6 +45,80 @@ class VKMapType(IntEnum):
 	"""Maps a virtual key code to a scan code."""
 
 
+class KeyEventFlag(IntFlag):
+	"""Specifies various aspects of a keystroke in a KEYBDINPUT struct.
+
+	.. seealso::
+		https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
+	"""
+
+	EXTENDED_KEY = 0x0001
... (残り 93 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\_remoteClient\secureDesktop.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\secureDesktop.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\secureDesktop.py"
index a7ae635..1a3993e 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\secureDesktop.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\secureDesktop.py"
@@ -19,34 +19,19 @@
     to exchange connection information between sessions.
 """
 
-from enum import IntEnum
 import json
 import socket
 import threading
 import uuid
 from pathlib import Path
 from typing import Any, Optional
-from ctypes import (
-	POINTER,
-	FormatError,
-	GetLastError,
-	c_size_t,
-	sizeof,
-	windll,
-	create_unicode_buffer,
-	WINFUNCTYPE,
-	wstring_at,
-)
-from ctypes.wintypes import BOOL, DWORD, HANDLE, LPCVOID, LPCWSTR, LPVOID, WCHAR
-from serial.win32 import INVALID_HANDLE_VALUE
+from ctypes import create_unicode_buffer
 
 import shlobj
 from logHandler import log
 from winAPI.secureDesktop import post_secureDesktopStateChange
 from NVDAHelper import localLib
-from winBindings import kernel32 as _kernel32
-from winKernel import closeHandle
-from winKernel import ERROR_ALREADY_EXISTS, SECURITY_ATTRIBUTES
+from winBindings import kernel32
 
 from . import bridge, server
 from .connectionInfo import ConnectionInfo, ConnectionMode
@@ -56,193 +41,6 @@
 from .transport import RelayTransport
 
 
-class PAGE(IntEnum):
-	"""
-	Specifies the page protection of a file mapping object.
-
-	.. note::
... (残り 413 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\_remoteClient\server.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\server.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\server.py"
index 3a9b296..aa6fdb0 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\server.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\server.py"
@@ -25,27 +25,25 @@
 """
 
 import os
-import shutil
 import socket
 import ssl
-import tempfile
 import time
 from datetime import datetime, timedelta, timezone
 from pathlib import Path
 from select import select
 from itertools import count
-from typing import Any, Final, cast
+from typing import Any, Final
 
 import cffi  # noqa # required for cryptography
 from cryptography import x509
 from cryptography.hazmat.primitives import hashes, serialization
 from cryptography.hazmat.primitives.asymmetric import rsa
 from cryptography.x509.oid import NameOID
-from NVDAState import WritePaths, shouldWriteToDisk
 from logHandler import log
 
 from . import configuration
 from .protocol import RemoteMessageType
+from .secureDesktop import getProgramDataTempPath
 from .serializer import JSONSerializer
 
 
@@ -58,39 +56,42 @@ class RemoteCertificateManager:
 	:ivar fingerprintPath: Path to the fingerprint file
 	"""
 
-	CERT_DIR: Final[Path] = Path(WritePaths.remoteAccessDir, "localRelay")
-	CERT_PATH: Final[Path] = CERT_DIR / "NvdaRemoteRelay.pem"
-	KEY_PATH: Final[Path] = CERT_DIR / "NvdaRemoteRelay.key"
-	FINGERPRINT_PATH: Final[Path] = CERT_DIR / "NvdaRemoteRelay.fingerprint"
-	CERT_DURATION_DAYS: Final[int] = 365
-	CERT_RENEWAL_THRESHOLD_DAYS: Final[int] = 30
+	CERT_FILE = "NvdaRemoteRelay.pem"
+	KEY_FILE = "NvdaRemoteRelay.key"
+	FINGERPRINT_FILE = "NvdaRemoteRelay.fingerprint"
+	CERT_DURATION_DAYS = 365
+	CERT_RENEWAL_THRESHOLD_DAYS = 30
 
... (残り 212 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\_remoteClient\session.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\session.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\session.py"
index d068b30..ba613f9 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\session.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\session.py"
@@ -315,8 +315,8 @@ def __init__(
 			RemoteMessageType.SET_DISPLAY_SIZE,
 			self.setDisplaySize,
 		)
-		braille.filter_displayDimensions.register(
-			self.localMachine._handleFilterDisplayDimensions,
+		braille.filter_displaySize.register(
+			self.localMachine.handleFilterDisplaySize,
 		)
 		self.transport.registerInbound(
 			RemoteMessageType.BRAILLE_INPUT,
@@ -396,7 +396,7 @@ def handleTransportDisconnected(self) -> None:
 	def handleClientDisconnected(self, client: dict[str, Any]) -> None:
 		super().handleClientDisconnected(client)
 		if client["connection_type"] == connectionInfo.ConnectionMode.LEADER.value:
-			log.info(f"Leader client disconnected: {client!r}")
+			log.info("Leader client disconnected: %r", client)
 			del self.leaders[client["id"]]
 		elif client["connection_type"] == connectionInfo.ConnectionMode.FOLLOWER.value:
 			self.followers.discard(client["id"])
@@ -407,7 +407,7 @@ def setDisplaySize(self, sizes: list[int] | None = None) -> None:
 		self.leaderDisplaySizes = (
 			sizes if sizes else [info.get("braille_numCells", 0) for info in self.leaders.values()]
 		)
-		log.debug(f"Setting follower display size to: {self.leaderDisplaySizes!r}")
+		log.debug("Setting follower display size to: %r", self.leaderDisplaySizes)
 		self.localMachine.setBrailleDisplaySize(self.leaderDisplaySizes)
 
 	def handleBrailleInfo(
@@ -590,14 +590,17 @@ def handleClientDisconnected(self, client: dict[str, Any] | None = None):
 	def sendBrailleInfo(
 		self,
 		display: braille.BrailleDisplayDriver | None = None,
-		displayDimensions: braille.DisplayDimensions | None = None,
+		displaySize: int | None = None,
 	) -> None:
 		if display is None:
 			display = braille.handler.display
-		if displayDimensions is None:
-			displayDimensions = braille.handler.displayDimensions
-		displaySize = displayDimensions.numCols
-		log.debug(f"Sending braille info to follower - display: {display.name}, width: {displaySize}")
+		if displaySize is None:
+			displaySize = braille.handler.displaySize
+		log.debug(
+			"Sending braille info to follower - display: %s, size: %d",
... (残り 31 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\_remoteClient\transport.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\transport.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\transport.py"
index 5ed6cfe..f220da7 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\transport.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\transport.py"
@@ -521,9 +521,6 @@ def parse(self, line: bytes) -> None:
 		except ValueError:
 			log.warn(f"Received message with invalid type: {obj!r}")
 			return
-		if messageType is RemoteMessageType.PING:
-			# No handling is required
-			return
 		del obj["type"]
 		extensionPoint = self.inboundHandlers.get(messageType)
 		if not extensionPoint:
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\addonHandler\__init__.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\addonHandler\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\addonHandler\\__init__.py"
index 8e25e97..173a25f 100644
--- "a/F:\\nvda\\gh\\beta\\source\\addonHandler\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\addonHandler\\__init__.py"
@@ -31,7 +31,6 @@
 from configobj import ConfigObj
 from configobj.validate import Validator
 import config
-from config.registry import ADDON_BUNDLE_EXTENSION
 import languageHandler
 from logHandler import log
 import winBindings.kernel32
@@ -44,7 +43,6 @@
 from addonStore.models.status import AddonStateCategory, SupportsAddonState
 from addonStore.models.version import MajorMinorPatch, SupportsVersionCheck
 import extensionPoints
-from utils._deprecate import handleDeprecations, MovedSymbol
 from utils.caseInsensitiveCollections import CaseInsensitiveSet
 from utils.tempFile import _createEmptyTempFileForDeletingFile
 
@@ -63,22 +61,11 @@
 		InstalledAddonStoreModel,
 	)
 
-__getattr__ = handleDeprecations(
-	MovedSymbol(
-		"BUNDLE_EXTENSION",
-		"config",
-		"registry",
-		"ADDON_BUNDLE_EXTENSION",
-	),
-	MovedSymbol(
-		"NVDA_ADDON_PROG_ID",
-		"config.registry",
-	),
-)
-
 MANIFEST_FILENAME = "manifest.ini"
 stateFilename = "addonsState.pickle"
+BUNDLE_EXTENSION = "nvda-addon"
 BUNDLE_MIMETYPE = "application/x-nvda-addon"
+NVDA_ADDON_PROG_ID = "NVDA.Addon.1"
 ADDON_PENDINGINSTALL_SUFFIX = ".pendingInstall"
 DELETEDIR_SUFFIX = ".delete"
 
@@ -800,7 +787,7 @@ def _cleanupAddonImports(self) -> None:
 		self._importedAddonModules.clear()
 		for modName in set(sys.modules.keys()) - self._modulesBeforeInstall:
 			module = sys.modules[modName]
-			if module.__name__ and module.__name__.startswith(self.path):
... (残り 13 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\addonStore\models\addon.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\addonStore\\models\\addon.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\addonStore\\models\\addon.py"
index 97443de..aa17a08 100644
--- "a/F:\\nvda\\gh\\beta\\source\\addonStore\\models\\addon.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\addonStore\\models\\addon.py"
@@ -24,7 +24,6 @@
 from NVDAState import WritePaths
 
 from .channel import Channel
-from .scanResults import VirusTotalScanResults
 from .status import SupportsAddonState
 from .version import (
 	MajorMinorPatch,
@@ -59,8 +58,7 @@ class _AddonGUIModel(SupportsAddonState, SupportsVersionCheck, Protocol):
 	description: str
 	addonVersionName: str
 	channel: Channel
-	homepage: str | None
-	changelog: str | None
+	homepage: Optional[str]
 	minNVDAVersion: MajorMinorPatch
 	lastTestedVersion: MajorMinorPatch
 	legacy: bool
@@ -116,21 +114,19 @@ class _AddonStoreModel(_AddonGUIModel):
 	description: str
 	addonVersionName: str
 	channel: Channel
-	homepage: str | None
-	changelog: str | None
+	homepage: Optional[str]
 	minNVDAVersion: MajorMinorPatch
 	lastTestedVersion: MajorMinorPatch
 	legacy: bool
 	publisher: str
 	license: str
-	licenseURL: str | None
+	licenseURL: Optional[str]
 	sourceURL: str
 	URL: str
 	sha256: str
 	addonVersionNumber: MajorMinorPatch
-	reviewURL: str | None
+	reviewURL: Optional[str]
 	submissionTime: int | None
-	scanResults: VirusTotalScanResults | None = None
 
 	@property
 	def tempDownloadPath(self) -> str:
@@ -225,11 +221,6 @@ def description(self) -> str:
 			return ""
 		return description
... (残り 78 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\appModuleHandler.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\appModuleHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModuleHandler.py"
index 85b52b5..097e766 100644
--- "a/F:\\nvda\\gh\\beta\\source\\appModuleHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModuleHandler.py"
@@ -604,17 +604,9 @@ def __repr__(self):
 	def _get_appModuleName(self):
 		return self.__class__.__module__.split(".")[-1]
 
-	_liveForEver: bool = False
-	"""
-	Set to true when NVDA cannot get enough permissions to successfully verify if the process is dead.
-	E.g. Security software such as 1Password which blocks the SYNCHRONIZE access right.
-	"""
-
 	isAlive: bool
 
 	def _get_isAlive(self) -> bool:
-		if self._liveForEver:
-			return True
 		try:
 			return bool(winKernel.waitForSingleObject(self.processHandle, 0))
 		except OSError as e:
@@ -624,16 +616,6 @@ def _get_isAlive(self) -> bool:
 					f"Process handle {self.processHandle} for {self} is invalid, assuming process is dead.",
 				)
 				return False
-			elif e.winerror == winKernel.ERROR_ACCESS_DENIED:
-				# Although we opened the process asking for the SYNCHRONIZE access right,
-				# The process is refusing us the permission when waiting on the handle.
-				# This may be a protected process like 1Password.
-				# Currently there is no alternative way to check if the process is dead, so we must assume it stays alive for ever.
-				log.debugWarning(
-					f"Access denied waiting on Process handle {self.processHandle} for {self}, cannot verify dead, marking as living for ever.",
-				)
-				self._liveForEver = True
-				return True
 			raise
 
 	def terminate(self):
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\appModules\explorer.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\appModules\\explorer.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\explorer.py"
index 7f71607..4888034 100644
--- "a/F:\\nvda\\gh\\beta\\source\\appModules\\explorer.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\explorer.py"
@@ -45,6 +45,21 @@ def _get_container(self):
 			return super(MultitaskingViewFrameListItem, self).container
 
 
+# Support for Win8 start screen search suggestions.
+class SuggestionListItem(UIA):
+	def event_UIA_elementSelected(self):
+		speech.cancelSpeech()
+		if api.setNavigatorObject(self, isFocus=True):
+			self.reportFocus()
+			super().event_UIA_elementSelected()
+
+
+# Windows 8 hack: Class to disable incorrect focus on windows 8 search box
+# (containing the already correctly focused edit field)
+class SearchBoxClient(IAccessible):
+	shouldAllowIAccessibleFocusEvent = False
+
+
 # Class for menu items  for Windows Places and Frequently used Programs (in start menu)
 # Also used for desktop items
 class SysListView32EmittingDuplicateFocusEvents(IAccessible):
@@ -149,6 +164,47 @@ def event_show(self):
 			super().event_show()
 
 
+class GridTileElement(UIA):
+	role = controlTypes.Role.TABLECELL
+
+	def _get_description(self):
+		name = self.name
+		descriptionStrings = []
+		for child in self.children:
+			description = child.basicText
+			if not description or description == name:
+				continue
+			descriptionStrings.append(description)
+		return " ".join(descriptionStrings)
+		return description
+
+
+class GridListTileElement(UIA):
+	role = controlTypes.Role.TABLECELL
+	description = None
+
+
... (残り 59 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\appModules\outlook.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\appModules\\outlook.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\outlook.py"
index 09e46f8..f73bbda 100644
--- "a/F:\\nvda\\gh\\beta\\source\\appModules\\outlook.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\outlook.py"
@@ -342,7 +342,7 @@ def event_valueChange(self):
 		"""Set focus back to the edit field when an auto-complete list item is confirmed."""
 		if vision.handler:
 			vision.handler.handleGainFocus(self)
-			api.setNavigatorObject(self, isFocus=True)
+		api.setNavigatorObject(self)
 		super().event_valueChange()
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\brailleDisplayDrivers\papenmeier.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\brailleDisplayDrivers\\papenmeier.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleDisplayDrivers\\papenmeier.py"
index 2bd13ac..e17e762 100644
--- "a/F:\\nvda\\gh\\beta\\source\\brailleDisplayDrivers\\papenmeier.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleDisplayDrivers\\papenmeier.py"
@@ -20,7 +20,6 @@
 try:
 	import ftdi2
 except:  # noqa: E722
-	log.debug("Failed to import ftdi2.", exc_info=True)
 	ftdi2 = None
 # for bluetooth
 import hwPortUtils
@@ -167,18 +166,18 @@ def connectBluetooth(self):
 							)
 							log.info("connectBluetooth success")
 						except:  # noqa: E722
-							log.debugWarning("connectBluetooth failed", exc_info=True)
+							log.debugWarning("connectBluetooth failed")
 
 	def connectUSB(self, devlist: List[bytes]):
 		"""Try to connect to usb device, this is triggered when bluetooth
 		connection could not be established"""
 		try:
-			self._dev = ftdi2.openEx(devlist[0])
+			self._dev = ftdi2.open_ex(devlist[0])
 			self._dev.set_baud_rate(self._baud)
-			self._dev.inWaiting = self._dev.getQueueStatus
+			self._dev.inWaiting = self._dev.get_queue_status
 			log.info("connectUSB success")
 		except:  # noqa: E722
-			log.debugWarning("connectUSB failed", exc_info=True)
+			log.debugWarning("connectUSB failed")
 
 	def __init__(self):
 		"""initialize driver"""
@@ -195,7 +194,7 @@ def __init__(self):
 		# try to connect to usb device,
 		# if no usb device is found there may be a bluetooth device
 		if ftdi2:
-			devlist = ftdi2.listDevices()
+			devlist = ftdi2.list_devices()
 		if len(devlist) == 0:
 			self.connectBluetooth()
 		elif ftdi2:
@@ -308,7 +307,7 @@ def __init__(self):
 						log.debugWarning("UNKNOWN BRAILLE")
 
 			except:  # noqa: E722
-				log.debugWarning("BROKEN PIPE - THIS SHOULD NEVER HAPPEN", exc_info=True)
+				log.debugWarning("BROKEN PIPE - THIS SHOULD NEVER HAPPEN")
... (残り 40 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\brailleInput.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\brailleInput.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleInput.py"
index 4b7fedb..0e961cb 100644
--- "a/F:\\nvda\\gh\\beta\\source\\brailleInput.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleInput.py"
@@ -409,12 +409,12 @@ def sendChars(self, chars: str):
 			for ch in chars
 		)
 		for ch in chars:
-			for direction in (0, winBindings.user32.KEYEVENTF.KEYUP):
+			for direction in (0, winUser.KEYEVENTF_KEYUP):
 				input = winBindings.user32.INPUT()
-				input.type = winBindings.user32.INPUT_TYPE.KEYBOARD
+				input.type = winUser.INPUT_KEYBOARD
 				input.ii.ki = winBindings.user32.KEYBDINPUT()
 				input.ii.ki.wScan = ord(ch)
-				input.ii.ki.dwFlags = winBindings.user32.KEYEVENTF.UNICODE | direction
+				input.ii.ki.dwFlags = winUser.KEYEVENTF_UNICODE | direction
 				inputs.append(input)
 		winUser.SendInput(inputs)
 		focusObj = api.getFocusObject()
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\controlTypes\processAndLabelStates.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\controlTypes\\processAndLabelStates.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\controlTypes\\processAndLabelStates.py"
index 79a5b2a..8bb5b50 100644
--- "a/F:\\nvda\\gh\\beta\\source\\controlTypes\\processAndLabelStates.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\controlTypes\\processAndLabelStates.py"
@@ -5,27 +5,25 @@
 
 from typing import Dict, List, Optional, Set
 
-import config
-
-from .outputReason import OutputReason
 from .role import Role, clickableRoles
-from .state import STATES_LINK_TYPE, STATES_SORTED, State
+from .state import State, STATES_SORTED, STATES_LINK_TYPE
+from .outputReason import OutputReason
 
 
 def _processPositiveStates(
 	role: Role,
-	states: set[State],
+	states: Set[State],
 	reason: OutputReason,
-	positiveStates: set[State] | None = None,
-) -> set[State]:
+	positiveStates: Optional[Set[State]] = None,
+) -> Set[State]:
 	"""Processes the states for an object and returns the positive states to output for a specified reason.
 	For example, if C{State.CHECKED} is in the returned states, it means that the processed object is checked.
-	:param role: The role of the object to process states for (e.g. C{Role.CHECKBOX}).
-	:param states: The raw states for an object to process.
-	:param reason: The reason to process the states (e.g. C{OutputReason.FOCUS}).
-	:param positiveStates: Used for C{OutputReason.CHANGE}, specifies states changed from negative to
+	@param role: The role of the object to process states for (e.g. C{Role.CHECKBOX}).
+	@param states: The raw states for an object to process.
+	@param reason: The reason to process the states (e.g. C{OutputReason.FOCUS}).
+	@param positiveStates: Used for C{OutputReason.CHANGE}, specifies states changed from negative to
 	positive.
-	:return: The processed positive states.
+	@return: The processed positive states.
 	"""
 	positiveStates = positiveStates.copy() if positiveStates is not None else states.copy()
 	# The user never cares about certain states.
@@ -35,15 +33,6 @@ def _processPositiveStates(
 		positiveStates.discard(State.VISITED)
 		positiveStates.discard(State.INTERNAL_LINK)
 	positiveStates.discard(State.SELECTABLE)
-	if not config.conf["presentation"]["reportMultiSelect"] or role in (
-		Role.LISTITEM,
-		Role.TREEVIEWITEM,
-		Role.MENUITEM,
... (残り 27 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\easeOfAccess.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\easeOfAccess.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\easeOfAccess.py"
index c9c5ea7..e4b4cb6 100644
--- "a/F:\\nvda\\gh\\beta\\source\\easeOfAccess.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\easeOfAccess.py"
@@ -138,7 +138,6 @@ def _getAutoStartConfiguration(autoStartContext: AutoStartContext) -> list[str]:
 			exc_info=True,
 		)
 	else:
-		k.Close()
 		if not conf[0]:
 			# "".split(",") returns [""], so remove the empty string.
 			del conf[0]
@@ -168,11 +167,11 @@ def setAutoStart(autoStartContext: AutoStartContext, enable: bool) -> None:
 		changed = True
 
 	if changed:
-		with winreg.OpenKey(
+		k = winreg.OpenKey(
 			autoStartContext.value,
 			_RegistryKey.EASE_OF_ACCESS.value,
 			access=winreg.KEY_READ | winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY,
-		) as k:
+		)
 		winreg.SetValueEx(
 			k,
 			"Configuration",
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\gui\_localCaptioner\messageDialogs.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\_localCaptioner\\messageDialogs.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\_localCaptioner\\messageDialogs.py"
index c7a3e7c..86421d4 100644
--- "a/F:\\nvda\\gh\\beta\\source\\gui\\_localCaptioner\\messageDialogs.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\_localCaptioner\\messageDialogs.py"
@@ -4,46 +4,31 @@
 # For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
 
 from gui.message import MessageDialog, DefaultButton, ReturnCode, DialogType
-import gui
-from _localCaptioner.modelDownloader import ModelDownloader, ProgressCallback
+from _localCaptioner.modelDownloader import ModelDownloader
 import threading
 from threading import Thread
 import wx
 import ui
 import _localCaptioner
 
-
-class ImageDescDownloader:
 _downloadThread: Thread | None = None
-	isOpening: bool = False
-
-	def __init__(self):
-		self.downloadDict: dict[str, tuple[int, int]] = {}
-		self.modelDownloader: ModelDownloader | None = None
-		self._shouldCancel = False
-		self._progressDialog: wx.ProgressDialog | None = None
-		self.filesToDownload = [
-			"onnx/encoder_model_quantized.onnx",
-			"onnx/decoder_model_merged_quantized.onnx",
-			"config.json",
-			"vocab.json",
-			"preprocessor_config.json",
-		]
-
-	def onDownload(self, progressCallback: ProgressCallback) -> None:
-		self.modelDownloader = ModelDownloader()
-		(success, fail) = self.modelDownloader.downloadModelsMultithreaded(
-			filesToDownload=self.filesToDownload,
-			progressCallback=progressCallback,
-		)
-		if len(fail) == 0:
-			wx.CallAfter(self.openSuccessDialog)
+_failedFiles: list[str] = []
+
+
+def onDownload() -> None:
+	modelDownloader = ModelDownloader()
+	(successful, failed) = modelDownloader.downloadModelsMultithreaded()
+	if len(failed) == 0:
... (残り 153 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\gui\addonStoreGui\controls\details.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\addonStoreGui\\controls\\details.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\addonStoreGui\\controls\\details.py"
index c42a5f8..c0bced3 100644
--- "a/F:\\nvda\\gh\\beta\\source\\gui\\addonStoreGui\\controls\\details.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\addonStoreGui\\controls\\details.py"
@@ -362,33 +362,6 @@ def _refresh(self):
 							pgettext("addonStore", "Publication date:"),
 							details.publicationDate,
 						)
-
-				if isinstance(details, _AddonStoreModel):
-					if details.scanResults is not None:
-						malicious = details.scanResults.totalFlagged
-						self._appendDetailsLabelValue(
-							# Translators: Label for an extra detail field for the selected add-on. In the add-on store dialog.
-							pgettext("addonStore", "VirusTotal scan results:"),
-							npgettext(
-								"addonStore",
-								# Translators: Summary of VirusTotal scan results for the selected add-on.
-								# {malicious} is the number of vendors that detected the add-on as malicious,
-								# {total} is the total number of vendors that scanned the add-on.
-								# In the add-on store dialog.
-								"{malicious} malware scanner detected this add-on as potentially malicious (out of {total}).",
-								"{malicious} malware scanners detected this add-on as potentially malicious (out of {total}).",
-								malicious,
-							).format(
-								malicious=malicious,
-								total=details.scanResults.totalScans,
-							),
-						)
-						self._appendDetailsLabelValue(
-							# Translators: Label for an extra detail field for the selected add-on. In the add-on store dialog.
-							pgettext("addonStore", "VirusTotal scan URL:"),
-							details.scanResults.scanUrl,
-						)
-
 				self.contentsPanel.Show()
 
 		self.Layout()
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\gui\addonStoreGui\controls\messageDialogs.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\addonStoreGui\\controls\\messageDialogs.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\addonStoreGui\\controls\\messageDialogs.py"
index 67300b5..f658a84 100644
--- "a/F:\\nvda\\gh\\beta\\source\\gui\\addonStoreGui\\controls\\messageDialogs.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\addonStoreGui\\controls\\messageDialogs.py"
@@ -19,10 +19,11 @@
 	_AddonManifestModel,
 )
 from addonStore.dataManager import addonDataManager
-from addonStore.models.status import _StatusFilterKey, getStatus
+from addonStore.models.status import _StatusFilterKey, AvailableAddonStatus, getStatus
 import config
 from config.configFlags import AddonsAutomaticUpdate
 import gui
+from gui import nvdaControls
 from gui.addonGui import ConfirmAddonInstallDialog, ErrorAddonInstallDialog, promptUserForRestart
 from gui.addonStoreGui.viewModels.addonList import AddonListItemVM
 from gui.contextHelp import ContextHelpMixin
@@ -403,7 +404,7 @@ def _setupUI(self):
 		mainSizer.Add(sHelper.sizer, border=BORDER_FOR_DIALOGS, flag=wx.ALL)
 		self.Sizer = mainSizer
 		mainSizer.Fit(self)
-		self.CenterOnScreen()
+		self.CentreOnScreen()
 
 	def onCharHook(self, evt: wx.KeyEvent):
 		if evt.KeyCode == wx.WXK_ESCAPE:
@@ -444,23 +445,41 @@ def _setupButtons(self, sHelper: BoxSizerHelper):
 		closeButton.Bind(wx.EVT_BUTTON, self.onCloseButton)
 
 	def _createAddonsPanel(self, sHelper: BoxSizerHelper):
-		from .actions import _MonoActionsContextMenu
-		from .addonList import AddonVirtualList
-		from gui.addonStoreGui.viewModels.store import AddonStoreVM
+		# Translators: the label for the addons list in the updatable addons dialog.
+		entriesLabel = pgettext("addonStore", "Updatable Add-ons")
+		self.addonsList = sHelper.addLabeledControl(
+			entriesLabel,
+			nvdaControls.AutoWidthColumnListCtrl,
+			style=wx.LC_REPORT | wx.LC_SINGLE_SEL,
+		)
 
-		_storeVM = AddonStoreVM()
-		_storeVM._filteredStatusKey = _StatusFilterKey.UPDATE
-		_storeVM._filterIncludeIncompatible = config.conf["addonStore"]["allowIncompatibleUpdates"]
-		_storeVM.refresh()
-		self.addonsList = AddonVirtualList(
-			parent=self,
-			addonsListVM=_storeVM.listVM,
-			actionsContextMenu=_MonoActionsContextMenu(_storeVM),
+		# Translators: Label for an extra detail field for an add-on. In the add-on store UX.
... (残り 50 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\gui\addonStoreGui\controls\storeDialog.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\addonStoreGui\\controls\\storeDialog.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\addonStoreGui\\controls\\storeDialog.py"
index 7283f2a..1c67707 100644
--- "a/F:\\nvda\\gh\\beta\\source\\gui\\addonStoreGui\\controls\\storeDialog.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\addonStoreGui\\controls\\storeDialog.py"
@@ -7,6 +7,9 @@
 import wx
 from wx.adv import BannerWindow
 
+from addonHandler import (
+	BUNDLE_EXTENSION,
+)
 from addonStore.dataManager import addonDataManager
 from addonStore.models.channel import Channel, _channelFilters
 from addonStore.models.status import (
@@ -14,7 +17,6 @@
 	_statusFilters,
 	_StatusFilterKey,
 )
-from config.registry import ADDON_BUNDLE_EXTENSION
 from core import callLater
 import globalVars
 import gui
@@ -416,7 +418,7 @@ def openExternalInstall(self, evt: wx.EVT_BUTTON):
 			# Translators: The message displayed in the dialog that
 			# allows you to choose an add-on package for installation.
 			message=pgettext("addonStore", "Choose Add-on Package File"),
-			wildcard=(fileTypeLabel + "|*.{ext}").format(ext=ADDON_BUNDLE_EXTENSION),
+			wildcard=(fileTypeLabel + "|*.{ext}").format(ext=BUNDLE_EXTENSION),
 			defaultDir="c:",
 			style=wx.FD_OPEN,
 		)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\gui\addonStoreGui\viewModels\store.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\addonStoreGui\\viewModels\\store.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\addonStoreGui\\viewModels\\store.py"
index 6adc3f4..36c155f 100644
--- "a/F:\\nvda\\gh\\beta\\source\\gui\\addonStoreGui\\viewModels\\store.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\addonStoreGui\\viewModels\\store.py"
@@ -17,8 +17,6 @@
 import threading
 
 import addonHandler
-from markdown import markdown
-import ui
 from addonStore.dataManager import addonDataManager
 from addonStore.install import installAddon
 from addonStore.models.addon import (
@@ -261,36 +259,6 @@ def _makeActionsList(self):
 				),
 				actionTarget=selectedListItem,
 			),
-			AddonActionVM(
-				# Translators: Label for an action that opens the VirusTotal scan results for the selected addon
-				displayName=pgettext("addonStore", "VirusTotal scan results"),
-				actionHandler=lambda aVM: startfile(cast(_AddonStoreModel, aVM.model).scanResults.scanUrl),
-				validCheck=lambda aVM: isinstance(aVM.model, _AddonStoreModel)
-				and aVM.model.scanResults is not None,
-				actionTarget=selectedListItem,
-			),
-			AddonActionVM(
-				# Translators: Label for an action that shows changelog for the selected addon
-				displayName=pgettext("addonStore", "&What's new"),
-				actionHandler=lambda aVM: ui.browseableMessage(
-					markdown(
-						str(
-							cast(_AddonStoreModel, aVM.model).changelog,
-						),
-					),
-					# Translators: Title for a message showing changes for the current add-on version.
-					title=pgettext("addonStore", "Changes for {curVersion}").format(
-						curVersion=aVM.model.addonVersionName,
-					),
-					isHtml=True,
-					copyButton=True,
-					closeButton=True,
-				),
-				validCheck=lambda aVM: (
-					isinstance(aVM.model, _AddonStoreModel) and aVM.model.changelog is not None
-				),
-				actionTarget=selectedListItem,
-			),
 		]
 
 	def helpAddon(self, listItemVM: AddonListItemVM) -> None:
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\gui\configProfiles.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\configProfiles.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\configProfiles.py"
index 8e33c8b..d29ce69 100644
--- "a/F:\\nvda\\gh\\beta\\source\\gui\\configProfiles.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\configProfiles.py"
@@ -4,11 +4,11 @@
 # See the file COPYING for more details.
 
 import wx
-import NVDAState
 import config
 import api
 import gui
 from logHandler import log
+import globalVars
 from . import guiHelper
 import gui.contextHelp
 
@@ -110,7 +110,7 @@ def __init__(self, parent):
 		self.Bind(wx.EVT_BUTTON, self.onClose, id=wx.ID_CLOSE)
 		self.EscapeId = wx.ID_CLOSE
 
-		if not NVDAState.shouldWriteToDisk():
+		if globalVars.appArgs.secure:
 			for item in newButton, triggersButton, self.renameButton, self.deleteButton:
 				item.Disable()
 		self.onProfileListChoice(None)
@@ -242,7 +242,7 @@ def onProfileListChoice(self, evt):
 			label = _("Manual activate")
 		self.changeStateButton.Label = label
 		self.changeStateButton.Enabled = enable
-		if not NVDAState.shouldWriteToDisk():
+		if globalVars.appArgs.secure:
 			return
 		self.deleteButton.Enabled = enable
 		self.renameButton.Enabled = enable
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\gui\installerGui.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\installerGui.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\installerGui.py"
index 3c90c5e..3e58886 100644
--- "a/F:\\nvda\\gh\\beta\\source\\gui\\installerGui.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\installerGui.py"
@@ -140,7 +140,7 @@ def doInstall(
 	newNVDA = None
 	if startAfterInstall:
 		newNVDA = core.NewNVDAInstance(
-			filePath=os.path.join(WritePaths.defaultInstallDir, "nvda.exe"),
+			filePath=os.path.join(installer.defaultInstallPath, "nvda.exe"),
 			parameters=_generate_executionParameters(),
 		)
 	if not core.triggerNVDAExit(newNVDA):
@@ -219,11 +219,11 @@ def __init__(self, parent, isUpdate):
 				# Translators: An informational message in the Install NVDA dialog.
 				"A previous copy of NVDA has been found on your system. This copy will be updated.",
 			)
-			if not os.path.isdir(WritePaths.defaultInstallDir):
+			if not os.path.isdir(installer.defaultInstallPath):
 				msg += " " + _(
 					# Translators: a message in the installer telling the user NVDA is now located in a different place.
 					"The installation path for NVDA has changed. it will now  be installed in {path}",
-				).format(path=WritePaths.defaultInstallDir)
+				).format(path=installer.defaultInstallPath)
 		if shouldAskAboutAddons:
 			msg += "\n\n" + getAddonCompatibilityMessage()
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\gui\nvdaControls.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\nvdaControls.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\nvdaControls.py"
index a43d044..bd3524e 100644
--- "a/F:\\nvda\\gh\\beta\\source\\gui\\nvdaControls.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\nvdaControls.py"
@@ -14,6 +14,7 @@
 import warnings
 
 import wx
+from wx.lib import scrolledpanel
 from wx.lib.mixins import listctrl as listmix
 
 import config
@@ -42,6 +43,7 @@
 	"MessageDialog",
 	"_ContinueCancelDialog",
 	"EnhancedInputSlider",
+	"TabbableScrolledPanel",
 	"FeatureFlagCombo",
 ]
 
@@ -432,6 +434,44 @@ def onSliderChar(self, evt):
 		self.SetValue(newValue)
 
 
+class TabbableScrolledPanel(scrolledpanel.ScrolledPanel):
+	"""
+	This class was created to ensure a ScrolledPanel scrolls to nested children of the panel when navigating
+	with tabs (#12224). A PR to wxPython implementing this fix can be tracked on
+	https://github.com/wxWidgets/Phoenix/pull/1950
+	"""
+
+	def GetChildRectRelativeToSelf(self, child: wx.Window) -> wx.Rect:
+		"""
+		window.GetRect returns the size of a window, and its position relative to its parent.
+		When calculating ScrollChildIntoView, the position relative to its parent is not relevant unless the
+		parent is the ScrolledPanel itself. Instead, calculate the position relative to scrolledPanel
+		"""
+		childRectRelativeToScreen = child.GetScreenRect()
+		scrolledPanelScreenPosition = self.GetScreenPosition()
+		return wx.Rect(
+			childRectRelativeToScreen.x - scrolledPanelScreenPosition.x,
+			childRectRelativeToScreen.y - scrolledPanelScreenPosition.y,
+			childRectRelativeToScreen.width,
+			childRectRelativeToScreen.height,
+		)
+
+	def ScrollChildIntoView(self, child: wx.Window) -> None:
+		"""
+		Overrides child.GetRect with `GetChildRectRelativeToSelf` before calling
+		`super().ScrollChildIntoView`. `super().ScrollChildIntoView` incorrectly uses child.GetRect to
... (残り 14 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\hwIo\ioThread.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\hwIo\\ioThread.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\hwIo\\ioThread.py"
index fbcc13f..e88298e 100644
--- "a/F:\\nvda\\gh\\beta\\source\\hwIo\\ioThread.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\hwIo\\ioThread.py"
@@ -207,7 +207,7 @@ def setWaitableTimer(
 		winKernel.setWaitableTimer(
 			handle,
 			dueTime,
-			completionRoutine=ctypes.cast(self._internalApc, winBindings.kernel32.PTIMERAPCROUTINE),
+			completionRoutine=self._internalApc,
 			arg=internalParam,
 		)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\IAccessibleHandler\__init__.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\IAccessibleHandler\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\IAccessibleHandler\\__init__.py"
index 8e7e93b..44405be 100644
--- "a/F:\\nvda\\gh\\beta\\source\\IAccessibleHandler\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\IAccessibleHandler\\__init__.py"
@@ -369,11 +369,10 @@ def accessibleObjectFromPoint(x, y):
 	return normalizeIAccessible(pacc, child), child
 
 
-def windowFromAccessibleObject(ia) -> int:
+def windowFromAccessibleObject(ia):
 	try:
 		return oleacc.WindowFromAccessibleObject(ia)
-	except WindowsError:
-		log.debugWarning("windowFromAccessibleObject failed", exc_info=True)
+	except:  # noqa: E722 Bare except
 		return 0
 
 
@@ -602,15 +601,20 @@ def winEventToNVDAEvent(  # noqa: C901
 	return (NVDAEventName, obj)
 
 
-def processGenericWinEvent(eventID: int, window: int, objectID: int, childID: int) -> bool:
+def processGenericWinEvent(eventID, window, objectID, childID):
 	"""Converts the win event to an NVDA event,
 	Checks to see if this NVDAObject  equals the current focus.
 	If all goes well, then the event is queued and we return True
-	:param eventID: a win event ID (type)
-	:param window: a win event's window handle
-	:param objectID: a win event's object ID
-	:param childID: a win event's child ID
-	:return: True if the event was processed, False otherwise.
+	@param eventID: a win event ID (type)
+	@type eventID: integer
+	@param window: a win event's window handle
+	@type window: integer
+	@param objectID: a win event's object ID
+	@type objectID: integer
+	@param childID: a win event's child ID
+	@type childID: integer
+	@returns: True if the event was processed, False otherwise.
+	@rtype: boolean
 	"""
 	if isMSAADebugLoggingEnabled():
 		log.debug(
@@ -676,15 +680,19 @@ def processGenericWinEvent(eventID: int, window: int, objectID: int, childID: in
 	return True
 
 
-def processFocusWinEvent(window: int, objectID: int, childID: int, force: bool = False) -> bool:
... (残り 57 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\IAccessibleHandler\internalWinEventHandler.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\IAccessibleHandler\\internalWinEventHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\IAccessibleHandler\\internalWinEventHandler.py"
index 4669248..e2b17d4 100644
--- "a/F:\\nvda\\gh\\beta\\source\\IAccessibleHandler\\internalWinEventHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\IAccessibleHandler\\internalWinEventHandler.py"
@@ -66,17 +66,7 @@
 
 
 # C901: winEventCallback is too complex
-def winEventCallback(
-	handle: int | None,
-	eventID: int,
-	window: int | None,
-	objectID: int,
-	childID: int,
-	threadID: int,
-	timestamp: int,
-) -> None:  # noqa: C901
-	if window is None:
-		window = 0
+def winEventCallback(handle, eventID, window, objectID, childID, threadID, timestamp):  # noqa: C901
 	if isMSAADebugLoggingEnabled():
 		log.debug(
 			f"Hook received winEvent: {getWinEventLogInfo(window, objectID, childID, eventID, threadID)}",
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\IAccessibleHandler\orderedWinEventLimiter.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\IAccessibleHandler\\orderedWinEventLimiter.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\IAccessibleHandler\\orderedWinEventLimiter.py"
index 2e6575d..d58fb5a 100644
--- "a/F:\\nvda\\gh\\beta\\source\\IAccessibleHandler\\orderedWinEventLimiter.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\IAccessibleHandler\\orderedWinEventLimiter.py"
@@ -50,12 +50,12 @@ def addEvent(
 		threadID: int,
 	) -> bool:
 		"""Adds a winEvent to the limiter.
-		:param eventID: the winEvent type
-		:param window: the window handle of the winEvent
-		:param objectID: the objectID of the winEvent
-		:param childID: the childID of the winEvent
-		:param threadID: the threadID of the winEvent
-		:return: C{True} if the event was added, C{False} if it was discarded.
+		@param eventID: the winEvent type
+		@param window: the window handle of the winEvent
+		@param objectID: the objectID of the winEvent
+		@param childID: the childID of the winEvent
+		@param threadID: the threadID of the winEvent
+		@return: C{True} if the event was added, C{False} if it was discarded.
 		"""
 		if eventID == winUser.EVENT_OBJECT_FOCUS:
 			if objectID in (winUser.OBJID_SYSMENU, winUser.OBJID_MENU) and childID == 0:
@@ -83,13 +83,13 @@ def addEvent(
 	def flushEvents(
 		self,
 		alwaysAllowedObjects: Optional[List[IAccessibleObjectIdentifierType]] = None,
-	) -> list[tuple[int, int, int, int]]:
+	) -> List:
 		"""Returns a list of winEvents that have been added.
 		Due to limiting, it will not necessarily be all the winEvents that were originally added.
 		They are definitely guaranteed to be in the correct order though.
 		winEvents for objects listed in alwaysAllowedObjects will always be emitted,
 		Even if the winEvent limit for that thread has been exceeded.
-		:return: a list of tuples with eventID,window,objectID,childID
+		@return Tuple[eventID,window,objectID,childID]
 		"""
 		if self._lastMenuEvent is not None:
 			heapq.heappush(self._eventHeap, self._lastMenuEvent)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\inputCore.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\inputCore.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\inputCore.py"
index 3bcfc19..d2529a4 100644
--- "a/F:\\nvda\\gh\\beta\\source\\inputCore.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\inputCore.py"
@@ -43,7 +43,7 @@
 import languageHandler
 import controlTypes
 import extensionPoints
-from NVDAState import WritePaths, shouldWriteToDisk
+from NVDAState import WritePaths
 
 
 InputGestureBindingClassT = TypeVar("InputGestureBindingClassT")
@@ -438,9 +438,6 @@ def save(self):
 		"""Save this gesture map to disk.
 		@precondition: L{load} must have been called.
 		"""
-		if not shouldWriteToDisk():
-			log.debug("Not saving user gesture map, as shouldWriteToDisk returned false.")
-			return
 		if not self.fileName:
 			raise ValueError("No file name")
 		out = configobj.ConfigObj(self.export(), encoding="UTF-8")
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\markdownTranslate.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\markdownTranslate.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\markdownTranslate.py"
index 0e9e333..341ead6 100644
--- "a/F:\\nvda\\gh\\beta\\source\\markdownTranslate.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\markdownTranslate.py"
@@ -4,7 +4,6 @@
 # See the file COPYING for more details.
 
 from typing import Generator
-from collections.abc import Iterable
 import tempfile
 import os
 import contextlib
@@ -30,7 +29,6 @@
 re_postTableHeaderLine = re.compile(r"^(\|\s*-+\s*)+\|$")
 re_tableRow = re.compile(r"^(\|)(.+)(\|)$")
 re_translationID = re.compile(r"^(.*)\$\(ID:([0-9a-f-]+)\)(.*)$")
-re_inlineMarkdownLintComment = re.compile(r"^(.*?)(?:\s*<!-- markdownlint.*-->)(\s*)$")
 
 
 def prettyPathString(path: str) -> str:
@@ -90,18 +88,6 @@ def getRawGithubURLForPath(filePath: str) -> str:
 	return f"{RAW_GITHUB_REPO_URL}/{commitID}/{relativePath}"
 
 
-def preprocessMarkdownLines(mdLines: Iterable[str]) -> Iterable[str]:
-	"""
-	Preprocess markdown lines such as removing inline markdown lint comments.\
-	:param mdLines: The markdown lines to preprocess
-	:returns: The preprocessed markdown lines
-	"""
-	for mdLine in mdLines:
-		# #18982: Remove markdown lint comments completely - not needed for intermediate markdown or final html.
-		mdLine = re_inlineMarkdownLintComment.sub(r"\1\2", mdLine)
-		yield mdLine
-
-
 def skeletonizeLine(mdLine: str) -> str | None:
 	prefix = ""
 	suffix = ""
@@ -143,7 +129,7 @@ def generateSkeleton(mdPath: str, outputPath: str) -> Result_generateSkeleton:
 		open(mdPath, "r", encoding="utf8") as mdFile,
 		open(outputPath, "w", encoding="utf8", newline="") as outputFile,
 	):
-		for mdLine in preprocessMarkdownLines(mdFile.readlines()):
+		for mdLine in mdFile.readlines():
 			res.numTotalLines += 1
 			skelLine = skeletonizeLine(mdLine)
 			if skelLine:
@@ -199,9 +185,7 @@ def updateSkeleton(
 		newMdFile = stack.enter_context(open(newMdPath, "r", encoding="utf8"))
... (残り 48 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\mathPres\MathCAT\MathCAT.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\mathPres\\MathCAT\\MathCAT.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\mathPres\\MathCAT\\MathCAT.py"
index 00de1eb..db39595 100644
--- "a/F:\\nvda\\gh\\beta\\source\\mathPres\\MathCAT\\MathCAT.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\mathPres\\MathCAT\\MathCAT.py"
@@ -42,7 +42,6 @@
 
 import mathPres
 from .localization import getLanguageToUse
-from .preferences import setEffectiveBrailleCode
 from .speech import convertSSMLTextForNVDA
 
 
@@ -333,7 +332,6 @@ def __init__(self):
 			log.info(f"MathCAT {libmathcat.GetVersion()} installed. Using rules dir: {rulesDir}")
 			libmathcat.SetRulesDir(rulesDir)
 			libmathcat.SetPreference("TTS", "SSML")
-			setEffectiveBrailleCode()
 		except Exception:
 			log.exception()
 			# Translators: this message directs users to look in the log file
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\mathPres\MathCAT\preferences.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\mathPres\\MathCAT\\preferences.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\mathPres\\MathCAT\\preferences.py"
index 67a3d3f..10be2c4 100644
--- "a/F:\\nvda\\gh\\beta\\source\\mathPres\\MathCAT\\preferences.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\mathPres\\MathCAT\\preferences.py"
@@ -7,8 +7,8 @@
 import os
 
 import config
-import languageHandler
 import yaml
+from languageHandler import getLanguage
 from logHandler import log
 from NVDAState import ReadPaths
 from utils.displayString import DisplayStringStrEnum
@@ -241,7 +241,7 @@ def getAutoBrailleCode(
 	if not availableCodes:
 		availableCodes = getBrailleCodes()
 	if languageCode is None:
-		languageCode = languageHandler.getLanguage()
+		languageCode = getLanguage()
 
 	# de, nb, and nn should probably use Marburg when implemented upstream
 	languagesToBrailleCodes: dict[str, str] = {
@@ -285,7 +285,6 @@ def setEffectiveBrailleCode() -> None:
 			exc_info=True,
 		)
 
-
 def toNVDAConfigKey(key: str) -> str:
 	"""Converts a key for MathCAT's preferences (UpperCamelCase) to a
 	key for NVDA's configobj-based configuration (lowerCamelCase).
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\NVDAHelper\localLib.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\NVDAHelper\\localLib.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAHelper\\localLib.py"
index 9c55b8b..7b56faa 100644
--- "a/F:\\nvda\\gh\\beta\\source\\NVDAHelper\\localLib.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAHelper\\localLib.py"
@@ -666,7 +666,7 @@ class EXCEL_CELLINFO(Structure):
 )
 
 isScreenFullyBlack = dll.isScreenFullyBlack
-isScreenFullyBlack.argtypes = ()
+isScreenFullyBlack.argtypes = tuple()
 isScreenFullyBlack.restype = c_bool
 
 localListeningSocketExists = dll.localListeningSocketExists
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\NVDAObjects\IAccessible\__init__.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\IAccessible\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\__init__.py"
index 5e6e77d..8273713 100644
--- "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\IAccessible\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\__init__.py"
@@ -650,6 +650,10 @@ def findOverlayClasses(self, clsList):
 			from . import mscandui
 
 			mscandui.findExtraOverlayClasses(self, clsList)
+		elif windowClassName[:5] in ("ATOK2", "ATOK3"):
+			from . import atok
+
+			atok.findExtraOverlayClasses(self, clsList)
 		elif (
 			windowClassName == "GeckoPluginWindow"
 			and self.event_objectID == 0
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\NVDAObjects\IAccessible\adobeAcrobat.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\IAccessible\\adobeAcrobat.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\adobeAcrobat.py"
index 631fc36..5feb3b4 100644
--- "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\IAccessible\\adobeAcrobat.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\adobeAcrobat.py"
@@ -175,7 +175,7 @@ def _getNodeMathMl(self, node: IPDDomElement) -> str:
 		answer += ">"
 		val = node.GetValue()
 		if val:
-			answer += html.escape(val)
+			answer += val
 		else:
 			for childNum in range(node.GetChildCount()):
 				try:
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\NVDAObjects\IAccessible\sysListView32.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\IAccessible\\sysListView32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\sysListView32.py"
index 3ed2abb..a62b3bd 100644
--- "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\IAccessible\\sysListView32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\sysListView32.py"
@@ -8,7 +8,6 @@
 import ctypes
 from ctypes.wintypes import *  # noqa: F403
 from comtypes import BSTR
-from enum import IntFlag
 import NVDAHelper
 import watchdog
 import controlTypes
@@ -23,7 +22,6 @@
 from locationHelper import RectLTRB
 from logHandler import log
 from typing import Optional
-from utils import _deprecate
 
 # Window messages
 LVM_FIRST = 0x1000
@@ -68,49 +66,9 @@
 LVIS_SELECTED = 0x02
 LVIS_STATEIMAGEMASK = 0xF000
 
-
-class ListViewWindowStyle(IntFlag):
-	"""Window styles  specific to list-view controls.
-
-	.. seealso::
-		https://learn.microsoft.com/en-us/windows/win32/controls/list-view-window-styles
-	"""
-
-	REPORT = 0x0001
-	"""This style specifies report view."""
-	TYPEMASK = 0x0003
-	"""Determines the control's current window style."""
-	SINGLESEL = 0x0004
-	"""Only one item at a time can be selected.
-	By default, multiple items may be selected."""
-	OWNERDRAWFIXED = 0x0400
-	"""The owner window can paint items in report view."""
-
-
-__getattr__ = _deprecate.handleDeprecations(
-	_deprecate.MovedSymbol(
-		"LVS_REPORT",
-		__name__,
-		"ListViewWindowStyle",
-		"REPORT",
-		"value",
... (残り 73 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\NVDAObjects\UIA\wordDocument.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\UIA\\wordDocument.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\UIA\\wordDocument.py"
index c160ddf..f5603d8 100644
--- "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\UIA\\wordDocument.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\UIA\\wordDocument.py"
@@ -412,10 +412,10 @@ def getTextWithFields(  # noqa: C901
 			return fields
 
 		# MS Word tries to produce speakable math content within equations.
-		# However, using math presentation providers with the exposed mathml property on the equation is much nicer.
+		# However, using mathPlayer with the exposed mathml property on the equation is much nicer.
 		# But, we therefore need to remove the inner math content if reading by line
 		if not formatConfig or not formatConfig.get("extraDetail"):
-			# We really only want to remove content if we can guarantee that a math presentation provider is available.
+			# We really only want to remove content if we can guarantee that mathPlayer is available.
 			if mathPres.speechProvider or mathPres.brailleProvider:
 				curLevel = 0
 				mathLevel = None
@@ -601,7 +601,7 @@ def _shouldSetFocusToObj(self, obj: NVDAObject) -> bool:
 		):
 			return False
 		elif obj.role == controlTypes.Role.MATH:
-			# Don't set focus to math equations otherwise they cannot be interacted  with by math presentation providers.
+			# Don't set focus to math equations otherwise they cannot be interacted  with mathPlayer.
 			return False
 		return super()._shouldSetFocusToObj(obj)
 
@@ -612,7 +612,7 @@ def shouldPassThrough(self, obj, reason=None):
 		):
 			return False
 		elif obj.role == controlTypes.Role.MATH:
-			# Don't  activate focus mode for math equations otherwise they cannot be interacted  with by math presentation providers.
+			# Don't  activate focus mode for math equations otherwise they cannot be interacted  with mathPlayer.
 			return False
 		return super(WordBrowseModeDocument, self).shouldPassThrough(obj, reason=reason)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\NVDAState.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\NVDAState.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAState.py"
index f08f227..54d1a86 100644
--- "a/F:\\nvda\\gh\\beta\\source\\NVDAState.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAState.py"
@@ -3,9 +3,7 @@
 # This file may be used under the terms of the GNU General Public License, version 2 or later.
 # For more details see: https://www.gnu.org/licenses/gpl-2.0.html
 
-from functools import lru_cache
 import os
-import platform
 import sys
 import sysconfig
 import time
@@ -43,10 +41,6 @@ def addonStoreDownloadDir(self) -> str:
 	def profilesDir(self) -> str:
 		return os.path.join(self.configDir, "profiles")
 
-	@property
-	def remoteAccessDir(self) -> str:
-		return os.path.join(self.configDir, "remoteAccess")
-
 	@property
 	def scratchpadDir(self) -> str:
 		return os.path.join(self.configDir, "scratchpad")
@@ -101,97 +95,6 @@ def updateCheckStateFile(self) -> str:
 	def guiStateFile(self) -> str:
 		return os.path.join(self.configDir, "guiState.ini")
 
-	@property
-	def defaultStartMenuFolder(self) -> str:
-		"""Name of a specific folder in the start menu, not a full path"""
-		return buildVersion.name
-
-	@property
-	@lru_cache(maxsize=1)
-	def startMenuFolder(self) -> str | None:
-		"""Name of a specific folder in the start menu, not a full path"""
-		from config.registry import RegistryKey
-
-		try:
-			with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value) as k:
-				return winreg.QueryValueEx(k, "Start Menu Folder")[0]
-		except WindowsError:
-			return None
-
-	@property
-	@lru_cache(maxsize=1)
-	def _startMenuFolderX86(self) -> str | None:
-		"""Name of a specific folder in the start menu, not a full path"""
... (残り 100 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\oleacc.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\oleacc.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\oleacc.py"
index 1c6168d..c1457e9 100644
--- "a/F:\\nvda\\gh\\beta\\source\\oleacc.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\oleacc.py"
@@ -5,7 +5,6 @@
 
 from ctypes import *  # noqa: F403
 from ctypes.wintypes import *  # noqa: F403
-from ctypes.wintypes import HWND
 from comtypes import *  # noqa: F403
 from comtypes.automation import *  # noqa: F403
 import comtypes.client
@@ -313,16 +312,17 @@ def AccessibleObjectFromEvent_safe(hwnd, objectID, childID, timeout=2):
 	return (obj, childID)
 
 
-def WindowFromAccessibleObject(pacc) -> int:
+def WindowFromAccessibleObject(pacc):
 	"""
-	Retrieves the handle of the window this IAccessible object belongs to.
-	:param pacc: the IAccessible object who's window you want to fetch.
-	:type pacc: POINTER(IAccessible)
-	:return: the window handle.
+	Retreaves the handle of the window this IAccessible object belongs to.
+	@param pacc: the IAccessible object who's window you want to fetch.
+	@type pacc: POINTER(IAccessible)
+	@return: the window handle.
+	@rtype: int
 	"""
-	hwnd = HWND()
+	hwnd = c_int()  # noqa: F405
 	winBindings.oleacc.WindowFromAccessibleObject(pacc, byref(hwnd))  # noqa: F405
-	return hwnd.value or 0
+	return hwnd.value
 
 
 def AccessibleObjectFromPoint(x, y):
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\screenBitmap.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\screenBitmap.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\screenBitmap.py"
index da079b2..54ad64b 100644
--- "a/F:\\nvda\\gh\\beta\\source\\screenBitmap.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\screenBitmap.py"
@@ -64,7 +64,7 @@ def captureImage(self, x, y, w, h):
 			winGDI.SRCCOPY,
 		)
 		# Fetch the pixels from our memory bitmap and store them in a buffer to be returned
-		buffer = (winBindings.gdi32.RGBQUAD * self.width * self.height)()
+		buffer = (winBindings.gdi32.RGBQUAD * (self.width * self.height))()
 		winBindings.gdi32.GetDIBits(
 			self._memDC,
 			self._memBitmap,
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
index 830b57b..c24c2af 100644
--- "a/F:\\nvda\\gh\\beta\\source\\speech\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\speech\\__init__.py"
@@ -35,7 +35,7 @@
 	getTextInfoSpeech,
 	IDT_BASE_FREQUENCY,
 	IDT_MAX_SPACES,
-	getIndentToneDuration,
+	IDT_TONE_DURATION,
 	isBlank,
 	LANGS_WITH_CONJUNCT_CHARS,
 	pauseSpeech,
@@ -115,7 +115,7 @@
 	"getTextInfoSpeech",
 	"IDT_BASE_FREQUENCY",
 	"IDT_MAX_SPACES",
-	"getIndentToneDuration",
+	"IDT_TONE_DURATION",
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

### ⚫ **要確認**: `source\speech\speech.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\speech\\speech.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\speech\\speech.py"
index bb6b873..48a48ee 100644
--- "a/F:\\nvda\\gh\\beta\\source\\speech\\speech.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\speech\\speech.py"
@@ -6,6 +6,7 @@
 
 """High-level functions to speak information."""
 
+import jpUtils
 import itertools
 import typing
 import weakref
@@ -190,6 +191,7 @@ def processText(
 	text = speechDictHandler.processText(text)
 	text = characterProcessing.processSpeechSymbols(locale, text, symbolLevel)
 	text = RE_CONVERT_WHITESPACE.sub(" ", text)
+	text = jpUtils.processKangxiRadicals(text)
 	if normalize:
 		text = unicodeNormalize(text)
 		# keep leading space for normalization message
@@ -311,11 +313,17 @@ def getCurrentLanguage() -> str:
 def spellTextInfo(
 	info: textInfos.TextInfo,
 	useCharacterDescriptions: bool = False,
+	useDetails: bool = False,
 	priority: Optional[Spri] = None,
 ) -> None:
 	"""Spells the text from the given TextInfo, honouring any LangChangeCommand objects it finds if autoLanguageSwitching is enabled."""
 	if not languageHandling.shouldMakeLangChangeCommand():
-		speakSpelling(info.text, useCharacterDescriptions=useCharacterDescriptions)
+		speakSpelling(
+			info.text,
+			useCharacterDescriptions=useCharacterDescriptions,
+			useDetails=useDetails,
+			priority=priority,
+		)
 		return
 	curLanguage = None
 	for field in info.getTextWithFields({}):
@@ -324,6 +332,7 @@ def spellTextInfo(
 				field,
 				curLanguage,
 				useCharacterDescriptions=useCharacterDescriptions,
+				useDetails=useDetails,
 				priority=priority,
 			)
 		elif isinstance(field, textInfos.FieldCommand) and field.command == "formatChange":
@@ -334,6 +343,7 @@ def speakSpelling(
 	text: str,
 	locale: Optional[str] = None,
... (残り 108 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\speechDictHandler\__init__.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\speechDictHandler\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\speechDictHandler\\__init__.py"
index bafa772..ac0794d 100644
--- "a/F:\\nvda\\gh\\beta\\source\\speechDictHandler\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\speechDictHandler\\__init__.py"
@@ -10,7 +10,7 @@
 import os
 import codecs
 
-from NVDAState import WritePaths, shouldWriteToDisk
+from NVDAState import WritePaths
 from . import dictFormatUpgrade
 
 
@@ -118,9 +118,6 @@ def load(self, fileName):
 		return
 
 	def save(self, fileName=None):
-		if not shouldWriteToDisk():
-			log.debugWarning("Not writing dictionary, as shouldWriteToDisk returned False.")
-			return
 		if not fileName:
 			fileName = getattr(self, "fileName", None)
 		if not fileName:
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\versionInfo.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\versionInfo.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\versionInfo.py"
index e504ce0..05627c6 100644
--- "a/F:\\nvda\\gh\\beta\\source\\versionInfo.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\versionInfo.py"
@@ -29,11 +29,9 @@
 URL: {url}
 {copyright}
 
-{name} is covered by the GNU General Public License (Version 2 or later).
-You are free to share or change this software in any way you like as long as it is accompanied by the license and you make all source code available to anyone who wants it.
-This applies to both original and modified copies of this software, plus any derivative works.
+{name} is covered by the GNU General Public License (Version 2). You are free to share or change this software in any way you like as long as it is accompanied by the license and you make all source code available to anyone who wants it. This applies to both original and modified copies of this software, plus any derivative works.
 For further details, you can view the license from the Help menu.
-It can also be viewed online at: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html and https://www.gnu.org/licenses/gpl-3.0.en.html
+It can also be viewed online at: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
 
 {name} is developed by NV Access, a non-profit organisation committed to helping and promoting free and open source solutions for blind and vision impaired people.
 If you find NVDA useful and want it to continue to improve, please consider donating to NV Access. You can do this by selecting Donate from the NVDA menu.""",  # noqa: E501 line too long
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\visionEnhancementProviders\NVDAHighlighter.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\visionEnhancementProviders\\NVDAHighlighter.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\visionEnhancementProviders\\NVDAHighlighter.py"
index ea881f6..e8e5f4e 100644
--- "a/F:\\nvda\\gh\\beta\\source\\visionEnhancementProviders\\NVDAHighlighter.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\visionEnhancementProviders\\NVDAHighlighter.py"
@@ -24,7 +24,7 @@
 )
 import api
 from ctypes import byref, WinError
-from ctypes.wintypes import MSG
+from ctypes.wintypes import COLORREF, MSG
 import winUser
 from logHandler import log
 from mouseHandler import getTotalWidthAndHeightAndMinimumPosition
@@ -32,7 +32,6 @@
 from collections import namedtuple
 import threading
 from winAPI.messageWindow import WindowMessage
-import winBindings.gdi32
 import winGDI
 import weakref
 from colors import RGB
@@ -95,7 +94,7 @@ class HighlightWindow(CustomWindow):
 	def _get__wClass(cls):
 		wClass = super()._wClass
 		wClass.style = winUser.CS_HREDRAW | winUser.CS_VREDRAW
-		wClass.hbrBackground = winBindings.gdi32.CreateSolidBrush(cls.transparentColor)
+		wClass.hbrBackground = winGDI.gdi32.CreateSolidBrush(COLORREF(cls.transparentColor))
 		return wClass
 
 	def updateLocationForDisplays(self):
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\vkCodes.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\vkCodes.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\vkCodes.py"
index 63c801c..b983bdb 100644
--- "a/F:\\nvda\\gh\\beta\\source\\vkCodes.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\vkCodes.py"
@@ -31,6 +31,7 @@
 	(0x13, None): "pause",
 	(0x14, None): "capsLock",
 	(0x18, None): "IMEFinalMode",
+	(0x19, None): "IMEChangeStatus1",
 	(0x1B, None): "escape",
 	(0x1C, None): "IMEConvert",
 	(0x1D, None): "IMENonconvert",
@@ -132,6 +133,8 @@
 	(0xB5, None): "launchMediaPlayer",
 	(0xB6, None): "launchApp1",
 	(0xB7, None): "launchApp2",
+	(0xF3, None): "IMEChangeStatus2",
+	(0xF4, None): "IMEChangeStatus3",
 }
 
 #: Maps key names to vk codes.
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\watchdog.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\watchdog.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\watchdog.py"
index c9f55be..bf47358 100644
--- "a/F:\\nvda\\gh\\beta\\source\\watchdog.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\watchdog.py"
@@ -4,6 +4,7 @@
 # See the file COPYING for more details.
 
 import sys
+import os
 import time
 from time import perf_counter as _timer
 import threading
@@ -13,19 +14,15 @@
 import inspect
 import ctypes.wintypes
 import comtypes
-import globalVars
 import winBindings.ole32
 import winBindings.dbgHelp
 import winBindings.kernel32
+from winBindings.kernel32 import UnhandledExceptionFilter
 import winUser
 import winKernel
 from logHandler import log
 import logHandler
-from utils._crashHandler import (
-	CRASH_STATS,
-	crashHandler,
-	loadRecentCrashTimestamps,
-)
+import globalVars
 import core
 import exceptions
 import NVDAHelper
@@ -239,6 +236,30 @@ def _recoverAttempt():
 		pass
 
 
+@UnhandledExceptionFilter
+def _crashHandler(exceptionInfo):
+	threadId = winBindings.kernel32.GetCurrentThreadId()
+	# An exception might have been set for this thread.
+	# Clear it so that it doesn't get raised in this function.
+	ctypes.pythonapi.PyThreadState_SetAsyncExc(threadId, None)
+
+	# Write a minidump.
+	dumpPath = os.path.join(os.path.dirname(globalVars.appArgs.logFileName), "nvda_crash.dmp")
+	if not NVDAHelper.localLib.writeCrashDump(dumpPath, exceptionInfo):
+		log.critical("NVDA crashed! Error writing minidump", exc_info=True)
+	else:
... (残り 37 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winAPI\_powerTracking.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winAPI\\_powerTracking.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winAPI\\_powerTracking.py"
index 26ada01..b697f01 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winAPI\\_powerTracking.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winAPI\\_powerTracking.py"
@@ -218,21 +218,6 @@ def _getBatteryInformation(systemPowerStatus: SystemPowerStatus) -> List[str]:
 	SECONDS_PER_MIN = 60
 	if systemPowerStatus.BatteryLifeTime != BATTERY_LIFE_TIME_UNKNOWN:
 		nHours = systemPowerStatus.BatteryLifeTime // SECONDS_PER_HOUR
-		nMinutes = (systemPowerStatus.BatteryLifeTime % SECONDS_PER_HOUR) // SECONDS_PER_MIN
-
-		# Skip if no time, as it likely means the status check is inaccurate
-		if systemPowerStatus.BatteryLifeTime == 0:
-			return text
-		if nHours == 0 and nMinutes == 0:
-			# Translators: Reported when battery time is less than 1 minute.
-			text.append(_("Less than 1 minute remaining"))
-			return text
-
-		hourText: str | None = None
-		minuteText: str | None = None
-
-		# Handle hours - only if greater than 0
-		if nHours > 0:
 		hourText = ngettext(
 			# Translators: This is the hour string part of the estimated remaining runtime of the laptop battery.
 			# E.g. if the full string is "1 hour and 34 minutes remaining", this string is "1 hour".
@@ -240,9 +225,7 @@ def _getBatteryInformation(systemPowerStatus: SystemPowerStatus) -> List[str]:
 			"{hours:d} hours",
 			nHours,
 		).format(hours=nHours)
-
-		# Handle minutes - only if greater than 0
-		if nMinutes > 0:
+		nMinutes = (systemPowerStatus.BatteryLifeTime % SECONDS_PER_HOUR) // SECONDS_PER_MIN
 		minuteText = ngettext(
 			# Translators: This is the minute string part of the estimated remaining runtime of the laptop battery.
 			# E.g. if the full string is "1 hour and 34 minutes remaining", this string is "34 minutes".
@@ -250,24 +233,9 @@ def _getBatteryInformation(systemPowerStatus: SystemPowerStatus) -> List[str]:
 			"{minutes:d} minutes",
 			nMinutes,
 		).format(minutes=nMinutes)
-
-		# Combine hours and minutes appropriately
-		if hourText is not None and minuteText is not None:
 		text.append(
 			# Translators: This is the main string for the estimated remaining runtime of the laptop battery.
 			# E.g. hourText is replaced by "1 hour" and minuteText by "34 minutes".
 			_("{hourText} and {minuteText} remaining").format(hourText=hourText, minuteText=minuteText),
 		)
-		elif hourText is not None:
... (残り 12 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\bthprops.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\bthprops.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\bthprops.py"
index 89349e8..d615a9f 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\bthprops.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\bthprops.py"
@@ -14,7 +14,7 @@
 )
 from ctypes.wintypes import BOOL, DWORD, HANDLE, ULONG, WCHAR
 
-from winBindings.kernel32 import SYSTEMTIME
+from winKernel import SYSTEMTIME
 
 cpl = windll["bthprops.cpl"]
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\cfgmgr32.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\cfgmgr32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\cfgmgr32.py"
index faf7d36..56d1ac2 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\cfgmgr32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\cfgmgr32.py"
@@ -5,11 +5,7 @@
 
 """Functions exported by cfgmgr32.dll, and supporting data structures and enumerations."""
 
-from ctypes import (
-	WINFUNCTYPE,
-	c_wchar_p,
-	windll,
-)
+from ctypes import c_wchar_p, windll
 from ctypes.wintypes import DWORD, ULONG
 
 dll = windll.cfgmgr32
@@ -17,7 +13,7 @@
 CR_SUCCESS = 0
 MAX_DEVICE_ID_LEN = 200
 
-CM_Get_Device_ID = WINFUNCTYPE(None)(("CM_Get_Device_IDW", dll))
+CM_Get_Device_ID = dll.CM_Get_Device_IDW
 """
 Retrieves the device instance ID for a specified device instance on the local machine.
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\dbgHelp.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\dbgHelp.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\dbgHelp.py"
index b41b016..7b13700 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\dbgHelp.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\dbgHelp.py"
@@ -6,7 +6,6 @@
 """Functions exported by dbgHelp.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	c_void_p,
 	POINTER,
 	Structure,
@@ -38,7 +37,7 @@ class MINIDUMP_EXCEPTION_INFORMATION(Structure):
 dll = windll.dbgHelp
 
 
-MiniDumpWriteDump = WINFUNCTYPE(None)(("MiniDumpWriteDump", dll))
+MiniDumpWriteDump = dll.MiniDumpWriteDump
 """
 Writes a memory dump of the specified process to a file.
 .. seealso::
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\gdi32.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\gdi32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\gdi32.py"
index 06c4047..40e99bd 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\gdi32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\gdi32.py"
@@ -6,7 +6,6 @@
 """Functions exported by gdi32.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	Structure,
 	c_ubyte,
 	c_int,
@@ -33,7 +32,7 @@
 dll = windll.gdi32
 
 
-GetDeviceCaps = WINFUNCTYPE(None)(("GetDeviceCaps", dll))
+GetDeviceCaps = dll.GetDeviceCaps
 """
 Retrieves device-specific information for the specified device.
 
@@ -47,7 +46,7 @@
 )
 
 
-CreateCompatibleDC = WINFUNCTYPE(None)(("CreateCompatibleDC", dll))
+CreateCompatibleDC = dll.CreateCompatibleDC
 """
 Creates a memory device context (DC) compatible with the specified device.
 
@@ -60,7 +59,7 @@
 )
 
 
-CreateCompatibleBitmap = WINFUNCTYPE(None)(("CreateCompatibleBitmap", dll))
+CreateCompatibleBitmap = dll.CreateCompatibleBitmap
 """
 Creates a bitmap compatible with the device that is associated with the specified device context.
 
@@ -75,7 +74,7 @@
 )
 
 
-SelectObject = WINFUNCTYPE(None)(("SelectObject", dll))
+SelectObject = dll.SelectObject
 """
 Selects an object into the specified device context (DC).
 
@@ -89,7 +88,7 @@
 )
... (残り 51 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\gdiplus.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\gdiplus.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\gdiplus.py"
index a9b5b81..cf38551 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\gdiplus.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\gdiplus.py"
@@ -6,7 +6,6 @@
 """Functions exported by gdiplus.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	Structure,
 	c_float,
 	c_int,
@@ -66,7 +65,7 @@ class GdiplusStartupOutput(Structure):
 	]
 
 
-GdiplusStartup = WINFUNCTYPE(None)(("GdiplusStartup", dll))
+GdiplusStartup = dll.GdiplusStartup
 """
 Initializes Windows GDI+.
 
@@ -81,7 +80,7 @@ class GdiplusStartupOutput(Structure):
 )
 
 
-GdiplusShutdown = WINFUNCTYPE(None)(("GdiplusShutdown", dll))
+GdiplusShutdown = dll.GdiplusShutdown
 """
 Cleans up resources used by Windows GDI+.
 
@@ -94,7 +93,7 @@ class GdiplusStartupOutput(Structure):
 )
 
 
-GdipCreateFromHDC = WINFUNCTYPE(None)(("GdipCreateFromHDC", dll))
+GdipCreateFromHDC = dll.GdipCreateFromHDC
 """
 Creates a Graphics object that is associated with a specified device context.
 
@@ -110,7 +109,7 @@ class GdiplusStartupOutput(Structure):
 )
 
 
-GdipCreatePen1 = WINFUNCTYPE(None)(("GdipCreatePen1", dll))
+GdipCreatePen1 = dll.GdipCreatePen1
 """
 Creates a Pen object that has specified color, width, and style.
 
@@ -126,7 +125,7 @@ class GdiplusStartupOutput(Structure):
 )
... (残り 42 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\hid.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\hid.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\hid.py"
index 93c9ad2..30bfaf6 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\hid.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\hid.py"
@@ -5,33 +5,11 @@
 
 """Functions exported by hid.dll, and supporting data structures and enumerations."""
 
-from ctypes import (
-	WINFUNCTYPE,
-	POINTER,
-	Structure,
-	c_void_p,
-	sizeof,
-	windll,
-)
-from ctypes.wintypes import (
-	BOOLEAN,
-	HANDLE,
-	ULONG,
-	USHORT,
-	PCHAR,
-	PULONG,
-	PUSHORT,
-)
+from ctypes import POINTER, Structure, c_void_p, sizeof, windll
+from ctypes.wintypes import BOOLEAN, HANDLE, ULONG, USHORT
+
 from comtypes import GUID
-from hidpi import (
-	HIDP_CAPS,
-	NTSTATUS,
-	HIDP_REPORT_TYPE,
-	USAGE,
-	HIDP_DATA,
-	HIDP_VALUE_CAPS,
-	HIDP_BUTTON_CAPS,
-)
+from hidpi import HIDP_CAPS, NTSTATUS
 
 dll = windll.hid
 
@@ -57,7 +35,7 @@ def __init__(self, **kwargs):
 
 PHID_ATTRIBUTES = POINTER(HIDD_ATTRIBUTES)
 
-HidD_GetAttributes = WINFUNCTYPE(None)(("HidD_GetAttributes", dll))
+HidD_GetAttributes = dll.HidD_GetAttributes
 """
 The HidD_GetAttributes routine returns the attributes of a specified top-level collection.
... (残り 219 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\kernel32.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\kernel32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\kernel32.py"
index 64c7f7a..63cb580 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\kernel32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\kernel32.py"
@@ -222,6 +222,19 @@
 )
 OpenProcess.restype = HANDLE
 
+OpenThread = WINFUNCTYPE(None)(("OpenThread", dll))
+"""
+Opens an existing thread object.
+.. seealso::
+	https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openthread
+"""
+OpenThread.argtypes = (
+	DWORD,  # dwDesiredAccess
+	BOOL,  # bInheritHandle
+	DWORD,  # dwThreadId
+)
+OpenThread.restype = HANDLE
+
 VirtualAllocEx = WINFUNCTYPE(None)(("VirtualAllocEx", dll))
 """
 Allocates memory in the virtual address space of a specified process.
@@ -369,7 +382,6 @@
 )
 SetUnhandledExceptionFilter.restype = UnhandledExceptionFilter
 
-
 GetCurrentThreadId = WINFUNCTYPE(None)(("GetCurrentThreadId", dll))
 """
 Retrieves the thread identifier of the calling thread.
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\mshtml.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\mshtml.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\mshtml.py"
index 8870286..bf2d735 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\mshtml.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\mshtml.py"
@@ -6,7 +6,6 @@
 """Functions exported by mshtml.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	windll,
 	POINTER,
 )
@@ -23,7 +22,7 @@
 dll = windll.mshtml
 
 
-ShowHTMLDialogEx = WINFUNCTYPE(None)(("ShowHTMLDialogEx", dll))
+ShowHTMLDialogEx = dll.ShowHTMLDialogEx
 """
 Creates a modeless HTML dialog box.
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\ole32.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\ole32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\ole32.py"
index 5409dc9..0beb1fb 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\ole32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\ole32.py"
@@ -6,7 +6,6 @@
 """Functions exported by ole32.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	c_voidp,
 	POINTER,
 	windll,
@@ -31,7 +30,7 @@
 dll = windll.ole32
 
 
-CoTaskMemFree = WINFUNCTYPE(None)(("CoTaskMemFree", dll))
+CoTaskMemFree = dll.CoTaskMemFree
 """
 Frees a block of task memory previously allocated through a call to the CoTaskMemAlloc or CoTaskMemRealloc function.
 
@@ -43,7 +42,7 @@
 	LPVOID,  # pv: A pointer to the memory block to be freed.
 )
 
-CoCancelCall = WINFUNCTYPE(None)(("CoCancelCall", dll))
+CoCancelCall = dll.CoCancelCall
 """
 Requests that a call be canceled.
 
@@ -56,7 +55,7 @@
 	ULONG,  # ulTimeout: The number of milliseconds to wait for the call cancellation.
 )
 
-CoDisableCallCancellation = WINFUNCTYPE(None)(("CoDisableCallCancellation", dll))
+CoDisableCallCancellation = dll.CoDisableCallCancellation
 """
 Undoes the action of a call to CoEnableCallCancellation. Disables cancellation of synchronous calls on the calling thread when all calls to CoEnableCallCancellation are balanced by calls to CoDisableCallCancellation.
 
@@ -68,7 +67,7 @@
 	LPVOID,  # pReserved: This parameter is reserved and must be NULL.
 )
 
-CoEnableCallCancellation = WINFUNCTYPE(None)(("CoEnableCallCancellation", dll))
+CoEnableCallCancellation = dll.CoEnableCallCancellation
 """
 Enables cancellation of synchronous calls on the calling thread.
 
@@ -80,7 +79,7 @@
 	LPVOID,  # pReserved: This parameter is reserved and must be NULL.
... (残り 42 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\oleacc.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\oleacc.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\oleacc.py"
index 3259f54..38372ca 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\oleacc.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\oleacc.py"
@@ -6,7 +6,6 @@
 """Functions exported by oleacc.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	HRESULT,
 	windll,
 	POINTER,
@@ -30,7 +29,7 @@
 
 dll = windll.oleacc
 
-GetProcessHandleFromHwnd = WINFUNCTYPE(None)(("GetProcessHandleFromHwnd", dll))
+GetProcessHandleFromHwnd = dll.GetProcessHandleFromHwnd
 """
 Retrieves a process handle from a window handle.
 .. seealso::
@@ -41,7 +40,7 @@
 )
 GetProcessHandleFromHwnd.restype = HANDLE
 
-AccNotifyTouchInteraction = WINFUNCTYPE(None)(("AccNotifyTouchInteraction", dll))
+AccNotifyTouchInteraction = dll.AccNotifyTouchInteraction
 """
 Notifies the system that a touch interaction has occurred.
 .. seealso::
@@ -54,7 +53,7 @@
 )
 AccNotifyTouchInteraction.restype = HRESULT
 
-AccSetRunningUtilityState = WINFUNCTYPE(None)(("AccSetRunningUtilityState", dll))
+AccSetRunningUtilityState = dll.AccSetRunningUtilityState
 """
 Sets the running utility state for accessibility.
 .. seealso::
@@ -67,7 +66,7 @@
 )
 AccSetRunningUtilityState.restype = HRESULT
 
-AccessibleChildren = WINFUNCTYPE(None)(("AccessibleChildren", dll))
+AccessibleChildren = dll.AccessibleChildren
 """
 Retrieves the specified children of an accessible object.
 .. seealso::
@@ -82,7 +81,7 @@
 )
... (残り 88 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\oleaut32.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\oleaut32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\oleaut32.py"
index a596c52..7c5e352 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\oleaut32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\oleaut32.py"
@@ -6,7 +6,6 @@
 """Functions exported by oleaut32.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	windll,
 )
 from comtypes import BSTR
@@ -15,7 +14,7 @@
 dll = windll.oleaut32
 
 
-SysFreeString = WINFUNCTYPE(None)(("SysFreeString", dll))
+SysFreeString = dll.SysFreeString
 """
 Frees a string allocated previously by the SysAllocString, SysAllocStringLen, SysAlloc
 StringByteLen, or SysReAllocString functions.
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\rpcrt4.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\rpcrt4.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\rpcrt4.py"
index ea12165..af1a264 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\rpcrt4.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\rpcrt4.py"
@@ -6,7 +6,6 @@
 """Functions exported by rpcrt4.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	c_long,
 	c_ulong,
 	c_void_p,
@@ -21,7 +20,7 @@
 RPC_BINDING_HANDLE = c_void_p
 
 
-I_RpcBindingInqLocalClientPID = WINFUNCTYPE(None)(("I_RpcBindingInqLocalClientPID", dll))
+I_RpcBindingInqLocalClientPID = dll.I_RpcBindingInqLocalClientPID
 """
 Obtains the process identifier (PID) of the local client process that made the remote procedure call.
 
@@ -34,7 +33,7 @@
 	POINTER(c_long),  # ClientPID: Pointer to receive the client process ID
 )
 
-RpcBindingFree = WINFUNCTYPE(None)(("RpcBindingFree", dll))
+RpcBindingFree = dll.RpcBindingFree
 """
 Releases binding handle resources.
 
@@ -46,7 +45,7 @@
 	POINTER(RPC_BINDING_HANDLE),  # Binding: Pointer to the binding handle to free
 )
 
-RpcSsDestroyClientContext = WINFUNCTYPE(None)(("RpcSsDestroyClientContext", dll))
+RpcSsDestroyClientContext = dll.RpcSsDestroyClientContext
 """
 Destroys a client context handle and releases associated resources.
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\sas.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\sas.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\sas.py"
index e32406e..39c047c 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\sas.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\sas.py"
@@ -6,7 +6,6 @@
 """Functions exported by sas.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	windll,
 )
 from ctypes.wintypes import (
@@ -17,7 +16,7 @@
 dll = windll.sas
 
 
-SendSAS = WINFUNCTYPE(None)(("SendSAS", dll))
+SendSAS = dll.SendSAS
 """
 Simulates a secure attention sequence (SAS).
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\setupapi.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\setupapi.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\setupapi.py"
index 1ecb7c3..84d1d78 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\setupapi.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\setupapi.py"
@@ -5,16 +5,7 @@
 
 """Functions exported by setupapi.dll, and supporting data structures and enumerations."""
 
-from ctypes import (
-	WINFUNCTYPE,
-	POINTER,
-	Structure,
-	WinError,
-	c_void_p,
-	c_wchar_p,
-	sizeof,
-	windll,
-)
+from ctypes import POINTER, Structure, WinError, c_void_p, c_wchar_p, sizeof, windll
 from ctypes.wintypes import BOOL, DWORD, HKEY, HWND, PDWORD, PULONG, ULONG, WCHAR
 from enum import IntEnum
 
@@ -166,7 +157,7 @@ class _Dummy(Structure):
 PSP_DEVICE_INTERFACE_DETAIL_DATA = c_void_p
 
 
-SetupDiDestroyDeviceInfoList = WINFUNCTYPE(None)(("SetupDiDestroyDeviceInfoList", dll))
+SetupDiDestroyDeviceInfoList = dll.SetupDiDestroyDeviceInfoList
 """
 Deletes a device information set and frees all associated memory.
 
@@ -185,7 +176,7 @@ def _validHandle_errcheck(res, func, args):
 	return res
 
 
-SetupDiGetClassDevs = WINFUNCTYPE(None)(("SetupDiGetClassDevsW", dll))
+SetupDiGetClassDevs = dll.SetupDiGetClassDevsW
 """
 Returns a handle to a device information set that contains requested device information elements for a local computer.
 
@@ -201,7 +192,7 @@ def _validHandle_errcheck(res, func, args):
 SetupDiGetClassDevs.restype = HDEVINFO
 SetupDiGetClassDevs.errcheck = _validHandle_errcheck  # HDEVINFO
 
-SetupDiGetDeviceProperty = WINFUNCTYPE(None)(("SetupDiGetDevicePropertyW", dll))
+SetupDiGetDeviceProperty = dll.SetupDiGetDevicePropertyW
 """
 The SetupDiGetDeviceProperty function retrieves a device instance property.
 
@@ -220,7 +211,7 @@ def _validHandle_errcheck(res, func, args):
... (残り 43 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\shcore.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\shcore.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\shcore.py"
index 14daa06..ae7df18 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\shcore.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\shcore.py"
@@ -6,7 +6,6 @@
 """Functions exported by shcore.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	c_long,
 	windll,
 )
@@ -16,7 +15,7 @@
 dll = windll.shcore
 
 
-SetProcessDpiAwareness = WINFUNCTYPE(None)(("SetProcessDpiAwareness", dll))
+SetProcessDpiAwareness = dll.SetProcessDpiAwareness
 """
 Sets the current process to a specified dots per inch (DPI) awareness level. The DPI awareness levels are from the PROCESS_DPI_AWARENESS enumeration.
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\shell32.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\shell32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\shell32.py"
index 6d22b27..e30c65c 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\shell32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\shell32.py"
@@ -6,7 +6,6 @@
 """Functions exported by shell32.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	POINTER,
 	sizeof,
 	Structure,
@@ -39,7 +38,7 @@
 dll = windll.shell32
 
 
-IsUserAnAdmin = WINFUNCTYPE(None)(("IsUserAnAdmin", dll))
+IsUserAnAdmin = dll.IsUserAnAdmin
 """
 Tests whether the current user is a member of the Administrator's group.
 
@@ -49,7 +48,7 @@
 IsUserAnAdmin.restype = BOOL
 IsUserAnAdmin.argtypes = ()
 
-SHGetKnownFolderPath = WINFUNCTYPE(None)(("SHGetKnownFolderPath", dll))
+SHGetKnownFolderPath = dll.SHGetKnownFolderPath
 """
 Retrieves the full path of a known folder identified by the folder's KNOWNFOLDERID.
 
@@ -64,7 +63,7 @@
 	POINTER(c_wchar_p),  # ppszPath: Address of a pointer to a null-terminated Unicode string
 )
 
-ShellExecute = WINFUNCTYPE(None)(("ShellExecuteW", dll))
+ShellExecute = dll.ShellExecuteW
 """
 Performs an operation on a specified file.
 
@@ -114,7 +113,7 @@ def __init__(self, **kwargs):
 
 SHELLEXECUTEINFO = SHELLEXECUTEINFOW
 
-ShellExecuteEx = WINFUNCTYPE(None)(("ShellExecuteExW", dll))
+ShellExecuteEx = dll.ShellExecuteExW
 """
 Performs an operation on a specified file with extended options.
 
@@ -126,7 +125,7 @@ def __init__(self, **kwargs):
 	POINTER(SHELLEXECUTEINFOW),  # pExecInfo: Pointer to a SHELLEXECUTEINFO structure
... (残り 6 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\shlwapi.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\shlwapi.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\shlwapi.py"
index 378765c..b83e1b1 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\shlwapi.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\shlwapi.py"
@@ -6,7 +6,6 @@
 """Functions exported by shlwapi.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	c_uint,
 	c_void_p,
 	c_wchar_p,
@@ -20,7 +19,7 @@
 dll = windll.shlwapi
 
 
-SHLoadIndirectString = WINFUNCTYPE(None)(("SHLoadIndirectString", dll))
+SHLoadIndirectString = dll.SHLoadIndirectString
 """
 Extracts a specified text resource when given an indirect string.
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\uiAutomationCore.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\uiAutomationCore.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\uiAutomationCore.py"
index 444d12e..db16b1e 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\uiAutomationCore.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\uiAutomationCore.py"
@@ -5,10 +5,7 @@
 
 """Functions exported by UIAutomationCore.dll, and supporting data structures and enumerations."""
 
-from ctypes import (
-	WINFUNCTYPE,
-	windll,
-)
+from ctypes import windll
 from ctypes.wintypes import (
 	BOOL,
 	HWND,
@@ -19,7 +16,7 @@
 
 dll = windll.UIAutomationCore
 
-UiaHasServerSideProvider = WINFUNCTYPE(None)(("UiaHasServerSideProvider", dll))
+UiaHasServerSideProvider = dll.UiaHasServerSideProvider
 """
 Returns a Boolean value that indicates whether a window has a Microsoft UI Automation server-side provider.
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\urlmon.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\urlmon.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\urlmon.py"
index f53efd7..6caefa8 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\urlmon.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\urlmon.py"
@@ -6,7 +6,6 @@
 """Functions exported by urlmon.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	windll,
 	POINTER,
 )
@@ -21,7 +20,7 @@
 dll = windll.urlmon
 
 
-CreateURLMonikerEx = WINFUNCTYPE(None)(("CreateURLMonikerEx", dll))
+CreateURLMonikerEx = dll.CreateURLMonikerEx
 """
 Creates a URL moniker from a full or partial URL string.
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\user32.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\user32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\user32.py"
index 3fc6462..8771860 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\user32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\user32.py"
@@ -19,6 +19,7 @@
 	windll,
 	POINTER,
 )
+from enum import IntEnum, IntFlag
 from ctypes.wintypes import (
 	BOOL,
 	COLORREF,
@@ -57,7 +58,6 @@
 	WPARAM,
 	ATOM,
 )
-from enum import IntEnum, IntFlag
 
 UINT_PTR = c_size_t
 ULONG_PTR = c_size_t
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\version.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\version.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\version.py"
index 110f385..2263476 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\version.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\version.py"
@@ -6,7 +6,6 @@
 """Functions exported by version.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	POINTER,
 	windll,
 )
@@ -24,7 +23,7 @@
 dll = windll.version
 
 
-GetFileVersionInfoSize = WINFUNCTYPE(None)(("GetFileVersionInfoSizeW", dll))
+GetFileVersionInfoSize = dll.GetFileVersionInfoSizeW
 """
 Determines whether the operating system can retrieve version information for a specified file.
 
@@ -37,7 +36,7 @@
 	LPDWORD,  # lpdwHandle: Pointer to a variable that the function sets to zero (can be NULL)
 )
 
-GetFileVersionInfo = WINFUNCTYPE(None)(("GetFileVersionInfoW", dll))
+GetFileVersionInfo = dll.GetFileVersionInfoW
 """
 Retrieves version information for the specified file.
 
@@ -52,7 +51,7 @@
 	LPVOID,  # lpData: Pointer to a buffer that receives the file-version information
 )
 
-VerQueryValue = WINFUNCTYPE(None)(("VerQueryValueW", dll))
+VerQueryValue = dll.VerQueryValueW
 """
 Retrieves specified version information from the specified version-information resource.
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\winmm.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\winmm.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\winmm.py"
index f0d814f..9bcbf23 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\winmm.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\winmm.py"
@@ -6,7 +6,6 @@
 """Functions exported by winmm.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	c_size_t,
 	windll,
 	c_long,
@@ -24,7 +23,7 @@
 dll = windll.winmm
 
 
-waveOutGetNumDevs = WINFUNCTYPE(None)(("waveOutGetNumDevs", dll))
+waveOutGetNumDevs = dll.waveOutGetNumDevs
 """
 Retrieves the number of waveform-audio output devices present in the system.
 
@@ -34,7 +33,7 @@
 waveOutGetNumDevs.restype = UINT
 waveOutGetNumDevs.argtypes = ()
 
-waveOutMessage = WINFUNCTYPE(None)(("waveOutMessage", dll))
+waveOutMessage = dll.waveOutMessage
 """
 Sends a message to the given waveform-audio output device.
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winBindings\wtsapi32.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\wtsapi32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\wtsapi32.py"
index 8208a38..25fdd3a 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\wtsapi32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\wtsapi32.py"
@@ -6,7 +6,6 @@
 """Functions exported by wtsapi32.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	POINTER,
 	c_int,
 	c_void_p,
@@ -23,7 +22,7 @@
 dll = windll.wtsapi32
 
 
-WTSFreeMemory = WINFUNCTYPE(None)(("WTSFreeMemory", dll))
+WTSFreeMemory = dll.WTSFreeMemory
 """
 Frees memory allocated by a Windows Terminal Services function.
 
@@ -35,7 +34,7 @@
 	c_void_p,  # pMemory: Pointer to the memory to free
 )
 
-WTSQuerySessionInformation = WINFUNCTYPE(None)(("WTSQuerySessionInformationW", dll))
+WTSQuerySessionInformation = dll.WTSQuerySessionInformationW
 """
 Retrieves session information for the specified session on the specified Remote Desktop Session Host server.
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\wincon.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\wincon.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\wincon.py"
index 1f49bad..7ce1ab7 100644
--- "a/F:\\nvda\\gh\\beta\\source\\wincon.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\wincon.py"
@@ -6,13 +6,10 @@
 
 from ctypes import (
 	byref,
-	cast,
 	WinError,
-	create_unicode_buffer,
-	c_char,
-	c_void_p,
+	create_string_buffer,
+	c_int,
 )
-from ctypes.wintypes import DWORD
 import winBindings.kernel32
 from winBindings.kernel32 import (
 	COORD as _COORD,
@@ -69,14 +66,15 @@
 
 def GetConsoleSelectionInfo():
 	info = _CONSOLE_SELECTION_INFO()
-	if winBindings.kernel32.GetConsoleSelectionInfo(byref(info)) == 0:
-		raise WinError()
+	if winBindings.kernel32.GetConsoleSelectionInfo(byref(info)) == 0:  # noqa: F405
+		raise WinError()  # noqa: F405
 	return info
 
 
 def ReadConsoleOutputCharacter(handle, length, x, y):
-	buf = create_unicode_buffer(length)
-	numCharsRead = DWORD()
+	# Use a string buffer, as from an unicode buffer, we can't get the raw data.
+	buf = create_string_buffer(length * 2)  # noqa: F405
+	numCharsRead = c_int()  # noqa: F405
 	if (
 		winBindings.kernel32.ReadConsoleOutputCharacter(
 			handle,
@@ -84,16 +82,12 @@ def ReadConsoleOutputCharacter(handle, length, x, y):
 			length,
 			_COORD(x, y),
 			byref(numCharsRead),
-		)
+		)  # noqa: F405
 		== 0
-	):
-		raise WinError()
-	numRawBytes = numCharsRead.value * 2
... (残り 73 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\windowUtils.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\windowUtils.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\windowUtils.py"
index 59f5cd5..31f7e6e 100644
--- "a/F:\\nvda\\gh\\beta\\source\\windowUtils.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\windowUtils.py"
@@ -16,7 +16,7 @@
 import winBindings.user32
 import winBindings.gdi32
 import winUser
-from winBindings.user32 import WNDCLASSEXW, WNDPROC
+from winUser import WNDCLASSEXW, WNDPROC
 from logHandler import log
 from abc import abstractmethod
 from baseObject import AutoPropertyObject
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winKernel.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winKernel.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winKernel.py"
index c634743..e31eacf 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winKernel.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winKernel.py"
@@ -29,7 +29,6 @@
 import winBindings.kernel32
 from winBindings.kernel32 import (
 	FILETIME as _FILETIME,
-	PTIMERAPCROUTINE as _PTIMERAPCROUTINE,
 	SYSTEMTIME as _SYSTEMTIME,
 	TIME_ZONE_INFORMATION as _TIME_ZONE_INFORMATION,
 )
@@ -177,34 +176,30 @@ def createWaitableTimer(securityAttributes=None, manualReset=False, name=None):
 	return res
 
 
-def setWaitableTimer(
-	handle: int,
-	dueTime: int,
-	period: int = 0,
-	completionRoutine: _PTIMERAPCROUTINE | None = None,
-	arg: int | None = None,
-	resume: bool = False,
-):
+def setWaitableTimer(handle, dueTime, period=0, completionRoutine=None, arg=None, resume=False):
 	"""Wrapper to the kernel32 SETWaitableTimer function.
-
-	Consult https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-setwaitabletimer for Microsoft's documentation.
-
-	:param handle: A handle to the timer object.
-	:param dueTime: Relative time (in milliseconds).
+	Consult https://msdn.microsoft.com/en-us/library/windows/desktop/ms686289.aspx for Microsoft's documentation.
+	@param handle: A handle to the timer object.
+	@type handle: int
+	@param dueTime: Relative time (in miliseconds).
 		Note that the original function requires relative time to be supplied as a negative nanoseconds value.
-	:param period: Defaults to 0, timer is only executed once.
-		Value should be supplied in milliseconds.
-	:param completionRoutine: An optional function to be executed when the timer elapses.
-	:param arg: A pointer to a structure that is passed to the completion routine, defaults to ``None``. .
-	:param resume: Whether to restore a system in suspended power conservation mode when the timer state is set to signaled, defaults to ``False``.
-		If the system does not support a restore, the call succeeds, but ``GetLastError`` returns ``ERROR_NOT_SUPPORTED``.
+	@type dueTime: int
+	@param period: Defaults to 0, timer is only executed once.
+		Value should be supplied in miliseconds.
+	@type period: int
+	@param completionRoutine: The function to be executed when the timer elapses.
+	@type completionRoutine: L{PAPCFUNC}
+	@param arg: Defaults to C{None}; a pointer to a structure that is passed to the completion routine.
+	@type arg: L{ctypes.c_void_p}
... (残り 32 行)
```

#### 確認事項

- [ ] 本家版の変更内容を確認
- [ ] JP固有の機能に影響がないか確認
- [ ] ビルド・型チェック・テストを実行
- [ ] 問題なければ本家版の変更を適用

---

### ⚫ **要確認**: `source\winUser.py`

- **優先度**: 6
- **理由**: その他の変更（要確認）
- **追加行数**: 0
- **削除行数**: 0
- **変更タイプ**: unknown

#### 差分プレビュー

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winUser.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winUser.py"
index 17ae727..140bb7a 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winUser.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winUser.py"
@@ -275,7 +275,9 @@ class NMHdrStruct(Structure):
 VK_MENU = 18
 VK_PAUSE = 19
 VK_CAPITAL = 20
+VK_IME_ON = 0x16
 VK_FINAL = 0x18
+VK_IME_OFF = 0x1A
 VK_ESCAPE = 0x1B
 VK_CONVERT = 0x1C
 VK_NONCONVERT = 0x1D
@@ -554,8 +556,7 @@ def isDescendantWindow(parentHwnd, childHwnd):
 
 
 def getForegroundWindow() -> HWNDVal:
-	hwnd = _user32.GetForegroundWindow()
-	return hwnd or 0
+	return _user32.GetForegroundWindow()
 
 
 def setForegroundWindow(hwnd):
@@ -567,8 +568,7 @@ def setFocus(hwnd):
 
 
 def getDesktopWindow() -> HWNDVal:
-	hwnd = _user32.GetDesktopWindow()
-	return hwnd or 0
+	return _user32.GetDesktopWindow()
 
 
 def getControlID(hwnd):
@@ -619,9 +619,8 @@ def mouse_event(*args):
 	return _user32.mouse_event(*args)
 
 
-def getAncestor(hwnd: HWNDVal, flags: int) -> HWNDVal:
-	hwnd = _user32.GetAncestor(hwnd, flags)
-	return hwnd or 0
+def getAncestor(hwnd, flags):
+	return _user32.GetAncestor(hwnd, flags)
 
 
 def setCursorPos(x, y):
@@ -640,9 +639,8 @@ def getCaretPos():
 	return [point.x, point.y]
 
 
... (残り 35 行)
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
   - 本家版のファイルを確認: `F:\nvda\gh\beta\source\winUser.py`
   - 現在のファイルを確認: `source\source\winUser.py`
   - 差分を確認: projectDocs/jp/compare-with-beta/generated/source_source_winUser_py.md
   - 本家版の変更を適用
   - ビルド・型チェック・テストを実行
   - 問題なければコミット

## 参考

- 元の比較結果: `projectDocs/jp/compare-with-beta/summary.md`
- ファイル一覧: `projectDocs/jp/compare-with-beta/file-list.md`