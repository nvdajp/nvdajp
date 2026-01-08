# Diff for: `source\gui\settingsDialogs.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\gui\settingsDialogs.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\settingsDialogs.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\settingsDialogs.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\settingsDialogs.py"
index 73559b0..12a8f2b 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\settingsDialogs.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\settingsDialogs.py"
@@ -5,89 +5,102 @@
 # Thomas Stivers, Julien Cochuyt, Peter Vágner, Cyrille Bougot, Mesar Hameed,
 # Łukasz Golonka, Aaron Cannon, Adriani90, André-Abush Clause, Dawid Pieper,
 # Takuya Nishimoto, jakubl7545, Tony Malykh, Rob Meredith,
-# Burman's Computer and Education Ltd, hwf1324, Cary-rowen, Christopher Proß.
+# Burman's Computer and Education Ltd, hwf1324, Cary-rowen, Christopher Proß, Tianze
+# Neil Soiffer, Ryan McCleary.
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
-from collections.abc import Container
-import logging
-from abc import ABCMeta, abstractmethod
 import copy
+import logging
 import os
-from enum import IntEnum
-from locale import strxfrm
 import re
 import typing
+from abc import ABCMeta, abstractmethod
+from collections.abc import Container
+from enum import IntEnum
+from locale import strxfrm
+from typing import (
+	Any,
+	Callable,
+	List,
+	Optional,
+	Set,
+	Type,
+)
+
+import audio
+import audioDucking
+import braille
+import brailleInput
+import brailleTables
+import characterProcessing
+import config
+import core
+import globalVars
+import installer
+import keyboardHandler
+import languageHandler
+import logHandler
+import queueHandler
 import requests
+import speech
+import systemUtils
+import vision
+import vision.providerBase
+import vision.providerInfo
+import winUser
 import wx
-import wx.adv
+from wx.lib import scrolledpanel
 from NVDAState import WritePaths
 
+import screenCurtain._screenCurtain
 from utils import mmdevice
 from vision.providerBase import VisionEnhancementProviderSettings
 from wx.lib.expando import ExpandoTextCtrl
 import wx.lib.newevent
-import winUser
-import logHandler
-import installer
-from synthDriverHandler import changeVoice, getSynth, getSynthList, setSynth, SynthDriver
-import config
+from addonStore.models.channel import UpdateChannel
 from config.configFlags import (
 	AddonsAutomaticUpdate,
 	NVDAKey,
+	OutputMode,
+	ParagraphStartMarker,
 	RemoteConnectionMode,
 	RemoteServerType,
-	ShowMessages,
-	TetherTo,
-	ParagraphStartMarker,
+	ReportCellBorders,
 	ReportLineIndentation,
+	ReportNotSupportedLanguage,
+	ReportSpellingErrors,
 	ReportTableHeaders,
-	ReportCellBorders,
-	OutputMode,
+	ShowMessages,
+	TetherTo,
 	TypingEcho,
-	ReportNotSupportedLanguage,
+	LoggingLevel,
 )
-import languageHandler
-import speech
-import systemUtils
+from logHandler import log
+from synthDriverHandler import SynthDriver, changeVoice, getSynth, getSynthList, setSynth
+from utils.displayString import DisplayStringEnum
+
 import gui
 import gui.contextHelp
-import globalVars
-from logHandler import log
-import audio
-import audioDucking
-import queueHandler
-import braille
-import brailleTables
-import brailleInput
-from addonStore.models.channel import UpdateChannel
-import vision
-import vision.providerInfo
-import vision.providerBase
-from typing import (
-	Any,
-	Callable,
-	List,
-	Optional,
-	Set,
-)
-import core
-import keyboardHandler
-import characterProcessing
+import screenCurtain
+import api
+import ui
 from . import guiHelper
 
 try:
 	import updateCheck
 except RuntimeError:
 	updateCheck = None
-from . import nvdaControls
-from autoSettingsUtils.utils import UnsupportedConfigParameterError
-from autoSettingsUtils.autoSettings import AutoSettings
-from autoSettingsUtils.driverSetting import BooleanDriverSetting, NumericDriverSetting, DriverSetting
+import time
+import weakref
+
 import touchHandler
 import winVersion
-import weakref
-import time
+from autoSettingsUtils.autoSettings import AutoSettings
+from autoSettingsUtils.driverSetting import BooleanDriverSetting, DriverSetting, NumericDriverSetting
+from autoSettingsUtils.utils import UnsupportedConfigParameterError
+
+from . import nvdaControls
 from .dpiScalingHelper import DpiScalingHelperMixinWithoutInit
 
 #: The size that settings panel text descriptions should be wrapped at.
@@ -583,7 +596,7 @@ def makeSettings(self, settingsSizer):
 		# The provided column header is just a placeholder, as it is hidden due to the wx.LC_NO_HEADER style flag.
 		self.catListCtrl.InsertColumn(0, categoriesLabelText)
 
