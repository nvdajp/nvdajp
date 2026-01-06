# Diff for: `source\NVDAObjects\window\scintilla.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\window\scintilla.py`  
**Current**: `F:\nvda\gh\alphajp\source\NVDAObjects\window\scintilla.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\window\\scintilla.py" "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\window\\scintilla.py"
index 31ccf59045..5b7f694962 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\window\\scintilla.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\window\\scintilla.py"
@@ -313,16 +313,6 @@ def _getCharacterOffsets(self, offset):
 				tempOffset -= 1
 		return [start, end]
 
-	def collapse(self, end: bool = False):
-		"""Before collapsing to end, if no text is selected, TextInfo is expanded to line.
-		This fixes a bug where next braille line command didn't move the cursor to the last empty line
-		in Notepad++ documents.
-		https://github.com/nvaccess/nvda/issues/17430
-		"""
-		if end and self.obj.makeTextInfo(textInfos.POSITION_SELECTION).isCollapsed:
-			self.expand(textInfos.UNIT_LINE)
-		super().collapse(end=end)
-
 
 # The Scintilla NVDA object, inherists the generic MSAA NVDA object
 class Scintilla(EditableTextWithAutoSelectDetection, Window):

```