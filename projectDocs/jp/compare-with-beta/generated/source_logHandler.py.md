# Diff for: `source\logHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\logHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\logHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\logHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\logHandler.py"
index 9ecc27a..6a33bb2 100644
--- "a/F:\\nvda\\gh\\beta\\source\\logHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\logHandler.py"
@@ -184,11 +184,17 @@ def shouldPlayErrorSound() -> bool:
 	"""Indicates if an error sound should be played when an error is logged."""
 	import config
 
+	# BEGIN JP PATCH
+	# nvdajp: Only play the error sound if the config explicitly states it (Yes = 1).
+	# All versions are treated as release versions, so buildVersion.isTestVersion is not checked.
+	# END JP PATCH
 	# Only play the error sound if this is a test version or if the config states it explicitly.
+	# 0: Only in test versions, 1: Yes
 	return (
-		buildVersion.isTestVersion
-		# Play error sound: 1 = Yes
-		or (config.conf is not None and config.conf["featureFlag"]["playErrorSound"] == 1)
+		# BEGIN JP PATCH
+		# buildVersion.isTestVersion  # nvdajp: disabled - all versions treated as release
+		# END JP PATCH
+		config.conf is not None and config.conf["featureFlag"]["playErrorSound"] == 1
 	)
 
 

```