-		self.container = nvdaControls.TabbableScrolledPanel(
+		self.container = scrolledpanel.ScrolledPanel(
 			parent=self,
 			style=wx.TAB_TRAVERSAL | wx.BORDER_THEME,
 			size=containerDim,
@@ -789,18 +802,6 @@ class GeneralSettingsPanel(SettingsPanel):
 	# Translators: This is the label for the general settings panel.
 	title = _("General")
 	helpId = "GeneralSettings"
-	LOG_LEVELS = (
-		# Translators: One of the log levels of NVDA (the disabled mode turns off logging completely).
-		(log.OFF, _("disabled")),
-		# Translators: One of the log levels of NVDA (the info mode shows info as NVDA runs).
-		(log.INFO, _("info")),
-		# Translators: One of the log levels of NVDA (the debug warning shows debugging messages and warnings as NVDA runs).
-		(log.DEBUGWARNING, _("debug warning")),
-		# Translators: One of the log levels of NVDA (the input/output shows keyboard commands and/or braille commands as well as speech and/or braille output of NVDA).
-		(log.IO, _("input/output")),
-		# Translators: One of the log levels of NVDA (the debug mode shows debug messages as NVDA runs).
-		(log.DEBUG, _("debug")),
-	)
 
 	def makeSettings(self, settingsSizer):
 		settingsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
@@ -859,27 +860,6 @@ def makeSettings(self, settingsSizer):
 		self.playStartAndExitSoundsCheckBox.SetValue(config.conf["general"]["playStartAndExitSounds"])
 		settingsSizerHelper.addItem(self.playStartAndExitSoundsCheckBox)
 
-		# Translators: The label for a setting in general settings to select logging level of NVDA as it runs
-		# (available options and what they are logging are found under comments for the logging level messages
-		# themselves).
-		logLevelLabelText = _("L&ogging level:")
-		logLevelChoices = [name for level, name in self.LOG_LEVELS]
-		self.logLevelList = settingsSizerHelper.addLabeledControl(
-			logLevelLabelText,
-			wx.Choice,
-			choices=logLevelChoices,
-		)
-		self.bindHelpEvent("GeneralSettingsLogLevel", self.logLevelList)
-		curLevel = log.getEffectiveLevel()
-		if logHandler.isLogLevelForced():
-			self.logLevelList.Disable()
-		for index, (level, name) in enumerate(self.LOG_LEVELS):
-			if level == curLevel:
-				self.logLevelList.SetSelection(index)
-				break
-		else:
-			log.debugWarning("Could not set log level list to current log level")
-
 		# Translators: The label for a setting in general settings to allow NVDA to start after logging onto
 		# Windows (if checked, NVDA will start automatically after logging into Windows; if not, user must
 		# start NVDA by pressing the shortcut key (CTRL+Alt+N by default).
@@ -920,7 +900,6 @@ def makeSettings(self, settingsSizer):
 			self.copySettingsButton.Disable()
 		settingsSizerHelper.addItem(self.copySettingsButton)
 
-		if updateCheck:
 		item = self.autoCheckForUpdatesCheckBox = wx.CheckBox(
 			self,
 			# Translators: The label of a checkbox in general settings to toggle automatic checking for updated versions of NVDA.
@@ -929,7 +908,8 @@ def makeSettings(self, settingsSizer):
 		)
 		self.bindHelpEvent("GeneralSettingsCheckForUpdates", self.autoCheckForUpdatesCheckBox)
 		item.Value = config.conf["update"]["autoCheck"]
-			if globalVars.appArgs.secure:
+		if not updateCheck:
+			item.Value = False
 			item.Disable()
 		settingsSizerHelper.addItem(item)
 
@@ -941,19 +921,8 @@ def makeSettings(self, settingsSizer):
 		)
 		self.bindHelpEvent("GeneralSettingsNotifyPendingUpdates", self.notifyForPendingUpdateCheckBox)
 		item.Value = config.conf["update"]["startupNotification"]
-			if globalVars.appArgs.secure:
-				item.Disable()
-			settingsSizerHelper.addItem(item)
-			item = self.allowUsageStatsCheckBox = wx.CheckBox(
-				self,
-				# Translators: The label of a checkbox in general settings to toggle allowing of usage stats gathering
-				label=_("Allow NV Access to gather NVDA usage statistics").replace(
-					"NV Access", _("NVDA Japanese Team")
-				),
-			)
-			self.bindHelpEvent("GeneralSettingsGatherUsageStats", self.allowUsageStatsCheckBox)
-			item.Value = config.conf["update"]["allowUsageStats"]
-			if globalVars.appArgs.secure:
+		if not updateCheck:
+			item.Value = False
 			item.Disable()
 		settingsSizerHelper.addItem(item)
 
@@ -986,7 +955,7 @@ def makeSettings(self, settingsSizer):
 		self.bindHelpEvent("UpdateMirror", mirrorBox)
 		self.mirrorURLTextBox.Bind(wx.EVT_CHAR_HOOK, self._enterTriggersOnChangeMirrorURL)
 		changeMirrorBtn.Bind(wx.EVT_BUTTON, self.onChangeMirrorURL)
-			if globalVars.appArgs.secure:
+		if not updateCheck:
 			mirrorBox.Disable()
 
 		item = self.preventDisplayTurningOffCheckBox = wx.CheckBox(
@@ -1097,10 +1066,6 @@ def onSave(self):
 		config.conf["general"]["saveConfigurationOnExit"] = self.saveOnExitCheckBox.IsChecked()
 		config.conf["general"]["askToExit"] = self.askToExitCheckBox.IsChecked()
 		config.conf["general"]["playStartAndExitSounds"] = self.playStartAndExitSoundsCheckBox.IsChecked()
-		logLevel = self.LOG_LEVELS[self.logLevelList.GetSelection()][0]
-		if not logHandler.isLogLevelForced():
-			config.conf["general"]["loggingLevel"] = logging.getLevelName(logLevel)
-			logHandler.setLogLevelFromConfig()
 		if self.startAfterLogonCheckBox.IsEnabled():
 			config.setStartAfterLogon(self.startAfterLogonCheckBox.GetValue())
 		if self.startOnLogonScreenCheckBox.IsEnabled():
@@ -1115,7 +1080,6 @@ def onSave(self):
 				)
 		if updateCheck:
 			config.conf["update"]["autoCheck"] = self.autoCheckForUpdatesCheckBox.IsChecked()
-			config.conf["update"]["allowUsageStats"] = self.allowUsageStatsCheckBox.IsChecked()
 			config.conf["update"]["startupNotification"] = self.notifyForPendingUpdateCheckBox.IsChecked()
 			updateCheck.terminate()
 			updateCheck.initialize()
@@ -1181,6 +1145,7 @@ def onRestartNowButton(self, evt):
 		queueHandler.queueFunction(queueHandler.eventQueue, core.restart)
 
 
+# BEGIN JP PATCH (Japanese language settings panel)
 class LanguageSettingsPanel(SettingsPanel):
 	# Translators: This is the label for the language settings dialog.
 	title = _("Language Settings")
@@ -1299,6 +1264,9 @@ def onSave(self):
 		config.conf["language"]["halfShapePitchChange"] = self.halfShapePitchChangeEdit.Value
 
 
+# END JP PATCH
+
+
 class SpeechSettingsPanel(SettingsPanel):
 	# Translators: This is the label for the speech panel
 	title = _("Speech")
@@ -2244,7 +2212,7 @@ def makeSettings(self, settingsSizer):
 		)
 		self.bindHelpEvent("KeyboardSettingsAlertForSpellingErrors", self.alertForSpellingErrorsCheckBox)
 		self.alertForSpellingErrorsCheckBox.SetValue(config.conf["keyboard"]["alertForSpellingErrors"])
-		if not config.conf["documentFormatting"]["reportSpellingErrors"]:
+		if not config.conf["documentFormatting"]["reportSpellingErrors2"]:
 			self.alertForSpellingErrorsCheckBox.Disable()
 
 		# Translators: This is the label for a checkbox in the
@@ -2598,6 +2566,15 @@ def makeSettings(self, settingsSizer):
 			config.conf["presentation"]["guessObjectPositionInformationWhenUnavailable"],
 		)
 
+		# Translators: This is the label for a checkbox in the
+		# object presentation settings panel.
+		reportMultiSelectText = _("Report when objects support &multiple selection")
+		self.reportMultiSelectCheckBox = sHelper.addItem(wx.CheckBox(self, label=reportMultiSelectText))
+		self.bindHelpEvent("ReportMultiSelect", self.reportMultiSelectCheckBox)
+		self.reportMultiSelectCheckBox.SetValue(
+			config.conf["presentation"]["reportMultiSelect"],
+		)
+
 		# Translators: This is the label for a checkbox in the
 		# object presentation settings panel.
 		descriptionText = _("Report object &descriptions")
@@ -2662,6 +2639,7 @@ def onSave(self):
 		config.conf["presentation"]["guessObjectPositionInformationWhenUnavailable"] = (
 			self.guessPositionInfoCheckBox.IsChecked()
 		)
