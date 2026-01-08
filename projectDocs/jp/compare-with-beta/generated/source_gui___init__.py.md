# Diff for: `source\gui\__init__.py`

**Source**: `F:\nvda\gh\beta\source\gui\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\__init__.py"
index 5391ccc..9a91800 100644
--- "a/F:\\nvda\\gh\\beta\\source\\gui\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\__init__.py"
@@ -3,6 +3,7 @@
 # Thomas Stivers, Babbage B.V., Accessolutions, Julien Cochuyt, Cyrille Bougot, Luke Davis
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
+# nvdajp modification by Takuya Nishimoto, Masataka.Shinke
 
 from collections.abc import Callable
 import os
@@ -56,6 +57,7 @@
 	GeneralSettingsPanel,
 	InputCompositionPanel,
 	KeyboardSettingsPanel,
+	LanguageSettingsPanel,  # nvdajp
 	LocalCaptionerSettingsPanel,
 	MouseSettingsPanel,
 	MultiCategorySettingsDialog,
@@ -96,10 +98,14 @@ def quit():
 except RuntimeError:
 	updateCheck = None
 
+from . import jpBrailleViewer  # nvdajp
+
 ### Constants
 NVDA_PATH = globalVars.appDir
-ICON_PATH = os.path.join(NVDA_PATH, "images", "nvda.ico")
-DONATE_URL = f"{buildVersion.url}/donate/"
+# ICON_PATH=os.path.join(NVDA_PATH, "images", "nvda.ico")
+ICON_PATH = os.path.join(NVDA_PATH, "images", "nvdajp3.ico")
+# DONATE_URL = f"{versionInfo.url}/donate/"
+DONATE_URL = "https://www.nvda.jp/donate.html"
 
 ### Globals
 mainFrame: "MainFrame | None" = None
@@ -332,6 +338,10 @@ def onNVDASettingsCommand(self, evt):
 	def onGeneralSettingsCommand(self, evt):
 		self.popupSettingsDialog(NVDASettingsDialog, GeneralSettingsPanel)
 
+	# nvdajp
+	def onLanguageSettingsCommand(self, evt):
+		self._popupSettingsDialog(NVDASettingsDialog, LanguageSettingsPanel)
+
 	def onSelectSynthesizerCommand(self, evt):
 		self.popupSettingsDialog(SynthesizerSelectionDialog)
 
@@ -515,6 +525,18 @@ def onReloadPluginsCommand(self, evt):
 		globalPluginHandler.reloadGlobalPlugins()
 		NVDAObject.clearDynamicClassCache()
 
+	# nvdajp begin
+	@blockAction.when(blockAction.Context.SECURE_MODE)
+	def onToggleJpBrailleViewerCommand(self, evt):
+		if not jpBrailleViewer.isActive:
+			jpBrailleViewer.activate()
+			self.sysTrayIcon.menu_tools_toggleJpBrailleViewer.Check(True)
+		else:
+			jpBrailleViewer.deactivate()
+			self.sysTrayIcon.menu_tools_toggleJpBrailleViewer.Check(False)
+
+	# nvdajp end
+
 	@blockAction.when(
 		blockAction.Context.SECURE_MODE,
 		blockAction.Context.MODAL_DIALOG_OPEN,
@@ -523,7 +545,7 @@ def onCreatePortableCopyCommand(self, evt):
 		self.prePopup()
 		from . import installerGui
 
-		d = installerGui.PortableCreaterDialog(mainFrame)
+		d = installerGui.PortableCreaterDialog(self)
 		d.Show()
 		self.postPopup()
 
@@ -712,6 +734,15 @@ def __init__(self, frame: MainFrame):
 			# Translators: The label for the menu item to reload plugins.
 			item = menu_tools.Append(wx.ID_ANY, _("Reload plugins"))
 			self.Bind(wx.EVT_MENU, frame.onReloadPluginsCommand, item)
+		# nvdajp begin
+		if not globalVars.appArgs.secure:
+			item = self.menu_tools_toggleJpBrailleViewer = menu_tools.AppendCheckItem(
+				wx.ID_ANY,
+				# Translators: The label for the menu item to open jp braille viewer.
+				_("Japanese Braille viewer"),
+			)
+			self.Bind(wx.EVT_MENU, frame.onToggleJpBrailleViewerCommand, item)
+		# nvdajp end
 		# Translators: The label for the Tools submenu in NVDA menu.
 		self.menu.AppendSubMenu(menu_tools, _("&Tools"))
 
@@ -832,6 +863,9 @@ def _appendHelpSubMenu(self, frame: MainFrame) -> None:
 		self.helpMenu = wx.Menu()
 
 		if not globalVars.appArgs.secure:
+			# Translators: The label for the menu item to open jp readme.
+			item = self.helpMenu.Append(wx.ID_ANY, _("&Readme (nvdajp)"))
+			self.Bind(wx.EVT_MENU, lambda evt: self._openDocumentationFile("readmejp.html"), item)
 			# Translators: The label of a menu item to open NVDA user guide.
 			item = self.helpMenu.Append(wx.ID_ANY, _("&User Guide"))
 			self.Bind(wx.EVT_MENU, lambda evt: self._openDocumentationFile("userGuide.html"), item)
@@ -844,9 +878,12 @@ def _appendHelpSubMenu(self, frame: MainFrame) -> None:
 
 			self.helpMenu.AppendSeparator()
 
+			# Translators: The label for the menu item to view the NVDA Japanese Team
+			item = self.helpMenu.Append(wx.ID_ANY, _("NVDAJP web site"))
+			self.Bind(wx.EVT_MENU, lambda evt: os.startfile("https://www.nvda.jp/"), item)
 			# Translators: The label for the menu item to view the NVDA website
 			item = self.helpMenu.Append(wx.ID_ANY, _("NV Access &web site"))
-			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(buildVersion.url), item)
+			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(versionInfo.url), item)
 			# Translators: The label for the menu item to view the NVDA website's get help section
 			item = self.helpMenu.Append(wx.ID_ANY, _("&Help, training and support"))
 			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(f"{buildVersion.url}/get-help/"), item)

```