# Diff for: `source\gui\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\gui\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\__init__.py"
index 3ba58a5..4882b02 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\__init__.py"
@@ -1,4 +1,3 @@
-# -*- coding: UTF-8 -*-
 # A part of NonVisual Desktop Access (NVDA)
 # Copyright (C) 2006-2025 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Mesar Hameed, Joseph Lee,
 # Thomas Stivers, Babbage B.V., Accessolutions, Julien Cochuyt, Cyrille Bougot, Luke Davis
@@ -8,29 +7,28 @@
 
 from collections.abc import Callable
 import os
-import ctypes
 import warnings
 import wx
 import wx.adv
 import wx.lib.agw.persist
 
+import winBindings.kernel32
 import globalVars
 import tones
 import ui
 from documentationUtils import getDocFilePath, displayLicense, reportNoDocumentation
 from logHandler import log
 import config
+import buildVersion
 import versionInfo
 import speech
 import queueHandler
 import core
-from typing import (
-	Any,
-	Optional,
-	Type,
-)
+from typing import Any
 import systemUtils
 from .message import (
+	Button,
+	Payload,
 	# messageBox is accessed through `gui.messageBox` as opposed to `gui.message.messageBox` throughout NVDA,
 	# be cautious when removing
 	messageBox,
@@ -57,9 +55,10 @@
 	BrowseModePanel,
 	DocumentFormattingPanel,
 	GeneralSettingsPanel,
-	LanguageSettingsPanel,
 	InputCompositionPanel,
 	KeyboardSettingsPanel,
+	LanguageSettingsPanel,  # nvdajp
+	LocalCaptionerSettingsPanel,
 	MouseSettingsPanel,
 	MultiCategorySettingsDialog,
 	NVDASettingsDialog,
@@ -99,15 +98,6 @@ def quit():
 	updateCheck = None
 
 from . import jpBrailleViewer  # nvdajp
-import subprocess  # nvdajp
-
-
-def run_hta(hta_file_path: str) -> None:
-	SYSTEM_ROOT = os.path.expandvars("%SYSTEMROOT%")
-	SYSTEM32 = os.path.join(SYSTEM_ROOT, "System32")
-	MSHTA_PATH = os.path.join(SYSTEM32, "mshta.exe")
-	subprocess.Popen([MSHTA_PATH, hta_file_path])
-
 
 ### Constants
 NVDA_PATH = globalVars.appDir
@@ -117,7 +107,7 @@ def run_hta(hta_file_path: str) -> None:
 DONATE_URL = "https://www.nvda.jp/donate.html"
 
 ### Globals
-mainFrame: Optional["MainFrame"] = None
+mainFrame: "MainFrame | None" = None
 """Set by initialize. Should be used as the parent for "top level" dialogs.
 """
 
@@ -159,7 +149,7 @@ class MainFrame(wx.Frame):
 
 	def __init__(self):
 		style = wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX ^ wx.MINIMIZE_BOX | wx.FRAME_NO_TASKBAR
-		super(MainFrame, self).__init__(None, wx.ID_ANY, versionInfo.name, size=(1, 1), style=style)
+		super().__init__(None, wx.ID_ANY, buildVersion.name, size=(1, 1), style=style)
 		self.Bind(wx.EVT_CLOSE, self.onExitCommand)
 		self.sysTrayIcon = SysTrayIcon(self)
 		#: The focus before the last popup or C{None} if unknown.
@@ -264,7 +254,7 @@ def onSaveConfigurationCommand(self, evt):
 			)
 
 	@blockAction.when(blockAction.Context.MODAL_DIALOG_OPEN)
-	def popupSettingsDialog(self, dialog: Type[SettingsDialog], *args, **kwargs):
+	def popupSettingsDialog(self, dialog: type[SettingsDialog], *args, **kwargs):
 		self.prePopup()
 		try:
 			dialog(self, *args, **kwargs).Show()
@@ -284,7 +274,7 @@ def popupSettingsDialog(self, dialog: Type[SettingsDialog], *args, **kwargs):
 
 	if NVDAState._allowDeprecatedAPI():
 
