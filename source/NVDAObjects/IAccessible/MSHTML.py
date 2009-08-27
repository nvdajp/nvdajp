#NVDAObjects/MSHTML.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import ctypes
from comtypes import COMError
import comtypes.client
import comtypes.automation
from comtypes import IServiceProvider
import winUser
import globalVars
import oleacc
import aria
from keyUtils import key, sendKey
import api
import textInfos
from logHandler import log
import speech
import controlTypes
from . import IAccessible
import NVDAObjects
import virtualBufferHandler

lastMSHTMLEditGainFocusTimeStamp=0

IID_IHTMLElement=comtypes.GUID('{3050F1FF-98B5-11CF-BB82-00AA00BDCE0B}')

def nextIAccessibleInDom(HTMLNode,back=False):
	notFound=False
	firstLoop=True
	while HTMLNode: 
		if not firstLoop:
			child=HTMLNode.firstChild if not back else HTMLNode.lastChild
		else:
			child=None
			firstLoop=False
		if child:
			HTMLNode=child
		else:
			sibling=HTMLNode.nextSibling if not back else HTMLNode.previousSibling
			if not sibling:
				try:
					parent=HTMLNode.parentNode
				except COMError:
					parent=None
				while parent and not HTMLNodeHasIAccessible(parent):
					sibling=parent.nextSibling if not back else parent.previousSibling
					if sibling:
						break
					try:
						parent=parent.parentElement
					except COMError:
						parent=None
			HTMLNode=sibling
		if HTMLNode:
			try:
				return IAccessibleFromHTMLNode(HTMLNode)
			except NotImplementedError:
				pass

def IAccessibleFromHTMLNode(HTMLNode):
	try:
		s=HTMLNode.QueryInterface(IServiceProvider)
		return s.QueryService(oleacc.IAccessible._iid_,oleacc.IAccessible)
	except COMError:
		raise NotImplementedError

def HTMLNodeHasIAccessible(HTMLNode):
	try:
		return bool(IAccessibleFromHTMLNode(HTMLNode))
	except NotImplementedError:
		return False

def HTMLNodeFromIAccessible(IAccessibleObject):
	try:
		s=IAccessibleObject.QueryInterface(IServiceProvider)
		return comtypes.client.dynamic.Dispatch(s.QueryService(IID_IHTMLElement,comtypes.automation.IDispatch))
	except COMError:
		raise NotImplementedError

def locateHTMLElementByID(document,ID):
	element=document.getElementById(ID)
	if element:
		return element
	nodeName=document.body.nodeName.lower()
	if nodeName=="frameset":
		tag="frame"
	else:
		tag="iframe"
	frames=document.getElementsByTagName(tag)
	for frame in frames:
		pacc=IAccessibleFromHTMLNode(frame)
		childPacc=pacc.accChild(1)
		childElement=HTMLNodeFromIAccessible(childPacc)
		childElement=locateHTMLElementByID(childElement.document,ID)
		if childElement:
			return childElement

