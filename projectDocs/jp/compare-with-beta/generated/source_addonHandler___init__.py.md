# Diff for: `source\addonHandler\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\addonHandler\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\addonHandler\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\addonHandler\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\addonHandler\\__init__.py"
index 8e25e97..173a25f 100644
--- "a/F:\\nvda\\gh\\beta\\source\\addonHandler\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\addonHandler\\__init__.py"
@@ -31,7 +31,6 @@
 from configobj import ConfigObj
 from configobj.validate import Validator
 import config
-from config.registry import ADDON_BUNDLE_EXTENSION
 import languageHandler
 from logHandler import log
 import winBindings.kernel32
@@ -44,7 +43,6 @@
 from addonStore.models.status import AddonStateCategory, SupportsAddonState
 from addonStore.models.version import MajorMinorPatch, SupportsVersionCheck
 import extensionPoints
-from utils._deprecate import handleDeprecations, MovedSymbol
 from utils.caseInsensitiveCollections import CaseInsensitiveSet
 from utils.tempFile import _createEmptyTempFileForDeletingFile
 
@@ -63,22 +61,11 @@
 		InstalledAddonStoreModel,
 	)
 
-__getattr__ = handleDeprecations(
-	MovedSymbol(
-		"BUNDLE_EXTENSION",
-		"config",
-		"registry",
-		"ADDON_BUNDLE_EXTENSION",
-	),
-	MovedSymbol(
-		"NVDA_ADDON_PROG_ID",
-		"config.registry",
-	),
-)
-
 MANIFEST_FILENAME = "manifest.ini"
 stateFilename = "addonsState.pickle"
+BUNDLE_EXTENSION = "nvda-addon"
 BUNDLE_MIMETYPE = "application/x-nvda-addon"
+NVDA_ADDON_PROG_ID = "NVDA.Addon.1"
 ADDON_PENDINGINSTALL_SUFFIX = ".pendingInstall"
 DELETEDIR_SUFFIX = ".delete"
 
@@ -800,7 +787,7 @@ def _cleanupAddonImports(self) -> None:
 		self._importedAddonModules.clear()
 		for modName in set(sys.modules.keys()) - self._modulesBeforeInstall:
 			module = sys.modules[modName]
-			if module.__name__ and module.__name__.startswith(self.path):
+			if module.__file__ and module.__file__.startswith(self.path):
 				log.debug(f"Removing module {module} from cache of imported modules")
 				del sys.modules[modName]
 
@@ -991,7 +978,7 @@ def createAddonBundleFromPath(path, destDir=None):
 	if manifest.errors is not None:
 		_report_manifest_errors(manifest)
 		raise AddonError("Manifest file has errors.")
-	bundleFilename = f"{manifest['name']}-{manifest['version']}.{ADDON_BUNDLE_EXTENSION}"
+	bundleFilename = "%s-%s.%s" % (manifest["name"], manifest["version"], BUNDLE_EXTENSION)
 	bundleDestination = os.path.join(destDir, bundleFilename)
 	with zipfile.ZipFile(bundleDestination, "w") as z:
 		# FIXME: the include/exclude feature may or may not be useful. Also python files can be pre-compiled.

```