# Diff for: `source\appModules\windowsinternal_composableshell_experiences_textinput_inputapp.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\appModules\windowsinternal_composableshell_experiences_textinput_inputapp.py`  
**Current**: `F:\nvda\gh\alphajp\source\appModules\windowsinternal_composableshell_experiences_textinput_inputapp.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModules\\windowsinternal_composableshell_experiences_textinput_inputapp.py" "b/F:\\nvda\\gh\\alphajp\\source\\appModules\\windowsinternal_composableshell_experiences_textinput_inputapp.py"
index d77b87d04d..0416fc267b 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModules\\windowsinternal_composableshell_experiences_textinput_inputapp.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\appModules\\windowsinternal_composableshell_experiences_textinput_inputapp.py"
@@ -447,10 +447,3 @@ def event_NVDAObject_init(self, obj: NVDAObject) -> None:
 			controlTypes.Role.LIST,  # Clipboard history item actions list
 		):
 			obj._shouldAllowUIALiveRegionChangeEvent = False
-
-
-if config.conf["keyboard"]["nvdajpEnableKeyEvents"]:
-	if winVersion.getWinVer() >= winVersion.WIN11:
-		from .windowsinternal_composableshell_experiences_textinput_inputapp_jp import AppModule  # noqa: F401
-	else:
-		from .windowsinternal_composableshell_experiences_textinput_inputapp_jp_win10 import AppModule  # noqa: F401

```