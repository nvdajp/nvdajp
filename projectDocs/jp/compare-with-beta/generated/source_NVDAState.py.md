# Diff for: `source\NVDAState.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\NVDAState.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAState.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

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
-		from config.registry import RegistryKey
-
-		try:
-			with winreg.OpenKey(
-				winreg.HKEY_LOCAL_MACHINE,
-				RegistryKey.NVDA.value,
-				access=winreg.KEY_WOW64_32KEY,
-			) as k:
-				return winreg.QueryValueEx(k, "Start Menu Folder")[0]
-		except WindowsError:
-			return None
-
-	@property
-	@lru_cache(maxsize=1)
-	def defaultInstallDir(self) -> str:
-		from config.registry import RegistryKey
-
-		with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.CURRENT_VERSION.value) as k:
-			programFilesPath = winreg.QueryValueEx(k, "ProgramFilesDir")[0]
-		return os.path.join(programFilesPath, buildVersion.name)
-
-	@property
-	@lru_cache(maxsize=1)
-	def _defaultInstallDirX86(self) -> str:
-		from config.registry import RegistryKey, _RegistryKeyX86
-
-		if platform.architecture()[0].startswith("64"):
-			# We are a 64-bit process, so we want to get the 32-bit view of the registry.
-			# Using winreg.KEY_WOW64_32KEY in this case raises Access Denied on a non-elevated process.
-			key = _RegistryKeyX86.CURRENT_VERSION.value
-		else:
-			# We are a 32-bit process, so RegistryKey defaults to the 32-bit view of the registry.
-			key = RegistryKey.CURRENT_VERSION.value
-
-		with winreg.OpenKey(
-			winreg.HKEY_LOCAL_MACHINE,
-			key,
-		) as k:
-			programFilesPath = winreg.QueryValueEx(k, "ProgramFilesDir")[0]
-		return os.path.join(programFilesPath, buildVersion.name)
-
-	@property
-	@lru_cache(maxsize=1)
-	def installDir(self) -> str | None:
-		from config.registry import RegistryKey
-
-		try:
-			with winreg.OpenKey(
-				winreg.HKEY_LOCAL_MACHINE,
-				RegistryKey.INSTALLED_COPY.value,
-			) as k:
-				return winreg.QueryValueEx(k, "UninstallDirectory")[0]
-		except WindowsError:
-			return None
-
-	@property
-	@lru_cache(maxsize=1)
-	def _installDirX86(self) -> str | None:
-		from config.registry import RegistryKey
-
-		try:
-			with winreg.OpenKey(
-				winreg.HKEY_LOCAL_MACHINE,
-				RegistryKey.INSTALLED_COPY.value,
-				access=winreg.KEY_WOW64_32KEY,
-			) as k:
-				return winreg.QueryValueEx(k, "UninstallDirectory")[0]
-		except WindowsError:
-			return None
-
 	def getSymbolsConfigFile(self, locale: str) -> str:
 		return os.path.join(self.configDir, f"symbols-{locale}.dic")
 
@@ -358,7 +261,7 @@ def _forceSecureModeEnabled() -> bool:
 	from config.registry import RegistryKey
 
 	try:
-		with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value) as k:
+		k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value)
 		return bool(winreg.QueryValueEx(k, RegistryKey.FORCE_SECURE_MODE_SUBKEY.value)[0])
 	except WindowsError:
 		# Expected state by default, forceSecureMode parameter not set
@@ -370,7 +273,7 @@ def _serviceDebugEnabled() -> bool:
 	from config.registry import RegistryKey
 
 	try:
-		with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value) as k:
+		k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value)
 		return bool(winreg.QueryValueEx(k, RegistryKey.SERVICE_DEBUG_SUBKEY.value)[0])
 	except WindowsError:
 		# Expected state by default, serviceDebug parameter not set
@@ -383,7 +286,7 @@ def _configInLocalAppDataEnabled() -> bool:
 	from logHandler import log
 
 	try:
-		with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value) as k:
+		k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value)
 		return bool(winreg.QueryValueEx(k, RegistryKey.CONFIG_IN_LOCAL_APPDATA_SUBKEY.value)[0])
 	except FileNotFoundError:
 		log.debug("Installed user config is not in local app data")

```