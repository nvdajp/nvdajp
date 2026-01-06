# Diff for: `tests\unit\test_installer.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\tests\unit\test_installer.py`  
**Current**: `F:\nvda\gh\alphajp\tests\unit\test_installer.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_installer.py" "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\test_installer.py"
index 1750fffc93..310aa09484 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_installer.py"
+++ "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\test_installer.py"
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