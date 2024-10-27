# characters.dic 形式から characterDescriptions.dic 書式にする

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
		hex_str = hex(ord(char))[2:-2] + "xx"
		if len(hex_str) < 5:
			hex_str = "0" * (5 - len(hex_str)) + hex_str
		print(f"# {hex_str}")
	reading = characters_dict[char][1]
	if "0" <= char <= "z" or "ｦ" <= char <= "ﾝ":
		reading = f"ハンカク {reading}"
	elif "ァ" <= char <= "ヾ":
		reading = f"カタカナ {reading}"
	print(f"{char}\t{reading}")
	prev_char = char
