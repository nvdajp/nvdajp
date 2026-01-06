# Diff for: `source\NVDAObjects\UIA\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\UIA\__init__.py`  
**Current**: `F:\nvda\gh\alphajp\source\NVDAObjects\UIA\__init__.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\UIA\\__init__.py" "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\UIA\\__init__.py"
index e06d16ce61..8d1e4a4b43 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\UIA\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\UIA\\__init__.py"
@@ -30,6 +30,7 @@
 import controlTypes
 from controlTypes import TextPosition, TextAlign
 import config
+from config.configFlags import ReportSpellingErrors
 import speech
 import api
 import textInfos
@@ -56,7 +57,6 @@
 from NVDAObjects.behaviors import (
 	ProgressBar,
 	EditableTextBase,
-	EditableTextWithoutAutoSelectDetection,
 	EditableTextWithAutoSelectDetection,
 	Dialog,
 	Notification,
@@ -313,7 +313,7 @@ def _getFormatFieldAnnotationTypes(
 		# Always mutate to a tuple to allow for a generic x in y matching
 		if not isinstance(annotationTypes, tuple):
 			annotationTypes = (annotationTypes,)
-		if formatConfig["reportSpellingErrors"]:
+		if formatConfig["reportSpellingErrors2"] != ReportSpellingErrors.OFF.value:
 			if UIAHandler.AnnotationType_SpellingError in annotationTypes:
 				formatField["invalid-spelling"] = True
 			if UIAHandler.AnnotationType_GrammarError in annotationTypes:
@@ -368,7 +368,7 @@ def _getFormatFieldAtRange(  # noqa: C901
 		if not isinstance(textRange, UIAHandler.IUIAutomationTextRange):
 			raise ValueError("%s is not a text range" % textRange)
 		fetchAnnotationTypes = (
-			formatConfig["reportSpellingErrors"]
+			formatConfig["reportSpellingErrors2"] != ReportSpellingErrors.OFF.value
 			or formatConfig["reportComments"]
 			or formatConfig["reportRevisions"]
 			or formatConfig["reportBookmarks"]
@@ -1196,11 +1196,7 @@ def findOverlayClasses(self, clsList):  # NOQA: C901
 		UIAClassName = self.UIAElement.cachedClassName
 		# #11445: to avoid COM errors, do not fetch cached UIA Automation Id from the underlying element.
 		UIAAutomationId = self.UIAAutomationId
-		if UIAClassName=="ModeTile":
-			clsList.append(ModeTile)
-		elif UIAClassName=="Input Flyout":
-			clsList.append(InputFlyout)
-		elif (
+		if (
 			UIAClassName == "NetUITWMenuItem"
 			and UIAControlType == UIAHandler.UIA_MenuItemControlTypeId
 			and not self.name
@@ -1452,10 +1448,7 @@ def findOverlayClasses(self, clsList):  # NOQA: C901
 				clsList.append(XamlEditableText)
 			elif UIAClassName == "WpfTextView":
 				clsList.append(WpfTextView)
-			if UIAHandler.autoSelectDetectionAvailable:
-				clsList.append(EditableTextWithAutoSelectDetection)
-			else:
-				clsList.append(EditableTextWithoutAutoSelectDetection)
+			clsList.append(EditableTextWithAutoSelectDetection)
 
 		clsList.append(UIA)
 
@@ -1895,6 +1888,7 @@ def _get_keyboardShortcut(self):
 
 	_UIAStatesPropertyIDs = {
 		UIAHandler.UIA_HasKeyboardFocusPropertyId,
+		UIAHandler.UIA.UIA_SelectionCanSelectMultiplePropertyId,
 		UIAHandler.UIA_SelectionItemIsSelectedPropertyId,
 		UIAHandler.UIA_IsDataValidForFormPropertyId,
 		UIAHandler.UIA_IsRequiredForFormPropertyId,
@@ -1938,6 +1932,8 @@ def _get_states(self):
 					if role == controlTypes.Role.RADIOBUTTON
 					else controlTypes.State.SELECTED,
 				)
+		if self._getUIACacheablePropertyValue(UIAHandler.UIA.UIA_SelectionCanSelectMultiplePropertyId):
+			states.add(controlTypes.State.MULTISELECTABLE)
 		if not self._getUIACacheablePropertyValue(UIAHandler.UIA_IsEnabledPropertyId, True):
 			states.add(controlTypes.State.UNAVAILABLE)
 		try:

```