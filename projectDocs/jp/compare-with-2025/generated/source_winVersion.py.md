# Diff for: `source\winVersion.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\winVersion.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winVersion.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winVersion.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winVersion.py"
index 7adf440..140f0d6 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winVersion.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winVersion.py"
@@ -105,15 +105,12 @@ def __init__(
 
 	def _getWindowsReleaseName(self) -> str:
 		"""Returns the public release name for a given Windows release based on major, minor, and build.
+		This also includes feature update release name.
 		This is useful if release names are not defined when constructing this class.
-		For example, 6.3 will return 'Windows 8.1'.
-		For Windows 10 and later, feature update release name will be included.
 		On server systems, unless noted otherwise, client release names will be returned.
-		For example, 'Windows 10 1809' will be returned on Server 2019 systems.
+		For example, 'Windows 11 24H2' will be returned on Server 2025 systems.
 		"""
 		match (self.major, self.minor):
-			case (6, 3):
-				return "Windows 8.1"
 			# From Windows 10 1511 (build 10586), release Id/display version comes from Windows Registry.
 			# However there are builds with no release name (Version 1507/10240)
 			# or releases with different builds.
@@ -147,7 +144,6 @@ def __ge__(self, other):
 
 
 # Windows releases to WinVersion instances for easing comparisons.
-WIN81 = WinVersion(major=6, minor=3, build=9600)
 WIN10 = WIN10_1507 = WinVersion(major=10, minor=0, build=10240)
 WIN10_1511 = WinVersion(major=10, minor=0, build=10586)
 WIN10_1607 = WinVersion(major=10, minor=0, build=14393)
@@ -171,7 +167,7 @@ def __ge__(self, other):
 
 
 @functools.lru_cache(maxsize=1)
-def getWinVer():
+def getWinVer() -> WinVersion:
 	"""Returns a record of current Windows version NVDA is running on."""
 	winVer = sys.getwindowsversion()
 	# #12509: on Windows 10, fetch whatever Windows Registry says for the current build.
@@ -215,34 +211,18 @@ def getWinVer():
 	)
 
 
-def isSupportedOS():
-	# NVDA can only run on Windows 8.1 (Blue) and above
-	return getWinVer() >= WIN81
+def isSupportedOS() -> bool:
+	# NVDA can only run on Windows 10 and above
+	return getWinVer() >= WIN10
 
 
 UWP_OCR_DATA_PATH = os.path.expandvars(r"$windir\OCR")
 
 
-def isUwpOcrAvailable():
+def isUwpOcrAvailable() -> bool:
 	return os.path.isdir(UWP_OCR_DATA_PATH)
 
 
-if NVDAState._allowDeprecatedAPI():
-
-	def isFullScreenMagnificationAvailable() -> bool:
-		"""
-		Technically this is always False. The Magnification API has been marked by MS as unsupported for
-		WOW64 applications such as NVDA. For our usages, support has been added since Windows 8, relying on our
-		testing our specific usage of the API with each Windows version since Windows 8
-		"""
-		log.debugWarning(
-			"Deprecated function called: winVersion.isFullScreenMagnificationAvailable, "
-			"use visionEnhancementProviders.screenCurtain.ScreenCurtainProvider.canStart instead.",
-			stack_info=True,
-		)
-		return True
-
-
 def __getattr__(attrName: str) -> Any:
 	"""Module level `__getattr__` used to preserve backward compatibility."""
 	if attrName == "WIN7" and NVDAState._allowDeprecatedAPI():
@@ -254,4 +234,7 @@ def __getattr__(attrName: str) -> Any:
 	if attrName == "WIN8" and NVDAState._allowDeprecatedAPI():
 		log.warning("WIN8 is deprecated.")
 		return WinVersion(major=6, minor=2, build=9200, releaseName="Windows 8")
+	if attrName == "WIN81" and NVDAState._allowDeprecatedAPI():
+		log.warning("WIN81 is deprecated.")
+		return WinVersion(major=6, minor=3, build=9600, releaseName="Windows 8.1")
 	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")

```