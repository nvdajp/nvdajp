# Diff for: `source\core.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\core.py`  
**Current**: `F:\nvda\gh\alphajp\source\core.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\core.py" "b/F:\\nvda\\gh\\alphajp\\source\\core.py"
index 02af36c8b9..25a34bb9be 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\core.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\core.py"
@@ -827,9 +827,9 @@ def main():
 		wx.CallAfter(audioDucking.initialize)
 
 	from winAPI.messageWindow import _MessageWindow
-	import versionInfo
+	import buildVersion
 
-	messageWindow = _MessageWindow(versionInfo.name)
+	messageWindow = _MessageWindow(buildVersion.name)
 
 	# initialize wxpython localization support
 	wxLocaleObj = wx.Locale()

```