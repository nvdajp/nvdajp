# Diff for: `tests\unit\test_installer.py`

**Source**: `F:\nvda\gh\alphajp-251219\tests\unit\test_installer.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\unit\test_installer.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_installer.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_installer.py"
index 1750fff..310aa09 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_installer.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_installer.py"
@@ -131,7 +131,7 @@ def test_shouldWarnBeforeUpdate(
 		isUserAnAdmin: bool,
 		expectedReturn: bool,
 	):
-		with patch("gui.installerGui._IsUserAnAdmin", return_value=isUserAnAdmin):
+		with patch("winBindings.shell32.IsUserAnAdmin", return_value=isUserAnAdmin):
 			with patch(
 				"_remoteClient.client.RemoteClient",
 				isConnectedAsFollower=isConnectedAsFollower,

```