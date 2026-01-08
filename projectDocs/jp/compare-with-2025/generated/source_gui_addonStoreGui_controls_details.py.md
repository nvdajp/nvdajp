# Diff for: `source\gui\addonStoreGui\controls\details.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\gui\addonStoreGui\controls\details.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\addonStoreGui\controls\details.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\addonStoreGui\\controls\\details.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\addonStoreGui\\controls\\details.py"
index 51cd152..c42a5f8 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\addonStoreGui\\controls\\details.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\addonStoreGui\\controls\\details.py"
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
@@ -359,6 +362,33 @@ def _refresh(self):
 							pgettext("addonStore", "Publication date:"),
 							details.publicationDate,
 						)
+
+				if isinstance(details, _AddonStoreModel):
+					if details.scanResults is not None:
+						malicious = details.scanResults.totalFlagged
+						self._appendDetailsLabelValue(
+							# Translators: Label for an extra detail field for the selected add-on. In the add-on store dialog.
+							pgettext("addonStore", "VirusTotal scan results:"),
+							npgettext(
+								"addonStore",
+								# Translators: Summary of VirusTotal scan results for the selected add-on.
+								# {malicious} is the number of vendors that detected the add-on as malicious,
+								# {total} is the total number of vendors that scanned the add-on.
+								# In the add-on store dialog.
+								"{malicious} malware scanner detected this add-on as potentially malicious (out of {total}).",
+								"{malicious} malware scanners detected this add-on as potentially malicious (out of {total}).",
+								malicious,
+							).format(
+								malicious=malicious,
+								total=details.scanResults.totalScans,
+							),
+						)
+						self._appendDetailsLabelValue(
+							# Translators: Label for an extra detail field for the selected add-on. In the add-on store dialog.
+							pgettext("addonStore", "VirusTotal scan URL:"),
+							details.scanResults.scanUrl,
+						)
+
 				self.contentsPanel.Show()
 
 		self.Layout()

```