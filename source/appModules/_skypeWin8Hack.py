#appModules/skype.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#Copyright (C) 2013 Masamitsu Misono (NVDA Japanese Team)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import controlTypes
import winUser
import threading
import ctypes
import comtypes
import UIAHandler
if UIAHandler.isUIAAvailable:
	from NVDAObjects.UIA import UIA
from comtypes.gen.UIAutomationClient import *

class AppModule(appModuleHandler.AppModule):

	_handler = None

	def __threadAddAutometion(self, evtId):
		ctypes.oledll.ole32.CoInitializeEx(None,comtypes.COINIT_MULTITHREADED)
		self._handler.clientObject.AddAutomationEventHandler(evtId, self._handler.rootElement, TreeScope_Subtree, self._handler.baseCacheRequest, self._handler)

	def __threadRemoveAutometion(self, evtId):
		ctypes.oledll.ole32.CoInitializeEx(None,comtypes.COINIT_MULTITHREADED)
		self._handler.clientObject.RemoveAutomationEventHandler(evtId, self._handler.rootElement, self._handler)

	def _threadAddAutometion(self, evtId):
		t = threading.Thread(target=self.__threadAddAutometion, args=(evtId,))
		t.setDaemon(True)
		t.start()
		if t is not None:
			if t.isAlive:
				t.join(0.5)

	def _threadRemoveAutometion(self, evtId):
		t = threading.Thread(target=self.__threadRemoveAutometion, args=(evtId,))
		t.setDaemon(True)
		t.start()
		if t is not None:
			if t.isAlive:
				t.join(0.5)

	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)
		if UIAHandler.isUIAAvailable:
			self._handler = UIAHandler.handler
			self._threadRemoveAutometion(UIAHandler.UIA_ToolTipOpenedEventId)

	def terminate(self):
		super(AppModule, self).terminate()
		if UIAHandler.isUIAAvailable:
			self._threadAddAutometion(UIAHandler.UIA_ToolTipOpenedEventId)
			self._handler = None

	def event_NVDAObject_init(self,obj):
		if controlTypes.STATE_FOCUSED in obj.states and obj.role not in (controlTypes.ROLE_POPUPMENU,controlTypes.ROLE_MENUITEM):
			obj.windowHandle=winUser.getGUIThreadInfo(None).hwndFocus
			obj.windowClassName=winUser.getClassName(obj.windowHandle)
		if obj.value and obj.windowClassName in ["TMainUserList", "TConversationList", "TInboxList", "TActiveConversationList", "TConversationsControl"] and not obj.role in [controlTypes.ROLE_MENUBAR, controlTypes.ROLE_MENUITEM, controlTypes.ROLE_POPUPMENU]:
			obj.name=obj.value
			obj.value=None
