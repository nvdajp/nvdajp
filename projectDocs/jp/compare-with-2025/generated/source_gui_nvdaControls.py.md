# Diff for: `source\gui\nvdaControls.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\gui\nvdaControls.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\nvdaControls.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\nvdaControls.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\nvdaControls.py"
index 4adf94d..a43d044 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\nvdaControls.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\nvdaControls.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2016-2024 NV Access Limited, Derek Riemer, Cyrille Bougot, Luke Davis, Leonard de Ruijter
+# Copyright (C) 2016-2025 NV Access Limited, Derek Riemer, Cyrille Bougot, Luke Davis, Leonard de Ruijter
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -14,7 +14,6 @@
 import warnings
 
 import wx
-from wx.lib import scrolledpanel
 from wx.lib.mixins import listctrl as listmix
 
 import config
@@ -23,6 +22,7 @@
 	FlagValueEnum as FeatureFlagEnumT,
 )
 import gui.message
+from winBindings import user32
 from .dpiScalingHelper import DpiScalingHelperMixin
 from . import (
 	guiHelper,
@@ -42,7 +42,6 @@
 	"MessageDialog",
 	"_ContinueCancelDialog",
 	"EnhancedInputSlider",
-	"TabbableScrolledPanel",
 	"FeatureFlagCombo",
 ]
 
@@ -406,7 +405,7 @@ def SetValue(self, i):
 		# HACK: Win events don't seem to be sent for certain explicitly set values,
 		# so send our own win event.
 		# This will cause duplicates in some cases, but NVDA will filter them out.
-		winUser.user32.NotifyWinEvent(
+		user32.NotifyWinEvent(
 			winUser.EVENT_OBJECT_VALUECHANGE,
 			self.Handle,
 			winUser.OBJID_CLIENT,
@@ -433,44 +432,6 @@ def onSliderChar(self, evt):
 		self.SetValue(newValue)
 
 
-class TabbableScrolledPanel(scrolledpanel.ScrolledPanel):
-	"""
-	This class was created to ensure a ScrolledPanel scrolls to nested children of the panel when navigating
-	with tabs (#12224). A PR to wxPython implementing this fix can be tracked on
-	https://github.com/wxWidgets/Phoenix/pull/1950
-	"""
-
-	def GetChildRectRelativeToSelf(self, child: wx.Window) -> wx.Rect:
-		"""
-		window.GetRect returns the size of a window, and its position relative to its parent.
-		When calculating ScrollChildIntoView, the position relative to its parent is not relevant unless the
-		parent is the ScrolledPanel itself. Instead, calculate the position relative to scrolledPanel
-		"""
-		childRectRelativeToScreen = child.GetScreenRect()
-		scrolledPanelScreenPosition = self.GetScreenPosition()
-		return wx.Rect(
-			childRectRelativeToScreen.x - scrolledPanelScreenPosition.x,
-			childRectRelativeToScreen.y - scrolledPanelScreenPosition.y,
-			childRectRelativeToScreen.width,
-			childRectRelativeToScreen.height,
-		)
-
-	def ScrollChildIntoView(self, child: wx.Window) -> None:
-		"""
-		Overrides child.GetRect with `GetChildRectRelativeToSelf` before calling
-		`super().ScrollChildIntoView`. `super().ScrollChildIntoView` incorrectly uses child.GetRect to
-		navigate scrolling, which is relative to the parent, where it should instead be relative to this
-		ScrolledPanel.
-		"""
-		oldChildGetRectFunction = child.GetRect
-		child.GetRect = lambda: self.GetChildRectRelativeToSelf(child)
-		try:
-			super().ScrollChildIntoView(child)
-		finally:
-			# ensure child.GetRect is reset properly even if super().ScrollChildIntoView throws an exception
-			child.GetRect = oldChildGetRectFunction
-
-
 class FeatureFlagCombo(wx.Choice):
 	"""Creates a combobox (wx.Choice) with a list of feature flags."""
 

```