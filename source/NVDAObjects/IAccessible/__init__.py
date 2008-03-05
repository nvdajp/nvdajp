#NVDAObjects/IAccessible.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import weakref
import re
import os
import tones
import time
import difflib
import ctypes
import comtypes.automation
import comtypes.client
import appModuleHandler
from keyUtils import sendKey, key 
import IAccessibleHandler
import JABHandler
import winUser
import winKernel
import globalVars
import speech
import api
import config
import controlTypes
from NVDAObjects.window import Window
from NVDAObjects import NVDAObject
import NVDAObjects.JAB

re_gecko_level=re.compile('.*?L([0-9]+).*')
re_gecko_position=re.compile('.*?([0-9]+) of ([0-9]+).*')
re_gecko_contains=re.compile('.*?with ([0-9]+).*')

def getNVDAObjectFromEvent(hwnd,objectID,childID):
	accHandle=IAccessibleHandler.accessibleObjectFromEvent(hwnd,objectID,childID)
	if not accHandle:
		return None
	(pacc,accChildID)=accHandle
	obj=IAccessible(IAccessibleObject=pacc,IAccessibleChildID=accChildID,event_windowHandle=hwnd,event_objectID=objectID,event_childID=childID)
	return obj

def getNVDAObjectFromPoint(x,y):
	accHandle=IAccessibleHandler.accessibleObjectFromPoint(x,y)
	if not accHandle:
		return None
	(pacc,child)=accHandle
	obj=IAccessible(IAccessibleObject=pacc,IAccessibleChildID=child)
	return obj

def processGeckoDescription(obj):
	if not obj.windowClassName.startswith('Mozilla'):
		return
	rawDescription=obj.description
	if not isinstance(rawDescription,basestring):
		return
	if rawDescription.startswith('Description: '):
		obj.description=rawDescription[13:]
		return
	m=re_gecko_level.match(rawDescription)
	groups=m.groups() if m else []
	if len(groups)>=1:
		level=_("level %s")%groups[0]
	else:
		level=None
	m=re_gecko_position.match(rawDescription)
	groups=m.groups() if m else []
	if len(groups)==2:
		positionString=_("%s of %s")%(groups[0],groups[1])
	else:
		positionString=None
	m=re_gecko_contains.match(rawDescription)
	groups=m.groups() if m else []
	if len(groups)>=1:
		contains=_("contains %s items")%groups[0]
	else:
		contains=None
		obj.positionString=" ".join([x for x in level,positionString,contains if x])
	obj.description=""

