# Diff for: `source\fileUtils.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\fileUtils.py`  
**Current**: `F:\nvda\gh\alphajp\source\fileUtils.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\fileUtils.py" "b/F:\\nvda\\gh\\alphajp\\source\\fileUtils.py"
index 3f8e752148..1a589f1ea8 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\fileUtils.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\fileUtils.py"
@@ -14,6 +14,7 @@
 import shlobj
 from functools import wraps
 import systemUtils
+import winBindings.version
 
 
 @contextmanager
@@ -78,17 +79,17 @@ def getFileVersionInfo(name, *attributes):
 		raise RuntimeError("The file %s does not exist" % name)
 	fileVersionInfo = {}
 	# Get size needed for buffer (0 if no info)
-	size = ctypes.windll.version.GetFileVersionInfoSizeW(name, None)
+	size = winBindings.version.GetFileVersionInfoSize(name, None)
 	if not size:
 		raise RuntimeError("No version information")
 	# Create buffer
 	res = ctypes.create_string_buffer(size)
 	# Load file informations into buffer res
-	ctypes.windll.version.GetFileVersionInfoW(name, None, size, res)
+	winBindings.version.GetFileVersionInfo(name, 0, size, res)
 	r = ctypes.c_void_p()
 	l = ctypes.c_uint()  # noqa: E741
 	# Look for codepages
-	ctypes.windll.version.VerQueryValueW(
+	winBindings.version.VerQueryValue(
 		res,
 		"\\VarFileInfo\\Translation",
 		ctypes.byref(r),
@@ -100,7 +101,7 @@ def getFileVersionInfo(name, *attributes):
 	codepage = array.array("H", ctypes.string_at(r.value, 4))
 	codepage = "%04x%04x" % tuple(codepage)
 	for attr in attributes:
-		if not ctypes.windll.version.VerQueryValueW(
+		if not winBindings.version.VerQueryValue(
 			res,
 			"\\StringFileInfo\\%s\\%s" % (codepage, attr),
 			ctypes.byref(r),

```