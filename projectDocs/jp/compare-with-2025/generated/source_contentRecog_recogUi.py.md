# Diff for: `source\contentRecog\recogUi.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\contentRecog\recogUi.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\contentRecog\recogUi.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\contentRecog\\recogUi.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\contentRecog\\recogUi.py"
index 5b8a608..86042fa 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\contentRecog\\recogUi.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\contentRecog\\recogUi.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2017-2025 NV Access Limited, James Teh, Leonard de Ruijter, Cyrille Bougot
+# Copyright (C) 2017-2025 NV Access Limited, James Teh, Leonard de Ruijter, Cyrille Bougot, Cary-rowen, hwf1324
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -22,6 +22,7 @@
 import eventHandler
 import textInfos
 from logHandler import log
+from speech import sayAll
 import queueHandler
 import core
 from scriptHandler import script
@@ -45,6 +46,7 @@ class RecogResultNVDAObject(cursorManager.CursorManager, NVDAObjects.window.Wind
 
 	def __init__(self, result=None, obj=None):
 		self.parent = parent = api.getFocusObject()
+		self._shouldSayAllOnFirstFocus = False
 		self.result = result
 		if result:
 			self._selection = self.makeTextInfo(textInfos.POSITION_FIRST)
@@ -160,6 +162,8 @@ def _onFirstResult(self, result: Union[RecognitionResult, Exception]):
 		self._selection = self.makeTextInfo(textInfos.POSITION_FIRST)
 		# This method queues an event to the main thread.
 		self.setFocus()
+		if self.recognizer.autoSayAllOnResult:
+			self._shouldSayAllOnFirstFocus = True
 		if self.recognizer.allowAutoRefresh:
 			self._scheduleRecognize()
 
@@ -204,6 +208,9 @@ def _onResult(self, result: Union[RecognitionResult, Exception]):
 
 	def event_gainFocus(self):
 		super().event_gainFocus()
+		if self._shouldSayAllOnFirstFocus:
+			self._shouldSayAllOnFirstFocus = False
+			sayAll.SayAllHandler.readText(sayAll.CURSOR.CARET)
 		if self.recognizer.allowAutoRefresh:
 			# Make LiveText watch for and report new text.
 			self.startMonitoring()
@@ -219,6 +226,8 @@ def start(self):
 
 #: Keeps track of the recognition in progress, if any.
 _activeRecog = None
+# Register the fake NVDA object class.
+api.fakeNVDAObjectClasses.add(RecogResultNVDAObject)
 
 
 def recognizeNavigatorObject(recognizer: ContentRecognizer):

```