# coding: UTF-8
#brailleDisplayDrivers/kgs.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011-2012 Masataka Shinke
#Copyright (C) 2013 Masamitsu Misono
#Copyright (C) 2011-2015 Takuya Nishimoto

import braille
import brailleInput
import inputCore
import hwPortUtils
import time
import tones
import os
from collections import OrderedDict
import ctypes
from ctypes import *
from ctypes.wintypes import *
import config
from logHandler import log
import sys
import _winreg
import itertools

kgs_dir = "brailleDisplayDrivers"
my_dir = unicode(os.path.dirname(__file__), "mbcs")
if 'addons' in my_dir.split(os.sep):
       kgs_dir = my_dir

fConnection = False
numCells = 0
isUnknownEquipment = False

#BM_DISPMODE_FOREGROUND = 0x01
#BM_DISPMODE_BACKGROUND = 0x02
#BM_DISPMODE_KEYHANDLER = 0x04
#BM_DISPMODE_SUSPENDED  = 0x08
KGS_DISPMODE = 0x02|0x04

# void (CALLBACK *pStatusChanged)(int nStatus, int nDispSize)
#@WINFUNCTYPE(c_void_p, c_int, c_int)
KGS_PSTATUSCALLBACK = WINFUNCTYPE(c_void_p, c_int, c_int)

def nvdaKgsStatusChangedProc(nStatus, nDispSize):
	global fConnection, numCells, isUnknownEquipment
	if 0==nStatus: #BMDRVS_DISCONNECTED
		fConnection = False
		tones.beep(1000, 300)
		log.info("disconnect")
	elif 1==nStatus: #BMDRVS_CONNECTED
		numCells = nDispSize
		fConnection = True
		tones.beep(1000, 30)
		log.info("display size:%d" % nDispSize)
	elif 2==nStatus: #BMDRVS_DRIVER_CANNOT_OPEN
		fConnection = False
		log.info("driver cannot open")
	elif 3==nStatus: #BMDRVS_INVALID_DRIVER
		fConnection = False
		log.info("invalid driver")
	elif 4==nStatus: #BMDRVS_OPEN_PORT_FAILED
		#fConnection = False
		log.info("open port failed")
	elif 5==nStatus: #BMDRVS_CREATE_THREAD_FAILED
		fConnection = False
		log.info("create thread failed")
	elif 6==nStatus: #BMDRVS_CHECKING_EQUIPMENT
		log.info("checking equipment")
	elif 7==nStatus: #BMDRVS_UNKNOWN_EQUIPMENT
		log.info("unknown equipment")
		isUnknownEquipment = True
	elif 8==nStatus: #BMDRVS_PORT_RELEASED
		log.info("port released")
	elif 9==nStatus: #BMDRVS_MAX
		log.info("max")
	else:
		log.info("status changed to %d" % nStatus)

# BOOL (CALLBACK *pHandleKeyInfo)(BYTE info[4])
# @WINFUNCTYPE(c_int, POINTER(c_ubyte))
KGS_PKEYCALLBACK = WINFUNCTYPE(c_int, POINTER(c_ubyte))

