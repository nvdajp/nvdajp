# Diff for: `source\versionInfo.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\versionInfo.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\versionInfo.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\versionInfo.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\versionInfo.py"
index c63692b..e504ce0 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\versionInfo.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\versionInfo.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2024 NV Access Limited
+# Copyright (C) 2006-2025 NV Access Limited
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -9,12 +9,16 @@
 To access version information for programmatic version checks before languageHandler.initialize, use the buildVersion module which contains all the non-localizable version information such as major and minor version, and version string etc.
 """
 
-from buildVersion import *  # noqa: F403
+from buildVersion import (
+	copyrightYears,
+	name,
+	url,
+	version,
+	version_detailed,
+)
 
 longName = _("NonVisual Desktop Access")
 description = _("A free and open source screen reader for Microsoft Windows")
-url = "https://www.nvaccess.org"
-copyrightYears = "2006-2025"
 copyright = _("Copyright (C) {years} NVDA Contributors").format(
 	years=copyrightYears,
 )
@@ -25,10 +29,19 @@
 URL: {url}
 {copyright}
 
-{name} is covered by the GNU General Public License (Version 2). You are free to share or change this software in any way you like as long as it is accompanied by the license and you make all source code available to anyone who wants it. This applies to both original and modified copies of this software, plus any derivative works.
+{name} is covered by the GNU General Public License (Version 2 or later).
+You are free to share or change this software in any way you like as long as it is accompanied by the license and you make all source code available to anyone who wants it.
+This applies to both original and modified copies of this software, plus any derivative works.
 For further details, you can view the license from the Help menu.
-It can also be viewed online at: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
+It can also be viewed online at: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html and https://www.gnu.org/licenses/gpl-3.0.en.html
 
 {name} is developed by NV Access, a non-profit organisation committed to helping and promoting free and open source solutions for blind and vision impaired people.
 If you find NVDA useful and want it to continue to improve, please consider donating to NV Access. You can do this by selecting Donate from the NVDA menu.""",  # noqa: E501 line too long
-).format(**globals())
+).format(
+	longName=longName,
+	name=name,
+	version=version,
+	version_detailed=version_detailed,
+	url=url,
+	copyright=copyright,
+)

```