+		config.conf["presentation"]["reportMultiSelect"] = self.reportMultiSelectCheckBox.IsChecked()
 		config.conf["presentation"]["reportObjectDescriptions"] = self.descriptionCheckBox.IsChecked()
 		config.conf["presentation"]["progressBarUpdates"]["progressBarOutputMode"] = self.progressLabels[
 			self.progressList.GetSelection()
@@ -2811,6 +2789,387 @@ def onSave(self):
 		)
 
 
+class MathSettingsPanel(SettingsPanel):
+	# Translators: Title of the math settings panel.
+	title = pgettext("math", "Math")
+	helpId = "MathSettings"
+	panelDescription = pgettext(
+		"math",
+		# Translators: The description of the math settings panel.
+		"The following options control the presentation of mathematical content.",
+	)
+
+	def _getSpeechStyleDisplayString(self, configValue: str) -> str:
+		"""Helper function to get the display string for a speech style config value.
+
+		:param configValue: The config value to find the display string for
+		:return: The display string to show in the UI
+		"""
+		from mathPres.MathCAT.preferences import SpeechStyleOption
+
+		# Check if it's a known enum value by comparing directly
+		knownStyleValues = [style.value for style in SpeechStyleOption]
+		if configValue in knownStyleValues:
+			enumOption = SpeechStyleOption(configValue)
+			return enumOption.displayString
+		else:
+			# Not a known enum, so the config value IS the display string
+			return configValue
+
+	def _getEnumIndexFromConfigValue(
+		self,
+		enumClass: Type[DisplayStringEnum],
+		configValue: Any,
+	) -> int:
+		"""Helper function to get the index of an enum option based on its config value.
+
+		:param enumClass: The DisplayStringEnum class to search in
+		:param configValue: The config value to find the index for
+		:return: The index of the enum option with the matching value
+		"""
+		try:
+			return list(enumClass).index(enumClass(configValue))
+		except (ValueError, KeyError):
+			# If the config value is not found, default to the first option
+			return 0
+
+	def _getEnumValueFromSelection(
+		self,
+		enumClass: Type[DisplayStringEnum],
+		selectionIndex: int,
+	) -> Any:
+		"""Helper function to get the config value from a selection index.
+
+		:param enumClass: The DisplayStringEnum class to get the value from
+		:param selectionIndex: The index of the selected option
+		:return: The config value of the selected enum option
+		"""
+		try:
+			return list(enumClass)[selectionIndex].value
+		except (IndexError, AttributeError):
+			# If the selection is invalid, return the first option's value
+			return list(enumClass)[0].value
+
+	def makeSettings(self, settingsSizer: wx.BoxSizer) -> None:
+		from mathPres.MathCAT import localization, preferences
+		from mathPres.MathCAT.preferences import (
+			ImpairmentOption,
+			DecimalSeparatorOption,
+			VerbosityOption,
+			ChemistryOption,
+			NavModeOption,
+			NavVerbosityOption,
+			CopyAsOption,
+			BrailleNavHighlightOption,
+			getSpeechStyleChoicesWithTranslations,
+		)
+
+		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
+
+		sHelper.addItem(wx.StaticText(self, label=self.panelDescription))
+
+		speechGroupText = pgettext("math", "Speech")
+		speechGroupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=speechGroupText)
+		speechGroupBox = speechGroupSizer.GetStaticBox()
+		speechGroup = guiHelper.BoxSizerHelper(self, sizer=speechGroupSizer)
+		sHelper.addItem(speechGroup)
+
+		# Translators: Select an impairment for MathCAT
+		impairmentText = pgettext("math", "Impairment")
+		self.impairmentList = speechGroup.addLabeledControl(
+			impairmentText,
+			wx.Choice,
+			choices=[option.displayString for option in ImpairmentOption],
+		)
+		self.bindHelpEvent("MathSpeechImpairment", self.impairmentList)
+		self.impairmentList.SetSelection(
+			self._getEnumIndexFromConfigValue(ImpairmentOption, config.conf["math"]["speech"]["impairment"]),
+		)
+
+		# Translators: MathCAT language option
+		languageText = pgettext("math", "Language")
+		self.languageOptions, self.languageCodes = localization.getLanguages()
+		self.languageList = speechGroup.addLabeledControl(
+			languageText,
+			wx.Choice,
+			choices=self.languageOptions,
+		)
+		self.bindHelpEvent("MathSpeechLanguage", self.languageList)
+		languageIndex = self.languageCodes.index(config.conf["math"]["speech"]["language"])
+		self.languageList.SetSelection(languageIndex)
+
+		# Translators: MathCAT decimal separator option.
+		decimalSeparatorText = pgettext("math", "Decimal separator for numbers:")
+		self.decimalSeparatorList = speechGroup.addLabeledControl(
+			decimalSeparatorText,
+			wx.Choice,
+			choices=[option.displayString for option in DecimalSeparatorOption],
+		)
+		self.bindHelpEvent("MathSpeechDecimalSeparator", self.decimalSeparatorList)
+		self.decimalSeparatorList.SetSelection(
+			self._getEnumIndexFromConfigValue(
+				DecimalSeparatorOption,
+				config.conf["math"]["other"]["decimalSeparator"],
+			),
+		)
+
+		# Translators: Select a speech style.
+		speechStyleText = pgettext("math", "Speech style")
+		self.speechStyleOptions = getSpeechStyleChoicesWithTranslations(
+			config.conf["math"]["speech"]["language"],
+		)
+		self.speechStyleList = speechGroup.addLabeledControl(
+			speechStyleText,
+			wx.Choice,
+			choices=self.speechStyleOptions,
+		)
+		self.bindHelpEvent("MathSpeechStyle", self.speechStyleList)
+		speechStyleDisplayString = self._getSpeechStyleDisplayString(
+			config.conf["math"]["speech"]["speechStyle"],
+		)
+		self.speechStyleList.SetStringSelection(speechStyleDisplayString)
+
+		# Translators: MathCAT's verbosity setting
+		speechAmountText = pgettext("math", "Speech verbosity")
+		self.speechAmountList = speechGroup.addLabeledControl(
+			speechAmountText,
+			wx.Choice,
+			choices=[option.displayString for option in VerbosityOption],
+		)
+		self.bindHelpEvent("MathSpeechVerbosity", self.speechAmountList)
+		self.speechAmountList.SetSelection(
+			self._getEnumIndexFromConfigValue(VerbosityOption, config.conf["math"]["speech"]["verbosity"]),
+		)
+
+		# Translators: MathCAT's relative speed setting
+		relativeSpeedText = pgettext("math", "Relative speech rate")
+		self.relativeSpeedSlider: nvdaControls.EnhancedInputSlider = speechGroup.addLabeledControl(
+			relativeSpeedText,
+			nvdaControls.EnhancedInputSlider,
+			minValue=10,
+			maxValue=100,
+		)
+		self.bindHelpEvent("MathRelativeSpeed", self.relativeSpeedSlider)
+		self.relativeSpeedSlider.SetValue(config.conf["math"]["speech"]["mathRate"])
+
+		# Translators: label for slider that specifies relative factor to increase or decrease pauses in the math speech
+		pauseFactorText = pgettext("math", "Pause factor")
+		self.pauseFactorSlider: nvdaControls.EnhancedInputSlider = speechGroup.addLabeledControl(
+			pauseFactorText,
+			nvdaControls.EnhancedInputSlider,
+			minValue=0,
+			maxValue=14,
+		)
+		self.bindHelpEvent("MathSpeechPauseFactor", self.pauseFactorSlider)
+		self.pauseFactorSlider.SetValue(config.conf["math"]["speech"]["pauseFactor"])
+
+		# Translators: label for check box controlling a beep sound when math speech starts/ends
+		speechSoundText = pgettext("math", "Make a sound when starting/ending math speech")
+		self.speechSoundCheckBox = speechGroup.addItem(wx.CheckBox(speechGroupBox, label=speechSoundText))
+		self.bindHelpEvent("MathSpeechSound", self.speechSoundCheckBox)
+		self.speechSoundCheckBox.SetValue(config.conf["math"]["speech"]["speechSound"] != "None")
+
+		# Translators: label for combobox to specify how verbose/terse the speech should be
+		speechForChemicalText = pgettext("math", "Speech for chemical formulas")
+		self.speechForChemicalList = speechGroup.addLabeledControl(
+			speechForChemicalText,
+			wx.Choice,
+			choices=[option.displayString for option in ChemistryOption],
+		)
+		self.bindHelpEvent("MathSpeechForChemical", self.speechForChemicalList)
+		self.speechForChemicalList.SetSelection(
+			self._getEnumIndexFromConfigValue(ChemistryOption, config.conf["math"]["speech"]["chemistry"]),
+		)
+
+		# Translators: Text for the navigation group.
+		navGroupText = pgettext("math", "Navigation")
+		navGroupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=navGroupText)
+		navGroupBox = navGroupSizer.GetStaticBox()
+		navGroup = guiHelper.BoxSizerHelper(self, sizer=navGroupSizer)
+		sHelper.addItem(navGroup)
+
+		# Translators: label for combobox to specify one of three modes use to navigate math expressions
+		navModeText = pgettext("math", "Navigation mode to use when beginning to navigate an equation")
+		self.navModeList = speechGroup.addLabeledControl(
+			navModeText,
+			wx.Choice,
+			choices=[option.displayString for option in NavModeOption],
+		)
+		self.bindHelpEvent("MathNavMode", self.navModeList)
+		self.navModeList.SetSelection(
+			self._getEnumIndexFromConfigValue(NavModeOption, config.conf["math"]["navigation"]["navMode"]),
+		)
+
+		# Translators: label for combobox to specify whether the expression is spoken or described (an overview)
+		navSpeechText = pgettext("math", "Navigation speech to use when beginning to navigate an equation")
+		navSpeechOptions: list[str] = [
+			# Translators: "Speak" the expression after moving to it
+			pgettext("math", "Speak"),
+			# Translators: "Describe" the expression after moving to it ("overview is a synonym")
+			pgettext("math", "Describe/overview"),
+		]
+		self.navSpeechList = speechGroup.addLabeledControl(
+			navSpeechText,
+			wx.Choice,
+			choices=navSpeechOptions,
+		)
+		self.bindHelpEvent("MathNavSpeech", self.navSpeechList)
+		if config.conf["math"]["navigation"]["overview"]:
+			self.navSpeechList.SetSelection(1)
+		else:
+			self.navSpeechList.SetSelection(0)
+
+		# Translators: label for check box controlling a beep sound when math speech starts/ends
+		resetNavSpeechText = pgettext("math", "Make a sound when starting/ending math speech")
+		self.resetNavSpeechCheckBox = navGroup.addItem(wx.CheckBox(navGroupBox, label=resetNavSpeechText))
+		self.bindHelpEvent("MathNavReset", self.resetNavSpeechCheckBox)
+		self.resetNavSpeechCheckBox.SetValue(config.conf["math"]["navigation"]["resetOverview"])
+
+		# Translators: label for checkbox that controls whether arrow keys move out of fractions, etc.,
+		# or whether you have to manually back out of the fraction, etc.
+		navAutoZoomText = pgettext("math", "Automatic zoom out of 2D notations")
+		self.navAutoZoomCheckBox = navGroup.addItem(wx.CheckBox(navGroupBox, label=navAutoZoomText))
+		self.bindHelpEvent("MathNavAutoZoom", self.navAutoZoomCheckBox)
+		self.navAutoZoomCheckBox.SetValue(config.conf["math"]["navigation"]["autoZoomOut"])
+
+		# Translators: label for combobox down to specify whether you want a terse or verbose reading of navigation commands
+		navSpeechAmountText = pgettext("math", "Speech amount for navigation")
+		self.navSpeechAmountList = navGroup.addLabeledControl(
+			navSpeechAmountText,
+			wx.Choice,
+			choices=[option.displayString for option in NavVerbosityOption],
+		)
+		self.bindHelpEvent(
+			"MathNavSpeechAmount",
+			self.navSpeechAmountList,
+		)
+		self.navSpeechAmountList.SetSelection(
+			self._getEnumIndexFromConfigValue(
+				NavVerbosityOption,
+				config.conf["math"]["navigation"]["navVerbosity"],
+			),
+		)
+
+		# Translators: label for combobox to specify how math will be copied to the clipboard
+		navCopyAsText = pgettext("math", "Copy math as")
+		self.navCopyAsList = navGroup.addLabeledControl(
+			navCopyAsText,
+			wx.Choice,
+			choices=[option.displayString for option in CopyAsOption],
+		)
+		self.bindHelpEvent("MathNavCopyAs", self.navCopyAsList)
+		self.navCopyAsList.SetSelection(
+			self._getEnumIndexFromConfigValue(CopyAsOption, config.conf["math"]["navigation"]["copyAs"]),
+		)
+
+		# Translators: Text for the braille group.
+		brailleGroupText = pgettext("math", "Braille")
+		brailleGroupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=brailleGroupText)
+		brailleGroup = guiHelper.BoxSizerHelper(self, sizer=brailleGroupSizer)
+		sHelper.addItem(brailleGroup)
+
+		# Translators: label for combobox to specify which braille code to use
+		brailleMathCodeText = pgettext("math", "Braille math code for refreshable displays")
+		brailleMathCodeOptions: list[str] = preferences.getBrailleCodes()
+		self.brailleMathCodeList = navGroup.addLabeledControl(
+			brailleMathCodeText,
+			wx.Choice,
+			choices=brailleMathCodeOptions,
+		)
+		self.bindHelpEvent("MathBrailleCode", self.brailleMathCodeList)
+		self.brailleMathCodeList.SetStringSelection(config.conf["math"]["braille"]["brailleCode"])
+
+		# Translators: label for combobox to specify how braille dots should be modified when navigating/selecting subexprs
+		brailleHighlightsText = pgettext("math", "Highlight the current navigation node with dots 7 and 8")
+		self.brailleHighlightsList = navGroup.addLabeledControl(
+			brailleHighlightsText,
+			wx.Choice,
+			choices=[option.displayString for option in BrailleNavHighlightOption],
+		)
+		self.bindHelpEvent("MathBrailleHighlights", self.brailleHighlightsList)
+		self.brailleHighlightsList.SetSelection(
+			self._getEnumIndexFromConfigValue(
+				BrailleNavHighlightOption,
+				config.conf["math"]["braille"]["brailleNavHighlight"],
+			),
+		)
+
+	def onSave(self):
+		import math
+
+		from mathPres.MathCAT.preferences import MathCATUserPreferences
+		from mathPres.MathCAT.preferences import (
+			ImpairmentOption,
+			VerbosityOption,
+			DecimalSeparatorOption,
+			ChemistryOption,
+			NavModeOption,
+			NavVerbosityOption,
+			CopyAsOption,
+			BrailleNavHighlightOption,
+			PauseFactor,
+			getSpeechStyleConfigValue,
+		)
+
+		mathConf = config.conf["math"]
+		mathConf["speech"]["impairment"] = self._getEnumValueFromSelection(
+			ImpairmentOption,
+			self.impairmentList.GetSelection(),
+		)
+		mathConf["speech"]["language"] = self.languageCodes[self.languageList.GetSelection()]
+		mathConf["other"]["decimalSeparator"] = self._getEnumValueFromSelection(
+			DecimalSeparatorOption,
+			self.decimalSeparatorList.GetSelection(),
+		)
+		mathConf["speech"]["speechStyle"] = getSpeechStyleConfigValue(
+			self.speechStyleList.GetStringSelection(),
+		)
+		mathConf["speech"]["verbosity"] = self._getEnumValueFromSelection(
+			VerbosityOption,
+			self.speechAmountList.GetSelection(),
+		)
+		mathConf["speech"]["mathRate"] = self.relativeSpeedSlider.GetValue()
+		pfSlider: int = self.pauseFactorSlider.GetValue()
+		pauseFactor: int = (
+			0
+			if pfSlider == 0
+			else round(PauseFactor.SCALE.value * math.pow(PauseFactor.LOG_BASE.value, pfSlider))
+		)  # avoid log(0)
+		mathConf["speech"]["pauseFactor"] = pauseFactor
+		if self.speechSoundCheckBox.GetValue():
+			mathConf["speech"]["speechSound"] = "Beep"
+		else:
+			mathConf["speech"]["speechSound"] = "None"
+		mathConf["speech"]["chemistry"] = self._getEnumValueFromSelection(
+			ChemistryOption,
+			self.speechForChemicalList.GetSelection(),
+		)
+		mathConf["navigation"]["navMode"] = self._getEnumValueFromSelection(
+			NavModeOption,
+			self.navModeList.GetSelection(),
+		)
+		mathConf["navigation"]["resetNavMode"] = self.resetNavSpeechCheckBox.GetValue()
+		mathConf["navigation"]["navVerbosity"] = self._getEnumValueFromSelection(
+			NavVerbosityOption,
+			self.navSpeechAmountList.GetSelection(),
+		)
+		mathConf["navigation"]["overview"] = self.navSpeechList.GetSelection() != 0
+		mathConf["navigation"]["resetOverview"] = self.resetNavSpeechCheckBox.GetValue()
+		mathConf["navigation"]["autoZoomOut"] = self.navAutoZoomCheckBox.GetValue()
+		mathConf["navigation"]["copyAs"] = self._getEnumValueFromSelection(
+			CopyAsOption,
+			self.navCopyAsList.GetSelection(),
+		)
+
+		mathConf["braille"]["brailleNavHighlight"] = self._getEnumValueFromSelection(
+			BrailleNavHighlightOption,
+			self.brailleHighlightsList.GetSelection(),
+		)
+		mathConf["braille"]["brailleCode"] = self.brailleMathCodeList.GetStringSelection()
+		mcPrefs: MathCATUserPreferences = MathCATUserPreferences.fromNVDAConfig()
+		mcPrefs.save()
+
+
 class DocumentFormattingPanel(SettingsPanel):
 	# Translators: This is the label for the document formatting panel.
 	title = _("Document Formatting")
