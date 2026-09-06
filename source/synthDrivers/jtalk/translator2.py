# coding: UTF-8
# translator2.py (compatibility shim over the vendored libkuraji)
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2026 Takuya Nishimoto (NVDA Japanese Team / Shuaruta Inc.)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
#
# The Japanese braille word-separation engine now lives in libkuraji
# (source/libkuraji, vendored from https://github.com/nishimotz/libkuraji,
# BSD 3-Clause). This module keeps the historical NVDAJP entry points and
# wires in the MeCab analyzer (JTalk extended dictionary) on demand.

import sys
from pathlib import Path

try:
	from libkuraji import translator2 as _t2
except ImportError:
	# tools such as jptools run with only synthDrivers/jtalk on sys.path;
	# make the source directory importable so that libkuraji resolves
	sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
	from libkuraji import translator2 as _t2

try:
	from .mecabAnalyzer import MecabAnalyzer
except (ImportError, ValueError):
	from mecabAnalyzer import MecabAnalyzer  # type: ignore

_logwrite = None
try:
	from logHandler import log  # type: ignore

	_logwrite = log.debug
except Exception:

	def __print(s):
		print(s)

	_logwrite = __print

# re-exported helpers used by jptools and tests
mecab_to_morphs = _t2.mecab_to_morphs
mergePositionMap = _t2.mergePositionMap
makeOutPos = _t2.makeOutPos


def initialize(logwrite=_logwrite, mecab_dir_=None, dic_dir_=None, user_dics_=None, analyzer=None):
	if analyzer is None:
		analyzer = MecabAnalyzer()
		# raises RuntimeError when MeCab is not actually ready
		analyzer.initialize(logwrite, mecab_dir_, dic_dir_, user_dics_)
	_t2.initialize(analyzer=analyzer, logwrite=logwrite)


def terminate():
	_t2.terminate()


def _ensure_initialized(logwrite):
	if not _t2.mecab_initialized:
		initialize(logwrite=logwrite)


def translateWithInPos2(
	inbuf,
	logwrite=_logwrite,
	nabcc=False,
	louisTranslate=None,
	louisTableList=None,
	use_foreign_quotes=False,
):
	_ensure_initialized(logwrite)
	return _t2.translateWithInPos2(
		inbuf,
		logwrite=logwrite,
		nabcc=nabcc,
		louisTranslate=louisTranslate,
		louisTableList=louisTableList,
		use_foreign_quotes=use_foreign_quotes,
	)


# for brailleViewer
def getReadingAndBraille(text, logwrite=_logwrite, nabcc=False):
	return translateWithInPos2(text, logwrite=logwrite, nabcc=nabcc)[0:2]


def japaneseToUnicodeBraille(text, logwrite=_logwrite, nabcc=False):
	return translateWithInPos2(text, logwrite=logwrite, nabcc=nabcc)[0]


def translate(
	inbuf,
	cursorPos=0,
	logwrite=_logwrite,
	unicodeIO=False,
	nabcc=False,
	louisTranslate=None,
	louisTableList=None,
	use_foreign_quotes=False,
):
	"""Translate with the libkuraji engine.

	Note: libkuraji enforces a max input length (65,536 chars by default,
	see libkuraji.limits) and raises InputTooLongError. The braille path in
	louisHelper catches it and falls back to liblouis; other callers must
	handle the exception themselves.
	"""
	_ensure_initialized(logwrite)
	return _t2.translate(
		inbuf,
		cursorPos=cursorPos,
		logwrite=logwrite,
		unicodeIO=unicodeIO,
		nabcc=nabcc,
		louisTranslate=louisTranslate,
		louisTableList=louisTableList,
		use_foreign_quotes=use_foreign_quotes,
	)
