# Diff for: `source\speechViewer.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\speechViewer.py`  
**Current**: `F:\nvda\gh\alphajp\source\speechViewer.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\speechViewer.py" "b/F:\\nvda\\gh\\alphajp\\source\\speechViewer.py"
index f746e40896..e4a6286043 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\speechViewer.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\speechViewer.py"
@@ -63,7 +63,6 @@ def __init__(self, onDestroyCallBack: Callable[[], None]):
 
 		self._createControls(sizer=self.panelContentsSizer, parent=self.panel)
 
-		self.SetTransparent(229)  # int(255.0 * 0.90)
 		# Don't let speech viewer to steal keyboard focus when opened
 		self.ShowWithoutActivating()
 
@@ -106,7 +105,6 @@ def _createControls(self, sizer, parent):
 		)
 		if isLockScreenModeActive():
 			self.shouldShowOnStartupCheckBox.Disable()
-		self.SetTransparent(229)  # int(255.0 * 0.90)
 
 	def _onDialogActivated(self, evt):
 		# Check for destruction, if the speechviewer window has focus when we exit NVDA it regains focus briefly

```