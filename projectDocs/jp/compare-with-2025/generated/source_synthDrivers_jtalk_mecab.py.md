# Diff for: `source\synthDrivers\jtalk\mecab.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\synthDrivers\jtalk\mecab.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\synthDrivers\jtalk\mecab.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\mecab.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDrivers\\jtalk\\mecab.py"
index c637fad..80fa9ff 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\mecab.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDrivers\\jtalk\\mecab.py"
@@ -3,15 +3,43 @@
 
 CODE = "utf-8"
 
-import os
-import re
-import sys
-import threading
-from ctypes import *
+import os  # noqa: E402
+import re  # noqa: E402
+import sys  # noqa: E402
+import threading  # noqa: E402
+from ctypes import (  # noqa: E402
+	POINTER,
+	Structure,
+	byref,
+	cast,
+	c_char,
+	c_char_p,
+	c_double,
+	c_float,
+	c_int,
+	c_long,
+	c_short,
+	c_ubyte,
+	c_uint,
+	c_ulonglong,
+	c_ushort,
+	c_void_p,
+	cdll,
+	create_string_buffer,
+	memmove,
+	string_at,
+	windll,
+)
+from pathlib import Path  # noqa: E402
+from typing import Callable, Optional  # noqa: E402
+
+# Type alias for logging functions
+# Accepts both logHandler.log.debug (method) and custom print functions (callable)
+# Used in Mecab_initialize, Mecab_analysis, etc.
+LogWriteFunc = Optional[Callable[[str], None]]
 
 # Try to import Windows API for code page detection
 try:
-    from ctypes import windll
 	_kernel32 = windll.kernel32
 except (ImportError, AttributeError):
 	_kernel32 = None
@@ -132,7 +160,7 @@ def __del__(self):
 		for i in range(0, FECOUNT):
 			try:
 				mc_free(self.feature[i])
-            except:
+			except Exception:
 				pass
 
 
@@ -148,9 +176,11 @@ def __del__(self):
 		lock.release()
 
 
-def Mecab_initialize(logwrite_=None, libmecab_dir=None, dic=None, user_dics=None):
-    mecab_dll = os.path.join(libmecab_dir, "libmecab.dll")
-    global libmc
+def Mecab_initialize(logwrite_: LogWriteFunc = None, libmecab_dir=None, dic=None, user_dics=None):
+	if libmecab_dir is None or dic is None:
+		raise ValueError("libmecab_dir and dic must be provided")
+	mecab_dll = str(Path(libmecab_dir) / "libmecab.dll")
+	global libmc, mecab
 	if libmc is None:
 		libmc = cdll.LoadLibrary(mecab_dll)
 		# Configure ctypes signatures. On 64-bit Python, we must explicitly
