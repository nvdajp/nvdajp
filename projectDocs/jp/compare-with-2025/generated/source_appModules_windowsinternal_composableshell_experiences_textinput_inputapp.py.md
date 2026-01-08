# Diff for: `source\appModules\windowsinternal_composableshell_experiences_textinput_inputapp.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\appModules\windowsinternal_composableshell_experiences_textinput_inputapp.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\appModules\windowsinternal_composableshell_experiences_textinput_inputapp.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModules\\windowsinternal_composableshell_experiences_textinput_inputapp.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\windowsinternal_composableshell_experiences_textinput_inputapp.py"
index d77b87d..889ec45 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModules\\windowsinternal_composableshell_experiences_textinput_inputapp.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\windowsinternal_composableshell_experiences_textinput_inputapp.py"
@@ -449,8 +449,10 @@ def event_NVDAObject_init(self, obj: NVDAObject) -> None:
 			obj._shouldAllowUIALiveRegionChangeEvent = False
 
 
+# BEGIN JP PATCH
 if config.conf["keyboard"]["nvdajpEnableKeyEvents"]:
 	if winVersion.getWinVer() >= winVersion.WIN11:
 		from .windowsinternal_composableshell_experiences_textinput_inputapp_jp import AppModule  # noqa: F401
 	else:
 		from .windowsinternal_composableshell_experiences_textinput_inputapp_jp_win10 import AppModule  # noqa: F401
+# END JP PATCH

```