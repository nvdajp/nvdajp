# Diff for: `source\synthDrivers\jtalk\jtalkCore.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\synthDrivers\jtalk\jtalkCore.py`  
**Current**: `F:\nvda\gh\alphajp\source\synthDrivers\jtalk\jtalkCore.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\jtalkCore.py" "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\jtalk\\jtalkCore.py"
index 1f42da7d3d..b5e3c0402e 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\jtalkCore.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\jtalk\\jtalkCore.py"
@@ -3,11 +3,54 @@
 # Copyright (C) 2013-2019 Takuya Nishimoto
 
 import os
+from pathlib import Path
+from typing import Callable, Optional
+from ctypes import (
+	POINTER,
+	Structure,
+	byref,
+	cast,
+	c_char,
+	c_char_p,
+	c_double,
+	c_int,
+	c_short,
+	c_size_t,
+	c_void_p,
+	create_string_buffer,
+	sizeof,
+	string_at,
+	CDLL,
+)
 
+# Import mecab-specific types and functions
 try:
-    from .mecab import *
+	from .mecab import (
+		FEATURE_ptr_array_ptr,
+		Mecab_initialize,  # noqa: F401
+		Mecab_analysis,  # noqa: F401
+		Mecab_print,  # noqa: F401
+		Mecab_correctFeatures,  # noqa: F401
+		Mecab_utf8_to_cp932,  # noqa: F401
+		MecabFeatures,  # noqa: F401
+		NonblockingMecabFeatures,  # noqa: F401
+	)
+	from .text2mecab import text2mecab  # noqa: F401
 except (ImportError, ValueError):
-    from mecab import *
+	from mecab import (  # type: ignore
+		FEATURE_ptr_array_ptr,
+	)
+
+	try:
+		from text2mecab import text2mecab  # type: ignore  # noqa: F401
+	except ImportError:
+		pass  # type: ignore
+
+# Define type aliases (matching mecab.py definitions)
+c_double_p = POINTER(c_double)
+c_double_p_p = POINTER(c_double_p)
+c_short_p = POINTER(c_short)
+c_char_p_p = POINTER(c_char_p)
 
 ############################################
 
@@ -217,6 +260,7 @@ class JPCommonLabelPhoneme(Structure):
 
 JPCommonLabelPhoneme_ptr = POINTER(JPCommonLabelPhoneme)
 
+
 # jpcommon/jpcommon.h
 class JPCommonLabel(Structure):
 	_fields_ = [
@@ -256,10 +300,10 @@ class JPCommon(Structure):
 FILENAME_ptr = POINTER(FILENAME)
 FILENAME_ptr_ptr = POINTER(FILENAME_ptr)
 
-libjt = None
-njd = NJD()
-jpcommon = JPCommon()
-engine = HTS_Engine()
+libjt: Optional[CDLL] = None
+njd: NJD = NJD()
+jpcommon: JPCommon = JPCommon()
+engine: HTS_Engine = HTS_Engine()
 
 
 def libjt_version():
@@ -273,19 +317,19 @@ def libjt_initialize(JT_DLL):
 
 	if libjt is None:
 		# Use absolute path and add DLL directory to search path
-        dll_path = os.path.abspath(JT_DLL)
-        dll_dir = os.path.dirname(dll_path)
+		dll_path = Path(JT_DLL).resolve()
+		dll_dir = dll_path.parent
 
 		# Ensure DLL directory exists
-        if not os.path.isdir(dll_dir):
+		if not dll_dir.is_dir():
 			raise OSError(f"DLL directory does not exist: {dll_dir}")
-        if not os.path.exists(dll_path):
+		if not dll_path.exists():
 			raise OSError(f"DLL file does not exist: {dll_path}")
 
 		# Add DLL directory to search path for dependencies
 		if hasattr(os, "add_dll_directory"):
 			try:
-                os.add_dll_directory(dll_dir)
+				os.add_dll_directory(str(dll_dir))
 			except OSError:
 				pass  # Ignore if already added or fails
 
@@ -293,19 +337,23 @@ def libjt_initialize(JT_DLL):
 		try:
 			from ctypes import windll, CDLL, cdll
 			from ctypes.wintypes import HANDLE, DWORD, LPCWSTR
+
 			LOAD_WITH_ALTERED_SEARCH_PATH = 0x00000008
 			LoadLibraryExW = windll.kernel32.LoadLibraryExW
 			LoadLibraryExW.argtypes = [LPCWSTR, HANDLE, DWORD]
 			LoadLibraryExW.restype = HANDLE
 
-            h = LoadLibraryExW(dll_path, None, LOAD_WITH_ALTERED_SEARCH_PATH)
+			h = LoadLibraryExW(str(dll_path), None, LOAD_WITH_ALTERED_SEARCH_PATH)
 			if not h:
 				raise OSError(f"LoadLibraryExW failed for {dll_path}")
 			libjt = CDLL("libopenjtalk", handle=h)
 		except (ImportError, AttributeError, OSError):
 			# Fallback to standard LoadLibrary if LoadLibraryExW fails
 			from ctypes import cdll
-            libjt = cdll.LoadLibrary(dll_path)
+
+			libjt = cdll.LoadLibrary(str(dll_path))
+	# At this point, libjt is guaranteed to be initialized (not None)
+	assert libjt is not None  # Type narrowing for type checkers
 	libjt.jt_version.restype = c_char_p
 
 	# argtypes & restype
@@ -357,12 +405,12 @@ def libjt_initialize(JT_DLL):
 	# MSD threshold
 	libjt.HTS_Engine_set_msd_threshold.argtypes = [HTS_Engine_ptr, c_size_t, c_double]
 	libjt.HTS_Engine_get_msd_threshold.argtypes = [HTS_Engine_ptr, c_size_t]
-    libjt.HTS_Engine_get_msd_threshold.restypes = c_double
+	libjt.HTS_Engine_get_msd_threshold.restype = c_double
 
 	# GV weight
 	libjt.HTS_Engine_set_gv_weight.argtypes = [HTS_Engine_ptr, c_size_t, c_double]
 	libjt.HTS_Engine_get_gv_weight.argtypes = [HTS_Engine_ptr, c_size_t]
-    libjt.HTS_Engine_get_gv_weight.restypes = c_double
+	libjt.HTS_Engine_get_gv_weight.restype = c_double
 
 	# alpha
 	libjt.HTS_Engine_set_alpha.argtypes = [HTS_Engine_ptr, c_double]
@@ -430,6 +478,7 @@ def libjt_initialize(JT_DLL):
 
 def libjt_load(VOICE):
 	global libjt, engine
+	assert libjt is not None  # Type narrowing for type checkers
 	fn_buf = create_string_buffer(VOICE.encode("mbcs"))
 	fn_buf_ptr = cast(byref(fn_buf), FILENAME_ptr)
 	fn_buf_ptr_ptr = cast(byref(fn_buf_ptr), FILENAME_ptr_ptr)
@@ -437,21 +486,23 @@ def libjt_load(VOICE):
 
 
 def libjt_refresh():
+	assert libjt is not None  # Type narrowing for type checkers
 	libjt.HTS_Engine_refresh(engine)
 	libjt.JPCommon_refresh(jpcommon)
 	libjt.NJD_refresh(njd)
 
 
 def libjt_clear():
+	assert libjt is not None  # Type narrowing for type checkers
 	libjt.NJD_clear(njd)
 	libjt.JPCommon_clear(jpcommon)
 	libjt.HTS_Engine_clear(engine)
 
 
-libjt_on_done = None
+libjt_on_done: Optional[Callable[[], None]] = None
 
 
-def libjt_set_on_done(func):
+def libjt_set_on_done(func: Callable[[], None]) -> None:
 	global libjt_on_done
 	libjt_on_done = func
 
@@ -473,6 +524,7 @@ def libjt_synthesis(
 ):
 	if feature is None or size is None:
 		return None
+	assert libjt is not None  # Type narrowing for type checkers
 	if logwrite_:
 		logwrite_("libjt_synthesis start.")
 	libjt.HTS_Engine_set_fperiod(engine, fperiod_)
@@ -492,9 +544,7 @@ def libjt_synthesis(
 	buf = None
 	if s > 2:
 		f = libjt.JPCommon_get_label_feature(jpcommon)
-        ret = libjt.HTS_Engine_synthesize_from_strings_ex(
-            engine, f, s, lf0_offset_, lf0_amp_
-        )
+		ret = libjt.HTS_Engine_synthesize_from_strings_ex(engine, f, s, lf0_offset_, lf0_amp_)
 		if ord(ret) == 0:
 			libjt_refresh()
 			return None
@@ -525,29 +575,35 @@ def libjt_synthesis(
 
 def libjt_set_alpha(d):
 	global libjt, engine
+	assert libjt is not None  # Type narrowing for type checkers
 	libjt.HTS_Engine_set_alpha(engine, d)
 
 
 def libjt_get_alpha():
 	global libjt, engine
+	assert libjt is not None  # Type narrowing for type checkers
 	return libjt.HTS_Engine_get_alpha(engine)
 
 
 def libjt_set_beta(d):
 	global libjt, engine
+	assert libjt is not None  # Type narrowing for type checkers
 	libjt.HTS_Engine_set_beta(engine, d)
 
 
 def libjt_get_beta():
 	global libjt, engine
+	assert libjt is not None  # Type narrowing for type checkers
 	return libjt.HTS_Engine_get_beta(engine)
 
 
 def libjt_set_gv_interpolation_weight(a, b, d):
 	global libjt, engine
+	assert libjt is not None  # Type narrowing for type checkers
 	libjt.HTS_Engine_set_gv_interpolation_weight(engine, a, b, d)
 
 
 def libjt_get_gv_interpolation_weight(a, b):
 	global libjt, engine
+	assert libjt is not None  # Type narrowing for type checkers
 	return libjt.HTS_Engine_get_gv_interpolation_weight(engine, a, b)

```