-		def _popupSettingsDialog(self, dialog: Type[SettingsDialog], *args, **kwargs):
+		def _popupSettingsDialog(self, dialog: type[SettingsDialog], *args, **kwargs):
 			log.warning(
 				"_popupSettingsDialog is deprecated, use popupSettingsDialog instead.",
 				stack_info=True,
@@ -404,6 +394,10 @@ def onUwpOcrCommand(self, evt):
 	def onRemoteAccessSettingsCommand(self, evt):
 		self.popupSettingsDialog(NVDASettingsDialog, RemoteSettingsPanel)
 
+	@blockAction.when(blockAction.Context.SECURE_MODE)
+	def onLocalCaptionerSettingsCommand(self, evt):
+		self.popupSettingsDialog(NVDASettingsDialog, LocalCaptionerSettingsPanel)
+
 	@blockAction.when(blockAction.Context.SECURE_MODE)
 	def onAdvancedSettingsCommand(self, evt: wx.CommandEvent):
 		self.popupSettingsDialog(NVDASettingsDialog, AdvancedPanel)
@@ -416,9 +410,26 @@ def onSpeechSymbolsCommand(self, evt):
 	def onInputGesturesCommand(self, evt):
 		self.popupSettingsDialog(InputGesturesDialog)
 
-	def onAboutCommand(self, evt):
+	@staticmethod
+	def _copyVersionToClipboard(p: Payload):
+		versionStr = f"{versionInfo.version} ({versionInfo.version_detailed})"
+		api.copyToClip(versionStr)
+		# Translators: A message when the version number is copied to clipboard
+		# from the about dialog
+		ui.message(_("Copied to clipboard"))
+
+	def onAboutCommand(self, evt: wx.CommandEvent):
+		copyButton = Button(
+			id=wx.ID_COPY,
+			# Translators: The label for a button to copy the NVDA version number from the about dialog.
+			label=_("&Copy version number"),
+			callback=self._copyVersionToClipboard,
+			closesDialog=False,
+		)
 		# Translators: The title of the dialog to show about info for NVDA.
-		MessageDialog(None, versionInfo.aboutMessage, _("About NVDA")).Show()
+		aboutDialog = MessageDialog(None, versionInfo.aboutMessage, _("About NVDA"))
+		aboutDialog.addButton(copyButton)
+		aboutDialog.Show()
 
 	@blockAction.when(blockAction.Context.SECURE_MODE)
 	def onCheckForUpdateCommand(self, evt):
@@ -530,7 +541,7 @@ def onCreatePortableCopyCommand(self, evt):
 		self.prePopup()
 		from . import installerGui
 
-		d = installerGui.PortableCreaterDialog(mainFrame)
+		d = installerGui.PortableCreaterDialog(self)
 		d.Show()
 		self.postPopup()
 
@@ -643,7 +654,7 @@ class SysTrayIcon(wx.adv.TaskBarIcon):
 	def __init__(self, frame: MainFrame):
 		super(SysTrayIcon, self).__init__()
 		icon = wx.Icon(ICON_PATH, wx.BITMAP_TYPE_ICO)
-		self.SetIcon(icon, versionInfo.name)
+		self.SetIcon(icon, buildVersion.name)
 
 		self.menu = wx.Menu()
 		menu_preferences = self.preferencesMenu = wx.Menu()
@@ -871,10 +882,10 @@ def _appendHelpSubMenu(self, frame: MainFrame) -> None:
 			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(versionInfo.url), item)
 			# Translators: The label for the menu item to view the NVDA website's get help section
 			item = self.helpMenu.Append(wx.ID_ANY, _("&Help, training and support"))
-			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(f"{versionInfo.url}/get-help/"), item)
+			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(f"{buildVersion.url}/get-help/"), item)
 			# Translators: The label for the menu item to view the NVDA website's get help section
 			item = self.helpMenu.Append(wx.ID_ANY, _("NV Access &shop"))
-			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(f"{versionInfo.url}/shop/"), item)
+			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(f"{buildVersion.url}/shop/"), item)
 
 			self.helpMenu.AppendSeparator()
 
@@ -903,9 +914,6 @@ def _openDocumentationFile(self, fileName: str) -> None:
 		if helpFile is None:
 			reportNoDocumentation(fileName, useMsgBox=True)
 			return
-		if config.conf["language"]["openDocFileByMSHTA"]:
-			run_hta(helpFile)
-			return
 		os.startfile(helpFile)
 
 	def _appendPendingUpdateSection(self, frame: MainFrame) -> None:
@@ -1025,7 +1033,7 @@ def shouldConfigProfileTriggersBeSuspended():
 	Top-level windows that require this behavior should have a C{shouldSuspendConfigProfileTriggers} attribute set to C{True}.
 	Because these dialogs are often opened via the NVDA menu, this applies to the NVDA menu as well.
 	"""
-	if winUser.getGUIThreadInfo(ctypes.windll.kernel32.GetCurrentThreadId()).flags & 0x00000010:
+	if winUser.getGUIThreadInfo(winBindings.kernel32.GetCurrentThreadId()).flags & 0x00000010:
 		# The NVDA menu is active.
 		return True
 	for window in wx.GetTopLevelWindows():

```