# Diff for: `source\gui\addonStoreGui\viewModels\store.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\gui\addonStoreGui\viewModels\store.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\addonStoreGui\viewModels\store.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\addonStoreGui\\viewModels\\store.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\addonStoreGui\\viewModels\\store.py"
index 36c155f..6adc3f4 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\addonStoreGui\\viewModels\\store.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\addonStoreGui\\viewModels\\store.py"
@@ -17,6 +17,8 @@
 import threading
 
 import addonHandler
+from markdown import markdown
+import ui
 from addonStore.dataManager import addonDataManager
 from addonStore.install import installAddon
 from addonStore.models.addon import (
@@ -259,6 +261,36 @@ def _makeActionsList(self):
 				),
 				actionTarget=selectedListItem,
 			),
+			AddonActionVM(
+				# Translators: Label for an action that opens the VirusTotal scan results for the selected addon
+				displayName=pgettext("addonStore", "VirusTotal scan results"),
+				actionHandler=lambda aVM: startfile(cast(_AddonStoreModel, aVM.model).scanResults.scanUrl),
+				validCheck=lambda aVM: isinstance(aVM.model, _AddonStoreModel)
+				and aVM.model.scanResults is not None,
+				actionTarget=selectedListItem,
+			),
+			AddonActionVM(
+				# Translators: Label for an action that shows changelog for the selected addon
+				displayName=pgettext("addonStore", "&What's new"),
+				actionHandler=lambda aVM: ui.browseableMessage(
+					markdown(
+						str(
+							cast(_AddonStoreModel, aVM.model).changelog,
+						),
+					),
+					# Translators: Title for a message showing changes for the current add-on version.
+					title=pgettext("addonStore", "Changes for {curVersion}").format(
+						curVersion=aVM.model.addonVersionName,
+					),
+					isHtml=True,
+					copyButton=True,
+					closeButton=True,
+				),
+				validCheck=lambda aVM: (
+					isinstance(aVM.model, _AddonStoreModel) and aVM.model.changelog is not None
+				),
+				actionTarget=selectedListItem,
+			),
 		]
 
 	def helpAddon(self, listItemVM: AddonListItemVM) -> None:

```