class MSHTMLTextInfo(textInfos.TextInfo):

	def _expandToLine(self,textRange):
		parent=textRange.parentElement()
		if not parent.isMultiline: #fastest solution for single line edits (<input type="text">)
			textRange.expand("textEdit")
			return
		parentRect=parent.getBoundingClientRect()
		#This can be simplified when comtypes is fixed
		lineTop=comtypes.client.dynamic._Dispatch(textRange._comobj).offsetTop
		lineLeft=parentRect.left+parent.clientLeft
		#editable documents have a different right most boundary to <textarea> elements.
		if self.obj.HTMLNode.document.body.isContentEditable:
			lineRight=parentRect.right 
		else:
			lineRight=parentRect.left+parent.clientWidth
		tempRange=textRange.duplicate()
		tempRange.moveToPoint(lineLeft,lineTop)
		textRange.setEndPoint("startToStart",tempRange)
		tempRange.moveToPoint(lineRight,lineTop)
		textRange.setEndPoint("endToStart",tempRange)

	def __init__(self,obj,position,_rangeObj=None):
		super(MSHTMLTextInfo,self).__init__(obj,position)
		if _rangeObj:
			self._rangeObj=_rangeObj.duplicate()
			return
		try:
			editableBody=self.obj.HTMLNode.tagName=="BODY" and self.obj.HTMLNode.isContentEditable
		except:
			editableBody=False
		if editableBody:
			self._rangeObj=self.obj.HTMLNode.document.selection.createRange()
		else:
			self._rangeObj=self.obj.HTMLNode.createTextRange()
		if position in (textInfos.POSITION_CARET,textInfos.POSITION_SELECTION):
			if self.obj.HTMLNode.uniqueID!=self.obj.HTMLNode.document.activeElement.uniqueID:
				raise RuntimeError("Only works with currently selected element")
			if not editableBody:
				mark=self.obj.HTMLNode.document.selection.createRange().GetBookmark()
				self._rangeObj.MoveToBookmark(mark)
				t=self._rangeObj.duplicate()
				if not t.expand("word"):
					self._rangeObj.expand("textedit")
					self._rangeObj.collapse(False)
			if position==textInfos.POSITION_CARET:
				self._rangeObj.collapse()
			return
		if position==textInfos.POSITION_FIRST:
			self._rangeObj.collapse()
		elif position==textInfos.POSITION_LAST:
			self._rangeObj.expand("textedit")
			self.collapse(True)
			self._rangeObj.move("character",-1)
		elif position==textInfos.POSITION_ALL:
			self._rangeObj.expand("textedit")
		elif isinstance(position,textInfos.Bookmark):
			if position.infoClass==self.__class__:
				self._rangeObj.moveToBookmark(position.data)
			else:
				raise TypeError("Bookmark was for %s type, not for %s type"%(position.infoClass.__name__,self.__class__.__name__))
		else:
			raise NotImplementedError("position: %s"%position)

	def expand(self,unit):
		if unit==textInfos.UNIT_PARAGRAPH:
			unit=textInfos.UNIT_LINE
		if unit==textInfos.UNIT_LINE and self.basePosition not in [textInfos.POSITION_SELECTION,textInfos.POSITION_CARET]:
			unit=textInfos.UNIT_SENTENCE
		if unit==textInfos.UNIT_READINGCHUNK:
			unit=textInfos.UNIT_SENTENCE
		if unit==textInfos.UNIT_CHARACTER:
			self._rangeObj.expand("character")
		elif unit==textInfos.UNIT_WORD:
			#Expand to word at the start of a control is broken in MSHTML
			#Unless we expand to character first.
			self._rangeObj.expand("character")
			self._rangeObj.expand("word")
		elif unit==textInfos.UNIT_SENTENCE:
			self._rangeObj.expand("sentence")
		elif unit==textInfos.UNIT_LINE:
			self._expandToLine(self._rangeObj)
		elif unit==textInfos.UNIT_STORY:
			self._rangeObj.expand("textedit")
		else:
			raise NotImplementedError("unit: %s"%unit)

	def _get_isCollapsed(self):
		if self._rangeObj.compareEndPoints("startToEnd",self._rangeObj)==0:
			return True
		else:
			return False

	def collapse(self,end=False):
		self._rangeObj.collapse(not end)

	def copy(self):
		return self.__class__(self.obj,None,_rangeObj=self._rangeObj.duplicate())

	def compareEndPoints(self,other,which):
		return self._rangeObj.compareEndPoints(which,other._rangeObj)

	def setEndPoint(self,other,which):
		self._rangeObj.setEndPoint(which,other._rangeObj)

	def _get_text(self):
		text=self._rangeObj.text
		if not text:
			text=""
		if controlTypes.STATE_PROTECTED in self.obj.states:
			text='*'*len(text)
		return text

	def move(self,unit,direction, endPoint=None):
		if unit in [textInfos.UNIT_READINGCHUNK,textInfos.UNIT_LINE]:
			unit=textInfos.UNIT_SENTENCE
		if unit==textInfos.UNIT_STORY:
			unit="textedit"
		if endPoint=="start":
			moveFunc=self._rangeObj.moveStart
		elif endPoint=="end":
			moveFunc=self._rangeObj.moveEnd
		else:
			moveFunc=self._rangeObj.move
		res=moveFunc(unit,direction)
		return res

	def updateCaret(self):
		self._rangeObj.select()

	def updateSelection(self):
		self._rangeObj.select()

	def _get_bookmark(self):
		return textInfos.Bookmark(self.__class__,self._rangeObj.getBookmark())

