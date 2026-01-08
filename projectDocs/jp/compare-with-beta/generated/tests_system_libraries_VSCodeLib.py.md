# Diff for: `tests\system\libraries\VSCodeLib.py`

**Source**: `F:\nvda\gh\beta\tests\system\libraries\VSCodeLib.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\system\libraries\VSCodeLib.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\system\\libraries\\VSCodeLib.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\VSCodeLib.py"
index 8f18c92..7a42199 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\system\\libraries\\VSCodeLib.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\VSCodeLib.py"
@@ -55,24 +55,13 @@ def _findCodeLauncher() -> str:
 				return f'"{resolved}"'
 		raise AssertionError("Visual Studio Code launcher not found. Is it installed?")
 
-	def start_vscode(self, targetPath: str | None = None) -> _Window:
-		"""Start Visual Studio Code.
-
-		:param targetPath: The path to the folder or file to open, defaults to a temporary directory.
-		:return: The window object for the started Visual Studio Code instance
-		"""
+	def start_vscode(self) -> _Window:
 		launcher = self._findCodeLauncher()
 		if VSCodeLib._testTempDir is None:
 			VSCodeLib._testTempDir = _tempfile.mkdtemp(prefix="nvdatest")
 		userDataDir = _os.path.join(VSCodeLib._testTempDir, "vscodeUserData")
 		_os.makedirs(userDataDir, exist_ok=True)
 
-		if targetPath is None:
-			targetPath = _os.path.join(VSCodeLib._testTempDir, "testDirectory")
-
-		if not _os.path.exists(targetPath):
-			_os.makedirs(targetPath, exist_ok=True)
-
 		# Prepare user settings to suppress welcome/startup screen
 		userSettingsDir = _os.path.join(userDataDir, "User")
 		_os.makedirs(userSettingsDir, exist_ok=True)
@@ -108,7 +97,6 @@ def start_vscode(self, targetPath: str | None = None) -> _Window:
 			f"--skip-add-to-recently-opened "
 			f"-n "
 			f"--wait"
-			f' "{targetPath}"'
 		)
 		_builtIn.log(f"Starting Visual Studio Code: {cmd}", level="DEBUG")
 		VSCodeLib._processRFHandleForStart = _process.start_process(

```