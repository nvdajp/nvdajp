# Diff for: `source\hidpi.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\hidpi.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\hidpi.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\hidpi.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\hidpi.py"
index 2fed2f6..3c6f728 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\hidpi.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\hidpi.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2021 NV Access Limited
+# Copyright (C) 2021-2025 NV Access Limited
 
 """
 Required types and defines from Windows SDK's hidpi.h
@@ -9,7 +9,7 @@
 """
 
 import enum
-from ctypes import Structure, Union, c_byte
+from ctypes import Structure, Union, c_byte, c_long
 from ctypes.wintypes import USHORT, BOOLEAN, ULONG, LONG
 
 
@@ -52,6 +52,17 @@ class HIDP_REPORT_TYPE(enum.IntEnum):
 	OUTPUT = 1
 	FEATURE = 2
 
+	@classmethod
+	def from_param(cls, obj):
+		"""
+		Used by ctypes for automatic parameter conversion when passing
+		HIDP_REPORT_TYPE values to C functions. Converts the enum or integer
+		to a c_long as required by the Windows API.
+		"""
+		if isinstance(obj, (cls, int)):
+			return c_long(obj)
+		raise TypeError(f"Expected {cls.__name__} or int, got {type(obj).__name__}")
+
 
 class _HIDP_DATA_U1(Union):
 	_fields_ = [
@@ -68,7 +79,7 @@ class HIDP_DATA(Structure):
 	]
 
 
-class _HIDP_VALUE_CAPS_U1_RANGE(Structure):
+class _HIDP_VALUE_AND_BUTTON_CAPS_U1_RANGE(Structure):
 	_fields_ = [
 		("UsageMin", USAGE),
 		("UsageMax", USAGE),
@@ -81,7 +92,7 @@ class _HIDP_VALUE_CAPS_U1_RANGE(Structure):
 	]
 
 
-class _HIDP_VALUE_CAPS_U1_NOT_RANGE(Structure):
+class _HIDP_VALUE_AND_BUTTON_CAPS_U1_NOT_RANGE(Structure):
 	_fields_ = [
 		("Usage", USAGE),
 		("Reserved1", USAGE),
@@ -94,14 +105,22 @@ class _HIDP_VALUE_CAPS_U1_NOT_RANGE(Structure):
 	]
 
 
-class _HIDP_VALUE_CAPS_U1(Union):
+class _HIDP_VALUE_AND_BUTTON_CAPS_U1(Union):
 	_fields_ = [
-		("Range", _HIDP_VALUE_CAPS_U1_RANGE),
-		("NotRange", _HIDP_VALUE_CAPS_U1_NOT_RANGE),
+		("Range", _HIDP_VALUE_AND_BUTTON_CAPS_U1_RANGE),
+		("NotRange", _HIDP_VALUE_AND_BUTTON_CAPS_U1_NOT_RANGE),
 	]
 
 
 class HIDP_VALUE_CAPS(Structure):
+	"""
+	Contains information that describes the capability of a set of HID control values (either a single usage or a usage range).
+	..seealso::
+		https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidpi/ns-hidpi-_hidp_value_caps
+	Note that both HIDP_BUTTON_CAPS and HIDP_VALUE_CAPS have a member named u1, which are the same type.
+	However the members before are different.
+	"""
+
 	_fields_ = [
 		("UsagePage", USAGE),
 		("ReportID", UCHAR),
@@ -125,7 +144,35 @@ class HIDP_VALUE_CAPS(Structure):
 		("LogicalMax", LONG),
 		("PhysicalMin", LONG),
 		("PhysicalMax", LONG),
-		("u1", _HIDP_VALUE_CAPS_U1),
+		("u1", _HIDP_VALUE_AND_BUTTON_CAPS_U1),
+	]
+
+
+class HIDP_BUTTON_CAPS(Structure):
+	"""
+	Contains information about the capability of a HID control button usage (or a set of buttons associated with a usage range).
+	..seealso::
+		https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/hidpi/ns-hidpi-_hidp_button_caps
+	Note that both HIDP_BUTTON_CAPS and HIDP_VALUE_CAPS have a member named u1, which are the same type.
+	However the members before are different.
+	"""
+
+	_fields_ = [
+		("UsagePage", USAGE),
+		("ReportID", UCHAR),
+		("IsAlias", BOOLEAN),
+		("BitField", USHORT),
+		("LinkCollection", USHORT),
+		("LinkUsage", USAGE),
+		("LinkUsagePage", USAGE),
+		("IsRange", BOOLEAN),
+		("IsStringRange", BOOLEAN),
+		("IsDesignatorRange", BOOLEAN),
+		("IsAbsolute", BOOLEAN),
+		("ReportCount", USHORT),
+		("Reserved2", USHORT),
+		("Reserved3", ULONG * 9),
+		("u1", _HIDP_VALUE_AND_BUTTON_CAPS_U1),
 	]
 
 

```