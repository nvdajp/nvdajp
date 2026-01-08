# Diff for: `source\NVDAObjects\inputComposition.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\NVDAObjects\inputComposition.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\inputComposition.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\inputComposition.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\inputComposition.py"
index 8f7e721..ae0906b 100644
--- "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\inputComposition.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\inputComposition.py"
@@ -14,6 +14,14 @@
 from .behaviors import EditableTextWithAutoSelectDetection, CandidateItem as CandidateItemBehavior
 from textInfos.offsets import OffsetsTextInfo
 
+# nvdajp begin
+from logHandler import log
+import jpUtils
+import winUser
+import time
+import braille
+# nvdajp end
+
 
 def calculateInsertedChars(oldComp, newComp):
 	oldLen = len(oldComp)
@@ -52,6 +60,76 @@ def _getStoryLength(self):
 		return len(self._getStoryText())
 
 
+# nvdajp begin
+# from keyboardHandler.internal_keyDownEvent
+lastKeyGesture = None
+
+
+def reportKeyDownEvent(gesture):
+	global lastKeyGesture
+	lastKeyGesture = gesture
+
+
+def needDiscriminantReading(gesture):
+	if not gesture:
+		return False
+	if (winUser.VK_CONTROL, False) in gesture.generalizedModifiers or gesture.vkCode in (
+		winUser.VK_SPACE,
+		winUser.VK_CONVERT,
+		winUser.VK_IME_ON,
+		winUser.VK_LEFT,
+		winUser.VK_RIGHT,
+		winUser.VK_UP,
+		winUser.VK_DOWN,
+		winUser.VK_F2,
+		winUser.VK_F3,
+		winUser.VK_F4,
+		winUser.VK_F5,
+		winUser.VK_F6,
+		winUser.VK_F7,
+		winUser.VK_F8,
+		winUser.VK_F9,
+		winUser.VK_F10,
+		winUser.VK_F11,
+		winUser.VK_NONCONVERT,
+		winUser.VK_IME_OFF,
+		winUser.VK_ESCAPE,
+		winUser.VK_TAB,
+	):
+		return True
+	# VK_RCONTROL
+	if (winUser.VK_CONTROL, True) in gesture.generalizedModifiers:
+		return True
+	return False
+
+
+lastCompositionText = None
+lastCompositionTime = None
+
+
+# from NVDAHelper.nvdaControllerInternal_inputCompositionUpdate
+def reportPartialSelection(sel):
+	global lastCompositionText, lastCompositionTime
+	newText = jpUtils.getDiscriminantReading(sel)
+	newTextForBraille = jpUtils.getDescriptionForBraille(sel)
+	if lastCompositionText == newText and lastCompositionTime and time.time() - lastCompositionTime < 0.1:
+		newText = None
+	if newText:
+		log.debug(newText)
+		lastCompositionTime = time.time()
+		lastCompositionText = newText
+		queueHandler.queueFunction(queueHandler.eventQueue, braille.handler.message, newTextForBraille)
+		queueHandler.queueFunction(
+			queueHandler.eventQueue,
+			speech.speakText,
+			newText,
+			symbolLevel=characterProcessing.SymbolLevel.ALL,
+		)
+
+
+# nvdajp end
+
+
 class InputComposition(EditableTextWithAutoSelectDetection, Window):
 	TextInfo = InputCompositionTextInfo
 	# Translators: The label for a 'composition' Window that appears when the user is typing one or more east-Asian characters into a document.
@@ -68,6 +146,7 @@ class InputComposition(EditableTextWithAutoSelectDetection, Window):
 	compositionSelectionOffsets = (0, 0)
 	readingSelectionOffsets = (0, 0)
 	isReading = False
+	IAccessibleRole = role
 
 	def __init__(self, parent=None):
 		self.parent = parent
@@ -78,21 +157,54 @@ def findOverlayClasses(self, clsList):
 		clsList.append(InputComposition)
 		return clsList
 
-	def reportNewText(self, oldString, newString):
+	def reportNewText(self, oldString, newString, forceNewText=False):
+		global lastCompositionText, lastCompositionTime  # nvdajp
+		# nvdajp begin
+		newTextForBraille = newText = calculateInsertedChars(
+			oldString.strip("\u3000"), newString.strip("\u3000")
+		)
+		if forceNewText:
+			newText = newString.strip("\u3000")
+		isCandidate = False
+		if (
+			config.conf["keyboard"]["nvdajpEnableKeyEvents"]
+			and config.conf["inputComposition"]["announceSelectedCandidate"]
+			and needDiscriminantReading(lastKeyGesture)
+		):
+			ns = newString.strip("\u3000")
+			newText = jpUtils.getDiscriminantReading(ns)
+			newTextForBraille = jpUtils.getDescriptionForBraille(ns)
+			isCandidate = True
+		if lastCompositionText == newText and lastCompositionTime and time.time() - lastCompositionTime < 1.0:
+			newText = None
+			isCandidate = False
+		# if isCandidate:
+		# import tones
+		# tones.beep(1000,10)
+		if newText:
+			if config.conf["keyboard"]["nvdajpEnableKeyEvents"]:
+				newText = jpUtils.fixNewText(newText, isCandidate)
+				lastCompositionTime = time.time()
+				lastCompositionText = newText
+				queueHandler.queueFunction(
+					queueHandler.eventQueue, braille.handler.message, newTextForBraille
+				)
 		if (
 			config.conf["keyboard"]["speakTypedCharacters"] != TypingEcho.OFF.value
 			or config.conf["keyboard"]["speakTypedWords"] != TypingEcho.OFF.value
+			or isCandidate
 		):
-			newText = calculateInsertedChars(oldString.strip("\u3000"), newString.strip("\u3000"))
-			if newText:
 			queueHandler.queueFunction(
 				queueHandler.eventQueue,
 				speech.speakText,
 				newText,
 				symbolLevel=characterProcessing.SymbolLevel.ALL,
 			)
+		# nvdajp end
 
-	def compositionUpdate(self, compositionString, selectionStart, selectionEnd, isReading, announce=True):
+	def compositionUpdate(
+		self, compositionString, selectionStart, selectionEnd, isReading, announce=True, forceNewText=False
+	):
 		if isReading and not config.conf["inputComposition"]["reportReadingStringChanges"]:
 			return
 		if not isReading and not config.conf["inputComposition"]["reportCompositionStringChanges"]:
@@ -101,7 +213,8 @@ def compositionUpdate(self, compositionString, selectionStart, selectionEnd, isR
 			self.reportNewText(
 				(self.readingString if isReading else self.compositionString),
 				compositionString,
-			)
+				forceNewText=forceNewText,
+			)  # noqa: E701
 		hasChanged = False
 		if isReading:
 			self.readingString = compositionString

```