class IAccessible(Window):
	"""
the NVDAObject for IAccessible
@ivar IAccessibleChildID: the IAccessible object's child ID
@type IAccessibleChildID: int
"""

	def __new__(cls,windowHandle=None,IAccessibleObject=None,IAccessibleChildID=None,event_windowHandle=None,event_objectID=None,event_childID=None):
		"""
Checks the window class and IAccessible role against a map of IAccessible sub-types, and if a match is found, returns that rather than just IAccessible.
"""  
		if windowHandle and not IAccessibleObject:
			(IAccessibleObject,IAccessibleChildID)=IAccessibleHandler.accessibleObjectFromEvent(windowHandle,-4,0)
		elif not windowHandle and not IAccessibleObject:
			raise ArgumentError("Give either a windowHandle, or windowHandle, childID, objectID, or IAccessibleObject")
		if IAccessibleObject:
			if isinstance(IAccessibleObject,IAccessibleHandler.IAccessible2): 
				IA2Class=__import__("IA2",globals(),locals(),[]).IA2
				obj=Window.__new__(IA2Class,windowHandle=windowHandle)
				obj.__init__(windowHandle=windowHandle,IAccessibleObject=IAccessibleObject,IAccessibleChildID=IAccessibleChildID,event_windowHandle=event_windowHandle,event_objectID=event_objectID,event_childID=event_childID)
				return obj
		if not windowHandle:
			windowHandle=IAccessibleHandler.windowFromAccessibleObject(IAccessibleObject)
		if not windowHandle:
			return None #We really do need a window handle
		windowClassName=winUser.getClassName(windowHandle)
		try:
			IAccessibleRole=IAccessibleObject.accRole(IAccessibleChildID)
		except:
			IAccessibleRole=0
		classString=None
		if _staticMap.has_key((windowClassName,IAccessibleRole)):
			classString=_staticMap[(windowClassName,IAccessibleRole)]
		elif _staticMap.has_key((windowClassName,None)):
			classString=_staticMap[(windowClassName,None)]
		elif _staticMap.has_key((None,IAccessibleRole)):
			classString=_staticMap[(None,IAccessibleRole)]
		if classString is None:
			classString="IAccessible"
		if classString.find('.')>0:
			modString,classString=os.path.splitext(classString)
			classString=classString[1:]
			mod=__import__(modString,globals(),locals(),[])
			newClass=getattr(mod,classString)
		else:
			newClass=globals()[classString]
		obj=Window.__new__(newClass,windowHandle=windowHandle)
		obj.windowClassName=windowClassName
		obj.IAccessibleRole=IAccessibleRole
		obj.__init__(windowHandle=windowHandle,IAccessibleObject=IAccessibleObject,IAccessibleChildID=IAccessibleChildID,event_windowHandle=event_windowHandle,event_objectID=event_objectID,event_childID=event_childID)
		return obj

	def __init__(self,windowHandle=None,IAccessibleObject=None,IAccessibleChildID=None,event_windowHandle=None,event_objectID=None,event_childID=None):
		"""
@param pacc: a pointer to an IAccessible object
@type pacc: ctypes.POINTER(IAccessible)
@param child: A child ID that will be used on all methods of the IAccessible pointer
@type child: int
@param hwnd: the window handle, if known
@type hwnd: int
@param objectID: the objectID for the IAccessible Object, if known
@type objectID: int
"""
		if hasattr(self,"_doneInit"):
			return
		self.IAccessibleObject=IAccessibleObject
		self.IAccessibleChildID=IAccessibleChildID
		self.event_windowHandle=event_windowHandle
		self.event_objectID=event_objectID
		self.event_childID=event_childID
		Window.__init__(self,windowHandle=windowHandle)
		#Mozilla Gecko objects use the description property to report other info
		processGeckoDescription(self)
		self._doneInit=True

	def _isEqual(self,other):
		if not isinstance(other,IAccessible):
			return False
		if self.IAccessibleChildID!=other.IAccessibleChildID:
			return False
		if self.IAccessibleObject==other.IAccessibleObject: 
			return True
		if self.event_windowHandle is not None and other.event_windowHandle is not None and self.event_windowHandle!=other.event_windowHandle:
			return False
		if self.event_objectID is not None and other.event_objectID is not None and self.event_objectID!=other.event_objectID:
			return False
		if self.event_childID is not None and other.event_childID is not None and self.event_childID!=other.event_childID:
			return False
		if not super(IAccessible,self)._isEqual(other):
			return False
		selfIden=self.IAccessibleIdentityString
		otherIden=other.IAccessibleIdentityString
		if selfIden!=otherIden:
			return False
		if self.location!=other.location:
			return False
 		if self.IAccessibleRole!=other.IAccessibleRole:
			return False
		if self.name!=other.name:
			return False
		return True

	def _get_name(self):
		try:
			res=self.IAccessibleObject.accName(self.IAccessibleChildID)
		except:
			res=None
		return res if isinstance(res,basestring) and not res.isspace() else None

	def _get_value(self):
		try:
			res=self.IAccessibleObject.accValue(self.IAccessibleChildID)
		except:
			res=None
		return res if isinstance(res,basestring) and not res.isspace() else None

	def _get_actionStrings(self):
		try:
			action=self.IAccessibleObject.accDefaultAction()
		except:
			action=None
		if action:
			return [action]
		else:
			return super(IAccessible,self)._get_actionStrings()

	def doAction(self,index):
		if index==0:
			self.IAccessibleObject.accDoDefaultAction()

	def _get_IAccessibleIdentityString(self):
		if not hasattr(self,'_IAccessibleIdentityString'):
			try:
				self._IAccessibleIdentityString=IAccessibleHandler.getIAccIdentityString(self.IAccessibleObject,self.IAccessibleChildID)
			except:
				self._IAccessibleIdentityString=None
		return self._IAccessibleIdentityString

	def _get_IAccessibleRole(self):
		if not hasattr(self,'_IAccessibleRole'):
			try:
				self._IAccessibleRole=self.IAccessibleObject.accRole(self.IAccessibleChildID)
			except:
				self._IAccessibleRole=None
		return self._IAccessibleRole

	def _get_role(self):
		IARole=self.IAccessibleRole
		if isinstance(IARole,basestring):
			IARole=IARole.split(',')[0].lower()
			globalVars.log.info("IARole: %s"%IARole)
		return IAccessibleHandler.IAccessibleRolesToNVDARoles.get(IARole,controlTypes.ROLE_UNKNOWN)

	def _get_IAccessibleStates(self):
		try:
			res=self.IAccessibleObject.accState(self.IAccessibleChildID)
		except:
			return 0
		return res if isinstance(res,int) else 0

	def _get_states(self):
		try:
			IAccessibleStates=self.IAccessibleStates
		except:
			globalVars.log.warning("could not get IAccessible states",exc_info=True)
			return set()
		return set(IAccessibleHandler.IAccessibleStatesToNVDAStates[x] for x in (y for y in (1<<z for z in xrange(32)) if y&IAccessibleStates) if IAccessibleHandler.IAccessibleStatesToNVDAStates.has_key(x))

	def _get_description(self):
		try:
			res=self.IAccessibleObject.accDescription(self.IAccessibleChildID)
		except:
			res=None
		return res if isinstance(res,basestring) and not res.isspace() else None

	def _get_keyboardShortcut(self):
		try:
			res=self.IAccessibleObject.accKeyboardShortcut(self.IAccessibleChildID)
		except:
			res=None
		return res if isinstance(res,basestring) and not res.isspace() else None

	def _get_childCount(self):
		count=IAccessibleHandler.accChildCount(self.IAccessibleObject)
		return count

	def _get_location(self):
		location=IAccessibleHandler.accLocation(self.IAccessibleObject,self.IAccessibleChildID)
		return location

	def _get_labeledBy(self):
		try:
			(pacc,accChild)=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVRELATION_LABELLED_BY)
			obj=IAccessible(IAccessibleObject=pacc,IAccessibleChildID=accChild)
			return obj
		except:
			return None

	def _get_parent(self):
		if self.IAccessibleChildID>0:
			return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=0,event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=0)
		res=IAccessibleHandler.accParent(self.IAccessibleObject,self.IAccessibleChildID)
		if res:
			if res[0].accRole(res[1])!=IAccessibleHandler.ROLE_SYSTEM_WINDOW or IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVDIR_NEXT) or IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVDIR_PREVIOUS): 
				return IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1])
			res=IAccessibleHandler.accParent(res[0],res[1])
			if res:
				return IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1])
		return super(IAccessible,self)._get_parent()

	def _get_next(self):
		next=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVDIR_NEXT)
		if not next:
			next=None
			parent=IAccessibleHandler.accParent(self.IAccessibleObject,self.IAccessibleChildID)
			if not IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVDIR_PREVIOUS) and (parent and parent[0].accRole(parent[1])==IAccessibleHandler.ROLE_SYSTEM_WINDOW): 
				parentNext=IAccessibleHandler.accNavigate(parent[0],parent[1],IAccessibleHandler.NAVDIR_NEXT)
				if parentNext and parentNext[0].accRole(parentNext[1])>0:
					next=parentNext
		if next and next[0]==self.IAccessibleObject:
			return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=next[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=next[1])
		if next and next[0].accRole(next[1])==IAccessibleHandler.ROLE_SYSTEM_WINDOW:
			child=IAccessibleHandler.accChild(next[0],-4)
			if not IAccessibleHandler.accNavigate(child[0],child[1],IAccessibleHandler.NAVDIR_PREVIOUS) and not IAccessibleHandler.accNavigate(child[0],child[1],IAccessibleHandler.NAVDIR_NEXT):
				next=child
		if next and next[0].accRole(next[1])>0:
			return IAccessible(IAccessibleObject=next[0],IAccessibleChildID=next[1])
 
	def _get_previous(self):
		previous=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVDIR_PREVIOUS)
		if not previous:
			previous=None
			parent=IAccessibleHandler.accParent(self.IAccessibleObject,self.IAccessibleChildID)
			if not IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVDIR_NEXT) and (parent and parent[0].accRole(parent[1])==IAccessibleHandler.ROLE_SYSTEM_WINDOW): 
				parentPrevious=IAccessibleHandler.accNavigate(parent[0],parent[1],IAccessibleHandler.NAVDIR_PREVIOUS)
				if parentPrevious and parentPrevious[0].accRole(parentPrevious[1])>0:
					previous=parentPrevious
		if previous and previous[0]==self.IAccessibleObject:
			return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=previous[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=previous[1])
		if previous and previous[0].accRole(previous[1])==IAccessibleHandler.ROLE_SYSTEM_WINDOW:
			child=IAccessibleHandler.accChild(previous[0],-4)
			if not IAccessibleHandler.accNavigate(child[0],child[1],IAccessibleHandler.NAVDIR_PREVIOUS) and not IAccessibleHandler.accNavigate(child[0],child[1],IAccessibleHandler.NAVDIR_NEXT):
				previous=child
		if previous and previous[0].accRole(previous[1])>0:
			return IAccessible(IAccessibleObject=previous[0],IAccessibleChildID=previous[1])

	def _get_firstChild(self):
		firstChild=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVDIR_FIRSTCHILD)
		if not firstChild and self.IAccessibleChildID==0:
			children=IAccessibleHandler.accessibleChildren(self.IAccessibleObject,0,1)
			if len(children)>0:
				firstChild=children[0]
		if firstChild and firstChild[0]==self.IAccessibleObject:
			return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=firstChild[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=firstChild[1])
		if firstChild and firstChild[0].accRole(firstChild[1])==IAccessibleHandler.ROLE_SYSTEM_WINDOW:
			child=IAccessibleHandler.accChild(firstChild[0],-4)
			if not child:
				child=IAccessibleHandler.accNavigate(firstChild[0],firstChild[1],IAccessibleHandler.NAVDIR_FIRSTCHILD)
			if child and not IAccessibleHandler.accNavigate(child[0],child[1],IAccessibleHandler.NAVDIR_PREVIOUS) and not IAccessibleHandler.accNavigate(child[0],child[1],IAccessibleHandler.NAVDIR_NEXT):
				firstChild=child
		if firstChild and firstChild[0].accRole(firstChild[1])>0:
			obj=IAccessible(IAccessibleObject=firstChild[0],IAccessibleChildID=firstChild[1])
			if (obj and winUser.isDescendantWindow(self.windowHandle,obj.windowHandle)) or self.windowHandle==winUser.getDesktopWindow():
				return obj

	def _get_lastChild(self):
		lastChild=IAccessibleHandler.accNavigate(self.IAccessibleObject,self.IAccessibleChildID,IAccessibleHandler.NAVDIR_LASTCHILD)
		if lastChild and lastChild[0]==self.IAccessibleObject:
			return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=lastChild[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=lastChild[1])
		if lastChild and lastChild[0].accRole(lastChild[1])==IAccessibleHandler.ROLE_SYSTEM_WINDOW:
			child=IAccessibleHandler.accChild(lastChild[0],-4)
			if not IAccessibleHandler.accNavigate(child[0],child[1],IAccessibleHandler.NAVDIR_PREVIOUS) and not IAccessibleHandler.accNavigate(child[0],child[1],IAccessibleHandler.NAVDIR_NEXT):
				lastChild=child
		if lastChild and lastChild[0].accRole(lastChild[1])>0:
			obj=IAccessible(IAccessibleObject=lastChild[0],IAccessibleChildID=lastChild[1])
			if (obj and winUser.isDescendantWindow(self.windowHandle,obj.windowHandle)) or self.windowHandle==winUser.getDesktopWindow():
				return obj

	def _get_children(self):
		if self.IAccessibleChildID>0:
			return []
		childCount= self.IAccessibleObject.accChildCount
		if childCount==0:
			return []
		children=[]
		for child in IAccessibleHandler.accessibleChildren(self.IAccessibleObject,0,childCount):
			if child and child[0]==self.IAccessibleObject:
				children.append(IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=child[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=child[1]))
			elif child and child[0].accRole(child[1])==IAccessibleHandler.ROLE_SYSTEM_WINDOW:
				children.append(getNVDAObjectFromEvent(IAccessibleHandler.windowFromAccessibleObject(child[0]),IAccessibleHandler.OBJID_CLIENT,0))
		children=[x for x in children if x and winUser.isDescendantWindow(self.windowHandle,x.windowHandle)]
		return children

	def doDefaultAction(self):
		IAccessibleHandler.accDoDefaultAction(self.IAccessibleObject,self.IAccessibleChildID)

	def _get_activeChild(self):
		if self.IAccessibleChildID==0:
			res=IAccessibleHandler.accFocus(self.IAccessibleObject)
			if res:
				if res[0]==self.IAccessibleObject:
					return IAccessible(windowHandle=self.windowHandle,IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=res[1],event_windowHandle=self.event_windowHandle,event_objectID=self.event_objectID,event_childID=res[1])
				return IAccessible(IAccessibleObject=res[0],IAccessibleChildID=res[1])

	def _get_hasFocus(self):
		if (self.IAccessibleStates&IAccessibleHandler.STATE_SYSTEM_FOCUSED):
			return True
		else:
			return False

	def setFocus(self):
		try:
			self.IAccessibleObject.accSelect(1,self.IAccessibleChildID)
		except:
			pass

	def _get_statusBar(self):
		windowClasses=(u'msctls_statusbar32',u'TTntStatusBar.UnicodeClass',u'ATL:msctls_statusbar32')
		curWindow=self.windowHandle
		statusWindow=0
		while not statusWindow and curWindow:
			for windowClass in windowClasses:
				statusWindow=ctypes.windll.user32.FindWindowExW(curWindow,0,windowClass,0)
				if statusWindow:
					break
			curWindow=winUser.getAncestor(curWindow,winUser.GA_PARENT)
		if statusWindow:
			return getNVDAObjectFromEvent(statusWindow,IAccessibleHandler.OBJID_CLIENT,0)
		else:
			return None

	def _get_positionString(self):
		position=""
		childID=self.IAccessibleChildID
		if childID>0:
			parent=self.parent
			if parent:
				parentChildCount=parent.childCount
				if parentChildCount>=childID:
					position=_("%s of %s")%(childID,parentChildCount)
		return position

	def event_show(self):
		if self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP:
			self.event_menuStart()

	def _get_groupName(self):
		return None
		if self.IAccessibleChildID>0:
			return None
		else:
			return super(IAccessible,self)._get_groupName()

	def speakDescendantObjects(self,hashList=None):
		if hashList is None:
			hashList=[]
		child=self.firstChild
		while child and winUser.isDescendantWindow(self.windowHandle,child.windowHandle):
			h=hash(child)
			if h not in hashList:
				hashList.append(h)
				speech.speakObject(child,reason=speech.REASON_FOCUS)
				child.speakDescendantObjects(hashList=hashList)
			child=child.next

	def event_gainFocus(self):
		if self.IAccessibleRole in [IAccessibleHandler.ROLE_SYSTEM_MENUITEM,IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP,IAccessibleHandler.ROLE_SYSTEM_MENUBAR]:
			parent=self.parent
			if parent and parent.role in (controlTypes.ROLE_MENUBAR,controlTypes.ROLE_POPUPMENU,controlTypes.ROLE_MENUITEM):
				speech.cancelSpeech()
		Window.event_gainFocus(self)

	def event_menuStart(self):
		focusObject=api.getFocusObject()
		parentObject=focusObject.parent if focusObject else None
		if self!=focusObject and self!=parentObject  and self.IAccessibleRole in [IAccessibleHandler.ROLE_SYSTEM_MENUITEM,IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP]:
			api.setFocusObject(self)
			speech.cancelSpeech()
			if self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP and isinstance(focusObject,IAccessible) and focusObject.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_MENUITEM:
				speech.speakObject(self,reason=speech.REASON_FOCUS)
			else:
				speech.speakObject(self,reason=speech.REASON_FOCUS)

	def event_menuEnd(self):
		oldFocus=api.getFocusObject()
		if self.IAccessibleRole in (IAccessibleHandler.ROLE_SYSTEM_MENUITEM,IAccessibleHandler.ROLE_SYSTEM_MENUPOPUP) and self!=api.getFocusObject():
			return
		api.processPendingEvents()
		focusObject=api.getFocusObject()
		if focusObject.role not in (controlTypes.ROLE_MENUITEM,controlTypes.ROLE_POPUPMENU) or focusObject!=oldFocus:
			return
		obj=api.findObjectWithFocus()
		IAccessibleHandler.focus_manageEvent(obj)


	def event_selection(self):
		return self.event_stateChange()

	def event_selectionAdd(self):
		return self.event_stateChange()

	def event_selectionRemove(self):
		return self.event_stateChange()

	def event_selectionWithIn(self):
		return self.event_stateChange()