@@ -2904,7 +3263,7 @@ def makeSettings(self, settingsSizer):
 
 		# Translators: This is the label for a checkbox in the
 		# document formatting settings panel.
-		commentsText = _("No&tes and comments")
+		commentsText = _("Commen&ts")
 		self.commentsCheckBox = docInfoGroup.addItem(wx.CheckBox(docInfoBox, label=commentsText))
 		self.commentsCheckBox.SetValue(config.conf["documentFormatting"]["reportComments"])
 
@@ -2920,11 +3279,23 @@ def makeSettings(self, settingsSizer):
 		self.revisionsCheckBox = docInfoGroup.addItem(wx.CheckBox(docInfoBox, label=revisionsText))
 		self.revisionsCheckBox.SetValue(config.conf["documentFormatting"]["reportRevisions"])
 
-		# Translators: This is the label for a checkbox in the
+		self._spellingErrorsChecklist = docInfoGroup.addLabeledControl(
+			# Translators: This is the label for a checklist in the
 			# document formatting settings panel.
-		spellingErrorText = _("Spelling e&rrors")
-		self.spellingErrorsCheckBox = docInfoGroup.addItem(wx.CheckBox(docInfoBox, label=spellingErrorText))
-		self.spellingErrorsCheckBox.SetValue(config.conf["documentFormatting"]["reportSpellingErrors"])
+			_("Spelling or grammar e&rrors"),
+			nvdaControls.CustomCheckListBox,
+			choices=[i.displayString for i in ReportSpellingErrors],
+		)
+		checkedItems = []
+		for i, mode in enumerate(ReportSpellingErrors):
+			if config.conf["documentFormatting"]["reportSpellingErrors2"] & mode.value:
+				checkedItems.append(i)
+		self._spellingErrorsChecklist.SetCheckedItems(checkedItems)
+		self._spellingErrorsChecklist.Select(0)
+		self.bindHelpEvent(
+			"reportSpellingErrors",
+			self._spellingErrorsChecklist,
+		)
 
 		# Translators: This is the label for a group of document formatting options in the
 		# document formatting settings panel
