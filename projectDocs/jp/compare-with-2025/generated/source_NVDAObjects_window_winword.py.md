# Diff for: `source\NVDAObjects\window\winword.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\window\winword.py`  
**Current**: `F:\nvda\gh\alphajp\source\NVDAObjects\window\winword.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\window\\winword.py" "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\window\\winword.py"
index b61ffd7aad..1fd074d93c 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\window\\winword.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\window\\winword.py"
@@ -28,6 +28,7 @@
 import NVDAHelper
 import XMLFormatting
 from logHandler import log
+from winBindings import user32
 import winUser
 import oleacc
 import speech
@@ -471,7 +472,7 @@ class WinWordColor(IntEnum):
 
 winwordWindowIid = GUID("{00020962-0000-0000-C000-000000000046}")
 
-wm_winword_expandToLine = ctypes.windll.user32.RegisterWindowMessageW("wm_winword_expandToLine")
+wm_winword_expandToLine = user32.RegisterWindowMessage("wm_winword_expandToLine")
 
 NVDAUnitsToWordUnits = {
 	textInfos.UNIT_CHARACTER: wdCharacter,

```