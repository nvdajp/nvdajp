# Diff for: `source\speechViewer.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\speechViewer.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\speechViewer.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\speechViewer.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\speechViewer.py"
index f746e40..38c0d1a 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\speechViewer.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\speechViewer.py"
@@ -63,7 +63,10 @@ def __init__(self, onDestroyCallBack: Callable[[], None]):
 
 		self._createControls(sizer=self.panelContentsSizer, parent=self.panel)
 
+		# BEGIN JP PATCH
+		# nvdajp: set window transparency (90% opacity)
 		self.SetTransparent(229)  # int(255.0 * 0.90)
+		# END JP PATCH
 		# Don't let speech viewer to steal keyboard focus when opened
 		self.ShowWithoutActivating()
 
@@ -106,7 +109,10 @@ def _createControls(self, sizer, parent):
 		)
 		if isLockScreenModeActive():
 			self.shouldShowOnStartupCheckBox.Disable()
+		# BEGIN JP PATCH
+		# nvdajp: set window transparency (90% opacity)
 		self.SetTransparent(229)  # int(255.0 * 0.90)
+		# END JP PATCH
 
 	def _onDialogActivated(self, evt):
 		# Check for destruction, if the speechviewer window has focus when we exit NVDA it regains focus briefly

```