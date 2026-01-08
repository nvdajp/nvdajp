# Diff for: `source\setup.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\setup.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\setup.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\setup.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\setup.py"
index 531153b..a4ffdd1 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\setup.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\setup.py"
@@ -1,4 +1,3 @@
-# -*- coding: UTF-8 -*-
 # A part of NonVisual Desktop Access (NVDA)
 # Copyright (C) 2006-2025 NV Access Limited, Peter Vágner, Joseph Lee
 # This file is covered by the GNU General Public License.
@@ -8,6 +7,12 @@
 import os
 import sys
 import gettext
+from buildVersion import (
+	formatBuildVersionString,
+	name,
+	publisher,
+	version,
+)
 
 gettext.install("nvda")
 from glob import glob  # noqa: E402
@@ -18,11 +23,7 @@
 from versionInfo import (  # noqa: E402
 	copyright as NVDAcopyright,  # copyright is a reserved python keyword
 	description,
-	formatBuildVersionString,
-	name,
-	publisher,
-	version,
-)  # noqa: E402
+)
 from py2exe import freeze  # noqa: E402
 from py2exe.dllfinder import DllFinder  # noqa: E402
 import wx  # noqa: E402
@@ -192,7 +193,7 @@ def _genManifestTemplate(shouldHaveUIAccess: bool) -> tuple[int, int, bytes]:
 	options={
 		"verbose": 2,
 		# Removes assertions for builds.
-		# https://docs.python.org/3.11/tutorial/modules.html#compiled-python-files
+		# https://docs.python.org/3.13/tutorial/modules.html#compiled-python-files
 		"optimize": 1,
 		"bundle_files": 3,
 		"dist_dir": "../dist",
@@ -212,12 +213,10 @@ def _genManifestTemplate(shouldHaveUIAccess: bool) -> tuple[int, int, bytes]:
 			# winxptheme is optionally used by wx.lib.agw.aui.
 			# We don't need this.
 			"winxptheme",
-			# numpy is an optional dependency of comtypes but we don't require it.
-			"numpy",
 			# multiprocessing isn't going to work in a frozen environment
 			"multiprocessing",
 			"concurrent.futures.process",
-			# Tomli is part of Python 3.11 as Tomlib, but is imported as tomli by cryptography, which causes an infinite loop in py2exe
+			# Tomli is part of Python 3.11+ as Tomlib, but is imported as tomli by cryptography, which causes an infinite loop in py2exe
 			"tomli",
 		],
 		"packages": [
@@ -245,6 +244,8 @@ def _genManifestTemplate(shouldHaveUIAccess: bool) -> tuple[int, int, bytes]:
 			"mdx_truly_sane_lists",
 			"mdx_gh_links",
 			"pymdownx",
+			# Required for local image captioning
+			"numpy",
 		],
 		"includes": [
 			"nvdaBuiltin",
@@ -252,15 +253,18 @@ def _genManifestTemplate(shouldHaveUIAccess: bool) -> tuple[int, int, bytes]:
 			"bisect",
 			# robotremoteserver (for system tests) depends on xmlrpc.server
 			"xmlrpc.server",
+			# required for import numpy without error
+			"numpy._core._exceptions",
+			"numpy._core._multiarray_umath",
 		],
 	},
 	data_files=[
-		(".", ["ja-jp-comp6.utb", "ja-jp-rokutenkanji.tbl"]),
 		(".", glob("*.dll") + glob("*.manifest") + ["builtin.dic"]),
 		("documentation", ["../copying.txt"]),
-		("lib/%s" % version, glob("lib/*.dll") + glob("lib/*.manifest")),
-		("lib64/%s" % version, glob("lib64/*.dll") + glob("lib64/*.exe")),
-		("libArm64/%s" % version, glob("libArm64/*.dll") + glob("libArm64/*.exe")),
+		("lib/%s/x86" % version, glob("lib/x86/*.dll") + glob("lib/x86/*.exe")),
+		("lib/%s/x64" % version, glob("lib/x64/*.dll") + glob("lib/x64/*.exe")),
+		("lib/%s/arm64" % version, glob("lib/arm64/*.dll") + glob("lib/arm64/*.exe")),
+		("lib/%s/arm64ec" % version, glob("lib/arm64ec/*.dll") + glob("lib/arm64ec/*.exe")),
 		("waves", glob("waves/*.wav")),
 		("images", glob("images/*.ico")),
 		("fonts", glob("fonts/*.ttf")),
@@ -271,8 +275,18 @@ def _genManifestTemplate(shouldHaveUIAccess: bool) -> tuple[int, int, bytes]:
 		(".", ["message.html"]),
 		(".", [os.path.join(sys.base_prefix, "python3.dll")]),
 	]
+	# BEGIN JP PATCH (Japanese braille tables)
+	# ja-jp-comp6.utb: JP-specific table, installed to dist root (TABLES_DIR_JP)
+	+ [(".", ["ja-jp-comp6.utb"])]
+	# Note: ja-rokutenkanji.utb is provided by liblouis 3.36.0+ (include/liblouis/tables/ja-rokutenkanji.utb)
+	# and is automatically copied to source/louis/tables/ by nvdaHelper/liblouis/sconscript
+	# END JP PATCH
 	+ (
 		getLocaleDataFiles()
+		+ getRecursiveDataFiles(
+			"include/nvda-mathcat/assets",
+			"../include/nvda-mathcat/assets",
+		)
 		+ getRecursiveDataFiles(
 			"synthDrivers",
 			"synthDrivers",

```