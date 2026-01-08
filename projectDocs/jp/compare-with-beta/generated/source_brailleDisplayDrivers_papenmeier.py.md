# Diff for: `source\brailleDisplayDrivers\papenmeier.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\brailleDisplayDrivers\papenmeier.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\brailleDisplayDrivers\papenmeier.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\brailleDisplayDrivers\\papenmeier.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleDisplayDrivers\\papenmeier.py"
index 2bd13ac..e17e762 100644
--- "a/F:\\nvda\\gh\\beta\\source\\brailleDisplayDrivers\\papenmeier.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleDisplayDrivers\\papenmeier.py"
@@ -20,7 +20,6 @@
 try:
 	import ftdi2
 except:  # noqa: E722
-	log.debug("Failed to import ftdi2.", exc_info=True)
 	ftdi2 = None
 # for bluetooth
 import hwPortUtils
@@ -167,18 +166,18 @@ def connectBluetooth(self):
 							)
 							log.info("connectBluetooth success")
 						except:  # noqa: E722
-							log.debugWarning("connectBluetooth failed", exc_info=True)
+							log.debugWarning("connectBluetooth failed")
 
 	def connectUSB(self, devlist: List[bytes]):
 		"""Try to connect to usb device, this is triggered when bluetooth
 		connection could not be established"""
 		try:
-			self._dev = ftdi2.openEx(devlist[0])
+			self._dev = ftdi2.open_ex(devlist[0])
 			self._dev.set_baud_rate(self._baud)
-			self._dev.inWaiting = self._dev.getQueueStatus
+			self._dev.inWaiting = self._dev.get_queue_status
 			log.info("connectUSB success")
 		except:  # noqa: E722
-			log.debugWarning("connectUSB failed", exc_info=True)
+			log.debugWarning("connectUSB failed")
 
 	def __init__(self):
 		"""initialize driver"""
@@ -195,7 +194,7 @@ def __init__(self):
 		# try to connect to usb device,
 		# if no usb device is found there may be a bluetooth device
 		if ftdi2:
-			devlist = ftdi2.listDevices()
+			devlist = ftdi2.list_devices()
 		if len(devlist) == 0:
 			self.connectBluetooth()
 		elif ftdi2:
@@ -308,7 +307,7 @@ def __init__(self):
 						log.debugWarning("UNKNOWN BRAILLE")
 
 			except:  # noqa: E722
-				log.debugWarning("BROKEN PIPE - THIS SHOULD NEVER HAPPEN", exc_info=True)
+				log.debugWarning("BROKEN PIPE - THIS SHOULD NEVER HAPPEN")
 		if self.numCells == 0:
 			raise Exception("no device found")
 
@@ -401,7 +400,6 @@ def terminate(self):
 				self._dev.close()
 			self._dev = None
 		except:  # noqa: E722
-			log.debug("Failed to terminate braille display.", exc_info=True)
 			self._dev = None
 
 	def display(self, cells: List[int]):
@@ -411,7 +409,6 @@ def display(self, cells: List[int]):
 		try:
 			self._dev.write(brl_out(cells, self._nlk, self._nrk, self._voffset))
 		except:  # noqa: E722
-			log.debug("Failed to write to braille display.", exc_info=True)
 			self._dev.close()
 			self._dev = None
 
@@ -425,11 +422,10 @@ def _handleKeyPresses(self):
 		try:
 			if self._dev is None and self._baud > 0:
 				try:
-					devlist: List[bytes] = ftdi2.listDevices()
+					devlist: List[bytes] = ftdi2.list_devices()
 					if len(devlist) > 0:
 						self.connectUSB(devlist)
 				except:  # noqa: E722
-					log.debug("Failed to connect to device.", exc_info=True)
 					return
 			s: bytes = brl_poll(self._dev)
 			if s:
@@ -441,7 +437,6 @@ def _handleKeyPresses(self):
 					ig = InputGesture(None, self)
 					self.executeGesture(ig)
 		except:  # noqa: E722
-			log.debug("Failed to read keys.", exc_info=True)
 			if self._dev != None:  # noqa: E711
 				self._dev.close()
 			self._dev = None

```