class IAccessibleWindow(IAccessible):

	def _get_name(self):
		return super(IAccessibleWindow,self)._get_name()
		if not name or (isinstance(name,basestring) and name.isspace()):
			name=self.windowClassName
		return name

	def _get_firstChild(self):
		child=super(IAccessibleWindow,self)._get_firstChild()
		if child:
			return child
		if JABHandler.isJavaWindow(self.windowHandle):
			jabContext=JABHandler.JABContext(hwnd=self.windowHandle)
			return NVDAObjects.JAB.JAB(jabContext=jabContext)
		return None

	def _get_lastChild(self):
		child=super(IAccessibleWindow,self)._get_lastChild()
		if child:
			return child
		if JABHandler.isJavaWindow(self.windowHandle):
			jabContext=JABHandler.JABContext(hwnd=self.windowHandle)
			return NVDAObjects.JAB.JAB(jabContext=jabContext)
		return None

	def _get_children(self):
		children=super(IAccessibleWindow,self)._get_children()
		if children:
			return children
		children=[]
		if JABHandler.isJavaWindow(self.windowHandle):
			jabContext=JABHandler.JABContext(hwnd=self.windowHandle)
			obj=NVDAObjects.JAB.JAB(jabContext=jabContext)
			if obj:
				children.append(obj)
		return children

