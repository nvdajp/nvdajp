# Diff for: `source\updateCheck.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\updateCheck.py`  
**Current**: `F:\nvda\gh\alphajp\source\updateCheck.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\updateCheck.py" "b/F:\\nvda\\gh\\alphajp\\source\\updateCheck.py"
index 9dfabc3f3f..0bf98787d4 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\updateCheck.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\updateCheck.py"
@@ -29,9 +29,9 @@
 	raise RuntimeError("updates disabled in secure mode")
 elif config.isAppX:
 	raise RuntimeError("updates managed by Windows Store")
-import versionInfo
+import buildVersion
 
-if not versionInfo.updateVersionType:
+if not buildVersion.updateVersionType:
 	raise RuntimeError("No update version type, update checking not supported")
 # Avoid a E402 'module level import not at top of file' warning, because several checks are performed above.
 import gui.contextHelp  # noqa: E402
@@ -73,8 +73,9 @@
 
 
 #: The URL to use for update checks.
-# _DEFAULT_CHECK_URL = "https://api.nvaccess.org/nvdaUpdateCheck"
+# BEGIN JP PATCH (Japanese update server URL)
 _DEFAULT_CHECK_URL = "https://www.nvda.jp/updateCheck/"
+# END JP PATCH
 #: The time to wait between checks.
 CHECK_INTERVAL = 86400  # 1 day
 #: The time to wait before retrying a failed check.
@@ -202,8 +203,8 @@ def checkForUpdate(auto: bool = False) -> UpdateInfo | None:
 	params = {
 		"autoCheck": auto,
 		"allowUsageStats": allowUsageStats,
-		"version": versionInfo.version,
-		"versionType": versionInfo.updateVersionType,
+		"version": buildVersion.version,
+		"versionType": buildVersion.updateVersionType,
 		"osVersion": winVersionText,
 		# Check if the architecture is the most common: "AMD64"
 		# Available values of PROCESSOR_ARCHITEW6432 found in:
@@ -1051,7 +1052,7 @@ def initialize():
 
 	# check the pending version against the current version
 	# and make sure that pendingUpdateFile and pendingUpdateVersion are part of the state dictionary.
-	if "pendingUpdateVersion" not in state or state["pendingUpdateVersion"] == versionInfo.version:
+	if "pendingUpdateVersion" not in state or state["pendingUpdateVersion"] == buildVersion.version:
 		_setStateToNone(state)
 	# remove all update files except the one that is currently pending (if any)
 	try:

```