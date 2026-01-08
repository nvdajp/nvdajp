# Diff for: `source\fileUtils.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\fileUtils.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\fileUtils.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\fileUtils.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\fileUtils.py"
index 3f8e752..c880f90 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\fileUtils.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\fileUtils.py"
@@ -9,11 +9,11 @@
 from contextlib import contextmanager
 from tempfile import NamedTemporaryFile
 from logHandler import log
-from six import text_type
 import winKernel
 import shlobj
 from functools import wraps
 import systemUtils
+import winBindings.version
 
 
 @contextmanager
@@ -31,7 +31,7 @@ def FaultTolerantFile(name):
 	This creates a temporary file, and the writes actually happen on this temp file. At the end of the
 	`with` block, when `f` goes out of context the temporary file is closed and, this temporary file replaces "myFile.txt"
 	"""
-	if not isinstance(name, text_type):
+	if not isinstance(name, str):
 		raise TypeError("name must be an unicode string")
 	dirpath, filename = os.path.split(name)
 	with NamedTemporaryFile(dir=dirpath, prefix=filename, suffix=".tmp", delete=False) as f:
@@ -72,23 +72,23 @@ def funcWrapper(filePath, *attributes):
 @_suspendWow64RedirectionForFileInfoRetrieval
 def getFileVersionInfo(name, *attributes):
 	"""Gets the specified file version info attributes from the provided file."""
-	if not isinstance(name, text_type):
+	if not isinstance(name, str):
 		raise TypeError("name must be an unicode string")
 	if not os.path.exists(name):
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
@@ -100,7 +100,7 @@ def getFileVersionInfo(name, *attributes):
 	codepage = array.array("H", ctypes.string_at(r.value, 4))
 	codepage = "%04x%04x" % tuple(codepage)
 	for attr in attributes:
-		if not ctypes.windll.version.VerQueryValueW(
+		if not winBindings.version.VerQueryValue(
 			res,
 			"\\StringFileInfo\\%s\\%s" % (codepage, attr),
 			ctypes.byref(r),

```