# Diff for: `source\installer.py`

**Source**: `F:\nvda\gh\beta\source\installer.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\installer.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\installer.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\installer.py"
index 44fa20c..717996a 100644
--- "a/F:\\nvda\\gh\\beta\\source\\installer.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\installer.py"
@@ -275,7 +275,7 @@ def getUninstallerRegInfo(installDir: str) -> dict[str, str | int]:
 	return dict(
 		DisplayName=f"{buildVersion.name} {buildVersion.version}",
 		DisplayVersion=buildVersion.version_detailed,
-		DisplayIcon=os.path.join(installDir, "images", "nvda.ico"),
+		DisplayIcon=os.path.join(installDir, "images", "nvdajp3.ico"),  # nvdajp
 		# EstimatedSize is in KiB
 		EstimatedSize=getDirectorySize(installDir) // 1024,
 		InstallDir=installDir,
@@ -472,6 +472,17 @@ def _updateShortcuts(
 		prependSpecialFolder="AllUsersPrograms",
 	)
 
+	# nvdajp begin
+	# Translators: A label for a shortcut in start menu and a menu entry in NVDA menu (to go to NVDAJP website).
+	jpWebSiteTranslated = _("NVDAJP web site")
+	_createShortcutWithFallback(
+		path=os.path.join(startMenuFolder, jpWebSiteTranslated + ".lnk"),
+		fallbackPath=os.path.join(startMenuFolder, "NVDAJP web site.lnk"),
+		targetPath="https://www.nvda.jp/",
+		prependSpecialFolder="AllUsersPrograms",
+	)
+	# nvdajp end
+
 	# Translators: A label for a shortcut item in start menu to uninstall NVDA from the computer.
 	uninstallTranslated = _("Uninstall NVDA")
 	_createShortcutWithFallback(
@@ -522,6 +533,16 @@ def _updateShortcuts(
 		targetPath=getDocFilePath("changes.html", installDir),
 		prependSpecialFolder="AllUsersPrograms",
 	)
+	# nvdajp begin
+	# Translators: A label for a shortcut in start menu to open NVDAJP readme
+	readmeJpTranslated = _("&Readme (nvdajp)")
+	_createShortcutWithFallback(
+		path=os.path.join(docFolder, readmeJpTranslated + ".lnk"),
+		fallbackPath=os.path.join(docFolder, "Readme (nvdajp).lnk"),
+		targetPath=getDocFilePath("readmejp.html", installDir),
+		prependSpecialFolder="AllUsersPrograms",
+	)
+	# nvdajp end
 
 
 def isDesktopShortcutInstalled():

```