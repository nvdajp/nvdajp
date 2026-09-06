# coding: UTF-8
# mecab.py for python-jtalk

CODE = "utf-8"

import os
import re
import sys
import threading
from ctypes import (
	POINTER,
	Structure,
	byref,
	cast,
	c_char,
	c_char_p,
	c_double,
	c_float,
	c_int,
	c_long,
	c_short,
	c_ubyte,
	c_uint,
	c_ulonglong,
	c_ushort,
	c_void_p,
	cdll,
	create_string_buffer,
	memmove,
	string_at,
	windll,
)
from pathlib import Path
from typing import Optional
from collections.abc import Callable

# Type alias for logging functions
# Accepts both logHandler.log.debug (method) and custom print functions (callable)
# Used in Mecab_initialize, Mecab_analysis, etc.
LogWriteFunc = Optional[Callable[[str], None]]

# Try to import Windows API for code page detection
try:
	_kernel32 = windll.kernel32
except (ImportError, AttributeError):
	_kernel32 = None

try:
	from ._nvdajp_spellchar import convert as convertSpellChar
	from .roma2kana import getKanaFromRoma
	from .text2mecab import text2mecab
except (ImportError, ValueError):
	from _nvdajp_spellchar import convert as convertSpellChar  # type: ignore
	from roma2kana import getKanaFromRoma  # type: ignore
	from text2mecab import text2mecab  # type: ignore

c_double_p = POINTER(c_double)
c_double_p_p = POINTER(c_double_p)
c_short_p = POINTER(c_short)
c_char_p_p = POINTER(c_char_p)

##############################################

# http://mecab.sourceforge.net/libmecab.html
# c:/mecab/sdk/mecab.h
MECAB_NOR_NODE = 0
MECAB_UNK_NODE = 1
MECAB_BOS_NODE = 2
MECAB_EOS_NODE = 3


class mecab_token_t(Structure):
	pass


mecab_token_t_ptr = POINTER(mecab_token_t)


class mecab_path_t(Structure):
	pass


mecab_path_t_ptr = POINTER(mecab_path_t)


class mecab_node_t(Structure):
	pass


mecab_node_t_ptr = POINTER(mecab_node_t)
mecab_node_t_ptr_ptr = POINTER(mecab_node_t_ptr)
mecab_node_t._fields_ = [
	("prev", mecab_node_t_ptr),
	("next", mecab_node_t_ptr),
	("enext", mecab_node_t_ptr),
	("bnext", mecab_node_t_ptr),
	("rpath", mecab_path_t_ptr),
	("lpath", mecab_path_t_ptr),
	("surface", c_char_p),
	("feature", c_char_p),
	("id", c_uint),
	("length", c_ushort),
	("rlength", c_ushort),
	("rcAttr", c_ushort),
	("lcAttr", c_ushort),
	("posid", c_ushort),
	("char_type", c_ubyte),
	("stat", c_ubyte),
	("isbest", c_ubyte),
	("alpha", c_float),
	("beta", c_float),
	("prob", c_float),
	("wcost", c_short),
	("cost", c_long),
]

############################################

FELEN = 2000  # string len
FECOUNT = 1000
FEATURE = c_char * FELEN
FEATURE_ptr = POINTER(FEATURE)
FEATURE_ptr_array = FEATURE_ptr * FECOUNT
FEATURE_ptr_array_ptr = POINTER(FEATURE_ptr_array)

mecab = None
libmc = None
lock = threading.Lock()

# Configure malloc/calloc/free for x64 safety
# On x64, we must explicitly specify argtypes to ensure correct argument sizes
# size_t is 8 bytes on x64, so we use c_size_t (or c_ulonglong as fallback)
try:
	from ctypes import c_size_t
except ImportError:
	# Fallback for older Python versions: use c_ulonglong (8 bytes on x64)
	c_size_t = c_ulonglong

mc_malloc = cdll.msvcrt.malloc
mc_malloc.argtypes = [c_size_t]  # malloc(size_t size)
mc_malloc.restype = POINTER(c_ubyte)

mc_calloc = cdll.msvcrt.calloc
mc_calloc.argtypes = [c_size_t, c_size_t]  # calloc(size_t nmemb, size_t size)
mc_calloc.restype = POINTER(c_ubyte)

mc_free = cdll.msvcrt.free
mc_free.argtypes = [c_void_p]  # free(void *ptr)
mc_free.restype = None


class NonblockingMecabFeatures:
	def __init__(self):
		self.size = 0
		self.feature = FEATURE_ptr_array()
		for i in range(FECOUNT):
			buf = mc_malloc(FELEN)
			if not buf:
				# memmove into a NULL slot would corrupt memory silently;
				# fail loudly instead. Slots already allocated are freed by
				# __del__ (free(NULL) is a safe no-op for the rest).
				raise MemoryError("mecab: failed to allocate feature buffer")
			self.feature[i] = cast(buf, FEATURE_ptr)

	def __del__(self):
		for i in range(FECOUNT):
			try:
				mc_free(self.feature[i])
			except Exception:
				pass


