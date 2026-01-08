# Diff for: `miscDepsJp\jptools\jtalk\custom_dic_maker.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\miscDepsJp\jptools\jtalk\custom_dic_maker.py`  
**Current**: `F:\nvda\gh\alphajp-260109\miscDepsJp\jptools\jtalk\custom_dic_maker.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtalk\\custom_dic_maker.py" "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\jtalk\\custom_dic_maker.py"
index 4163364..fd75eef 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtalk\\custom_dic_maker.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\jtalk\\custom_dic_maker.py"
@@ -9,7 +9,7 @@
 open_file = lambda name, mode, encoding: open(name, mode, encoding=encoding)
 
 
-from os import path
+from pathlib import Path
 
 
 jdic = [
@@ -166,6 +166,7 @@
 	["各方面", "カクホーメン", "1/6", None, None, "カク ホーメン"],
 	["旧陸軍", "キューリクグン", "1/6", None, None, "キュー リクグン"],
 	["山や川", "ヤマヤカワ", "2/5", None, None, "ヤマヤ カワ"],
+	["山や川等", "ヤマヤカワナド", "2/7", -1000, "名詞,一般,*,*,*,*", "ヤマヤ カワナド"],
 	["相対する", "アイタイスル"],
 	["相たずさえて", "アイタズサエテ"],
 	["相整う", "アイトトノウ"],
@@ -225,13 +226,32 @@
 	{"text": "一言の下", "braille": "1ゴンノ モト", "speech": "イチゴンノモト"},
 	{"text": "一日三秋", "braille": "1ジツ 3シュー", "speech": "イチジツサンシュー"},
 	{"text": "一日の長", "braille": "1ジツノ チョー", "speech": "イチジツノチョー"},
-    {"text": "一日中", "braille": "1ニチジュー", "speech": "イチニチジュー"},
-    {"text": "一日増し", "braille": "1ニチマシ", "speech": "イチニチマシ"},
+	# 複合語として優先させるためコストを下げる
+	{
+		"text": "一日中",
+		"braille": "1ニチジュー",
+		"speech": "イチニチジュー",
+		"cost": -1000,
+		"pos": "名詞,一般,*,*,*,*",
+	},
+	{
+		"text": "一日増し",
+		"braille": "1ニチマシ",
+		"speech": "イチニチマシ",
+		"cost": -2000,
+		"pos": "名詞,一般,*,*,*,*",
+	},
 	{"text": "一割一分", "braille": "1ワリ 1ブ", "speech": "イチワリイチブ"},
 	{"text": "一番星", "braille": "1バンボシ", "speech": "イチバンボシ"},
 	{"text": "一木一草", "braille": "1ボク 1ソー", "speech": "イチボクイッソー"},
 	{"text": "一木造り", "braille": "1ボクヅクリ", "speech": "イチボクヅクリ"},
-    {"text": "一念岩", "braille": "イチネン イワ"},
+	{
+		"text": "一念岩",
+		"braille": "イチネン イワ",
+		"speech": "イチネンイワ",
+		"cost": -1000,
+		"pos": "名詞,一般,*,*,*,*",
+	},
 	{"text": "一谷嫩軍記", "braille": "イチノタニ フタバ グンキ"},
 	{"text": "一分の隙", "braille": "イチブノ スキ"},
 	{"text": "一分一厘狂い", "braille": "1ブ 1リン クルイ", "speech": "イチブイチリンクルイ"},
@@ -262,7 +282,7 @@
 	{"text": "勝敗は一に時", "braille": "ショーハイワ イツニ トキ"},
 	{"text": "何時になく", "braille": "イツニ ナク"},
 	{"text": "一波動けば万波", "braille": "1パ ウゴケバ バンパ", "speech": "イッパウゴケババンパ"},
-    {"text": "一敗", "braille": "1パイ", "speech": "イッパイ"},
+	{"text": "一敗", "braille": "1パイ", "speech": "イッパイ", "cost": -1000, "pos": "名詞,一般,*,*,*,*"},
 	{"text": "一筆画", "braille": "1ピツガ", "speech": "イッピツガ"},
 	{"text": "一本背負い", "braille": "1ポンゼオイ", "speech": "イッポンゼオイ"},
 	{"text": "一本道", "braille": "1ポンミチ", "speech": "イッポンミチ"},
@@ -396,12 +416,13 @@
 		"speech": "トーキング",
 		"accent": "1/5",
 	},
+	# nvdajp ticket34973: 曜日の括弧表記（コストを低く設定して優先）
 	{
 		"text": "（日）",
 		"speech": "（ニチ）",
 		"braille": "（ニチ）",
 		"accent": "1/2",
-        "cost": 1345,
+		"cost": -1000,
 		"pos": "名詞,一般,*,*,*,*",
 	},
 	{
@@ -409,7 +430,7 @@
 		"speech": "（ゲツ）",
 		"braille": "（ゲツ）",
 		"accent": "1/2",
-        "cost": 1345,
+		"cost": -1000,
 		"pos": "名詞,一般,*,*,*,*",
 	},
 	{
@@ -417,7 +438,7 @@
 		"speech": "（カ）",
 		"braille": "（カ）",
 		"accent": "1/1",
-        "cost": 1345,
+		"cost": -1000,
 		"pos": "名詞,一般,*,*,*,*",
 	},
 	{
@@ -425,7 +446,7 @@
 		"speech": "（スイ）",
 		"braille": "（スイ）",
 		"accent": "1/2",
-        "cost": 1345,
+		"cost": -1000,
 		"pos": "名詞,一般,*,*,*,*",
 	},
 	{
@@ -433,7 +454,7 @@
 		"speech": "（モク）",
 		"braille": "（モク）",
 		"accent": "1/2",
-        "cost": 1345,
+		"cost": -1000,
 		"pos": "名詞,一般,*,*,*,*",
 	},
 	{
@@ -876,6 +897,13 @@
 		"braille": "フ エイヨーカ",
 		"accent": "1/6",
 	},
+	{
+		"text": "満遍無く",
+		"pos": "副詞,*,*,*,*,*",
+		"speech": "マンベンナク",
+		"braille": "マンベンナク",
+		"cost": -1000,
+	},
 	{
 		"text": "丸１日",
 		"pos": "名詞,一般,*,*,*,*",
@@ -997,6 +1025,7 @@
 		"pos": "名詞,一般,*,*,*,*",
 		"braille": "イッペン",
 		"accent": "3/4",
+		"cost": -1000,
 	},
 	{
 		"text": "ギアボックス",
@@ -1458,7 +1487,12 @@ def __init__(self, a):
 
 
 def make_dic(CODE, THISDIR):
-    with open_file(path.join(THISDIR, OUT_FILE), "w", CODE) as file:
+	# Accept both str and Path objects for compatibility
+	if isinstance(THISDIR, Path):
+		THISDIR = Path(THISDIR)
+	else:
+		THISDIR = Path(THISDIR)
+	with open_file(str(THISDIR / OUT_FILE), "w", CODE) as file:
 		## jdic
 		for i in jdic:
 			di = DicItem(i)

```