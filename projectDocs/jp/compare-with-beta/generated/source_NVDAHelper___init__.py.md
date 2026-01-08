# Diff for: `source\NVDAHelper\__init__.py`

**Source**: `F:\nvda\gh\beta\source\NVDAHelper\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAHelper\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\NVDAHelper\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAHelper\\__init__.py"
index e15d0ee..35b4e31 100644
--- "a/F:\\nvda\\gh\\beta\\source\\NVDAHelper\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAHelper\\__init__.py"
@@ -67,6 +67,13 @@
 _remoteLoaderARM64: "_RemoteLoader | None" = None
 lastLanguageID = None
 lastLayoutString = None
+# BEGIN JP PATCH
+# nvdajp: Japanese input composition variables
+lastCompAttr = None
+lastCompString = None
+lastSelectionStart = None
+lastSelectionEnd = None
+# END JP PATCH
 
 
 # utility function to point an exported function pointer in a dll  to a ctypes wrapped python function
@@ -413,7 +420,79 @@ def handleInputCompositionStart(compositionString, selectionStart, selectionEnd,
 
 @WINFUNCTYPE(c_long, c_wchar_p, c_int, c_int, c_int)
 def nvdaControllerInternal_inputCompositionUpdate(compositionString, selectionStart, selectionEnd, isReading):
+	# BEGIN JP PATCH
+	global lastCompAttr, lastCompString
+	global lastSelectionStart, lastSelectionEnd
 	from NVDAObjects.inputComposition import InputComposition
+
+	# nvdajp begin
+	compAttr = ""
+	if "\t" in compositionString:
+		compositionString, compAttr = compositionString.split("\t")
+		if (
+			lastCompString == compositionString
+			and lastCompAttr == compAttr
+			and lastSelectionStart == selectionStart
+			and lastSelectionEnd == selectionEnd
+			and not (
+				compositionString in (" ", "\u3000")
+				and compAttr == ""
+				and selectionStart == -1
+				and selectionEnd == -1
+			)
+		):
+			log.debug(
+				f"ignored ({compositionString=}) ({compAttr=}) ({selectionStart=}) ({selectionEnd=}) ({lastCompString=}) ({lastCompAttr=}) ({lastSelectionStart=}) ({lastSelectionEnd=})"
+			)
+			return 0
+		log.debug(f"({lastCompString=}) ({compositionString=})")
+		deletedString = ""
+		if (
+			lastCompString
+			and compositionString
+			and len(lastCompString) > len(compositionString)
+			and lastCompString.startswith(compositionString)
+		):
+			deletedString = lastCompString[len(compositionString) :]
+		_lastCompAttr = lastCompAttr
+		lastCompAttr = compAttr
+		lastCompString = compositionString
+		lastSelectionStart = selectionStart
+		lastSelectionEnd = selectionEnd
+		if config.conf["keyboard"]["nvdajpEnableKeyEvents"]:
+			if badCompositionUpdate(compositionString, compAttr):
+				return 0
+			log.debug(f"({compositionString=}) ({compAttr=}) ({selectionStart=}) ({selectionEnd=})")
+			extractedString, endIndex = extractCompositionString(
+				compAttr, compositionString, selectionStart, selectionEnd, _lastCompAttr
+			)
+			log.debug(f"({extractedString=}) ({endIndex=}) ({deletedString=})")
+			if extractedString:
+				focus = api.getFocusObject()
+				if isinstance(focus, InputComposition):
+					focus.compositionUpdate(extractedString, 0, endIndex, 0, forceNewText=True)
+				return 0
+			elif deletedString:
+				focus = api.getFocusObject()
+				if focus and hasattr(focus, "windowClassName") and focus.windowClassName == "Scintilla":
+					import ui
+
+					ui.message(deletedString)
+					return 0
+	else:
+		log.debug(f"{compositionString=} {selectionStart=} {selectionEnd=} {isReading=} {lastCompString=}")
+		if (
+			lastCompString
+			and not compositionString
+			and selectionStart == -1
+			and selectionEnd == -1
+			and isReading == 0
+		):
+			queueHandler.queueFunction(queueHandler.eventQueue, handleInputCompositionEnd, lastCompString)
+			return 0
+		resetInputCompositionVariables()
+	# nvdajp end
+	# END JP PATCH
 	from NVDAObjects.IAccessible.mscandui import ModernCandidateUICandidateItem
 
 	if selectionStart == -1:
@@ -772,6 +851,104 @@ def terminate(self):
 		winKernel.closeHandle(self._process)
 
 
+# BEGIN JP PATCH
+# nvdajp: Japanese input composition variables reset function
+def resetInputCompositionVariables():
+	global lastCompAttr, lastCompString, lastSelectionStart, lastSelectionEnd
+	lastCompAttr = None
+	lastCompString = None
+	lastSelectionStart = None
+	lastSelectionEnd = None
+
+
+def badCompositionUpdate(compositionString: str, compAttr: str) -> bool:
+	"""
+	Validates the given input composition string and its attributes.
+	If the string meets certain conditions, this function returns True.
+
+	This function is designed to ignore certain compositionUpdate events,
+	specifically those where an alphabetic character is inserted
+	in the middle of a string of Kana characters, such as
+	"ほｎあいうえお".
+	This is done to prevent unexpected behavior in the input composition process
+	for languages that use Kana characters.
+
+	Args:
+	compositionString (str): The input composition string to validate.
+	compAttr (str): The attributes of the input composition string.
+
+	Returns:
+	bool: True if the string meets certain conditions, False otherwise.
+	"""
+	if len(compositionString) <= 2:
+		return False
+	if any(c != "0" for c in compAttr):
+		return False
+	from unicodedata import category
+
+	if (
+		any(category(c) == "Ll" for c in compositionString[1:-1])
+		and category(compositionString[0]) == "Lo"
+		and category(compositionString[-1]) == "Lo"
+	):
+		log.debug("(%s) (%s) should be ignored" % (compositionString, compAttr))
+		return True
+	return False
+
+
+def extractCompositionString(
+	compAttr: str, compositionString: str, selectionStart: int, selectionEnd: int, lastCompAttr: str
+) -> tuple[str, int]:
+	"""
+	This function extracts a part of the composition string based on the attribute values.
+	It checks the attribute values in a specific order and extracts the corresponding characters from the composition string.
+	The function also returns the end index of the extracted string in the original composition string.
+
+	Args:
+		compAttr (str): The attribute values for the composition string.
+			Each character in this string corresponds to a TF_ATTR value ('0', '1', etc.) for the corresponding character in the composition string.
+		compositionString (str): The composition string.
+		selectionStart (int): The start index of the selection in the composition string.
+		selectionEnd (int): The end index of the selection in the composition string.
+		lastCompAttr (str): The last attribute values for the composition string.
+
+	TF_ATTR values represent different states of text in an input composition string:
+	TF_ATTR_INPUT                = 0: The text is in the process of being composed.
+	TF_ATTR_TARGET_CONVERTED     = 1: The text has been converted as a result of the user accepting a conversion candidate.
+	TF_ATTR_CONVERTED            = 2: The text has been converted.
+	TF_ATTR_TARGET_NOTCONVERTED  = 3: The text is a target for conversion, but has not yet been converted.
+	TF_ATTR_INPUT_ERROR          = 4: There was an error in inputting the text.
+	TF_ATTR_FIXEDCONVERTED       = 5: The text has been converted and fixed, and can no longer be modified.
+
+	Returns:
+		Tuple[str, int]: The extracted string and its end index in the original composition string.
+	"""
+	extractedString = ""
+	endIndex = 0
+
+	# This inner function extracts characters from the composition string where the attribute value matches the given condition.
+	def extractString(condition: str) -> str:
+		return "".join(compositionString[i] for i, attr in enumerate(compAttr) if attr == condition)
+
+	# Check the attribute values in a specific order and extract the corresponding characters.
+	if ("3" in compAttr) and ("1" not in compAttr):
+		endIndex = len(compositionString)
+		extractedString = extractString("3")
+	elif ("1" in compAttr) and (lastCompAttr is None or any([c != "0" for c in lastCompAttr])):
+		extractedString = extractString("1")
+	elif ("0" in compAttr) and ("2" in compAttr):
+		extractedString = extractString("0")
+	elif all([c == "0" for c in compAttr]) and 0 <= selectionStart == selectionEnd < len(compAttr):
+		# reviewing pre-edit character
+		extractedString = compositionString[selectionStart]
+		log.debug("((%s))" % extractedString)
+	return extractedString, endIndex
+
+
+resetInputCompositionVariables()
+# END JP PATCH
+
+
 def initialize() -> None:
 	global _remoteLib, _remoteLoaderX86, _remoteLoaderAMD64, _remoteLoaderARM64
 	global lastLanguageID, lastLayoutString
@@ -846,21 +1023,16 @@ def initialize() -> None:
 	# Manually start the in-process manager thread for this NVDA main thread now, as a slow system can cause this action to confuse WX
 	_remoteLib.initInprocManagerThreadIfNeeded()
 	arch = winVersion.getWinVer().processorArchitecture
-	if arch == "AMD64":
-		if ReadPaths.coreArchLibPath != ReadPaths.versionedLibX86Path:
+	if arch != "x86" and ReadPaths.coreArchLibPath != ReadPaths.versionedLibX86Path:
 		_remoteLoaderX86 = _RemoteLoader(ReadPaths.versionedLibX86Path)
-		if ReadPaths.coreArchLibPath != ReadPaths.versionedLibAMD64Path:
+	elif arch in ("AMD64", "ARM64") and ReadPaths.coreArchLibPath != ReadPaths.versionedLibAMD64Path:
 		_remoteLoaderAMD64 = _RemoteLoader(ReadPaths.versionedLibAMD64Path)
-	elif arch == "ARM64":
-		if ReadPaths.coreArchLibPath != ReadPaths.versionedLibX86Path:
-			_remoteLoaderX86 = _RemoteLoader(ReadPaths.versionedLibX86Path)
-		if ReadPaths.coreArchLibPath != ReadPaths.versionedLibAMD64Path:
-			# Windows 10 on ARM does not support AMD64 emulation.
-			# Thus only start the AMD64 remote loader if on Windows 11 or above.
+	elif arch == "ARM64" and ReadPaths.coreArchLibPath != ReadPaths.versionedLibARM64Path:
+		_remoteLoaderARM64 = _RemoteLoader(ReadPaths.versionedLibARM64Path)
+		# Windows on ARM from Windows 11 supports running AMD64 apps.
+		# Thus we also need to be able to inject into these.
 		if winVersion.getWinVer() >= winVersion.WIN11:
 			_remoteLoaderAMD64 = _RemoteLoader(ReadPaths.versionedLibAMD64Path)
-		if ReadPaths.coreArchLibPath != ReadPaths.versionedLibARM64Path:
-			_remoteLoaderARM64 = _RemoteLoader(ReadPaths.versionedLibARM64Path)
 
 
 def terminate():

```