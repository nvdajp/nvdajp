# Diff for: `source\bdDetect.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\bdDetect.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\bdDetect.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\bdDetect.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\bdDetect.py"
index 7da4fc6..50c112e 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\bdDetect.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\bdDetect.py"
@@ -20,18 +20,10 @@
 from enum import StrEnum
 from typing import (
 	Any,
-	Callable,
-	Dict,
-	Generator,
-	Iterable,
-	Iterator,
-	List,
 	NamedTuple,
-	Optional,
-	OrderedDict,
-	Tuple,
-	Type,
 )
+from collections import OrderedDict
+from collections.abc import Callable, Generator, Iterable, Iterator
 import hwPortUtils
 import NVDAState
 import braille
@@ -128,11 +120,11 @@ class DeviceMatch(NamedTuple):
 	"""The identifier of the device."""
 	port: str
 	"""The port that can be used by a driver to communicate with a device."""
-	deviceInfo: Dict[str, str]
+	deviceInfo: dict[str, str]
 	"""All known information about a device."""
 
 
-MatchFuncT = Callable[[DeviceMatch], bool]
+type MatchFuncT = Callable[[DeviceMatch], bool]
 
 
 @dataclass(frozen=True)
@@ -168,8 +160,9 @@ def matches(self, deviceMatch: DeviceMatch) -> bool:
 
 DriverDictT = defaultdict[CommunicationType, set[_UsbDeviceRegistryEntry] | MatchFuncT]
 _driverDevices = OrderedDict[str, DriverDictT]()
+type DriverAndDeviceMatch = tuple[str, DeviceMatch]
 
-scanForDevices = extensionPoints.Chain[Tuple[str, DeviceMatch]]()
+scanForDevices = extensionPoints.Chain[DriverAndDeviceMatch]()
 """
 A Chain that can be iterated to scan for devices.
 Registered handlers should yield a tuple containing a driver name as str and DeviceMatch
@@ -179,25 +172,27 @@ def matches(self, deviceMatch: DeviceMatch) -> bool:
 @param bluetooth: Whether the handler is expected to yield USB devices.
 @type bluetooth: bool
 @param limitToDevices: Drivers to which detection should be limited.
-	C{None} if no driver filtering should occur.
+	``None`` if no driver filtering should occur.
 @type limitToDevices: Optional[List[str]]
 """
 
 
-def _isDebug():
-	return config.conf["debugLog"]["hwIo"]
+def _isDebug() -> bool:
+	return config.conf["debugLog"]["bdDetect"]
 
 
 def getDriversForConnectedUsbDevices(
-	limitToDevices: Optional[List[str]] = None,
-) -> Iterator[Tuple[str, DeviceMatch]]:
+	limitToDevices: list[str] | None = None,
+) -> Iterator[DriverAndDeviceMatch]:
 	"""Get any matching drivers for connected USB devices.
 	Looks for (and yields) custom drivers first, then considers if the device is may be compatible with the
 	Standard HID Braille spec.
-	@param limitToDevices: Drivers to which detection should be limited.
-		C{None} if no driver filtering should occur.
-	@return: Generator of pairs of drivers and device information.
+	:param limitToDevices: Drivers to which detection should be limited.
+		``None`` if no driver filtering should occur.
+	:return: Generator of pairs of drivers and device information.
 	"""