class MecabFeatures(NonblockingMecabFeatures):
	def __init__(self):
		lock.acquire()
		# The lock must be released exactly once even if buffer allocation
		# fails here or __del__ runs more than once, otherwise every later
		# MeCab consumer deadlocks waiting on the lock.
		self._lock_held = True
		try:
			super().__init__()
		except Exception:
			self._lock_held = False
			lock.release()
			raise

	def __del__(self):
		super().__del__()
		if getattr(self, "_lock_held", False):
			self._lock_held = False
			lock.release()


def mecab_analyze_and_correct(
	src: bytes,
	logwrite_: LogWriteFunc = None,
) -> NonblockingMecabFeatures:
	"""Run Mecab_analysis and Mecab_correctFeatures with minimal lock duration.

	nvdajp/nvdajp#114: When JTalk (speech) and braille display both use MeCab,
	they contend on a single lock. Previously MecabFeatures held the lock for
	its entire lifetime including during libjt_synthesis (which can take seconds).
	This blocked braille updates on the main thread, causing lag and unresponsive
	speech cancellation when pressing cursor keys rapidly.

	This helper holds the lock only during the actual MeCab DLL calls. Callers
	can then process the returned features (Mecab_splitFeatures, mecab_to_morphs,
	libjt_synthesis, etc.) without blocking other MeCab consumers.
	"""
	mf = NonblockingMecabFeatures()
	with lock:
		Mecab_analysis(src, mf, logwrite_=logwrite_)
		Mecab_correctFeatures(mf, logwrite_=logwrite_)
	return mf


# Dictionary configuration of the current tagger: (dic, user_dics) both
# normalized to strings. None while no tagger exists. Mecab_initialize uses
# this to decide whether an existing tagger can be reused or must be rebuilt.
_mecab_config = None


def Mecab_terminate(logwrite_: LogWriteFunc = None) -> None:
	"""Destroy the current MeCab tagger so Mecab_initialize can rebuild it.

	Mecab_initialize calls this automatically when it is invoked with a
	dictionary configuration different from the current tagger's, so callers
	normally do not need to call it themselves.
	"""
	global mecab, _mecab_config
	if mecab is None:
		return
	with lock:
		if libmc is not None:
			try:
				libmc.mecab_destroy(mecab)
			except Exception:
				if logwrite_:
					logwrite_("Mecab_terminate: mecab_destroy failed")
		mecab = None
		_mecab_config = None


