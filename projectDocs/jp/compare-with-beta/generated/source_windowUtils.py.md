# Diff for: `source\windowUtils.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\windowUtils.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\windowUtils.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\windowUtils.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\windowUtils.py"
index 59f5cd5..31f7e6e 100644
--- "a/F:\\nvda\\gh\\beta\\source\\windowUtils.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\windowUtils.py"
@@ -16,7 +16,7 @@
 import winBindings.user32
 import winBindings.gdi32
 import winUser
-from winBindings.user32 import WNDCLASSEXW, WNDPROC
+from winUser import WNDCLASSEXW, WNDPROC
 from logHandler import log
 from abc import abstractmethod
 from baseObject import AutoPropertyObject

```