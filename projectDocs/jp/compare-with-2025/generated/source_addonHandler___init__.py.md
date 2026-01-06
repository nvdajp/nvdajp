# Diff for: `source\addonHandler\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\addonHandler\__init__.py`  
**Current**: `F:\nvda\gh\alphajp\source\addonHandler\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\addonHandler\\__init__.py" "b/F:\\nvda\\gh\\alphajp\\source\\addonHandler\\__init__.py"
index a4abb87186..d6b9e05860 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\addonHandler\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\addonHandler\\__init__.py"
@@ -1019,6 +1019,10 @@ class AddonManifest(ConfigObj):
 # Suggested convention is <major>.<minor>.<patch> format.
 version = string()
 
+# Changelog for the add-on version.
+# Document changes between the previous and the current versions.
+changelog = string(default=None)
+
 # The minimum required NVDA version for this add-on to work correctly.
 # Should be less than or equal to lastTestedNVDAVersion
 minimumNVDAVersion = apiVersion(default="0.0.0")
@@ -1080,7 +1084,7 @@ def __init__(self, input: IO[bytes], translatedInput: IO[bytes] | None = None):
 		self._translatedConfig = None
 		if translatedInput is not None:
 			self._translatedConfig = ConfigObj(translatedInput, encoding="utf-8", default_encoding="utf-8")
-			for k in ("summary", "description"):
+			for k in ("summary", "description", "changelog"):
 				val = self._translatedConfig.get(k)
 				if val:
 					self[k] = val

```