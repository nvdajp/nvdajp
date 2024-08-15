# coding: UTF-8
#brailleDisplayDrivers/kgsbn46.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011-2012 Masataka Shinke
#Copyright (C) 2013 Masamitsu Misono
#Copyright (C) 2011-2019 Takuya Nishimoto

import braille
import inputCore
import time
import tones
import os
from collections import OrderedDict
from ctypes import *  # noqa: F403
from ctypes.wintypes import *  # noqa: F403
from logHandler import log
import sys
if sys.version_info.major >= 3:
	xrange = range
	byte = lambda x: x.to_bytes(1, 'big')  # noqa: E731
else:
	byte = chr

from .kgs import kgsListComPorts, waitAfterDisconnect, kgs_dir, processEvents, BMDRVS, KGS_DISPMODE, lock, unlock

fConnection = False
numCells = 0
isUnknownEquipment = False

KGS_PSTATUSCALLBACK = WINFUNCTYPE(c_void_p, c_int, c_int)  # noqa: F405

def nvdaKgsStatusChangedProc(nStatus, nDispSize):
	global fConnection, numCells, isUnknownEquipment
	if nStatus == BMDRVS.DISCONNECTED:
		fConnection = False
		tones.beep(1000, 300)
		log.info("disconnect")
	elif nStatus == BMDRVS.CONNECTED:
		numCells = nDispSize
		fConnection = True
		tones.beep(1000, 30)
		log.info("display size:%d" % nDispSize)
	elif nStatus == BMDRVS.DRIVER_CANNOT_OPEN:
		fConnection = False
		log.info("driver cannot open")
	elif nStatus == BMDRVS.INVALID_DRIVER:
		fConnection = False
		log.info("invalid driver")
	elif nStatus == BMDRVS.OPEN_PORT_FAILED:
		#fConnection = False
		log.info("open port failed")
	elif nStatus == BMDRVS.CREATE_THREAD_FAILED:
		fConnection = False
		log.info("create thread failed")
	elif nStatus == BMDRVS.CHECKING_EQUIPMENT:
		log.info("checking equipment")
	elif nStatus == BMDRVS.UNKNOWN_EQUIPMENT:
		log.info("unknown equipment")
		isUnknownEquipment = True
	elif nStatus == BMDRVS.PORT_RELEASED:
		log.info("port released")
	elif nStatus == BMDRVS.MAX:
		log.info("max")
	else:
		log.info("status changed to %d" % nStatus)

KGS_PKEYCALLBACK = WINFUNCTYPE(c_int, POINTER(c_ubyte))  # noqa: F405

def nvdaKgsHandleKeyInfoProc(lpKeys):
	keys = (lpKeys[0], lpKeys[1], lpKeys[2])
	log.io("keyInfo %d %d %d" % keys)
	log.io("keyInfo hex %x %x %x" % keys)
	names = []
	routingIndex = None
	if keys[0] == 0:
		if keys[1] &   1: names.append('lf')  # noqa: E701
		if keys[1] &   2: names.append('bk')  # noqa: E701
		if keys[1] &   4: names.append('sr')  # noqa: E701
		if keys[1] &   8: names.append('sl')  # noqa: E701
		if keys[1] &  16: names.append('func1')  # noqa: E701
		if keys[1] &  32: names.append('func2')  # noqa: E701
		if keys[1] &  64: names.append('func3')  # noqa: E701
		if keys[1] & 128: names.append('func4')  # noqa: E701
	else:
		tCode = 240
		if keys[0] &   1+tCode: names.append('func1')  # noqa: E701
		if keys[0] &   2+tCode: names.append('func2')  # noqa: E701
		if keys[0] &   4+tCode: names.append('func3')  # noqa: E701
		if keys[0] &   8+tCode: names.append('func4')  # noqa: E701
		names.append('route')
		routingIndex = keys[1] - 1
	if routingIndex is not None:
		log.io("names %s %d" % ('+'.join(names), routingIndex))
	else:
		log.io("names %s" % '+'.join(names))
	if len(names):
		try:
			inputCore.manager.executeGesture(InputGesture(names, routingIndex))
		except inputCore.NoInputGestureAction:
			pass
		return True
	return False

def _fixConnection(hBrl, devName, port, keyCallbackInst, statusCallbackInst):
	global fConnection, isUnknownEquipment
	log.info("scanning port %s" % port)
	if port[:3] == 'COM':
		_port = int(port[3:])-1
	else:
		return False, None
	SPEED = 3 # 9600bps
	fConnection = False
	isUnknownEquipment = False
	ret = hBrl.bmStart(devName, _port, SPEED, statusCallbackInst)
	log.info("bmStart(%s) returns %d" % (port, ret))
	if ret:
		for loop in xrange(15):
			if fConnection:
				ret = hBrl.bmStartDisplayMode2(KGS_DISPMODE, keyCallbackInst)
				log.info("bmStartDisplayMode2() returns %d" % ret)
				break
			elif isUnknownEquipment:
				log.info("isUnknownEquipment")
				break
			time.sleep(0.5)
			tones.beep(400+(loop*20), 20)
			processEvents()
	if not fConnection:
		bmDisConnect(hBrl, _port)
		port = None
		tones.beep(200, 100)
	log.info("connection:%d port:%d" % (fConnection, _port))
	return fConnection, port

def _autoConnection(hBrl, devName, port, keyCallbackInst, statusCallbackInst):
	Port = _port = None
	ret = False
	for portInfo in kgsListComPorts(preferSerial=True):
		_port = portInfo["port"]
		hwID = portInfo["hardwareID"]
		frName = portInfo.get("friendlyName")
		btName = portInfo.get("bluetoothName")
		# skip non BMsmart device
		if btName and btName.lower() == 'bm series':
			continue
		log.info(u"set port:{_port} hw:{hwID} fr:{frName} bt:{btName}".format(_port=_port, hwID=hwID, btName=btName, frName=frName))
		ret, Port = _fixConnection(hBrl, devName, _port, keyCallbackInst, statusCallbackInst)
		if ret:
			break
	return ret, Port

