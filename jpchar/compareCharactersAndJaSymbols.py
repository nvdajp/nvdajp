# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023 Takuya Nishimoto, NVDA Japanese Team, Shuaruta Inc.
# characters.dic にある文字で ja/symbols.dic にないものを探す

import pathlib
import sys
import io
from _jpchar import (
	read_symbols_dic,
	read_characters_dic,
	read_character_descriptions_dic,
)

# リダイレクトされた標準出力を文字コード UTF-8 で扱う
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

en_symbols_dict = read_symbols_dic(pathlib.Path.cwd().parent / "source" / "locale" / "en" / "symbols.dic")
ja_symbols_dict = read_symbols_dic(pathlib.Path.cwd().parent / "source" / "locale" / "ja" / "symbols.dic")
ja_cldr_dict = read_symbols_dic(
	pathlib.Path.cwd().parent / "include" / "nvda-cldr" / "locale" / "ja" / "cldr.dic"
)
ja_descs_dict = read_character_descriptions_dic(
	pathlib.Path.cwd().parent / "source" / "locale" / "ja" / "characterDescriptions.dic"
)
characters_dict = read_characters_dic(
	pathlib.Path.cwd().parent / "source" / "locale" / "ja" / "characters.dic"
)

# characters_dict にある文字で ja_symbols_dict にないものを探す
# u+100 ごとにコメントを出力する
prev_char = chr(0)
for char in characters_dict.keys():
	if char not in ja_symbols_dict.keys():
		reading = characters_dict[char][1]

		# 下から3桁目よりも上を比較する
		if hex(ord(prev_char))[:-2] != hex(ord(char))[:-2]:
			print("")
			print(f"# {hex(ord(char)).replace('0x', 'U+')[:-2]}00-")

		# symbols.dic の形式で出力する
		print(f"{char}\t{reading}")
	prev_char = char