def Mecab_initialize(
	logwrite_: LogWriteFunc = None,
	libmecab_dir: str | Path | None = None,
	dic: str | Path | None = None,
	user_dics: list[str] | None = None,
) -> None:
	"""Initialize or reuse the process-global MeCab tagger.

	If a tagger already exists but the requested ``(dic, user_dics)`` differs
	from ``_mecab_config``, the old tagger is destroyed and rebuilt. Previously
	the first successful initialization won for the rest of the process (silent
	no-op on later calls), which made jpSmokeTests order-dependent. Production
	callers such as ``translator2.initialize`` and ``jtalkDriver`` normally pass
	the same ``user_dics`` and are unaffected.

	Config comparison and ``mecab_new`` run outside ``lock``; smoke tests are
	single-threaded. See ``projectDocs/jp/tab-character-analysis.md`` (2026-06-11).
	"""
	if libmecab_dir is None or dic is None:
		raise ValueError("libmecab_dir and dic must be provided")
	mecab_dll = str(Path(libmecab_dir) / "libmecab.dll")
	global libmc, mecab
	if libmc is None:
		libmc = cdll.LoadLibrary(mecab_dll)
		# Configure ctypes signatures. On 64-bit Python, we must explicitly
		# specify pointer argument and return types so that 8-byte pointers
		# are handled correctly.
		libmc.mecab_version.restype = c_char_p
		libmc.mecab_strerror.restype = c_char_p
		libmc.mecab_strerror.argtypes = [c_void_p]
		libmc.mecab_sparse_tonode.restype = mecab_node_t_ptr
		libmc.mecab_sparse_tonode.argtypes = [c_void_p, c_char_p]
		libmc.mecab_new.argtypes = [c_int, c_char_p_p]
		libmc.mecab_new.restype = c_void_p
		libmc.mecab_destroy.argtypes = [c_void_p]
		libmc.mecab_destroy.restype = None
	# At this point, libmc is guaranteed to be initialized (not None)
	assert libmc is not None  # Type narrowing for type checkers
	global mecab, _mecab_config
	# Normalize the requested configuration the same way it is consumed below:
	# an empty user_dics list selects the same tagger as None.
	requested_config = (
		str(dic),
		tuple(str(s) for s in user_dics) if user_dics else None,
	)
	if mecab is not None and requested_config != _mecab_config:
		# A tagger built for a different dictionary configuration exists.
		# Initialization used to be a silent no-op here, which made results
		# depend on which module initialized MeCab first in the process.
		if logwrite_:
			logwrite_(
				f"Mecab_initialize: dictionary configuration changed, reinitializing: "
				f"{_mecab_config} -> {requested_config}",
			)
		Mecab_terminate(logwrite_)
	# Always print/log the version and dictionary info if logwrite_ is provided,
	# even if mecab is already initialized.
	if logwrite_:
		logwrite_("dic: %s" % dic)
		try:
			dic_version_path = Path(dic) / "DIC_VERSION"
			s = dic_version_path.read_text(encoding="utf-8").strip()
			version_str = libmc.mecab_version().decode("utf-8", "ignore")
			logwrite_("mecab:" + version_str + " " + s)
		except Exception:
			pass
	if mecab is None:
		# libmc is guaranteed to be initialized at this point (asserted above)
		assert libmc is not None  # Type narrowing for type checkers
		try:
			dic_version_path = Path(dic) / "DIC_VERSION"
			s = dic_version_path.read_text(encoding="utf-8").strip()
			# check utf-8 dictionary
			if CODE not in s:
				raise RuntimeError("utf-8 dictionary for mecab required.")
		except Exception:
			pass
		mecabrc = str(Path(libmecab_dir) / "mecabrc")
		dic_str = str(dic)
		argc, args = (
			5,
			(c_char_p * 5)(b"mecab", b"-d", dic_str.encode("utf-8"), b"-r", mecabrc.encode("utf-8")),
		)
		if user_dics:
			# ignore item which contains comma
			ud = ",".join([s for s in user_dics if "," not in s])
			if logwrite_:
				logwrite_("user_dics: %s" % ud)
			argc, args = (
				7,
				(c_char_p * 7)(
					b"mecab",
					b"-d",
					dic_str.encode("utf-8"),
					b"-r",
					mecabrc.encode("utf-8"),
					b"-u",
					ud.encode("utf-8"),
				),
			)
		mecab_result = libmc.mecab_new(argc, args)
		# CRITICAL FIX: On x64, mecab_new may return int despite restype=c_void_p
		# Convert to c_void_p explicitly to ensure correct 8-byte pointer handling
		if mecab_result:
			if isinstance(mecab_result, int):
				mecab = c_void_p(mecab_result)
				if logwrite_:
					logwrite_(
						f"Mecab_initialize: converted mecab from int to c_void_p: {mecab_result} -> {mecab.value}",
					)
			elif not isinstance(mecab_result, c_void_p):
				mecab = cast(mecab_result, c_void_p)
				if logwrite_:
					logwrite_(
						f"Mecab_initialize: converted mecab to c_void_p: {type(mecab_result)} -> {mecab.value}",
					)
			else:
				mecab = mecab_result
				if logwrite_:
					logwrite_(f"Mecab_initialize: mecab is already c_void_p: {mecab.value}")
		else:
			mecab = None
		if not mecab:
			# mecab_new failed - mecab_strerror should not be called with NULL pointer (causes access violation on x64)
			error_msg = "mecab_new failed: failed to initialize MeCab"
			if logwrite_:
				logwrite_(error_msg)
			# Raise exception to prevent using uninitialized mecab (causes access violation on x64)
			raise RuntimeError(error_msg)
		_mecab_config = requested_config
		if logwrite_:
			s = libmc.mecab_strerror(mecab).strip()
			if s:
				logwrite_(s)


