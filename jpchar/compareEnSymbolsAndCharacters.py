# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023 Takuya Nishimoto, NVDA Japanese Team, Shuaruta Inc.
# en/symbols.dic にある文字で characters.dic に含まれていない文字を検出する
# usage:
# > cd jpchar
# > py -3 checkEnSymbolsAndCharacters.py

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

# en_symbols_dict にある文字が characters_dict に含まれていない場合を検出する
for char in en_symbols_dict.keys():
	if char not in characters_dict.keys():
		code = en_symbols_dict[char][1].replace("u+00", "").replace("u+0", "").replace("u+", "")
		reading = description = en_symbols_dict[char][2]

		# ja_cldr_dict に含まれている場合は読みと説明を上書きする
		if char in ja_cldr_dict.keys():
			reading = description = ja_cldr_dict[char][2]

		# ja_symbols_dict に含まれている場合は読みを上書きする
		if char in ja_symbols_dict.keys():
			reading = description = ja_symbols_dict[char][2]

		# ja_descs_dict に含まれている場合は説明を上書きする
		if char in ja_descs_dict.keys():
			description = ja_descs_dict[char]

		# characters.dic の形式で出力する
		print(f"{char}\t{code}\t[{reading}]\t{description}")
