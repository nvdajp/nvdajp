# eng_dic_maker.py for nvdajp_jtalk
# -*- coding: utf-8 -*-
# since 2010-12-05 by Takuya Nishimoto
# bep-eng.dic is available at:
# http://cpansearch.perl.org/src/MASH/Lingua-JA-Yomi-0.01/lib/Lingua/JA/bep-eng.dic

IN_FILE_DEFAULT = "c:/work/nvda/bep-eng.dic"
OUT_FILE = "nvdajp-eng-dic.csv"
DEFAULT_COST = 1600


open_file = lambda name, mode, encoding: open(name, mode, encoding=encoding)


from pathlib import Path

from alpha2mb import alpha2mb


def make_dic(IN_FILE, CODE, THISDIR):
	# Accept both str and Path objects for compatibility
	if isinstance(IN_FILE, Path):
		IN_FILE = str(IN_FILE)
	if isinstance(THISDIR, Path):
		THISDIR = Path(THISDIR)
	else:
		THISDIR = Path(THISDIR)
	import re

	d = [
		["alt", "オルト"],
		["acrobat", "アクロバット"],
		["adobe", "アドビー", "1/4", 1000],
		["about", "アバウト", "2/4"],
		["ass", "アス", "1/2", 10000],
		["azure", "アジュール", None, 100],
		["api", "エーピーアイ", None, 500],
		["animations", "アニメイションズ"],
		["audio", "オーディオ", "1/4", 610],
		["app", "アップ"],
		["approximately", "アプロクシメットゥリー", "3/10"],
		# ['anpi', 		'アンピ',			"1/3", 1000],
		["asian", "アジアン", "1/4", 1000],
		# ['asahi', 		'アサヒ',			"1/3", 1000],
		["appropriately", "アプロプリエトリィ"],
		["agreed", "アグリード"],
		["akb", "エーケービー", "1/6", 1000],
		["au", "エーユー", "1/4", 600],
		["allowed", "アラウド", "2/4"],
		[
			"adsl",
			"エーディーエスエル1/8",
		],
		["akita", "アキタ", None, 1000],
		["aomori", "アオモリ", None, 1000],
		[
			"asshuku",
			"アッシュク",
			"0/4",
		],
		["blank", "ブランク"],
		["biz", "ビズ"],
		["bazaar", "バザール"],
		["blog", "ブログ", None, 1000],
		["butt", "バットゥ", "1/4", 10000],
		["backups", "バックアップス"],
		["cam", "キャム"],
		["ctrl", "コントロール"],
		["console", "コンソール"],
		["caps", "キャプス"],
		["cygwin", "シグウィン"],
		["choose", "チュウズ", None, 1000],
		["cortana", "コルタナ"],
		["cygdrive", "シグドライブ", None, 1000],
		["completely", "コンプリートリィ"],
		["cycles", "サイクルズ"],
		["conspicuously", "コンスピシャスリィ"],
		["changed", "チェインジド"],
		["characters", "キャラクターズ"],
		["controls", "コントゥロウルズ"],
		["currently", "カレントリ"],
		["clicks", "クリックス"],
		["contains", "コンテインズ", "3/6"],
		["covered", "カバード", "1/4"],
		["considered", "コンシダード"],
		["closed", "クローズド", "2/5"],
		["contributions", "コントリビューションズ"],
		["co", "シーオー", "1/4", 1000],
		["certainly", "サートゥンリー", "1/6"],
		["delete", "デリート"],
		["del", "デリート"],
		["doxygen", "ドキシゲン"],
		["dev", "デブ"],
		["desktop", "デスクトップ", None, 1000],
		["documents", "ドキュメンツ", "1/5"],
		["distributable", "ディストリビュータブル", "5/9"],
		["drivers", "ドゥライバーズ"],
		["directly", "ダイレクトリィ"],
		["draggable", "ドゥラッガブル", "2/6"],
		["designed", "デザインド", "2/5"],
		["database", "デイタベイス", "1/5"],
		["docs", "ドックス", "1/4", 600],
		["explorer", "エクスプローラ"],
		["esc", "エスケープ"],
		["enter", "エンター"],
		["editions", "エディションズ"],
		["essentials", "エセンシャルズ"],
		["extentions", "エクステンションズ"],
		["edu", "エデュー", "1/3", 1000],
		["epub", "イーパブ"],
		["expressly", "エクスプレスリィ"],
		["entered", "エンタード"],
		["errors", "エラーズ"],
		["editable", "エディタブル", "1/5"],
		["everyone", "エブリワン", "1/5"],
		["euc", "イーユーシー", "1/6", 1000],
		["explicitly", "イクスプリシットリィ"],
		["firefox", "ファイアフォックス"],
		["for", "フォー"],
		["foryou", "フォーユー"],
		["folders", "フォルダーズ"],
		["favo", "ファボ"],
		["failed", "フェイルド"],
		["facebook", "フェイスブック", None, 1000],
		["favorites", "フェイバリッツ", "1/6"],
		["flanger", "フランジャー"],
		["files", "ファイルズ", "1/4", 600],
		["focusable", "フォウカサブル", "1/6"],
		["faq", "エフエーキュー", "1/6", 1000],
		["fukushima", "フクシマ", "2/4", 1000],
		["guide", "ガイド", None, 1000],
		["google", "グーグル"],
		["gnu", "グニュー"],
		["guidebook", "ガイドブック", None, 1000],
		["gamba", "ガンバ", "1/3", 1000],
		# ['genpatsu',	'ゲンパツ',		"1/4", 1000],
		["git", "ギットゥ"],
		["gpu", "ジーピーユー"],
		["gaming", "ゲイミング"],
		["hub", "ハブ"],
		["href", "エイチレフ"],
		["home", "ホーム", None, 1000],
		# ['hinan', 		'ヒナン', 			"1/3", 1000],
		# ['horijun',		'ホリジュン',		"1/4", 1000],
		# ['hokkaido', 	'ホッカイドー', 	None, 1000],
		["hachinohe", "ハチノヘ", None, 1000],
		["homepage", "ホームページ", None, 1000],
		["hidari", "ヒダリ"],
		["internet", "インターネット"],
		["insert", "インサート"],
		["iis", "アイアイエス"],
		["impaired", "インペアド"],
		["incorporate", "インコーポレイト"],
		["incorporates", "インコーポレイツ"],
		["ioc", "アイオーシー"],
		# ['inosenaoki',	'イノセナオキ',	"1/7", 1000],
		["inaccurate", "インアキュレイト"],
		["iconified", "アイコニファイド", "1/8"],
		["interactively", "インタラクティブリィ"],
		["iaea", "アイエーイーエー", "7/8", 1000],
		["id", "アイディー", "3/4", 1000],
		# ['it', 			'アイティー', 			"3/4", 1000],
		["ime", "アイエムイー", "0/6", 600],
		["iwate", "イワテ", None, 1000],
		["inking", "インキング"],
		["instagram", "インスタグラム"],
		["java", "ジャバ"],
		["jaxa", "ジャクサ"],
		["jis", "ジス", "1/2", 1000],
		["japan", "ジャパン", "2/3", 1000],
		["japanese", "ジャパニーズ", "3/5", 900],
		["jp", "ジェーピー", "1/4", 1000],
		["konica", "コニカ"],
		["kinect", "キネクト"],
		["kddi", "ケーディーディーアイ"],
		["killed", "キルド"],
		["keyboard", "キーボード", None, 1000],
		# ['kahoku', 		'カホク', 			"1/3", 1000],
		# ['kurogen',		'クロゲン',		"1/4", 1000],
		["keys", "キーズ"],
		["kesennuma", "ケセンヌマ", None, 1000],
		["kantei", "カンテー", None, 1000],
		["kashima", "カシマ", None, 1000],
		["kita", "キタ", "0/2"],
		["libre", "リブレ"],
		["levels", "レベルズ"],
		["locks", "ロックス"],
		["layered", "レイヤード", "1/5"],
		["manage", "マネイジ", None, 1000],
		["micro", "マイクロ"],
		["mozilla", "モジラ"],
		["media", "メディア", "1/3", 1000],
		["mixi", "ミクシー"],
		["matlab", "マトラブ", None, 1000],
		["mouse", "マウス", "1/3", 500],
		["medic", "メディック", "1/4", 1000],
		# ['mizu',			'ミズ',			"2/2", 1000],
		# ['minpo', 		'ミンポー',		"1/4", 1000],
		["moves", "ムーブズ"],
		["morioka", "モリオカ", "2/4", 1000],
		["miyagi", "ミヤギ", "1/3", 1000],
		["mei", "メイ", "1/2", 100],
		["meiryo", "メイリョー", "1/4"],
		["metered", "ミータードゥ"],
		["notepad", "ノートパッド", None, 1000],
		["nullsoft", "ヌルソフト", None, 1000],
		["npo", "エヌピーオー", "2/6", 1000],
		[
			"nec",
			"エヌイーシー",
			"1/6",
		],
		["nvda", "エヌブイディーエー", "1/8", 1000],
		["nico", "ニコ", "1/2", 1000],
		["niigata", "ニーガタ", "0/4", 1000],
		["nishimoto", "ニシモト"],
		["nippon", "ニッポン", "3/4", None, "固有名詞"],
		["nvaccess", "エヌブイアクセス", "5/8", None, "固有名詞"],
		["open", "オープン"],
		["office", "オフィス"],
		["operation", "オペレーション", None, 1000],
		["opensource", "オープンソース", None, 1000],
		["output", "アウトプット", None, 1000],
		["opened", "オープンド", "1/5"],
		["oshu", "オーシュー", None, 1000],
		["onsite", "オンサイトゥ", None, 1000],
		[
			"obviously",
			"オブビアスリー",
		],
		["python", "パイソン"],
		["pro", "プロ"],
		["plugins", "プラグインズ", None, 1000],
		["pref", "プリフ", "1/3", 1000],
		["previously", "プリビアスリ"],
		["permission", "パーミッション"],
		["page", "ページ", "1/3", 600],
		["quickly", "クイックリィ"],
		["radio", "ラジオ", "1/3", 800],
		["redistributable", "リディストリビュータブル", "6/10"],
		["renderings", "レンダリングズ"],
		["rect", "レクト"],
		["resample", "リサンプル"],
		["reuse", "リユーズ"],
		["runs", "ランズ"],
		["runtime", "ランタイム", "3/5"],
		["rendered", "レンダード"],
		["required", "リクワイアード", "3/7"],
		["recently", "リーセントゥリー"],
		["shift", "シフト"],
		["skype", "スカイプ", "2/4"],
		["soft", "ソフト"],
		["setup", "セットアップ"],
		["systems", "システムズ"],
		["shared", "シェアード"],
		["shares", "シェアーズ"],
		["suite", "スイート", "2/4", 1000],
		["settings", "セッティングズ", "1/6"],
		# ['seikatsu',	'セーカツ',		"1/4", 1000],
		# ['sagasu',		'サガス',			"1/3", 1000],
		["shimpo", "シンポー", "1/4", 1000],
		["shimbun", "シンブン", "1/4", 1000],
		["speaks", "スピークス"],
		["simultaneously", "サイマルテニアスリィ"],
		["synth", "シンセ"],
		["shimane", "シマネ", "1/3"],
		["sjis", "エスジス", "0/4", 1000],
		["saigai", "サイガイ", None, 1000],
		[
			"sumaho",
			"スマホ",
			"1/3",
		],
		[
			"smap",
			"スマップ",
			"2/4",
		],
		[
			"sr",
			"エスアール",
			"3/5",
		],
		[
			"someone",
			"サムワン",
			"1/4",
		],
		[
			"sometime",
			"サムタイム",
			"1/5",
		],
		["think", "シンク"],
		["threatened", "スレッテンド"],
		["thoroughly", "サラフリィ"],
		["talk", "トーク"],
		["tab", "タブ"],
		["tunes", "チューンズ", "1/4", 10],
		["tools", "ツールズ", "1/4"],
		["togetter", "トゥギャッター"],
		["tube", "チューブ", "1/3", 600],
		["time", "タイム", None, 1000],
		["tepco", "テプコ", "1/3", 1000],
		["types", "タイプス"],
		# ['teiden', 		'テーデン',		"1/4", 1000],
		# ['tokuho',		'トクホー',		"1/4", 1000],
		# ['takeyama', 	'タケヤマ',		"1/4", 1000],
		# ['takeshi',		'タケシ',			"1/3", 1000],
		["turns", "ターンズ"],
		["toggles", "トグルズ"],
		["tsukuba", "ツクバ", None, 1000],
		["tochigi", "トチギ", None, 1000],
		["themes", "スィームズ"],
		["tasks", "タスクス"],
		["teatime", "ティータイム"],
		["tiflotecnia", "ティフロテクニア"],
		["update", "アップデート"],
		["ui", "ユーアイ"],
		["uac", "ユーエーシー"],
		["ustream", "ユーストリーム", None, 1000],
		["ubuntu", "ウブンツー", None, 1000],
		["unicode", "ユニコウドゥ"],
		["usa", "ユーエスエー", "0/6"],
		["unenforceable", "アンエンフォーサブル"],
		["unveil", "アンベイル"],
		["undefined", "アンデファインドゥ"],
		["unicode", "ユニコウドゥ"],
		["untitled", "アンタイトルド"],
		["unlocks", "アンロックス"],
		["usb", "ユーエスビー", "1/6", 1000],
		["users", "ユーザーズ", "1/5"],
		["updates", "アップデーツ"],
		["uninstall", "アンインストール"],
		["version", "バージョン"],
		["versions", "バージョンズ"],
		["vantage", "バンテージ"],
		["visum", "ビズム"],
		["viewing", "ビューイング"],
		["waic", "ウェイク"],
		["wave", "ウェーブ"],
		["welcome", "ウェルカム"],
		["windows", "ウィンドウズ"],
		["ware", "ウェアー", None, 1000],
		["warranties", "ワランティーズ"],
		["wikipedia", "ウイキペディーア", "0/8", 1000],
		["warehouse", "ウェアーハウス", "1/6"],
		["xna", "エクスエヌエー"],
		["you", "ユー", None, 660],
		["yahoo", "ヤフー", "2/3", 1000],
		["yamagata", "ヤマガタ", None, 1000],
		["zune", "ズーン"],
	]
	k = {}
	for i in d:
		k[i[0]] = True
	for line in open_file(IN_FILE, "r", "utf-8"):
		if line[0] == "#":
			continue
		a1, a2 = line.rstrip().split(" ")
		a1 = re.sub("'", "\\'", a1)
		a1 = a1.lower()
		if a1 not in k:
			d.append([a1, a2])
			k[a1] = True
	d.sort()
	with open_file(str(THISDIR / OUT_FILE), "w", CODE) as file:
		for i in d:
			k = i[0]
			# skip such as SHE'LL
			if "'" in k:
				continue
			alpha_count = len(k)
			k1 = alpha2mb(k.lower())
			# https://github.com/nvdajp/nvdajpmiscdep/issues/53
			# skip 'WORDS' (ワーズ)
			if k1 == "ｗｏｒｄｓ":
				continue
			y = i[1]
			# 'WORD' ワードゥ -> ワード
			if y == "ワードゥ":
				y = "ワード"
			# work around ポッ゜シビリティー
			y = re.sub("゜", "", y)
			# default pros
			mora_count = len(y)
			pros = "0/%d" % mora_count
			# default cost
			cost = DEFAULT_COST
			if alpha_count <= 2:
				cost = cost * 5
			# override by entry
			hin1 = "一般"
			if len(i) >= 3 and i[2] is not None:
				pros = i[2]
			if len(i) >= 4 and i[3] is not None:
				cost = i[3]
			if len(i) >= 5 and i[4] is not None:
				hin1 = i[4]
			# naist-jdic の文脈ID (left-id.def/right-id.def) は
			# 「名詞,固有名詞,一般,...」のように細分類2まで持つ。
			# 「名詞,固有名詞,*,...」だと mecab-dict-index の文脈ID解決が
			# 失敗するため、細分類2を補う。
			hin2 = "一般" if hin1 == "固有名詞" else "*"
			# 表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
			# 左右文脈IDは明示的に 0 (BOS/EOS) を指定する。空欄にすると
			# mecab-dict-index の文脈ID解決に依存し、過去には解決失敗時の
			# 未定義動作で sys.dic が非決定的になっていた。0,0 は従来の
			# テスト済み挙動（読み・マスアケ）を保存する。
			s = "%s,0,0,%d,名詞,%s,%s,*,*,*,%s,%s,%s,%s,C0\n" % (
				k1,
				cost,
				hin1,
				hin2,
				k1,
				y,
				y,
				pros,
			)
			file.write(s)


if __name__ == "__main__":
	make_dic(IN_FILE_DEFAULT)
