# Diff for: `source\gui\nvdaControls.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\gui\nvdaControls.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\nvdaControls.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\nvdaControls.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\nvdaControls.py"
index a43d044..bd3524e 100644
--- "a/F:\\nvda\\gh\\beta\\source\\gui\\nvdaControls.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\nvdaControls.py"
@@ -14,6 +14,7 @@
 import warnings
 
 import wx
+from wx.lib import scrolledpanel
 from wx.lib.mixins import listctrl as listmix
 
 import config
@@ -42,6 +43,7 @@
 	"MessageDialog",
 	"_ContinueCancelDialog",
 	"EnhancedInputSlider",
+	"TabbableScrolledPanel",
 	"FeatureFlagCombo",
 ]
 
@@ -432,6 +434,44 @@ def onSliderChar(self, evt):
 		self.SetValue(newValue)
 
 
+class TabbableScrolledPanel(scrolledpanel.ScrolledPanel):
+	"""
+	This class was created to ensure a ScrolledPanel scrolls to nested children of the panel when navigating
+	with tabs (#12224). A PR to wxPython implementing this fix can be tracked on
+	https://github.com/wxWidgets/Phoenix/pull/1950
+	"""
+
+	def GetChildRectRelativeToSelf(self, child: wx.Window) -> wx.Rect:
+		"""
+		window.GetRect returns the size of a window, and its position relative to its parent.
+		When calculating ScrollChildIntoView, the position relative to its parent is not relevant unless the
+		parent is the ScrolledPanel itself. Instead, calculate the position relative to scrolledPanel
+		"""
+		childRectRelativeToScreen = child.GetScreenRect()
+		scrolledPanelScreenPosition = self.GetScreenPosition()
+		return wx.Rect(
+			childRectRelativeToScreen.x - scrolledPanelScreenPosition.x,
+			childRectRelativeToScreen.y - scrolledPanelScreenPosition.y,
+			childRectRelativeToScreen.width,
+			childRectRelativeToScreen.height,
+		)
+
+	def ScrollChildIntoView(self, child: wx.Window) -> None:
+		"""
+		Overrides child.GetRect with `GetChildRectRelativeToSelf` before calling
+		`super().ScrollChildIntoView`. `super().ScrollChildIntoView` incorrectly uses child.GetRect to
+		navigate scrolling, which is relative to the parent, where it should instead be relative to this
+		ScrolledPanel.
+		"""
+		oldChildGetRectFunction = child.GetRect
+		child.GetRect = lambda: self.GetChildRectRelativeToSelf(child)
+		try:
+			super().ScrollChildIntoView(child)
+		finally:
+			# ensure child.GetRect is reset properly even if super().ScrollChildIntoView throws an exception
+			child.GetRect = oldChildGetRectFunction
+
+
 class FeatureFlagCombo(wx.Choice):
 	"""Creates a combobox (wx.Choice) with a list of feature flags."""
 

```