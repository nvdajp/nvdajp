# coding: UTF-8
#brailleDisplayDrivers/kgsbn46.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2014 Takuya Nishimoto

from logHandler import log
import inputCore
from kgs import BrailleDisplayDriver, InputGesture


kgsBn46GestureMapData = {
	"globalCommands.GlobalCommands": {
		"showGui": ("br(kgsbn46):func1",),
		"braille_routeTo": ("br(kgsbn46):route",),
		"braille_scrollBack": ("br(kgsbn46):sl",),
		"braille_scrollForward": ("br(kgsbn46):sr",),
		"review_previousLine": ("br(kgsbn46):func2+bk",),
		"review_nextLine": ("br(kgsbn46):func2+lf",),
		"review_previousWord": ("br(kgsbn46):func2+sl",),
		"review_nextWord": ("br(kgsbn46):func2+sr",),
		"kb:upArrow": ("br(kgsbn46):bk",),
		"kb:downArrow": ("br(kgsbn46):lf",),
		"kb:leftArrow": ("br(kgsbn46):func3",),
		"kb:rightArrow": ("br(kgsbn46):func4",),
	}
}


class BrailleDisplayDriver(BrailleDisplayDriver):
	name = "kgsbn46"
	description = _(u"KGS BrailleNote 46C/46D")
	devName = u"ブレイルノート46C/46D".encode('shift-jis')

	@classmethod
	def getKeyCallback(cls):
		return nvdaKgsBn46HandleKeyInfoProc

	def __init__(self, port="auto"):
		super(BrailleDisplayDriver,self).__init__(port=port)
		self.gestureMap = inputCore.GlobalGestureMap(kgsBn46GestureMapData)


class InputGesture(InputGesture):
	source = BrailleDisplayDriver.name


def nvdaKgsBn46HandleKeyInfoProc(lpKeys):
	keys = (lpKeys[0], lpKeys[1], lpKeys[2])
	log.io("keyInfo %d %d %d" % keys)
	log.io("keyInfo hex %x %x %x" % keys)
	names = set()
	routingIndex = None
	if keys[0] == 0:
		if keys[1] &   1: names.add('lf')
		if keys[1] &   2: names.add('bk')
		if keys[1] &   4: names.add('sr')
		if keys[1] &   8: names.add('sl')
		if keys[1] &  16: names.add('func1')
		if keys[1] &  32: names.add('func2')
		if keys[1] &  64: names.add('func3')
		if keys[1] & 128: names.add('func4')
	else:
		tCode = 240
		if keys[0] &   1+tCode: names.add('func1')
		if keys[0] &   2+tCode: names.add('func2')
		if keys[0] &   4+tCode: names.add('func3')
		if keys[0] &   8+tCode: names.add('func4')
		names.add('route')
		routingIndex = keys[1] - 1
	if routingIndex is not None:
		log.io("names %s %d" % ('+'.join(names), routingIndex))
	else:
		log.io("names %s" % '+'.join(names))
	if len(names):
		inputCore.manager.executeGesture(InputGesture(names, routingIndex))
		return True
	return False