class Groupbox(IAccessible):

	def _get_description(self):
		next=self.next
		if next and next.name==self.name and next.role==controlTypes.ROLE_GRAPHIC:
			next=next.next
		if next and next.role==controlTypes.ROLE_STATICTEXT:
			nextNext=next.next
			if nextNext and nextNext.name!=next.name:
				return next.name
		return super(Groupbox,self)._get_description()

class Dialog(IAccessible):
	"""
	Based on NVDAObject but on foreground events, the dialog contents gets read.
	"""

	def _get_role(self):
		return controlTypes.ROLE_DIALOG

	def _get_value(self):
		return None

	def _get_description(self):
		children=self.children
		if len(children)==1 and children[0].role==controlTypes.ROLE_PANE:
			children=children[0].children
		textList=[]
		childCount=len(children)
		for index in range(childCount):
			if children[index].role==controlTypes.ROLE_STATICTEXT:
				childName=children[index].name
				childStates=children[index].states
				if controlTypes.STATE_INVISIBLE in childStates or controlTypes.STATE_UNAVAILABLE in childStates:
					continue
				if index>0 and children[index-1].role==controlTypes.ROLE_GROUPING:
					continue
				if index>1 and children[index-1].role==controlTypes.ROLE_GRAPHIC and children[index-2].role==controlTypes.ROLE_GROUPING:
					continue
				if childName and ((index+1)>=childCount or children[index+1].role in (controlTypes.ROLE_GRAPHIC,controlTypes.ROLE_STATICTEXT,controlTypes.ROLE_SEPARATOR) or children[index+1].name!=childName):
 					textList.append(childName)
		return " ".join(textList)

	def event_gainFocus(self):
		super(Dialog,self).event_gainFocus()
		children=self.children
		for child in children:
			if child.role==controlTypes.ROLE_PROPERTYPAGE:
				IAccessibleHandler.focus_manageEvent(child,needsFocusState=False)


