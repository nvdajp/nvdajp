# Diff for: `source\gui\jpBrailleViewer.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\gui\jpBrailleViewer.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\jpBrailleViewer.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\jpBrailleViewer.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\jpBrailleViewer.py"
index b3de5e2..51dd28a 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\jpBrailleViewer.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\jpBrailleViewer.py"
@@ -31,7 +31,9 @@ def __init__(self):
 
 	def onClose(self, evt):
 		deactivate()
-		if gui.mainFrame.sysTrayIcon and hasattr(gui.mainFrame.sysTrayIcon, 'menu_tools_toggleJpBrailleViewer'):
+		if gui.mainFrame.sysTrayIcon and hasattr(
+			gui.mainFrame.sysTrayIcon, "menu_tools_toggleJpBrailleViewer"
+		):
 			gui.mainFrame.sysTrayIcon.menu_tools_toggleJpBrailleViewer.Check(False)
 
 

```