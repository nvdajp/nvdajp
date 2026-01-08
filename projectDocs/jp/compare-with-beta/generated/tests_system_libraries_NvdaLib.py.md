# Diff for: `tests\system\libraries\NvdaLib.py`

**Source**: `F:\nvda\gh\beta\tests\system\libraries\NvdaLib.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\system\libraries\NvdaLib.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\system\\libraries\\NvdaLib.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\NvdaLib.py"
index 7bae843..5d2697d 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\system\\libraries\\NvdaLib.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\NvdaLib.py"
@@ -100,12 +100,15 @@ def findInstalledNVDAPath(self) -> _Optional[str]:
 		NVDAFilePath = _pJoin(_expandvars("%PROGRAMFILES%"), "nvda", "nvda.exe")
 		legacyNVDAFilePath = _pJoin(_expandvars("%PROGRAMFILES%"), "NVDA", "nvda.exe")
 		exeErrorMsg = f"Unable to find installed NVDA exe. Paths tried: {NVDAFilePath}, {legacyNVDAFilePath}"
-		try:
-			opSys.file_should_exist(NVDAFilePath)
+		# Check if file exists before using file_should_exist to avoid early failure during import
+		import os
+		if os.path.isfile(NVDAFilePath):
 			return NVDAFilePath
-		except AssertionError:
-			# Older versions of NVDA (<=2020.4) install the exe in NVDA\nvda.exe
-			opSys.file_should_exist(legacyNVDAFilePath, exeErrorMsg)
+		elif os.path.isfile(legacyNVDAFilePath):
+			return legacyNVDAFilePath
+		else:
+			# If neither file exists, raise error with helpful message
+			opSys.file_should_exist(NVDAFilePath, exeErrorMsg)
 			return legacyNVDAFilePath
 
 	def ensureInstallerPathsExist(self):

```