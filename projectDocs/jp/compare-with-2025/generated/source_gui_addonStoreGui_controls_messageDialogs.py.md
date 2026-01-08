# Diff for: `source\gui\addonStoreGui\controls\messageDialogs.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\gui\addonStoreGui\controls\messageDialogs.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\addonStoreGui\controls\messageDialogs.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\addonStoreGui\\controls\\messageDialogs.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\addonStoreGui\\controls\\messageDialogs.py"
index f658a84..67300b5 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\addonStoreGui\\controls\\messageDialogs.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\addonStoreGui\\controls\\messageDialogs.py"
@@ -19,11 +19,10 @@
 	_AddonManifestModel,
 )
 from addonStore.dataManager import addonDataManager
-from addonStore.models.status import _StatusFilterKey, AvailableAddonStatus, getStatus
+from addonStore.models.status import _StatusFilterKey, getStatus
 import config
 from config.configFlags import AddonsAutomaticUpdate
 import gui
-from gui import nvdaControls
 from gui.addonGui import ConfirmAddonInstallDialog, ErrorAddonInstallDialog, promptUserForRestart
 from gui.addonStoreGui.viewModels.addonList import AddonListItemVM
 from gui.contextHelp import ContextHelpMixin
@@ -404,7 +403,7 @@ def _setupUI(self):
 		mainSizer.Add(sHelper.sizer, border=BORDER_FOR_DIALOGS, flag=wx.ALL)
 		self.Sizer = mainSizer
 		mainSizer.Fit(self)
-		self.CentreOnScreen()
+		self.CenterOnScreen()
 
 	def onCharHook(self, evt: wx.KeyEvent):
 		if evt.KeyCode == wx.WXK_ESCAPE:
@@ -445,41 +444,23 @@ def _setupButtons(self, sHelper: BoxSizerHelper):
 		closeButton.Bind(wx.EVT_BUTTON, self.onCloseButton)
 
 	def _createAddonsPanel(self, sHelper: BoxSizerHelper):
-		# Translators: the label for the addons list in the updatable addons dialog.
-		entriesLabel = pgettext("addonStore", "Updatable Add-ons")
-		self.addonsList = sHelper.addLabeledControl(
-			entriesLabel,
-			nvdaControls.AutoWidthColumnListCtrl,
-			style=wx.LC_REPORT | wx.LC_SINGLE_SEL,
-		)
+		from .actions import _MonoActionsContextMenu
+		from .addonList import AddonVirtualList
+		from gui.addonStoreGui.viewModels.store import AddonStoreVM
 
-		# Translators: Label for an extra detail field for an add-on. In the add-on store UX.
-		nameLabel = pgettext("addonStore", "Name")
-		# Translators: Label for an extra detail field for an add-on. In the add-on store UX.
-		installedVersionLabel = pgettext("addonStore", "Installed version")
-		# Translators: Label for an extra detail field for an add-on. In the add-on store UX.
-		availableVersionLabel = pgettext("addonStore", "Available version")
-		# Translators: Label for an extra detail field for an add-on. In the add-on store UX.
-		channelLabel = pgettext("addonStore", "Channel")
-		# Translators: Label for an extra detail field for an add-on. In the add-on store UX.
-		statusLabel = pgettext("addonStore", "Status")
-
-		self.addonsList.AppendColumn(nameLabel, width=300)
-		self.addonsList.AppendColumn(installedVersionLabel, width=200)
-		self.addonsList.AppendColumn(availableVersionLabel, width=200)
-		self.addonsList.AppendColumn(channelLabel, width=150)
-		self.addonsList.AppendColumn(statusLabel, width=300)
-		for addon in self.addonsPendingUpdate:
-			self.addonsList.Append(
-				(
-					addon.displayName,
-					addon._addonHandlerModel.version,
-					addon.addonVersionName,
-					addon.channel.displayString,
-					AvailableAddonStatus.UPDATE.displayString,
-				),
+		_storeVM = AddonStoreVM()
+		_storeVM._filteredStatusKey = _StatusFilterKey.UPDATE
+		_storeVM._filterIncludeIncompatible = config.conf["addonStore"]["allowIncompatibleUpdates"]
+		_storeVM.refresh()
+		self.addonsList = AddonVirtualList(
+			parent=self,
+			addonsListVM=_storeVM.listVM,
+			actionsContextMenu=_MonoActionsContextMenu(_storeVM),
 		)
+		self.addonsList.SetMinSize(self.addonsList.scaleSize((500, 100)))
+		self.SetMinSize(self.addonsList.scaleSize((500, 100)))
 		self.addonsList.Refresh()
+		sHelper.addItem(self.addonsList, proportion=1)
 
 	def onOpenStoreButton(self, evt: wx.CommandEvent):
 		"""Open the Add-on Store to update add-ons"""
@@ -590,6 +571,8 @@ def delayCreateDialog():
 				wx.CallAfter(delayCreateDialog)
 
 			case AddonsAutomaticUpdate.UPDATE:
+				# Translators: Message shown when updating add-ons automatically
+				wx.CallAfter(ui.message, pgettext("addonStore", "Updating add-ons..."), SpeechPriority.NEXT)
 				threading.Thread(
 					name="AutomaticAddonUpdate",
 					target=_updateAddons,
@@ -609,8 +592,6 @@ def _updateAddons(addonsPendingUpdate: list[_AddonGUIModel]):
 	"""
 	from ..viewModels.store import AddonStoreVM
 
-	# Translators: Message shown when updating add-ons automatically
-	ui.message(pgettext("addonStore", "Updating add-ons..."), SpeechPriority.NEXT)
 	listVMs = {AddonListItemVM(a, status=getStatus(a, _StatusFilterKey.UPDATE)) for a in addonsPendingUpdate}
 	AddonStoreVM.getAddons(
 		listVMs,

```