def Mecab_analysis(
	src: bytes,
	features: MecabFeatures | NonblockingMecabFeatures,
	logwrite_: LogWriteFunc = None,
) -> None:
	# CRITICAL: Declare global mecab at the start of the function
	# This must be before any reference to mecab to avoid SyntaxError
	global mecab

	# Helper function to write to debug log file (ensures logs are captured even on crash)
	def _write_debug_log(msg):
		try:
			debug_log_path = Path(__file__).parent / "mecab_debug.log"
			with open(debug_log_path, "a", encoding="utf-8", errors="replace") as f:
				f.write(msg + "\n")
				f.flush()
				os.fsync(f.fileno())  # Force write to disk
		except Exception:
			# Debug logging is best-effort only. Failures when writing the debug log
			# must not interfere with normal Mecab operation, so we intentionally
			# ignore any exceptions raised here.
			pass

	# Log code page information for debugging (Windows only)
	code_page_info = ""
	if _kernel32 is not None:
		try:
			cp = _kernel32.GetACP()
			code_page_info = f", code_page={cp}"
		except Exception:
			# Code page detection is best-effort only. Failures must not interfere
			# with normal Mecab operation, so we intentionally ignore exceptions.
			pass

	_write_debug_log(
		f"Mecab_analysis: called with src type={type(src)}, len={len(src) if src else 0}{code_page_info}",
	)

	if not src:
		msg = "src empty"
		_write_debug_log(msg)
		if logwrite_:
			logwrite_(msg)
		features.size = 0
		return
	# Check if mecab and libmc are initialized (prevents access violation on x64)
	if mecab is None or libmc is None:
		if logwrite_:
			logwrite_("mecab or libmc is not initialized")
		features.size = 0
		return
	# Ensure src is bytes (required for mecab_sparse_tonode on x64)
	if not isinstance(src, bytes):
		if logwrite_:
			logwrite_(f"src is not bytes: {type(src)}")
		features.size = 0
		return
	assert isinstance(src, bytes), "mecab: src must be bytes"
	assert len(src) > 0, "mecab: src is empty"
	assert b"\0" not in src, "mecab: src contains NUL byte"
	assert b"\n" not in src and b"\r" not in src, "mecab: src contains CR/LF bytes"
	# Ensure UTF-8 decoding is possible for debug purposes (expected input encoding).
	try:
		src.decode(CODE)
	except Exception as e:
		assert False, f"mecab: src is not valid {CODE}: {e}"
	# Log src type and content for debugging (first 100 bytes)
	if logwrite_:
		try:
			src_preview = src[:100] if len(src) > 100 else src
			null_byte = b"\0"
			ends_with_null = src.endswith(null_byte)
			logwrite_(
				f"Mecab_analysis: src type={type(src)}, len={len(src)}, preview={src_preview!r}, ends_with_null={ends_with_null}",
			)
			if len(src) <= 256:
				logwrite_(f"Mecab_analysis: src_full_bytes={src!r}")
		except Exception:
			# Logging is best-effort only. Failures must not interfere
			# with normal Mecab operation, so we intentionally ignore exceptions.
			pass
	# Validate mecab pointer is not NULL (prevents access violation on x64)
	# CRITICAL FIX: On x64, mecab may be stored as int (from previous code or ctypes behavior)
	# Convert to c_void_p explicitly to ensure correct 8-byte pointer handling
	if not mecab:
		if logwrite_:
			logwrite_("mecab pointer is NULL or invalid")
		features.size = 0
		return
	# Ensure mecab is c_void_p type (required for x64)
	mecab_original_type = type(mecab)
	mecab_original_value = mecab.value if hasattr(mecab, "value") else mecab
	if isinstance(mecab, int):
		mecab = c_void_p(mecab) if mecab else None
		_write_debug_log(
			f"Mecab_analysis: converted mecab from int to c_void_p: {mecab_original_type} -> {type(mecab)}, value={mecab.value if mecab else None}",
		)
	elif not isinstance(mecab, c_void_p):
		mecab = cast(mecab, c_void_p) if mecab else None
		_write_debug_log(
			f"Mecab_analysis: converted mecab to c_void_p: {mecab_original_type} -> {type(mecab)}, value={mecab.value if mecab else None}",
		)
	else:
		_write_debug_log(
			f"Mecab_analysis: mecab is already c_void_p: {mecab_original_type}, value={mecab_original_value}",
		)
	if not mecab:
		if logwrite_:
			logwrite_("mecab pointer is NULL or invalid after conversion")
		features.size = 0
		return
	mecab_value = mecab.value if hasattr(mecab, "value") else (mecab if mecab else 0)
	if mecab_value == 0:
		if logwrite_:
			logwrite_("mecab pointer value is 0")
		features.size = 0
		return
	# Log debug info before calling mecab_sparse_tonode (for troubleshooting)
	# Use multiple output methods for maximum reliability:
	# 1. sys.stderr (unbuffered, captured by CI) - only if NVDA_MECAB_STDERR_DEBUG is set
	# 2. logwrite_ (may be io.StringIO() buffer, can be lost on crash)
	# 3. Try to write to file if possible (most reliable for crash debugging)
	# Note: ctypes automatically null-terminates bytes when converting to c_char_p,
	# so no manual null termination is needed (matches original jtalk.py behavior)
	log_msg = f"Mecab_analysis: calling mecab_sparse_tonode with mecab={mecab_value}, src_len={len(src)}"

	# Method 1: Write to stderr first (unbuffered, captured by CI)
	# Only output to stderr if explicitly enabled via environment variable to avoid
	# excessive logging during normal operation (e.g., jp smoke tests, production builds)
	#
	# When to enable NVDA_MECAB_STDERR_DEBUG=1:
	# - When debugging MeCab-related crashes that occur before logwrite_ or debug log file
	#   can be written (e.g., access violations in mecab_sparse_tonode)
	# - When investigating issues in CI environments where stderr is captured but
	#   log files may not be accessible
	# - When reproducing specific crashes in development environments
	# - NOT needed for normal jp smoke tests (sufficient logging via logwrite_ and
	#   mecab_debug.log is available)
	#
	# Usage example:
	#   $env:NVDA_MECAB_STDERR_DEBUG="1"; python -m unittest miscDepsJp.jptools.test
	if os.environ.get("NVDA_MECAB_STDERR_DEBUG") == "1":
		try:
			sys.stderr.write(log_msg + "\n")
			sys.stderr.flush()
		except Exception:
			# stderr writing is best-effort only. Failures must not interfere
			# with normal Mecab operation, so we intentionally ignore exceptions.
			pass

	# Method 2: Write to logwrite_ if available (may be io.StringIO() buffer)
	if logwrite_:
		try:
			logwrite_(log_msg)
		except Exception:
			# logwrite_ callback is best-effort only. Failures must not interfere
			# with normal Mecab operation, so we intentionally ignore exceptions.
			pass

	# Method 3: Try to write to a debug file (most reliable for crash debugging)
	# This ensures logs are captured even if process crashes immediately
	_write_debug_log(log_msg)
	# Call mecab_sparse_tonode - argtypes are already configured for x64 safety
	# Pass bytes directly (matches original jtalk.py implementation)
	# ctypes will automatically convert bytes to c_char_p when argtypes is [c_void_p, c_char_p]
	# Note: access violations may not be caught by Python exception handlers,
	# but logging before the call ensures we capture state even if crash occurs
	head = libmc.mecab_sparse_tonode(mecab, src)
	if head is None:
		if logwrite_:
			logwrite_("mecab_sparse_tonode result empty")
		features.size = 0
		return
	# Validate head pointer is not NULL (prevents access violation on x64)
	# head is mecab_node_t_ptr type, check if it's a valid pointer
	if hasattr(head, "value") and head.value == 0:
		if logwrite_:
			logwrite_("mecab_sparse_tonode returned NULL pointer")
		features.size = 0
		return
	features.size = 0

	# make array of features
	node = head
	i = 0
	while node:
		s = node[0].stat
		if s != MECAB_BOS_NODE and s != MECAB_EOS_NODE:
			c = node[0].length
			s = string_at(node[0].surface, c) + b"," + string_at(node[0].feature)
			assert i < FECOUNT, "mecab node count exceeds FECOUNT"
			assert len(s) < FELEN, "mecab feature buffer overflow risk"
			if logwrite_:
				logwrite_(s.decode(CODE, "ignore"))
			buf = create_string_buffer(s)
			dst_ptr = features.feature[i]
			src_ptr = byref(buf)
			memmove(dst_ptr, src_ptr, len(s) + 1)
			i += 1
		node = node[0].next
		features.size = i
		if i >= FECOUNT:
			if logwrite_:
				logwrite_("too many nodes")
			return
	return


