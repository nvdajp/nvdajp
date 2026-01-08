# Diff for: `tests\unit\__init__.py`

**Source**: `F:\nvda\gh\alphajp-251219\tests\unit\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\unit\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\__init__.py"
index 2b33114..c5626f4 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\__init__.py"
@@ -132,10 +132,9 @@ def _patched_handleReviewMove(shouldAutoTether=True):
 # textutils tests need uniscribe in NVDAHelper local lib
 import ctypes  # noqa: E402
 import NVDAHelper  # noqa: E402
+import NVDAState  # noqa: E402
 
-NVDAHelper.localLib = ctypes.cdll.LoadLibrary(
-	os.path.join(NVDAHelper.versionedLibPath, "nvdaHelperLocal.dll"),
-)
+NVDAHelper.localLib = ctypes.cdll.LoadLibrary(NVDAState.ReadPaths.nvdaHelperLocalDll)
 # The focus and navigator objects need to be initialized to something.
 from .objectProvider import PlaceholderNVDAObject, NVDAObjectWithRole  # noqa: E402, F401
 

```