class PropertyPage(Dialog):

	def _get_role(self):
		return controlTypes.ROLE_PROPERTYPAGE

	def _get_name(self):
		name=super(PropertyPage,self)._get_name()
		if not name:
			tc=self.next
			if tc and tc.role==controlTypes.ROLE_TABCONTROL:
				children=tc.children
				for index in range(len(children)):
					if (children[index].role==controlTypes.ROLE_TAB) and (controlTypes.STATE_SELECTED in children[index].states):
						name=children[index].name
						break
		return name

class TrayClockWClass(IAccessible):
	"""
	Based on NVDAObject but the role is changed to clock.
	"""

	def _get_role(self):
		return controlTypes.ROLE_CLOCK

class OutlineItem(IAccessible):

	def _get_value(self):
		val=super(OutlineItem,self)._get_value()
		try:
			int(val)
		except:
			return val

class Tooltip(IAccessible):

	def event_show(self):
		if (config.conf["presentation"]["reportTooltips"] and (self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_TOOLTIP)) or (config.conf["presentation"]["reportHelpBalloons"] and (self.IAccessibleRole==IAccessibleHandler.ROLE_SYSTEM_HELPBALLOON)):
			speech.speakObject(self,reason=speech.REASON_FOCUS)

class ConsoleWindowClass(IAccessible):

	def event_nameChange(self):
		pass

