# Diff for: `source\installer.py`

**Source**: `F:\nvda\gh\beta\source\installer.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\installer.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\installer.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\installer.py"
index 44fa20c..a552ccc 100644
--- "a/F:\\nvda\\gh\\beta\\source\\installer.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\installer.py"
@@ -3,8 +3,6 @@
 # See the file COPYING for more details.
 # Copyright (C) 2011-2025 NV Access Limited, Joseph Lee, Babbage B.V., Łukasz Golonka, Cyrille Bougot
 
-from collections.abc import Iterable
-import comtypes.client
 import ctypes
 import pathlib
 import winreg
@@ -12,12 +10,13 @@
 import os
 import tempfile
 import shutil
+import itertools
 import winBindings.kernel32
 import shellapi
 import globalVars
 import languageHandler
 import config
-from config.registry import NVDA_ADDON_PROG_ID, RegistryKey, _deleteKeyAndSubkeys
+from config.registry import RegistryKey
 import versionInfo
 import buildVersion
 from logHandler import log
@@ -25,44 +24,42 @@
 import easeOfAccess
 import COMRegistrationFixes
 import winKernel
+import winBindings.kernel32
+from typing import (
+	Dict,
+	Iterable,
+	Union,
+)
 import NVDAState
 from NVDAState import WritePaths
 from utils.tempFile import _createEmptyTempFileForDeletingFile
-from utils._deprecate import handleDeprecations, MovedSymbol
 
 _wsh = None
 
-__getattr__ = handleDeprecations(
-	MovedSymbol(
-		"defaultStartMenuFolder",
-		"NVDAState",
-		"WritePaths",
-		"defaultStartMenuFolder",
-	),
-	MovedSymbol(
-		"defaultInstallPath",
-		"NVDAState",
-		"WritePaths",
-		"defaultInstallDir",
-	),
-)
-
 
 def _getWSH():
 	global _wsh
 	if not _wsh:
+		import comtypes.client
+
 		_wsh = comtypes.client.CreateObject("wScript.Shell", dynamic=True)
 	return _wsh
 
 
+defaultStartMenuFolder = buildVersion.name
+with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.CURRENT_VERSION.value) as k:
+	programFilesPath = winreg.QueryValueEx(k, "ProgramFilesDir")[0]
+defaultInstallPath = os.path.join(programFilesPath, buildVersion.name)
+
+
 def createShortcut(
-	path: str,
-	targetPath: str | None = None,
-	arguments: str | None = None,
-	iconLocation: str | None = None,
-	workingDirectory: str | None = None,
-	hotkey: str | None = None,
-	prependSpecialFolder: str | None = None,
+	path,
+	targetPath=None,
+	arguments=None,
+	iconLocation=None,
+	workingDirectory=None,
+	hotkey=None,
+	prependSpecialFolder=None,
 ):
 	# #7696: The shortcut is only physically saved to disk if it does not already exist, or one or more properties have changed.
 	wsh = _getWSH()
@@ -93,40 +90,42 @@ def createShortcut(
 		short.Save()
 
 
+def getStartMenuFolder(noDefault=False):
+	try:
+		with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value) as k:
+			return winreg.QueryValueEx(k, "Start Menu Folder")[0]
+	except WindowsError:
+		return defaultStartMenuFolder if not noDefault else None
+
+
+def getInstallPath(noDefault: bool = False) -> str | None:
+	try:
+		k = winreg.OpenKey(
+			winreg.HKEY_LOCAL_MACHINE,
+			RegistryKey.INSTALLED_COPY.value,
+		)
+		return winreg.QueryValueEx(k, "UninstallDirectory")[0]
+	except WindowsError:
+		return defaultInstallPath if not noDefault else None
+
+
 def comparePreviousInstall() -> int | None:
 	"""Returns 1 if the existing installation is newer than this running version,
 	0 if it is the same, -1 if it is older,
 	None if there is no existing installation.
 	"""
-	pathX86 = WritePaths._installDirX86
-	pathX86Exists = pathX86 and os.path.isdir(pathX86)
-	path = WritePaths.installDir
-	pathExists = path and os.path.isdir(path)
-	oldTime = None
-	if not (pathExists or pathX86Exists):
+	path = getInstallPath(True)
+	if not path or not os.path.isdir(path):
 		return None
-	if pathExists:
 	try:
 		oldTime = os.path.getmtime(os.path.join(path, "nvda_slave.exe"))
-		except OSError:
-			log.debug("Unable to get modification time of nvda_slave.exe in previous installation.")
-			return None
-	elif pathX86Exists:
-		try:
-			oldTime = os.path.getmtime(os.path.join(pathX86, "nvda_slave.exe"))
-		except OSError:
-			log.debug("Unable to get modification time of nvda_slave.exe in previous installation (x86).")
-			return None
-	try:
 		newTime = os.path.getmtime("nvda_slave.exe")
 	except OSError:
-		# This should never happen.
-		log.error("Unable to get modification time of nvda_slave.exe in current process.")
 		return None
 	return (oldTime > newTime) - (oldTime < newTime)
 
 
-def getDocFilePath(fileName: str, installDir: str):
+def getDocFilePath(fileName, installDir):
 	rootPath = os.path.join(installDir, "documentation")
 	lang = languageHandler.getLanguage()
 	tryLangs = [lang]
@@ -145,7 +144,7 @@ def getDocFilePath(fileName: str, installDir: str):
 			return tryPath
 
 
-def copyProgramFiles(destPath: str):
+def copyProgramFiles(destPath):
 	sourcePath = globalVars.appDir
 	detectUserConfig = True
 	for curSourceDir, subDirs, files in os.walk(sourcePath):
@@ -166,7 +165,7 @@ def copyProgramFiles(destPath: str):
 			tryCopyFile(sourceFilePath, destFilePath)
 
 
-def copyUserConfig(destPath: str):
+def copyUserConfig(destPath):
 	sourcePath = WritePaths.configDir
 	for curSourceDir, subDirs, files in os.walk(sourcePath):
 		curDestDir = os.path.join(destPath, os.path.relpath(curSourceDir, sourcePath))
@@ -178,11 +177,13 @@ def copyUserConfig(destPath: str):
 			tryCopyFile(sourceFilePath, destFilePath)
 
 
-def removeOldLibFiles(destPath: str, rebootOK: bool = False):
+def removeOldLibFiles(destPath, rebootOK=False):
 	"""
 	Removes library files from previous versions of NVDA.
-	:param destPath: The path where NVDA is installed.
-	:param rebootOK: If true then files can be removed on next reboot if trying to do so now fails.
+	@param destPath: The path where NVDA is installed.
+	@type destPath: string
+	@param rebootOK: If true then files can be removed on next reboot if trying to do so now fails.
+	@type rebootOK: boolean
 	"""
 	for topDir in ("lib", "lib64", "libArm64"):
 		currentLibPath = os.path.join(destPath, topDir, buildVersion.version)
@@ -217,7 +218,7 @@ def removeOldLibFiles(destPath: str, rebootOK: bool = False):
 					)
 
 
-def removeOldProgramFiles(destPath: str):
+def removeOldProgramFiles(destPath):
 	# #3181: Remove espeak-ng-data\voices except for variants.
 	# Otherwise, there will be duplicates if voices have been moved in this new eSpeak version.
 	root = os.path.join(destPath, "synthDrivers", "espeak-ng-data", "voices")
@@ -267,7 +268,7 @@ def removeOldProgramFiles(destPath: str):
 					log.warning(f"Couldn't remove file: {path!r}")
 
 
-def getUninstallerRegInfo(installDir: str) -> dict[str, str | int]:
+def getUninstallerRegInfo(installDir: str) -> Dict[str, Union[str, int]]:
 	"""
 	Constructs a dictionary that is written to the registry for NVDA to show up
 	in the Windows "Apps and Features" overview.
@@ -275,7 +276,7 @@ def getUninstallerRegInfo(installDir: str) -> dict[str, str | int]:
 	return dict(
 		DisplayName=f"{buildVersion.name} {buildVersion.version}",
 		DisplayVersion=buildVersion.version_detailed,
-		DisplayIcon=os.path.join(installDir, "images", "nvda.ico"),
+		DisplayIcon=os.path.join(installDir, "images", "nvdajp3.ico"),
 		# EstimatedSize is in KiB
 		EstimatedSize=getDirectorySize(installDir) // 1024,
 		InstallDir=installDir,
@@ -370,15 +371,15 @@ def registerInstallation(
 
 
 def _createShortcutWithFallback(
-	path: str,
-	targetPath: str | None = None,
-	arguments: str | None = None,
-	iconLocation: str | None = None,
-	workingDirectory: str | None = None,
-	hotkey: str | None = None,
-	prependSpecialFolder: str | None = None,
-	fallbackHotkey: str | None = None,
-	fallbackPath: str | None = None,
+	path,
+	targetPath=None,
+	arguments=None,
+	iconLocation=None,
+	workingDirectory=None,
+	hotkey=None,
+	prependSpecialFolder=None,
+	fallbackHotkey=None,
+	fallbackPath=None,
 ):
 	"""Sometimes translations are used (for `path` or `hotkey` arguments) which include unicode characters
 	which cause the createShortcut method to fail. In these cases, try again using the English string if it is
@@ -428,13 +429,7 @@ def _createShortcutWithFallback(
 			)
 
 
-def _updateShortcuts(
-	NVDAExe: str,
-	installDir: str,
-	shouldCreateDesktopShortcut: bool,
-	slaveExe: str,
-	startMenuFolder: str,
-) -> None:
+def _updateShortcuts(NVDAExe, installDir, shouldCreateDesktopShortcut, slaveExe, startMenuFolder) -> None:
 	if shouldCreateDesktopShortcut:
 		# Translators: The shortcut key used to start NVDA.
 		# This should normally be left as is, but might be changed for some locales
@@ -472,6 +467,17 @@ def _updateShortcuts(
 		prependSpecialFolder="AllUsersPrograms",
 	)
 
+	# nvdajp begin
+	# Translators: A label for a shortcut in start menu and a menu entry in NVDA menu (to go to NVDAJP website).
+	jpWebSiteTranslated = _("NVDAJP web site")
+	_createShortcutWithFallback(
+		path=os.path.join(startMenuFolder, jpWebSiteTranslated + ".lnk"),
+		fallbackPath=os.path.join(startMenuFolder, "NVDAJP web site.lnk"),
+		targetPath="https://www.nvda.jp/",
+		prependSpecialFolder="AllUsersPrograms",
+	)
+	# nvdajp end
+
 	# Translators: A label for a shortcut item in start menu to uninstall NVDA from the computer.
 	uninstallTranslated = _("Uninstall NVDA")
 	_createShortcutWithFallback(
@@ -522,6 +528,16 @@ def _updateShortcuts(
 		targetPath=getDocFilePath("changes.html", installDir),
 		prependSpecialFolder="AllUsersPrograms",
 	)
+	# nvdajp begin
+	# Translators: A label for a shortcut in start menu to open NVDAJP readme
+	readmeJpTranslated = _("&Readme (nvdajp)")
+	_createShortcutWithFallback(
+		path=os.path.join(docFolder, readmeJpTranslated + ".lnk"),
+		fallbackPath=os.path.join(docFolder, "Readme (nvdajp).lnk"),
+		targetPath=getDocFilePath("readmejp.html", installDir),
+		prependSpecialFolder="AllUsersPrograms",
+	)
+	# nvdajp end
 
 
 def isDesktopShortcutInstalled():
@@ -531,23 +547,16 @@ def isDesktopShortcutInstalled():
 	return os.path.isfile(shortcutPath)
 
 
-def _unregisterEaseOfAccessApp():
+def unregisterInstallation(keepDesktopShortcut: bool = False) -> None:
 	try:
 		winreg.DeleteKeyEx(
 			winreg.HKEY_LOCAL_MACHINE,
 			RegistryKey.EASE_OF_ACCESS_APP.value,
-			# TODO: remove when NVDA is 64-bit only.
-			access=winreg.KEY_WOW64_64KEY,
+			winreg.KEY_WOW64_64KEY,
 		)
-	except WindowsError:
-		log.debug("Ease of Access app key not found. Nothing to unregister.")
-	try:
 		easeOfAccess.setAutoStart(easeOfAccess.AutoStartContext.ON_LOGON_SCREEN, False)
 	except WindowsError:
-		log.debug("Could not disable auto start on logon screen.")
-
-
-def _unregisterDesktopShortcut(keepDesktopShortcut: bool):
+		pass
 	wsh = _getWSH()
 	desktopPath = os.path.join(wsh.SpecialFolders("AllUsersDesktop"), "NVDA.lnk")
 	if not keepDesktopShortcut and os.path.isfile(desktopPath):
@@ -555,104 +564,39 @@ def _unregisterDesktopShortcut(keepDesktopShortcut: bool):
 			os.remove(desktopPath)
 		except WindowsError:
 			pass
-
-
-def _unregisterFromStartMenu() -> None:
-	wsh = _getWSH()
+	startMenuFolder = getStartMenuFolder()
+	if startMenuFolder:
 		programsPath = wsh.SpecialFolders("AllUsersPrograms")
-	startMenuFolder = WritePaths.startMenuFolder
-	if startMenuFolder is None:
-		startMenuFolder = WritePaths.defaultStartMenuFolder
 		startMenuPath = os.path.join(programsPath, startMenuFolder)
 		if os.path.isdir(startMenuPath):
 			shutil.rmtree(startMenuPath, ignore_errors=True)
-		log.debug(f"Removed start menu folder: {startMenuPath}")
-	# Also remove the x86 start menu folder if it is different.
-	startMenuFolderX86 = WritePaths._startMenuFolderX86
-	if startMenuFolderX86 is None:
-		startMenuFolderX86 = WritePaths.defaultStartMenuFolder
-	startMenuPathX86 = os.path.join(programsPath, startMenuFolderX86)
-	if os.path.isdir(startMenuPathX86):
-		shutil.rmtree(startMenuPathX86, ignore_errors=True)
-		log.debug(f"Removed start menu (x86) folder: {startMenuPathX86}")
-
-
-def _unregisterFromUninstallRegistry() -> None:
 	try:
-		winreg.DeleteKeyEx(
+		winreg.DeleteKey(
 			winreg.HKEY_LOCAL_MACHINE,
 			RegistryKey.INSTALLED_COPY.value,
-			# TODO: remove when NVDA is 64-bit only.
-			access=winreg.KEY_WOW64_64KEY,
 		)
 	except WindowsError:
-		log.debug("Uninstall registry key not found for 64-bit, nothing to unregister.")
-	try:
-		winreg.DeleteKeyEx(
-			winreg.HKEY_LOCAL_MACHINE,
-			RegistryKey.INSTALLED_COPY.value,
-			access=winreg.KEY_WOW64_32KEY,
-		)
-	except WindowsError:
-		log.debug("Uninstall registry key not found for 32-bit, nothing to unregister.")
-
-
-def _unregisterFromAppPathRegistry() -> None:
-	try:
-		winreg.DeleteKeyEx(
-			winreg.HKEY_LOCAL_MACHINE,
-			RegistryKey.APP_PATH.value,
-			# TODO: remove when NVDA is 64-bit only.
-			access=winreg.KEY_WOW64_64KEY,
-		)
-	except WindowsError:
-		log.debug("App path registry key not found for 64-bit, nothing to unregister.")
+		pass
 	try:
-		winreg.DeleteKeyEx(
+		winreg.DeleteKey(
 			winreg.HKEY_LOCAL_MACHINE,
 			RegistryKey.APP_PATH.value,
-			access=winreg.KEY_WOW64_32KEY,
 		)
 	except WindowsError:
-		log.debug("App path registry key not found for 32-bit, nothing to unregister.")
-
-
-def _unregisterFromSoftwareRegistry() -> None:
-	try:
-		winreg.DeleteKeyEx(
-			winreg.HKEY_LOCAL_MACHINE,
-			RegistryKey.NVDA.value,
-			# TODO: remove when NVDA is 64-bit only.
-			access=winreg.KEY_WOW64_64KEY,
-		)
-	except WindowsError:
-		log.debug("NVDA registry key not found for 64-bit, nothing to unregister.")
+		pass
 	try:
-		winreg.DeleteKeyEx(
-			winreg.HKEY_LOCAL_MACHINE,
-			RegistryKey.NVDA.value,
-			access=winreg.KEY_WOW64_32KEY,
-		)
+		winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.NVDA.value)
 	except WindowsError:
-		log.debug("NVDA registry key not found for 32-bit, nothing to unregister.")
-
-
-def unregisterInstallation(keepDesktopShortcut: bool = False) -> None:
-	_unregisterEaseOfAccessApp()
-	_unregisterDesktopShortcut(keepDesktopShortcut)
-	_unregisterFromStartMenu()
-	_unregisterFromUninstallRegistry()
-	_unregisterFromAppPathRegistry()
-	_unregisterFromSoftwareRegistry()
+		pass
 	unregisterAddonFileAssociation()
 
 
-def registerAddonFileAssociation(slaveExe: str):
+def registerAddonFileAssociation(slaveExe):
 	try:
 		# Create progID for NVDA ad-ons
 		with winreg.CreateKeyEx(
 			winreg.HKEY_LOCAL_MACHINE,
-			RegistryKey.ADDON_PROG.value,
+			"SOFTWARE\\Classes\\%s" % addonHandler.NVDA_ADDON_PROG_ID,
 			0,
 			winreg.KEY_WRITE,
 		) as k:
@@ -667,21 +611,21 @@ def registerAddonFileAssociation(slaveExe: str):
 					None,
 					0,
 					winreg.REG_SZ,
-					f'"{slaveExe}" addons_installAddonPackage "%1"',
+					'"{slaveExe}" addons_installAddonPackage "%1"'.format(slaveExe=slaveExe),
 				)
 		# Now associate addon extension to the created prog id.
 		with winreg.CreateKeyEx(
 			winreg.HKEY_LOCAL_MACHINE,
-			RegistryKey.ADDON_EXT.value,
+			"SOFTWARE\\Classes\\.%s" % addonHandler.BUNDLE_EXTENSION,
 			0,
 			winreg.KEY_WRITE,
 		) as k:
-			winreg.SetValueEx(k, None, 0, winreg.REG_SZ, NVDA_ADDON_PROG_ID)
+			winreg.SetValueEx(k, None, 0, winreg.REG_SZ, addonHandler.NVDA_ADDON_PROG_ID)
 			winreg.SetValueEx(k, "Content Type", 0, winreg.REG_SZ, addonHandler.BUNDLE_MIMETYPE)
 			# Add NVDA to the "open With" list
 			k2 = winreg.CreateKeyEx(
 				k,
-				os.path.join("OpenWithProgids", NVDA_ADDON_PROG_ID),
+				"OpenWithProgids\\%s" % addonHandler.NVDA_ADDON_PROG_ID,
 				0,
 				winreg.KEY_WRITE,
 			)
@@ -692,35 +636,36 @@ def registerAddonFileAssociation(slaveExe: str):
 		log.error("Can not create addon file association.", exc_info=True)
 
 
-def unregisterAddonFileAssociation() -> None:
-	shouldNotifyShell = False
+def unregisterAddonFileAssociation():
 	try:
 		# As per MSDN recomendation, we only need to remove the prog ID.
 		_deleteKeyAndSubkeys(
 			winreg.HKEY_LOCAL_MACHINE,
-			RegistryKey.ADDON_PROG.value,
-			# TODO: remove when NVDA is 64-bit only.
-			access=winreg.KEY_WOW64_64KEY,
-		)
-	except WindowsError:
-		log.debug("Addon prog ID registry key not found for 64-bit, nothing to unregister.")
-	else:
-		shouldNotifyShell = True
-	try:
-		_deleteKeyAndSubkeys(
-			winreg.HKEY_LOCAL_MACHINE,
-			RegistryKey.ADDON_PROG.value,
-			access=winreg.KEY_WOW64_32KEY,
+			"Software\\Classes\\%s" % addonHandler.NVDA_ADDON_PROG_ID,
 		)
 	except WindowsError:
-		log.debug("Addon prog ID registry key not found for 32-bit, nothing to unregister.")
-	else:
-		shouldNotifyShell = True
-	if shouldNotifyShell:
+		# This is probably the first install, so just ignore the error.
+		return
 	# Notify the shell that a file association has changed:
 	shellapi.SHChangeNotify(shellapi.SHCNE_ASSOCCHANGED, shellapi.SHCNF_IDLIST, None, None)
 
 
+# Windows API call regDeleteTree is only available on vist and above so rule our own.
+def _deleteKeyAndSubkeys(key, subkey):
+	with winreg.OpenKey(key, subkey, access=winreg.KEY_WRITE | winreg.KEY_READ) as k:
+		# Recursively delete subkeys (Depth first search order)
+		# So Pythonic... </rant>
+		for i in itertools.count():
+			try:
+				subkeyName = winreg.EnumKey(k, i)
+			except WindowsError:
+				break
+			# Recursive call.
+			_deleteKeyAndSubkeys(k, subkeyName)
+		# Delete this key
+		winreg.DeleteKey(k, "")
+
+
 class RetriableFailure(Exception):
 	pass
 
@@ -766,7 +711,7 @@ def tryRemoveFile(
 	raise RetriableFailure("File %s could not be removed" % path)
 
 
-def tryCopyFile(sourceFilePath: str, destFilePath: str):
+def tryCopyFile(sourceFilePath, destFilePath):
 	if not sourceFilePath.startswith("\\\\"):
 		sourceFilePath = "\\\\?\\" + sourceFilePath
 	if not destFilePath.startswith("\\\\"):
@@ -794,7 +739,6 @@ def tryCopyFile(sourceFilePath: str, destFilePath: str):
 	"nvda.exe",
 	"nvda_noUIAccess.exe",
 	"nvda_uiAccess.exe",
-	"nvda_dmp.exe",
 	"nvda_slave.exe",
 }
 
@@ -864,14 +808,10 @@ def _deleteFileGroupOrFail(
 			log.debugWarning(f"Failed to remove temp directory {tempDir}", exc_info=True)
 
 
-def install(shouldCreateDesktopShortcut: bool = True, shouldRunAtLogon: bool = True) -> None:
-	prevInstallPath = WritePaths.installDir
-	installDir = WritePaths.defaultInstallDir
-	installDirX86 = WritePaths._installDirX86 or WritePaths._defaultInstallDirX86
-	startMenuFolder = WritePaths.defaultStartMenuFolder
-	shouldCleanX86 = (
-		installDirX86 is not None and os.path.isdir(installDirX86) and installDirX86 != installDir
-	)
+def install(shouldCreateDesktopShortcut: bool = True, shouldRunAtLogon: bool = True):
+	prevInstallPath = getInstallPath(noDefault=True)
+	installDir = defaultInstallPath
+	startMenuFolder = defaultStartMenuFolder
 	# Give some time for the installed NVDA (which may have been running on a secure screen)
 	# to shut down before we start deleting files.
 	time.sleep(1)
@@ -891,19 +831,10 @@ def install(shouldCreateDesktopShortcut: bool = True, shouldRunAtLogon: bool = T
 		numTries=6,
 		retryWaitInterval=0.5,
 	)
-	if shouldCleanX86:
-		_deleteFileGroupOrFail(
-			installDirX86,
-			_nvdaExes.union({"nvda_service.exe", "nvda_eoaProxy.exe"}),
-			numTries=6,
-			retryWaitInterval=0.5,
-		)
 	unregisterInstallation(keepDesktopShortcut=shouldCreateDesktopShortcut)
 	if prevInstallPath:
 		removeOldLoggedFiles(prevInstallPath)
 	removeOldProgramFiles(installDir)
-	if shouldCleanX86:
-		removeOldProgramFiles(installDirX86)
 	copyProgramFiles(installDir)
 	for f in ("nvda_UIAccess.exe", "nvda_noUIAccess.exe"):
 		f = os.path.join(installDir, f)
@@ -913,8 +844,6 @@ def install(shouldCreateDesktopShortcut: bool = True, shouldRunAtLogon: bool = T
 	else:
 		raise RuntimeError("No available executable to use as nvda.exe")
 	removeOldLibFiles(installDir, rebootOK=True)
-	if shouldCleanX86:
-		removeOldLibFiles(installDirX86, rebootOK=True)
 	registerInstallation(
 		installDir,
 		startMenuFolder,
@@ -922,15 +851,10 @@ def install(shouldCreateDesktopShortcut: bool = True, shouldRunAtLogon: bool = T
 		shouldRunAtLogon,
 		NVDAState._configInLocalAppDataEnabled(),
 	)
-	if shouldCleanX86:
-		oldSystemConfigPath = os.path.join(installDirX86, "systemConfig")
-		if os.path.isdir(oldSystemConfigPath):
-			config._setSystemConfig(oldSystemConfigPath, prefix=installDir)
-		tryRemoveFile(installDirX86, rebootOK=True)
 	COMRegistrationFixes.fixCOMRegistrations()
 
 
-def removeOldLoggedFiles(installPath: str):
+def removeOldLoggedFiles(installPath):
 	datPath = os.path.join(installPath, "uninstall.dat")
 	lines = []
 	if os.path.isfile(datPath):
@@ -946,7 +870,7 @@ def removeOldLoggedFiles(installPath: str):
 			tryRemoveFile(filePath, rebootOK=True)
 
 
-def createPortableCopy(destPath: str, shouldCopyUserConfig: bool = True):
+def createPortableCopy(destPath, shouldCopyUserConfig=True):
 	assert os.path.isabs(destPath), f"Destination path {destPath} is not absolute"
 	# Remove all the main executables always
 	_deleteFileGroupOrFail(destPath, {"nvda.exe", "nvda_noUIAccess.exe", "nvda_UIAccess.exe"})
@@ -958,7 +882,7 @@ def createPortableCopy(destPath: str, shouldCopyUserConfig: bool = True):
 	removeOldLibFiles(destPath, rebootOK=True)
 
 
-def registerEaseOfAccess(installDir: str):
+def registerEaseOfAccess(installDir):
 	with winreg.CreateKeyEx(
 		winreg.HKEY_LOCAL_MACHINE,
 		RegistryKey.EASE_OF_ACCESS_APP.value,

```