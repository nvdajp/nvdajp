# coding: utf-8

import re

RE_ALPHA = re.compile("^[Ａ-Ｚａ-ｚ]+$")
RE_NUM_SYMBOL = re.compile("^[０-９・．＆＿＋　／―′－]+$")
RE_NUMBERS = re.compile("^[０-９]{2,}$")


def is_alpha_jp_mixed(s):
	has_alpha = has_jp = False
	for c in s:
		if RE_ALPHA.match(c):
			has_alpha = True
		elif not RE_NUM_SYMBOL.match(c):
			has_jp = True
	return has_alpha and has_jp


# 0:表層形,1:左文脈ID,2:右文脈ID,3:コスト,
# 4:品詞,5:品詞細分類1,6:品詞細分類2,7:品詞細分類3,
# 8:活用形,9:活用型,10:原形,11:読み,12:発音,
# 13:アクセント位置/モーラ数,14:アクセント属性, (Open JTalk の拡張情報)
# 15:点訳 (拡張情報)
def filter_jdic(s):
	a = s.split(",")
	if a[0] == "盲" and a[11] == "メクラ":
		a[11], a[12], a[13] = "モウ", "モー", "1/2"
		s = ",".join(a)
	elif a[0] == "盲" and a[11] == "メシイ":
		s = ""
	elif a[0] == "聾" and a[11] == "ツンボ":
		a[11], a[12], a[13] = "ロウ", "ロー", "1/2"
		s = ",".join(a)
	elif a[0] == "ｚ" and a[11] == "ズィー":
		s = ""
	elif a[0] in ("ＨＴＳ", "Ｈｔｓ", "ｈｔｓ"):
		s = ""
	elif a[0] == "規" and a[11] == "ブンマワシ":
		s = ""
	elif a[0] == "全" and a[11] == "チョン":
		s = ""
	elif a[0] == "行" and a[6] == "助数詞" and a[11] == "コウ":
		s = ""
	elif a[0] == "柵" and a[11] == "シガラミ":
		s = ""
	elif a[0] == "罰" and a[11] == "バッ":
		s = ""
	elif a[0] == "罰" and a[11] == "バチ":
		s = ""
	elif a[0] == "殺" and a[11] == "コロセ":
		s = ""
	elif a[0] == "殺" and a[11] == "ヤ":
		s = ""
	elif a[0] == "００７" and a[11] == "ゼロゼロセブン":
		s = ""
	elif a[0] == "未曾有" and a[12] == "ミゾー":
		a[12] = "ミゾウ"
		s = ",".join(a)
	elif a[0] == "言う" and a[12] == "ユウ":
		a[12] = "イウ"
		s = ",".join(a)
	elif a[0] == "まごう" and a[12] == "マゴウ":
		a[12] = "マゴー"
		s = ",".join(a)
	elif a[0] == "ゆう" and a[12] == "ユウ":
		a[12] = "ユー"
		s = ",".join(a)
	elif a[0] == "おおきい" and a[12] == "オーキイ" and len(a) == 15:
		a.append(a[11])
		s = ",".join(a)
	elif a[0] == "おおまか" and a[12] == "オーマカ" and len(a) == 15:
		a.append(a[11])
		s = ",".join(a)
	elif a[0][0] == "大" and a[12][0:2] == "オー" and len(a) == 15:
		a.append(a[11])
		s = ",".join(a)
	elif a[0] == "仰せ" and a[12] == "オーセ":
		a[12] = "オオセ"
		s = ",".join(a)
	elif a[0] == "おおせる" and a[12] == "オーセル":
		a[12] = "オオセル"
		s = ",".join(a)
	elif a[0] == "車前草" and a[12] == "オーバコ":
		a[12] = "オオバコ"
		s = ",".join(a)
	elif a[0] == "概ね" and a[12] == "オームネ":
		a[12] = "オオムネ"
		s = ",".join(a)
	elif a[0] == "公" and a[12] == "オーヤケ":
		a[12] = "オオヤケ"
		s = ",".join(a)
	elif a[0] == "氷" and a[12] == "コーリ":
		a[12] = "コオリ"
		s = ",".join(a)
	elif a[0] == "凍る" and a[12] == "コール":
		a[12] = "コオル"
		s = ",".join(a)
	elif a[0] == "滞る" and a[12] == "トドコール":
		a[12] = "トドコオル"
		s = ",".join(a)
	elif a[0] == "憤る" and a[12] == "イキドール":
		a[12] = "イキドオル"
		s = ",".join(a)
	elif a[0] == "蟋蟀" and a[12] == "コーロギ":
		a[12] = "コオロギ"
		s = ",".join(a)
	elif a[0] == "遠い" and a[12] == "トーイ":
		a[12] = "トオイ"
		s = ",".join(a)
	elif a[0] == "通る" and a[12] == "トール":
		a[12] = "トオル"
		s = ",".join(a)
	elif a[0] == "頬" and a[12] == "ホー":
		a[12] = "ホオ"
		s = ",".join(a)
	elif a[0] == "酸漿" and a[12] == "ホーズキ":
		a[12] = "ホオズキ"
		s = ",".join(a)
	elif a[0] == "大目" and a[12] == "オーメ":
		a[12] = "オオメ"
		s = ",".join(a)
	elif a[0] == "大通り" and a[12] == "オードーリ":
		a[12] = "オオドオリ"
		s = ",".join(a)
	elif a[0] == "凍り付く" and a[12] == "コーリツク":
		a[12] = "コオリツク"
		s = ",".join(a)
	elif a[0] == "遠ざかる" and a[12] == "トーザカル":
		a[12] = "トオザカル"
		s = ",".join(a)
	elif a[0] == "通す" and a[12] == "トース":
		a[12] = "トオス"
		s = ",".join(a)
	elif a[0] == "頬張る" and a[12] == "ホーバル":
		a[12] = "ホオバル"
		s = ",".join(a)
	elif a[0] == "いとおしい" and a[12] == "イトーシイ":
		a[12] = "イトオシイ"
		s = ",".join(a)
	elif a[0] == "凡そ" and a[12] == "オヨソ":
		a[11] = a[12] = "オオヨソ"
		a[13] = "0/4"
		s = ",".join(a)
	elif a[0] == "無花果" and a[12] == "イチジュク":
		a[11] = a[12] = "イチジク"
		s = ",".join(a)
	elif a[0] == "鼓" and a[12] == "コ":
		a[11] = a[12] = "ツヅミ"
		s = ",".join(a)
	elif a[0] == "葛籠" and a[12] == "ツズロ":
		s = ""
	elif a[0] == "葛籠" and a[12] == "ツズラ":
		a[12] = "ツヅラ"
		s = ",".join(a)
	elif a[0] == "提灯" and a[12] == "ヂョウチン":
		a[11] = a[12] = "ヂョーチン"
		s = ",".join(a)
	elif a[0] == "青梅" and a[12] == "オウメ":
		a[11] = a[12] = "オーメ"
		s = ",".join(a)
	elif a[0] == "クヮルテット" and a[12] == "クヮルテット":
		a[11] = a[12] = "クァルテット"
		s = ",".join(a)
	elif a[0] == "スェーター" and a[12] == "スェーター":
		a[11] = a[12] = "スエーター"
		s = ",".join(a)
	elif a[0] == "憤る" and a[12] in ("ムズカル", "ムツカル"):
		s = ""
	elif a[0] == "いひ" and a[12] in ("ユイ", "イイ"):
		s = ""
	elif a[0] == "八幡平" and a[12] == "ヤワタダイラ":
		s = ""
	elif a[0] == "好かん" and a[12] == "コーカン":
		s = ""
	elif a[0] == "おおきに" and a[12] == "オーキニ":
		s = s + "," + a[11]
	elif a[0] == "かほる" and a[11] == "カホル" and a[12] == "カオル":
		s = s + "," + a[11]
	elif a[0] == "かほる" and a[11] == "カホル" and a[12] == "カホル":
		s = ""
	elif a[0] == "さをり" and a[12] == "サオリ":
		s = s + "," + a[11]
	elif a[0] == "透" and a[12] == "トール":
		s = s + "," + a[11]
	elif a[0] == "大阪" and a[12] == "オーサカ":
		s = s + "," + a[11]
	elif a[0] == "遠野" and a[12] == "トーノ":
		s = s + "," + a[11]
	elif a[0] == "みさを" and a[12] == "ミサオ":
		s = s + "," + a[11]
	elif a[0] == "そういう" and a[12] == "ソーユウ":
		s = s + ",ソー イウ"
	elif a[0] == "どうして" and a[12] == "ドーシテ":
		s = s + ",ドー シテ"
	elif a[0] == "フィードバック" and len(a) == 15:
		a.append("フィード バック")
		a[11] = a[12] = a[15].replace(" ", "")
		s = ",".join(a)
	elif a[0] == "インターフェース" and len(a) == 15:
		a.append("インター フェース")
		a[11] = a[12] = a[15].replace(" ", "")
		s = ",".join(a)
	elif a[0] == "オペレーティングシステム" and len(a) == 15:
		a.append("オペレーティング システム")
		a[11] = a[12] = a[15].replace(" ", "")
		s = ",".join(a)
	elif a[0] == "アイスクリーム" and len(a) == 15:
		a.append("アイス クリーム")
		a[11] = a[12] = a[15].replace(" ", "")
		s = ",".join(a)
	elif a[0] == "日本点字図書館" and len(a) == 15:
		a.append("ニッポン テンジ トショカン")
		a[11] = a[12] = a[15].replace(" ", "")
		s = ",".join(a)
	elif a[0] == "通り" and a[11] == "トオリ" and len(a) == 15:
		a.append(a[11])
		s = ",".join(a)
	elif a[0] == "狼" and a[11] == "オオカミ" and len(a) == 15:
		a.append(a[11])
		s = ",".join(a)
	elif a[0] == "多い" and a[11] == "オオイ" and len(a) == 15:
		a.append(a[11])
		s = ",".join(a)
	elif a[0] == "多く" and a[11] == "オオク" and len(a) == 15:
		a.append(a[11])
		s = ",".join(a)
	elif a[0] == "大晦日" and a[11] == "オオミソカ" and len(a) == 15:
		a.append(a[11])
		s = ",".join(a)
	elif a[0] == "うるう年" and a[11] == "ウルウドシ" and len(a) == 15:
		a.append(a[11])
		s = ",".join(a)
	elif a[0] == "手作り" and a[11] == "テヅクリ" and len(a) == 15:
		a.append(a[11])
		s = ",".join(a)
	elif a[0] == "南半球" and len(a) == 15:
		a.append("ミナミ ハンキュー")
		s = ",".join(a)
	elif a[0] == "アメリカ合衆国" and len(a) == 15:
		a.append("アメリカ ガッシューコク")
		s = ",".join(a)
	elif a[0] == "第一人者" and len(a) == 15:
		a.append("ダイ1ニンシャ")
		s = ",".join(a)
	elif a[0] == "一流" and len(a) == 15:
		a.append("1リュー")
		s = ",".join(a)
	elif a[0] in ("一月", "１月") and len(a) == 15:
		a.append("1ガツ")
		s = ",".join(a)
	elif a[0] in ("二月", "２月") and len(a) == 15:
		a.append("2ガツ")
		s = ",".join(a)
	elif a[0] in ("三月", "３月") and len(a) == 15:
		a.append("3ガツ")
		s = ",".join(a)
	elif a[0] in ("四月", "４月") and len(a) == 15:
		a.append("4ガツ")
		s = ",".join(a)
	elif a[0] in ("五月", "５月") and len(a) == 15:
		a.append("5ガツ")
		s = ",".join(a)
	elif a[0] in ("六月", "６月") and len(a) == 15:
		a.append("6ガツ")
		s = ",".join(a)
	elif a[0] in ("七月", "７月") and len(a) == 15:
		a.append("7ガツ")
		s = ",".join(a)
	elif a[0] in ("八月", "８月") and len(a) == 15:
		a.append("8ガツ")
		s = ",".join(a)
	elif a[0] in ("九月", "９月") and len(a) == 15:
		a.append("9ガツ")
		s = ",".join(a)
	elif a[0] in ("十月", "一〇月", "１０月") and len(a) == 15:
		a.append("10ガツ")
		s = ",".join(a)
	elif a[0] in ("十一月", "一一月", "１１月") and len(a) == 15:
		a.append("11ガツ")
		s = ",".join(a)
	elif a[0] in ("十二月", "一二月", "１２月") and len(a) == 15:
		a.append("12ガツ")
		s = ",".join(a)
	elif a[0] == "四方" and len(a) == 15:
		a.append("4ホー")
		s = ",".join(a)
	elif a[0] == "六法全書" and len(a) == 15:
		a.append("6ポー ゼンショ")
		s = ",".join(a)
	elif a[0] == "百人一首" and len(a) == 15:
		a.append("100ニン 1シュ")
		s = ",".join(a)
	elif a[0] == "日本コロムビア" and len(a) == 15:
		a.append("ニッポン コロムビア")
		a[11] = a[12] = a[15].replace(" ", "")
		s = ",".join(a)
	elif a[0] == "ビタミンＥ" and len(a) == 15:
		a.append("ビタミン E")
		s = ",".join(a)
	elif a[0] == "劇団四季" and len(a) == 15:
		a.append("ゲキダン 4キ")
		s = ",".join(a)
	elif a[0] == "四季" and len(a) == 15:
		a.append("4キ")
		s = ",".join(a)
	elif a[0] == "四半期" and len(a) == 15:
		a.append("4ハンキ")
		s = ",".join(a)
	elif a[0] == "四角形" and len(a) == 15:
		a.append("4カクケイ")
		s = ",".join(a)
	elif a[0] == "四条" and len(a) == 15:
		a.append("4ジョー")
		s = ",".join(a)
	elif a[0] == "二男" and len(a) == 15:
		a.append("2ナン")
		s = ",".join(a)
	elif a[0] == "十数" and len(a) == 15:
		a.append("10スー")
		s = ",".join(a)
	elif a[0] == "一輪車" and len(a) == 15:
		a.append("1リンシャ")
		s = ",".join(a)
	elif a[0] == "三塁打" and len(a) == 15:
		a.append("3ルイダ")
		s = ",".join(a)
	elif a[0] == "一汁一菜" and len(a) == 15:
		a.append("1ジュー 1サイ")
		s = ",".join(a)
	elif a[0] == "五臓六腑" and len(a) == 15:
		a.append("5ゾー 6プ")
		s = ",".join(a)
	elif a[0] == "一段" and len(a) == 15:
		a.append("1ダン")
		s = ",".join(a)
	elif a[0] == "七転び八起き" and len(a) == 15:
		a.append("ナナコロビ ヤオキ")
		s = ",".join(a)
	elif a[0] == "十重二十重" and len(a) == 15:
		a.append("トエ ハタエ")
		s = ",".join(a)
	elif a[0] == "３ラン" and len(a) == 15:
		a.append("3ラン")
		s = ",".join(a)
	elif a[0] == "さんりんしゃ" and len(a) == 15:
		a.append("3リンシャ")
		s = ",".join(a)
	elif a[0] == "いちばん" and len(a) == 15:
		a.append("1バン")
		s = ",".join(a)
	elif a[0] == "Ｘ線" and len(a) == 15:
		a.append("Xセン")
		s = ",".join(a)
	elif a[0] == "二・二六事件" and len(a) == 15:
		a.append("2⠼26 ジケン")
		s = ",".join(a)
	elif a[0] == "Ｂ５判" and len(a) == 15:
		a.append("B5ハン")
		s = ",".join(a)
	elif a[0] == "この間" and a[12] == "コノカン":
		s = ""
	elif a[0] == "インターネット" and len(a) == 15:
		a.append("インター ネット")
		s = ",".join(a)
	elif a[0] == "各党" and len(a) == 15:
		a.append("カク トー")
		s = ",".join(a)
	elif a[0] == "よろしくお願いします" and len(a) == 15:
		a.append("ヨロシク オネガイ シマス")
		s = ",".join(a)
	elif a[0] == "ありがとうございます" and len(a) == 15:
		a.append("アリガトー ゴザイマス")
		s = ",".join(a)
	elif a[0] == "金" and a[12] == "キム":
		s = ""
	elif a[0] == "湯川" and a[12] == "ユガワ":
		s = ""
	elif a[0] == "有難う" and a[12] == "アリガター":
		s = ""
	elif a[0] == "有り難う" and a[12] == "アリガター":
		s = ""
	elif a[0] == "難う" and a[12] == "ガター":
		s = ""
	elif a[0] == "山西" and a[12] == "サンセイ":
		s = ""
	elif a[0] == "梅木" and a[12] in ("ウメノキ", "ウメギ"):
		s = ""
	elif a[0] == "御園" and a[12] == "ミソ":
		s = ""
	elif a[0] == "新家" and a[11] in ("シンヤ", "ニイノミ"):
		s = ""
	elif a[0] == "新家" and a[6] != "人名" and a[11] == "シンケ":
		s = ""
	elif a[0] == "正岡子規":
		a.append("マサオカ シキ")
		s = ",".join(a)
	elif a[0] == "作" and a[6] == "人名" and a[11] == "ツクル":
		s = ""
	elif a[0] == "宗谷岬" and a[12] == "ソーヤミサキ":
		a.append("ソーヤ ミサキ")
		s = ",".join(a)
	elif a[0] == "丹後半島" and a[12] == "タンゴハントー":
		a.append("タンゴ ハントー")
		s = ",".join(a)
	elif a[0] == "もうすぐ" and a[12] == "モースグ":
		a.append("モー スグ")
		s = ",".join(a)
	elif a[0] == "リニアモーターカー" and a[12] == "リニアモーターカー":
		a.append("リニア モーターカー")
		s = ",".join(a)
	elif a[0] == "プレイガイド" and a[12] == "プレイガイド":
		a.append("プレイ ガイド")
		s = ",".join(a)
	elif a[0] == "仝":
		# 同上記号
		# 仝	4edd	[ドージョー]	ドージョー
		s = ""  # custom_dic_maker
	elif a[0] == "〃":
		# ノノ字点（ののじてん）・同じく記号
		# 〃	3003	[オナジク]	オナジク
		s = ""  # custom_dic_maker
	elif a[0] == "Ｎ響":
		a.append("Nキョー")
		s = ",".join(a)
	elif a[0] == "ｉモード":
		a.append("iモード")
		s = ",".join(a)
	elif a[0] == "Ｔシャツ":
		a.append("Tシャツ")
		s = ",".join(a)
	elif a[0] == "正しく" and a[4] == "副詞" and a[12] == "マサシク":
		s = ""
	elif a[0] == "築" and a[4] == "動詞" and a[12] == "キズケ":
		s = ""
	elif a[0] == "今" and a[4] == "接頭詞" and a[12] == "コン":
		s = ""
	elif a[0] == "少し" and a[4] == "形容詞" and a[12] == "スクナシ":
		s = ""
	elif a[0] == "後" and a[4] == "接頭詞" and a[12] == "コー":
		s = ""
	elif a[0] == "居" and a[4] == "名詞" and a[12] == "キョ":
		s = ""
	elif a[0] == "いう" and a[4] == "形容詞" and a[12] == "イー":
		s = ""
	elif a[0] == "暇" and a[4] == "名詞" and a[12] == "イトマ":
		s = ""
	elif a[0] == "継子" and a[4] == "名詞" and a[12] == "ケイシ":
		s = ""
	elif a[0] == "無し" and a[12] == "ムシ" and len(a) == 15:
		s = ""
	elif a[0] == "一塊" and a[12] == "ヒトカタマリ" and len(a) == 15:
		a[11] = a[12] = "イッカイ"
		s = ",".join(a)
	elif a[0] == "白一色" and a[12] == "ハクイッショク" and len(a) == 15:
		a[11] = a[12] = "シロイッショク"
		a.append("シロ 1ショク")
		s = ",".join(a)
	elif a[0] == "こういう" and a[12] == "コーユウ" and len(a) == 15:
		a.append("コー イウ")
		s = ",".join(a)
	elif a[0] == "日本一" and a[12] == "ニッポンイチ" and len(a) == 15:
		a[11] = a[12] = "ニホンイチ"
		a.append("ニホン1")
		s = ",".join(a)
	elif a[0] == "一線" and a[12] == "イッセン" and len(a) == 15:
		a.append("1セン")
		s = ",".join(a)
	elif a[0] == "一双" and a[12] == "イッソー" and len(a) == 15:
		a.append("1ソー")
		s = ",".join(a)
	elif a[0] == "一言一行" and a[12] == "イチゲンイッコー" and len(a) == 15:
		a.append("1ゲン 1コー")
		s = ",".join(a)
	elif a[0] == "一語" and a[12] == "イチゴ" and len(a) == 15:
		a.append("1ゴ")
		s = ",".join(a)
	elif a[0] == "一転機" and a[12] == "イッテンキ" and len(a) == 15:
		a.append("1テンキ")
		s = ",".join(a)
	elif a[0] == "一酸化" and a[12] == "イッサンカ" and len(a) == 15:
		a.append("1サンカ")
		s = ",".join(a)
	elif a[0] == "一子" and a[12] == "イッシ" and len(a) == 15:
		a.append("1シ")
		s = ",".join(a)
	elif a[0] == "もうける" and a[12] == "モウケル" and len(a) == 15:
		a.append("モーケル")
		s = ",".join(a)
	elif a[0] == "一死" and a[12] == "イッシ" and len(a) == 15:
		a.append("1シ")
		s = ",".join(a)
	elif a[0] == "七生" and a[12] == "シチショー" and len(a) == 15:
		a.append("7ショー")
		s = ",".join(a)
	elif a[0] == "一転機" and a[12] == "イチテンキ" and len(a) == 15:
		s = ""
	elif a[0] == "一道" and a[12] == "イチドー" and len(a) == 15:
		a.append("1ドー")
		s = ",".join(a)
	elif a[0] == "一周" and a[12] == "イッシュー" and len(a) == 15:
		a.append("1シュー")
		s = ",".join(a)
	elif a[0] == "一唱三嘆" and a[12] == "イッショーサンタン" and len(a) == 15:
		a.append("1ショー 3タン")
		s = ",".join(a)
	elif a[0] == "一神教" and a[12] == "イッシンキョー" and len(a) == 15:
		a.append("1シンキョー")
		s = ",".join(a)
	elif a[0] == "一世一元" and a[12] == "イッセイイチゲン" and len(a) == 15:
		a.append("1セイ 1ゲン")
		s = ",".join(a)
	elif a[0] == "一石二鳥" and a[12] == "イッセキニチョー" and len(a) == 15:
		a.append("1セキ 2チョー")
		s = ",".join(a)
	elif a[0] == "一白" and a[12] == "イッパク" and len(a) == 15:
		a.append("1パク")
		s = ",".join(a)
	elif a[0] == "一夫一妻" and a[12] == "イップイッサイ" and len(a) == 15:
		a.append("1プ 1サイ")
		s = ",".join(a)
	elif a[0] == "五条" and a[12] == "ゴジョー" and len(a) == 15:
		a.append("5ジョー")
		s = ",".join(a)
	elif a[0] == "一紙半銭" and a[12] == "イッシハンセン" and len(a) == 15:
		a.append("イッシ ハンセン")
		s = ",".join(a)
	elif a[0] == "一所懸命" and a[12] == "イッショケンメイ" and len(a) == 15:
		a.append("イッショ ケンメイ")
		s = ",".join(a)
	elif a[0] == "一生懸命" and a[12] == "イッショーケンメイ" and len(a) == 15:
		a.append("イッショー ケンメイ")
		s = ",".join(a)
	elif a[0] == "一心不乱" and a[12] == "イッシンフラン" and len(a) == 15:
		a.append("イッシン フラン")
		s = ",".join(a)
	elif a[0] == "一進一退" and a[12] == "イッシンイッタイ" and len(a) == 15:
		a.append("イッシン イッタイ")
		s = ",".join(a)
	elif a[0] == "一顰一笑" and a[12] == "イッピンイッショー" and len(a) == 15:
		a.append("イッピン イッショー")
		s = ",".join(a)
	elif a[0] == "命知らず" and a[12] == "イノチシラズ" and len(a) == 15:
		a.append("イノチ シラズ")
		s = ",".join(a)
	elif a[0] == "一分一厘" and a[12] == "イチブイチリン" and len(a) == 15:
		s = ""
	elif a[0] == "一昨昨年" and a[12] == "サキオトトシ":
		a[11] = a[12] = "イッサクサクネン"
		s = ",".join(a)
	elif a[0] == "一昨日" and a[12] == "オトトイ":
		a[11] = a[12] = "イッサクジツ"
		s = ",".join(a)
	elif a[0] == "犬追物" and a[11] == "イヌオウモノ" and a[12] == "イヌオーモノ":
		a[12] = a[11]
		s = ",".join(a)
	elif a[0] == "ううん" and a[12] == "ウーン" and len(a) == 15:
		a.append("ウウン")
		s = ",".join(a)
	elif a[0] == "閏年" and a[12] == "ウルードシ" and len(a) == 15:
		a.append("ウルウドシ")
		s = ",".join(a)
	elif a[0] == "凡河内躬恒" and a[12] == "オーシコーチノミツネ" and len(a) == 15:
		a.append("オオシコーチノ ミツネ")
		s = ",".join(a)
	elif a[0] == "太安万侶" and a[11] == "オオノヤスマロ" and len(a) == 15:
		a.append("オオノ ヤスマロ")
		s = ",".join(a)
	elif a[0] == "上" and a[4] == "名詞" and a[5] == "接尾" and a[11] == "ジョウ" and len(a) == 15:
		s = ""
	elif a[0] == "上" and a[4] == "名詞" and a[5] == "非自立" and a[11] == "ジョウ" and len(a) == 15:
		s = ""
	elif a[0] == "傀儡" and a[12] == "クグツ" and len(a) == 15:
		s = ""
	elif a[0] == "鍛冶" and a[12] == "タンヤ" and len(a) == 15:
		s = ""
	elif a[0] == "自分勝手" and a[12] == "ジブンガッテ" and len(a) == 15:
		s = ""
	elif a[0] == "仮名" and a[12] == "カメイ" and len(a) == 15:
		s = ""
	elif a[0] == "仮名" and a[12] == "ガナ" and len(a) == 15:
		s = ""
	elif a[0] == "桃栗三年柿八年" and a[12] == "モモクリサンネンカキハチネン" and len(a) == 15:
		a.append("モモ クリ 3ネン カキ 8ネン")
		s = ",".join(a)
	elif a[0] == "カリ肥料" and a[12] == "カリヒリョー" and len(a) == 15:
		a.append("カリ ヒリョー")
		s = ",".join(a)
	elif a[0] == "画竜点睛" and a[12] == "ガリョーテンセイ" and len(a) == 15:
		a.append("ガリョー テンセイ")
		s = ",".join(a)
	elif a[0] == "感無量" and a[12] == "カンムリョー" and len(a) == 15:
		a.append("カン ムリョー")
		s = ",".join(a)
	elif a[0] == "寒冷前線" and a[12] == "カンレイゼンセン" and len(a) == 15:
		a.append("カンレイ ゼンセン")
		s = ",".join(a)
	elif a[0] == "乞食" and a[12] == "ホイト" and len(a) == 15:
		s = ""
	elif a[0] == "一人娘" and a[12] == "ヒトリムスメ" and len(a) == 15:
		a.append("ヒトリ ムスメ")
		s = ",".join(a)
	elif a[0] == "絵羽模様" and a[12] == "エバモヨー" and len(a) == 15:
		a.append("エバ モヨー")
		s = ",".join(a)
	elif a[0] == "塩化ナトリウム" and a[12] == "エンカナトリューム" and len(a) == 15:
		a.append("エンカ ナトリウム")
		s = ",".join(a)
	elif a[0] == "朴の木" and a[12] == "ホーノキ" and len(a) == 15:
		a.append("ホオノ キ")
		s = ",".join(a)
	elif a[0] == "松の木" and a[12] == "マツノキ" and len(a) == 15:
		a.append("マツノ キ")
		s = ",".join(a)
	elif a[0] == "気に入る" and a[12] == "キニイル" and len(a) == 15:
		a.append("キニ イル")
		s = ",".join(a)
	elif a[0] == "やる気" and a[12] == "ヤルキ" and len(a) == 15:
		a.append("ヤル キ")
		s = ",".join(a)
	elif a[0] == "一基" and a[12] == "イッキ" and len(a) == 15:
		a.append("1キ")
		s = ",".join(a)
	elif a[0] == "日本書紀" and a[12] == "ニホンショキ" and len(a) == 15:
		a.append("ニホン ショキ")
		s = ",".join(a)
	elif a[0] == "軌を一に" and a[12] == "キヲイツニ" and len(a) == 15:
		a.append("キヲ イツニ")
		s = ",".join(a)
	elif a[0] == "私儀" and a[12] == "ワタクシギ" and len(a) == 15:
		a.append("ワタクシ ギ")
		s = ",".join(a)
	elif a[0] == "第一義" and a[12] == "ダイイチギ" and len(a) == 15:
		a.append("ダイ1ギ")
		s = ",".join(a)
	elif a[0] == "キーパンチャー" and a[12] == "キーパンチャー" and len(a) == 15:
		a.append("キー パンチャー")
		s = ",".join(a)
	elif a[0] == "キーポイント" and a[12] == "キーポイント" and len(a) == 15:
		a.append("キー ポイント")
		s = ",".join(a)
	elif a[0] == "キーホルダー" and a[12] == "キーホルダー" and len(a) == 15:
		a.append("キー ホルダー")
		s = ",".join(a)
	elif a[0] == "マスターキー" and a[12] == "マスターキー" and len(a) == 15:
		a.append("マスター キー")
		s = ",".join(a)
	elif a[0] == "幾何級数" and a[12] == "キカキュースー" and len(a) == 15:
		a.append("キカ キュースー")
		s = ",".join(a)
	elif a[0] == "危機一髪" and a[12] == "キキイッパツ" and len(a) == 15:
		a.append("キキ イッパツ")
		s = ",".join(a)
	elif a[0] == "奇奇怪怪" and a[12] == "キキカイカイ" and len(a) == 15:
		a.append("キキ カイカイ")
		s = ",".join(a)
	elif a[0] == "菊の節句" and a[12] == "キクノセック" and len(a) == 15:
		a.append("キクノ セック")
		s = ",".join(a)
	elif a[0] == "一杯機嫌" and a[12] == "イッパイキゲン" and len(a) == 15:
		a.append("1パイ キゲン")
		s = ",".join(a)
	elif a[0] == "刻み煙草" and a[12] == "キザミタバコ" and len(a) == 15:
		a.append("キザミ タバコ")
		s = ",".join(a)
	elif a[0] == "起死回生" and a[12] == "キシカイセイ" and len(a) == 15:
		a.append("キシ カイセイ")
		s = ",".join(a)
	elif a[0] == "起承転結" and a[12] == "キショーテンケツ" and len(a) == 15:
		a.append("キショー テンケツ")
		s = ",".join(a)
	elif a[0] == "木曽福島" and a[12] == "キソフクシマ" and len(a) == 15:
		a.append("キソ フクシマ")
		s = ",".join(a)
	elif a[0] == "奇想天外" and a[12] == "キソーテンガイ" and len(a) == 15:
		a.append("キソー テンガイ")
		s = ",".join(a)
	elif a[0] == "規則正しい" and a[12] == "キソクタダシイ" and len(a) == 15:
		a.append("キソク タダシイ")
		s = ",".join(a)
	elif a[0] == "着た切り雀" and a[12] == "キタキリスズメ" and len(a) == 15:
		a.append("キタキリ スズメ")
		s = ",".join(a)
	elif a[0] == "キックボクシング" and a[12] == "キックボクシング" and len(a) == 15:
		a.append("キック ボクシング")
		s = ",".join(a)
	elif a[0] == "帝国ホテル" and a[12] == "テイコクホテル" and len(a) == 15:
		a.append("テイコク ホテル")
		s = ",".join(a)
	elif a[0] == "狐の嫁入り" and a[12] == "キツネノヨメイリ" and len(a) == 15:
		a.append("キツネノ ヨメイリ")
		s = ",".join(a)
	elif a[0] == "喜怒哀楽" and a[12] == "キドアイラク" and len(a) == 15:
		a.append("キド アイラク")
		s = ",".join(a)
	elif a[0] == "木戸御免" and a[12] == "キドゴメン" and len(a) == 15:
		a.append("キド ゴメン")
		s = ",".join(a)
	elif a[0] == "昨日今日" and a[12] == "キノーキョー" and len(a) == 15:
		a.append("キノー キョー")
		s = ",".join(a)
	elif a[0] == "甲子" and a[12] == "キノエネ" and len(a) == 15:
		a.append("キノエ ネ")
		s = ",".join(a)
	elif a[0] == "気に入り" and a[12] == "キニイリ" and len(a) == 15:
		a.append("キニ イリ")
		s = ",".join(a)
	elif a[0] == "木の芽" and a[12] == "キノメ" and len(a) == 15:
		a.append("キノ メ")
		s = ",".join(a)
	elif a[0] == "寄付行為" and a[12] == "キフコーイ" and len(a) == 15:
		a.append("キフ コーイ")
		s = ",".join(a)
	elif a[0] == "ギブアンドテイク" and a[12] == "ギブアンドテイク" and len(a) == 15:
		a.append("ギブ アンド テイク")
		s = ",".join(a)
	elif a[0] == "ギフトチェック" and a[12] == "ギフトチェック" and len(a) == 15:
		a.append("ギフト チェック")
		s = ",".join(a)
	elif a[0] == "気味が悪い" and a[12] == "キミガワルイ" and len(a) == 15:
		a.append("キミガ ワルイ")
		s = ",".join(a)
	elif a[0] == "君が代" and a[12] == "キミガヨ" and len(a) == 15:
		a.append("キミガ ヨ")
		s = ",".join(a)
	elif a[0] == "気持ちよい" and a[12] == "キモチヨイ" and len(a) == 15:
		a.append("キモチ ヨイ")
		s = ",".join(a)
	elif a[0] == "三角" and a[12] == "サンカク" and len(a) == 15:
		a.append("3カク")
		s = ",".join(a)
	elif a[0] == "オールスターキャスト" and a[12] == "オールスターキャスト" and len(a) == 15:
		a.append("オール スター キャスト")
		s = ",".join(a)
	elif a[0] == "キャッシュカード" and a[12] == "キャッシュカード" and len(a) == 15:
		a.append("キャッシュ カード")
		s = ",".join(a)
	elif a[0] == "キャッチフレーズ" and a[12] == "キャッチフレーズ" and len(a) == 15:
		a.append("キャッチ フレーズ")
		s = ",".join(a)
	elif a[0] == "キャッチボール" and a[12] == "キャッチボール" and len(a) == 15:
		a.append("キャッチ ボール")
		s = ",".join(a)
	elif a[0] == "キャッチャーボート" and a[12] == "キャッチャーボート" and len(a) == 15:
		a.append("キャッチャー ボート")
		s = ",".join(a)
	elif a[0] == "ナイトキャップ" and a[12] == "ナイトキャップ" and len(a) == 15:
		a.append("ナイト キャップ")
		s = ",".join(a)
	elif a[0] == "アイスキャンデー" and a[12] == "アイスキャンデー" and len(a) == 15:
		a.append("アイス キャンデー")
		s = ",".join(a)
	elif a[0] == "キャンプファイア" and a[12] == "キャンプファイア" and len(a) == 15:
		a.append("キャンプ ファイア")
		s = ",".join(a)
	elif a[0] == "ライトヘビー" and a[12] == "ライトヘビー" and len(a) == 15:
		a.append("ライト ヘビー")
		s = ",".join(a)
	elif a[0] == "万事休す" and a[12] == "バンジキュース" and len(a) == 15:
		a.append("バンジ キュース")
		s = ",".join(a)
	elif a[0] == "旧石器時代" and a[12] == "キューセッキジダイ" and len(a) == 15:
		a.append("キューセッキ ジダイ")
		s = ",".join(a)
	elif a[0] == "急転直下" and a[12] == "キューテンチョッカ" and len(a) == 15:
		a.append("キューテン チョッカ")
		s = ",".join(a)
	elif a[0] == "三拝九拝" and a[12] == "サンパイキューハイ" and len(a) == 15:
		a.append("3パイ 9ハイ")
		s = ",".join(a)
	elif a[0] == "器用貧乏" and a[12] == "キヨービンボー" and len(a) == 15:
		a.append("キヨー ビンボー")
		s = ",".join(a)
	elif a[0] == "狂言回し" and a[12] == "キョーゲンマワシ" and len(a) == 15:
		a.append("キョーゲン マワシ")
		s = ",".join(a)
	elif a[0] == "当たり狂言" and a[12] == "アタリキョーゲン" and len(a) == 15:
		a.append("アタリ キョーゲン")
		s = ",".join(a)
	elif a[0] == "驚天動地" and a[12] == "キョーテンドーチ" and len(a) == 15:
		a.append("キョーテン ドーチ")
		s = ",".join(a)
	elif a[0] == "興味津々" and a[12] == "キョーミシンシン" and len(a) == 15:
		a.append("キョーミ シンシン")
		s = ",".join(a)
	elif a[0] == "虚虚実実" and a[12] == "キョキョジツジツ" and len(a) == 15:
		a.append("キョキョ ジツジツ")
		s = ",".join(a)
	elif a[0] == "挙国一致" and a[12] == "キョコクイッチ" and len(a) == 15:
		a.append("キョコク イッチ")
		s = ",".join(a)
	elif a[0] == "きりきりしゃんと" and a[12] == "キリキリシャント" and len(a) == 15:
		a.append("キリキリ シャント")
		s = ",".join(a)
	elif a[0] == "キリスト教徒" and a[12] == "キリストキョート" and len(a) == 15:
		a.append("キリスト キョート")
		s = ",".join(a)
	elif a[0] == "桐一葉" and a[12] == "キリヒトハ" and len(a) == 15:
		a.append("キリ ヒトハ")
		s = ",".join(a)
	elif a[0] == "きりりしゃんと" and a[12] == "キリリシャント" and len(a) == 15:
		a.append("キリリ シャント")
		s = ",".join(a)
	elif a[0] == "極まりない" and a[12] == "キワマリナイ" and len(a) == 15:
		a.append("キワマリ ナイ")
		s = ",".join(a)
	elif a[0] == "感極まっ" and a[12] == "カンキワマッ" and len(a) == 15:
		a.append("カン キワマッ")
		s = ",".join(a)
	elif a[0] == "金一封" and a[12] == "キンイップー" and len(a) == 15:
		a.append("キン イップー")
		s = ",".join(a)
	elif a[0] == "金科玉条" and a[12] == "キンカギョクジョー" and len(a) == 15:
		a.append("キンカ ギョクジョー")
		s = ",".join(a)
	elif a[0] == "欣喜雀躍" and a[12] == "キンキジャクヤク" and len(a) == 15:
		a.append("キンキ ジャクヤク")
		s = ",".join(a)
	elif a[0] == "キングコング" and a[12] == "キングコング" and len(a) == 15:
		a.append("キング コング")
		s = ",".join(a)
	elif a[0] == "近郷近在" and a[12] == "キンゴーキンザイ" and len(a) == 15:
		a.append("キンゴー キンザイ")
		s = ",".join(a)
	elif a[0] == "日本銀行" and a[12] == "ニッポンギンコー" and len(a) == 15:
		a.append("ニッポン ギンコー")
		s = ",".join(a)
	elif a[0] == "筋ジストロフィー" and a[12] == "キンジストロフィー" and len(a) == 15:
		a.append("キン ジストロフィー")
		s = ",".join(a)
	elif a[0] == "近所合壁" and a[12] == "キンジョガッペキ" and len(a) == 15:
		a.append("キンジョ ガッペキ")
		s = ",".join(a)
	elif a[0] == "琴の琴" and a[12] == "キンノコト" and len(a) == 15:
		a.append("キンノ コト")
		s = ",".join(a)
	elif a[0] == "吟遊詩人" and a[12] == "ギンユーシジン" and len(a) == 15:
		a.append("ギンユー シジン")
		s = ",".join(a)
	elif a[0] == "金襴緞子" and a[12] == "キンランドンス" and len(a) == 15:
		a.append("キンラン ドンス")
		s = ",".join(a)
	elif a[0] == "一朝" and a[12] == "イッチョー" and len(a) == 15:
		a.append("1チョー")
		s = ",".join(a)
	elif a[0] == "三面" and a[12] == "サンメン" and len(a) == 15:
		a.append("3メン")
		s = ",".join(a)
	elif a[0] == "十二宮" and a[12] == "ジューニキュー" and len(a) == 15:
		a.append("12キュー")
		s = ",".join(a)
	elif a[0] == "九紫" and a[12] == "キューシ" and len(a) == 15:
		a.append("9シ")
		s = ",".join(a)
	elif a[0] == "九星" and a[12] == "キューセイ" and len(a) == 15:
		a.append("9セイ")
		s = ",".join(a)
	elif a[0] == "三碧" and a[12] == "サンペキ" and len(a) == 15:
		a.append("3ペキ")
		s = ",".join(a)
	elif a[0] == "四緑" and a[12] == "シロク" and len(a) == 15:
		a.append("4ロク")
		s = ",".join(a)
	elif a[0] == "五黄" and a[12] == "ゴオー" and len(a) == 15:
		a.append("5オー")
		s = ",".join(a)
	elif a[0] == "六白" and a[12] == "ロッパク" and len(a) == 15:
		a.append("6パク")
		s = ",".join(a)
	elif a[0] == "七赤" and a[12] == "シチセキ" and len(a) == 15:
		a.append("7セキ")
		s = ",".join(a)
	elif a[0] == "八白" and a[12] == "ハッパク" and len(a) == 15:
		a.append("8パク")
		s = ",".join(a)
	elif a[0] == "九紫" and a[12] == "キューシ" and len(a) == 15:
		a.append("9シ")
		s = ",".join(a)
	elif a[0] == "九族" and a[12] == "キューゾク" and len(a) == 15:
		a.append("9ゾク")
		s = ",".join(a)
	elif a[0] == "聞き捨て" and a[12] == "キキステ" and len(a) == 15:
		s = ""
	elif a[0] == "米ドル" and a[12] == "アメリカドル" and len(a) == 15:
		s = ""
	elif a[0] == "米" and a[12] == "メートル" and len(a) == 15:
		s = ""
	elif a[0] == "っていう" and a[12] == "ッテユウ" and len(a) == 15:
		a.append("ッテ イウ")
		s = ",".join(a)
	elif a[0] == "どういう" and a[12] == "ドーユウ" and len(a) == 15:
		a.append("ドウ イウ")
		s = ",".join(a)
	elif a[0] == "とかいう" and a[12] == "トカユウ" and len(a) == 15:
		a.append("トカ イウ")
		s = ",".join(a)
	elif a[0] == "ａ" and a[12] == "アール" and len(a) == 15:
		s = ""
	elif a[0] == "通帳" and a[12] == "カヨイチョー" and len(a) == 15:
		s = ""
	elif a[0] == "指原" and a[12] == "サスハラ" and len(a) == 15:
		# https://github.com/nvdajp/nvdajpmiscdep/issues/64
		s = ""
	elif a[0] == "松坂" and a[12] == "マツサカ" and len(a) == 15:
		# https://github.com/nvdajp/nvdajpmiscdep/issues/64
		s = ""
	elif a[0] == "菅田" and a[12] == "スゲタ" and len(a) == 15:
		# https://github.com/nvdajp/nvdajpmiscdep/issues/64
		s = ""
	elif a[0] == "菅田" and a[12] == "スガタ" and len(a) == 15:
		# https://github.com/nvdajp/nvdajpmiscdep/issues/64
		s = ""
	elif a[0] == "菅田" and a[12] == "スガダ" and len(a) == 15:
		# https://github.com/nvdajp/nvdajpmiscdep/issues/64
		s = ""
	elif a[0] == "真麻" and a[12] == "マサ" and len(a) == 15:
		# https://github.com/nvdajp/nvdajpmiscdep/issues/64
		s = ""
	elif a[0] == "点点" and a[12] == "チョボチョボ" and len(a) == 15:
		# https://github.com/nvdajp/nvdajp/issues/294
		s = ""
	elif a[0] == "ｏｐｅｎ＿ｊｔａｌｋ" and a[12] == "オープンジェートーク" and len(a) == 15:
		# https://github.com/nvdajp/nvdajpmiscdep/issues/66
		a.append("⠠⠦open_jtalk⠠⠴")
		s = ",".join(a)
	elif a[0] == "おうち" and a[12] == "オーチ" and len(a) == 15:
		# https://github.com/nvdajp/nvdajpmiscdep/issues/56
		a.append("オウチ")
		s = ",".join(a)
	elif a[0] == "既" and a[12] == "スンデ" and len(a) == 15:
		# https://github.com/nvdajp/nvdajpmiscdep/issues/69
		s = ""
	elif a[0] == "必須" and a[12] == "ヒッス":
		# https://github.com/nvdajp/nvdajp/issues/125
		a[12] = a[12] = "ヒッスー"
		a[13] = "0/4"
		a.append("ヒッス")
		s = ",".join(a)
	elif a[0] == "あっという間" and a[12] == "アットユウマ" and len(a) == 15:
		# https://github.com/nvdajp/nvdajp/issues/231
		a.append("アット イウ マ")
		s = ",".join(a)
	elif RE_NUMBERS.match(a[0]) and len(a) == 15:
		# https://github.com/nvdajp/nvdajpmiscdep/issues/70
		s = ""
	elif is_alpha_jp_mixed(a[0]):
		# print a[0]
		s = ""
	return s
