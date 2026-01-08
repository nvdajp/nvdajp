# Diff for: `source\NVDAObjects\window\scintilla.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\window\scintilla.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\window\scintilla.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\window\\scintilla.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\window\\scintilla.py"
index 31ccf59..4a7f7b2 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\window\\scintilla.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\window\\scintilla.py"
@@ -6,6 +6,7 @@
 # See the file COPYING for more details.
 
 import ctypes
+import textInfos
 import textInfos.offsets
 import winKernel
 import winUser
@@ -313,6 +314,8 @@ def _getCharacterOffsets(self, offset):
 				tempOffset -= 1
 		return [start, end]
 
+	# BEGIN JP PATCH
+	# nvdajp: Fix for issue #17430 - Notepad++ braille line navigation
 	def collapse(self, end: bool = False):
 		"""Before collapsing to end, if no text is selected, TextInfo is expanded to line.
 		This fixes a bug where next braille line command didn't move the cursor to the last empty line
@@ -323,6 +326,8 @@ def collapse(self, end: bool = False):
 			self.expand(textInfos.UNIT_LINE)
 		super().collapse(end=end)
 
+	# END JP PATCH
+
 
 # The Scintilla NVDA object, inherists the generic MSAA NVDA object
 class Scintilla(EditableTextWithAutoSelectDetection, Window):

```