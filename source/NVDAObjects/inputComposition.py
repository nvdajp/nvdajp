# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2025 NV Access Limited, Cary-Rowen
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import eventHandler  # noqa: I001
import queueHandler
import controlTypes
from config.configFlags import TypingEcho
import characterProcessing
import speech
import config
from NVDAObjects.window import Window
from .behaviors import EditableTextWithAutoSelectDetection, CandidateItem as CandidateItemBehavior
from textInfos.offsets import OffsetsTextInfo

# nvdajp begin
from logHandler import log
import jpUtils
import winUser
import time
import braille
# nvdajp end


def calculateInsertedChars(oldComp, newComp):
	oldLen = len(oldComp)
	newLen = len(newComp)
	minLen = min(oldLen, newLen)
	diffStart = 0
	diffEnd = newLen
	for index in range(minLen):
		if newComp[index] != oldComp[index]:
			break
		diffStart = index + 1
	for index in range(minLen, 0, -1):
		backIndex = index - minLen - 1
		if newComp[backIndex] != oldComp[backIndex]:
			break
		diffEnd = newLen + backIndex
	diffEnd = max(diffEnd, diffStart + (newLen - oldLen))
	return newComp[diffStart:diffEnd]


class InputCompositionTextInfo(OffsetsTextInfo):
	encoding = None

	def _getSelectionOffsets(self):
		return (
			self.obj.readingSelectionOffsets if self.obj.isReading else self.obj.compositionSelectionOffsets
		)

	def _getCaretOffset(self):
		return self._getSelectionOffsets()[0]

	def _getStoryText(self):
		return self.obj.readingString if self.obj.isReading else self.obj.compositionString

	def _getStoryLength(self):
		return len(self._getStoryText())


# nvdajp begin
# from keyboardHandler.internal_keyDownEvent
lastKeyGesture = None
# Session id for compAttr IME Enter vs cancel detection. compAttr IMEs may send
# (empty, -1, -1) on commit as well as on cancel.
_compositionSessionId = 0
_compositionCommitEnterSessionId: int | None = None
_compositionSessionInProgress = False


def beginCompositionSessionIfNeeded() -> None:
	global _compositionSessionId, _compositionCommitEnterSessionId, _compositionSessionInProgress
	if _compositionSessionInProgress:
		return
	_compositionSessionId += 1
	_compositionCommitEnterSessionId = None
	_compositionSessionInProgress = True


def endCompositionSession() -> None:
	global _compositionSessionId, _compositionCommitEnterSessionId, _compositionSessionInProgress
	_compositionCommitEnterSessionId = None
	_compositionSessionInProgress = False
	_compositionSessionId += 1


def resetCompositionKeyState() -> None:
	endCompositionSession()


def isCompositionActive() -> bool:
	from NVDAHelper import lastCompString

	if lastCompString:
		return True
	if not isInInputComposition():
		return False
	import api

	focus = api.getFocusObject()
	if isinstance(focus, InputComposition):
		comp = focus
	elif isinstance(focus.parent, InputComposition):
		comp = focus.parent
	else:
		return False
	return bool(comp.compositionString or comp.readingString)


def isCompositionCommitFromEnter() -> bool:
	return (
		_compositionCommitEnterSessionId is not None
		and _compositionCommitEnterSessionId == _compositionSessionId
		and _compositionSessionInProgress
	)


def isInInputComposition(focus=None) -> bool:
	if focus is None:
		import api

		focus = api.getFocusObject()
	if isinstance(focus, InputComposition):
		return True
	if isinstance(focus.parent, InputComposition):
		return True
	if isinstance(focus, CandidateItemBehavior):
		return isinstance(focus.parent, InputComposition)
	return False


def noteCompositionKeyDown(vkCode: int) -> None:
	global _compositionCommitEnterSessionId
	if vkCode == winUser.VK_RETURN and isCompositionActive():
		_compositionCommitEnterSessionId = _compositionSessionId


def reportKeyDownEvent(gesture):
	global lastKeyGesture
	lastKeyGesture = gesture