class MozillaProgressBar(IAccessible):

	def event_valueChange(self):
		if config.conf["presentation"]["beepOnProgressBarUpdates"] and winUser.isDescendantWindow(winUser.getForegroundWindow(),self.windowHandle):
			val=self.value
			if val=="" or val is None:
				return
			if val!=globalVars.lastProgressValue:
				baseFreq=110
				tones.beep(baseFreq*(1+(float(val[:-1])/6.25)),40)
				globalVars.lastProgressValue=val
		else:
			super(MozillaProgressBar,self).event_valueChange()

class MozillaUIWindowClass_application(IAccessible):

	def _get_value(self):
		return None

	def event_nameChange(self):
		if self.windowHandle==api.getForegroundObject().windowHandle:
			speech.speakObjectProperties(self,name=True,reason=speech.REASON_QUERY)

class MozillaDocument(IAccessible):

	def _get_value(self):
		return 

class MozillaListItem(IAccessible):

	def _get_name(self):
		name=super(MozillaListItem,self)._get_name()
		if self.IAccessibleStates&IAccessibleHandler.STATE_SYSTEM_READONLY:
			children=super(MozillaListItem,self)._get_children()
			if len(children)>0 and (children[0].IAccessibleRole in ["bullet",IAccessibleHandler.ROLE_SYSTEM_STATICTEXT]):
				name=children[0].value
		return name

	def _get_children(self):
		children=super(MozillaListItem,self)._get_children()
		if self.IAccessibleStates&IAccessibleHandler.STATE_SYSTEM_READONLY and len(children)>0 and (children[0].IAccessibleRole in ["bullet",IAccesssibleHandler.ROLE_SYSTEM_STATICTEXT]):
			del children[0]
		return children

