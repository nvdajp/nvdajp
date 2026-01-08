# Diff for: `source\NVDAObjects\window\excel.py`

**Source**: `F:\nvda\gh\beta\source\NVDAObjects\window\excel.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\window\excel.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\window\\excel.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\window\\excel.py"
index 61f240c..d05ed8b 100644
--- "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\window\\excel.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\window\\excel.py"
@@ -1181,6 +1181,11 @@ def script_changeActiveCell(self, gesture: inputCore.InputGesture) -> None:
 			"kb:control+shift+8",
 			"kb:control+pageUp",
 			"kb:control+pageDown",
+			# BEGIN JP PATCH
+			# nvdajp: restore Shift+Control+PageUp/Down key bindings for Excel cell navigation
+			"kb:shift+control+pageUp",
+			"kb:shift+control+pageDown",
+			# END JP PATCH
 			"kb:control+a",
 			"kb:control+v",
 			"kb:shift+f11",
@@ -1462,7 +1467,7 @@ class NvCellState(enum.IntEnum):
 	NvCellState.HASPOPUP: controlTypes.State.HASPOPUP,
 	NvCellState.PROTECTED: controlTypes.State.PROTECTED,
 	NvCellState.HASFORMULA: controlTypes.State.HASFORMULA,
-	NvCellState.HASCOMMENT: controlTypes.State.HASNOTE,
+	NvCellState.HASCOMMENT: controlTypes.State.HASCOMMENT,
 	NvCellState.CROPPED: controlTypes.State.CROPPED,
 	NvCellState.OVERFLOWING: controlTypes.State.OVERFLOWING,
 	NvCellState.UNLOCKED: controlTypes.State.UNLOCKED,

```