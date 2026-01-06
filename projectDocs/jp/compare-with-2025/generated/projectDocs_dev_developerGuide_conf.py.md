# Diff for: `projectDocs\dev\developerGuide\conf.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\projectDocs\dev\developerGuide\conf.py`  
**Current**: `F:\nvda\gh\alphajp\projectDocs\dev\developerGuide\conf.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\projectDocs\\dev\\developerGuide\\conf.py" "b/F:\\nvda\\gh\\alphajp\\projectDocs\\dev\\developerGuide\\conf.py"
index e35104d115..898a9f4924 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\projectDocs\\dev\\developerGuide\\conf.py"
+++ "b/F:\\nvda\\gh\\alphajp\\projectDocs\\dev\\developerGuide\\conf.py"
@@ -44,26 +44,27 @@
 
 
 # Import NVDA's versionInfo module.
+import buildVersion  # noqa: E402
 import versionInfo  # noqa: E402
 
 # Set a suitable updateVersionType for the updateCheck module to be imported
-versionInfo.updateVersionType = "stable"
+buildVersion.updateVersionType = "stable"
 
 # -- Project information -----------------------------------------------------
 
-project = versionInfo.name
+project = buildVersion.name
 copyright = versionInfo.copyright
-author = versionInfo.publisher
+author = buildVersion.publisher
 
 # The major project version
-version = versionInfo.formatVersionForGUI(
-	versionInfo.version_year,
-	versionInfo.version_major,
-	versionInfo.version_minor,
+version = buildVersion.formatVersionForGUI(
+	buildVersion.version_year,
+	buildVersion.version_major,
+	buildVersion.version_minor,
 )
 
 # The full version, including alpha/beta/rc tags
-release = versionInfo.version
+release = buildVersion.version
 
 # -- General configuration ---------------------------------------------------
 

```