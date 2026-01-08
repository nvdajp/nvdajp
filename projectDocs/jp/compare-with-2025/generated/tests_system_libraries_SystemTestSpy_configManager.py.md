# Diff for: `tests\system\libraries\SystemTestSpy\configManager.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\tests\system\libraries\SystemTestSpy\configManager.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\system\libraries\SystemTestSpy\configManager.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\system\\libraries\\SystemTestSpy\\configManager.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\SystemTestSpy\\configManager.py"
index fda1830..ae9286a 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\system\\libraries\\SystemTestSpy\\configManager.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\SystemTestSpy\\configManager.py"
@@ -105,6 +105,9 @@ def setupProfile(
 		_pJoin(repoRoot, "tests", "system", "nvdaSettingsFiles", settingsFileName),
 		_pJoin(stagingDir, "nvdaProfile", "nvda.ini"),
 	)
+	if _shouldGenerateMockModel(_pJoin(stagingDir, "nvdaProfile", "nvda.ini")):
+		_configModels(_pJoin(stagingDir, "nvdaProfile", "models", "mock", "vit-gpt2-image-captioning"))
+
 	if gesturesFileName is not None:
 		opSys.copy_file(
 			# Despite duplication, specify full paths for clarity.
@@ -128,3 +131,26 @@ def teardownProfile(stagingDir: str):
 		_pJoin(stagingDir, "nvdaProfile"),
 		recursive=True,
 	)
+
+
+def _configModels(modelsDirectory: str) -> None:
+	from .mockModels import MockVisionEncoderDecoderGenerator
+
+	generator = MockVisionEncoderDecoderGenerator(randomSeed=8)
+	generator.generateAllFiles(modelsDirectory)
+
+
+def _shouldGenerateMockModel(iniPath: str) -> bool:
+	# Read original lines
+	with open(iniPath, "r", encoding="utf-8") as f:
+		lines = f.readlines()
+
+	for line in lines:
+		# Detect section headers
+		stripLine = line.strip()
+		if stripLine.startswith("[") and stripLine.endswith("]"):
+			hasCaptionSection = stripLine.lower() == "[automatedimagedescriptions]"
+			if hasCaptionSection:
+				return True
+			else:
+				continue

```