# coding: UTF-8
#brailleDisplayDrivers/kgs.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011-2015 Takuya Nishimoto
#Copyright (C) 2011-2012 Masataka Shinke
#Copyright (C) 2013 Masamitsu Misono

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
import core

kgs_dir = unicode(os.path.dirname(__file__), "mbcs")
if (not 'addons' in os.path.split(kgs_dir)) and hasattr(sys, 'frozen'):
	d = os.path.join(os.getcwdu(), 'brailleDisplayDrivers')
	if os.path.isdir(d):
		kgs_dir = d

class KgsStatus(object):
	def __init__(self):
		self.fConnection = False
		self.numCells = 0
		self.lastReleaseTime = None
		self.portName = None
		self.driverName = None
		self.directBM = None
		self.directBMCount = 0

	def freeDirectBM(self):
		if self.directBM is None:
			return -1
		ret = windll.kernel32.FreeLibrary(self.directBM._handle)
		self.directBM = None
		return ret


kgsStatus = KgsStatus()

#BM_DISPMODE_FOREGROUND = 0x01
#BM_DISPMODE_BACKGROUND = 0x02
#BM_DISPMODE_KEYHANDLER = 0x04
#BM_DISPMODE_SUSPENDED  = 0x08
KGS_DISPMODE = 0x02|0x04

# void (CALLBACK *pStatusChanged)(int nStatus, int nDispSize)
#@WINFUNCTYPE(c_void_p, c_int, c_int)
KGS_PSTATUSCALLBACK = WINFUNCTYPE(c_void_p, c_int, c_int)

def nvdaKgsStatusChangedProc(nStatus, nDispSize):
	if 0==nStatus: #BMDRVS_DISCONNECTED
		kgsStatus.fConnection = False
		tones.beep(1000, 300)
		log.info("disconnect")
	elif 1==nStatus: #BMDRVS_CONNECTED
		kgsStatus.numCells = nDispSize
		kgsStatus.fConnection = True
		tones.beep(1000, 30)
		log.info("display size:%d" % nDispSize)
	elif 2==nStatus: #BMDRVS_DRIVER_CANNOT_OPEN
		kgsStatus.fConnection = False
		log.info("driver cannot open")
	elif 3==nStatus: #BMDRVS_INVALID_DRIVER
		kgsStatus.fConnection = False
		log.info("invalid driver")
	elif 4==nStatus: #BMDRVS_OPEN_PORT_FAILED
		#kgsStatus.fConnection = False
		log.info("open port failed")
	elif 5==nStatus: #BMDRVS_CREATE_THREAD_FAILED
		kgsStatus.fConnection = False
		log.info("create thread failed")
	elif 6==nStatus: #BMDRVS_CHECKING_EQUIPMENT
		log.info("checking equipment")
	elif 7==nStatus: #BMDRVS_UNKNOWN_EQUIPMENT
		log.info("unknown equipment")
	elif 8==nStatus: #BMDRVS_PORT_RELEASED
		log.info("port released")
	elif 9==nStatus: #BMDRVS_MAX
		log.info("max")
	else:
		log.info("status changed to %d" % nStatus)

def kgsHandleKeyInfo(lpKeys):
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
	return names, routingIndex

# BOOL (CALLBACK *pHandleKeyInfo)(BYTE info[4])
# @WINFUNCTYPE(c_int, POINTER(c_ubyte))
KGS_PKEYCALLBACK = WINFUNCTYPE(c_int, POINTER(c_ubyte))

def nvdaKgsHandleKeyInfoProc(lpKeys):
	names, routingIndex = kgsHandleKeyInfo(lpKeys)
	if len(names):
		inputCore.manager.executeGesture(InputGesture(names, routingIndex))
		return True
	return False

def _listComPorts(allowSerial=True):
	ports = []

	# BT ports and serial ports (if allowed)
	# use bluetooth name if KGS devices are found
	for p in hwPortUtils.listComPorts():
		if 'bluetoothName' in p and p['bluetoothName'][:2] == u'BM':
			p['friendlyName'] = u"%s %s" % (p['port'], p['bluetoothName'])
			ports.append(p)
		elif allowSerial:
			if (' (' + p['port'] + ')') in p['friendlyName']:
				p['friendlyName'] = p['port'] + ' ' + p['friendlyName'].replace((' (' + p['port'] + ')'), '')
			ports.append(p)

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
							'friendlyName': u'%s KGS BM-SMART USB Serial' % portName,
							'hardwareID': ur'USB\VID_1148&PID_0301',
							'port': unicode(portName)
						})
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
							'friendlyName': u'%s KGS USB To Serial Com Port' % portName,
							'hardwareID': ur'USB\VID_1148&PID_0001',
							'port': unicode(portName)
						})
				except WindowsError:
					continue
	log.debug(unicode(ports))
	return ports

