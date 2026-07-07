# coding: UTF-8
# mecabAnalyzer.py (adapter between translator2 and the MeCab wrapper)
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 Takuya Nishimoto (NVDA Japanese Team)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
#
# translator2 consumes morphological analysis results as a list of
# decoded MeCab feature lines. This module hides the ctypes-based MeCab
# wrapper, the dictionary location and the input encoding behind that
# interface, so that translator2 itself has no MeCab dependency and an
# alternative analyzer can be injected (e.g. for the libkuraji library).

from ctypes import string_at

try:
	from . import mecab as _mecab_module
	from .mecab import (
		CODE,
		Mecab_initialize,
		Mecab_print,
		mecab_analyze_and_correct,
	)
	from .text2mecab import text2mecab
	from .jtalkDir import jtalk_dir, dic_dir, user_dics
except (ImportError, ValueError):
	import mecab as _mecab_module  # type: ignore
	from mecab import (  # type: ignore
		CODE,
		Mecab_initialize,
		Mecab_print,
		mecab_analyze_and_correct,
	)
	from text2mecab import text2mecab  # type: ignore
	from jtalkDir import jtalk_dir, dic_dir, user_dics  # type: ignore


class MecabAnalyzer:
	"""Morphological analyzer backed by the bundled MeCab wrapper.

	The analyzer interface expected by translator2 is:
	- ``initialize(logwrite, mecab_dir, dic_dir, user_dics)``
	- ``is_ready() -> bool``
	- ``analyze(text, logwrite) -> list[str]`` returning decoded MeCab
	  feature lines (CSV: surface,POS1,POS2,...).
	"""

	def initialize(self, logwrite=None, mecab_dir=None, dic_dir_=None, user_dics_=None):
		if mecab_dir and dic_dir_ and user_dics_:
			Mecab_initialize(logwrite, mecab_dir, dic_dir_, user_dics_)
		else:
			Mecab_initialize(logwrite, jtalk_dir, dic_dir, user_dics)
		if not self.is_ready():
			msg = "MeCab initialization failed: libmc=%s, mecab=%s" % (
				_mecab_module.libmc,
				_mecab_module.mecab,
			)
			if logwrite:
				logwrite(msg)
			raise RuntimeError(msg)

	def is_ready(self):
		return _mecab_module.libmc is not None and _mecab_module.mecab is not None

	def analyze(self, text, logwrite=None):
		text = text2mecab(text)
		mf = mecab_analyze_and_correct(text, logwrite_=logwrite)
		Mecab_print(mf, logwrite, output_header=False)
		lines = []
		if mf is not None and mf.feature is not None and mf.size is not None:
			for i in range(mf.size):
				s = string_at(mf.feature[i])
				if s:
					lines.append(s.decode(CODE, "ignore"))
		return lines