@@ -3147,7 +3518,11 @@ def onSave(self):
 		config.conf["documentFormatting"]["reportHighlight"] = self.highlightCheckBox.IsChecked()
 		config.conf["documentFormatting"]["reportAlignment"] = self.alignmentCheckBox.IsChecked()
 		config.conf["documentFormatting"]["reportStyle"] = self.styleCheckBox.IsChecked()
-		config.conf["documentFormatting"]["reportSpellingErrors"] = self.spellingErrorsCheckBox.IsChecked()
+		config.conf["documentFormatting"]["reportSpellingErrors2"] = sum(
+			mode.value
+			for (n, mode) in enumerate(ReportSpellingErrors)
+			if self._spellingErrorsChecklist.IsChecked(n)
+		)
 		config.conf["documentFormatting"]["reportPage"] = self.pageCheckBox.IsChecked()
 		config.conf["documentFormatting"]["reportLineNumber"] = self.lineNumberCheckBox.IsChecked()
 		config.conf["documentFormatting"]["reportLineIndentation"] = self.lineIndentationCombo.GetSelection()
@@ -3757,6 +4132,53 @@ def onSave(self):
 				_remoteClient.terminate()
 
 
+class LocalCaptionerSettingsPanel(SettingsPanel):
+	"""Settings panel for Local captioner configuration."""
+
+	# Translators: This is the label for the local captioner settings panel.
+	title = pgettext("imageDesc", "AI Image Descriptions")
+	helpId = "LocalCaptionerSettings"
+	panelDescription = pgettext(
+		"imageDesc",
+		# Translators: This is a label appearing on the AI Image Descriptions settings panel.
+		"Warning: AI image descriptions are experimental. "
+		"Do not use this feature in circumstances where inaccurate descriptions could cause harm.",
+	)
+
+	def makeSettings(self, settingsSizer: wx.BoxSizer):
+		"""Create the settings controls for the panel.
+
+		:param settingsSizer: The sizer to add settings controls to.
+		"""
+
+		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
+
+		self.windowText = sHelper.addItem(
+			wx.StaticText(self, label=self.panelDescription),
+		)
+		self.windowText.Wrap(self.scaleSize(PANEL_DESCRIPTION_WIDTH))
+
+		self.enable = sHelper.addItem(
+			# Translators: A configuration in settings dialog.
+			wx.CheckBox(self, label=pgettext("imageDesc", "Enable image captioner")),
+		)
+		self.enable.SetValue(config.conf["automatedImageDescriptions"]["enable"])
+		self.bindHelpEvent("LocalCaptionToggle", self.enable)
+
+	def onSave(self) -> None:
+		"""Save the configuration settings."""
+		enabled = self.enable.GetValue()
+		oldEnabled = config.conf["automatedImageDescriptions"]["enable"]
+
+		if enabled != oldEnabled:
+			import _localCaptioner
+
+			if enabled != _localCaptioner.isModelLoaded():
+				_localCaptioner.toggleImageCaptioning()
+
+		config.conf["automatedImageDescriptions"]["enable"] = enabled
+
+
 class TouchInteractionPanel(SettingsPanel):
 	# Translators: This is the label for the touch interaction settings panel.
 	title = _("Touch Interaction")