def _fixConnection(hBrl, devName, port, keyCallbackInst, statusCallbackInst):
	log.info("scanning port %s" % port)
	if port[:3] == 'COM':
		_port = int(port[3:])-1
	else:
		return False, None
	SPEED = 3 # 9600bps
	kgsStatus.fConnection = False
	if kgsStatus.lastReleaseTime is not None and time.time() - kgsStatus.lastReleaseTime < 5.0:
		for loop in xrange(10):
			time.sleep(0.5)
			tones.beep(450-(loop*20), 20)
			core.requestPump()
	ret = hBrl.bmStart(devName, _port, SPEED, statusCallbackInst)
	log.info("bmStart %s returned %d" % (port, ret))
	if ret != 1:
		tones.beep(200, 100)
		return False, None
	for loop in xrange(30):
		try:
			if kgsStatus.fConnection:
				kgsStatus.portName = port
				ret = hBrl.bmStartDisplayMode2(KGS_DISPMODE, keyCallbackInst)
				log.info("bmStartDisplayMode2 %s returned %d" % (port, ret))
				break
			time.sleep(0.5)
			tones.beep(400+(loop*20), 20)
			core.requestPump()
		except:
			raise
	if kgsStatus.fConnection:
		log.info("connection %s done" % port)
	else:
		log.warning("connection %s failed" % port)
		bmDisConnect(hBrl, _port)
		port = None
		tones.beep(200, 100)
	return kgsStatus.fConnection, port

def _autoConnection(hBrl, devName, port, allowSerial, keyCallbackInst, statusCallbackInst):
	Port = _port = None
	ret = False
	for portInfo in _listComPorts(allowSerial=allowSerial):
		_port = portInfo["port"]
		hwID = portInfo["hardwareID"]
		frName = portInfo.get("friendlyName")
		btName = portInfo.get("bluetoothName")
		log.info(u"set port:{_port} hw:{hwID} fr:{frName} bt:{btName}".format(_port=_port, hwID=hwID, btName=btName, frName=frName))
		#if hwID[:3] != 'USB':
		#	continue
		ret, Port = _fixConnection(hBrl, devName, _port, keyCallbackInst, statusCallbackInst)
		if ret:
			break
	return ret, Port

def bmConnect(hBrl, port, devName, allowSerial, keyCallbackInst, statusCallbackInst, execEndConnection=False):
	if execEndConnection:
		if kgsStatus.portName:
			bmDisConnect(hBrl, kgsStatus.portName)
		else:
			bmDisConnect(hBrl, port)
	if port is None or port=="auto":
		ret, pName = _autoConnection(hBrl, devName, port, allowSerial, keyCallbackInst, statusCallbackInst)
	else:
		ret, pName = _fixConnection(hBrl, devName, port, keyCallbackInst, statusCallbackInst)
	return ret, pName

def bmDisConnect(hBrl, port):
	ret = hBrl.bmEndDisplayMode()
	log.info("BmEndDisplayMode %s %d" % (port, ret))
	for loop in xrange(10):
		time.sleep(0.1)
		core.requestPump()
	ret = hBrl.bmEnd()
	log.info("BmEnd %s %d" % (port, ret))
	for loop in xrange(10):
		time.sleep(0.1)
		core.requestPump()
	kgsStatus.numCells = 0
	kgsStatus.fConnection = False
	kgsStatus.lastReleaseTime = time.time()
	kgsStatus.portName = None
	return ret

kgsGestureMapData = {
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
}