# for debug
def Mecab_print(
	mf: MecabFeatures | NonblockingMecabFeatures,
	logwrite_: LogWriteFunc = None,
	CODE_: str = CODE,
	output_header: bool = True,
) -> None:
	if logwrite_ is None:
		return
	feature = mf.feature
	size = mf.size
	if feature is None or size is None:
		if output_header:
			logwrite_("Mecab_print size: 0")
		return
	s2 = ""
	if output_header:
		s2 += "Mecab_print size: %d\n" % size
	for i in range(size):
		s = string_at(feature[i])
		if s:
			if CODE_ is None:
				s2 += "%d %s\n" % (i, s)
			else:
				s2 += "%d %s\n" % (i, s.decode(CODE_, "ignore"))
		else:
			s2 += "[None]\n"
	logwrite_(s2)


def Mecab_getFeature(mf: MecabFeatures | NonblockingMecabFeatures, pos: int, CODE_: str = CODE) -> str:
	s = string_at(mf.feature[pos])
	return s.decode(CODE_, "ignore")


def Mecab_setFeature(
	mf: MecabFeatures | NonblockingMecabFeatures,
	pos: int,
	s: str,
	CODE_: str = CODE,
) -> None:
	s_encoded = s.encode(CODE_, "ignore")
	# Security: each feature slot is a fixed FELEN-byte heap buffer
	# (see NonblockingMecabFeatures). Writing a longer feature would
	# overflow the heap. Fail loudly instead, the same way Mecab_analysis
	# asserts len(s) < FELEN for freshly parsed nodes.
	if len(s_encoded) >= FELEN:
		raise ValueError(f"mecab feature too long: {len(s_encoded)} bytes >= {FELEN}")
	buf = create_string_buffer(s_encoded)
	dst_ptr = mf.feature[pos]
	src_ptr = byref(buf)
	memmove(dst_ptr, src_ptr, len(s_encoded) + 1)


def getMoraCount(s: str) -> int:
	# 1/3 => 3
	# */* => 0
	m = s.split("/")
	if len(m) == 2:
		m2 = m[1]
		if m2 != "*":
			return int(m2)
	return 0


RE_FULLSHAPE_ALPHA = re.compile("^[Ａ-Ｚａ-ｚ]+$")


def _shouldWorkAroundLatinWordPostfix(ar3, ar2, ar):
	return (
		(not (ar3 and ar3[0] == "\u3000" and ar2 and ar2[0] == "’"))
		and ar2
		and ar[0] in ("ｓ", "ｄ", "ｅｄ", "ｒ", "ｔｉｎｇ", "ｔ")
	)


