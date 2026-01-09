# Diff for: `source\winUser.py`

**Source**: `F:\nvda\gh\beta\source\winUser.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winUser.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winUser.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winUser.py"
index 17ae727..583663e 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winUser.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winUser.py"
@@ -275,7 +275,15 @@ class NMHdrStruct(Structure):
 VK_MENU = 18
 VK_PAUSE = 19
 VK_CAPITAL = 20
+# BEGIN JP PATCH
+# nvdajp: IME ON/OFF virtual key codes for Japanese IME support
+VK_IME_ON = 0x16
+# END JP PATCH
 VK_FINAL = 0x18
+# BEGIN JP PATCH
+# nvdajp: IME OFF virtual key code
+VK_IME_OFF = 0x1A
+# END JP PATCH
 VK_ESCAPE = 0x1B
 VK_CONVERT = 0x1C
 VK_NONCONVERT = 0x1D

```