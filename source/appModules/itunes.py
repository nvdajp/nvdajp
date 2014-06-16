import appModuleHandler
from comtypes import COMError
import controlTypes
import oleacc
import winUser
import speech
import treeInterceptorHandler
import api
import eventHandler
import NVDAObjects.IAccessible

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self,obj):
		if isinstance(obj,NVDAObjects.IAccessible.IAccessible):
			if obj.windowClassName=="WebViewWindowClass":
				if obj.IAccessibleRole==oleacc.ROLE_SYSTEM_WINDOW:
					#Disable a safety mechonism in our IAccessible support as in iTunes it causes an infinit ancestry.
					obj.parentUsesSuperOnWindowRootIAccessible=False
				else:
					obj.hasEncodedAccDescription=True
			elif obj.role==controlTypes.ROLE_BUTTON:
				# iTunes seems to put some controls inside a button.
				# Don't report this weirdness to the user.
				obj.isPresentableFocusAncestor=False

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		windowClassName=obj.windowClassName
		role=obj.role
		if windowClassName in ('iTunesList','iTunesSources','iTunesTrackList') and role in (controlTypes.ROLE_LISTITEM,controlTypes.ROLE_TREEVIEWITEM):
			clsList.insert(0, ITunesItem)
		elif windowClassName=="iTunesWebViewControl" and role==controlTypes.ROLE_DOCUMENT:
			clsList.insert(0,WebKitWrapper)
		elif windowClassName=="iTunes" and obj.IAccessibleRole==oleacc.ROLE_SYSTEM_CLIENT:
			clsList.insert(0, TopLevelClient)

class ITunesItem(NVDAObjects.IAccessible.IAccessible):
	"""Retreaves position information encoded in the accDescription"""

	hasEncodedAccDescription=True
	value = None

	def _get_next(self):
		next=super(ITunesItem,self).next
		if next:
			return next
		try:
			parentChildCount=self.IAccessibleObject.accChildCount
		except COMError:
			parentChildCount=0
		if self.IAccessibleChildID>0 and self.IAccessibleChildID<parentChildCount:
			return NVDAObjects.IAccessible.IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=self.IAccessibleChildID+1)
		return None

	def _get_previous(self):
		previous=super(ITunesItem,self).previous
		if not previous and self.IAccessibleChildID>1:
			previous=NVDAObjects.IAccessible.IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=self.IAccessibleChildID-1)
		return previous

	def _get_shouldAllowIAccessibleFocusEvent(self):
		# These items can fire spurious focus events; e.g. when tabbing out of the Music list.
		# The list reports that it's focused even when it isn't.
		# Thankfully, the list items don't.
		return self.hasFocus

class WebKitWrapper(NVDAObjects.IAccessible.IAccessible):
	"""An iTunes wrapper around a WebKit document.
	"""
	# This wrapper should never be seen by the user.
	shouldAllowIAccessibleFocusEvent = False
	presentationType = NVDAObjects.IAccessible.IAccessible.presType_layout

	def event_stateChange(self):
		# iTunes has indicated that a page has died and been replaced by a new one.
		focus = api.getFocusObject()
		if not winUser.isDescendantWindow(self.windowHandle, focus.windowHandle):
			return
		# The new page has the same event params, so we must bypass NVDA's IAccessible caching.
		obj = NVDAObjects.IAccessible.getNVDAObjectFromEvent(focus.windowHandle, winUser.OBJID_CLIENT, 0)
		if not obj:
			return
		if focus.treeInterceptor:
			speech.cancelSpeech()
			treeInterceptorHandler.killTreeInterceptor(focus.treeInterceptor)
		eventHandler.queueEvent("gainFocus",obj)

class TopLevelClient(NVDAObjects.IAccessible.IAccessible):

	def _isEqual(self, other):
		# The location seems to be reported differently depending on how you get to this object.
		# This causes the focus ancestry to change when it really hasn't,
		# which in turn causes spurious reporting.
		if self.IAccessibleIdentity == other.IAccessibleIdentity:
			return True
		return super(TopLevelClient, self)._isEqual(other)
