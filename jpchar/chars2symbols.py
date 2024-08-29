# coding: utf-8
# characters.dic 形式から Unicode 番号順に並べて symbols.dic 書式にする
# 必ずこの文字で音声エンジンに読ませる場合のための定義
#
# input (tab separated):
# 䪼	4abc	[セツ]	デグチノ デルニ ミギガ オーガイノ セツ
#
# output (tab separated):
# 䪼	セツ		# 䪼 U+4abc

import pathlib
import sys
import io
from _jpchar import (
	read_characters_dic,
)

# リダイレクトされた標準出力を文字コード UTF-8 で扱う
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

characters_dict = read_characters_dic(
	pathlib.Path.cwd().parent / "source" / "locale" / "ja" / "characters.dic"
)

# characters_dict を Unicode 番号順に並べて出力する
# 文字コード16進でソートされている
# u+100 ごとにコメントを出力する
prev_char = chr(0)
for char in sorted(characters_dict.keys()):
	# 下から3桁目よりも上を比較する
	if hex(ord(prev_char))[:-2] != hex(ord(char))[:-2]:
		print("")
		print(f"# {hex(ord(char))[:-2]}00-")
	print(f"{char}\t{characters_dict[char][1]}")
	prev_char = char