@@ -3820,10 +4242,19 @@ def makeSettings(self, settingsSizer):
 		self.bindHelpEvent("Win10OcrSettingsAutoRefresh", self.autoRefreshCheckbox)
 		self.autoRefreshCheckbox.SetValue(config.conf["uwpOcr"]["autoRefresh"])
 
+		# Translators: The label for a setting in OCR settings to automatically say all on result.
+		autoSayAllText = _("Automatically say all on result")
+		self.autoSayAllOnResultCheckbox = sHelper.addItem(
+			wx.CheckBox(self, label=autoSayAllText),
+		)
+		self.bindHelpEvent("Win10OcrSettingsAutoSayAllOnResult", self.autoSayAllOnResultCheckbox)
+		self.autoSayAllOnResultCheckbox.SetValue(config.conf["uwpOcr"]["autoSayAllOnResult"])
+
 	def onSave(self):
 		lang = self.languageCodes[self.languageChoice.Selection]
 		config.conf["uwpOcr"]["language"] = lang
 		config.conf["uwpOcr"]["autoRefresh"] = self.autoRefreshCheckbox.IsChecked()
+		config.conf["uwpOcr"]["autoSayAllOnResult"] = self.autoSayAllOnResultCheckbox.IsChecked()
 
 
 class AdvancedPanelControls(
@@ -4181,17 +4612,6 @@ def __init__(self, parent):
 		self.trimLeadingSilenceCheckBox.SetValue(config.conf["speech"]["trimLeadingSilence"])
 		self.trimLeadingSilenceCheckBox.defaultValue = self._getDefaultValue(["speech", "trimLeadingSilence"])
 
-		# Translators: This is the label for a combo-box control in the
-		#  Advanced settings panel.
-		label = _("Use WASAPI for SAPI 4 audio output:")
-		self.useWASAPIForSAPI4Combo = speechGroup.addLabeledControl(
-			labelText=label,
-			wxCtrlClass=nvdaControls.FeatureFlagCombo,
-			keyPath=["speech", "useWASAPIForSAPI4"],
-			conf=config.conf,
-		)
-		self.bindHelpEvent("UseWASAPIForSAPI4", self.useWASAPIForSAPI4Combo)
-
 		# Translators: This is the label for a group of advanced options in the
 		#  Advanced settings panel
 		label = _("Virtual Buffers")
@@ -4278,6 +4698,7 @@ def __init__(self, parent):
 			"garbageHandler",
 			"remoteClient",
 			"externalPythonDependencies",
+			"bdDetect",
 		]
 		# Translators: This is the label for a list in the
 		#  Advanced settings panel
@@ -4303,10 +4724,8 @@ def __init__(self, parent):
 		# Translators: Label for the Play a sound for logged errors combobox, in the Advanced settings panel.
 		label = _("Play a sound for logged e&rrors:")
 		playErrorSoundChoices = (
-			# # Translators: Label for a value in the Play a sound for logged errors combobox, in the Advanced settings.
-			# pgettext("advanced.playErrorSound", "Only in NVDA test versions"),
 			# Translators: Label for a value in the Play a sound for logged errors combobox, in the Advanced settings.
-			_("No"),
+			pgettext("advanced.playErrorSound", "Only in NVDA test versions"),
 			# Translators: Label for a value in the Play a sound for logged errors combobox, in the Advanced settings.
 			pgettext("advanced.playErrorSound", "Yes"),
 		)
@@ -4381,7 +4800,6 @@ def haveConfigDefaultsBeenRestored(self):
 			and self.cancelExpiredFocusSpeechCombo.GetSelection()
 			== self.cancelExpiredFocusSpeechCombo.defaultValue
 			and self.trimLeadingSilenceCheckBox.IsChecked() == self.trimLeadingSilenceCheckBox.defaultValue
-			and self.useWASAPIForSAPI4Combo.isValueConfigSpecDefault()
 			and self.loadChromeVBufWhenBusyCombo.isValueConfigSpecDefault()
 			and self.caretMoveTimeoutSpinControl.GetValue() == self.caretMoveTimeoutSpinControl.defaultValue
 			and self.reportTransparentColorCheckBox.GetValue()
@@ -4411,7 +4829,6 @@ def restoreToDefaults(self):
 		self.wtStrategyCombo.resetToConfigSpecDefault()
 		self.cancelExpiredFocusSpeechCombo.SetSelection(self.cancelExpiredFocusSpeechCombo.defaultValue)
 		self.trimLeadingSilenceCheckBox.SetValue(self.trimLeadingSilenceCheckBox.defaultValue)