def needDiscriminantReading(gesture):
	if not gesture:
		return False
	if (winUser.VK_CONTROL, False) in gesture.generalizedModifiers or gesture.vkCode in (
		winUser.VK_SPACE,
		winUser.VK_CONVERT,
		winUser.VK_IME_ON,
		winUser.VK_LEFT,
		winUser.VK_RIGHT,
		winUser.VK_UP,
		winUser.VK_DOWN,
		winUser.VK_F2,
		winUser.VK_F3,
		winUser.VK_F4,
		winUser.VK_F5,
		winUser.VK_F6,
		winUser.VK_F7,
		winUser.VK_F8,
		winUser.VK_F9,
		winUser.VK_F10,
		winUser.VK_F11,
		winUser.VK_NONCONVERT,
		winUser.VK_IME_OFF,
		winUser.VK_ESCAPE,
		winUser.VK_TAB,
	):
		return True
	# VK_RCONTROL
	return (winUser.VK_CONTROL, True) in gesture.generalizedModifiers


lastCompositionText = None
lastCompositionTime = None


# from NVDAHelper.nvdaControllerInternal_inputCompositionUpdate
def reportPartialSelection(sel):
	global lastCompositionText, lastCompositionTime
	newText = jpUtils.getDiscriminantReading(sel)
	newTextForBraille = jpUtils.getDescriptionForBraille(sel)
	if lastCompositionText == newText and lastCompositionTime and time.time() - lastCompositionTime < 0.1:
		newText = None
	if newText:
		log.debug(newText)
		lastCompositionTime = time.time()
		lastCompositionText = newText
		queueHandler.queueFunction(queueHandler.eventQueue, braille.handler.message, newTextForBraille)
		queueHandler.queueFunction(
			queueHandler.eventQueue,
			speech.speakText,
			newText,
			symbolLevel=characterProcessing.SymbolLevel.ALL,
		)


# nvdajp end


class InputComposition(EditableTextWithAutoSelectDetection, Window):
	TextInfo = InputCompositionTextInfo
	# Translators: The label for a 'composition' Window that appears when the user is typing one or more east-Asian characters into a document.
	name = _("Composition")
	role = controlTypes.Role.EDITABLETEXT
	next = None
	previous = None
	firstChild = None
	lastChild = None
	states = set()  # noqa: RUF012
	location = None
	compositionString = ""
	readingString = ""
	compositionSelectionOffsets = (0, 0)
	readingSelectionOffsets = (0, 0)
	isReading = False
	IAccessibleRole = role

	def __init__(self, parent=None):
		self.parent = parent
		super().__init__(windowHandle=parent.windowHandle)

	def findOverlayClasses(self, clsList):
		clsList.append(InputComposition)
		clsList.append(InputComposition)
		return clsList

	def reportNewText(self, oldString, newString, forceNewText=False):
		global lastCompositionText, lastCompositionTime  # nvdajp
		# nvdajp begin
		newTextForBraille = newText = calculateInsertedChars(
			oldString.strip("\u3000"),
			newString.strip("\u3000"),
		)
		if forceNewText:
			newText = newString.strip("\u3000")
		isCandidate = False
		if (
			config.conf["keyboard"]["nvdajpEnableKeyEvents"]
			and config.conf["inputComposition"]["announceSelectedCandidate"]
			and needDiscriminantReading(lastKeyGesture)
		):
			ns = newString.strip("\u3000")
			newText = jpUtils.getDiscriminantReading(ns)
			newTextForBraille = jpUtils.getDescriptionForBraille(ns)
			isCandidate = True
		if lastCompositionText == newText and lastCompositionTime and time.time() - lastCompositionTime < 1.0:
			newText = None
			isCandidate = False
		# if isCandidate:
		# import tones
		# tones.beep(1000,10)
		if newText:
			if config.conf["keyboard"]["nvdajpEnableKeyEvents"]:
				newText = jpUtils.fixNewText(newText, isCandidate)
				lastCompositionTime = time.time()
				lastCompositionText = newText
				queueHandler.queueFunction(
					queueHandler.eventQueue,
					braille.handler.message,
					newTextForBraille,
				)
			if (
				config.conf["keyboard"]["speakTypedCharacters"] != TypingEcho.OFF.value
				or config.conf["keyboard"]["speakTypedWords"] != TypingEcho.OFF.value
				or isCandidate
			):
				queueHandler.queueFunction(
					queueHandler.eventQueue,
					speech.speakText,
					newText,
					symbolLevel=characterProcessing.SymbolLevel.ALL,
				)
		# nvdajp end

	def compositionUpdate(
		self,
		compositionString,
		selectionStart,
		selectionEnd,
		isReading,
		announce=True,
		forceNewText=False,
	):
		if isReading and not config.conf["inputComposition"]["reportReadingStringChanges"]:
			return
		if not isReading and not config.conf["inputComposition"]["reportCompositionStringChanges"]:
			return
		if announce:
			self.reportNewText(
				(self.readingString if isReading else self.compositionString),
				compositionString,
				forceNewText=forceNewText,
			)
		hasChanged = False
		if isReading:
			self.readingString = compositionString
			self.readingSelectionOffsets = (selectionStart, selectionEnd)
			self.isReading = True
			hasChanged = True
		elif (
			compositionString != self.compositionString
			or (selectionStart, selectionEnd) != self.compositionSelectionOffsets
		):
			self.readingString = ""
			self.readingSelectionOffsets = (0, 0)
			self.isReading = False
			self.compositionString = compositionString
			self.compositionSelectionOffsets = (selectionStart, selectionEnd)
			hasChanged = True
		if hasChanged:
			eventHandler.queueEvent("valueChange", self)
			eventHandler.queueEvent("caret", self)

	def reportFocus(self):
		pass