def _makeFeatureFromLatinWordAndPostfix(org, ar, symbol=""):
	_hyoki = ar[0]
	_yomi = ar[8] if len(ar) > 8 else convertSpellChar(_hyoki).replace(" ", "")
	_pron = ar[9] if len(ar) > 9 else convertSpellChar(_hyoki).replace(" ", "")
	hin1 = ar[1]
	hin2 = ar[2]
	hin3 = ar[3]
	postfix = ""
	if org == "ｓ":
		postfix = "ズ"
		if _hyoki.endswith("ｐ") or _hyoki.endswith("ｋｅ") or _hyoki.endswith("ｒｋ"):
			postfix = "ス"
		elif _hyoki.endswith("ｔｈａｔ"):
			# that's ザットゥズ -> ザッツ
			postfix = "ツ"
			_yomi = _yomi[:-2]
			_pron = _pron[:-2]
		elif _hyoki.endswith("ｗｏｒｄ"):
			# https://github.com/nvdajp/nvdajpmiscdep/issues/53
			# words ワードズ -> ワーズ
			postfix = "ズ"
			_yomi = _yomi[:-1]
			_pron = _pron[:-1]
	elif org == "ｔ":
		postfix = "ト"
	elif org in ("ｄ", "ｅｄ"):
		if _hyoki.endswith("ｔｅ") and _yomi.endswith("ト"):
			# update アップデート -> updated アップデーティド
			postfix = "ティド"
			_yomi = _yomi[:-1]
			_pron = _pron[:-1]
		else:
			postfix = "ド"
	elif org == "ｒ":
		postfix = "ア"
		if _hyoki.endswith("ｓｅ"):
			postfix = "ザー"
			_yomi = _yomi[:-1]
			_pron = _pron[:-1]
	elif _hyoki.endswith("ｔ") and _yomi.endswith("ト") and org == "ｔｉｎｇ":
		postfix = "ティング"
		_yomi = _yomi[:-1]
		_pron = _pron[:-1]
	hyoki = _hyoki + symbol + org
	yomi = _yomi + postfix
	pron = _pron + postfix
	mora = getMoraCount(ar[10]) + 1 if len(ar) > 10 else len(pron)
	feature = f"{hyoki},{hin1},{hin2},{hin3},*,*,*,{hyoki},{yomi},{pron},0/{mora},C0"
	return feature


def _makeBraillePatternReading(s):
	n = ord(s) - 0x2800
	if n == 0:
		return "マスアケ"
	ar = []
	if n & 0x01:
		ar.append("イチ")
	if n & 0x02:
		ar.append("ニー")
	if n & 0x04:
		ar.append("サン")
	if n & 0x08:
		ar.append("ヨン")
	if n & 0x10:
		ar.append("ゴー")
	if n & 0x20:
		ar.append("ロク")
	if n & 0x40:
		ar.append("ナナ")
	if n & 0x80:
		ar.append("ハチ")
	return "".join(ar) + "ノテン"