@@ -163,39 +193,69 @@ def Mecab_initialize(logwrite_=None, libmecab_dir=None, dic=None, user_dics=None
 		libmc.mecab_sparse_tonode.argtypes = [c_void_p, c_char_p]
 		libmc.mecab_new.argtypes = [c_int, c_char_p_p]
 		libmc.mecab_new.restype = c_void_p
+	# At this point, libmc is guaranteed to be initialized (not None)
+	assert libmc is not None  # Type narrowing for type checkers
 	global mecab
 	if mecab is None:
+		# libmc is guaranteed to be initialized at this point (asserted above)
+		assert libmc is not None  # Type narrowing for type checkers
 		if logwrite_:
 			logwrite_("dic: %s" % dic)
 		try:
-            f = open(os.path.join(dic, "DIC_VERSION"))
-            s = f.read().strip()
-            f.close()
+			dic_version_path = Path(dic) / "DIC_VERSION"
+			s = dic_version_path.read_text(encoding="utf-8").strip()
+			if logwrite_:
 				logwrite_("mecab:" + libmc.mecab_version() + " " + s)
 			# check utf-8 dictionary
 			if CODE not in s:
 				raise RuntimeError("utf-8 dictionary for mecab required.")
-        except:
+		except Exception:
 			pass
-        mecabrc = os.path.join(libmecab_dir, "mecabrc")
-        argc, args = 5, (c_char_p * 5)(
-            b"mecab", b"-d", dic.encode("utf-8"), b"-r", mecabrc.encode("utf-8")
+		mecabrc = str(Path(libmecab_dir) / "mecabrc")
+		dic_str = str(dic)
+		argc, args = (
+			5,
+			(c_char_p * 5)(b"mecab", b"-d", dic_str.encode("utf-8"), b"-r", mecabrc.encode("utf-8")),
 		)
 		if user_dics:
 			# ignore item which contains comma
 			ud = ",".join([s for s in user_dics if "," not in s])
 			if logwrite_:
 				logwrite_("user_dics: %s" % ud)
-            argc, args = 7, (c_char_p * 7)(
+			argc, args = (
+				7,
+				(c_char_p * 7)(
 					b"mecab",
 					b"-d",
-                dic.encode("utf-8"),
+					dic_str.encode("utf-8"),
 					b"-r",
 					mecabrc.encode("utf-8"),
 					b"-u",
 					ud.encode("utf-8"),
+				),
+			)
+		mecab_result = libmc.mecab_new(argc, args)
+		# CRITICAL FIX: On x64, mecab_new may return int despite restype=c_void_p
+		# Convert to c_void_p explicitly to ensure correct 8-byte pointer handling
+		if mecab_result:
+			if isinstance(mecab_result, int):
+				mecab = c_void_p(mecab_result)
+				if logwrite_:
+					logwrite_(
+						f"Mecab_initialize: converted mecab from int to c_void_p: {mecab_result} -> {mecab.value}"
+					)
+			elif not isinstance(mecab_result, c_void_p):
+				mecab = cast(mecab_result, c_void_p)
+				if logwrite_:
+					logwrite_(
+						f"Mecab_initialize: converted mecab to c_void_p: {type(mecab_result)} -> {mecab.value}"
 					)
-        mecab = libmc.mecab_new(argc, args)
+			else:
+				mecab = mecab_result
+				if logwrite_:
+					logwrite_(f"Mecab_initialize: mecab is already c_void_p: {mecab.value}")
+		else:
+			mecab = None
 		if not mecab:
 			# mecab_new failed - mecab_strerror should not be called with NULL pointer (causes access violation on x64)
 			error_msg = "mecab_new failed: failed to initialize MeCab"
@@ -209,11 +269,15 @@ def Mecab_initialize(logwrite_=None, libmecab_dir=None, dic=None, user_dics=None
 				logwrite_(s)
 
 
-def Mecab_analysis(src, features, logwrite_=None):
+def Mecab_analysis(src, features, logwrite_: LogWriteFunc = None):
+	# CRITICAL: Declare global mecab at the start of the function
+	# This must be before any reference to mecab to avoid SyntaxError
+	global mecab
+
 	# Helper function to write to debug log file (ensures logs are captured even on crash)
 	def _write_debug_log(msg):
 		try:
-            debug_log_path = os.path.join(os.path.dirname(__file__), "mecab_debug.log")
+			debug_log_path = Path(__file__).parent / "mecab_debug.log"
 			with open(debug_log_path, "a", encoding="utf-8", errors="replace") as f:
 				f.write(msg + "\n")
 				f.flush()
@@ -235,7 +299,9 @@ def _write_debug_log(msg):
 			# with normal Mecab operation, so we intentionally ignore exceptions.
 			pass
 
-    _write_debug_log(f"Mecab_analysis: called with src type={type(src)}, len={len(src) if src else 0}{code_page_info}")
+	_write_debug_log(
+		f"Mecab_analysis: called with src type={type(src)}, len={len(src) if src else 0}{code_page_info}"
+	)
 
 	if not src:
 		msg = "src empty"
@@ -256,29 +322,73 @@ def _write_debug_log(msg):
 			logwrite_(f"src is not bytes: {type(src)}")
 		features.size = 0
 		return
+	# BEGIN JP PATCH (assert basic bytes invariants before calling MeCab)
+	assert isinstance(src, bytes), "mecab: src must be bytes"
+	assert len(src) > 0, "mecab: src is empty"
+	assert b"\0" not in src, "mecab: src contains NUL byte"
+	assert b"\n" not in src and b"\r" not in src, "mecab: src contains CR/LF bytes"
+	# Ensure UTF-8 decoding is possible for debug purposes (expected input encoding).
+	try:
+		src.decode(CODE)
+	except Exception as e:
+		assert False, f"mecab: src is not valid {CODE}: {e}"
+	# END JP PATCH
 	# Log src type and content for debugging (first 100 bytes)
 	if logwrite_:
 		try:
 			src_preview = src[:100] if len(src) > 100 else src
-            null_byte = b'\0'
+			null_byte = b"\0"
 			ends_with_null = src.endswith(null_byte)
-            logwrite_(f"Mecab_analysis: src type={type(src)}, len={len(src)}, preview={src_preview!r}, ends_with_null={ends_with_null}")
+			logwrite_(
+				f"Mecab_analysis: src type={type(src)}, len={len(src)}, preview={src_preview!r}, ends_with_null={ends_with_null}"
+			)
+			# BEGIN JP PATCH (log full bytes for short inputs)
+			if len(src) <= 256:
+				logwrite_(f"Mecab_analysis: src_full_bytes={src!r}")
+			# END JP PATCH
 		except Exception:
 			# Logging is best-effort only. Failures must not interfere
 			# with normal Mecab operation, so we intentionally ignore exceptions.
 			pass
 	# Validate mecab pointer is not NULL (prevents access violation on x64)
-    # mecab is already c_void_p type from mecab_new, so check value directly
-    mecab_value = mecab.value if hasattr(mecab, 'value') else mecab
-    if not mecab or mecab_value == 0:
+	# CRITICAL FIX: On x64, mecab may be stored as int (from previous code or ctypes behavior)
+	# Convert to c_void_p explicitly to ensure correct 8-byte pointer handling
+	if not mecab:
 		if logwrite_:
 			logwrite_("mecab pointer is NULL or invalid")
 		features.size = 0
 		return
+	# Ensure mecab is c_void_p type (required for x64)
+	mecab_original_type = type(mecab)
+	mecab_original_value = mecab.value if hasattr(mecab, "value") else mecab
+	if isinstance(mecab, int):
+		mecab = c_void_p(mecab) if mecab else None
+		_write_debug_log(
+			f"Mecab_analysis: converted mecab from int to c_void_p: {mecab_original_type} -> {type(mecab)}, value={mecab.value if mecab else None}"
+		)
+	elif not isinstance(mecab, c_void_p):
+		mecab = cast(mecab, c_void_p) if mecab else None
+		_write_debug_log(
+			f"Mecab_analysis: converted mecab to c_void_p: {mecab_original_type} -> {type(mecab)}, value={mecab.value if mecab else None}"
+		)
+	else:
+		_write_debug_log(
+			f"Mecab_analysis: mecab is already c_void_p: {mecab_original_type}, value={mecab_original_value}"
+		)
+	if not mecab:
+		if logwrite_:
+			logwrite_("mecab pointer is NULL or invalid after conversion")
+		features.size = 0
+		return
+	mecab_value = mecab.value if hasattr(mecab, "value") else (mecab if mecab else 0)
+	if mecab_value == 0:
+		if logwrite_:
+			logwrite_("mecab pointer value is 0")
+		features.size = 0
+		return
 	# Log debug info before calling mecab_sparse_tonode (for troubleshooting)
-    # Force immediate output to stderr to ensure logs are captured even on crash
 	# Use multiple output methods for maximum reliability:
-    # 1. sys.stderr (unbuffered, captured by CI)
+	# 1. sys.stderr (unbuffered, captured by CI) - only if NVDA_MECAB_STDERR_DEBUG is set
 	# 2. logwrite_ (may be io.StringIO() buffer, can be lost on crash)
 	# 3. Try to write to file if possible (most reliable for crash debugging)
 	# Note: ctypes automatically null-terminates bytes when converting to c_char_p,
@@ -286,6 +396,21 @@ def _write_debug_log(msg):
 	log_msg = f"Mecab_analysis: calling mecab_sparse_tonode with mecab={mecab_value}, src_len={len(src)}"
 
 	# Method 1: Write to stderr first (unbuffered, captured by CI)
+	# Only output to stderr if explicitly enabled via environment variable to avoid
+	# excessive logging during normal operation (e.g., jp smoke tests, production builds)
+	#
+	# When to enable NVDA_MECAB_STDERR_DEBUG=1:
+	# - When debugging MeCab-related crashes that occur before logwrite_ or debug log file
+	#   can be written (e.g., access violations in mecab_sparse_tonode)
+	# - When investigating issues in CI environments where stderr is captured but
+	#   log files may not be accessible
+	# - When reproducing specific crashes in development environments
+	# - NOT needed for normal jp smoke tests (sufficient logging via logwrite_ and
+	#   mecab_debug.log is available)
+	#
+	# Usage example:
+	#   $env:NVDA_MECAB_STDERR_DEBUG="1"; python -m unittest miscDepsJp.jptools.test
+	if os.environ.get("NVDA_MECAB_STDERR_DEBUG") == "1":
 		try:
 			sys.stderr.write(log_msg + "\n")
 			sys.stderr.flush()
@@ -319,7 +444,7 @@ def _write_debug_log(msg):
 		return
 	# Validate head pointer is not NULL (prevents access violation on x64)
 	# head is mecab_node_t_ptr type, check if it's a valid pointer
-    if hasattr(head, 'value') and head.value == 0:
+	if hasattr(head, "value") and head.value == 0:
 		if logwrite_:
 			logwrite_("mecab_sparse_tonode returned NULL pointer")
 		features.size = 0
@@ -334,6 +459,10 @@ def _write_debug_log(msg):
 		if s != MECAB_BOS_NODE and s != MECAB_EOS_NODE:
 			c = node[0].length
 			s = string_at(node[0].surface, c) + b"," + string_at(node[0].feature)
+			# BEGIN JP PATCH (assert buffer bounds before memmove)
+			assert i < FECOUNT, "mecab node count exceeds FECOUNT"
+			assert len(s) < FELEN, "mecab feature buffer overflow risk"
+			# END JP PATCH
 			if logwrite_:
 				logwrite_(s.decode(CODE, "ignore"))
 			buf = create_string_buffer(s)
@@ -527,9 +656,7 @@ def Mecab_correctFeatures(mf, CODE_=CODE):
 				Mecab_setFeature(mf, pos - 2, ",,,*,*,*,*", CODE_=CODE_)
 				Mecab_setFeature(mf, pos - 1, ",,,*,*,*,*", CODE_=CODE_)
 				Mecab_setFeature(mf, pos, feature, CODE_=CODE_)
-        elif (ar[2] == "数" and ar[7] == "*") or (
-            ar[1] == "名詞" and ar[2] == "サ変接続" and ar[7] == "*"
-        ):
+		elif (ar[2] == "数" and ar[7] == "*") or (ar[1] == "名詞" and ar[2] == "サ変接続" and ar[7] == "*"):
 			# PATTERN 1
 			# before:
 			# 1 五絡脈病証,名詞,数,*,*,*,*,*
@@ -560,9 +687,7 @@ def Mecab_correctFeatures(mf, CODE_=CODE):
 						pron += ar2[9]
 						mora += getMoraCount(ar2[10])
 			nbmf = None
-            feature = "{h},名詞,普通名詞,*,*,*,*,{h},{y},{p},0/{m},C0".format(
-                h=hyoki, y=yomi, p=pron, m=mora
-            )
+			feature = "{h},名詞,普通名詞,*,*,*,*,{h},{y},{p},0/{m},C0".format(h=hyoki, y=yomi, p=pron, m=mora)
 			Mecab_setFeature(mf, pos, feature, CODE_=CODE_)
 		elif ar2 and ar[0] == "ー" and ar[1] == "名詞" and ar[2] == "一般":
 			# PATTERN 3
@@ -585,7 +710,7 @@ def Mecab_correctFeatures(mf, CODE_=CODE):
 					h=hyoki, h1=hin1, h2=hin2, y=yomi, p=pron, m=mora
 				)
 				Mecab_setFeature(mf, pos - 1, feature, CODE_=CODE_)
-            elif ar3 and len(ar3) > 10 and ar3[1] != "記号":
+			elif ar3 and ar2 and len(ar3) > 10 and ar3[1] != "記号":
 				hyoki = ar3[0] + ar2[0] + "ー"
 				hin1 = ar3[1]
 				hin2 = ar3[2]
@@ -600,7 +725,7 @@ def Mecab_correctFeatures(mf, CODE_=CODE):
 			# https://github.com/nvdajp/nvdajpmiscdep/issues/42
 			# print ((unicode(ar3[0]) if ar3 else '*') + '/' + (unicode(ar2[0]) if ar2 else '*') + '/' + (unicode(ar[0]) if ar else '*')).encode('utf-8')
 			# pattern 5
-            if ar3 and ar2[0] in ("'", "’"):
+			if ar3 and ar2 and ar2[0] in ("'", "’"):
 				# PATTERN 5 "author's"
 				# before:
 				# 0 ａｕｔｈｏｒ,名詞,一般,*,*,*,*,ａｕｔｈｏｒ,オーサー,オーサー,1/4,C0
@@ -615,7 +740,7 @@ def Mecab_correctFeatures(mf, CODE_=CODE):
 				Mecab_setFeature(mf, pos - 1, ",,,*,*,*,*", CODE_=CODE_)
 				f = _makeFeatureFromLatinWordAndPostfix(ar[0], ar3, symbol="'")
 				Mecab_setFeature(mf, pos, f, CODE_=CODE_)
-            elif len(ar2) > 10 and RE_FULLSHAPE_ALPHA.match(ar2[0]) and len(ar2[0]) > 1:
+			elif ar2 and len(ar2) > 10 and RE_FULLSHAPE_ALPHA.match(ar2[0]) and len(ar2[0]) > 1:
 				# PATTERN 4
 				# before:
 				# 0 ｔａｋｅ,名詞,一般,*,*,*,*,ｔａｋｅ,テイク,テイク,1/3,C0
@@ -627,9 +752,7 @@ def Mecab_correctFeatures(mf, CODE_=CODE):
 				Mecab_setFeature(mf, pos - 1, ",,,*,*,*,*", CODE_=CODE_)
 				f = _makeFeatureFromLatinWordAndPostfix(ar[0], ar2)
 				Mecab_setFeature(mf, pos, f, CODE_=CODE_)
-        elif (
-            ar2 and RE_FULLSHAPE_ALPHA.match(ar[0]) and RE_FULLSHAPE_ALPHA.match(ar2[0])
-        ):
+		elif ar2 and RE_FULLSHAPE_ALPHA.match(ar[0]) and RE_FULLSHAPE_ALPHA.match(ar2[0]):
 			# and not (len(ar2) > 10 and ar2[10] and ar2[10][0] == '0' and len(ar) > 10 and ar[10] and ar[10][0] == '0'):
 			# 0 ｓｈｉ,名詞,一般,*,*,*,*,ｓｈｉ,シ,シ,1/1,C0
 			# 1 ｍａｎｅ,名詞,一般,*,*,*,*,ｍａｎｅ,メイン,メイン,1/3,C0

```