# Diff for: `source\braille.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\braille.py`  
**Current**: `F:\nvda\gh\alphajp\source\braille.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\braille.py" "b/F:\\nvda\\gh\\alphajp\\source\\braille.py"
index f3296cb19b..35f453ece3 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\braille.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\braille.py"
@@ -12,6 +12,7 @@
 	Any,
 	Callable,
 	Dict,
+	Final,
 	Generator,
 	Iterable,
 	List,
@@ -41,6 +42,7 @@
 import keyboardHandler
 import baseObject
 import config
+import easeOfAccess
 from config.configFlags import (
 	ShowMessages,
 	TetherTo,
@@ -66,6 +68,7 @@
 import brailleViewer
 from autoSettingsUtils.driverSetting import BooleanDriverSetting, NumericDriverSetting
 from utils.security import objectBelowLockScreenAndWindowsIsLocked, post_sessionLockStateChanged
+from winAPI.secureDesktop import post_secureDesktopStateChange
 from textUtils import isUnicodeNormalized, UnicodeNormalizationOffsetConverter
 import hwIo
 from editableText import EditableText
@@ -279,6 +282,8 @@
 	controlTypes.State.ON: "⣏⣿⣹",
 	# Translators: Displayed in braille when a link destination points to the same page
 	controlTypes.State.INTERNAL_LINK: _("smp"),
+	# Translators: Displayed in braille when an object supports multiple selected items.
+	controlTypes.State.MULTISELECTABLE: _("msel"),
 }
 negativeStateLabels = {
 	# Translators: Displayed in braille when an object is not selected.
@@ -308,7 +313,7 @@
 	"form": pgettext("braille landmark abbreviation", "form"),
 }
 
-# nvdajp begin
+# BEGIN JP PATCH
 from jpBrailleUtils import (  # noqa: E402
 	roleLabels as rawRoleLabels,
 	positiveStateLabels as rawPositiveStateLabels,
@@ -363,7 +368,7 @@ def getLandmarkLabels() -> typing.Dict[str, str]:
 	return landmarkLabels
 
 
-# nvdajp end
+# END JP PATCH
 
 #: Cursor shapes
 CURSOR_SHAPES = (
@@ -439,7 +444,7 @@ class FormatTagDelimiter(StrEnum):
 #: @type: str
 AUTO_DISPLAY_NAME = AUTOMATIC_PORT[0]
 
-NO_BRAILLE_DISPLAY_NAME: str = "noBraille"
+NO_BRAILLE_DISPLAY_NAME: Final[str] = "noBraille"
 """The name of the noBraille display driver."""
 
 #: A port name which indicates that USB should be used.
@@ -719,7 +724,9 @@ def _getAnnotationProperty(
 		hasDetailsRoleTemplate = _("has %s")
 		rolesLabels = list(
 			(
+				# BEGIN JP PATCH
 				hasDetailsRoleTemplate % getRoleLabel(role, role.displayString)
+				# END JP PATCH
 				for role in detailsRoles
 				if role  # handle None case without the "has X" grammar.
 			)
@@ -735,7 +742,7 @@ def _getAnnotationProperty(
 def getPropertiesBraille(**propertyValues) -> str:  # noqa: C901
 	textList = []
 	name = propertyValues.get("name")
-	# nvdajp begin
+	# BEGIN JP PATCH
 	# if name:
 	# textList.append(name)
 	isComposition = True
@@ -746,7 +753,7 @@ def getPropertiesBraille(**propertyValues) -> str:  # noqa: C901
 	else:
 		if name:
 			textList.append(name)
-	# nvdajp end
+	# END JP PATCH
 	role: Optional[Union[controlTypes.Role, int]] = propertyValues.get("role")
 	roleText = propertyValues.get("roleText")
 	states = propertyValues.get("states")
@@ -766,29 +773,48 @@ def getPropertiesBraille(**propertyValues) -> str:  # noqa: C901
 		if role == controlTypes.Role.HEADING and level:
 			# Translators: Displayed in braille for a heading with a level.
 			# %s is replaced with the level.
+			# BEGIN JP PATCH
 			roleText = _nvdajp("h%s") % level
+			# END JP PATCH
 			level = None
 		elif role == controlTypes.Role.LINK and states and controlTypes.State.VISITED in states:
 			states = states.copy()
 			states.discard(controlTypes.State.VISITED)
 			# Translators: Displayed in braille for a link which has been visited.
+			# BEGIN JP PATCH
 			roleText = _nvdajp("vlnk")
+			# END JP PATCH
+		elif (
+			role == controlTypes.Role.LIST
+			and states
+			and controlTypes.State.MULTISELECTABLE in states
+			and config.conf["presentation"]["reportMultiSelect"]
+		):
+			# Collapse the list role and multiselectable state into a single role text.
+			# Note that for other cases where this state is found, regular processing with
+			# controlTypes.processAndLabelStates will discard the state if necessary.
+			states = states.copy()
+			states.discard(controlTypes.State.MULTISELECTABLE)
+			# Translators: Displayed in braille for a multi select list.
+			roleText = _("mslst")
 		elif (
 			name or cellCoordsText or rowNumber or columnNumber
 		) and role in controlTypes.silentRolesOnFocus:
 			roleText = None
 		else:
+			# BEGIN JP PATCH
 			roleText = getRoleLabel(role, role.displayString)
+			# END JP PATCH
 	elif role is None:
 		role = propertyValues.get("_role")
-	# nvdajp begin
+	# BEGIN JP PATCH
 	if (
 		config.conf["keyboard"]["nvdajpEnableKeyEvents"]
 		and isComposition
 		and role == controlTypes.Role.EDITABLETEXT
 	):
 		roleText = None
-	# nvdajp end
+	# END JP PATCH
 	value = propertyValues.get("value")
 	if value and role not in controlTypes.silentValuesForRoles:
 		textList.append(value)
@@ -800,9 +826,11 @@ def getPropertiesBraille(**propertyValues) -> str:  # noqa: C901
 				controlTypes.OutputReason.FOCUS,
 				states,
 				None,
+				# BEGIN JP PATCH
 				getPositiveStateLabels(),
 				getNegativeStateLabels(),
-			)
+				# END JP PATCH
+			),
 		)
 	if roleText:
 		textList.append(roleText)
@@ -832,14 +860,14 @@ def getPropertiesBraille(**propertyValues) -> str:  # noqa: C901
 			# Translators: Displayed in braille when an object (e.g. a tree view item) has a hierarchical level.
 			# %s is replaced with the level.
 			textList.append(_("lv %s") % positionInfo["level"])
-	# nvdajp begin https://github.com/nvdajp/nvdajp/issues/109
+	# BEGIN JP PATCH https://github.com/nvdajp/nvdajp/issues/109
 	rowHeaderText = propertyValues.get("rowHeaderText")
 	if rowHeaderText:
 		textList.append(rowHeaderText)
 	columnHeaderText = propertyValues.get("columnHeaderText")
 	if columnHeaderText:
 		textList.append(columnHeaderText)
-	# nvdajp end
+	# END JP PATCH
 	if rowNumber:
 		if includeTableCellCoords and not cellCoordsText:
 			if rowSpan > 1:
@@ -855,10 +883,11 @@ def getPropertiesBraille(**propertyValues) -> str:  # noqa: C901
 				rowStr = _("r{rowNumber}").format(rowNumber=rowNumber)
 			textList.append(rowStr)
 	if columnNumber:
-		# nvdajp (moved to above) https://github.com/nvdajp/nvdajp/issues/109
+		# BEGIN JP PATCH (moved to above) https://github.com/nvdajp/nvdajp/issues/109
 		# columnHeaderText = propertyValues.get("columnHeaderText")
 		# if columnHeaderText:
 		# textList.append(columnHeaderText)
+		# END JP PATCH
 		if includeTableCellCoords and not cellCoordsText:
 			if columnSpan > 1:
 				# Translators: Displayed in braille for the table cell column numbers when a cell spans multiple columns.
@@ -930,6 +959,7 @@ def update(self):
 		)
 		description = obj.description if _shouldUseDescription else None
 		detailsRoles = obj.annotations.roles if obj.annotations else None
+		# BEGIN JP PATCH
 		columnHeaderText = None
 		try:
 			if hasattr(obj, "columnHeaderText") and config.conf["documentFormatting"]["reportTableHeaders"]:
@@ -942,6 +972,7 @@ def update(self):
 				rowHeaderText = obj.rowHeaderText
 		except NotImplementedError:
 			pass
+		# END JP PATCH
 		text = getPropertiesBraille(
 			name=name,
 			role=role,
@@ -958,8 +989,10 @@ def update(self):
 			cellCoordsText=obj.cellCoordsText
 			if config.conf["documentFormatting"]["reportTableCellCoords"]
 			else None,
+			# BEGIN JP PATCH
 			columnHeaderText=columnHeaderText,
 			rowHeaderText=rowHeaderText,
+			# END JP PATCH
 			errorMessage=errorMessage,
 		)
 		if role == controlTypes.Role.MATH:
@@ -1052,7 +1085,9 @@ def getControlFieldBraille(
 	roleText = field.get("roleTextBraille", field.get("roleText"))
 	landmark = field.get("landmark")
 	if not roleText and role == controlTypes.Role.LANDMARK and landmark:
+		# BEGIN JP PATCH
 		roleText = f"{getRoleLabel(controlTypes.Role.LANDMARK)} {getLandmarkLabel(landmark)}"
+		# END JP PATCH
 
 	content = field.get("content")
 
@@ -1265,7 +1300,9 @@ def getFormatFieldBraille(field, fieldCache, isAtStart, formatConfig):
 		link = field.get("link")
 		oldLink = fieldCache.get("link")
 		if link and link != oldLink:
+			# BEGIN JP PATCH
 			textList.append(getRoleLabel(controlTypes.Role.LINK))
+			# END JP PATCH
 	if formatConfig["reportComments"]:
 		comment = field.get("comment")
 		oldComment = fieldCache.get("comment") if fieldCache is not None else None
@@ -1510,7 +1547,9 @@ def _addTextWithFields(self, info, formatConfig, isSelection=False):
 									formatConfig,
 								)
 								if not presCat or presCat is field.PRESCAT_LAYOUT:
+									# BEGIN JP PATCH
 									textList.append(getPositiveStateLabel(controlTypes.State.CLICKABLE))
+									# END JP PATCH
 								inClickable = True
 						text = info.getControlFieldBraille(field, ctrlFields, True, formatConfig)
 						if text:
@@ -2517,6 +2556,7 @@ def __init__(self):
 		self.ackTimerHandle = winKernel.createWaitableTimer()
 
 		post_sessionLockStateChanged.register(self._onSessionLockStateChanged)
+		post_secureDesktopStateChange.register(self._onSecureDesktopStateChanged)
 		brailleViewer.postBrailleViewerToolToggledAction.register(self._onBrailleViewerChangedState)
 		# noqa: F401 avoid module level import to prevent cyclical dependency
 		# between speech and braille
@@ -2540,6 +2580,7 @@ def terminate(self):
 			self._cursorBlinkTimer.Stop()
 			self._cursorBlinkTimer = None
 		config.post_configProfileSwitch.unregister(self.handlePostConfigProfileSwitch)
+		post_secureDesktopStateChange.unregister(self._onSecureDesktopStateChanged)
 		post_sessionLockStateChanged.unregister(self._onSessionLockStateChanged)
 		if self.display:
 			self.display.terminate()
@@ -2558,6 +2599,33 @@ def _clearAll(self) -> None:
 			self._dismissMessage(False)
 		self.update()
 
+	def _onSecureDesktopStateChanged(self, isSecureDesktop: bool):
+		self.mainBuffer.clear()
+		if not easeOfAccess.isRegistered():
+			if isSecureDesktop:
+				log.warning("Not disabling braille because not registered in ease of access")
+			return
+		if isSecureDesktop:
+			self._disableDetection()  # Does nothing when detection inactive
+			if self.display:
+				# Suppress setting the display with empty cells when terminating it.
+				self.display._suppressDisplayClear = True
+			self.setDisplayByName(NO_BRAILLE_DISPLAY_NAME, isFallback=True)
+		else:
+			configured = config.conf["braille"]["display"]
+			if configured == AUTO_DISPLAY_NAME:
+				lastRequested = (self._lastRequestedDisplayName, self._lastRequestedDeviceMatch)
+				preferredDevice: bdDetect.DriverAndDeviceMatch | None = (
+					lastRequested if all(lastRequested) else None
+				)
+				self._enableDetection(preferredDevice=preferredDevice)
+			else:
+				# Note, this is executed on the main thread and can take some time for slower drivers.
+				self.setDisplayByName(
+					configured,
+					isFallback=True,  # Don't write to config
+				)
+
 	def _onSessionLockStateChanged(self, isNowLocked: bool):
 		"""Clear the braille buffers and update the braille display to prevent leaking potentially sensitive information from a locked session.
 
@@ -2738,10 +2806,14 @@ def _handleEnabledDecisionFalse(self):
 		if self.buffer is self.messageBuffer:
 			self._dismissMessage(shouldUpdate=False)
 
-	_lastRequestedDisplayName = None
+	_lastRequestedDisplayName: str | None = None
 	"""The name of the last requested braille display driver with setDisplayByName,
 	even if it failed and has fallen back to no braille.
 	"""
+	_lastRequestedDeviceMatch: bdDetect.DeviceMatch | None = None
+	"""The last requested device match belonging to _lastRequestedDisplayName,
+	even if it failed and has fallen back to no braille.
+	"""
 
 	def setDisplayByName(
 		self,
@@ -2757,6 +2829,7 @@ def setDisplayByName(
 		elif not isFallback:
 			# #8032: Take note of the display requested, even if it is going to fail.
 			self._lastRequestedDisplayName = name
+			self._lastRequestedDeviceMatch = detected
 			if not detected:
 				self._disableDetection()
 
@@ -3305,25 +3378,38 @@ def _enableDetection(
 		usb: bool = True,
 		bluetooth: bool = True,
 		limitToDevices: Optional[List[str]] = None,
+		preferredDevice: bdDetect.DriverAndDeviceMatch | None = None,
 	):
 		"""Enables automatic detection of braille displays.
 		When auto detection is already active, this will force a rescan for devices.
 		This should also be executed when auto detection should be resumed due to loss of display connectivity.
 		In that case, it is triggered by L{setDisplayByname}.
-		@param usb: Whether to scan for USB devices
-		@param bluetooth: Whether to scan for Bluetooth devices.
-		@param limitToDevices: An optional list of driver names a scan should be limited to.
+		:param usb: Whether to scan for USB devices
+		:param bluetooth: Whether to scan for Bluetooth devices.
+		:param limitToDevices: An optional list of driver names a scan should be limited to.
 			This is used when a Bluetooth device is detected, in order to switch to USB
 			when an USB device for the same driver is found.
-			C{None} if no driver filtering should occur.
+			``None`` if no driver filtering should occur.
+		:param preferredDevice: An optional preferred device to use for detection.
+			this device is attempted to be used before a scan is started.
 		"""
 		self.setDisplayByName(NO_BRAILLE_DISPLAY_NAME, isFallback=True)
 		if self._detector:
-			self._detector.rescan(usb=usb, bluetooth=bluetooth, limitToDevices=limitToDevices)
+			self._detector.rescan(
+				usb=usb,
+				bluetooth=bluetooth,
+				limitToDevices=limitToDevices,
+				preferredDevice=preferredDevice,
+			)
 			return
 		config.conf["braille"]["display"] = AUTO_DISPLAY_NAME
 		self._detector = bdDetect._Detector()
-		self._detector._queueBgScan(usb=usb, bluetooth=bluetooth, limitToDevices=limitToDevices)
+		self._detector._queueBgScan(
+			usb=usb,
+			bluetooth=bluetooth,
+			limitToDevices=limitToDevices,
+			preferredDevice=preferredDevice,
+		)
 
 	def _disableDetection(self):
 		"""Disables automatic detection of braille displays."""
@@ -3517,6 +3603,9 @@ def terminate(self):
 		@postcondition: This instance can no longer be used unless it is constructed again.
 		"""
 		super().terminate()
+		if getattr(self, "_suppressDisplayClear", False):
+			self._suppressDisplayClear = False
+			return
 		# Clear the display.
 		try:
 			self.display([0] * self.numCells)

```