class SHELLDLL_DefView_client(IAccessible):

	speakOnGainFocus=False

class List(IAccessible):

	def _get_name(self):
		name=super(List,self)._get_name()
		if not name:
			name=super(IAccessible,self)._get_name()
		return name

	def _get_role(self):
		return controlTypes.ROLE_LIST

	def speakDescendantObjects(self,hashList=None):
		child=self.activeChild
		if child:
			speech.speakObject(child,reason=speech.REASON_FOCUS)

class ComboBox(IAccessible):

	def speakDescendantObjects(self,hashList=None):
		child=self.activeChild
		if child:
			speech.speakObject(child,reason=speech.REASON_FOCUS)

class Outline(IAccessible):

	def speakDescendantObjects(self,hashList=None):
		child=self.activeChild
		if child:
			speech.speakObject(child,reason=speech.REASON_FOCUS)

class ProgressBar(IAccessible):

	def event_valueChange(self):
		if config.conf["presentation"]["beepOnProgressBarUpdates"] and controlTypes.STATE_INVISIBLE not in self.states and winUser.isWindowVisible(self.windowHandle) and winUser.isDescendantWindow(winUser.getForegroundWindow(),self.windowHandle):
			val=self.value
			if val!=globalVars.lastProgressValue:
				baseFreq=110
				tones.beep(int(baseFreq*(1+(float(val[:-1])/6.25))),40)
				globalVars.lastProgressValue=val
		else:
			super(ProgressBar,self).event_valueChange()

class InternetExplorerClient(IAccessible):

	def _get_description(self):
		return None

class StatusBar(IAccessible):

	def _get_value(self):
		oldValue=super(StatusBar,self)._get_value()
		valueFromChildren=" ".join([" ".join([y for y in (x.name,x.value) if y and not y.isspace()]) for x in super(StatusBar,self)._get_children() if x.role in (controlTypes.ROLE_EDITABLETEXT,controlTypes.ROLE_STATICTEXT)])
		if valueFromChildren:
			return valueFromChildren
		else:
			return oldValue

	def _get_firstChild(self):
		return None

	def _get_lastChild(self):
		return None

	def _get_children(self):
		return []

class SysLink(IAccessible):

	def reportFocus(self):
		pass

class TaskListIcon(IAccessible):

	def _get_role(self):
		return controlTypes.ROLE_ICON

	def reportFocus(self):
		if controlTypes.STATE_INVISIBLE in self.states:
			return
		super(TaskListIcon,self).reportFocus()


class ToolBarButton(IAccessible):

	def old_event_gainFocus(self):
		super(ToolBarButton, self).event_gainFocus()
		# If the mouse is on another toolbar control, some toolbars will rudely
		# bounce the focus back to the object under the mouse after a brief pause.
		# This is particularly annoying in the system tray in Windows XP.
		# Moving the mouse to the focus object isn't a good solution because
		# sometimes, the focus can't be moved away from the object under the mouse.
		# Therefore, move the mouse out of the way.
		winUser.setCursorPos(1, 1)

class MenuItem(IAccessible):

	def _get_description(self):
		name=self.name
		description=super(MenuItem,self)._get_description()
		if description!=name:
			return description
		else:
			return None

###class mappings

