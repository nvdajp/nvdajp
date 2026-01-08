# Diff for: `source\hwPortUtils.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\hwPortUtils.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\hwPortUtils.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\hwPortUtils.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\hwPortUtils.py"
index 7a04040..83a84f2 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\hwPortUtils.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\hwPortUtils.py"
@@ -9,152 +9,57 @@
 import math
 import typing
 import winreg
-from ctypes.wintypes import BOOL, DWORD, HWND, PDWORD, ULONG, USHORT, WCHAR
-
-from comtypes import GUID
+from ctypes.wintypes import DWORD, WCHAR
 
 import config
 import hidpi
+import utils._deprecate
 import winKernel
+from comtypes import GUID
 from logHandler import log
 from winAPI.constants import SystemErrorCodes
-from winKernel import SYSTEMTIME
-
-
-def ValidHandle(value):
-	if value == 0:
-		raise ctypes.WinError()
-	return value
-
-
-HDEVINFO = ctypes.c_void_p
-
-
-class SP_DEVINFO_DATA(ctypes.Structure):
-	_fields_ = (
-		("cbSize", DWORD),
-		("ClassGuid", GUID),
-		("DevInst", DWORD),
-		("Reserved", ctypes.POINTER(ULONG)),
+from winBindings.advapi32 import RegCloseKey as _RegCloseKey
+from winBindings.bthprops import (
+	BLUETOOTH_DEVICE_INFO as _BLUETOOTH_DEVICE_INFO,
+	BluetoothGetDeviceInfo as _BluetoothGetDeviceInfo,
 )
-
-	def __str__(self):
-		return f"ClassGuid:{self.ClassGuid} DevInst:{self.DevInst}"
-
-
-PSP_DEVINFO_DATA = ctypes.POINTER(SP_DEVINFO_DATA)
-
-
-class SP_DEVICE_INTERFACE_DATA(ctypes.Structure):
-	_fields_ = (
-		("cbSize", DWORD),
-		("InterfaceClassGuid", GUID),
-		("Flags", DWORD),
-		("Reserved", ctypes.POINTER(ULONG)),
+from winBindings.hid import (
+	HIDD_ATTRIBUTES as _HIDD_ATTRIBUTES,
+	HidD_FreePreparsedData as _HidD_FreePreparsedData,
+	HidD_GetAttributes as _HidD_GetAttributes,
+	HidD_GetHidGuid as _HidD_GetHidGuid,
+	HidD_GetManufacturerString as _HidD_GetManufacturerString,
+	HidD_GetPreparsedData as _HidD_GetPreparsedData,
+	HidD_GetProductString as _HidD_GetProductString,
+	HidP_GetCaps as _HidP_GetCaps,
 )
-
-	def __str__(self):
-		return f"InterfaceClassGuid:{self.InterfaceClassGuid} Flags:{self.Flags}"
-
-
-PSP_DEVICE_INTERFACE_DATA = ctypes.POINTER(SP_DEVICE_INTERFACE_DATA)
-
-PSP_DEVICE_INTERFACE_DETAIL_DATA = ctypes.c_void_p
-
-
-class DEVPROPKEY(ctypes.Structure):
-	_fields_ = (
-		("DEVPROPGUID", GUID),
-		("DEVPROPID", ULONG),
+from winBindings.setupapi import (
+	DICS_FLAG,
+	DIGCF,
+	DIREG,
+	GUID_CLASS_COMPORT as _GUID_CLASS_COMPORT,
+	GUID_DEVINTERFACE_USB_DEVICE as _GUID_DEVINTERFACE_USB_DEVICE,
+	HDEVINFO as _HDEVINFO,
+	SIZEOF_SP_DEVICE_INTERFACE_DETAIL_DATA_W as _SIZEOF_SP_DEVICE_INTERFACE_DETAIL_DATA_W,
+	SP_DEVICE_INTERFACE_DATA as _SP_DEVICE_INTERFACE_DATA,
+	SP_DEVINFO_DATA as _SP_DEVINFO_DATA,
+	SPDRP,
+	DEVPKEY_Device_BusReportedDeviceDesc as _DEVPKEY_Device_BusReportedDeviceDesc,
+	SetupDiDestroyDeviceInfoList as _SetupDiDestroyDeviceInfoList,
+	SetupDiEnumDeviceInterfaces as _SetupDiEnumDeviceInterfaces,
+	SetupDiGetClassDevs as _SetupDiGetClassDevs,
+	SetupDiGetDeviceInterfaceDetail as _SetupDiGetDeviceInterfaceDetail,
+	SetupDiGetDeviceProperty as _SetupDiGetDeviceProperty,
+	SetupDiGetDeviceRegistryProperty as _SetupDiGetDeviceRegistryProperty,
+	SetupDiOpenDevRegKey as _SetupDiOpenDevRegKey,
+	_Dummy,
 )
 
 
-class dummy(ctypes.Structure):
-	_fields_ = (("d1", DWORD), ("d2", WCHAR))
-	# SetupAPI.h in the Windows headers includes pshpack8.h when 64 bit, pshpack1.h otherwise
-	_pack_ = 8 if ctypes.sizeof(ctypes.c_void_p) == 8 else 1
-
-
-SIZEOF_SP_DEVICE_INTERFACE_DETAIL_DATA_W = ctypes.sizeof(dummy)
-
-SetupDiDestroyDeviceInfoList = ctypes.windll.setupapi.SetupDiDestroyDeviceInfoList
-SetupDiDestroyDeviceInfoList.argtypes = (HDEVINFO,)
-SetupDiDestroyDeviceInfoList.restype = BOOL
-
-SetupDiGetClassDevs = ctypes.windll.setupapi.SetupDiGetClassDevsW
-SetupDiGetClassDevs.argtypes = (ctypes.POINTER(GUID), ctypes.c_wchar_p, HWND, DWORD)
-SetupDiGetClassDevs.restype = ValidHandle  # HDEVINFO
-
-SetupDiGetDeviceProperty = ctypes.windll.setupapi.SetupDiGetDevicePropertyW
-SetupDiGetDeviceProperty.argtypes = (
-	HDEVINFO,  # [in]            HDEVINFO         DeviceInfoSet
-	PSP_DEVINFO_DATA,  # [in]            PSP_DEVINFO_DATA DeviceInfoData
-	ctypes.POINTER(DEVPROPKEY),  # [in]            const DEVPROPKEY *PropertyKey
-	PDWORD,  # [out]           DEVPROPTYPE      *PropertyType
-	ctypes.c_void_p,  # [out, optional] PBYTE            PropertyBuffer
-	DWORD,  # [in]            DWORD            PropertyBufferSize
-	PDWORD,  # [out, optional] PDWORD           RequiredSize
-	DWORD,  # [in]            DWORD            Flags
-)
-SetupDiGetDeviceProperty.restype = BOOL
-
-SetupDiEnumDeviceInterfaces = ctypes.windll.setupapi.SetupDiEnumDeviceInterfaces
-SetupDiEnumDeviceInterfaces.argtypes = (
-	HDEVINFO,
-	PSP_DEVINFO_DATA,
-	ctypes.POINTER(GUID),
-	DWORD,
-	PSP_DEVICE_INTERFACE_DATA,
-)
-SetupDiEnumDeviceInterfaces.restype = BOOL
-
-SetupDiGetDeviceInterfaceDetail = ctypes.windll.setupapi.SetupDiGetDeviceInterfaceDetailW
-SetupDiGetDeviceInterfaceDetail.argtypes = (
-	HDEVINFO,
-	PSP_DEVICE_INTERFACE_DATA,
-	PSP_DEVICE_INTERFACE_DETAIL_DATA,
-	DWORD,
-	PDWORD,
-	PSP_DEVINFO_DATA,
-)
-SetupDiGetDeviceInterfaceDetail.restype = BOOL
-
-SetupDiGetDeviceRegistryProperty = ctypes.windll.setupapi.SetupDiGetDeviceRegistryPropertyW
-SetupDiGetDeviceRegistryProperty.argtypes = (
-	HDEVINFO,
-	PSP_DEVINFO_DATA,
-	DWORD,
-	PDWORD,
-	ctypes.c_void_p,
-	DWORD,
-	PDWORD,
-)
-SetupDiGetDeviceRegistryProperty.restype = BOOL
-
-SetupDiEnumDeviceInfo = ctypes.windll.setupapi.SetupDiEnumDeviceInfo
-SetupDiEnumDeviceInfo.argtypes = (HDEVINFO, DWORD, PSP_DEVINFO_DATA)
-SetupDiEnumDeviceInfo.restype = BOOL
-
-CM_Get_Device_ID = ctypes.windll.cfgmgr32.CM_Get_Device_IDW
-CM_Get_Device_ID.argtypes = (DWORD, ctypes.c_wchar_p, ULONG, ULONG)
-CM_Get_Device_ID.restype = DWORD
-CR_SUCCESS = 0
-MAX_DEVICE_ID_LEN = 200
-
-GUID_CLASS_COMPORT = GUID("{86e0d1e0-8089-11d0-9ce4-08003e301f73}")
-GUID_DEVINTERFACE_USB_DEVICE = GUID("{a5dcbf10-6530-11d2-901f-00c04fb951ed}")
-DEVPKEY_Device_BusReportedDeviceDesc = DEVPROPKEY(GUID("{540b947e-8b40-45bc-a8a2-6a0b894cbda2}"), 4)
-DIGCF_PRESENT = 2
-DIGCF_DEVICEINTERFACE = 16
-INVALID_HANDLE_VALUE = 0
-ERROR_INSUFFICIENT_BUFFER = 122
-SPDRP_DEVICEDESC = 0
-SPDRP_HARDWAREID = 1
-SPDRP_FRIENDLYNAME = 12
-SPDRP_LOCATION_INFORMATION = 13
-ERROR_NO_MORE_ITEMS = 259
-DICS_FLAG_GLOBAL = 0x00000001
-DIREG_DEV = 0x00000001
+def _ValidHandle(value):
+	if value == 0:
+		raise ctypes.WinError()
+	return value
 
 
 def _isDebug():
@@ -219,31 +124,31 @@ def listComPorts(onlyAvailable: bool = True) -> typing.Iterator[dict]:
 	:param onlyAvailable: Only return ports that are currently available.
 	:return: Dicts including keys of port, friendlyName and hardwareID.
 	"""
-	for g_hdi, _idd, devinfo, buf in _listDevices(GUID_CLASS_COMPORT, onlyAvailable):
+	for g_hdi, _idd, devinfo, buf in _listDevices(_GUID_CLASS_COMPORT, onlyAvailable):
 		entry = {}
 		# hardware ID
-		if not SetupDiGetDeviceRegistryProperty(
+		if not _SetupDiGetDeviceRegistryProperty(
 			g_hdi,
 			ctypes.byref(devinfo),
-			SPDRP_HARDWAREID,
+			SPDRP.HARDWAREID,
 			None,
 			ctypes.byref(buf),
 			ctypes.sizeof(buf) - 1,
 			None,
 		):
 			# Ignore ERROR_INSUFFICIENT_BUFFER
-			if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
+			if ctypes.GetLastError() != SystemErrorCodes.INSUFFICIENT_BUFFER:
 				raise ctypes.WinError()
 		else:
 			hwID = entry["hardwareID"] = buf.value
 
 		# Port info
-		regKey = ctypes.windll.setupapi.SetupDiOpenDevRegKey(
+		regKey = _SetupDiOpenDevRegKey(
 			g_hdi,
 			ctypes.byref(devinfo),
-			DICS_FLAG_GLOBAL,
+			DICS_FLAG.GLOBAL,
 			0,
-			DIREG_DEV,
+			DIREG.DEV,
 			winreg.KEY_READ,
 		)
 		try:
@@ -254,13 +159,13 @@ def listComPorts(onlyAvailable: bool = True) -> typing.Iterator[dict]:
 				port = portInfo["port"]
 				entry.update(portInfo)
 		finally:
-			ctypes.windll.advapi32.RegCloseKey(regKey)
+			_RegCloseKey(regKey)
 
 		# friendly name
-		if not SetupDiGetDeviceRegistryProperty(
+		if not _SetupDiGetDeviceRegistryProperty(
 			g_hdi,
 			ctypes.byref(devinfo),
-			SPDRP_FRIENDLYNAME,
+			SPDRP.FRIENDLYNAME,
 			None,
 			ctypes.byref(buf),
 			ctypes.sizeof(buf) - 1,
@@ -280,30 +185,9 @@ def listComPorts(onlyAvailable: bool = True) -> typing.Iterator[dict]:
 		log.debug("Finished listing com ports")
 
 
-BLUETOOTH_MAX_NAME_SIZE = 248
-BTH_ADDR = BLUETOOTH_ADDRESS = ctypes.c_ulonglong
-
-
-class BLUETOOTH_DEVICE_INFO(ctypes.Structure):
-	_fields_ = (
-		("dwSize", DWORD),
-		("address", BLUETOOTH_ADDRESS),
-		("ulClassofDevice", ULONG),
-		("fConnected", BOOL),
-		("fRemembered", BOOL),
-		("fAuthenticated", BOOL),
-		("stLastSeen", SYSTEMTIME),
-		("stLastUsed", SYSTEMTIME),
-		("szName", WCHAR * BLUETOOTH_MAX_NAME_SIZE),
-	)
-
-	def __init__(self, **kwargs):
-		super().__init__(dwSize=ctypes.sizeof(self), **kwargs)
-
-
 def getBluetoothDeviceInfo(address):
-	devInfo = BLUETOOTH_DEVICE_INFO(address=address)
-	res = ctypes.windll["bthprops.cpl"].BluetoothGetDeviceInfo(None, ctypes.byref(devInfo))
+	devInfo = _BLUETOOTH_DEVICE_INFO(address=address)
+	res = _BluetoothGetDeviceInfo(None, ctypes.byref(devInfo))
 	if res != 0:
 		raise ctypes.WinError(res)
 	return devInfo
@@ -362,36 +246,36 @@ def getWidcommBluetoothPortInfo(port):
 def _listDevices(
 	deviceClass: GUID,
 	onlyAvailable: bool = True,
-) -> typing.Iterator[tuple[HDEVINFO, ctypes.Structure, SP_DEVINFO_DATA, ctypes.c_wchar * 1024]]:
+) -> typing.Iterator[tuple[_HDEVINFO, ctypes.Structure, _SP_DEVINFO_DATA, ctypes.c_wchar * 1024]]:
 	"""Internal helper function to list devices on the system for a specific device class.
 	@param deviceClass: The device class GUID.
 	:param onlyAvailable: Only return devices that are currently available.
 	"""
-	flags = DIGCF_DEVICEINTERFACE
+	flags = DIGCF.DEVICEINTERFACE
 	if onlyAvailable:
-		flags |= DIGCF_PRESENT
+		flags |= DIGCF.PRESENT
 
 	buf = ctypes.create_unicode_buffer(1024)
-	g_hdi = SetupDiGetClassDevs(ctypes.byref(deviceClass), None, None, flags)
+	g_hdi = _SetupDiGetClassDevs(ctypes.byref(deviceClass), None, None, flags)
 	try:
 		for dwIndex in range(256):
-			did = SP_DEVICE_INTERFACE_DATA()
+			did = _SP_DEVICE_INTERFACE_DATA()
 			did.cbSize = ctypes.sizeof(did)
 
-			if not SetupDiEnumDeviceInterfaces(
+			if not _SetupDiEnumDeviceInterfaces(
 				g_hdi,
 				None,
 				ctypes.byref(deviceClass),
 				dwIndex,
 				ctypes.byref(did),
 			):
-				if ctypes.GetLastError() != ERROR_NO_MORE_ITEMS:
+				if ctypes.GetLastError() != SystemErrorCodes.NO_MORE_ITEMS:
 					raise ctypes.WinError()
 				break
 
 			dwNeeded = DWORD()
 			# get the size
-			if not SetupDiGetDeviceInterfaceDetail(
+			if not _SetupDiGetDeviceInterfaceDetail(
 				g_hdi,
 				ctypes.byref(did),
 				None,
@@ -400,7 +284,7 @@ def _listDevices(
 				None,
 			):
 				# Ignore ERROR_INSUFFICIENT_BUFFER
-				if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
+				if ctypes.GetLastError() != SystemErrorCodes.INSUFFICIENT_BUFFER:
 					raise ctypes.WinError()
 
 			# allocate buffer
@@ -413,16 +297,16 @@ class SP_DEVICE_INTERFACE_DETAIL_DATA_W(ctypes.Structure):
 						WCHAR * math.ceil((dwNeeded.value - ctypes.sizeof(DWORD)) / ctypes.sizeof(WCHAR)),
 					),
 				)
-				_pack_ = dummy._pack_
+				_pack_ = _Dummy._pack_
 
 				def __str__(self):
 					return f"DevicePath:{self.DevicePath!r}"
 
 			idd = SP_DEVICE_INTERFACE_DETAIL_DATA_W()
-			idd.cbSize = SIZEOF_SP_DEVICE_INTERFACE_DETAIL_DATA_W
-			devinfo = SP_DEVINFO_DATA()
+			idd.cbSize = _SIZEOF_SP_DEVICE_INTERFACE_DETAIL_DATA_W
+			devinfo = _SP_DEVINFO_DATA()
 			devinfo.cbSize = ctypes.sizeof(devinfo)
-			if not SetupDiGetDeviceInterfaceDetail(
+			if not _SetupDiGetDeviceInterfaceDetail(
 				g_hdi,
 				ctypes.byref(did),
 				ctypes.byref(idd),
@@ -435,7 +319,7 @@ def __str__(self):
 			yield (g_hdi, idd, devinfo, buf)
 
 	finally:
-		SetupDiDestroyDeviceInfoList(g_hdi)
+		_SetupDiDestroyDeviceInfoList(g_hdi)
 
 
 def listUsbDevices(onlyAvailable: bool = True) -> typing.Iterator[dict]:
@@ -443,20 +327,20 @@ def listUsbDevices(onlyAvailable: bool = True) -> typing.Iterator[dict]:
 	:param onlyAvailable: Only return devices that are currently available.
 	:return: Generates dicts including keys of usbID (VID and PID), devicePath and hardwareID.
 	"""
-	for g_hdi, idd, devinfo, buf in _listDevices(GUID_DEVINTERFACE_USB_DEVICE, onlyAvailable):
+	for g_hdi, idd, devinfo, buf in _listDevices(_GUID_DEVINTERFACE_USB_DEVICE, onlyAvailable):
 		entry = {}
 		# hardware ID
-		if not SetupDiGetDeviceRegistryProperty(
+		if not _SetupDiGetDeviceRegistryProperty(
 			g_hdi,
 			ctypes.byref(devinfo),
-			SPDRP_HARDWAREID,
+			SPDRP.HARDWAREID,
 			None,
 			ctypes.byref(buf),
 			ctypes.sizeof(buf) - 1,
 			None,
 		):
 			# Ignore ERROR_INSUFFICIENT_BUFFER
-			if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
+			if ctypes.GetLastError() != SystemErrorCodes.INSUFFICIENT_BUFFER:
 				raise ctypes.WinError()
 		else:
 			# The string is of the form "usb\VID_xxxx&PID_xxxx&..."
@@ -473,10 +357,10 @@ def listUsbDevices(onlyAvailable: bool = True) -> typing.Iterator[dict]:
 
 		# Bus reported device description
 		propRegDataType = DWORD()
-		if not SetupDiGetDeviceProperty(
+		if not _SetupDiGetDeviceProperty(
 			g_hdi,
 			ctypes.byref(devinfo),
-			ctypes.byref(DEVPKEY_Device_BusReportedDeviceDesc),
+			ctypes.byref(_DEVPKEY_Device_BusReportedDeviceDesc),
 			ctypes.byref(propRegDataType),
 			ctypes.byref(buf),
 			ctypes.sizeof(buf) - 1,
@@ -494,18 +378,6 @@ def listUsbDevices(onlyAvailable: bool = True) -> typing.Iterator[dict]:
 		log.debug("Finished listing USB devices")
 
 
-class HIDD_ATTRIBUTES(ctypes.Structure):
-	_fields_ = (
-		("Size", ULONG),
-		("VendorID", USHORT),
-		("ProductID", USHORT),
-		("VersionNumber", USHORT),
-	)
-
-	def __init__(self, **kwargs):
-		super().__init__(Size=ctypes.sizeof(HIDD_ATTRIBUTES), **kwargs)
-
-
 _getHidInfoCache: dict[str, dict] = {}
 
 
@@ -554,8 +426,8 @@ def _getHidInfo(hwId: str, path: str) -> dict[str, typing.Any]:
 			log.debugWarning(f"Opening device {path} to get additional info failed: {ctypes.WinError(err)}")
 		return info
 	try:
-		attribs = HIDD_ATTRIBUTES()
-		if ctypes.windll.hid.HidD_GetAttributes(handle, ctypes.byref(attribs)):
+		attribs = _HIDD_ATTRIBUTES()
+		if _HidD_GetAttributes(handle, ctypes.byref(attribs)):
 			info["vendorID"] = attribs.VendorID
 			info["productID"] = attribs.ProductID
 			info["versionNumber"] = attribs.VersionNumber
@@ -564,18 +436,18 @@ def _getHidInfo(hwId: str, path: str) -> dict[str, typing.Any]:
 				log.debugWarning("HidD_GetAttributes failed")
 		buf = ctypes.create_unicode_buffer(128)
 		nrOfBytes = ctypes.sizeof(buf)
-		if ctypes.windll.hid.HidD_GetManufacturerString(handle, buf, nrOfBytes):
+		if _HidD_GetManufacturerString(handle, buf, nrOfBytes):
 			info["manufacturer"] = buf.value
-		if ctypes.windll.hid.HidD_GetProductString(handle, buf, nrOfBytes):
+		if _HidD_GetProductString(handle, buf, nrOfBytes):
 			info["product"] = buf.value
 		pd = ctypes.c_void_p()
-		if ctypes.windll.hid.HidD_GetPreparsedData(handle, ctypes.byref(pd)):
+		if _HidD_GetPreparsedData(handle, ctypes.byref(pd)):
 			try:
 				caps = hidpi.HIDP_CAPS()
-				ctypes.windll.hid.HidP_GetCaps(pd, ctypes.byref(caps))
+				_HidP_GetCaps(pd, ctypes.byref(caps))
 				info["HIDUsagePage"] = caps.UsagePage
 			finally:
-				ctypes.windll.hid.HidD_FreePreparsedData(pd)
+				_HidD_FreePreparsedData(pd)
 	finally:
 		winKernel.closeHandle(handle)
 	_getHidInfoCache[path] = info
@@ -595,21 +467,21 @@ def listHidDevices(onlyAvailable: bool = True) -> typing.Iterator[dict]:
 	global _hidGuid
 	if not _hidGuid:
 		_hidGuid = GUID()
-		ctypes.windll.hid.HidD_GetHidGuid(ctypes.byref(_hidGuid))
+		_HidD_GetHidGuid(ctypes.byref(_hidGuid))
 
 	for g_hdi, idd, devinfo, buf in _listDevices(_hidGuid, onlyAvailable):
 		# hardware ID
-		if not SetupDiGetDeviceRegistryProperty(
+		if not _SetupDiGetDeviceRegistryProperty(
 			g_hdi,
 			ctypes.byref(devinfo),
-			SPDRP_HARDWAREID,
+			SPDRP.HARDWAREID,
 			None,
 			ctypes.byref(buf),
 			ctypes.sizeof(buf) - 1,
 			None,
 		):
 			# Ignore ERROR_INSUFFICIENT_BUFFER
-			if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
+			if ctypes.GetLastError() != SystemErrorCodes.INSUFFICIENT_BUFFER:
 				raise ctypes.WinError()
 		else:
 			hwId = buf.value
@@ -620,3 +492,79 @@ def listHidDevices(onlyAvailable: bool = True) -> typing.Iterator[dict]:
 
 	if _isDebug():
 		log.debug("Finished listing HID devices")
+
+
+__getattr__ = utils._deprecate.handleDeprecations(
+	# Now in winBindings.advapi32
+	utils._deprecate.MovedSymbol("RegCloseKey", "winBindings.advapi32"),
+	# Now in winBindings.bthprops
+	utils._deprecate.MovedSymbol("BLUETOOTH_ADDRESS", "winBindings.bthprops"),
+	utils._deprecate.MovedSymbol("BLUETOOTH_DEVICE_INFO", "winBindings.bthprops"),
+	utils._deprecate.MovedSymbol("BLUETOOTH_MAX_NAME_SIZE", "winBindings.bthprops"),
+	utils._deprecate.MovedSymbol("BluetoothGetDeviceInfo", "winBindings.bthprops"),
+	utils._deprecate.MovedSymbol("BTH_ADDR", "winBindings.bthprops", "BLUETOOTH_ADDRESS"),
+	# Now in winBindings.cfgmgr32
+	utils._deprecate.MovedSymbol("CM_Get_Device_ID", "winBindings.cfgmgr32"),
+	utils._deprecate.MovedSymbol("CR_SUCCESS", "winBindings.cfgmgr32"),
+	utils._deprecate.MovedSymbol("MAX_DEVICE_ID_LEN", "winBindings.cfgmgr32"),
+	# Now in winBindings.hid
+	utils._deprecate.MovedSymbol("HIDD_ATTRIBUTES", "winBindings.hid"),
+	utils._deprecate.MovedSymbol("HidD_FreePreparsedData", "winBindings.hid"),
+	utils._deprecate.MovedSymbol("HidD_GetAttributes", "winBindings.hid"),
+	utils._deprecate.MovedSymbol("HidD_GetHidGuid", "winBindings.hid"),
+	utils._deprecate.MovedSymbol("HidD_GetManufacturerString", "winBindings.hid"),
+	utils._deprecate.MovedSymbol("HidD_GetPreparsedData", "winBindings.hid"),
+	utils._deprecate.MovedSymbol("HidD_GetProductString", "winBindings.hid"),
+	utils._deprecate.MovedSymbol("HidP_GetCaps", "winBindings.hid"),
+	# Now in winBindings.setupapi
+	utils._deprecate.MovedSymbol("DEVPKEY_Device_BusReportedDeviceDesc", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("DEVPROPKEY", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("DICS_FLAG_GLOBAL", "winBindings.setupapi", "DICS_FLAG", "GLOBAL"),
+	utils._deprecate.MovedSymbol("DIGCF_DEVICEINTERFACE", "winBindings.setupapi", "DIGCF", "DEVICEINTERFACE"),
+	utils._deprecate.MovedSymbol("DIGCF_PRESENT", "winBindings.setupapi", "DIGCF", "PRESENT"),
+	utils._deprecate.MovedSymbol("DIREG_DEV", "winBindings.setupapi", "DIREG", "DEV"),
+	utils._deprecate.MovedSymbol("dummy", "winBindings.setupapi", "_Dummy"),
+	utils._deprecate.MovedSymbol("GUID_CLASS_COMPORT", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("GUID_DEVINTERFACE_USB_DEVICE", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("HDEVINFO", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("PSP_DEVICE_INTERFACE_DATA", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("PSP_DEVICE_INTERFACE_DETAIL_DATA", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("PSP_DEVINFO_DATA", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("SetupDiDestroyDeviceInfoList", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("SetupDiEnumDeviceInfo", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("SetupDiEnumDeviceInterfaces", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("SetupDiGetClassDevs", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("SetupDiGetDeviceInterfaceDetail", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("SetupDiGetDeviceProperty", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("SetupDiGetDeviceRegistryProperty", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("SetupDiOpenDevRegKey", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("SIZEOF_SP_DEVICE_INTERFACE_DETAIL_DATA_W", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("SP_DEVICE_INTERFACE_DATA", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("SP_DEVINFO_DATA", "winBindings.setupapi"),
+	utils._deprecate.MovedSymbol("SPDRP_DEVICEDESC", "winBindings.setupapi", "SPDRP", "DEVICEDESC"),
+	utils._deprecate.MovedSymbol("SPDRP_FRIENDLYNAME", "winBindings.setupapi", "SPDRP", "FRIENDLYNAME"),
+	utils._deprecate.MovedSymbol("SPDRP_HARDWAREID", "winBindings.setupapi", "SPDRP", "HARDWAREID"),
+	utils._deprecate.MovedSymbol(
+		"SPDRP_LOCATION_INFORMATION",
+		"winBindings.setupapi",
+		"SPDRP",
+		"LOCATION_INFORMATION",
+	),
+	# Now in winAPI.constants
+	utils._deprecate.MovedSymbol(
+		"ERROR_INSUFFICIENT_BUFFER",
+		"winAPI.constants",
+		"SystemErrorCodes",
+		"INSUFFICIENT_BUFFER",
+	),
+	utils._deprecate.MovedSymbol(
+		"ERROR_NO_MORE_ITEMS",
+		"winAPI.constants",
+		"SystemErrorCodes",
+		"NO_MORE_ITEMS",
+	),
+	# No longer part of the public API
+	utils._deprecate.RemovedSymbol("INVALID_HANDLE_VALUE", 0),
+	utils._deprecate.RemovedSymbol("ValidHandle", _ValidHandle),
+)
+"""Module __getattr__ to handle backward compatibility."""

```