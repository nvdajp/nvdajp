# custom_dic_maker.py for nvdajp_jtalk
# -*- coding: utf-8 -*-
# since 2011-01-19 by Takuya Nishimoto

OUT_FILE = "nvdajp-custom-dic.csv"

import sys

open_file = lambda name, mode, encoding: open(name, mode, encoding=encoding)


from pathlib import Path


jdic = [
	# first item should use fullshape(zenkaku) charactors
	["読み込み中", "ヨミコミチュー", "2/6"],
	# ['一行', 		'イチギョー',			"2/4"],
	# ['１行', 		'イチギョー',			"2/4"],
	# ['１行下', 	'イチギョーシタ',		"2/6"],
	# ['１行上', 	'イチギョーウエ',		"2/6"],
	# ['２行', 		'ニギョー',			"1/3"],
	# ['３行', 		'サンギョー',			"1/4"],
	["行", "ギョー", "1/2", 1000, "名詞,接尾,助数詞,*,*,*"],
	["行上", "ギョーウエ", "1/4", 1000, "名詞,接尾,助数詞,*,*,*"],
	["行下", "ギョーシタ", "1/4", 1000, "名詞,接尾,助数詞,*,*,*"],
	["５０音順", "ゴジューオンジュン", "0/7", None, None, "50オンジュン"],
	["空行", "クーギョー", "0/4"],
	["行末", "ギョーマツ", "0/4"],
	["複数行", "フクスーギョー", "3/6"],
	["現在行", "ゲンザイギョー", "3/6"],
	["最上行", "サイジョーギョー", "3/6"],
	["行操作", "ギョーソーサ", "1/5"],
	["誤判定", "ゴハンテイ", "2/5"],
	["表計算", "ヒョーケイサン", "3/5"],
	["空要素", "カラヨーソ", "3/5"],
	["拡張子", "カクチョーシ", "3/5"],
	["親オブジェクト", "オヤオブジェクト", "3/7"],
	["小文字", "コモジ", "0/3"],
	{"text": "大文字", "braille": "オオモジ", "speech": "オーモジ", "accent": "0/4"},
	["ニコ生", "ニコナマ", "0/4"],
	["スリーマイル島原発", "スリーマイルトーゲンパツ"],
	["孫正義", "ソンマサヨシ", "4/6", None, None, "ソン マサヨシ"],
	["池田信夫", "イケダノブオ", "0/6"],
	["方々", "カタガタ", "2/4"],
	["当分の間", "トーブンノアイダ", "0/8"],
	["中通り", "ナカドーリ", "3/5"],
	["中", "チュー", "1/2", 5000],
	["中の人", "ナカノヒト", "1/5"],
	["中程度", "チューテード", "3/5"],
	["各基", "カクキ", "1/3"],
	["高", "コー", "1/2", 5000],
	["県立高", "ケンリツコー", "0/6"],
	["業務", "ギョーム", "1/3"],
	["値", "アタイ", "0/3"],
	["２４時間", "ニジューヨジカン", "1/7", None, None, "24 ジカン"],
	["明朝", "ミンチョー", "1/4"],
	["障がい", "ショーガイ", "0/4"],
	["蓮舫", "レンホー", "1/4"],
	["既読", "キドク", "0/3"],
	["大嘘", "オーウソ", "0/4"],
	["１人", "ヒトリ", "2/3"],
	["一人ひとり", "ヒトリヒトリ", "0/6"],
	["日中", "ニッチュー", "3/4"],
	["次", "ツギ", "2/2", 5000],
	["他人事", "タニンゴト", "0/5"],
	["セブン―イレブン", "セブンイレブン", "5/7"],
	["東国原", "ヒガシコクバル", "5/7"],
	["中越", "チューエツ", "1/4"],
	["発災", "ハッサイ", "0/4"],
	["その上", "ソノウエ", "0/4"],
	["時期", "ジキ", "1/2"],
	["扱い", "アツカイ", "0/4"],
	["停波", "テイハ", "0/3"],
	["建屋", "タテヤ", "2/3"],
	["なう", "ナウ", "1/2"],
	["被り", "カブリ", "0/3"],
	["寺田寅彦", "テラダトラヒコ", "0/7"],
	["橋下", "ハシモト", "0/4"],
	["フレッツ光", "フレッツヒカリ", "2/7"],
	["選択行", "センタクギョー", "0/6"],
	["ベクレル", "ベクレル", "1/4", 1000, "名詞,接尾,助数詞,*,*,*"],
	["三毛猫", "ミケネコ", "0/4"],
	["数多く", "カズオオク", "1/5"],
	["繁体字", "ハンタイジ", "3/5"],
	["上矢印", "ウエヤジルシ", "4/6"],
	["下矢印", "シタヤジルシ", "4/6"],
	["大見出し", "オオミダシ", "3/5"],
	["前景色", "ゼンケイショク", "3/6"],
	["八ッ場", "ヤンバ", "0/3"],
	["梅雨前線", "バイウゼンセン", "4/7", None, None, "バイウ ゼンセン"],
	["１都５県", "イットゴケン"],
	["１都６県", "イットロッケン"],
	["昔々", "ムカシムカシ", "0/6", None, None, "ムカシ ムカシ"],
	["材販", "ザイハン", "0/4"],
	["盲ろう者", "モーローシャ", "3/5"],
	["えき", "エキ", "1/2"],
	["はは", "ハハ", "1/2"],
	["万国旗", "バンコクキ", "3/5"],
	["多角形", "タカクケイ", "2/5"],
	["高脂血症", "コーシケツショー", "0/7"],
	["買うた", "コータ", "1/3"],
	["縫うた", "ヌータ", "0/3"],
	["透徹る", "スキトオル", "3/5"],
	["八日", "ヨーカ", "0/3"],
	["何百", "ナンビャク", "1/4"],
	["十日", "トオカ", "0/3"],
	["ちゅうりっぷ", "チューリップ", "1/5"],
	["きゃりーぱみゅぱみゅ", "キャリーパミュパミュ", "4/7"],
	["為おおせる", "シオオセル", "4/5"],
	["砂利道", "ジャリミチ", "2/4"],
	["少しずつ", "スコシズツ", "4/5"],
	["まづ", "マズ", "1/2"],
	["一つづつ", "ヒトツズツ", "4/5"],
	["大きう", "オオキュー", "1/4"],
	["うれしう", "ウレシュー", "2/4"],
	["みづうみ", "ミズウミ", "2/4"],
	["もみぢ", "モミジ", "1/3"],
	["ヴァイオリン", "バイオリン", "0/5", None, None, "ヴァイオリン"],
	["ヴィタミン", "ビタミン", "1/4", None, None, "ヴィタミン"],
	["ラヂオ", "ラジオ", "1/3"],
	["ヂャケット", "ジャケット", "1/4"],
	["ウヰスキー", "ウイスキー", "1/5"],
	["スヰフト", "スイフト", "1/4"],
	["ヱルテル", "ウェルテル", "1/4"],
	["ヲルポール", "ウォルポール", "1/5"],
	["ヘリコプタア", "ヘリコプター", "1/6"],
	["ちゅうりっぷ", "チューリップ", "1/5"],
	["おみやぁさん", "オミャアサン", "2/5"],
	["先生ぇさまぁ", "センセエサマア", "0/7"],
	["おとゥ", "オトー", "2/3"],
	["ヂェスチャー", "ジェスチャー", "1/3"],
	["ヒァーッ", "ヒャーッ", "1/3"],
	["東井", "トーイ", "1/3"],
	["みやこをどり", "ミヤコオドリ", "4/6", None, None, "ミヤコ オドリ"],
	["をりがみ", "オリガミ", "2/4"],
	["キャレット", "キャレット", "1/4"],
	["ヱビスビール", "エビスビール", "4/6", None, None, "エビス ビール"],
	["十数人", "ジュースーニン", "3/6", None, None, "10スーニン"],
	["いらっしゃい", "イラッシャイ", "2/5"],
	["ごめんください", "ゴメンクダサイ", "0/7", None, None, "ゴメン クダサイ"],
	["おはようございます", "オハヨーゴザイマス", "0/9", None, None, "オハヨー ゴザイマス"],
	["嘘みたい", "ウソミタイ", "1/5"],
	["満遍", "マンベン", "0/4"],
	["形なし", "カタナシ", "0/4"],
	["わかりっこ", "ワカリッコ", "3/5"],
	["言わしむれば", "イワシムレバ", "4/6"],
	["一人", "ヒトリ", "2/3"],
	["二人", "フタリ", "0/3"],
	["於て", "オイテ", "1/3"],
	["この期", "コノゴ", "0/3"],
	["その節", "ソノセツ", "3/4"],
	["二十日", "ハツカ", "0/3"],
	["二十歳", "ハタチ", "1/3"],
	["３泊４日", "サンパクヨッカ", "1/7", None, None, "3パク ヨッカ"],
	["二百十日", "ニヒャクトーカ", "0/6", None, None, "2ヒャク トオカ"],
	["一日", "ツイタチ", "0/4"],
	["十日", "トーカ", "0/3", 100, None, "トオカ"],
	["十四日", "ジューヨッカ", "1/5", None, None, "14カ"],
	["二十四日", "ニジューヨッカ", "1/6", None, None, "24カ"],
	["三三七拍子", "サンサンナナビョーシ", "0/9", None, None, "3⠼3⠼7ビョーシ"],
	["三十三間堂", "サンジューサンゲンドー", "1/10", None, None, "33ゲンドー"],
	["フレンドシップ", "フレンドシップ", "5/7"],
	["我等", "ワレラ", "1/3"],
	["相たずさえる", "アイタズサエル", "1/7"],
	["各方面", "カクホーメン", "1/6", None, None, "カク ホーメン"],
	["旧陸軍", "キューリクグン", "1/6", None, None, "キュー リクグン"],
	["山や川", "ヤマヤカワ", "2/5", None, None, "ヤマヤ カワ"],
	["山や川等", "ヤマヤカワナド", "2/7", -1000, "名詞,一般,*,*,*,*", "ヤマヤ カワナド"],
	["相対する", "アイタイスル"],
	["相たずさえて", "アイタズサエテ"],
	["相整う", "アイトトノウ"],
	["相憐れむ", "アイアワレム"],
	["木立の間", "コダチノアイダ", None, None, None, "コダチノ アイダ"],
	["開いた口", "アイタクチ", None, None, None, "アイタ クチ"],
	["相無く", "アイナク"],
	["お生憎様", "オアイニクサマ"],
	["開かずの間", "アカズノマ", None, None, None, "アカズノ マ"],
	["不開の間", "アカズノマ", None, None, None, "アカズノ マ"],
	["山田県主", "ヤマダノアガタヌシ", None, None, None, "ヤマダノ アガタヌシ"],
	["暁闇", "アカツキヤミ"],
	["上がり降り", "アガリオリ"],
	["四条上ル", "シジョーアガル", "1/", None, None, "4ジョー アガル"],
	["秋津国", "アキツクニ"],
	["現つ神", "アキツカミ"],
	["阿Ｑ正伝", "アキューセイデン", "1/7", None, None, "アQ セイデン"],
	["悪源太", "アクゲンタ"],
	["明くる朝", "アクルアサ", None, None, None, "アクル アサ"],
	["明くる年", "アクルトシ", None, None, None, "アクル トシ"],
	["明の星", "アケノホシ", None, None, None, "アケノ ホシ"],
	["麻布十番", "アザブジューバン", None, None, None, "アザブ ジューバン"],
	["男漁り", "オトコアサリ", None, None, None, "オトコ アサリ"],
	["古本漁り", "フルホンアサリ", None, None, None, "フルホン アサリ"],
	["足の甲", "アシノコー", None, None, None, "アシノ コー"],
	["日の足", "ヒノアシ"],
	{"text": "醤油味", "speech": "ショーユアジ", "accent": "3/5", "braille": "ショーユ アジ"},
	{"text": "唯唯諾諾", "speech": "イイダクダク", "accent": "1/6", "braille": "イイ ダクダク"},
	{"text": "難度", "speech": "ナンド", "accent": "1/3", "braille": "ナンド"},
	{"text": "言い甲斐", "braille": "イイガイ"},
	{"text": "いい事尽くめ", "braille": "イイコトズクメ"},
	{"text": "良いとこ取り", "braille": "イイトコドリ"},
	{"text": "いいとこ取り", "braille": "イイトコドリ"},
	{"text": "言う側", "braille": "イウ ソバ"},
	{"text": "３国同盟", "speech": "サンゴクドーメイ", "braille": "3ゴク ドーメイ"},
	{"text": "家屋敷", "braille": "イエヤシキ"},
	{"text": "イエローストーン川", "braille": "イエロー ストーンガワ"},
	{"text": "陰イオン", "braille": "インイオン"},
	{"text": "幾ら何でも", "braille": "イクラ ナンデモ"},
	{"text": "不忍池", "braille": "シノバズノ イケ"},
	{"text": "行け行けどんどん", "braille": "イケ イケ ドンドン"},
	{"text": "行け行けギャル", "braille": "イケイケ ギャル"},
	{"text": "伊豆七島", "braille": "イズ 7トー", "speech": "イズシチトウ"},
	{"text": "伊勢参", "braille": "イセ マイリ"},
	{"text": "至る処人で", "braille": "イタル トコロ ヒトデ"},
	{"text": "至れり尽くせり", "braille": "イタレリ ツクセリ"},
	{"text": "門前市をなす", "braille": "モンゼン イチヲ ナス"},
	{"text": "ほおずき市", "braille": "ホオズキイチ"},
	{"text": "一握の砂", "braille": "イチアクノ スナ"},
	{"text": "正一位", "braille": "ショー1イ", "speech": "ショーイチイ"},
	{"text": "従一位", "braille": "ジュ1イ", "speech": "ジュイチイ"},
	{"text": "一一文句", "braille": "イチイチ モンク"},
	{"text": "一か八か", "braille": "イチカ バチカ"},
	{"text": "武田方", "braille": "タケダガタ"},
	{"text": "一期の不覚", "braille": "イチゴノ フカク"},
	{"text": "一言一句", "braille": "1ゴン 1ク", "speech": "イチゴンイック"},
	{"text": "一言の下", "braille": "1ゴンノ モト", "speech": "イチゴンノモト"},
	{"text": "一日三秋", "braille": "1ジツ 3シュー", "speech": "イチジツサンシュー"},
	{"text": "一日の長", "braille": "1ジツノ チョー", "speech": "イチジツノチョー"},
	# 複合語として優先させるためコストを下げる
	{
		"text": "一日中",
		"braille": "1ニチジュー",
		"speech": "イチニチジュー",
		"cost": -1000,
		"pos": "名詞,一般,*,*,*,*",
	},
	{
		"text": "一日増し",
		"braille": "1ニチマシ",
		"speech": "イチニチマシ",
		"cost": -2000,
		"pos": "名詞,一般,*,*,*,*",
	},
	{"text": "一割一分", "braille": "1ワリ 1ブ", "speech": "イチワリイチブ"},
	{"text": "一番星", "braille": "1バンボシ", "speech": "イチバンボシ"},
	{"text": "一木一草", "braille": "1ボク 1ソー", "speech": "イチボクイッソー"},
	{"text": "一木造り", "braille": "1ボクヅクリ", "speech": "イチボクヅクリ"},
	{
		"text": "一念岩",
		"braille": "イチネン イワ",
		"speech": "イチネンイワ",
		"cost": -1000,
		"pos": "名詞,一般,*,*,*,*",
	},
	{"text": "一谷嫩軍記", "braille": "イチノタニ フタバ グンキ"},
	{"text": "一分の隙", "braille": "イチブノ スキ"},
	{"text": "一分一厘狂い", "braille": "1ブ 1リン クルイ", "speech": "イチブイチリンクルイ"},
	{"text": "一文きなか", "braille": "1モン キナカ", "speech": "イチモンキナカ"},
	{"text": "一門一党", "braille": "1モン 1トー", "speech": "イチモンイットー"},
	{"text": "一六勝負", "braille": "1⠼6 ショーブ", "speech": "イチロクショーブ"},
	{"text": "一目も二目", "braille": "1モクモ 2モク", "speech": "イチモクモニモク"},
	{"text": "役者が一枚上", "braille": "ヤクシャガ イチマイ ウエ"},
	{"text": "相通じる", "braille": "アイツージル"},
	{"text": "お琴", "braille": "オコト"},
	{"text": "一文無し", "braille": "イチモンナシ"},
	{"text": "横一文字", "braille": "ヨコ イチモンジ"},
	{"text": "一文字せせり", "braille": "イチモンジ セセリ"},
	{"text": "一六タルト", "braille": "イチロク タルト"},
	{"text": "いつ何時", "braille": "イツ ナンドキ"},
	{"text": "御一行様", "braille": "ゴイッコーサマ"},
	{"text": "一昨三日", "braille": "イッサク ミッカ"},
	{"text": "一生涯", "braille": "イッショーガイ"},
	{"text": "一寸の虫にも五分", "braille": "1スンノ ムシニモ 5ブ", "speech": "イッスンノムシニモゴブ"},
	{"text": "親子は一世", "braille": "オヤコワ 1セ", "speech": "オヤコワイッセ"},
	{"text": "チャールズ一世", "braille": "チャールズ 1セイ", "speech": "チャールズイッセイ"},
	{"text": "一刹那", "braille": "イッセツナ"},
	{"text": "一隊", "braille": "イッタイ"},
	{"text": "言って退ける", "braille": "イッテ ノケル"},
	{"text": "罪一等", "braille": "ツミ 1トー", "speech": "ツミイットー"},
	{"text": "一党一派", "braille": "1トー 1パ", "speech": "イットーイッパ"},
	{"text": "何時何時", "braille": "イツ ナンドキ"},
	{"text": "勝敗は一に時", "braille": "ショーハイワ イツニ トキ"},
	{"text": "何時になく", "braille": "イツニ ナク"},
	{"text": "一波動けば万波", "braille": "1パ ウゴケバ バンパ", "speech": "イッパウゴケババンパ"},
	{"text": "一敗", "braille": "1パイ", "speech": "イッパイ", "cost": -1000, "pos": "名詞,一般,*,*,*,*"},
	{"text": "一筆画", "braille": "1ピツガ", "speech": "イッピツガ"},
	{"text": "一本背負い", "braille": "1ポンゼオイ", "speech": "イッポンゼオイ"},
	{"text": "一本道", "braille": "1ポンミチ", "speech": "イッポンミチ"},
	{"text": "異な事", "braille": "イナ コト"},
	{"text": "異なもの", "braille": "イナ モノ"},
	{"text": "大犬の陰嚢", "braille": "オオ イヌノ フグリ"},
	{"text": "乱暴者", "braille": "ランボーモノ"},
	{"text": "姑いびり", "braille": "シュートメ イビリ"},
	{"text": "居待ち月", "braille": "イマチヅキ"},
	{"text": "今際の際", "braille": "イマワノ キワ"},
	{"text": "妹背山婦女庭訓", "braille": "イモセヤマ オンナ テイキン"},
	{"text": "蘇我越智娘", "braille": "ソガノ オチノ イラツメ"},
	{"text": "坂上大嬢", "braille": "サカノウエノ オオイラツメ"},
	{"text": "彼岸の入り", "braille": "ヒガンノ イリ"},
	{"text": "入り小作", "braille": "イリコサク"},
	{"text": "東入", "braille": "ヒガシ イル"},
	{"text": "祝伸ばし", "braille": "イワイ ノバシ"},
	{"text": "卒業祝", "braille": "ソツギョー イワイ"},
	{"text": "木屋町", "braille": "キヤマチ"},
	{"text": "源朝臣頼政", "braille": "ミナモトノ アソン ヨリマサ", "accent": "6/"},
	{"text": "東漢直駒", "braille": "ヤマトノ アヤノ アタイノ コマ"},
	{"text": "兄貴風", "braille": "アニキカゼ", "accent": "3/5"},
	{"text": "触読", "braille": "ショクドク", "accent": "0/4"},
	{"text": "触手話", "braille": "ショクシュワ", "accent": "3/4"},
	{"text": "触読式時計", "braille": "ショクドクシキ トケイ", "accent": "0/9"},
	{"text": "盲ろう", "braille": "モーロー", "accent": "0/4"},
	{"text": "泉質", "braille": "センシツ"},
	{"text": "硫酸塩", "braille": "リューサンエン"},
	{"text": "硫酸塩泉", "braille": "リューサンエンセン"},
	{"text": "塩化物泉", "braille": "エンカブッセン"},
	{"text": "泉温", "braille": "センオン"},
	{"text": "冷鉱泉", "braille": "レイコーセン"},
	{"text": "微温泉", "braille": "ビオンセン"},
	{"text": "療養泉", "braille": "リョーヨーセン"},
	{"text": "低張性", "braille": "テイチョーセイ"},
	{"text": "等張性", "braille": "トーチョーセイ"},
	{"text": "高張性", "braille": "コーチョーセイ"},
	{"text": "酸性泉", "braille": "サンセイセン"},
	{"text": "放射能泉", "braille": "ホーシャノーセン"},
	{"text": "次章", "braille": "ジショー"},
	{"text": "更衣室", "braille": "コーイシツ"},
	{"text": "盗撮", "braille": "トーサツ"},
	{"text": "所により", "braille": "トコロニ ヨリ"},
	{"text": "編集人", "braille": "ヘンシューニン"},
	{"text": "発行人", "braille": "ハッコーニン"},
	{"text": "受取人", "braille": "ウケトリニン"},
	{"text": "配達人", "braille": "ハイタツニン"},
	{"text": "管理人", "braille": "カンリニン"},
	{"text": "下請人", "braille": "シタウケニン"},
	{
		"text": "名ｓｐｅｅｃｈ集",
		"speech": "メイスピーチシュー",
		"accent": "4/8",
		"braille": "メイspeechシュー",
		"cost": 1000,
	},
	{"text": "一人当り", "braille": "ヒトリアタリ", "accent": "4/6"},
	{"text": "天照大神", "braille": "アマテラス オオミカミ"},
	{"text": "天の岩戸", "braille": "アマノ イワト"},
	{"text": "天香具山", "braille": "アマノ カグヤマ"},
	{"text": "天の羽衣", "braille": "アマノ ハゴロモ"},
	{"text": "天の原", "braille": "アマノハラ"},
	{"text": "天鈿女命", "braille": "アメノ ウズメノ ミコト"},
	{"text": "水争", "braille": "ミズアラソイ"},
	{"text": "蟻の塔草", "braille": "アリノトーグサ"},
	{"text": "有りの儘", "braille": "アリノママ"},
	{"text": "有りの実", "braille": "アリノミ"},
	{"text": "栄えある", "braille": "ハエ アル"},
	{"text": "或る", "braille": "アル"},
	{"text": "或る程度", "braille": "アル テイド"},
	{"text": "有るが儘", "braille": "アルガ ママ"},
	{"text": "アルカリ泉", "braille": "アルカリセン"},
	{"text": "合わせ鏡", "braille": "アワセ カガミ"},
	{"text": "鬘合わせ", "braille": "カツラ アワセ"},
	{"text": "暗順応", "braille": "アンジュンノー"},
	{"text": "大慌て", "braille": "オオアワテ", "accent": "3/5"},
	{"text": "大旦那", "braille": "オオダンナ", "accent": "3/5"},
	{"text": "大人数", "braille": "オオニンズー", "accent": "3/6"},
	{"text": "付点", "speech": "フテン", "accent": "0/3"},
	{
		"text": "有り難う",
		"speech": "アリガトー",
		"braille": "アリガトー",
		"accent": "2/5",
		"cost": 1000,
		"pos": "感動詞,*,*,*,*,*",
	},
	{
		"text": "あいうえお",
		"speech": "アイウエオ",
		"braille": "アイウエオ",
		"accent": "0/5",
		"cost": 1000,
		"pos": "感動詞,*,*,*,*,*",
	},
	{
		"text": "かきくけこ",
		"speech": "カキクケコ",
		"braille": "カキクケコ",
		"accent": "0/5",
		"cost": 1000,
		"pos": "感動詞,*,*,*,*,*",
	},
	{"text": "テンカイ", "braille": "テンカイ"},
	{
		"text": "足手纏い",
		"pos": "名詞,形容動詞語幹,*,*,*,*",
		"speech": "アシデマトイ",
		"accent": "4/6",
		"braille": "アシデ マトイ",
	},
	{
		"text": "新家",
		"pos": "名詞,固有名詞,人名,姓,*,*",
		"speech": "シンケ",
		"accent": "1/3",
	},
	{
		"text": "京丹後",
		"pos": "名詞,固有名詞,地域,一般,*,*",
		"speech": "キョータンゴ",
		"accent": "3/5",
	},
	{
		"text": "インストーラー",
		"speech": "インストーラー",
		"accent": "4/7",
	},
	{
		"text": "トーキング",
		"speech": "トーキング",
		"accent": "1/5",
	},
	# nvdajp ticket34973: 曜日の括弧表記（コストを低く設定して優先）
	{
		"text": "（日）",
		"speech": "（ニチ）",
		"braille": "（ニチ）",
		"accent": "1/2",
		"cost": -1000,
		"pos": "名詞,一般,*,*,*,*",
	},
	{
		"text": "（月）",
		"speech": "（ゲツ）",
		"braille": "（ゲツ）",
		"accent": "1/2",
		"cost": -1000,
		"pos": "名詞,一般,*,*,*,*",
	},
	{
		"text": "（火）",
		"speech": "（カ）",
		"braille": "（カ）",
		"accent": "1/1",
		"cost": -1000,
		"pos": "名詞,一般,*,*,*,*",
	},
	{
		"text": "（水）",
		"speech": "（スイ）",
		"braille": "（スイ）",
		"accent": "1/2",
		"cost": -1000,
		"pos": "名詞,一般,*,*,*,*",
	},
	{
		"text": "（木）",
		"speech": "（モク）",
		"braille": "（モク）",
		"accent": "1/2",
		"cost": -1000,
		"pos": "名詞,一般,*,*,*,*",
	},
	{
		"text": "おおくり",
		"speech": "オオクリ",
		"braille": "オオクリ",
		"accent": "2/4",
		"pos": "名詞,一般,*,*,*,*",
	},
	{
		"text": "みぞう",
		"speech": "ミゾウ",
		"braille": "ミゾウ",
		"accent": "0/3",
		"pos": "名詞,一般,*,*,*,*",
	},
	{
		"text": "うるうどし",
		"speech": "ウルウドシ",
		"braille": "ウルウドシ",
		"accent": "2/5",
		"pos": "名詞,一般,*,*,*,*",
	},
	# 	['きゃ', 'キャ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['きゅ', 'キュ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['きょ', 'キョ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['しゃ', 'シャ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['しゅ', 'シュ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['しょ', 'ショ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['ちゃ', 'チャ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['ちゅ', 'チュ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['ちょ', 'チョ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['にゃ', 'ニャ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['にゅ', 'ニュ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['にょ', 'ニョ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['ひゃ', 'ヒャ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['ひゅ', 'ヒュ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['ひょ', 'ヒョ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['みゃ', 'ミャ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['みゅ', 'ミュ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['みょ', 'ミョ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['りゃ', 'リャ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['りゅ', 'リュ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['りょ', 'リョ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['くゎ', 'クワ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['ぎゅ', 'ギュ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['ぎょ', 'ギョ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['じゃ', 'ジャ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['じゅ', 'ジュ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['じょ', 'ジョ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['ぢゃ', 'ジャ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['ぢゅ', 'ジュ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['ぢょ', 'ジョ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['びゃ', 'ビャ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['びゅ', 'ビュ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['びょ', 'ビョ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['ぴゃ', 'ピャ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['ぴゅ', 'ピュ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['ぴょ', 'ピョ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	# 	['ぐゎ', 'グワ',		"1/1", 		15000,		"記号,一般,*,*,*,*"],
	{"text": "ト゚", "speech": "ト"},  # U+309a
	{"text": "ト　゚", "speech": "ト"},  # U+309a
	# {'text':'ト゜', 'speech':'ト'}, # U+309c
	# {'text':'トﾟ', 'speech':'ト'}, # U+ff9f
	# 同の字点
	# 々	3005	[クリカエシキゴー]	オドリジ
	{"text": "呉々", "braille": "クレグレ", "accent": "3/4"},
	{"text": "小々々支川", "braille": "ショーショーショーシセン"},
	{"text": "結婚式々場", "braille": "ケッコンシキ シキジョー"},
	# 片仮名繰り返し記号
	# ヽ	30fd	[カタカナクリカエシ]	クリカエシ
	# ヾ	30fe	[カタカナダクテンクリカエシ]	クリカエシ ダクテン
	{"text": "スヽメ", "braille": "ススメ"},
	# 仝	4edd	[ドージョー]	ドージョー
	{"text": "仝", "braille": "ドージョー", "cost": 5000},
	# ノノ字点（ののじてん）・同じく記号
	# 〃	3003	[オナジク]	オナジク
	{"text": "〃", "braille": "オナジク", "cost": 5000},
	# 二の字点（にのじてん）
	# 〻    303b
	{"text": "各〻", "braille": "オノオノ"},
	{"text": "屡〻", "braille": "シバシバ"},
	# くの字点（くのじてん）
	# 〱    3031 くの字点
	# 〲    3032 くの字点(濁点)
	# 〳    3033 くの字点上
	# 〴    3034 くの字点上(濁点)
	# 〵    3035 くの字点下
	{"text": "〱", "braille": "クノジテン"},
	{"text": "〲", "braille": "クノジテン ダクテン"},
	{"text": "〳", "braille": "クノジテン ウエ"},
	{"text": "〴", "braille": "クノジテン ウエ ダクテン"},
	{"text": "〵", "braille": "クノジテン シタ"},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/45
	{
		"text": "⢎⣿⡱",
		"braille": "⢎⣿⡱",
		"speech": "トグルボタンオサレテイル",
	},
	{
		"text": "⢎⣀⡱",
		"braille": "⢎⣀⡱",
		"speech": "トグルボタンオサレテイナイ",
	},
	{
		"text": "⣏⣿⣹",
		"braille": "⣏⣿⣹",
		"speech": "チェックボックスチェック",
	},
	{
		"text": "⣏⣸⣹",
		"braille": "⣏⣸⣹",
		"speech": "チェックボックスイチブチェック",
	},
	{
		"text": "⣏⣀⣹",
		"braille": "⣏⣀⣹",
		"speech": "チェックボックスチェックナシ",
	},
	# 乗,1000,1000,1000,名詞,一般,*,*,*,*,乗,ジョウ,ジョー,1/2,C2
	{
		"text": "乗",
		"cost": 1000,
		"pos": "名詞,一般,*,*,*,*",
		"speech": "ジョー",
		"accent": "1/2",
	},
	{
		"text": "揃え",
		"pos": "名詞,一般,*,*,*,*",
		"speech": "ソロエ",
		"accent": "0/3",
	},
	{
		"text": "初期値",
		"pos": "名詞,一般,*,*,*,*",
		"speech": "ショキチ",
		"accent": "2/3",
	},
	{
		"text": "静画",
		"pos": "名詞,固有名詞,一般,*,*,*",
		"speech": "セイガ",
		"accent": "1/3",
	},
	{
		"text": "下準備",
		"pos": "名詞,サ変接続,*,*,*,*",
		"speech": "シタジュンビ",
		"accent": "3/5",
	},
	{
		"text": "殺",
		"pos": "名詞,サ変接続,*,*,*,*",
		"speech": "サツ",
		"accent": "1/2",
	},
	{
		"text": "重殺",
		"pos": "名詞,サ変接続,*,*,*,*",
		"speech": "ジューサツ",
		"accent": "0/4",
	},
	{
		"text": "挟殺",
		"pos": "名詞,サ変接続,*,*,*,*",
		"speech": "キョーサツ",
		"accent": "0/4",
	},
	{
		"text": "捕殺",
		"pos": "名詞,サ変接続,*,*,*,*",
		"speech": "ホサツ",
		"accent": "0/3",
	},
	{
		"text": "天中殺",
		"pos": "名詞,サ変接続,*,*,*,*",
		"speech": "テンチューサツ",
		"accent": "3/6",
	},
	{
		"text": "殺人鬼",
		"pos": "名詞,サ変接続,*,*,*,*",
		"speech": "サツジンキ",
		"braille": "サツジン キ",
		"accent": "3/5",
	},
	{
		"text": "長押し",
		"speech": "ナガオシ",
		"accent": "0/4",
		"pos": "名詞,サ変接続,*,*,*,*",
	},
	{
		"text": "４分音符",
		"pos": "名詞,一般,*,*,*,*",
		"speech": "シブオンプ",
		"braille": "4ブ オンプ",
		"accent": "3/5",
	},
	{
		"text": "仏足石歌",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "ブッソクセキカ",
		"accent": "5/7",
	},
	{
		"text": "諸子百家",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "ショシ ヒャッカ",
		"accent": "3/5",
	},
	{
		"text": "梅が香",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "ウメガカ",
		"accent": "0/4",
	},
	{
		"text": "年回忌",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "ネンカイキ",
		"accent": "3/5",
	},
	{
		"text": "開店祝",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "カイテン イワイ",
		"accent": "5/7",
	},
	{
		"text": "大親分",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "オオオヤブン",
		"accent": "3/6",
	},
	{
		"text": "唐楓",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "トーカエデ",
		"accent": "3/5",
	},
	{
		"text": "返り入幕",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "カエリ ニューマク",
		"accent": "4/7",
	},
	{
		"text": "返り新参",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "カエリ シンザン",
		"accent": "4/7",
	},
	{
		"text": "顔形",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "カオカタチ",
		"accent": "0/5",
	},
	{
		"text": "大顔合わせ",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "オオカオアワセ",
		"accent": "0/7",
	},
	{
		"text": "呵呵大笑",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "カカ タイショー",
		"accent": "1/6",
	},
	{
		"text": "加賀鳶",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "カガトビ",
		"accent": "0/4",
	},
	{
		"text": "桃栗",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "モモ クリ",
		"accent": "0/4",
	},
	{
		"text": "数限り無い",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "カズ カギリ ナイ",
		"accent": "1/7",
	},
	{
		"text": "各区",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "カク ク",
		"accent": "1/3",
	},
	{
		"text": "終楽章",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "シューガクショー",
		"accent": "3/6",
	},
	{
		"text": "楽派",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "ガクハ",
		"accent": "1/3",
	},
	{
		"text": "馬鹿さ",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "バカサ",
		"accent": "0/3",
	},
	{
		"text": "金の減り",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "カネノ ヘリ",
		"accent": "0/5",
	},
	{
		"text": "駕籠",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "カゴ",
		"accent": "0/2",
	},
	{
		"text": "鵾駕籠",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "トーマルカゴ",
		"accent": "0/6",
	},
	{
		"text": "飾り職人",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "カザリ ショクニン",
		"accent": "4/7",
	},
	{
		"text": "蓬萊",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "ホーライ",
		"accent": "0/4",
	},
	{
		"text": "出て行けがし",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "デテイケガシ",
		"accent": "0/6",
	},
	{
		"text": "加持祈祷",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "カジ キトー",
		"accent": "1/4",
	},
	{
		"text": "太郎冠者",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "タロー カジャ",
		"accent": "4/5",
	},
	{
		"text": "古今和歌集",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "コキン ワカシュー",
		"accent": "0/7",
	},
	{
		"text": "数限りない",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "カズ カギリ ナイ",
		"accent": "1/7",
	},
	{
		"text": "過ぎ来し方",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "スギコシ カタ",
		"accent": "1/6",
	},
	{
		"text": "時の運",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "トキノ ウン",
		"accent": "4/5",
	},
	{
		"text": "我が儘",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "ワガママ",
		"accent": "0/4",
	},
	{
		"text": "上一段",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "カミ1ダン",
		"speech": "カミイチダン",
		"accent": "0/6",
	},
	{
		"text": "糅てて",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "カテテ",
		"accent": "1/3",
	},
	{
		"text": "漢方薬局",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "カンポー ヤッキョク",
		"accent": "5/8",
	},
	{
		"text": "ちゅうちゅう",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "チューチュー",
		"accent": "1/4",
	},
	{
		"text": "ぐうぐう",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "グーグー",
		"accent": "1/4",
	},
	{
		"text": "めえめえ",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "メエメエ",
		"accent": "1/4",
	},
	{
		"text": "ごおごお",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "ゴオゴオ",
		"accent": "1/4",
	},
	{
		"text": "富栄養化",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "フ エイヨーカ",
		"accent": "1/6",
	},
	{
		"text": "満遍無く",
		"pos": "副詞,一般,*,*,*,*",
		"speech": "マンベンナク",
		"braille": "マンベンナク",
		"cost": -1000,
	},
	{
		"text": "丸１日",
		"pos": "名詞,一般,*,*,*,*",
		"speech": "マルイチニチ",
		"braille": "マル 1ニチ",
		"accent": "0/6",
	},
	{
		"text": "こっきり",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "コッキリ",
		"accent": "1/4",
	},
	{
		"text": "手当たり次第",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "テアタリ シダイ",
		"accent": "5/7",
	},
	{
		"text": "ドライブウエイ",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "ドライブ ウエイ",
		"accent": "5/7",
	},
	{
		"text": "ロープウエイ",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "ロープ ウエイ",
		"accent": "4/6",
	},
	{
		"text": "塩基性塩",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "エンキセイエン",
		"accent": "4/7",
	},
	{
		"text": "アルミニウム塩",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "アルミニウムエン",
		"accent": "0/8",
	},
	{
		"text": "得たり賢し",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "エタリ カシコシ",
		"accent": "2/7",
	},
	{
		"text": "Ｈ形",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "Hガタ",
		"speech": "エイチガタ",
		"accent": "0/5",
	},
	{
		"text": "遠赤外線",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "エンセキガイセン",
		"accent": "1/8",
	},
	{
		"text": "薄ら",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "ウスラ",
		"accent": "0/3",
	},
	{
		"text": "カリ塩",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "カリエン",
		"accent": "2/4",
	},
	{
		"text": "クレオソート丸",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "クレオソートガン",
		"accent": "0/8",
	},
	{
		"text": "キーパーソン",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "キー パーソン",
		"accent": "3/6",
	},
	{
		"text": "ギフトカード",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "ギフト カード",
		"accent": "4/6",
	},
	{
		"text": "ロールキャベツ",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "ロール キャベツ",
		"accent": "4/6",
	},
	{
		"text": "筋紡錘",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "キンボースイ",
		"accent": "3/6",
	},
	{
		"text": "スターキング",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "スター キング",
		"accent": "4/6",
	},
	{
		"text": "坂田金時",
		"pos": "名詞,固有名詞,人名,一般,*,*",
		"braille": "サカタノ キントキ",
		"accent": "1/8",
	},
	{
		"text": "一遍",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "イッペン",
		"accent": "3/4",
		"cost": -1000,
	},
	{
		"text": "ギアボックス",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "ギア ボックス",
		"accent": "3/6",
	},
	{
		"text": "セカンドギア",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "セカンド ギア",
		"accent": "5/6",
	},
	{
		"text": "万葉",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "マンヨー",
		"accent": "0/4",
	},
	{
		"text": "英検",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "エイケン",
		"accent": "0/4",
	},
	{
		"text": "気いつけなはれ",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "キイ ツケナハレ",
		"accent": "6/7",
	},
	{
		"text": "木の芽和え",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "キノメアエ",
		"accent": "0/5",
	},
	{
		"text": "木の芽立ち",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "キノメダチ",
		"accent": "0/5",
	},
	{
		"text": "気を付け",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "キヲツケ",
		"accent": "2/4",
	},
	{
		"text": "お気を付け下さい",
		"pos": "名詞,一般,*,*,*,*",
		"braille": "オキヲツケ クダサイ",
		"accent": "8/9",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/55
	{
		"text": "ほらっ",
		"braille": "ホラッ",
		"speech": "ホラッ",
		"pos": "感動詞,*,*,*,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/57
	{
		"text": "京急",
		"speech": "ケイキュー",
		"pos": "名詞,固有名詞,組織,*,*,*",
		"accent": "1/4",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/61
	{
		"text": "従量制",
		"speech": "ジューリョーセイ",
		"pos": "名詞,一般,*,*,*,*",
		"accent": "0/6",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/58
	{
		"text": "注文書",
		"speech": "チューモンショ",
		"pos": "名詞,一般,*,*,*,*",
		"accent": "0/5",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "銀四郎",
		"braille": "ギンシロー",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "0/5",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "談四楼",
		"braille": "ダンシロー",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "0/5",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "立川談四楼",
		"braille": "タテカワ ダンシロー",
		"pos": "名詞,固有名詞,人名,一般,*,*",
		"accent": "2/9",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "晋三",
		"braille": "シンゾー",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "0/4",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "退所",
		"braille": "タイショ",
		"pos": "名詞,サ変接続,*,*,*,*",
		"accent": "0/4",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "笑点",
		"braille": "ショーテン",
		"pos": "名詞,一般,*,*,*,*",
		"accent": "1/4",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "笑福亭",
		"braille": "ショーフクテイ",
		"pos": "名詞,固有名詞,人名,姓,*,*",
		"accent": "0/6",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "鶴瓶",
		"braille": "ツルベ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "安住",
		"braille": "アズミ",
		"pos": "名詞,固有名詞,人名,姓,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "紳一郎",
		"braille": "シンイチロー",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "3/6",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "竜太",
		"braille": "リュータ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "倖田",
		"braille": "コウダ",
		"pos": "名詞,固有名詞,人名,姓,*,*",
		"accent": "0/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "來未",
		"braille": "クミ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/2",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "美嘉",
		"braille": "ミカ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/2",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "優樹菜",
		"braille": "ユキナ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "北乃",
		"braille": "キタノ",
		"pos": "名詞,固有名詞,人名,姓,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "指原",
		"braille": "サシハラ",
		"pos": "名詞,固有名詞,人名,姓,*,*",
		"accent": "2/4",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "莉乃",
		"braille": "リノ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/2",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "凜々花",
		"braille": "リリカ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "環奈",
		"braille": "カンナ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "村主",
		"braille": "スグリ",
		"pos": "名詞,固有名詞,人名,姓,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "章枝",
		"braille": "フミエ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "0/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "瑛士",
		"braille": "エイジ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "瑛太",
		"braille": "エイタ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "裕太",
		"braille": "ユータ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "亮廣",
		"braille": "アキヒロ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "2/4",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "翔平",
		"braille": "ショーヘイ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "0/4",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "春馬",
		"braille": "ハルマ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "徹平",
		"braille": "テッペイ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "0/4",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "真麻",
		"braille": "マアサ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "佑都",
		"braille": "ユート",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "桃李",
		"braille": "トオリ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "涼真",
		"braille": "リョーマ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "菅田",
		"braille": "スダ",
		"pos": "名詞,固有名詞,人名,姓,*,*",
		"accent": "0/2",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "将暉",
		"braille": "マサキ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "藤ヶ谷",
		"braille": "フジガヤ",
		"pos": "名詞,固有名詞,人名,姓,*,*",
		"accent": "2/4",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "太輔",
		"braille": "タイスケ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/4",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "太鳳",
		"braille": "タオ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/2",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "充希",
		"braille": "ミツキ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/3",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "望結",
		"braille": "ミユ",
		"pos": "名詞,固有名詞,人名,名,*,*",
		"accent": "1/2",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "日馬富士",
		"braille": "ハルマフジ",
		"pos": "名詞,固有名詞,人名,一般,*,*",
		"accent": "3/5",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "日馬富士関",
		"braille": "ハルマフジゼキ",
		"pos": "名詞,固有名詞,人名,一般,*,*",
		"accent": "5/7",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "京野菜",
		"speech": "キョーヤサイ",
		"pos": "名詞,一般,*,*,*,*",
		"accent": "3/5",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "洛南",
		"speech": "ラクナン",
		"pos": "名詞,固有名詞,地域,一般,*,*",
		"accent": "0/4",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/64
	{
		"text": "洛北",
		"speech": "ラクホク",
		"pos": "名詞,固有名詞,地域,一般,*,*",
		"accent": "0/4",
	},
	# https://github.com/nvdajp/nvdajp/issues/67
	{
		"text": "行頭文字",
		"speech": "ギョートーモジ",
		"braille": "ギョートー モジ",
		"pos": "名詞,一般,*,*,*,*",
		"accent": "5/6",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/74
	{
		"text": "縮約",
		"speech": "シュクヤク",
		"braille": "シュクヤク",
		"pos": "名詞,一般,*,*,*,*",
		"accent": "0/4",
	},
	# https://github.com/nvdajp/nvdajpmiscdep/issues/74
	{
		"text": "縮約形",
		"speech": "シュクヤクケイ",
		"braille": "シュクヤク ケイ",
		"pos": "名詞,一般,*,*,*,*",
		"accent": "0/6",
	},
	# https://github.com/nvdajp/nvdajp/issues/186
	{
		"text": "令和",
		"speech": "レイワ",
		"braille": "レイワ",
		"pos": "名詞,固有名詞,一般,*,*,*",
		"accent": "1/3",
	},
]


class DicItem(object):
	__slots__ = ("text", "speech", "accent", "cost", "pos", "braille")

	def __init__(self, a):
		if isinstance(a, list):
			self.text = a[0]
			self.speech = a[1]
			self.accent = a[2] if len(a) >= 3 else None
			self.cost = a[3] if len(a) >= 4 else None
			self.pos = a[4] if len(a) >= 5 else None
			self.braille = a[5] if len(a) >= 6 else None
		elif isinstance(a, dict):
			self.text = a["text"]
			if "speech" in a:
				self.speech = a["speech"]
			elif "braille" in a:
				self.speech = a["braille"].replace(" ", "").replace("/", "")
			else:
				print("data error: " + str(a))
				sys.exit(1)
			self.accent = a["accent"] if "accent" in a else None
			self.cost = a["cost"] if "cost" in a else None
			self.pos = a["pos"] if "pos" in a else None
			self.braille = a["braille"] if "braille" in a else None


def make_dic(CODE, THISDIR):
	# Accept both str and Path objects for compatibility
	if isinstance(THISDIR, Path):
		THISDIR = Path(THISDIR)
	else:
		THISDIR = Path(THISDIR)
	with open_file(str(THISDIR / OUT_FILE), "w", CODE) as file:
		## jdic
		for i in jdic:
			di = DicItem(i)
			k = di.text
			k1 = k
			y = di.speech
			mora_count = len(y)
			# アクセント位置を省略すると "0/(文字数)" になる
			pros = "0/%d" % mora_count
			cost = 1000
			pos = "名詞,一般,*,*,*,*"
			brl = None
			if di.accent:
				pros = di.accent
				# '3/' のようにアクセント位置だけを書けるようにする
				# 最後の文字が / であればモーラ数（文字数）を付与する
				if pros[-1] == "/":
					pros += str(mora_count)
			if di.cost:
				cost = di.cost
			if di.pos:
				pos = di.pos
			if di.braille:
				brl = di.braille
			# 表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
			# 左右文脈IDは明示的に 0 (BOS/EOS) を指定する。空欄にすると
			# mecab-dict-index の文脈ID解決に依存し、過去には解決失敗時の
			# 未定義動作で sys.dic が非決定的になっていた。0,0 は従来の
			# テスト済み挙動（読み・マスアケ）を保存する。
			s = "%s,0,0,%d,%s,%s,%s,%s,%s,C0" % (k1, cost, pos, k1, y, y, pros)
			if brl:
				s += "," + brl
			s += "\n"
			file.write(s)


if __name__ == "__main__":
	make_dic()
