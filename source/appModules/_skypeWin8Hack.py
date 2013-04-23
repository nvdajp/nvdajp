#appModules/skype.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import controlTypes
import winUser

# start nvdajp - misono modified
import threading
import ctypes
import comtypes
import UIAHandler
if UIAHandler.isUIAAvailable:
	from NVDAObjects.UIA import UIA
from comtypes.gen.UIAutomationClient import *
import time
# end nvdajp - misono modified

class AppModule(appModuleHandler.AppModule):

	# nvdajp begin

	_threadProc = False
	_comThread = None
	_handler = None

	def __Thread(self, evtId):
		self._threadProc = True
		ctypes.oledll.ole32.CoInitializeEx(None,comtypes.COINIT_MULTITHREADED)
		self._handler.clientObject.RemoveAutomationEventHandler(evtId, self._handler.rootElement, self._handler)
		cnt = 0
		while cnt<5:
			if not self._threadProc: break
			time.sleep(0.2)
		self._handler.clientObject.AddAutomationEventHandler(evtId, self._handler.rootElement, TreeScope_Subtree, self._handler.baseCacheRequest, self._handler)
		self._threadProc = False

	def _Thread(self, evtId):
		if self._threadProc: return
		self._comThread = threading.Thread(target=self.__Thread, args=(evtId,))
		self._comThread.setDaemon(True)
		self._comThread.start()

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		windowClass = obj.windowClassName
		role = obj.role
		if UIAHandler.isUIAAvailable:
			if windowClass in ["TMainUserList", "TConversationList", "TInboxList", "TActiveConversationList", "TConversationsControl", "TAccessibleEdit"] and not role in [controlTypes.ROLE_MENUBAR, controlTypes.ROLE_MENUITEM, controlTypes.ROLE_POPUPMENU]:
				self._Thread(UIAHandler.UIA_ToolTipOpenedEventId)

	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)
		self._threadProc = False
		self._comThread = None
		self._handler = UIAHandler.handler
		if UIAHandler.isUIAAvailable:
			self._Thread(UIAHandler.UIA_ToolTipOpenedEventId)

	def terminate(self):
		super(AppModule, self).terminate()
		self._threadProc = False

	# nvdajp end

	def event_NVDAObject_init(self,obj):
		if controlTypes.STATE_FOCUSED in obj.states and obj.role not in (controlTypes.ROLE_POPUPMENU,controlTypes.ROLE_MENUITEM):
			obj.windowHandle=winUser.getGUIThreadInfo(None).hwndFocus
			obj.windowClassName=winUser.getClassName(obj.windowHandle)
		if obj.value and obj.windowClassName in ["TMainUserList", "TConversationList", "TInboxList", "TActiveConversationList", "TConversationsControl"] and not obj.role in [controlTypes.ROLE_MENUBAR, controlTypes.ROLE_MENUITEM, controlTypes.ROLE_POPUPMENU]:
			obj.name=obj.value
			obj.value=None