+	if limitToDevices and _isDebug():
+		log.debug("Limiting connected USB device detection to drivers: %r", limitToDevices)
 	usbCustomDeviceMatches = (
 		DeviceMatch(ProtocolType.CUSTOM, port["usbID"], port["devicePath"], port)
 		for port in deviceInfoFetcher.usbDevices
@@ -212,22 +207,24 @@ def getDriversForConnectedUsbDevices(
 	# The corollary is that clients of this method don't have to process all devices (and create all
 	# device matches), if one is found early the iteration can stop.
 	usbHidDeviceMatches, usbHidDeviceMatchesForCustom = itertools.tee(
-		(
 		DeviceMatch(ProtocolType.HID, port["usbID"], port["devicePath"], port)
 		for port in deviceInfoFetcher.hidDevices
 		if port["provider"] == CommunicationType.USB
 	)
-	)
 
-	fallbackDriversAndMatches: list[tuple[str, DeviceMatch]] = []
+	fallbackDriversAndMatches: list[DriverAndDeviceMatch] = []
 	for match in itertools.chain(usbCustomDeviceMatches, usbHidDeviceMatchesForCustom, usbComDeviceMatches):
 		for driver, devs in _driverDevices.items():
 			if limitToDevices and driver not in limitToDevices:
+				if _isDebug():
+					log.debug("Skipping excluded driver %r for USB device match: %r", driver, match)
 				continue
 			usbDefinitions = devs[CommunicationType.USB]
 			for definition in usbDefinitions:
 				if definition.matches(match):
 					if definition.useAsFallback:
+						if _isDebug():
+							log.debug("Using USB device match %r as fallback for driver %r", match, driver)
 						fallbackDriversAndMatches.append((driver, match))
 					else:
 						yield (driver, match)
@@ -271,15 +268,17 @@ def HIDUsagePageMatchFuncFactory(usagePage: int) -> MatchFuncT:
 
 
 def getDriversForPossibleBluetoothDevices(
-	limitToDevices: Optional[List[str]] = None,
-) -> Iterator[Tuple[str, DeviceMatch]]:
+	limitToDevices: list[str] | None = None,
+) -> Iterator[DriverAndDeviceMatch]:
 	"""Get any matching drivers for possible Bluetooth devices.
 	Looks for (and yields) custom drivers first, then considers if the device is may be compatible with the
 	Standard HID Braille spec.
-	@param limitToDevices: Drivers to which detection should be limited.
-		C{None} if no driver filtering should occur.
-	@return: Generator of pairs of drivers and port information.
+	:param limitToDevices: Drivers to which detection should be limited.
+		``None`` if no driver filtering should occur.
+	:return: Generator of pairs of drivers and port information.
 	"""
+	if limitToDevices and _isDebug():
+		log.debug("Limiting possible Bluetooth device detection to drivers: %r", limitToDevices)
 	btSerialMatchesForCustom = (
 		DeviceMatch(ProtocolType.SERIAL, port["bluetoothName"], port["port"], port)
 		for port in deviceInfoFetcher.comPorts
@@ -291,18 +290,22 @@ def getDriversForPossibleBluetoothDevices(
 	# The corollary is that clients of this method don't have to process all devices (and create all
 	# device matches), if one is found early the iteration can stop.
 	btHidDevMatchesForHid, btHidDevMatchesForCustom = itertools.tee(
-		(
 		DeviceMatch(ProtocolType.HID, port["hardwareID"], port["devicePath"], port)
 		for port in deviceInfoFetcher.hidDevices
 		if port["provider"] == CommunicationType.BLUETOOTH
 	)
-	)
 	for match in itertools.chain(btSerialMatchesForCustom, btHidDevMatchesForCustom):
 		for driver, devs in _driverDevices.items():
 			if limitToDevices and driver not in limitToDevices:
 				continue
 			matchFunc = devs[CommunicationType.BLUETOOTH]
 			if not callable(matchFunc):
+				if _isDebug():
+					log.debugWarning(
+						"Skipping non-callable matchFunc %r for Bluetooth device match: %r",
+						matchFunc,
+						match,
+					)
 				continue
 			if matchFunc(match):
 				yield (driver, match)
@@ -318,7 +321,7 @@ def getDriversForPossibleBluetoothDevices(
 			yield (hidName, match)
 
 
-btDevsCacheT = Optional[List[Tuple[str, DeviceMatch]]]
+type btDevsCacheT = list[DriverAndDeviceMatch] | None
 
 
 class _DeviceInfoFetcher(AutoPropertyObject):
@@ -335,6 +338,8 @@ def __init__(self):
 
 	def _get_btDevsCache(self) -> btDevsCacheT:
 		with self._btDevsLock:
+			if _isDebug():
+				log.debug("Fetching Bluetooth device cache")
 			return self._btDevsCache.copy() if self._btDevsCache else None
 
 	def _set_btDevsCache(
@@ -342,6 +347,8 @@ def _set_btDevsCache(
 		cache: btDevsCacheT,
 	):
 		with self._btDevsLock:
+			if _isDebug():
+				log.debug("Setting Bluetooth device cache")
 			self._btDevsCache = cache.copy() if cache else None
 
 	#: Type info for auto property: _get_comPorts
@@ -351,9 +358,9 @@ def _get_comPorts(self) -> list[dict[str, str]]:
 		return list(hwPortUtils.listComPorts(onlyAvailable=True))
 
 	#: Type info for auto property: _get_usbDevices
-	usbDevices: List[Dict]
+	usbDevices: list[dict]
 
-	def _get_usbDevices(self) -> List[Dict]:
+	def _get_usbDevices(self) -> list[dict]:
 		return list(hwPortUtils.listUsbDevices(onlyAvailable=True))
 
 	#: Type info for auto property: _get_usbComPorts
@@ -374,13 +381,13 @@ def _get_usbComPorts(self) -> list[dict[str, str]]:
 		return comPorts
 
 	#: Type info for auto property: _get_hidDevices
-	hidDevices: List[Dict]
+	hidDevices: list[dict]
 
-	def _get_hidDevices(self) -> List[Dict]:
+	def _get_hidDevices(self) -> list[dict]:
 		return list(hwPortUtils.listHidDevices(onlyAvailable=True))
 
 
-deviceInfoFetcher: Optional[_DeviceInfoFetcher] = None
+deviceInfoFetcher: _DeviceInfoFetcher | None = None
 
 
 class _Detector:
@@ -393,72 +400,100 @@ def __init__(self):
 		After construction, a scan should be queued with L{queueBgScan}.
 		"""
 		self._executor = ThreadPoolExecutor(1)
-		self._queuedFuture: Optional[Future] = None
+		self._queuedFuture: Future | None = None
 		messageWindow.pre_handleWindowMessage.register(self.handleWindowMessage)
 		appModuleHandler.post_appSwitch.register(self.pollBluetoothDevices)
 		self._stopEvent = threading.Event()
 		self._detectUsb = True
 		self._detectBluetooth = True
-		self._limitToDevices: Optional[List[str]] = None
+		self._limitToDevices: list[str] | None = None
 
 	def _queueBgScan(
 		self,
 		usb: bool = False,
 		bluetooth: bool = False,
-		limitToDevices: Optional[List[str]] = None,
+		limitToDevices: list[str] | None = None,
+		preferredDevice: DriverAndDeviceMatch | None = None,
 	):
 		"""Queues a scan for devices.
 		If a scan is already in progress, a new scan will be queued after the current scan.
 		To explicitely cancel a scan in progress, use L{rescan}.
-		@param usb: Whether USB devices should be detected for this and subsequent scans.
-		@param bluetooth: Whether Bluetooth devices should be detected for this and subsequent scans.
-		@param limitToDevices: Drivers to which detection should be limited for this and subsequent scans.
-			C{None} if default driver filtering according to config should occur.
+		:param usb: Whether USB devices should be detected for this and subsequent scans.
+		:param bluetooth: Whether Bluetooth devices should be detected for this and subsequent scans.
+		:param limitToDevices: Drivers to which detection should be limited for this and subsequent scans.
+			``None`` if default driver filtering according to config should occur.
+		:param preferredDevice: An optional preferred device to use for detection before scanning.
+			``None`` if no preferred device should be used.
 		"""
+		if _isDebug():
+			log.debug(
+				"Queuing background scan: usb=%r, bluetooth=%r, limitToDevices=%r, preferredDevice=%r",
+				usb,
+				bluetooth,
+				limitToDevices,
+				preferredDevice,
+			)
+
 		self._detectUsb = usb
 		self._detectBluetooth = bluetooth
 		if limitToDevices is None and config.conf["braille"]["auto"]["excludedDisplays"]:
 			limitToDevices = list(getBrailleDisplayDriversEnabledForDetection())
+			if limitToDevices and _isDebug():
+				log.debug(
+					"Limiting device detection to drivers enabled for auto detection: %r",
+					limitToDevices,
+				)
 		self._limitToDevices = limitToDevices
 
 		if self._queuedFuture:
 			# This will cancel a queued scan (i.e. not the currently running scan, if any)
 			# If this future belongs to a scan that is currently running or finished, this does nothing.
+			if _isDebug():
+				log.debug("Cancelling queued future for next background scan")
 			self._queuedFuture.cancel()
-		self._queuedFuture = self._executor.submit(self._bgScan, usb, bluetooth, limitToDevices)
+		self._queuedFuture = self._executor.submit(
+			self._bgScan,
+			usb,
+			bluetooth,
+			limitToDevices,
+			preferredDevice,
+		)
 
 	def _stopBgScan(self):
 		"""Stops the current scan as soon as possible and prevents a queued scan to start."""
+		if _isDebug():
+			log.debug("Stopping background scan")
 		self._stopEvent.set()
 		if self._queuedFuture:
 			# This will cancel a queued scan (i.e. not the currently running scan, if any)
 			# If this future belongs to a scan that is currently running or finished, this does nothing.
+			if _isDebug():
+				log.debug("Cancelling queued future for next background scan")
 			self._queuedFuture.cancel()
 
 	@staticmethod
 	def _bgScanUsb(
 		usb: bool = True,
-		limitToDevices: Optional[List[str]] = None,
+		limitToDevices: list[str] | None = None,
 	):
 		"""Handler for L{scanForDevices} that yields USB devices.
 		See the L{scanForDevices} documentation for information about the parameters.
 		"""
 		if not usb:
 			return
-		for driver, match in getDriversForConnectedUsbDevices(limitToDevices):
-			yield (driver, match)
+		yield from getDriversForConnectedUsbDevices(limitToDevices)
 
 	@staticmethod
 	def _bgScanBluetooth(
 		bluetooth: bool = True,
-		limitToDevices: Optional[List[str]] = None,
+		limitToDevices: list[str] | None = None,
 	):
 		"""Handler for L{scanForDevices} that yields Bluetooth devices and keeps an internal cache of devices.
 		See the L{scanForDevices} documentation for information about the parameters.
 		"""
 		if not bluetooth:
 			return
-		btDevs: Optional[Iterable[Tuple[str, DeviceMatch]]] = deviceInfoFetcher.btDevsCache
+		btDevs: Iterable[DriverAndDeviceMatch] | None = deviceInfoFetcher.btDevsCache
 		if btDevs is None:
 			btDevs = getDriversForPossibleBluetoothDevices(limitToDevices)
 			# Cache Bluetooth devices for next time.
@@ -476,18 +511,42 @@ def _bgScan(
 		self,
 		usb: bool,
 		bluetooth: bool,
-		limitToDevices: Optional[List[str]],
+		limitToDevices: list[str] | None,
+		preferredDevice: DriverAndDeviceMatch | None,
 	):
 		"""Performs the actual background scan.
 		this function should be run on a background thread.
-		@param usb: Whether USB devices should be detected for this particular scan.
-		@param bluetooth: Whether Bluetooth devices should be detected for this particular scan.
-		@param limitToDevices: Drivers to which detection should be limited for this scan.
-			C{None} if no driver filtering should occur.
+		:param usb: Whether USB devices should be detected for this particular scan.
+		:param bluetooth: Whether Bluetooth devices should be detected for this particular scan.
+		:param limitToDevices: Drivers to which detection should be limited for this scan.
+			``None`` if no driver filtering should occur.
+		:param preferredDevice: An optional preferred device to use for detection before scanning.
+			``None`` if no preferred device should be used.
 		"""
+		if _isDebug():
+			log.debug(
+				"Starting background scan: usb=%r, bluetooth=%r, limitToDevices=%r, preferredDevice=%r",
+				usb,
+				bluetooth,
+				limitToDevices,
+				preferredDevice,
+			)
 		# Clear the stop event before a scan is started.
 		# Since a scan can take some time to complete, another thread can set the stop event to cancel it.
 		self._stopEvent.clear()
+		if preferredDevice:
+			if _isDebug():
+				log.debug("Trying preferred device first: %r", preferredDevice)
+			if braille.handler.setDisplayByName(preferredDevice[0], detected=preferredDevice[1]):
+				if _isDebug():
+					log.debug("Switched to preferred device: %r", preferredDevice[0])
+				return
+			elif _isDebug():
+				log.debug("Failed to switch to preferred device, continuing scan: %r", preferredDevice)
+
+		if self._stopEvent.is_set():
+			return
+
 		iterator = scanForDevices.iter(
 			usb=usb,
 			bluetooth=bluetooth,
@@ -496,8 +555,14 @@ def _bgScan(
 		for driver, match in iterator:
 			if self._stopEvent.is_set():
 				return
+			if _isDebug():
+				log.debug("Processing driver %r, match %r", driver, match)
 			if braille.handler.setDisplayByName(driver, detected=match):
+				if _isDebug():
+					log.debug("Switched to driver %r, match %r", driver, match)
 				return
+			elif _isDebug():
+				log.debug("Failed to switch to driver %r, match %r. Continuing", driver, match)
 			if self._stopEvent.is_set():
 				return
 
@@ -505,20 +570,26 @@ def rescan(
 		self,
 		usb: bool = True,
 		bluetooth: bool = True,
-		limitToDevices: Optional[List[str]] = None,
+		limitToDevices: list[str] | None = None,
+		preferredDevice: DriverAndDeviceMatch | None = None,
 	):
 		"""Stop a current scan when in progress, and start scanning from scratch.
-		@param usb: Whether USB devices should be detected for this and subsequent scans.
-		@type usb: bool
-		@param bluetooth: Whether Bluetooth devices should be detected for this and subsequent scans.
-		@type bluetooth: bool
-		@param limitToDevices: Drivers to which detection should be limited for this and subsequent scans.
-			C{None} if default driver filtering according to config should occur.
+		:param usb: Whether USB devices should be detected for this and subsequent scans.
+		:param bluetooth: Whether Bluetooth devices should be detected for this and subsequent scans.
+		:param limitToDevices: Drivers to which detection should be limited for this and subsequent scans.
+			``None`` if default driver filtering according to config should occur.
+		:param preferredDevice: An optional preferred device to use for detection before scanning.
+			``None`` if no preferred device should be used.
 		"""
 		self._stopBgScan()
 		# Clear the cache of bluetooth devices so new devices can be picked up.
 		deviceInfoFetcher.btDevsCache = None
-		self._queueBgScan(usb=usb, bluetooth=bluetooth, limitToDevices=limitToDevices)
+		self._queueBgScan(
+			usb=usb,
+			bluetooth=bluetooth,
+			limitToDevices=limitToDevices,
+			preferredDevice=preferredDevice,
+		)
 
 	def handleWindowMessage(self, msg=None, wParam=None):
 		if msg == winUser.WM_DEVICECHANGE and wParam == DBT_DEVNODES_CHANGED:
@@ -652,7 +723,7 @@ def driverIsEnabledForAutoDetection(driver: str) -> bool:
 
 def getSupportedBrailleDisplayDrivers(
 	onlyEnabled: bool = False,
-) -> Generator[Type["braille.BrailleDisplayDriver"], Any, Any]:
+) -> Generator[type["braille.BrailleDisplayDriver"], Any, Any]:
 	return braille.getDisplayDrivers(
 		lambda d: (
 			d.isThreadSafe
@@ -776,11 +847,9 @@ def addUsbDevices(
 		devs = self._getDriverDict()
 		driverUsb = devs[CommunicationType.USB]
 		driverUsb.update(
-			(
 			_UsbDeviceRegistryEntry(id=id, type=type, useAsFallback=useAsFallback, matchFunc=matchFunc)
 			for id in ids
 		)
-		)
 
 	def addBluetoothDevices(self, matchFunc: MatchFuncT):
 		"""Associate Bluetooth HID or COM ports with the driver on this instance.
@@ -793,7 +862,7 @@ def addBluetoothDevices(self, matchFunc: MatchFuncT):
 
 	def addDeviceScanner(
 		self,
-		scanFunc: Callable[..., Iterable[Tuple[str, DeviceMatch]]],
+		scanFunc: Callable[..., Iterable[DriverAndDeviceMatch]],
 		moveToStart: bool = False,
 	):
 		"""Register a callable to scan devices.
@@ -805,7 +874,7 @@ def addDeviceScanner(
 			@param bluetooth: Whether the handler is expected to yield USB devices.
 			@type bluetooth: bool
 			@param limitToDevices: Drivers to which detection should be limited.
-				C{None} if no driver filtering should occur.
+				``None`` if no driver filtering should occur.
 			@type limitToDevices: Optional[List[str]]
 		@param moveToStart: If C{True}, the registered callable will be moved to the start
 			of the list of registered handlers.

```