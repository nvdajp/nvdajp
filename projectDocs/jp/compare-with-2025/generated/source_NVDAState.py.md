# Diff for: `source\NVDAState.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\NVDAState.py`  
**Current**: `F:\nvda\gh\alphajp\source\NVDAState.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAState.py" "b/F:\\nvda\\gh\\alphajp\\source\\NVDAState.py"
index fd4b5c7946..2b0fdd67fb 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAState.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\NVDAState.py"
@@ -5,11 +5,15 @@
 
 import os
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
@@ -37,10 +41,6 @@ def addonStoreDownloadDir(self) -> str:
 	def profilesDir(self) -> str:
 		return os.path.join(self.configDir, "profiles")
 
-	@property
-	def remoteAccessDir(self) -> str:
-		return os.path.join(self.configDir, "remoteAccess")
-
 	@property
 	def scratchpadDir(self) -> str:
 		return os.path.join(self.configDir, "scratchpad")
@@ -98,7 +98,71 @@ def getProfileConfigFile(self, name: str) -> str:
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

```