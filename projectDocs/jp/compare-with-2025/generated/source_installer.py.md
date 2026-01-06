# Diff for: `source\installer.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\installer.py`  
**Current**: `F:\nvda\gh\alphajp\source\installer.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\installer.py" "b/F:\\nvda\\gh\\alphajp\\source\\installer.py"
index 2ed16054dc..f2f2b72869 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\installer.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\installer.py"
@@ -17,11 +17,13 @@
 import config
 from config.registry import RegistryKey
 import versionInfo
+import buildVersion
 from logHandler import log
 import addonHandler
 import easeOfAccess
 import COMRegistrationFixes
 import winKernel
+import winBindings.kernel32
 from typing import (
 	Dict,
 	Iterable,
@@ -43,10 +45,10 @@ def _getWSH():
 	return _wsh
 
 
-defaultStartMenuFolder = versionInfo.name
+defaultStartMenuFolder = buildVersion.name
 with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKey.CURRENT_VERSION.value) as k:
 	programFilesPath = winreg.QueryValueEx(k, "ProgramFilesDir")[0]
-defaultInstallPath = os.path.join(programFilesPath, versionInfo.name)
+defaultInstallPath = os.path.join(programFilesPath, buildVersion.name)
 
 
 def createShortcut(
@@ -183,7 +185,7 @@ def removeOldLibFiles(destPath, rebootOK=False):
 	@type rebootOK: boolean
 	"""
 	for topDir in ("lib", "lib64", "libArm64"):
-		currentLibPath = os.path.join(destPath, topDir, versionInfo.version)
+		currentLibPath = os.path.join(destPath, topDir, buildVersion.version)
 		for parent, subdirs, files in os.walk(os.path.join(destPath, topDir), topdown=False):
 			if os.path.commonpath(
 				[os.path.abspath(parent), os.path.abspath(currentLibPath)],
@@ -271,16 +273,16 @@ def getUninstallerRegInfo(installDir: str) -> Dict[str, Union[str, int]]:
 	in the Windows "Apps and Features" overview.
 	"""
 	return dict(
-		DisplayName=f"{versionInfo.name} {versionInfo.version}",
-		DisplayVersion=versionInfo.version_detailed,
+		DisplayName=f"{buildVersion.name} {buildVersion.version}",
+		DisplayVersion=buildVersion.version_detailed,
 		DisplayIcon=os.path.join(installDir, "images", "nvdajp3.ico"),
 		# EstimatedSize is in KiB
 		EstimatedSize=getDirectorySize(installDir) // 1024,
 		InstallDir=installDir,
-		Publisher=versionInfo.publisher,
+		Publisher=buildVersion.publisher,
 		UninstallDirectory=installDir,
 		UninstallString=os.path.join(installDir, "uninstall.exe"),
-		URLInfoAbout=versionInfo.url,
+		URLInfoAbout=buildVersion.url,
 	)
 
 
@@ -460,7 +462,7 @@ def _updateShortcuts(NVDAExe, installDir, shouldCreateDesktopShortcut, slaveExe,
 	_createShortcutWithFallback(
 		path=os.path.join(startMenuFolder, webSiteTranslated + ".lnk"),
 		fallbackPath=os.path.join(startMenuFolder, "NVDA web site.lnk"),
-		targetPath=versionInfo.url,
+		targetPath=buildVersion.url,
 		prependSpecialFolder="AllUsersPrograms",
 	)
 
@@ -713,7 +715,7 @@ def tryCopyFile(sourceFilePath, destFilePath):
 		sourceFilePath = "\\\\?\\" + sourceFilePath
 	if not destFilePath.startswith("\\\\"):
 		destFilePath = "\\\\?\\" + destFilePath
-	if ctypes.windll.kernel32.CopyFileW(sourceFilePath, destFilePath, False) == 0:
+	if winBindings.kernel32.CopyFile(sourceFilePath, destFilePath, False) == 0:
 		errorCode = ctypes.GetLastError()
 		log.debugWarning("Unable to copy %s, error %d" % (sourceFilePath, errorCode))
 		if not os.path.exists(destFilePath):
@@ -725,7 +727,7 @@ def tryCopyFile(sourceFilePath, destFilePath):
 			log.error("Failed to rename %s after failed overwrite" % destFilePath, exc_info=True)
 			raise RetriableFailure("Failed to rename %s after failed overwrite" % destFilePath)
 		winKernel.moveFileEx(tempPath, None, winKernel.MOVEFILE_DELAY_UNTIL_REBOOT)
-		if ctypes.windll.kernel32.CopyFileW(sourceFilePath, destFilePath, False) == 0:
+		if winBindings.kernel32.CopyFile(sourceFilePath, destFilePath, False) == 0:
 			errorCode = ctypes.GetLastError()
 			raise OSError(
 				"Unable to copy file %s to %s, error %d" % (sourceFilePath, destFilePath, errorCode),
@@ -736,6 +738,7 @@ def tryCopyFile(sourceFilePath, destFilePath):
 	"nvda.exe",
 	"nvda_noUIAccess.exe",
 	"nvda_uiAccess.exe",
+	"nvda_dmp.exe",
 	"nvda_slave.exe",
 }
 
@@ -891,7 +894,7 @@ def registerEaseOfAccess(installDir):
 			"ApplicationName",
 			None,
 			winreg.REG_SZ,
-			versionInfo.name,
+			buildVersion.name,
 		)
 		winreg.SetValueEx(
 			appKey,

```