# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023 Takuya Nishimoto, NVDA Japanese Team, Shuaruta Inc.
# en/symbols.dic にある文字で characters.dic に含まれていない文字を検出する
# usage:
# > cd jpchar
# > py -3 checkEnSymbolsAndCharacters.py

import pathlib
import sys
import io


# リダイレクトされた標準出力を文字コード UTF-8 で扱う
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# symbols.dic を読み込む
def read_symbols_dic(symbols_dic_path):
    symbols_dict = {}
    symbols_started = False
    with open(symbols_dic_path, "r", encoding="utf-8") as f:
        # ファイルからデータを読み込む
        lines = f.read().splitlines()

        # データを処理する
        line_number = 0
        for line in lines:
            line_number += 1

            # 空行の場合はスキップ
            if len(line) == 0:
                continue

            # symbols: という行が来るまではスキップ
            # この行が見つかったら symbols_started を True にする
            if line.endswith("symbols:"):
                symbols_started = True
                continue
            if not symbols_started:
                continue

            # 行の1文字目が # の場合はコメントとみなしてスキップ
            if line.startswith("#"):
                continue

            # 行の1文字目がバックスラッシュの場合は直後の # をコメントと見なさない
            line = line.replace("\\#", "#")

            # それ以外で1文字目がバックスラッシュの場合はスキップ
            if line.startswith("\\"):
                continue

            # 行をタブで分割して、各列を取得する
            cols = line.split("\t")
            if len(cols) < 2:
                continue

            # 各列の値を取得する
            char = cols[0]
            reading = cols[1]

            # char ends with sentence ending などの場合はスキップ
            if char.endswith("sentence ending"):
                continue
            if char.endswith("phrase ending"):
                continue
            if char.endswith("decimal point"):
                continue
            if char.endswith("decimal number"):
                continue
            if char.endswith("negative number"):
                continue
            if char.startswith("in-word"):
                continue
            if len(char) != 1:
                continue

            symbols_dict[char] = (line_number, f"u+{ord(char):04x}", reading)
    return symbols_dict


en_symbols_dict = read_symbols_dic(
    pathlib.Path.cwd().parent / "source" / "locale" / "en" / "symbols.dic"
)

ja_symbols_dict = read_symbols_dic(
    pathlib.Path.cwd().parent / "source" / "locale" / "ja" / "symbols.dic"
)

ja_cldr_dict = read_symbols_dic(
    pathlib.Path.cwd().parent / "include" / "nvda-cldr" / "locale" / "ja" / "cldr.dic"
)

# characterDescriptions.dic を読み込む
def read_character_descriptions_dic(character_descriptions_dic_path):
    descs_dict = {}

    with open(character_descriptions_dic_path, "r", encoding="utf-8") as f:
        # ファイルからデータを読み込む
        lines = f.read().splitlines()

        # データを処理する
        for line in lines:
            # 空行の場合はスキップ
            if len(line) == 0:
                continue

            # 行の1文字目が # の場合はコメントとみなしてスキップ
            if line.startswith("#"):
                continue

            # 行の1文字目がバックスラッシュの場合は直後の # をコメントと見なさない
            line = line.replace("\\#", "#")

            # 行をタブで分割して、各列を取得する
            cols = line.split("\t")
            if len(cols) < 2:
                continue

            # 各列の値を取得する
            char = cols[0]
            description = cols[1]

            descs_dict[char] = description
    return descs_dict


ja_descs_dict = read_character_descriptions_dic(
    pathlib.Path.cwd().parent / "source" / "locale" / "ja" / "characterDescriptions.dic"
)


# characters.dic を読み込む
def read_characters_dic(characters_dic_path):
    characters_dict = {}

    with open(characters_dic_path, "r", encoding="utf-8") as f:
        # ファイルからデータを読み込む
        lines = f.read().splitlines()

        # データを処理する
        for line in lines:
            # 空行の場合はスキップ
            if len(line) == 0:
                continue

            # 行の1文字目が # の場合はコメントとみなしてスキップ
            if line.startswith("#"):
                continue

            # 行の1文字目がバックスラッシュの場合は直後の # をコメントと見なさない
            line = line.replace("\\#", "#")

            # 行をタブで分割して、各列を取得する
            cols = line.split("\t")
            if len(cols) < 2:
                continue

            # 各列の値を取得する
            char = cols[0]
            code = cols[1]
            reading = cols[2].replace("[", "").replace("]", "")
            description = cols[3]

            characters_dict[char] = (reading, description, code)
    return characters_dict


characters_dict = read_characters_dic(
    pathlib.Path.cwd().parent / "source" / "locale" / "ja" / "characters.dic"
)

# en_symbols_dict にある文字が characters_dict に含まれていない場合を検出する
for char in en_symbols_dict.keys():
    if char not in characters_dict.keys():
        code = (
            en_symbols_dict[char][1]
            .replace("u+00", "")
            .replace("u+0", "")
            .replace("u+", "")
        )
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