class MSHTML(IAccessible):

	def __init__(self,*args,**kwargs):
		super(MSHTML,self).__init__(*args,**kwargs)
		try:
			self.HTMLNode.createTextRange()
			self.TextInfo=MSHTMLTextInfo
		except:
			pass
		if self.TextInfo==MSHTMLTextInfo:
			[self.bindKey_runtime(keyName,scriptName) for keyName,scriptName in [
				("ExtendedUp","moveByLine"),
				("ExtendedDown","moveByLine"),
				("ExtendedLeft","moveByCharacter"),
				("ExtendedRight","moveByCharacter"),
				("Control+ExtendedUp","moveByParagraph"),
				("Control+ExtendedDown","moveByParagraph"),
				("Control+ExtendedLeft","moveByWord"),
				("Control+ExtendedRight","moveByWord"),
				("Shift+ExtendedRight","changeSelection"),
				("Shift+ExtendedLeft","changeSelection"),
				("Shift+ExtendedHome","changeSelection"),
				("Shift+ExtendedEnd","changeSelection"),
				("Shift+ExtendedUp","changeSelection"),
				("Shift+ExtendedDown","changeSelection"),
				("Control+Shift+ExtendedLeft","changeSelection"),
				("Control+Shift+ExtendedRight","changeSelection"),
				("ExtendedHome","moveByCharacter"),
				("ExtendedEnd","moveByCharacter"),
				("control+extendedHome","moveByLine"),
				("control+extendedEnd","moveByLine"),
				("control+shift+extendedHome","changeSelection"),
				("control+shift+extendedEnd","changeSelection"),
				("ExtendedDelete","moveByCharacter"),
				("Back","backspace"),
			]]

	def _get_HTMLNode(self):
		if self.IAccessibleChildID>0:
			return
		if not hasattr(self,'_HTMLNode'):
			try:
				HTMLNode=HTMLNodeFromIAccessible(self.IAccessibleObject)
			except NotImplementedError:
				HTMLNode=None
			self._HTMLNode=HTMLNode
		return self._HTMLNode

	def _isEqual(self, other):
		try:
			return self.windowHandle == other.windowHandle and self.HTMLNode.uniqueNumber == other.HTMLNode.uniqueNumber
		except (COMError, AttributeError):
			pass
		return super(MSHTML, self)._isEqual(other)

	def _get_value(self):
		IARole=self.IAccessibleRole
		if IARole in (oleacc.ROLE_SYSTEM_PANE,oleacc.ROLE_SYSTEM_TEXT):
			return ""
		else:
			return super(MSHTML,self).value

	def _get_basicText(self):
		if self.HTMLNode:
			try:
				text=self.HTMLNode.innerText
			except COMError:
				text=None
			if text:
				return text
		return super(MSHTML,self).basicText

	def _get_role(self):
		if self.HTMLNode:
			try:
				ariaRole=self.HTMLNode.getAttribute('role')
			except COMError:
				ariaRole=None
			if ariaRole:
				role=aria.ariaRolesToNVDARoles.get(ariaRole)
				if role:
					return role
			try:
				nodeName=self.HTMLNode.NodeName
			except COMError:
				nodeName=None
			if nodeName:
				nodeName=nodeName.lower()
				if nodeName in ("body","frameset"):
					return controlTypes.ROLE_DOCUMENT
		if self.IAccessibleChildID>0:
			states=super(MSHTML,self).states
			if controlTypes.STATE_LINKED in states:
				return controlTypes.ROLE_LINK
		return super(MSHTML,self).role

	def _get_states(self):
		states=super(MSHTML,self).states
		e=self.HTMLNode
		if e:
			try:
				isContentEditable=e.isContentEditable
			except COMError:
				isContentEditable=False
			if isContentEditable:
				states.add(controlTypes.STATE_EDITABLE)
			try:
				isMultiline=e.isMultiline
			except COMError:
				isMultiline=False
			if self.TextInfo==MSHTMLTextInfo and isMultiline: 
				states.add(controlTypes.STATE_MULTILINE)
			try:
				required=e.getAttribute('aria-required')
			except COMError:
				required=None
			if required and required.lower()=='true':
				states.add(controlTypes.STATE_REQUIRED)
		return states

	def _get_isContentEditable(self):
		if self.HTMLNode:
			try:
				return bool(self.HTMLNode.isContentEditable)
			except:
				return False
		else:
			return False

	def _get_previous(self):
		if self.IAccessibleChildID>1:
			newChildID=self.IAccessibleChildID-1
			try:
				return IAccessible(IAccessibleObject=self.IAccessibleObject.accChild(newChildID),IAccessibleChildID=0)
			except COMError:
				return IAccessible(IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=newChildID)
		pacc=nextIAccessibleInDom(self.HTMLNode,back=True)
		if pacc:
			return IAccessible(IAccessibleObject=pacc,IAccessibleChildID=0)

	def _get_next(self):
		if self.IAccessibleChildID>0:
			if self.IAccessibleChildID<self.childCount:
				newChildID=self.IAccessibleChildID+1
				try:
					pacc=self.IAccessibleObject.accChild(newChildID)
					return IAccessible(IAccessibleObject=pacc,IAccessibleChildID=0)
				except COMError:
					return IAccessible(IAccessibleObject=self.IAccessibleObject,IAccessibleChildID=newChildID)
			return None
		pacc=nextIAccessibleInDom(self.HTMLNode)
		if pacc:
			return IAccessible(IAccessibleObject=pacc,IAccessibleChildID=0)

	def _get_firstChild(self):
		child=super(MSHTML,self).firstChild
		while isinstance(child,IAccessible) and child.IAccessibleChildID>0:
			child=child.next
		return child

	def _get_lastChild(self):
		child=super(MSHTML,self).lastChild
		while isinstance(child,IAccessible) and child.IAccessibleChildID>0:
			child=child.previous
		return child

	def _get_columnNumber(self):
		if not self.role==controlTypes.ROLE_TABLECELL or not self.HTMLNode:
			raise NotImplementedError
		try:
			return self.HTMLNode.cellIndex+1
		except:
			raise NotImplementedError

	def _get_rowNumber(self):
		if not self.role==controlTypes.ROLE_TABLECELL or not self.HTMLNode:
			raise NotImplementedError
		HTMLNode=self.HTMLNode
		while HTMLNode:
			try:
				return HTMLNode.rowIndex+1
			except:
				pass
			HTMLNode=HTMLNode.parentNode
		raise NotImplementedError

	def _get_rowCount(self):
		if self.role!=controlTypes.ROLE_TABLE or not self.HTMLNode:
			raise NotImplementedError
		try:
			return len([x for x in self.HTMLNode.rows])
		except:
			raise NotImplementedError

	def scrollIntoView(self):
		if not self.HTMLNode:
			return
		try:
			self.HTMLNode.scrollInToView()
		except COMError:
			pass

	def doAction(self, index=None):
		states = self.states
		if controlTypes.STATE_INVISIBLE in states or controlTypes.STATE_OFFSCREEN in states:
			raise NotImplementedError
		l = self.location
		if not l:
			raise NotImplementedError
		x = l[0] + (l[2] / 2)
		y = l[1] + (l[3] / 2)
		if x < 0 or y < 0:
			return
		oldX, oldY = winUser.getCursorPos()
		winUser.setCursorPos(x, y)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN, 0, 0, None, None)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP, 0, 0, None, None)
		winUser.setCursorPos(oldX, oldY)
