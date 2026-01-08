# Diff for: `source\addonHandler\__init__.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\addonHandler\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\addonHandler\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\addonHandler\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\addonHandler\\__init__.py"
index a4abb87..8e25e97 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\addonHandler\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\addonHandler\\__init__.py"
@@ -16,7 +16,6 @@
 import shutil
 from io import StringIO
 import pickle
-from six import string_types
 from typing import (
 	Callable,
 	Dict,
@@ -32,9 +31,10 @@
 from configobj import ConfigObj
 from configobj.validate import Validator
 import config
+from config.registry import ADDON_BUNDLE_EXTENSION
 import languageHandler
 from logHandler import log
-import winKernel
+import winBindings.kernel32
 import addonAPIVersion
 import importlib
 import NVDAState
@@ -44,6 +44,7 @@
 from addonStore.models.status import AddonStateCategory, SupportsAddonState
 from addonStore.models.version import MajorMinorPatch, SupportsVersionCheck
 import extensionPoints
+from utils._deprecate import handleDeprecations, MovedSymbol
 from utils.caseInsensitiveCollections import CaseInsensitiveSet
 from utils.tempFile import _createEmptyTempFileForDeletingFile
 
@@ -62,11 +63,22 @@
 		InstalledAddonStoreModel,
 	)
 
+__getattr__ = handleDeprecations(
+	MovedSymbol(
+		"BUNDLE_EXTENSION",
+		"config",
+		"registry",
+		"ADDON_BUNDLE_EXTENSION",
+	),
+	MovedSymbol(
+		"NVDA_ADDON_PROG_ID",
+		"config.registry",
+	),
+)
+
 MANIFEST_FILENAME = "manifest.ini"
 stateFilename = "addonsState.pickle"
-BUNDLE_EXTENSION = "nvda-addon"
 BUNDLE_MIMETYPE = "application/x-nvda-addon"
-NVDA_ADDON_PROG_ID = "NVDA.Addon.1"
 ADDON_PENDINGINSTALL_SUFFIX = ".pendingInstall"
 DELETEDIR_SUFFIX = ".delete"
 
@@ -788,7 +800,7 @@ def _cleanupAddonImports(self) -> None:
 		self._importedAddonModules.clear()
 		for modName in set(sys.modules.keys()) - self._modulesBeforeInstall:
 			module = sys.modules[modName]
-			if module.__file__ and module.__file__.startswith(self.path):
+			if module.__name__ and module.__name__.startswith(self.path):
 				log.debug(f"Removing module {module} from cache of imported modules")
 				del sys.modules[modName]
 
@@ -950,7 +962,8 @@ def extract(self, addonPath: Optional[str] = None):
 					# #2505: Handle non-Unicode file names.
 					# Most archivers seem to use the local OEM code page, even though the spec says only cp437.
 					# HACK: Overriding info.filename is a bit ugly, but it avoids a lot of code duplication.
-					info.filename = info.filename.decode("cp%d" % winKernel.kernel32.GetOEMCP())
+					oemcp = winBindings.kernel32.GetOEMCP()
+					info.filename = info.filename.decode(f"cp{oemcp}")
 				z.extract(info, addonPath)
 
 	@property
@@ -978,7 +991,7 @@ def createAddonBundleFromPath(path, destDir=None):
 	if manifest.errors is not None:
 		_report_manifest_errors(manifest)
 		raise AddonError("Manifest file has errors.")
-	bundleFilename = "%s-%s.%s" % (manifest["name"], manifest["version"], BUNDLE_EXTENSION)
+	bundleFilename = f"{manifest['name']}-{manifest['version']}.{ADDON_BUNDLE_EXTENSION}"
 	bundleDestination = os.path.join(destDir, bundleFilename)
 	with zipfile.ZipFile(bundleDestination, "w") as z:
 		# FIXME: the include/exclude feature may or may not be useful. Also python files can be pre-compiled.
@@ -1019,6 +1032,10 @@ class AddonManifest(ConfigObj):
 # Suggested convention is <major>.<minor>.<patch> format.
 version = string()
 
+# Changelog for the add-on version.
+# Document changes between the previous and the current versions.
+changelog = string(default=None)
+
 # The minimum required NVDA version for this add-on to work correctly.
 # Should be less than or equal to lastTestedNVDAVersion
 minimumNVDAVersion = apiVersion(default="0.0.0")
@@ -1080,7 +1097,7 @@ def __init__(self, input: IO[bytes], translatedInput: IO[bytes] | None = None):
 		self._translatedConfig = None
 		if translatedInput is not None:
 			self._translatedConfig = ConfigObj(translatedInput, encoding="utf-8", default_encoding="utf-8")
-			for k in ("summary", "description"):
+			for k in ("summary", "description", "changelog"):
 				val = self._translatedConfig.get(k)
 				if val:
 					self[k] = val
@@ -1111,7 +1128,7 @@ def validate_apiVersionString(value: str) -> Tuple[int, int, int]:
 
 	if not value or value == "None":
 		return (0, 0, 0)
-	if not isinstance(value, string_types):
+	if not isinstance(value, str):
 		raise ValidateError('Expected an apiVersion in the form of a string. EG "2019.1.0"')
 	try:
 		return addonAPIVersion.getAPIVersionTupleFromString(value)

```