# Diff for: `source\buildVersion.py`

**Source**: `F:\nvda\gh\beta\source\buildVersion.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\buildVersion.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\buildVersion.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\buildVersion.py"
index 75922db..ca8fd95 100644
--- "a/F:\\nvda\\gh\\beta\\source\\buildVersion.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\buildVersion.py"
@@ -79,4 +79,6 @@ def formatVersionForGUI(year, major, minor):
 
 version_detailed = formatBuildVersionString()
 # A test version is anything other than a final or rc release.
+# nvdajp: defensive programming to ensure version is never None or empty
+version = version or "dev"
 isTestVersion = not version[0].isdigit() or "alpha" in version or "beta" in version or "dev" in version

```