def getKbdcName(hBrl):
	if not hBrl.IsKbdcInstalled(b"Active KBDC"):
		log.warning("active kbdc not found")
	#return u"ブレイルノート46C/46D".encode('shift-jis')
	return u'\u30d6\u30ec\u30a4\u30eb\u30ce\u30fc\u30c846C/46D'.encode('shift-jis')

def bmConnect(hBrl, port, keyCallbackInst, statusCallbackInst, execEndConnection=False):
	if execEndConnection:
		bmDisConnect(hBrl, port)
		waitAfterDisconnect()
	devName = getKbdcName(hBrl)
	if port is None or port=="auto":
		ret, pName = _autoConnection(hBrl, devName, port, keyCallbackInst, statusCallbackInst)
	else:
		ret, pName = _fixConnection(hBrl, devName, port, keyCallbackInst, statusCallbackInst)
	return ret, pName

def bmDisConnect(hBrl, port):
	global fConnection, numCells
	ret = hBrl.bmEndDisplayMode()
	log.info("BmEndDisplayMode %s %d" % (port, ret))
	ret = hBrl.bmEnd()
	log.info("BmEnd %s %d" % (port, ret))
	numCells=0
	fConnection = False
	return ret

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "kgsbn46"
	# Translators: braille display driver description
	description = _(u"KGS BrailleNote 46C/46D")
	isThreadSafe = True
	_portName = None
	_directBM = None

	def __init__(self, port="auto"):
		super(BrailleDisplayDriver,self).__init__()
		global fConnection, numCells
		if not lock():
			return
		if port != self._portName and self._portName:
			execEndConnection = True
			log.info("changing connection %s to %s" % (self._portName, port))
		elif fConnection:
			log.info("already connection %s" % port)
			execEndConnection = False
			self.numCells = numCells
			unlock()
			return
		else:
			log.info("first connection %s" % port)
			execEndConnection = False
			self.numCells = 0
		kgs_dll = os.path.join(kgs_dir, 'DirectBM.dll')
		if sys.version_info.major <= 2:
			kgs_dll = kgs_dll.encode('mbcs')
		log.debug(kgs_dll)
		self._directBM = windll.LoadLibrary(kgs_dll)  # noqa: F405
		if not self._directBM:
			unlock()
			raise RuntimeError("No KGS instance found")
		self._keyCallbackInst = KGS_PKEYCALLBACK(nvdaKgsHandleKeyInfoProc)
		self._statusCallbackInst = KGS_PSTATUSCALLBACK(nvdaKgsStatusChangedProc)
		ret,self._portName = bmConnect(self._directBM, port, self._keyCallbackInst, self._statusCallbackInst, execEndConnection)
		if ret:
			self.numCells = numCells
			log.info("connected %s" % port)
		else:
			self.numCells = 0
			log.info("failed %s" % port)
			unlock()
			raise RuntimeError("No KGS display found")
		unlock()

	def terminate(self):
		if not lock():
			return
		super(BrailleDisplayDriver, self).terminate()
		if self._directBM and self._directBM._handle:
			bmDisConnect(self._directBM, self._portName)
			waitAfterDisconnect()
			ret = windll.kernel32.FreeLibrary(self._directBM._handle)  # noqa: F405
			# ret is not zero if success
			log.info("KGS driver terminated %d" % ret)
		self._directBM = None
		self._portName = None
		self._keyCallbackInst = None
		self._statusCallbackInst = None
		unlock()

	@classmethod
	def check(cls):
		return True

	@classmethod
	def getPossiblePorts(cls):
		ports = {}
		for p in kgsListComPorts():
			if 'bluetoothName' in p:
				p['friendlyName'] = u"Bluetooth: %s (%s)" % (p['bluetoothName'], p['port'])
			ports[p["port"]] = p["friendlyName"]
		ar = [cls.AUTOMATIC_PORT]
		for i in xrange(64):
			p = "COM%d" % (i + 1)
			if p in ports:
				fname = ports[p]
				ar.append( (p, fname) )
		return OrderedDict(ar)

	def display(self, data):
		if not data: return  # noqa: E701
		s = b''
		for c in data:
			d = 0
			if c & 0x01: d += 0x80  # noqa: E701
			if c & 0x02: d += 0x40  # noqa: E701
			if c & 0x04: d += 0x20  # noqa: E701
			if c & 0x08: d += 0x08  # noqa: E701
			if c & 0x10: d += 0x04  # noqa: E701
			if c & 0x20: d += 0x02  # noqa: E701
			if c & 0x40: d += 0x10  # noqa: E701
			if c & 0x80: d += 0x01  # noqa: E701
			s += byte(d)
		dataBuf   = create_string_buffer(s, 256)  # noqa: F405
		cursorBuf = create_string_buffer(b'', 256)  # noqa: F405
		try:
			ret = self._directBM.bmDisplayData(dataBuf, cursorBuf, self.numCells)
			log.debug("bmDisplayData %d" % ret)
		except:  # noqa: E722
			log.debug("error bmDisplayData")


	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"showGui": ("br(kgsbn46):func1",),
			"braille_routeTo": ("br(kgsbn46):route","br(kgsbn46):func1+func2+func3+func4+route",),
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
	})


class InputGesture(braille.BrailleDisplayGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, names, routingIndex):
		super(InputGesture, self).__init__()
		self.id = "+".join(names)
		self.routingIndex = routingIndex
