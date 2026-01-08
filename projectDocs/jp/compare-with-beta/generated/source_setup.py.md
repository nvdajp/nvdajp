# Diff for: `source\setup.py`

**Source**: `F:\nvda\gh\beta\source\setup.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\setup.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\setup.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\setup.py"
index bba5f0d..a4ffdd1 100644
--- "a/F:\\nvda\\gh\\beta\\source\\setup.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\setup.py"
@@ -121,7 +121,7 @@ def _genManifestTemplate(shouldHaveUIAccess: bool) -> tuple[int, int, bytes]:
 	{
 		"script": "nvda.pyw",
 		"dest_base": "nvda_noUIAccess",
-		"icon_resources": [(1, "images/nvda.ico")],
+		"icon_resources": [(1, "images/nvdajp3.ico")],
 		"other_resources": [_genManifestTemplate(shouldHaveUIAccess=False)],
 		"version_info": {
 			"version": formatBuildVersionString(),
@@ -135,7 +135,7 @@ def _genManifestTemplate(shouldHaveUIAccess: bool) -> tuple[int, int, bytes]:
 	# The nvda_uiAccess target will be added at runtime if required.
 	{
 		"script": "nvda_slave.pyw",
-		"icon_resources": [(1, "images/nvda.ico")],
+		"icon_resources": [(1, "images/nvdajp3.ico")],
 		"other_resources": [_genManifestTemplate(shouldHaveUIAccess=False)],
 		"version_info": {
 			"version": formatBuildVersionString(),
@@ -153,7 +153,7 @@ def _genManifestTemplate(shouldHaveUIAccess: bool) -> tuple[int, int, bytes]:
 		{
 			"script": "nvda.pyw",
 			"dest_base": "nvda_uiAccess",
-			"icon_resources": [(1, "images/nvda.ico")],
+			"icon_resources": [(1, "images/nvdajp3.ico")],
 			"other_resources": [_genManifestTemplate(shouldHaveUIAccess=True)],
 			"version_info": {
 				"version": formatBuildVersionString(),
@@ -275,6 +275,12 @@ def _genManifestTemplate(shouldHaveUIAccess: bool) -> tuple[int, int, bytes]:
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
 		+ getRecursiveDataFiles(

```