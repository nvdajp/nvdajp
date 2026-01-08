# Diff for: `source\COMRegistrationFixes\__init__.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\COMRegistrationFixes\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\COMRegistrationFixes\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\COMRegistrationFixes\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\COMRegistrationFixes\\__init__.py"
index 429213a..8bb504f 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\COMRegistrationFixes\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\COMRegistrationFixes\\__init__.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2018-2023 NV Access Limited, Luke Davis (Open Source Systems, Ltd.)
+# Copyright (C) 2018-2025 NV Access Limited, Luke Davis (Open Source Systems, Ltd.)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -12,6 +12,7 @@
 
 import os
 import subprocess
+import sysconfig
 import winVersion
 import globalVars
 from logHandler import log
@@ -28,12 +29,19 @@
 
 def register32bitServer(fileName: str) -> None:
 	"""Registers the COM proxy dll with the given file name, using the 32-bit version of regsvr32.
-	Note: this function is valid while NVDA remains a 32-bit app. Re-evaluate if we move to 64-bit.
 
-	:param fileName: The path to the DLL
+	:param fileName: The 32 bit path to the DLL
 	"""
-	# Points to the 32-bit version, on Windows 32-bit or 64-bit.
-	regsvr32 = os.path.join(SYSTEM32, "regsvr32.exe")
+	if sysconfig.get_platform() == "win32":
+		# NVDA is 32 bit.
+		# On 32-bit systems, the 32-bit version of regsvr32.exe is in System32.
+		# On 64-bit systems, the 32-bit version of regsvr32.exe is in SysWOW64,
+		# but system32 is automatically redirected to SysWOW64 for 32-bit applications.
+		regsvr32 = os.path.join(SYSTEM_ROOT, "system32", "regsvr32.exe")
+	else:
+		# NVDA is 64 bit, and therefore the OS is also 64 bit.
+		# On 64-bit systems, the 32-bit version of regsvr32.exe is in SysWOW64.
+		regsvr32 = os.path.join(SYSTEM_ROOT, "SysWOW64", "regsvr32.exe")
 	# Make sure a console window doesn't show when running regsvr32.exe
 	startupInfo = subprocess.STARTUPINFO()
 	startupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
@@ -48,12 +56,17 @@ def register32bitServer(fileName: str) -> None:
 
 def register64bitServer(fileName: str) -> None:
 	"""Registers the COM proxy dll with the given file name, using the 64-bit version of regsvr64.
-	Note: this function is valid while NVDA remains a 32-bit app. Re-evaluate if we move to 64-bit.
 
-	:param fileName: The path to the DLL
+	:param fileName: The 64 bit path to the DLL
 	"""
-	# SysWOW64 provides a virtual directory to allow 32-bit programs to reach 64-bit executables.
-	regsvr32 = os.path.join(SYSNATIVE, "regsvr32.exe")
+	if sysconfig.get_platform() == "win32":
+		# NVDA is 32 bit.
+		# On 64 bit systems, Sysnative provides a virtual directory to reach 64-bit executables from 32-bit applications.
+		regsvr32 = os.path.join(SYSTEM_ROOT, "Sysnative", "regsvr32.exe")
+	else:
+		# NVDA is 64 bit.
+		# On 64-bit systems, the 64-bit version of regsvr32.exe is in System32.
+		regsvr32 = os.path.join(SYSTEM_ROOT, "system32", "regsvr32.exe")
 	# Make sure a console window doesn't show when running regsvr32.exe
 	startupInfo = subprocess.STARTUPINFO()
 	startupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
@@ -68,13 +81,21 @@ def register64bitServer(fileName: str) -> None:
 
 def apply32bitRegistryPatch(fileName: str) -> None:
 	"""Applies the registry patch with the given file name, using 32-bit regExe.
-	Note: this function is valid while NVDA remains a 32-bit app. Re-evaluate if we move to 64-bit.
-	:param fileName: The path to the .reg file
+
+	:param fileName: The 32 bit path to the .reg file
 	"""
 	if not os.path.isfile(fileName):
 		raise FileNotFoundError(f"Cannot apply 32-bit registry patch: {fileName} not found.")
-	# On 32-bit systems, reg.exe is in System32. On 64-bit systems, SysWOW64 will redirect to 32-bit version.
+	if sysconfig.get_platform() == "win32":
+		# NVDA is 32 bit.
+		# On 32-bit systems, the 32-bit version of reg.exe is in System32.
+		# On 64-bit systems, the 32-bit version of reg.exe is in SysWOW64,
+		# but system32 is automatically redirected to SysWOW64 for 32-bit applications.
 		regExe = os.path.join(SYSTEM_ROOT, "System32", "reg.exe")
+	else:
+		# NVDA is 64 bit, and therefore the OS is also 64 bit.
+		# On 64-bit systems, the 32-bit version of reg.exe is in SysWOW64.
+		regExe = os.path.join(SYSTEM_ROOT, "SysWOW64", "reg.exe")
 	# Make sure a console window doesn't show when running reg.exe
 	startupInfo = subprocess.STARTUPINFO()
 	startupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
@@ -89,14 +110,19 @@ def apply32bitRegistryPatch(fileName: str) -> None:
 
 def apply64bitRegistryPatch(fileName: str) -> None:
 	"""Applies the registry patch with the given file name, using 64-bit regExe.
-	Note: this function is valid while NVDA remains a 32-bit app. Re-evaluate if we move to 64-bit.
 
-	:param fileName: The path to the .reg file
+	:param fileName: The 64 bit path to the .reg file
 	"""
 	if not os.path.isfile(fileName):
 		raise FileNotFoundError(f"Cannot apply 64-bit registry patch: {fileName} not found.")
-	# On 64-bit systems, SysWOW64 provides 32-bit apps with a virtual directory to reach 64-bit executables.
-	regExe = os.path.join(SYSNATIVE, "reg.exe")
+	if sysconfig.get_platform() == "win32":
+		# NVDA is 32 bit.
+		# On 64-bit systems, Sysnative provides a virtual directory to reach 64-bit executables from 32-bit applications.
+		regExe = os.path.join(SYSTEM_ROOT, "Sysnative", "reg.exe")
+	else:
+		# NVDA is 64 bit.
+		# On 64-bit systems, the 64-bit version of reg.exe is in System32.
+		regExe = os.path.join(SYSTEM_ROOT, "system32", "reg.exe")
 	# Make sure a console window doesn't show when running reg.exe
 	startupInfo = subprocess.STARTUPINFO()
 	startupInfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

```