def Mecab_correctFeatures(
	mf: MecabFeatures | NonblockingMecabFeatures,
	CODE_: str = CODE,
	logwrite_: LogWriteFunc = None,
) -> None:
	for pos in range(mf.size):
		ar = Mecab_getFeature(mf, pos, CODE_=CODE_).split(",")
		if pos >= 1:
			ar2 = Mecab_getFeature(mf, pos - 1, CODE_=CODE_).split(",")
		else:
			ar2 = None
		if pos >= 2:
			ar3 = Mecab_getFeature(mf, pos - 2, CODE_=CODE_).split(",")
		else:
			ar3 = None
		if (
			ar3
			and ar2
			and RE_FULLSHAPE_ALPHA.match(ar3[0])
			and RE_FULLSHAPE_ALPHA.match(ar2[0])
			and RE_FULLSHAPE_ALPHA.match(ar[0])
		):
			# nvdajp/nvdajpmiscdep#28
			# before:
			# 0 ｓ,記号,アルファベット,*,*,*,*,ｓ,エス,エス,1/2,*
			# 1 ａｔｏｋ,名詞,一般,*,*,*,*,ａｔｏｋ,エイトック,エイトック,0/5,C0
			# 2 ｏ,記号,アルファベット,*,*,*,*,ｏ,オー,オー,1/2,*
			# after:
			# 0 ,,,*,*,*,*
			# 1 ,,,*,*,*,*
			# 2 ｓａｔｏｋｏ,名詞,固有名詞,*,*,*,*,ｓａｔｏｋｏ,サトコ,サトコ,0/3,C0
			hyoki = ar3[0] + ar2[0] + ar[0]
			hin1 = "名詞"
			hin2 = "固有名詞"
			yomi = getKanaFromRoma(hyoki)
			if yomi:
				pron = yomi
				mora = len(yomi)
				feature = f"{hyoki},{hin1},{hin2},*,*,*,*,{hyoki},{yomi},{pron},0/{mora},C0"
				Mecab_setFeature(mf, pos - 2, ",,,*,*,*,*", CODE_=CODE_)
				Mecab_setFeature(mf, pos - 1, ",,,*,*,*,*", CODE_=CODE_)
				Mecab_setFeature(mf, pos, feature, CODE_=CODE_)
		elif (ar[2] == "数" and ar[7] == "*") or (ar[1] == "名詞" and ar[2] == "サ変接続" and ar[7] == "*"):
			# PATTERN 1
			# before:
			# 1 五絡脈病証,名詞,数,*,*,*,*,*
			#
			# after:
			# 1 五絡脈病証,名詞,普通名詞,*,*,*,*,五絡脈病証,ゴミャクラクビョウショウ,
			# ゴミャクラクビョーショー,1/9,C0
			#
			# PATTERN 2
			# before:
			# 0 ∫⣿♪　,名詞,サ変接続,*,*,*,*,*
			#
			# after:
			# 0 ∫⣿♪　,名詞,サ変接続,*,*,*,*,∫♪　,セキブンキゴーイチニーサンヨンゴーロクナナ
			# ハチノテンオンプ,セキブンキゴーイチニーサンヨンゴーロクナナハチノテンオンプ,1/29,C0
			#
			hyoki = ar[0]
			yomi = ""
			pron = ""
			mora = 0
			nbmf = NonblockingMecabFeatures()
			for c in hyoki:
				Mecab_analysis(text2mecab(c, CODE_=CODE_), nbmf)
				for pos2 in range(nbmf.size):
					ar2 = Mecab_getFeature(nbmf, pos2, CODE_=CODE_).split(",")
					if len(ar2) > 10:
						yomi += ar2[8]
						pron += ar2[9]
						mora += getMoraCount(ar2[10])
			nbmf = None
			feature = f"{hyoki},名詞,普通名詞,*,*,*,*,{hyoki},{yomi},{pron},0/{mora},C0"
			# Security: this pattern concatenates one re-parsed reading per
			# input character, so yomi/pron can grow far beyond the original
			# morpheme. The feature slot is a fixed FELEN-byte heap buffer;
			# if the result would not fit, skip the correction and keep the
			# original feature (JTalk already falls back for morphemes whose
			# reading is unknown).
			if len(feature.encode(CODE_, "ignore")) >= FELEN:
				if logwrite_:
					logwrite_(
						f"mecab_correctFeatures: corrected feature too long "
						f"({len(feature)} chars), skipped correction"
					)
				continue
			Mecab_setFeature(mf, pos, feature, CODE_=CODE_)
		elif ar2 and ar[0] == "ー" and ar[1] == "名詞" and ar[2] == "一般":
			# PATTERN 3
			# before:
			# 0 ま,接頭詞,名詞接続,*,*,*,*,ま,マ,マ,1/1,P2
			# 1 ー,名詞,一般,*,*,*,*,*
			#
			# after:
			# 0 ま,接頭詞,名詞接続,*,*,*,*,まー,マー,マー,1/2,P2
			# 1 ー,名詞,一般,*,*,*,*,*
			#
			if len(ar2) > 10:
				hyoki = ar2[0] + "ー"
				hin1 = ar2[1]
				hin2 = ar2[2]
				yomi = ar2[8] + "ー"
				pron = ar2[9] + "ー"
				mora = getMoraCount(ar2[10]) + 1
				feature = f"{hyoki},{hin1},{hin2},*,*,*,*,{hyoki},{yomi},{pron},0/{mora},C0"
				Mecab_setFeature(mf, pos - 1, feature, CODE_=CODE_)
			elif ar3 and ar2 and len(ar3) > 10 and ar3[1] != "記号":
				hyoki = ar3[0] + ar2[0] + "ー"
				hin1 = ar3[1]
				hin2 = ar3[2]
				yomi = ar3[8] + ar2[0] + "ー"
				pron = ar3[9] + ar2[0] + "ー"
				mora = getMoraCount(ar3[10]) + len(ar2[0]) + 1
				feature = f"{hyoki},{hin1},{hin2},*,*,*,*,{hyoki},{yomi},{pron},0/{mora},C0"
				Mecab_setFeature(mf, pos - 2, feature, CODE_=CODE_)
		elif _shouldWorkAroundLatinWordPostfix(ar3, ar2, ar):
			# https://github.com/nvdajp/nvdajpmiscdep/issues/42
			# print ((unicode(ar3[0]) if ar3 else '*') + '/' + (unicode(ar2[0]) if ar2 else '*') + '/' + (unicode(ar[0]) if ar else '*')).encode('utf-8')
			# pattern 5
			if ar3 and ar2 and ar2[0] in ("'", "’"):
				# PATTERN 5 "author's"
				# before:
				# 0 ａｕｔｈｏｒ,名詞,一般,*,*,*,*,ａｕｔｈｏｒ,オーサー,オーサー,1/4,C0
				# 1 ’,記号,括弧閉,*,*,*,*,’,’,’,*/*,*
				# 2 ｓ,記号,アルファベット,*,*,*,*,ｓ,エス,エス,1/2,*
				#
				# after:
				# 0 ,,,*,*,*,*
				# 1 ,,,*,*,*,*
				# 2 ａｕｔｈｏｒｓ,名詞,一般,*,*,*,*,ｓ,オーサーズ,オーサーズ,1/5,C0
				Mecab_setFeature(mf, pos - 2, ",,,*,*,*,*", CODE_=CODE_)
				Mecab_setFeature(mf, pos - 1, ",,,*,*,*,*", CODE_=CODE_)
				f = _makeFeatureFromLatinWordAndPostfix(ar[0], ar3, symbol="'")
				Mecab_setFeature(mf, pos, f, CODE_=CODE_)
			elif ar2 and len(ar2) > 10 and RE_FULLSHAPE_ALPHA.match(ar2[0]) and len(ar2[0]) > 1:
				# PATTERN 4
				# before:
				# 0 ｔａｋｅ,名詞,一般,*,*,*,*,ｔａｋｅ,テイク,テイク,1/3,C0
				# 1 ｓ,記号,アルファベット,*,*,*,*,ｓ,エス,エス,1/2,*
				#
				# after:
				# 0 ,,,*,*,*,*
				# 1 ｔａｋｅｓ,名詞,一般,*,*,*,*,ｔａｋｅ,テイクス,テイクス,1/4,C0
				Mecab_setFeature(mf, pos - 1, ",,,*,*,*,*", CODE_=CODE_)
				f = _makeFeatureFromLatinWordAndPostfix(ar[0], ar2)
				Mecab_setFeature(mf, pos, f, CODE_=CODE_)
		elif ar2 and RE_FULLSHAPE_ALPHA.match(ar[0]) and RE_FULLSHAPE_ALPHA.match(ar2[0]):
			# and not (len(ar2) > 10 and ar2[10] and ar2[10][0] == '0' and len(ar) > 10 and ar[10] and ar[10][0] == '0'):
			# 0 ｓｈｉ,名詞,一般,*,*,*,*,ｓｈｉ,シ,シ,1/1,C0
			# 1 ｍａｎｅ,名詞,一般,*,*,*,*,ｍａｎｅ,メイン,メイン,1/3,C0
			#
			# 0 ｋｉｔ,名詞,一般,*,*,*,*,ｋｉｔ,キットゥ,キットゥ,1/4,C0
			# 1 ａ,記号,アルファベット,*,*,*,*,ａ,エイ,エイ,1/2,*
			#
			# https://github.com/nvdajp/nvdajpmiscdep/issues/58
			# 英単語を0型アクセントで登録しているので、0型同士の場合は元の読みを使用する
			#
			hyoki = ar2[0] + ar[0]
			hin1 = "名詞"
			hin2 = "固有名詞"
			yomi = getKanaFromRoma(hyoki)
			if yomi:
				pron = yomi
				mora = len(yomi)
				feature = f"{hyoki},{hin1},{hin2},*,*,*,*,{hyoki},{yomi},{pron},0/{mora},C0"
				Mecab_setFeature(mf, pos - 1, ",,,*,*,*,*", CODE_=CODE_)
				Mecab_setFeature(mf, pos, feature, CODE_=CODE_)
		elif RE_FULLSHAPE_ALPHA.match(ar[0]) and ar[7] == "*":
			roma = ar[0]
			kana = getKanaFromRoma(roma)
			if kana:
				c = len(kana)
				Mecab_setFeature(
					mf,
					pos,
					"%s,名詞,固有名詞,*,*,*,*,%s,%s,%s,0/%d,C0" % (roma, roma, kana, kana, c),
					CODE_=CODE_,
				)
		elif len(ar[0]) == 1 and 0x2800 <= ord(ar[0]) <= 0x28FF:
			ar[8] = ar[9] = _makeBraillePatternReading(ar[0])
			Mecab_setFeature(mf, pos, ",".join(ar), CODE_=CODE_)


