# Diff for: `source\gui\installerGui.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\gui\installerGui.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\installerGui.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\installerGui.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\installerGui.py"
index 3c90c5e..3e58886 100644
--- "a/F:\\nvda\\gh\\beta\\source\\gui\\installerGui.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\installerGui.py"
@@ -140,7 +140,7 @@ def doInstall(
 	newNVDA = None
 	if startAfterInstall:
 		newNVDA = core.NewNVDAInstance(
-			filePath=os.path.join(WritePaths.defaultInstallDir, "nvda.exe"),
+			filePath=os.path.join(installer.defaultInstallPath, "nvda.exe"),
 			parameters=_generate_executionParameters(),
 		)
 	if not core.triggerNVDAExit(newNVDA):
@@ -219,11 +219,11 @@ def __init__(self, parent, isUpdate):
 				# Translators: An informational message in the Install NVDA dialog.
 				"A previous copy of NVDA has been found on your system. This copy will be updated.",
 			)
-			if not os.path.isdir(WritePaths.defaultInstallDir):
+			if not os.path.isdir(installer.defaultInstallPath):
 				msg += " " + _(
 					# Translators: a message in the installer telling the user NVDA is now located in a different place.
 					"The installation path for NVDA has changed. it will now  be installed in {path}",
-				).format(path=WritePaths.defaultInstallDir)
+				).format(path=installer.defaultInstallPath)
 		if shouldAskAboutAddons:
 			msg += "\n\n" + getAddonCompatibilityMessage()
 

```