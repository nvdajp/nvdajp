# Diff for: `source\config\registry.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\config\registry.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\config\registry.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\config\\registry.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\registry.py"
index 1f75a76..1ff385f 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\config\\registry.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\registry.py"
@@ -4,9 +4,14 @@
 # See the file COPYING for more details.
 
 from enum import Enum, nonmember
+import winreg
+
+from winBindings.advapi32 import RegDeleteTree
 
 
 EASE_OF_ACCESS_APP_KEY_NAME = "nvda_nvda_v1"
+NVDA_ADDON_PROG_ID = "NVDA.Addon.1"
+ADDON_BUNDLE_EXTENSION = "nvda-addon"
 
 
 class RegistryKey(str, Enum):
@@ -26,7 +31,12 @@ class RegistryKey(str, Enum):
 	NT_CURRENT_VERSION = rf"{_SOFTWARE}\Microsoft\Windows NT\CurrentVersion"
 	EASE_OF_ACCESS = rf"{NT_CURRENT_VERSION}\Accessibility"
 	EASE_OF_ACCESS_TEMP = rf"{NT_CURRENT_VERSION}\AccessibilityTemp"
+	# This should always be accessed with 64-bit view of the registry.
+	# TODO: remove winreg.KEY_WOW64_64KEY from usages when NVDA is 64-bit only.
 	EASE_OF_ACCESS_APP = rf"{EASE_OF_ACCESS}\ATs\{EASE_OF_ACCESS_APP_KEY_NAME}"
+	ADDON_PROG = rf"{_SOFTWARE}\Classes\{NVDA_ADDON_PROG_ID}"
+	ADDON_EXT = rf"{_SOFTWARE}\Classes\.{ADDON_BUNDLE_EXTENSION}"
+	REMOTE_URL_HANDLER = rf"{_SOFTWARE}\Classes\nvdaremote"
 
 	# Sub keys
 
@@ -52,13 +62,14 @@ class _RegistryKeyX86(str, Enum):  # type: ignore[reportUnusedClass]
 
 	_SOFTWARE = nonmember(r"SOFTWARE\WOW6432Node")
 	CURRENT_VERSION = rf"{_SOFTWARE}\Microsoft\Windows\CurrentVersion"
-	INSTALLED_COPY = rf"{CURRENT_VERSION}\Uninstall\NVDA"
-	RUN = rf"{CURRENT_VERSION}\Run"
-	NVDA = rf"{_SOFTWARE}\NVDA"
-	APP_PATH = rf"{CURRENT_VERSION}\App Paths\nvda.exe"
-	EXPLORER_ADVANCED = rf"{CURRENT_VERSION}\Explorer\Advanced"
-	SYSTEM_POLICIES = rf"{CURRENT_VERSION}\Policies\System"
-	NT_CURRENT_VERSION = rf"{_SOFTWARE}\Microsoft\Windows NT\CurrentVersion"
-	EASE_OF_ACCESS = rf"{NT_CURRENT_VERSION}\Accessibility"
-	EASE_OF_ACCESS_TEMP = rf"{NT_CURRENT_VERSION}\AccessibilityTemp"
-	EASE_OF_ACCESS_APP = rf"{EASE_OF_ACCESS}\ATs\{EASE_OF_ACCESS_APP_KEY_NAME}"
+
+
+def _deleteKeyAndSubkeys(key: int, subkey: str, access: int = 0) -> None:
+	"""Delete a registry key and all its subkeys using RegDeleteTree via winBindings.advapi32."""
+	with winreg.OpenKey(key, "", 0, winreg.KEY_WRITE | winreg.KEY_READ | access) as parent:
+		result = RegDeleteTree(
+			parent.handle,
+			subkey,
+		)
+	if result != 0:
+		raise WindowsError(result, f"RegDeleteTree failed for {subkey=}")

```