# characterDescriptions.dic 形式から characters.dic 書式にする

import pathlib
import sys
import io
from _jpchar import (
	read_character_descriptions_dic,
)

# リダイレクトされた標準出力を文字コード UTF-8 で扱う
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

character_descriptions_dict = read_character_descriptions_dic(
	pathlib.Path.cwd().parent / "source" / "locale" / "ja" / "characterDescriptions.dic"
)

# character_descriptions_dict を Unicode 番号順に並べて出力する
# 文字コード16進でソートされている
# u+100 ごとにコメントを出力する
prev_char = chr(0)
for char in sorted(character_descriptions_dict.keys()):
	# 下から3桁目よりも上を比較する
	if hex(ord(prev_char))[:-2] != hex(ord(char))[:-2]:
		print("")
		hex_str = hex(ord(char))[2:-2] + "xx"
		if len(hex_str) < 5:
			hex_str = "0" * (5 - len(hex_str)) + hex_str
		print(f"# {hex_str}")
	reading = character_descriptions_dict[char]
	code = f"{ord(char):04x}"
	print(f"{char}\t{code}\t[{reading}]\t{reading}")
	prev_char = char