-		self.useWASAPIForSAPI4Combo.resetToConfigSpecDefault()
 		self.loadChromeVBufWhenBusyCombo.resetToConfigSpecDefault()
 		self.caretMoveTimeoutSpinControl.SetValue(self.caretMoveTimeoutSpinControl.defaultValue)
 		self.reportTransparentColorCheckBox.SetValue(self.reportTransparentColorCheckBox.defaultValue)
@@ -4425,8 +4842,6 @@ def onSave(self):
 
 		shouldResetSynth = (
 			config.conf["speech"]["trimLeadingSilence"] != self.trimLeadingSilenceCheckBox.IsChecked()
-			or config.conf["speech"]["useWASAPIForSAPI4"]
-			!= self.useWASAPIForSAPI4Combo._getControlCurrentFlag()
 		)
 
 		config.conf["development"]["enableScratchpadDir"] = self.scratchpadCheckBox.IsChecked()
@@ -4442,7 +4857,6 @@ def onSave(self):
 			self.cancelExpiredFocusSpeechCombo.GetSelection()
 		)
 		config.conf["speech"]["trimLeadingSilence"] = self.trimLeadingSilenceCheckBox.IsChecked()
-		self.useWASAPIForSAPI4Combo.saveCurrentValueToConf()
 		config.conf["UIA"]["allowInChromium"] = self.UIAInChromiumCombo.GetSelection()
 		self.enhancedEventProcessingComboBox.saveCurrentValueToConf()
 		config.conf["terminals"]["speakPasswords"] = self.winConsoleSpeakPasswordsCheckBox.IsChecked()
@@ -5634,6 +6048,201 @@ def onSave(self):
 			self._providerSettings.onSave()
 
 
