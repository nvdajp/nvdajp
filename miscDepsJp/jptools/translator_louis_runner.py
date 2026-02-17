# -*- coding: utf-8 -*-
# jptools/translator_louis_runner.py
# translator_louis 単体テスト用: liblouis を直接呼び出し、英語 UEB Grade 2 等で変換する。
# 依存: scons で source をビルド済み（source/louis/tables, source/liblouis.dll）。
# LOUIS_TABLEPATH と sys.path を設定してから louis を import する。

from __future__ import annotations

import os
import sys
from pathlib import Path

# このファイルは miscDepsJp/jptools/translator_louis_runner.py
_jptools_dir = Path(__file__).resolve().parent
_repo_root = _jptools_dir.parent.parent  # miscDepsJp -> repo_root
_source_dir = _repo_root / "source"
_tables_dir = _source_dir / "louis" / "tables"

_louis_imported = False
_louis_module = None


def _ensure_louis():
	"""source/louis と liblouis を利用可能にし、louis モジュールを import する。失敗時は None を返す。"""
	global _louis_imported, _louis_module
	if _louis_imported:
		return _louis_module
	_louis_imported = True
	if not _tables_dir.is_dir():
		return None
	# liblouis がテーブルを探すパス（LOUIS_TABLEPATH はカンマ区切りで複数指定可）
	os.environ["LOUIS_TABLEPATH"] = str(_tables_dir)
	source_str = str(_source_dir)
	if source_str not in sys.path:
		sys.path.insert(0, source_str)
	try:
		if hasattr(os, "add_dll_directory"):
			os.add_dll_directory(source_str)
	except OSError:
		pass
	try:
		import louis as lou  # noqa: F401
		_louis_module = lou
		return lou
	except Exception:
		return None


def translate_english_ueb_g2(text: str) -> str | None:
	"""英文を liblouis の en-ueb-g2.ctb で UEB Grade 2 点字に変換する。
	Unicode 点字（U+2800–28FF）の文字列で返す。単語間はスペース (U+0020)。
	louis が利用できない場合は None を返す。"""
	lou = _ensure_louis()
	if lou is None:
		return None
	# dotsIO: 出力を Unicode 点字 (U+2800–28FF) で得る。harness と揃えるため空白は 0x20 に統一。
	mode = getattr(lou, "dotsIO", 0)
	try:
		out, inPos, outPos, cursorPos = lou.translate(
			["en-ueb-g2.ctb"],
			text,
			cursorPos=0,
			mode=mode,
		)
	except RuntimeError:
		return None
	# 既に Unicode 点字の場合はそのまま。0x80xx の場合は 0x2800+ に変換。
	chars = []
	for c in out:
		code = ord(c)
		if code == 0x20:
			chars.append(" ")
		elif 0x2800 <= code <= 0x28FF:
			chars.append(c)
		elif 0x8000 <= code <= 0x80FF:
			cell = code & 0xFF
			chars.append(chr(0x2800 + cell) if cell != 0 else " ")
		else:
			cell = code & 0xFF
			chars.append(chr(0x2800 + cell) if cell != 0 else " ")
	result = "".join(chars)
	# 空白セル (U+2800) をスペースに統一（harness 規約）
	return result.replace("\u2800", " ")


def is_louis_available() -> bool:
	"""liblouis と en-ueb-g2.ctb が利用可能なら True。"""
	return _ensure_louis() is not None


def get_louis_translate_for_pipeline(grade2_table="ueb"):
	"""translator2 パイプラインに渡す (louis.translate, table_list) を返す。
	grade2_table: "ueb" -> ["en-ueb-g2.ctb"], "us" -> ["en-us-g2.ctb"]。
	louis が利用できない場合は (None, None)。"""
	lou = _ensure_louis()
	if lou is None:
		return (None, None)
	if grade2_table == "us":
		return (lou.translate, ["en-us-g2.ctb"])
	return (lou.translate, ["en-ueb-g2.ctb"])
