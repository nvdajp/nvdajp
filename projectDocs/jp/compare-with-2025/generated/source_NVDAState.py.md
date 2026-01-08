# Diff for: `source\NVDAState.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\NVDAState.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAState.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAState.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAState.py"
index fd4b5c7..f08f227 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAState.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAState.py"
@@ -3,13 +3,19 @@
 # This file may be used under the terms of the GNU General Public License, version 2 or later.
 # For more details see: https://www.gnu.org/licenses/gpl-2.0.html
 
+from functools import lru_cache
 import os
+import platform
 import sys
+import sysconfig
 import time
 import winreg
 
+import buildVersion
 import globalVars
 
+from functools import cached_property
+
 
 class _WritePaths:
 	@property
@@ -61,6 +67,10 @@ def voiceDictsBackupDir(self) -> str:
 	def updatesDir(self) -> str:
 		return os.path.join(self.configDir, "updates")
 
+	@property
+	def modelsDir(self) -> str:
+		return os.path.join(self.configDir, "models")
+
 	@property
 	def nvdaConfigFile(self) -> str:
 		return os.path.join(self.configDir, "nvda.ini")
@@ -91,6 +101,97 @@ def updateCheckStateFile(self) -> str:
 	def guiStateFile(self) -> str:
 		return os.path.join(self.configDir, "guiState.ini")
 
+	@property
+	def defaultStartMenuFolder(self) -> str:
+		"""Name of a specific folder in the start menu, not a full path"""
+		return buildVersion.name
+
+	@property
+	@lru_cache(maxsize=1)
+	def startMenuFolder(self) -> str | None:
+		"""Name of a specific folder in the start menu, not a full path"""
+		from config.registry import RegistryKey
+
+		try:
+			with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value) as k:
+				return winreg.QueryValueEx(k, "Start Menu Folder")[0]
+		except WindowsError:
+			return None
+
+	@property
+	@lru_cache(maxsize=1)
+	def _startMenuFolderX86(self) -> str | None:
+		"""Name of a specific folder in the start menu, not a full path"""
+		from config.registry import RegistryKey
+
+		try:
+			with winreg.OpenKey(
+				winreg.HKEY_LOCAL_MACHINE,
+				RegistryKey.NVDA.value,
+				access=winreg.KEY_WOW64_32KEY,
+			) as k:
+				return winreg.QueryValueEx(k, "Start Menu Folder")[0]
+		except WindowsError:
+			return None
+
+	@property
+	@lru_cache(maxsize=1)
+	def defaultInstallDir(self) -> str:
+		from config.registry import RegistryKey
+
+		with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.CURRENT_VERSION.value) as k:
+			programFilesPath = winreg.QueryValueEx(k, "ProgramFilesDir")[0]
+		return os.path.join(programFilesPath, buildVersion.name)
+
+	@property
+	@lru_cache(maxsize=1)
+	def _defaultInstallDirX86(self) -> str:
+		from config.registry import RegistryKey, _RegistryKeyX86
+
+		if platform.architecture()[0].startswith("64"):
+			# We are a 64-bit process, so we want to get the 32-bit view of the registry.
+			# Using winreg.KEY_WOW64_32KEY in this case raises Access Denied on a non-elevated process.
+			key = _RegistryKeyX86.CURRENT_VERSION.value
+		else:
+			# We are a 32-bit process, so RegistryKey defaults to the 32-bit view of the registry.
+			key = RegistryKey.CURRENT_VERSION.value
+
+		with winreg.OpenKey(
+			winreg.HKEY_LOCAL_MACHINE,
+			key,
+		) as k:
+			programFilesPath = winreg.QueryValueEx(k, "ProgramFilesDir")[0]
+		return os.path.join(programFilesPath, buildVersion.name)
+
+	@property
+	@lru_cache(maxsize=1)
+	def installDir(self) -> str | None:
+		from config.registry import RegistryKey
+
+		try:
+			with winreg.OpenKey(
+				winreg.HKEY_LOCAL_MACHINE,
+				RegistryKey.INSTALLED_COPY.value,
+			) as k:
+				return winreg.QueryValueEx(k, "UninstallDirectory")[0]
+		except WindowsError:
+			return None
+
+	@property
+	@lru_cache(maxsize=1)
+	def _installDirX86(self) -> str | None:
+		from config.registry import RegistryKey
+
+		try:
+			with winreg.OpenKey(
+				winreg.HKEY_LOCAL_MACHINE,
+				RegistryKey.INSTALLED_COPY.value,
+				access=winreg.KEY_WOW64_32KEY,
+			) as k:
+				return winreg.QueryValueEx(k, "UninstallDirectory")[0]
+		except WindowsError:
+			return None
+
 	def getSymbolsConfigFile(self, locale: str) -> str:
 		return os.path.join(self.configDir, f"symbols-{locale}.dic")
 
