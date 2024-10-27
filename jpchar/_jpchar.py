# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023 Takuya Nishimoto, NVDA Japanese Team, Shuaruta Inc.


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
