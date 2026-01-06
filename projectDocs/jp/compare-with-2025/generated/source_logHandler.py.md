# Diff for: `source\logHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\logHandler.py`  
**Current**: `F:\nvda\gh\alphajp\source\logHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\logHandler.py" "b/F:\\nvda\\gh\\alphajp\\source\\logHandler.py"
index 985f611cc7..f4f630fc33 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\logHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\logHandler.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2007-2024 NV Access Limited, Rui Batista, Joseph Lee, Leonard de Ruijter, Babbage B.V.,
+# Copyright (C) 2007-2025 NV Access Limited, Rui Batista, Joseph Lee, Leonard de Ruijter, Babbage B.V.,
 # Accessolutions, Julien Cochuyt, Cyrille Bougot, Łukasz Golonka
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
@@ -22,7 +22,6 @@
 from typing import (
 	Literal,
 	NamedTuple,
-	Optional,
 	Protocol,
 	TYPE_CHECKING,
 )
@@ -159,7 +158,7 @@ def getCodePath(f):
 	return ".".join(x for x in (path, className, funcName) if x)
 
 
-_onErrorSoundRequested: Optional["extensionPoints.Action"] = None
+_onErrorSoundRequested: "extensionPoints.Action | None" = None
 """
 Triggered every time an error sound needs to be played.
 When nvwave is initialized, it registers the handler responsible for playing the error sound.
@@ -184,11 +183,16 @@ def shouldPlayErrorSound() -> bool:
 	"""Indicates if an error sound should be played when an error is logged."""
 	import config
 
+	# BEGIN JP PATCH
+	# nvdajp: Only play the error sound if the config explicitly states it (Yes = 1).
+	# All versions are treated as release versions, so buildVersion.isTestVersion is not checked.
+	# END JP PATCH
 	# Only play the error sound if this is a test version or if the config states it explicitly.
+	# 0: Only in test versions, 1: Yes
 	return (
-		# buildVersion.isTestVersion
-		# Play error sound: 1 = Yes
-		# or
+		# BEGIN JP PATCH
+		# buildVersion.isTestVersion  # nvdajp: disabled - all versions treated as release
+		# END JP PATCH
 		config.conf is not None and config.conf["featureFlag"]["playErrorSound"] == 1
 	)
 
@@ -266,13 +270,6 @@ def _log(
 				"".join(traceback.format_list(stack_info)).rstrip(),
 			)
 
-		from six import unichr, text_type
-		import re
-
-		try:
-			msg = re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x" + x.group(1), 16)), text_type(msg))
-		except:  # noqa: E722
-			pass
 		res = super()._log(level, msg, args, exc_info, extra)
 
 		if activateLogViewer:
@@ -388,12 +385,17 @@ def getFragment(self):
 
 class RemoteHandler(logging.Handler):
 	def __init__(self):
-		# Load nvdaHelperRemote.dll but with an altered search path so it can pick up other dlls in lib
-		path = os.path.join(globalVars.appDir, "lib", buildVersion.version, "nvdaHelperRemote.dll")
-		h = ctypes.windll.kernel32.LoadLibraryExW(path, 0, LOAD_WITH_ALTERED_SEARCH_PATH)
-		if not h:
-			raise OSError("Could not load %s" % path)
-		self._remoteLib = ctypes.WinDLL("nvdaHelperRemote", handle=h)
+		import winBindings.kernel32
+
+		h = winBindings.kernel32.LoadLibraryEx(
+			NVDAState.ReadPaths.nvdaHelperRemoteDll,
+			0,
+			# Using an altered search path is necessary here
+			# As NVDAHelperRemote needs to locate dependent dlls in the same directory
+			# such as IAccessible2proxy.dll.
+			winKernel.LOAD_WITH_ALTERED_SEARCH_PATH,
+		)
+		self._remoteLib = ctypes.CDLL("nvdaHelperRemote", handle=h)
 		logging.Handler.__init__(self)
 
 	def emit(self, record):
@@ -431,7 +433,7 @@ def format(self, record: logging.LogRecord) -> str:
 			record.codepath = "{name}.{funcName}".format(**record.__dict__)
 		return super().format(record)
 
-	def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None) -> str:
+	def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
 		"""Custom implementation of `formatTime` which avoids `time.localtime`
 		since it causes a crash under some versions of Universal CRT when Python locale
 		is set to a Unicode one (#12160, Python issue 36792)
@@ -485,7 +487,7 @@ def redirectStdout(logger):
 #: The singleton logger instance.
 log: Logger = logging.getLogger(NVDA_LOGGER_NAME)
 #: The singleton log handler instance.
-logHandler: Optional[logging.Handler] = None
+logHandler: logging.Handler | None = None
 
 
 def _getDefaultLogFilePath():

```