@@ -98,7 +199,87 @@ def getProfileConfigFile(self, name: str) -> str:
 		return os.path.join(self.profilesDir, f"{name}.ini")
 
 
+class _ReadPaths:
+	@property
+	def versionedLibPath(self) -> str:
+		versionedLibPath = os.path.join(globalVars.appDir, "lib")
+		if not isRunningAsSource():
+			# When running as a py2exe build, libraries are in a version-specific directory
+			versionedLibPath = os.path.join(versionedLibPath, buildVersion.version)
+		return versionedLibPath
+
+	@property
+	def versionedLibX86Path(self) -> str:
+		return os.path.join(self.versionedLibPath, "x86")
+
+	@cached_property
+	def versionedLibAMD64Path(self) -> str:
+		import winVersion
+
+		arch = winVersion.getWinVer().processorArchitecture
+		return os.path.join(
+			self.versionedLibPath,
+			(
+				# On ARM64 Windows, we use arm64ec libraries for interop with x64 code.
+				"arm64ec" if arch == "ARM64" else "x64"
+			),
+		)
+
+	@property
+	def versionedLibARM64Path(self) -> str:
+		return os.path.join(self.versionedLibPath, "arm64")
+
+	@cached_property
+	def coreArchLibPath(self) -> str:
+		match sysconfig.get_platform():
+			case "win-amd64":
+				return self.versionedLibAMD64Path
+			case "win-arm64":
+				return self.versionedLibARM64Path
+			case "win32":
+				return self.versionedLibX86Path
+			case _:
+				raise RuntimeError("Unsupported platform")
+
+	@property
+	def nvdaHelperRemoteDll(self) -> str:
+		return os.path.join(self.coreArchLibPath, "nvdaHelperRemote.dll")
+
+	@property
+	def nvdaHelperLocalDll(self) -> str:
+		return os.path.join(self.coreArchLibPath, "nvdaHelperLocal.dll")
+
+	@property
+	def nvdaHelperLocalWin10Dll(self) -> str:
+		return os.path.join(self.coreArchLibPath, "nvdaHelperLocalWin10.dll")
+
+	@property
+	def mathCATDir(self) -> str:
+		"""
+		Base directory for MathCAT assets (rules etc.).
+		"""
+		if isRunningAsSource():
+			base = os.path.dirname(globalVars.appDir)
+		else:
+			base = globalVars.appDir
+		return os.path.join(
+			base,
+			"include",
+			"nvda-mathcat",
+			"assets",
+		)
+
+	@property
+	def UIARemoteDll(self) -> str:
+		return os.path.join(self.coreArchLibPath, "UIARemote.dll")
+
+	@property
+	def javaAccessBridgeDLL(self) -> str:
+		return os.path.join(globalVars.appDir, "windowsaccessbridge.dll")
+
+
 WritePaths = _WritePaths()
+ReadPaths = _ReadPaths()
 
 
 def isRunningAsSource() -> bool:
@@ -177,7 +358,7 @@ def _forceSecureModeEnabled() -> bool:
 	from config.registry import RegistryKey
 
 	try:
-		k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value)
+		with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value) as k:
 			return bool(winreg.QueryValueEx(k, RegistryKey.FORCE_SECURE_MODE_SUBKEY.value)[0])
 	except WindowsError:
 		# Expected state by default, forceSecureMode parameter not set
@@ -189,7 +370,7 @@ def _serviceDebugEnabled() -> bool:
 	from config.registry import RegistryKey
 
 	try:
-		k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value)
+		with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value) as k:
 			return bool(winreg.QueryValueEx(k, RegistryKey.SERVICE_DEBUG_SUBKEY.value)[0])
 	except WindowsError:
 		# Expected state by default, serviceDebug parameter not set
@@ -202,7 +383,7 @@ def _configInLocalAppDataEnabled() -> bool:
 	from logHandler import log
 
 	try:
-		k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value)
+		with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value) as k:
 			return bool(winreg.QueryValueEx(k, RegistryKey.CONFIG_IN_LOCAL_APPDATA_SUBKEY.value)[0])
 	except FileNotFoundError:
 		log.debug("Installed user config is not in local app data")

```