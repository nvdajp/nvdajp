# Diff for: `source\easeOfAccess.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\easeOfAccess.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\easeOfAccess.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\easeOfAccess.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\easeOfAccess.py"
index c9c5ea7..e4b4cb6 100644
--- "a/F:\\nvda\\gh\\beta\\source\\easeOfAccess.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\easeOfAccess.py"
@@ -138,7 +138,6 @@ def _getAutoStartConfiguration(autoStartContext: AutoStartContext) -> list[str]:
 			exc_info=True,
 		)
 	else:
-		k.Close()
 		if not conf[0]:
 			# "".split(",") returns [""], so remove the empty string.
 			del conf[0]
@@ -168,11 +167,11 @@ def setAutoStart(autoStartContext: AutoStartContext, enable: bool) -> None:
 		changed = True
 
 	if changed:
-		with winreg.OpenKey(
+		k = winreg.OpenKey(
 			autoStartContext.value,
 			_RegistryKey.EASE_OF_ACCESS.value,
 			access=winreg.KEY_READ | winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY,
-		) as k:
+		)
 		winreg.SetValueEx(
 			k,
 			"Configuration",

```