class CandidateList(Window):
	# Translators: The label for a 'candidate' list that shows a choice of symbols a user can choose from when typing east-Asian characters into a document.
	name = _("Candidate")
	role = controlTypes.Role.LIST
	next = None
	previous = None
	firstChild = None
	lastChild = None
	states = set()  # noqa: RUF012

	def __init__(self, parent=None):
		self.parent = parent
		super().__init__(windowHandle=parent.windowHandle)

	def findOverlayClasses(self, clsList):
		clsList.append(CandidateList)
		return clsList


class CandidateItem(CandidateItemBehavior, Window):
	role = controlTypes.Role.LISTITEM
	firstChild = None
	lastChild = None
	states = set()  # noqa: RUF012

	def __init__(self, parent=None, candidateStrings=[], candidateIndex=0, inputMethod=None):  # noqa: B006
		self.parent = parent
		self.candidateStrings = candidateStrings
		self.candidateIndex = candidateIndex
		self.inputMethod = inputMethod
		super().__init__(windowHandle=parent.windowHandle)

	def findOverlayClasses(self, clsList):
		clsList.append(CandidateItem)
		return clsList

	def _get_candidateNumber(self):
		number = self.candidateIndex
		# Most candidate lists start at 1, except for Boshiami which starts at 0.
		if self.inputMethod != "LIUNT.IME":
			number += 1
		return number

	def _get_name(self):
		number = self.candidateNumber
		candidate = self.candidateStrings[self.candidateIndex]
		return self.getFormattedCandidateName(number, candidate)

	def _get_basicText(self):
		return self.candidateStrings[self.candidateIndex]

	def _get_description(self):
		candidate = self.candidateStrings[self.candidateIndex]
		return self.getFormattedCandidateDescription(candidate)

	def _get_next(self):
		if self.candidateIndex < (len(self.candidateStrings) - 1):
			return CandidateItem(
				parent=self.parent,
				candidateStrings=self.candidateStrings,
				candidateIndex=self.candidateIndex + 1,
				inputMethod=self.inputMethod,
			)

	def _get_previous(self):
		if self.candidateIndex > 0:
			return CandidateItem(
				parent=self.parent,
				candidateStrings=self.candidateStrings,
				candidateIndex=self.candidateIndex - 1,
				inputMethod=self.inputMethod,
			)
