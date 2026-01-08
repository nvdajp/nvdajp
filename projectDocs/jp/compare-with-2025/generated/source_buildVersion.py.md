# Diff for: `source\buildVersion.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\buildVersion.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\buildVersion.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\buildVersion.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\buildVersion.py"
index 26f303d..ca8fd95 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\buildVersion.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\buildVersion.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2024 NV Access Limited
+# Copyright (C) 2006-2025 NV Access Limited
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -63,12 +63,14 @@ def formatVersionForGUI(year, major, minor):
 
 # Version information for NVDA
 name = "NVDA"
-version_year = 2025
-version_major = 3
-version_minor = 2
+version_year = 2026
+version_major = 1
+version_minor = 0
 version_build = 0  # Should not be set manually. Set in 'sconscript'.
 version = _formatDevVersionString()
 publisher = "unknown"
+copyrightYears = "2006-2026"
+url = "https://www.nvaccess.org"
 updateVersionType = None
 try:
 	from _buildVersion import version, publisher, updateVersionType, version_build  # type: ignore[reportMissingModuleSource] # noqa: F401
@@ -77,5 +79,6 @@ def formatVersionForGUI(year, major, minor):
 
 version_detailed = formatBuildVersionString()
 # A test version is anything other than a final or rc release.
+# nvdajp: defensive programming to ensure version is never None or empty
 version = version or "dev"
 isTestVersion = not version[0].isdigit() or "alpha" in version or "beta" in version or "dev" in version

```