+class PrivacyAndSecuritySettingsPanel(SettingsPanel):
+	# Translators: The title of the privacy and security category in NVDA's settings.
+	title = _("Privacy and Security")
+	helpId = "PrivacyAndSecuritySettings"
+
+	def makeSettings(self, sizer: wx.BoxSizer):
+		sHelper = guiHelper.BoxSizerHelper(self, sizer=sizer)
+
+		# BEGIN JP PATCH (Fix KeyError: 'screenCurtain')
+		from visionEnhancementProviders.screenCurtain import ScreenCurtainProvider, WarnOnLoadDialog, warnOnLoadCheckBoxText
+		self._screenCurtainConfig = config.conf["screenCurtain"]
+		screenCurtainId = ScreenCurtainProvider.getSettings().getId()
+		screenCurtainProviderInfo = vision.handler.getProviderInfo(screenCurtainId)
+		screenCurtainInstance = vision.handler.getProviderInstance(screenCurtainProviderInfo)
+		# END JP PATCH
+		# Translators: Name for a feature that disables output to the screen,
+		# making it black.
+		screenCurtainSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=_("Screen Curtain"))
+		screenCurtainBox = screenCurtainSizer.GetStaticBox()
+		screenCurtainGroup = guiHelper.BoxSizerHelper(self, sizer=screenCurtainSizer)
+		sHelper.addItem(screenCurtainGroup)
+
+		self._screenCurtainEnabledCheckbox = screenCurtainGroup.addItem(
+			wx.CheckBox(
+				screenCurtainBox,
+				#  Translators: option to enable screen curtain in the privacy and security settings panel
+				label=_("Make screen black (immediate effect)"),
+			),
+		)
+		# BEGIN JP PATCH (Fix screenCurtain.screenCurtain reference)
+		self._screenCurtainEnabledCheckbox.SetValue(
+			screenCurtainInstance is not None and screenCurtainInstance.enabled,
+		)
+		self._screenCurtainEnabledCheckbox.Bind(wx.EVT_CHECKBOX, self._ensureScreenCurtainEnableState)
+		self._screenCurtainEnabledCheckbox.Enable(screenCurtainInstance is not None)
+		# END JP PATCH
+		self.bindHelpEvent("ScreenCurtainEnable", self._screenCurtainEnabledCheckbox)
+
+		self._screenCurtainWarnOnLoadCheckbox = screenCurtainGroup.addItem(
+			wx.CheckBox(
+				screenCurtainBox,
+				# BEGIN JP PATCH (Fix screenCurtain._screenCurtain reference)
+				label=warnOnLoadCheckBoxText,
+				# END JP PATCH
+			),
+		)
+		self._screenCurtainWarnOnLoadCheckbox.SetValue(self._screenCurtainConfig["warnOnLoad"])
+		self.bindHelpEvent("ScreenCurtainWarnOnLoad", self._screenCurtainWarnOnLoadCheckbox)
+
+		# BEGIN JP PATCH (Store provider info and instance for later use)
+		self._screenCurtainProviderInfo = screenCurtainProviderInfo
+		self._screenCurtainInstance = screenCurtainInstance
+		# END JP PATCH
+
+		self._screenCurtainPlayToggleSoundsCheckbox = screenCurtainGroup.addItem(
+			wx.CheckBox(
+				screenCurtainBox,
+				# Translators: Description for a screen curtain setting to play sounds when enabling/disabling the curtain
+				label=_("&Play sound when toggling Screen Curtain"),
+			),
+		)
+		self._screenCurtainPlayToggleSoundsCheckbox.SetValue(self._screenCurtainConfig["playToggleSounds"])
+		self.bindHelpEvent("ScreenCurtainPlayToggleSounds", self._screenCurtainPlayToggleSoundsCheckbox)
+
+		# Translators: name of a grouping in Privacy and Security settings
+		# which contains miscellaneous settings.
+		generalSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=_("General"))
+		generalBox = generalSizer.GetStaticBox()
+		generalGroup = guiHelper.BoxSizerHelper(self, sizer=generalSizer)
+		sHelper.addItem(generalGroup)
+
+		self._logLevelCombo: wx.Choice = generalGroup.addLabeledControl(
+			# Translators: The label for a setting in privacy and security settings to select NVDA's logging level
+			_("L&ogging level:"),
+			wx.Choice,
+			choices=[level.displayString for level in LoggingLevel],
+		)
+		self.bindHelpEvent("GeneralSettingsLogLevel", self._logLevelCombo)
+		if logHandler.isLogLevelForced():
+			self._logLevelCombo.Disable()
+		curLevel = log.getEffectiveLevel()
+		try:
+			self._logLevelCombo.SetSelection(
+				next(
+					filter(
+						lambda indexAndLevel: indexAndLevel[1] == curLevel,
+						enumerate(LoggingLevel.__members__.values()),
+					),
+				)[0],
+			)
+		except StopIteration:
+			log.debugWarning("Could not set log level list to current log level")
+
+		self._allowUsageStatsCheckBox: wx.CheckBox = generalGroup.addItem(
+			# Translators: The label of a checkbox in privacy and security settings to toggle allowing of usage stats gathering
+			wx.CheckBox(generalBox, label=_("Allow NV Access to gather NVDA usage statistics")),
+		)
+		self.bindHelpEvent("GeneralSettingsGatherUsageStats", self._allowUsageStatsCheckBox)
+		self._allowUsageStatsCheckBox.Value = config.conf["update"]["allowUsageStats"]
+		if not updateCheck:
+			self._allowUsageStatsCheckBox.Value = False
+			self._allowUsageStatsCheckBox.Disable()
+
+	def onSave(self):
+		# We intentionally don't save whether the screen curtain is enabled here,
+		# so we don't unintentionally persist a temporary screen curtain to config.
+		self._screenCurtainConfig["warnOnLoad"] = self._screenCurtainWarnOnLoadCheckbox.IsChecked()
+		self._screenCurtainConfig["playToggleSounds"] = (
+			self._screenCurtainPlayToggleSoundsCheckbox.IsChecked()
+		)
+
+		if not logHandler.isLogLevelForced():
+			config.conf["general"]["loggingLevel"] = logging.getLevelName(
+				list(LoggingLevel)[self._logLevelCombo.GetSelection()],
+			)
+			logHandler.setLogLevelFromConfig()
+
+		if updateCheck:
+			config.conf["update"]["allowUsageStats"] = self._allowUsageStatsCheckBox.IsChecked()
+			# updateCheck queries this value whenever checking for updates, so there's no need to restart it
+
+	def _ocrActive(self) -> bool:
+		"""
+		Outputs a message when trying to activate screen curtain when OCR is active.
+
+		:return: ``True`` when OCR is active, ``False`` otherwise.
+		"""
+		# Import late to avoid circular import
+		from contentRecog.recogUi import RefreshableRecogResultNVDAObject
+		# BEGIN JP PATCH (Fix screenCurtain._screenCurtain reference)
+		from screenCurtain._screenCurtain import UNAVAILABLE_WHEN_RECOGNISING_CONTENT_MESSAGE
+		# END JP PATCH
+
+		focusObj = api.getFocusObject()
+		if isinstance(focusObj, RefreshableRecogResultNVDAObject) and focusObj.recognizer.allowAutoRefresh:
+			ui.message(
+				UNAVAILABLE_WHEN_RECOGNISING_CONTENT_MESSAGE,
+				speechPriority=speech.priorities.Spri.NOW,
+			)
+			return True
+		return False
+
+	def _ensureScreenCurtainEnableState(self, evt: wx.CommandEvent):
+		"""Ensures that toggling the Screen Curtain checkbox toggles the Screen Curtain."""
+		# BEGIN JP PATCH (Fix screenCurtain.screenCurtain reference)
+		import speech
+		import ui
+		screenCurtainInstance = vision.handler.getProviderInstance(self._screenCurtainProviderInfo)
+		# END JP PATCH
+		shouldBeEnabled = evt.IsChecked()
+		if screenCurtainInstance is None:
+			self._screenCurtainEnabledCheckbox.SetValue(False)
+			return
+		currentlyEnabled = screenCurtainInstance.enabled
+		if shouldBeEnabled and not currentlyEnabled:
+			confirmed = self._confirmEnableScreenCurtainWithUser()
+			if not confirmed or self._ocrActive():
+				self._screenCurtainEnabledCheckbox.SetValue(False)
+			else:
+				try:
+					vision.handler.initializeProvider(self._screenCurtainProviderInfo)
+				except Exception:
+					# BEGIN JP PATCH (Fix screenCurtain._screenCurtain reference)
+					from screenCurtain._screenCurtain import ERROR_ENABLING_MESSAGE
+					# END JP PATCH
+					import logHandler
+					logHandler.log.error("Error enabling Screen Curtain.", exc_info=True)
+					ui.message(
+						ERROR_ENABLING_MESSAGE,
+						speechPriority=speech.priorities.Spri.NOW,
+					)
+					self._screenCurtainEnabledCheckbox.SetValue(False)
+		elif not shouldBeEnabled and currentlyEnabled:
+			vision.handler.terminateProvider(self._screenCurtainProviderInfo)
+
+	def _confirmEnableScreenCurtainWithUser(self) -> bool:
+		"""Confirm with the user before enabling Screen Curtain, if configured to do so.
+
+		:return: ``True`` if the Screen Curtain should be enabled; ``False`` otherwise.
+		"""
+		# BEGIN JP PATCH (Fix screenCurtain._screenCurtain reference)
+		from visionEnhancementProviders.screenCurtain import ScreenCurtainProvider, WarnOnLoadDialog
+		# END JP PATCH
+		if not self._screenCurtainConfig["warnOnLoad"]:
+			return True
+		with WarnOnLoadDialog(
+			screenCurtainSettingsStorage=self._screenCurtainConfig,
+			parent=self,
+		) as dlg:
+			res = dlg.ShowModal()
+			# WarnOnLoadDialog can change settings, reload them
+			self._screenCurtainWarnOnLoadCheckbox.SetValue(self._screenCurtainConfig["warnOnLoad"])
+			return res == wx.YES
+
+
 """ The name of the config profile currently being edited, if any.
 This is set when the currently edited configuration profile is determined and returned to None when the dialog is destroyed.
 This can be used by an AppModule for NVDA to identify and announce
@@ -5647,10 +6256,13 @@ class NVDASettingsDialog(MultiCategorySettingsDialog):
 	title = _("NVDA Settings")
 	categoryClasses = [
 		GeneralSettingsPanel,
+		# BEGIN JP PATCH (Japanese language settings panel)
 		LanguageSettingsPanel,
+		# END JP PATCH
 		SpeechSettingsPanel,
 		BrailleSettingsPanel,
 		AudioPanel,
+		PrivacyAndSecuritySettingsPanel,
 		VisionSettingsPanel,
 		KeyboardSettingsPanel,
 		MouseSettingsPanel,
@@ -5660,7 +6272,9 @@ class NVDASettingsDialog(MultiCategorySettingsDialog):
 		BrowseModePanel,
 		DocumentFormattingPanel,
 		DocumentNavigationPanel,
+		MathSettingsPanel,
 		RemoteSettingsPanel,
+		LocalCaptionerSettingsPanel,
 	]
 	# In secure mode, add-on update is disabled, so AddonStorePanel should not appear since it only contains
 	# add-on update related controls.
@@ -5689,6 +6303,9 @@ def _doOnCategoryChange(self):
 			or isinstance(self.currentCategory, GeneralSettingsPanel)
 			or isinstance(self.currentCategory, AddonStorePanel)
 			or isinstance(self.currentCategory, RemoteSettingsPanel)
+			or isinstance(self.currentCategory, LocalCaptionerSettingsPanel)
+			or isinstance(self.currentCategory, MathSettingsPanel)
+			or isinstance(self.currentCategory, PrivacyAndSecuritySettingsPanel)
 		):
 			# Translators: The profile name for normal configuration
 			NvdaSettingsDialogActiveConfigProfile = _("normal configuration")

```