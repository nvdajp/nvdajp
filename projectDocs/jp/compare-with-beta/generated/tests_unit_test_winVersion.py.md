# Diff for: `tests\unit\test_winVersion.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\tests\unit\test_winVersion.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\unit\test_winVersion.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_winVersion.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_winVersion.py"
index 4dbe9e9..47e80ce 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_winVersion.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_winVersion.py"
@@ -89,7 +89,7 @@ def test_winVerUnknownBuildToReleaseName(self):
 	def test_winVerProcessorArchitecture(self):
 		# See if processor architecture matches what Windows says.
 		# Use os.environ to guard against platform.machine() giving odd results.
-		actualArchitecture = os.environ["PROCESSOR_ARCHITECTURE"]
+		actualArchitecture = os.environ.get("PROCESSOR_ARCHITEW6432", os.environ["PROCESSOR_ARCHITECTURE"])
 		self.assertEqual(winVersion.getWinVer().processorArchitecture, actualArchitecture)
 
 	def test_winVerUnknownWin11BuildToReleaseName(self):

```