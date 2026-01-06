# Diff for: `source\config\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\config\__init__.py`  
**Current**: `F:\nvda\gh\alphajp\source\config\__init__.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\config\\__init__.py" "b/F:\\nvda\\gh\\alphajp\\source\\config\\__init__.py"
index 8e674888d4..2eadd6b186 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\config\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\config\\__init__.py"
@@ -13,7 +13,6 @@
 from enum import Enum
 import globalVars
 import winreg
-import ctypes
 import os
 import sys
 import errno
@@ -26,6 +25,7 @@
 from logHandler import log
 import logging
 from logging import DEBUG
+import winBindings.shell32
 from shlobj import FolderId, SHGetKnownFolderPath
 import baseObject
 import easeOfAccess
@@ -269,59 +269,9 @@ def getStartAfterLogon() -> bool:
 	"""Not to be confused with getStartOnLogonScreen.
 
 	Checks if NVDA is set to start after a logon.
-	Checks related easeOfAccess current user registry keys on Windows 8 or newer.
-	Then, checks the registry run key to see if NVDA
-	has been registered to start after logon on Windows 7
-	or by earlier NVDA versions.
+	Checks related easeOfAccess current user registry keys.
 	"""
-	if easeOfAccess.willAutoStart(easeOfAccess.AutoStartContext.AFTER_LOGON):
-		return True
-	try:
-		k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, _RegistryKey.RUN.value)
-	except FileNotFoundError:
-		log.debugWarning(
-			f"Unable to find run registry key {_RegistryKey.RUN}",
-			exc_info=True,
-		)
-		return False
-	except WindowsError:
-		log.error(
-			f"Unable to open run registry key {_RegistryKey.RUN}",
-			exc_info=True,
-		)
-		return False
-
-	try:
-		val = winreg.QueryValueEx(k, "nvda")[0]
-	except FileNotFoundError:
-		log.debug("NVDA is not set to start after logon")
-		return False
-	except WindowsError:
-		log.error("Failed to query NVDA key to set start after logon", exc_info=True)
-		return False
-
-	try:
-		startAfterLogonPath = os.stat(val)
-	except WindowsError:
-		log.error(
-			"Failed to access the start after logon directory.",
-			exc_info=True,
-		)
-		return False
-
-	try:
-		currentSourcePath = os.stat(sys.argv[0])
-	except FileNotFoundError:
-		log.debug("Failed to access the current running NVDA directory.")
-		return False
-	except WindowsError:
-		log.error(
-			"Failed to access the current running NVDA directory.",
-			exc_info=True,
-		)
-		return False
-
-	return currentSourcePath == startAfterLogonPath
+	return easeOfAccess.willAutoStart(easeOfAccess.AutoStartContext.AFTER_LOGON)
 
 
 def setStartAfterLogon(enable: bool) -> None:
@@ -329,33 +279,10 @@ def setStartAfterLogon(enable: bool) -> None:
 
 	Toggle if NVDA automatically starts after a logon.
 	Sets easeOfAccess related registry keys.
-
-	When toggling off, always delete the registry run key
-	in case it was set by an earlier version of NVDA.
 	"""
 	if getStartAfterLogon() == enable:
 		return
 	easeOfAccess.setAutoStart(easeOfAccess.AutoStartContext.AFTER_LOGON, enable)
-	if enable:
-		return
-	# We're disabling, so ensure the run key is cleared,
-	# as it might have been set by an old version.
-	k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, _RegistryKey.RUN.value, access=winreg.KEY_WRITE)
-	try:
-		winreg.QueryValue(k, "nvda")
-	except FileNotFoundError:
-		log.debug(
-			"The run registry key is not set for setStartAfterLogon."
-			"This is expected since ease of access is used",
-		)
-		return
-	try:
-		winreg.DeleteValue(k, "nvda")
-	except WindowsError:
-		log.error(
-			"Couldn't unset registry key for nvda to start after logon.",
-			exc_info=True,
-		)
 
 
 SLAVE_FILENAME = os.path.join(globalVars.appDir, "nvda_slave.exe")
@@ -367,27 +294,8 @@ def getStartOnLogonScreen() -> bool:
 	Checks if NVDA is set to start on the logon screen.
 
 	Checks related easeOfAccess local machine registry keys.
-	Then, checks a NVDA registry key to see if NVDA
-	has been registered to start on logon by earlier NVDA versions.
 	"""
-	if easeOfAccess.willAutoStart(easeOfAccess.AutoStartContext.ON_LOGON_SCREEN):
-		return True
-	try:
-		k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, _RegistryKey.NVDA.value)
-	except FileNotFoundError:
-		log.debugWarning(f"Could not find NVDA reg key {_RegistryKey.NVDA}", exc_info=True)
-	except WindowsError:
-		log.error(f"Failed to open NVDA reg key {_RegistryKey.NVDA}", exc_info=True)
-	else:
-		try:
-			return bool(winreg.QueryValueEx(k, "startOnLogonScreen")[0])
-		except FileNotFoundError:
-			log.debug(f"Could not find startOnLogonScreen value for {_RegistryKey.NVDA} - likely unset.")
-			return False
-		except WindowsError:
-			log.error(f"Failed to query startOnLogonScreen value for {_RegistryKey.NVDA}", exc_info=True)
-			return False
-	return False
+	return easeOfAccess.willAutoStart(easeOfAccess.AutoStartContext.ON_LOGON_SCREEN)
 
 
 def _setStartOnLogonScreen(enable: bool) -> None:
@@ -396,7 +304,7 @@ def _setStartOnLogonScreen(enable: bool) -> None:
 
 def setSystemConfigToCurrentConfig():
 	fromPath = WritePaths.configDir
-	if ctypes.windll.shell32.IsUserAnAdmin():
+	if winBindings.shell32.IsUserAnAdmin():
 		_setSystemConfig(fromPath)
 	else:
 		import systemUtils
@@ -458,7 +366,10 @@ def setStartOnLogonScreen(enable: bool) -> None:
 		# Try setting it directly.
 		_setStartOnLogonScreen(enable)
 	except WindowsError:
-		log.debugWarning("Failed to set start on logon screen's config.")
+		log.debugWarning(
+			"Failed to set start on logon screen's config, retrying elevated.",
+			exc_info=True,
+		)
 		# We probably don't have admin privs, so we need to elevate to do this using the slave.
 		import systemUtils
 
@@ -1286,7 +1197,7 @@ def __setitem__(
 
 		# Alias old config items to their new counterparts for backwards compatibility.
 		# Uncomment when there are new links that need to be made.
-		# if BACK_COMPAT_TO < (2026, 1, 0) and NVDAState._allowDeprecatedAPI():
+		# if BACK_COMPAT_TO < (2027, 1, 0) and NVDAState._allowDeprecatedAPI():
 		# self._linkDeprecatedValues(key, val)
 
 	def _linkDeprecatedValues(self, key: aggregatedSection._cacheKeyT, val: aggregatedSection._cacheValueT):

```