_staticMap={
	(None,IAccessibleHandler.ROLE_SYSTEM_WINDOW):"IAccessibleWindow",
	(None,IAccessibleHandler.ROLE_SYSTEM_CLIENT):"IAccessibleWindow",
	("tooltips_class32",IAccessibleHandler.ROLE_SYSTEM_TOOLTIP):"Tooltip",
	("tooltips_class32",IAccessibleHandler.ROLE_SYSTEM_HELPBALLOON):"Tooltip",
	(None,IAccessibleHandler.ROLE_SYSTEM_DIALOG):"Dialog",
	(None,IAccessibleHandler.ROLE_SYSTEM_PROPERTYPAGE):"PropertyPage",
	(None,IAccessibleHandler.ROLE_SYSTEM_GROUPING):"Groupbox",
	(None,IAccessibleHandler.ROLE_SYSTEM_ALERT):"Dialog",
	("TrayClockWClass",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"TrayClockWClass",
	("Edit",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TRxRichEdit",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"delphi.TRxRichEdit",
	("RichEdit20",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.RichEdit20",
	("RichEdit20A",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.RichEdit20",
	("RichEdit20W",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.RichEdit20",
	("RICHEDIT50W",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.RichEdit50",
	(None,IAccessibleHandler.ROLE_SYSTEM_OUTLINEITEM):"OutlineItem",
	("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_APPLICATION):"MozillaUIWindowClass_application",
	("MozillaUIWindowClass",IAccessibleHandler.ROLE_SYSTEM_APPLICATION):"MozillaUIWindowClass_application",
	("MozillaDialogClass",IAccessibleHandler.ROLE_SYSTEM_ALERT):"Dialog",
	("MozillaDialogClass",IAccessibleHandler.ROLE_SYSTEM_DIALOG):"Dialog",
	("MozillaUIWindowClass",IAccessibleHandler.ROLE_SYSTEM_ALERT):"Dialog",
	("MozillaUIWindowClass",IAccessibleHandler.ROLE_SYSTEM_DIALOG):"Dialog",
	("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_ALERT):"Dialog",
	("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_DIALOG):"Dialog",
	("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):"MozillaListItem",
	("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):"MozillaListItem",
	("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_DOCUMENT):"MozillaDocument",
	("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_DOCUMENT):"MozillaDocument",
	("MozillaContentWindowClass",IAccessibleHandler.ROLE_SYSTEM_PROGRESSBAR):"MozillaProgressBar",
	("MozillaWindowClass",IAccessibleHandler.ROLE_SYSTEM_PROGRESSBAR):"MozillaProgressBar",
	("ConsoleWindowClass",IAccessibleHandler.ROLE_SYSTEM_WINDOW):"ConsoleWindowClass",
	("ConsoleWindowClass",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"winConsole.WinConsole",
	("SHELLDLL_DefView",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"SHELLDLL_DefView_client",
	(None,IAccessibleHandler.ROLE_SYSTEM_LIST):"List",
	(None,IAccessibleHandler.ROLE_SYSTEM_COMBOBOX):"ComboBox",
	(None,IAccessibleHandler.ROLE_SYSTEM_OUTLINE):"Outline",
	("msctls_progress32",IAccessibleHandler.ROLE_SYSTEM_PROGRESSBAR):"ProgressBar",
	("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_TEXT):"MSHTML.MSHTML",
	("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_PANE):"MSHTML.MSHTML",
	("Internet Explorer_Server",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"InternetExplorerClient",
	("msctls_statusbar32",IAccessibleHandler.ROLE_SYSTEM_STATUSBAR):"StatusBar",
	("TTntEdit.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TMaskEdit",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TTntMemo.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TRichView",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"delphi.TRichView",
	("TRichViewEdit",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"delphi.TRichViewEdit",
	("TRichEdit",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"edit.Edit",
	("TTntDrawGrid.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"List",
	("SysListView32",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):"sysListView32.ListItem",
	("SysTreeView32",IAccessibleHandler.ROLE_SYSTEM_OUTLINEITEM):"sysTreeView32.TreeViewItem",
	("ATL:SysListView32",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):"sysListView32.ListItem",
	("TWizardForm",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"Dialog",
	("SysLink",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"SysLink",
	("_WwG",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"winword.WordDocument",
	("EXCEL7",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"excel.ExcelGrid",
	("Scintilla",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"scintilla.Scintilla",
	("#32771",IAccessibleHandler.ROLE_SYSTEM_LISTITEM):"TaskListIcon",
	("TInEdit.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TEdit",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TTntStatusBar.UnicodeClass",IAccessibleHandler.ROLE_SYSTEM_STATUSBAR):"StatusBar",
	("ToolbarWindow32",IAccessibleHandler.ROLE_SYSTEM_PUSHBUTTON):"ToolBarButton",
	("TFilenameEdit",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TSpinEdit",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TGroupBox",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"delphi.TGroupBox",
	("TFormOptions",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"delphi.TFormOptions",
	("TFormOptions",IAccessibleHandler.ROLE_SYSTEM_WINDOW):"delphi.TFormOptions",
	("TTabSheet",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"delphi.TTabSheet",
	("ThunderRT6TextBox",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("TMemo",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("RICHEDIT",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("MsiDialogCloseClass",IAccessibleHandler.ROLE_SYSTEM_CLIENT):"Dialog",
	("TPasswordEdit",IAccessibleHandler.ROLE_SYSTEM_TEXT):"edit.Edit",
	("#32768",IAccessibleHandler.ROLE_SYSTEM_MENUITEM):"MenuItem",
	("ToolbarWindow32",IAccessibleHandler.ROLE_SYSTEM_MENUITEM):"MenuItem",
	("ATL:msctls_statusbar32",IAccessibleHandler.ROLE_SYSTEM_STATUSBAR):"StatusBar",
}
