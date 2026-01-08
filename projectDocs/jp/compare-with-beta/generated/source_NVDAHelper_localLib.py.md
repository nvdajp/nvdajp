# Diff for: `source\NVDAHelper\localLib.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\NVDAHelper\localLib.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAHelper\localLib.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\NVDAHelper\\localLib.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAHelper\\localLib.py"
index 9c55b8b..7b56faa 100644
--- "a/F:\\nvda\\gh\\beta\\source\\NVDAHelper\\localLib.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAHelper\\localLib.py"
@@ -666,7 +666,7 @@ class EXCEL_CELLINFO(Structure):
 )
 
 isScreenFullyBlack = dll.isScreenFullyBlack
-isScreenFullyBlack.argtypes = ()
+isScreenFullyBlack.argtypes = tuple()
 isScreenFullyBlack.restype = c_bool
 
 localListeningSocketExists = dll.localListeningSocketExists

```