class BrailleDisplayDriver(braille.BrailleDisplayDriver):
	name = "kgs"
	description = _(u"KGS BrailleMemo series")
	devName = u"BMシリーズ機器".encode('shift-jis')
	allowAutomatic = True
	allowSerial = False
	allowUnavailablePorts = False

	@classmethod
	def getKeyCallback(cls):
		return nvdaKgsHandleKeyInfoProc

	def __init__(self, port="auto"):
		super(BrailleDisplayDriver,self).__init__()
		if port != kgsStatus.portName and kgsStatus.portName:
			execEndConnection = True
			log.info("changing from %s:%s to %s:%s" % (kgsStatus.driverName, kgsStatus.portName, self.name, port))
		elif kgsStatus.fConnection:
			log.info("already connection %s" % port)
			kgsStatus.driverName = self.name
			self.numCells = kgsStatus.numCells
			return
		else:
			log.info("first connection %s" % port)
			execEndConnection = False
			self.numCells = 0
		if kgsStatus.directBM:
			self._directBM = kgsStatus.directBM
			kgsStatus.directBMCount += 1
			log.info("directBMCount %d" % kgsStatus.directBMCount)
		else:
			kgs_dll = os.path.join(kgs_dir, 'DirectBM.dll')
			self._directBM = windll.LoadLibrary(kgs_dll.encode('mbcs'))
			if not self._directBM:
				raise RuntimeError("loading DirectBM")
			kgsStatus.directBM = self._directBM
			kgsStatus.directBMCount += 1
			log.info("directBMCount %d %s" % (kgsStatus.directBMCount, str(self._directBM)))
		self._keyCallbackInst = KGS_PKEYCALLBACK(self.getKeyCallback())
		self._statusCallbackInst = KGS_PSTATUSCALLBACK(nvdaKgsStatusChangedProc)
		ret,self._portName = bmConnect(self._directBM, port, self.devName, self.allowSerial, self._keyCallbackInst, self._statusCallbackInst, execEndConnection)
		if ret:
			#config.conf["braille"][self.name] = {"port" : self._portName}
			self.numCells = kgsStatus.numCells
			kgsStatus.driverName = self.name
			log.info("connected %s:%s" % (self.name, port))
		else:
			#config.conf["braille"][self.name] = {"port" : "auto"}
			self.numCells = 0
			kgsStatus.directBMCount -= 1
			log.info("directBMCount %d" % kgsStatus.directBMCount)
			if kgsStatus.directBMCount <= 0:
				ret = kgsStatus.freeDirectBM()
				# ret is not zero if success
				log.info("%s FreeLibrary done %d" % (self.name, ret))
				kgsStatus.directBMCount = 0
				log.info("directBMCount %d" % kgsStatus.directBMCount)
			raise RuntimeError("%s:%s" % (self.name, port))
		self.gestureMap = inputCore.GlobalGestureMap(kgsGestureMapData)

	def terminate(self):
		log.info("%s terminating" % self.name)
		super(BrailleDisplayDriver, self).terminate()
		if hasattr(self, "_directBM") and self._directBM:
			bmDisConnect(self._directBM, self._portName)
			log.info("bmDisConnect done")
		kgsStatus.directBMCount -= 1
		log.info("directBMCount %d" % kgsStatus.directBMCount)
		if kgsStatus.directBMCount <= 0:
			ret = kgsStatus.freeDirectBM()
			# ret is not zero if success
			log.info("%s FreeLibrary done %d" % (self.name, ret))
			kgsStatus.directBMCount = 0
			log.info("directBMCount %d" % kgsStatus.directBMCount)
		self._directBM = None
		self._portName = None
		self._keyCallbackInst = None
		self._statusCallbackInst = None
		log.info("%s terminating done" % self.name)

	@classmethod
	def check(cls):
		return True

	@classmethod
	def getPossiblePorts(cls):
		ar = []
		if cls.allowAutomatic:
			ar.append(cls.AUTOMATIC_PORT)
		ports = {}
		for p in _listComPorts(allowSerial=cls.allowSerial):
			log.debug(p)
			ports[p["port"]] = p["friendlyName"]
		log.debug(ports)
		for i in xrange(64):
			p = "COM%d" % (i + 1)
			if p in ports:
				fname = ports[p]
				ar.append( (p, fname) )
			elif cls.allowUnavailablePorts:
				fname = p
				ar.append( (p, fname) )
		return OrderedDict(ar)

	def display(self, data):
		if not data: return
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


class InputGesture(braille.BrailleDisplayGesture):

	source = BrailleDisplayDriver.name

	def __init__(self, names, routingIndex):
		super(InputGesture, self).__init__()
		self.id = "+".join(names)
		self.routingIndex = routingIndex
