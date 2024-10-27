# netradiorecorder4.py
# A part of NonVisual Desktop Access (NVDA)
# 2017-04-04 Takuya Nishimoto

import appModuleHandler
import api
import ui
from NVDAObjects.IAccessible import IAccessible


class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "FMTMainForm":
			clsList.insert(0, EnhancedForm)


class EnhancedForm(IAccessible):
	def script_reportItem(self, gesture):
		gesture.send()
		focusObject = api.getFocusObject()
		ui.message(focusObject.value)

	__gestures = {
		"kb:downArrow": "reportItem",
		"kb:upArrow": "reportItem",
		"kb:leftArrow": "reportItem",
		"kb:rightArrow": "reportItem",
	}
