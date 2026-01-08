# Diff for: `source\addonStore\models\addon.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\addonStore\models\addon.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\addonStore\models\addon.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\addonStore\\models\\addon.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\addonStore\\models\\addon.py"
index aa17a08..97443de 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\addonStore\\models\\addon.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\addonStore\\models\\addon.py"
@@ -24,6 +24,7 @@
 from NVDAState import WritePaths
 
 from .channel import Channel
+from .scanResults import VirusTotalScanResults
 from .status import SupportsAddonState
 from .version import (
 	MajorMinorPatch,
@@ -58,7 +59,8 @@ class _AddonGUIModel(SupportsAddonState, SupportsVersionCheck, Protocol):
 	description: str
 	addonVersionName: str
 	channel: Channel
-	homepage: Optional[str]
+	homepage: str | None
+	changelog: str | None
 	minNVDAVersion: MajorMinorPatch
 	lastTestedVersion: MajorMinorPatch
 	legacy: bool
@@ -114,19 +116,21 @@ class _AddonStoreModel(_AddonGUIModel):
 	description: str
 	addonVersionName: str
 	channel: Channel
-	homepage: Optional[str]
+	homepage: str | None
+	changelog: str | None
 	minNVDAVersion: MajorMinorPatch
 	lastTestedVersion: MajorMinorPatch
 	legacy: bool
 	publisher: str
 	license: str
-	licenseURL: Optional[str]
+	licenseURL: str | None
 	sourceURL: str
 	URL: str
 	sha256: str
 	addonVersionNumber: MajorMinorPatch
-	reviewURL: Optional[str]
+	reviewURL: str | None
 	submissionTime: int | None
+	scanResults: VirusTotalScanResults | None = None
 
 	@property
 	def tempDownloadPath(self) -> str:
@@ -221,6 +225,11 @@ def description(self) -> str:
 			return ""
 		return description
 
+	@property
+	def changelog(self) -> str | None:
+		changelog: str | None = self.manifest.get("changelog")
+		return changelog
+
 	@property
 	def installDate(self) -> datetime:
 		return datetime.fromtimestamp(os.path.getctime(self.installPath))
@@ -260,17 +269,18 @@ class InstalledAddonStoreModel(_AddonManifestModel, _AddonStoreModel):
 	publisher: str
 	addonVersionName: str
 	channel: Channel
-	homepage: Optional[str]
+	homepage: str | None
 	license: str
-	licenseURL: Optional[str]
+	licenseURL: str | None
 	sourceURL: str
 	URL: str
 	sha256: str
 	addonVersionNumber: MajorMinorPatch
 	minNVDAVersion: MajorMinorPatch
 	lastTestedVersion: MajorMinorPatch
-	reviewURL: Optional[str]
+	reviewURL: str | None
 	submissionTime: int | None
+	scanResults: VirusTotalScanResults | None = None
 	legacy: bool = False
 	"""
 	Legacy add-ons contain invalid metadata
@@ -297,18 +307,20 @@ class AddonStoreModel(_AddonStoreModel):
 	publisher: str
 	addonVersionName: str
 	channel: Channel
-	homepage: Optional[str]
+	homepage: str | None
+	changelog: str | None
 	license: str
-	licenseURL: Optional[str]
+	licenseURL: str | None
 	sourceURL: str
 	URL: str
 	sha256: str
 	addonVersionNumber: MajorMinorPatch
 	minNVDAVersion: MajorMinorPatch
 	lastTestedVersion: MajorMinorPatch
-	reviewURL: Optional[str]
+	reviewURL: str | None
 	submissionTime: int | None
 	legacy: bool = False
+	scanResults: VirusTotalScanResults | None = None
 	"""
 	Legacy add-ons contain invalid metadata
 	and should not be accessible through the add-on store.
@@ -341,6 +353,7 @@ def _createInstalledStoreModelFromData(addon: Dict[str, Any]) -> InstalledAddonS
 		lastTestedVersion=MajorMinorPatch(**addon["lastTestedVersion"]),
 		reviewURL=addon.get("reviewURL"),
 		submissionTime=addon.get("submissionTime"),
+		scanResults=VirusTotalScanResults.fromDict(addon),
 		legacy=addon.get("legacy", False),
 	)
 
@@ -355,6 +368,7 @@ def _createStoreModelFromData(addon: Dict[str, Any]) -> AddonStoreModel:
 		addonVersionName=addon["addonVersionName"],
 		addonVersionNumber=MajorMinorPatch(**addon["addonVersionNumber"]),
 		homepage=addon.get("homepage"),
+		changelog=addon.get("changelog"),
 		license=addon["license"],
 		licenseURL=addon.get("licenseURL"),
 		sourceURL=addon["sourceURL"],
@@ -364,6 +378,7 @@ def _createStoreModelFromData(addon: Dict[str, Any]) -> AddonStoreModel:
 		lastTestedVersion=MajorMinorPatch(**addon["lastTestedVersion"]),
 		reviewURL=addon.get("reviewUrl"),
 		submissionTime=addon.get("submissionTime"),
+		scanResults=VirusTotalScanResults.fromDict(addon),
 		legacy=addon.get("legacy", False),
 	)
 

```