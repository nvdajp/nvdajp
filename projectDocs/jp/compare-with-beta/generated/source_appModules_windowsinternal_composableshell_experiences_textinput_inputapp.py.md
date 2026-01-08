# Diff for: `source\appModules\windowsinternal_composableshell_experiences_textinput_inputapp.py`

**Source**: `F:\nvda\gh\beta\source\appModules\windowsinternal_composableshell_experiences_textinput_inputapp.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\appModules\windowsinternal_composableshell_experiences_textinput_inputapp.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\appModules\\windowsinternal_composableshell_experiences_textinput_inputapp.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\windowsinternal_composableshell_experiences_textinput_inputapp.py"
index 0416fc2..889ec45 100644
--- "a/F:\\nvda\\gh\\beta\\source\\appModules\\windowsinternal_composableshell_experiences_textinput_inputapp.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\windowsinternal_composableshell_experiences_textinput_inputapp.py"
@@ -447,3 +447,12 @@ def event_NVDAObject_init(self, obj: NVDAObject) -> None:
 			controlTypes.Role.LIST,  # Clipboard history item actions list
 		):
 			obj._shouldAllowUIALiveRegionChangeEvent = False
+
+
+# BEGIN JP PATCH
+if config.conf["keyboard"]["nvdajpEnableKeyEvents"]:
+	if winVersion.getWinVer() >= winVersion.WIN11:
+		from .windowsinternal_composableshell_experiences_textinput_inputapp_jp import AppModule  # noqa: F401
+	else:
+		from .windowsinternal_composableshell_experiences_textinput_inputapp_jp_win10 import AppModule  # noqa: F401
+# END JP PATCH

```