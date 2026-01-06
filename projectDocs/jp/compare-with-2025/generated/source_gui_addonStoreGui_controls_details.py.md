# Diff for: `source\gui\addonStoreGui\controls\details.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\gui\addonStoreGui\controls\details.py`  
**Current**: `F:\nvda\gh\alphajp\source\gui\addonStoreGui\controls\details.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\addonStoreGui\\controls\\details.py" "b/F:\\nvda\\gh\\alphajp\\source\\gui\\addonStoreGui\\controls\\details.py"
index 51cd152f08..c0bced3f43 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\addonStoreGui\\controls\\details.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\gui\\addonStoreGui\\controls\\details.py"
@@ -265,7 +265,10 @@ def _refresh(self):
 				)
 
 				currentStatusKey = self._actionsContextMenu._storeVM._filteredStatusKey
-				if currentStatusKey not in AddonListField.currentAddonVersionName.hideStatuses:
+				if (
+					currentStatusKey not in AddonListField.currentAddonVersionName.hideStatuses
+					and details._addonHandlerModel is not None
+				):
 					self._appendDetailsLabelValue(
 						# Translators: Label for an extra detail field for the selected add-on. In the add-on store dialog.
 						pgettext("addonStore", "Installed version:"),

```