# Diff for: `source\braille.py`

**Source**: `F:\nvda\gh\beta\source\braille.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\braille.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\braille.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\braille.py"
index c1c0abd..5936994 100644
--- "a/F:\\nvda\\gh\\beta\\source\\braille.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\braille.py"
@@ -316,6 +316,63 @@
 	"form": pgettext("braille landmark abbreviation", "form"),
 }
 
+# BEGIN JP PATCH
+from jpBrailleUtils import (  # noqa: E402
+	roleLabels as rawRoleLabels,
+	positiveStateLabels as rawPositiveStateLabels,
+	negativeStateLabels as rawNegativeStateLabels,
+	landmarkLabels as rawLandmarkLabels,
+)
+
+
+def useRawLabels() -> bool:
+	return config.conf["braille"]["expandAtCursor"]
+
+
+def _nvdajp(rawLabel: str) -> str:
+	if useRawLabels():
+		return rawLabel
+	return _(rawLabel)
+
+
+def getRoleLabel(role: controlTypes.Role, displayString: Optional[str] = None) -> str:
+	if useRawLabels():
+		return rawRoleLabels.get(role, displayString)
+	return roleLabels.get(role, displayString)
+
+
+def getPositiveStateLabel(state: controlTypes.State) -> str:
+	if useRawLabels():
+		return rawPositiveStateLabels.get(state)
+	return positiveStateLabels.get(state)
+
+
+def getPositiveStateLabels() -> typing.Dict[controlTypes.State, str]:
+	if useRawLabels():
+		return rawPositiveStateLabels
+	return positiveStateLabels
+
+
+def getNegativeStateLabels() -> typing.Dict[controlTypes.State, str]:
+	if useRawLabels():
+		return rawNegativeStateLabels
+	return negativeStateLabels
+
+
+def getLandmarkLabel(name: str) -> str:
+	if useRawLabels():
+		return rawLandmarkLabels.get(name)
+	return landmarkLabels.get(name)
+
+
+def getLandmarkLabels() -> typing.Dict[str, str]:
+	if useRawLabels():
+		return rawLandmarkLabels
+	return landmarkLabels
+
+
+# END JP PATCH
+
 #: Cursor shapes
 CURSOR_SHAPES = (
 	# Translators: The description of a braille cursor shape.
@@ -422,7 +479,6 @@ def shouldBeUsed(self, key) -> bool:
 			return bool(formatConfig["reportSpellingErrors2"] & ReportSpellingErrors.BRAILLE)
 		return formatConfig["fontAttributeReporting"] & OutputMode.BRAILLE
 
-
 fontAttributeFormattingMarkers: dict[str, FormattingMarker] = {
 	"bold": FormattingMarker(
 		# Translators: Brailled at the start of bold text.
@@ -696,7 +752,9 @@ def _getAnnotationProperty(
 		hasDetailsRoleTemplate = _("has %s")
 		rolesLabels = list(
 			(
-				hasDetailsRoleTemplate % roleLabels.get(role, role.displayString)
+				# BEGIN JP PATCH
+				hasDetailsRoleTemplate % getRoleLabel(role, role.displayString)
+				# END JP PATCH
 				for role in detailsRoles
 				if role  # handle None case without the "has X" grammar.
 			)
@@ -712,8 +770,18 @@ def _getAnnotationProperty(
 def getPropertiesBraille(**propertyValues) -> str:  # noqa: C901
 	textList = []
 	name = propertyValues.get("name")
+	# BEGIN JP PATCH
+	# if name:
+	# textList.append(name)
+	isComposition = True
+	if config.conf["keyboard"]["nvdajpEnableKeyEvents"]:
+		if name and name != _("Composition"):
+			isComposition = False
+			textList.append(name)
+	else:
 		if name:
 			textList.append(name)
+	# END JP PATCH
 	role: Optional[Union[controlTypes.Role, int]] = propertyValues.get("role")
 	roleText = propertyValues.get("roleText")
 	states = propertyValues.get("states")
@@ -734,13 +802,17 @@ def getPropertiesBraille(**propertyValues) -> str:  # noqa: C901
 		if role == controlTypes.Role.HEADING and level:
 			# Translators: Displayed in braille for a heading with a level.
 			# %s is replaced with the level.
-			roleText = _("h%s") % level
+			# BEGIN JP PATCH
+			roleText = _nvdajp("h%s") % level
+			# END JP PATCH
 			level = None
 		elif role == controlTypes.Role.LINK and states and controlTypes.State.VISITED in states:
 			states = states.copy()
 			states.discard(controlTypes.State.VISITED)
 			# Translators: Displayed in braille for a link which has been visited.
-			roleText = _("vlnk")
+			# BEGIN JP PATCH
+			roleText = _nvdajp("vlnk")
+			# END JP PATCH
 		elif role == controlTypes.Role.LIST:
 			if (
 				states
@@ -759,15 +831,24 @@ def getPropertiesBraille(**propertyValues) -> str:  # noqa: C901
 			if childControlCount:
 				roleText += childControlCount
 				childControlCount = None
-
 		elif (
 			name or cellCoordsText or rowNumber or columnNumber
 		) and role in controlTypes.silentRolesOnFocus:
 			roleText = None
 		else:
-			roleText = roleLabels.get(role, role.displayString)
+			# BEGIN JP PATCH
+			roleText = getRoleLabel(role, role.displayString)
+			# END JP PATCH
 	elif role is None:
 		role = propertyValues.get("_role")
+	# BEGIN JP PATCH
+	if (
+		config.conf["keyboard"]["nvdajpEnableKeyEvents"]
+		and isComposition
+		and role == controlTypes.Role.EDITABLETEXT
+	):
+		roleText = None
+	# END JP PATCH
 	value = propertyValues.get("value")
 	if value and role not in controlTypes.silentValuesForRoles:
 		textList.append(value)
@@ -779,8 +860,10 @@ def getPropertiesBraille(**propertyValues) -> str:  # noqa: C901
 				controlTypes.OutputReason.FOCUS,
 				states,
 				None,
-				positiveStateLabels,
-				negativeStateLabels,
+				# BEGIN JP PATCH
+				getPositiveStateLabels(),
+				getNegativeStateLabels(),
+				# END JP PATCH
 			),
 		)
 	if roleText:
@@ -807,12 +890,18 @@ def getPropertiesBraille(**propertyValues) -> str:  # noqa: C901
 			# {number} is replaced with the number of the item in the group.
 			# {total} is replaced with the total number of items in the group.
 			textList.append(_("{number} of {total}").format(number=indexInGroup, total=similarItemsInGroup))
-
 		if level is not None:
 			# Translators: Displayed in braille when an object (e.g. a tree view item) has a hierarchical level.
 			# %s is replaced with the level.
 			textList.append(_("lv %s") % positionInfo["level"])
-
+	# BEGIN JP PATCH https://github.com/nvdajp/nvdajp/issues/109
+	rowHeaderText = propertyValues.get("rowHeaderText")
+	if rowHeaderText:
+		textList.append(rowHeaderText)
+	columnHeaderText = propertyValues.get("columnHeaderText")
+	if columnHeaderText:
+		textList.append(columnHeaderText)
+	# END JP PATCH
 	if rowNumber:
 		if includeTableCellCoords and not cellCoordsText:
 			if rowSpan > 1:
@@ -828,9 +917,11 @@ def getPropertiesBraille(**propertyValues) -> str:  # noqa: C901
 				rowStr = _("r{rowNumber}").format(rowNumber=rowNumber)
 			textList.append(rowStr)
 	if columnNumber:
-		columnHeaderText = propertyValues.get("columnHeaderText")
-		if columnHeaderText:
-			textList.append(columnHeaderText)
+		# BEGIN JP PATCH (moved to above) https://github.com/nvdajp/nvdajp/issues/109
+		# columnHeaderText = propertyValues.get("columnHeaderText")
+		# if columnHeaderText:
+		# textList.append(columnHeaderText)
+		# END JP PATCH
 		if includeTableCellCoords and not cellCoordsText:
 			if columnSpan > 1:
 				# Translators: Displayed in braille for the table cell column numbers when a cell spans multiple columns.
@@ -902,6 +993,20 @@ def update(self):
 		)
 		description = obj.description if _shouldUseDescription else None
 		detailsRoles = obj.annotations.roles if obj.annotations else None
+		# BEGIN JP PATCH
+		columnHeaderText = None
+		try:
+			if hasattr(obj, "columnHeaderText") and config.conf["documentFormatting"]["reportTableHeaders"]:
+				columnHeaderText = obj.columnHeaderText
+		except NotImplementedError:
+			pass
+		rowHeaderText = None
+		try:
+			if hasattr(obj, "rowHeaderText") and config.conf["documentFormatting"]["reportTableHeaders"]:
+				rowHeaderText = obj.rowHeaderText
+		except NotImplementedError:
+			pass
+		# END JP PATCH
 		text = getPropertiesBraille(
 			name=name,
 			role=role,
@@ -918,6 +1023,10 @@ def update(self):
 			cellCoordsText=obj.cellCoordsText
 			if config.conf["documentFormatting"]["reportTableCellCoords"]
 			else None,
+			# BEGIN JP PATCH
+			columnHeaderText=columnHeaderText,
+			rowHeaderText=rowHeaderText,
+			# END JP PATCH
 			errorMessage=errorMessage,
 		)
 		if role == controlTypes.Role.MATH:
@@ -1010,7 +1119,9 @@ def getControlFieldBraille(
 	roleText = field.get("roleTextBraille", field.get("roleText"))
 	landmark = field.get("landmark")
 	if not roleText and role == controlTypes.Role.LANDMARK and landmark:
-		roleText = f"{roleLabels[controlTypes.Role.LANDMARK]} {landmarkLabels[landmark]}"
+		# BEGIN JP PATCH
+		roleText = f"{getRoleLabel(controlTypes.Role.LANDMARK)} {getLandmarkLabel(landmark)}"
+		# END JP PATCH
 
 	content = field.get("content")
 
@@ -1225,7 +1336,9 @@ def getFormatFieldBraille(field, fieldCache, isAtStart, formatConfig):
 		link = field.get("link")
 		oldLink = fieldCache.get("link")
 		if link and link != oldLink:
-			textList.append(roleLabels[controlTypes.Role.LINK])
+			# BEGIN JP PATCH
+			textList.append(getRoleLabel(controlTypes.Role.LINK))
+			# END JP PATCH
 	if formatConfig["reportComments"]:
 		comment = field.get("comment")
 		oldComment = fieldCache.get("comment") if fieldCache is not None else None
@@ -1468,7 +1581,9 @@ def _addTextWithFields(self, info, formatConfig, isSelection=False):
 									formatConfig,
 								)
 								if not presCat or presCat is field.PRESCAT_LAYOUT:
-									textList.append(positiveStateLabels[controlTypes.State.CLICKABLE])
+									# BEGIN JP PATCH
+									textList.append(getPositiveStateLabel(controlTypes.State.CLICKABLE))
+									# END JP PATCH
 								inClickable = True
 						text = info.getControlFieldBraille(field, ctrlFields, True, formatConfig)
 						if text:

```