def nvdaKgsHandleKeyInfoProc(lpKeys):
	keys = (lpKeys[0], lpKeys[1], lpKeys[2], lpKeys[3])
	log.io("keyInfo %d %d %d %d" % keys)
	log.io("keyInfo hex %x %x %x %x" % keys)
	names = set()
	routingIndex = None
	if keys[2] &   1: names.add('func1')
	if keys[2] &   2: names.add('func4')
	if keys[2] &   4: names.add('ctrl')
	if keys[2] &   8: names.add('alt')
	if keys[2] &  16: names.add('select')
	if keys[2] &  32: names.add('read')
	if keys[2] &  64: names.add('func2')
	if keys[2] & 128: names.add('func3')
	if keys[0] == 1:
		if keys[1] &   1: names.add('space')
		if keys[1] &   2: names.add('dot6')
		if keys[1] &   4: names.add('dot5')
		if keys[1] &   8: names.add('dot4')
		if keys[1] &  16: names.add('enter')
		if keys[1] &  32: names.add('dot3')
		if keys[1] &  64: names.add('dot2')
		if keys[1] & 128: names.add('dot1')
	elif keys[0] == 2:
		if keys[1] &   1: names.add('esc')
		if keys[1] &   2: names.add('inf')
		if keys[1] &   4: names.add('bs')
		if keys[1] &   8: names.add('del')
		if keys[1] &  16: names.add('ins')
		if keys[1] &  32: names.add('chng')
		if keys[1] &  64: names.add('ok')
		if keys[1] & 128: names.add('set')
	elif keys[0] == 3:
		if keys[1] & 1: names.add('upArrow')
		if keys[1] & 2: names.add('downArrow')
		if keys[1] & 4: names.add('leftArrow')
		if keys[1] & 8: names.add('rightArrow')
	elif keys[0] == 4:
		names.add('route')
		routingIndex = keys[1] - 1
	elif keys[0] == 6:
		if keys[1] & 1: names.add('bw')
		if keys[1] & 2: names.add('fw')
		if keys[1] & 4: names.add('ls')
		if keys[1] & 8: names.add('rs')
	if routingIndex is not None:
		log.io("names %s %d" % ('+'.join(names), routingIndex))
	else:
		log.io("names %s" % '+'.join(names))
	if len(names):
		inputCore.manager.executeGesture(InputGesture(names, routingIndex))
		return True
	return False

def kgsListComPorts(preferSerial=False):
	ports = []
	btPorts = {}
	usbPorts = {}

	# BM bluetooth ports
	for p in hwPortUtils.listComPorts(onlyAvailable=True):
		if 'bluetoothName' in p and p['bluetoothName'][:2].upper() == u'BM':
			p['friendlyName'] = u"Bluetooth: %s (%s)" % (p['bluetoothName'], p['port'])
			ports.append(p)
			btPorts[ p['port'] ] = True

	# BM-SMART USB
	try:
		rootKey = _winreg.OpenKey(
			_winreg.HKEY_LOCAL_MACHINE,
			r"SYSTEM\CurrentControlSet\Enum\USB\VID_1148&PID_0301"
		)
	except WindowsError as e:
		pass
	else:
		with rootKey:
			for index in itertools.count():
				try:
					keyName = _winreg.EnumKey(rootKey, index)
				except WindowsError:
					break
				try:
					with _winreg.OpenKey(rootKey, os.path.join(keyName, "Device Parameters")) as paramsKey:
						portName = _winreg.QueryValueEx(paramsKey, "PortName")[0]
						ports.append({
							'friendlyName': u'USB: KGS BM-SMART USB Serial (%s)' % portName,
							'hardwareID': ur'USB\VID_1148&PID_0301',
							'port': unicode(portName)
						})
						usbPorts[portName] = True
				except WindowsError:
					continue

	# KGS USB for BM46
	try:
		rootKey = _winreg.OpenKey(
			_winreg.HKEY_LOCAL_MACHINE,
			r"SYSTEM\CurrentControlSet\Enum\USB\VID_1148&PID_0001"
		)
	except WindowsError as e:
		pass
	else:
		with rootKey:
			for index in itertools.count():
				try:
					keyName = _winreg.EnumKey(rootKey, index)
				except WindowsError:
					break
				try:
					with _winreg.OpenKey(rootKey, os.path.join(keyName, "Device Parameters")) as paramsKey:
						portName = _winreg.QueryValueEx(paramsKey, "PortName")[0]
						ports.append({
							'friendlyName': u'USB: KGS USB To Serial Com Port (%s)' % portName,
							'hardwareID': ur'USB\VID_1148&PID_0001',
							'port': unicode(portName)
						})
						usbPorts[portName] = True
				except WindowsError:
					continue

	# serial ports
	for p in hwPortUtils.listComPorts(onlyAvailable=True):
		if 'hardwareID' in p and p['hardwareID'].upper().startswith(u'BTHENUM'):
			if p['hardwareID'].upper().startswith(ur'BTHENUM\{00001101-0000-1000-8000-00805F9B34FB}_LOCALMFG'):
				log.info("skipping %s" % p['hardwareID'])
				continue
			else:
				log.info("appending non-kgs device: %s" % p['hardwareID'])
				p["friendlyName"] = u"Bluetooth: {portName}".format(portName=p["friendlyName"])
				ports.append(p)
		elif p['port'] not in btPorts and p['port'] not in usbPorts:
			p["friendlyName"] = _("Serial: {portName}").format(portName=p["friendlyName"])
			if preferSerial:
				ports.insert(0, p)
			else:
				ports.append(p)

	log.info(unicode(ports))
	return ports

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
		for loop in xrange(30):
			if fConnection:
				ret = hBrl.bmStartDisplayMode2(KGS_DISPMODE, keyCallbackInst)
				log.info("bmStartDisplayMode2() returns %d" % ret)
				break
			elif isUnknownEquipment:
				log.info("isUnknownEquipment")
				break
			time.sleep(0.5)
			tones.beep(400+(loop*20), 20)
			msg=ctypes.wintypes.MSG()
			if ctypes.windll.user32.PeekMessageW(ctypes.byref(msg),None,0,0,1):
				ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
				ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
	if not fConnection:
		bmDisConnect(hBrl, _port)
		port = None
		tones.beep(200, 100)
	log.info("connection:%d port:%d" % (fConnection, _port))
	return fConnection, port

