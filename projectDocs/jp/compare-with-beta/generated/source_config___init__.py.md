# Diff for: `source\config\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\config\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\config\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

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
+		if globalVars.appArgs.secure:
 			return
 		fn = self._getProfileFn(name)
 		if not os.path.isfile(fn):
@@ -747,8 +744,7 @@ def renameProfile(self, oldName, newName):
 		@raise LookupError: If the profile doesn't exist.
 		@raise ValueError: If a profile with the new name already exists.
 		"""
-		if not NVDAState.shouldWriteToDisk():
-			log.debug("Not renaming profile, as shouldWriteToDisk returned False.")
+		if globalVars.appArgs.secure:
 			return
 		if newName == oldName:
 			return
@@ -925,9 +921,8 @@ def saveProfileTriggers(self):
 		"""Save profile trigger information to disk.
 		This should be called whenever L{profilesToTriggers} is modified.
 		"""
-		if not NVDAState.shouldWriteToDisk():
+		if globalVars.appArgs.secure:
 			# Never save if running securely.
-			log.debug("Not saving profile triggers, as shouldWriteToDisk returned False.")
 			return
 		self.triggersToProfiles.parent.write()
 		log.info("Profile triggers saved")

```