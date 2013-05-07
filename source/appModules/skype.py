# -*- coding: UTF-8 -*-
#appModules/skype.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2007-2013 Peter Vágner, NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from comtypes import COMError
import appModuleHandler
import controlTypes
import winUser
import NVDAObjects.IAccessible
import oleacc
import ui
import windowUtils
import displayModel
import queueHandler
import config

class ChatOutputList(NVDAObjects.IAccessible.IAccessible):

	def startMonitoring(self):
		self.oldLastMessageText = None
		self.update()
		displayModel.requestTextChangeNotifications(self, True)

	def stopMonitoring(self):
		displayModel.requestTextChangeNotifications(self, False)

	def reportMessage(self, text):
		if text.startswith("["):
			# Remove the timestamp.
			text = text.split("] ", 1)[1]
		ui.message(text)

	def update(self):
		reportNew = config.conf["presentation"]["reportDynamicContentChanges"] and self.oldLastMessageText

		# Ideally, we'd determine new messages based just on the change in child count,
		# but children can be inserted in the middle when messages are expanded.
		# Therefore, we have to use message text.
		newCount = self.childCount
		ia = self.IAccessibleObject
		newMessages = []
		# The list is chronological and we're looking for new messages,
		# so scan the list in reverse.
		for c in xrange(self.childCount, -1, -1):
			try:
				if ia.accRole(c) != oleacc.ROLE_SYSTEM_LISTITEM or ia.accState(c) & oleacc.STATE_SYSTEM_UNAVAILABLE:
					# Not a message.
					continue
			except COMError:
				# The child probably disappeared after we fetched childCount.
				continue
			text = ia.accName(c)
			if not text:
				continue
			if text == self.oldLastMessageText:
				# No more new messages.
				break
			newMessages.append(text)
			if not reportNew:
				# If we're not reporting new messages, we don't need to go any further than the last message.
				break

		if newMessages:
			self.oldLastMessageText = newMessages[0]
			if not reportNew:
				return
			for text in reversed(newMessages):
				self.reportMessage(text)

	def event_textChange(self):
		# This event is called from another thread, but this needs to run in the main thread.
		queueHandler.queueFunction(queueHandler.eventQueue, self.update)

class AppModule(appModuleHandler.AppModule):

	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)
		self.chatWindow = None
		self.chatOutputList = None

	def event_NVDAObject_init(self,obj):
		if obj.event_objectID is None and controlTypes.STATE_FOCUSED in obj.states and obj.role not in (controlTypes.ROLE_POPUPMENU,controlTypes.ROLE_MENUITEM,controlTypes.ROLE_MENUBAR):
			# The window handle reported by Skype accessibles is sometimes incorrect.
			# This object is focused, so we can override with the focus window.
			obj.windowHandle=winUser.getGUIThreadInfo(None).hwndFocus
			obj.windowClassName=winUser.getClassName(obj.windowHandle)
		if obj.value and obj.windowClassName in ("TMainUserList", "TConversationList", "TInboxList", "TActiveConversationList", "TConversationsControl"):
			# The name and value both include the user's name, so kill the value to avoid doubling up.
			# The value includes the Skype name,
			# but we care more about the additional info (e.g. new event count) included in the name.
			obj.value=None
		elif isinstance(obj, NVDAObjects.IAccessible.IAccessible) and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_PANE and not obj.name:
			# Prevent extraneous reporting of pane when tabbing through a conversation form.
			obj.shouldAllowIAccessibleFocusEvent = False

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "TChatContentControl" and obj.role == controlTypes.ROLE_LIST:
			clsList.insert(0, ChatOutputList)

	def conversationMaybeFocused(self, obj):
		if not isinstance(obj, NVDAObjects.IAccessible.IAccessible) or obj.windowClassName != "TConversationForm" or obj.IAccessibleRole != oleacc.ROLE_SYSTEM_CLIENT:
			# This isn't a Skype conversation.
			return

		# The user has entered a Skype conversation.
		window = obj.windowHandle
		self.chatWindow = window
		try:
			self.chatOutputList = NVDAObjects.IAccessible.getNVDAObjectFromEvent(
				windowUtils.findDescendantWindow(window, className="TChatContentControl"),
				winUser.OBJID_CLIENT, 1)
		except LookupError:
			pass
		else:
			self.chatOutputList.startMonitoring()

	def event_focusEntered(self, obj, nextHandler):
		self.conversationMaybeFocused(obj)
		nextHandler()

	def conversationLostFocus(self):
		self.chatWindow = None
		self.chatOutputList.stopMonitoring()
		self.chatOutputList = None

	def event_gainFocus(self, obj, nextHandler):
		if self.chatWindow and not winUser.isDescendantWindow(self.chatWindow, obj.windowHandle):
			self.conversationLostFocus()
		# A conversation might have its own top level window,
		# but foreground changes often trigger gainFocus instead of focusEntered.
		self.conversationMaybeFocused(obj)
		nextHandler()

	def event_appModule_loseFocus(self):
		if self.chatWindow:
			self.conversationLostFocus()