def _autoConnection(hBrl, devName, port, keyCallbackInst, statusCallbackInst):
	Port = _port = None
	ret = False
	for portInfo in kgsListComPorts():
		_port = portInfo["port"]
		hwID = portInfo["hardwareID"]
		frName = portInfo.get("friendlyName")
		btName = portInfo.get("bluetoothName")
		# skip non BMsmart device
		#if btName and btName.lower() == 'bm series':
		#	continue
		log.info(u"set port:{_port} hw:{hwID} fr:{frName} bt:{btName}".format(_port=_port, hwID=hwID, btName=btName, frName=frName))
		ret, Port = _fixConnection(hBrl, devName, _port, keyCallbackInst, statusCallbackInst)
		if ret:
			break
	return ret, Port

def getKbdcName(hBrl):
	if not hBrl.IsKbdcInstalled("Active KBDC"):
		log.warning("active kbdc not found")
	return "Active BM"

def waitAfterDisconnect():
	for loop in xrange(10):
		time.sleep(0.5)
		tones.beep(450-(loop*20), 20)
		msg=ctypes.wintypes.MSG()
		if ctypes.windll.user32.PeekMessageW(ctypes.byref(msg),None,0,0,1):
			ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
			ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))

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
	name = "kgs"
	description = _(u"KGS BrailleMemo series")
	_portName = None
	_directBM = None

	def __init__(self, port="auto"):
		super(BrailleDisplayDriver,self).__init__()
		global fConnection, numCells
		if port != self._portName and self._portName:
			execEndConnection = True
			log.info("changing connection %s to %s" % (self._portName, port))
		elif fConnection:
			log.info("already connection %s" % port)
			execEndConnection = False
			self.numCells = numCells
			return
		else:
			log.info("first connection %s" % port)
			execEndConnection = False
			self.numCells = 0
		kgs_dll = os.path.join(kgs_dir, 'DirectBM.dll')
		self._directBM = windll.LoadLibrary(kgs_dll.encode('mbcs'))
		if not self._directBM:
			raise RuntimeError("No KGS instance found")
		self._keyCallbackInst = KGS_PKEYCALLBACK(nvdaKgsHandleKeyInfoProc)
		self._statusCallbackInst = KGS_PSTATUSCALLBACK(nvdaKgsStatusChangedProc)
		ret,self._portName = bmConnect(self._directBM, port, self._keyCallbackInst, self._statusCallbackInst, execEndConnection)
		if ret:
			#config.conf["braille"][self.name] = {"port" : self._portName}
			self.numCells = numCells
			log.info("connected %s" % port)
		else:
			#config.conf["braille"][self.name] = {"port" : "auto"}
			self.numCells = 0
			log.info("failed %s" % port)
			raise RuntimeError("No KGS display found")

	def terminate(self):
		log.info("KGS driver terminating")
		super(BrailleDisplayDriver, self).terminate()
		if self._directBM and self._directBM._handle:
			bmDisConnect(self._directBM, self._portName)
			waitAfterDisconnect()
			ret = windll.kernel32.FreeLibrary(self._directBM._handle)
			# ret is not zero if success
			log.info("KGS driver terminated %d" % ret)
		self._directBM = None
		self._portName = None
		self._keyCallbackInst = None
		self._statusCallbackInst = None
		log.info("KGS driver terminating done")

	@classmethod
	def check(cls):
		return True

	@classmethod
	def getPossiblePorts(cls):
		ar = [cls.AUTOMATIC_PORT]
		ports = {}
		for p in kgsListComPorts():
			log.info(p)
			ports[p["port"]] = p["friendlyName"]
		log.info(ports)
		for i in xrange(64):
			p = "COM%d" % (i + 1)
			if p in ports:
				fname = ports[p]
				ar.append( (p, fname) )
			#else:
			#	fname = p
			#ar.append( (p, fname) )
		return OrderedDict(ar)

	def display(self, data):
		if not data or len(data) == 0: return
		s = ''
		for c in data:
			d = 0
			if c & 0x01: d += 0x80
			if c & 0x02: d += 0x40
			if c & 0x04: d += 0x20
			if c & 0x08: d += 0x08
			if c & 0x10: d += 0x04
			if c & 0x20: d += 0x02
			if c & 0x40: d += 0x10
			if c & 0x80: d += 0x01
			s += chr(d)
		dataBuf   = create_string_buffer(s, 256)
		cursorBuf = create_string_buffer('', 256)
		try:
			ret = self._directBM.bmDisplayData(dataBuf, cursorBuf, self.numCells)
			log.debug("bmDisplayData %d" % ret)
		except:
			log.debug("error bmDisplayData")


	gestureMap = inputCore.GlobalGestureMap({
		"globalCommands.GlobalCommands": {
			"showGui": ("br(kgs):ins",),
			"kb:escape": ("br(kgs):esc",),
			"kb:windows": ("br(kgs):read",),
			"kb:shift": ("br(kgs):select",),
			"kb:control": ("br(kgs):ctrl",),
			"kb:alt": ("br(kgs):alt",),
			"kb:alt+tab": ("br(kgs):alt+inf",),
			"kb:enter": ("br(kgs):enter","br(kgs):ok","br(kgs):set",),
			"kb:space": ("br(kgs):space",),
			"kb:delete": ("br(kgs):del",),
			"kb:backspace": ("br(kgs):bs",),
			"kb:tab": ("br(kgs):inf",),
			"kb:shift+tab": ("br(kgs):select+inf",),
			"kb:upArrow": ("br(kgs):upArrow",),
			"kb:downArrow": ("br(kgs):downArrow",),
			"kb:leftArrow": ("br(kgs):leftArrow",),
			"kb:rightArrow": ("br(kgs):rightArrow",),
			"kb:shift+upArrow": ("br(kgs):select+upArrow",),
			"kb:shift+downArrow": ("br(kgs):select+downArrow",),
			"kb:shift+leftArrow": ("br(kgs):select+leftArrow",),
			"kb:shift+rightArrow": ("br(kgs):select+rightArrow",),
			"review_previousLine": ("br(kgs):bw",),
			"review_nextLine": ("br(kgs):fw",),
			"review_previousWord": ("br(kgs):ls",),
			"review_nextWord": ("br(kgs):rs",),
			"braille_routeTo": ("br(kgs):route",),
			"braille_scrollBack": ("br(kgs):func1","br(kgs):func3+leftArrow",),
			"braille_scrollForward": ("br(kgs):func4","br(kgs):func3+rightArrow",),
			"braille_previousLine": ("br(kgs):func3+upArrow",),
			"braille_nextLine": ("br(kgs):func3+downArrow",),
			"kb:a": ("br(kgs):dot1",),
			"kb:b": ("br(kgs):dot1+dot2",),
			"kb:c": ("br(kgs):dot1+dot4",),
			"kb:d": ("br(kgs):dot1+dot4+dot5",),
			"kb:e": ("br(kgs):dot1+dot5",),
			"kb:f": ("br(kgs):dot1+dot2+dot4",),
			"kb:g": ("br(kgs):dot1+dot2+dot4+dot5",),
			"kb:h": ("br(kgs):dot1+dot2+dot5",),
			"kb:i": ("br(kgs):dot2+dot4",),
			"kb:j": ("br(kgs):dot2+dot4+dot5",),
			"kb:k": ("br(kgs):dot1+dot3",),
			"kb:l": ("br(kgs):dot1+dot2+dot3",),
			"kb:m": ("br(kgs):dot1+dot3+dot4",),
			"kb:n": ("br(kgs):dot1+dot3+dot4+dot5",),
			"kb:o": ("br(kgs):dot1+dot3+dot5",),
			"kb:p": ("br(kgs):dot1+dot2+dot3+dot4",),
			"kb:q": ("br(kgs):dot1+dot2+dot3+dot4+dot5",),
			"kb:r": ("br(kgs):dot1+dot2+dot3+dot5",),
			"kb:s": ("br(kgs):dot2+dot3+dot4",),
			"kb:t": ("br(kgs):dot2+dot3+dot4+dot5",),
			"kb:u": ("br(kgs):dot1+dot3+dot6",),
			"kb:v": ("br(kgs):dot1+dot2+dot3+dot6",),
			"kb:w": ("br(kgs):dot2+dot4+dot5+dot6",),
			"kb:x": ("br(kgs):dot1+dot3+dot4+dot6",),
			"kb:y": ("br(kgs):dot1+dot3+dot4+dot5+dot6",),
			"kb:z": ("br(kgs):dot1+dot3+dot5+dot6",),
			"kb:control+a": ("br(kgs):ctrl+dot1",),
			"kb:control+b": ("br(kgs):ctrl+dot1+dot2",),
			"kb:control+c": ("br(kgs):ctrl+dot1+dot4",),
			"kb:control+d": ("br(kgs):ctrl+dot1+dot4+dot5",),
			"kb:control+e": ("br(kgs):ctrl+dot1+dot5",),
			"kb:control+f": ("br(kgs):ctrl+dot1+dot2+dot4",),
			"kb:control+g": ("br(kgs):ctrl+dot1+dot2+dot4+dot5",),
			"kb:control+h": ("br(kgs):ctrl+dot1+dot2+dot5",),
			"kb:control+i": ("br(kgs):ctrl+dot2+dot4",),
			"kb:control+j": ("br(kgs):ctrl+dot2+dot4+dot5",),
			"kb:control+k": ("br(kgs):ctrl+dot1+dot3",),
			"kb:control+l": ("br(kgs):ctrl+dot1+dot2+dot3",),
			"kb:control+m": ("br(kgs):ctrl+dot1+dot3+dot4",),
			"kb:control+n": ("br(kgs):ctrl+dot1+dot3+dot4+dot5",),
			"kb:control+o": ("br(kgs):ctrl+dot1+dot3+dot5",),
			"kb:control+p": ("br(kgs):ctrl+dot1+dot2+dot3+dot4",),
			"kb:control+q": ("br(kgs):ctrl+dot1+dot2+dot3+dot4+dot5",),
			"kb:control+r": ("br(kgs):ctrl+dot1+dot2+dot3+dot5",),
			"kb:control+s": ("br(kgs):ctrl+dot2+dot3+dot4",),
			"kb:control+t": ("br(kgs):ctrl+dot2+dot3+dot4+dot5",),
			"kb:control+u": ("br(kgs):ctrl+dot1+dot3+dot6",),
			"kb:control+v": ("br(kgs):ctrl+dot1+dot2+dot3+dot6",),
			"kb:control+w": ("br(kgs):ctrl+dot2+dot4+dot5+dot6",),
			"kb:control+x": ("br(kgs):ctrl+dot1+dot3+dot4+dot6",),
			"kb:control+y": ("br(kgs):ctrl+dot1+dot3+dot4+dot5+dot6",),
			"kb:control+z": ("br(kgs):ctrl+dot1+dot3+dot5+dot6",),
			"kb:alt+a": ("br(kgs):alt+dot1",),
			"kb:alt+b": ("br(kgs):alt+dot1+dot2",),
			"kb:alt+c": ("br(kgs):alt+dot1+dot4",),
			"kb:alt+d": ("br(kgs):alt+dot1+dot4+dot5",),
			"kb:alt+e": ("br(kgs):alt+dot1+dot5",),
			"kb:alt+f": ("br(kgs):alt+dot1+dot2+dot4",),
			"kb:alt+g": ("br(kgs):alt+dot1+dot2+dot4+dot5",),
			"kb:alt+h": ("br(kgs):alt+dot1+dot2+dot5",),
			"kb:alt+i": ("br(kgs):alt+dot2+dot4",),
			"kb:alt+j": ("br(kgs):alt+dot2+dot4+dot5",),
			"kb:alt+k": ("br(kgs):alt+dot1+dot3",),
			"kb:alt+l": ("br(kgs):alt+dot1+dot2+dot3",),
			"kb:alt+m": ("br(kgs):alt+dot1+dot3+dot4",),
			"kb:alt+n": ("br(kgs):alt+dot1+dot3+dot4+dot5",),
			"kb:alt+o": ("br(kgs):alt+dot1+dot3+dot5",),
			"kb:alt+p": ("br(kgs):alt+dot1+dot2+dot3+dot4",),
			"kb:alt+q": ("br(kgs):alt+dot1+dot2+dot3+dot4+dot5",),
			"kb:alt+r": ("br(kgs):alt+dot1+dot2+dot3+dot5",),
			"kb:alt+s": ("br(kgs):alt+dot2+dot3+dot4",),
			"kb:alt+t": ("br(kgs):alt+dot2+dot3+dot4+dot5",),
			"kb:alt+u": ("br(kgs):alt+dot1+dot3+dot6",),
			"kb:alt+v": ("br(kgs):alt+dot1+dot2+dot3+dot6",),
			"kb:alt+w": ("br(kgs):alt+dot2+dot4+dot5+dot6",),
			"kb:alt+x": ("br(kgs):alt+dot1+dot3+dot4+dot6",),
			"kb:alt+y": ("br(kgs):alt+dot1+dot3+dot4+dot5+dot6",),
			"kb:alt+z": ("br(kgs):alt+dot1+dot3+dot5+dot6",),
			"kb:.": ("br(kgs):dot2+dot5+dot6",),
			"kb::": ("br(kgs):dot2+dot5",),
			"kb:;": ("br(kgs):dot2+dot3",),
			"kb:,": ("br(kgs):dot2",),
			"kb:-": ("br(kgs):dot3+dot6",),
			"kb:?": ("br(kgs):dot2+dot3+dot6",),
			"kb:!": ("br(kgs):dot2+dot3+dot5",),
			"kb:'": ("br(kgs):dot3",),
		}
	})


class InputGesture(braille.BrailleDisplayGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, names, routingIndex):
		super(InputGesture, self).__init__()
		self.id = "+".join(names)
		self.routingIndex = routingIndex