def Mecab_utf8_to_cp932(mf: MecabFeatures | NonblockingMecabFeatures) -> None:
	for pos in range(mf.size):
		s = Mecab_getFeature(mf, pos, CODE_="utf-8")
		Mecab_setFeature(mf, pos, s, CODE_="cp932")


def Mecab_duplicateFeatures(
	mf: MecabFeatures | NonblockingMecabFeatures,
	startPos: int = 0,
	stopPos: int | None = None,
	CODE_: str = "utf-8",
) -> NonblockingMecabFeatures:
	if not stopPos:
		stopPos = mf.size
	nbmf = NonblockingMecabFeatures()
	newPos = 0
	for pos in range(startPos, stopPos):
		s = Mecab_getFeature(mf, pos, CODE_)
		Mecab_setFeature(nbmf, newPos, s, CODE_)
		newPos += 1
	nbmf.size = newPos
	return nbmf


def Mecab_splitFeatures(
	mf: MecabFeatures | NonblockingMecabFeatures,
	CODE_: str = "utf-8",
) -> list[NonblockingMecabFeatures]:
	ar = []
	startPos = 0
	for pos in range(mf.size):
		a = Mecab_getFeature(mf, pos, CODE_).split(",")
		if a[0].isspace() or a[1] == "記号" and a[2] in ("空白", "句点", "読点"):
			f = Mecab_duplicateFeatures(mf, startPos, pos + 1, CODE_)
			ar.append(f)
			startPos = pos + 1
	if startPos < mf.size:
		f = Mecab_duplicateFeatures(mf, startPos, mf.size, CODE_)
		ar.append(f)
	return ar
