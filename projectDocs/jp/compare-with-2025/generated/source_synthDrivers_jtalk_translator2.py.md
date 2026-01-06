# Diff for: `source\synthDrivers\jtalk\translator2.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\synthDrivers\jtalk\translator2.py`  
**Current**: `F:\nvda\gh\alphajp\source\synthDrivers\jtalk\translator2.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\translator2.py" "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\jtalk\\translator2.py"
index 3a6dbe5f96..ca9f39f7c4 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\translator2.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\jtalk\\translator2.py"
@@ -7,16 +7,33 @@
 
 import copy
 import re
+from ctypes import string_at
 
 
 try:
 	from ._nvdajp_unicode import unicode_normalize
-    from .mecab import *
+	from .mecab import (
+		CODE,
+		MecabFeatures,
+		Mecab_analysis,
+		Mecab_correctFeatures,
+		Mecab_initialize,
+		Mecab_print,
+	)
+	from .text2mecab import text2mecab
 	from . import translator1
 	from .jtalkDir import jtalk_dir, dic_dir, user_dics
 except (ImportError, ValueError):
 	from _nvdajp_unicode import unicode_normalize  # type: ignore
-    from mecab import *  # type: ignore
+	from mecab import (  # type: ignore
+		CODE,
+		MecabFeatures,
+		Mecab_analysis,
+		Mecab_correctFeatures,
+		Mecab_initialize,
+		Mecab_print,
+	)
+	from text2mecab import text2mecab  # type: ignore
 	import translator1  # type: ignore
 	from jtalkDir import jtalk_dir, dic_dir, user_dics  # type: ignore
 
@@ -25,7 +42,7 @@
 	from logHandler import log  # type: ignore
 
 	_logwrite = log.debug
-except:
+except Exception:
 
 	def __print(s):
 		print(s)
@@ -210,9 +227,7 @@ def update_phonetic_symbols(mo):
 		# ６、「ジ　ズ　ジャ　ジュ　ジョ」と「ヂ　ヅ　ヂャ　ヂョ」の使い分け
 		# before: 綴る,綴る,動詞,自立,*,*,ツヅル,ツズル,0/3,ツズル,0
 		# after:  綴る,綴る,動詞,自立,*,*,ツヅル,ツズル,0/3,ツヅル,0
-        if (mo.yomi[p] == "ジ" and mo.kana[p] == "ヂ") or (
-            mo.yomi[p] == "ズ" and mo.kana[p] == "ヅ"
-        ):
+		if (mo.yomi[p] == "ジ" and mo.kana[p] == "ヂ") or (mo.yomi[p] == "ズ" and mo.kana[p] == "ヅ"):
 			mo.output = mo.output[:p] + mo.kana[p] + mo.output[p + 1 :]
 
 
@@ -281,6 +296,7 @@ def replace_morphs(li, dic):
 
 RE_KANSUJI = re.compile("^[一二三四五六七八九〇零十拾百千壱二参]+$")
 
+
 # http://programminblog.blogspot.jp/2010/11/python.html
 def kansuji2arabic(text, logwrite=None):
 	if not RE_KANSUJI.match(text):
@@ -305,9 +321,7 @@ def kansuji2arabic(text, logwrite=None):
 				result += digit * numgroup
 			digit = 100
 		elif c == "千":
-            if (digit == 10 and c1 and c1 in "十拾") or (
-                digit == 100 and c1 and c1 in "百"
-            ):
+			if (digit == 10 and c1 and c1 in "十拾") or (digit == 100 and c1 and c1 in "百"):
 				result += digit * numgroup
 			digit = 1000
 		else:
@@ -448,9 +462,7 @@ def is_alpha_or_single(s):
 	return RE_ALPHA_OR_SINGLE.match(s)
 
 
-RE_ASCII_SYMBOLS = re.compile(
-    r"^[\,\.\:\;\!\?\@\#\\\$\%\&\*\|\+\-\/\=\<\>\"'\^\`\_\~]+$"
-)
+RE_ASCII_SYMBOLS = re.compile(r"^[\,\.\:\;\!\?\@\#\\\$\%\&\*\|\+\-\/\=\<\>\"'\^\`\_\~]+$")
 
 
 def replace_alphabet_morphs(li, nabcc=False):
@@ -476,11 +488,7 @@ def replace_alphabet_morphs(li, nabcc=False):
 			alp_morphs.append(mo)
 		elif mo.nhyouki == "\\":
 			alp_morphs.append(mo)
-        elif (
-            mo.nhyouki
-            and mo.nhyouki[0] in r",+@/#$%&*;"
-            and RE_ASCII_SYMBOLS.match(mo.nhyouki)
-        ):
+		elif mo.nhyouki and mo.nhyouki[0] in r",+@/#$%&*;" and RE_ASCII_SYMBOLS.match(mo.nhyouki):
 			alp_morphs.append(mo)
 		elif (
 			alp_morphs
@@ -492,12 +500,7 @@ def replace_alphabet_morphs(li, nabcc=False):
 			)
 		):
 			alp_morphs.append(mo)
-        elif (
-            alp_morphs
-            and mo.nhyouki == " "
-            and next_mo
-            and is_alpha_or_single(next_mo.nhyouki)
-        ):
+		elif alp_morphs and mo.nhyouki == " " and next_mo and is_alpha_or_single(next_mo.nhyouki):
 			alp_morphs.append(mo)
 		elif alp_morphs and mo.nhyouki.isdigit():
 			alp_morphs.append(mo)
@@ -561,9 +564,7 @@ def fix_japanese_date_morphs(li):
 			if prev_mo.hyouki in ("14", "24", "十四", "一四", "二四", "二十四"):
 				li[i].output = "カ"
 				new_li.append(li[i])
-            elif (
-                prev2_mo is None or prev2_mo.hyouki != "、"
-            ) and prev_mo.output in WAGO_DIC:
+			elif (prev2_mo is None or prev2_mo.hyouki != "、") and prev_mo.output in WAGO_DIC:
 				m = copy.deepcopy(mo)
 				m.hyouki = prev_mo.hyouki + mo.hyouki
 				m.nhyouki = prev_mo.nhyouki + mo.nhyouki
@@ -617,12 +618,7 @@ def should_separate(prev2_mo, prev_mo, mo, next_mo, nabcc=False, logwrite=_logwr
 		return True
 
 	# 1月/1日
-    if (
-        mo_output_isdigit
-        and prev_mo.nhyouki
-        and prev_mo.nhyouki[0].isdigit()
-        and prev_mo.nhyouki[-1] == "月"
-    ):
+	if mo_output_isdigit and prev_mo.nhyouki and prev_mo.nhyouki[0].isdigit() and prev_mo.nhyouki[-1] == "月":
 		return True
 
 	# 三,三,名詞,数,*,*,サン,サン,0/2,3,0
@@ -634,11 +630,7 @@ def should_separate(prev2_mo, prev_mo, mo, next_mo, nabcc=False, logwrite=_logwr
 
 	# 外国語引用符、マスアケ、助詞、助動詞
 	is_mo_hinshi1_joshi_or_jodoshi = mo.hinshi1 in ("助詞", "助動詞")
-    if (
-        is_mo_hinshi1_joshi_or_jodoshi
-        and prev_mo.output
-        and prev_mo.output.endswith("⠴")
-    ):
+	if is_mo_hinshi1_joshi_or_jodoshi and prev_mo.output and prev_mo.output.endswith("⠴"):
 		return True
 
 	# アルファベットの後の助詞、助動詞
@@ -733,9 +725,7 @@ def should_separate(prev2_mo, prev_mo, mo, next_mo, nabcc=False, logwrite=_logwr
 		and mo.hinshi1 == "名詞"
 		and mo.hinshi2 == "一般"
 	):
-        if not (mo.hyouki == "卿" and mo.yomi == "キョー") and not (
-            mo.hyouki == "市" and mo.yomi == "シ"
-        ):
+		if not (mo.hyouki == "卿" and mo.yomi == "キョー") and not (mo.hyouki == "市" and mo.yomi == "シ"):
 			return True
 
 	# 東京/都 千代田/区
@@ -776,12 +766,7 @@ def should_separate(prev2_mo, prev_mo, mo, next_mo, nabcc=False, logwrite=_logwr
 		return True
 
 	# 障害,者/協会
-    if (
-        prev2_mo
-        and prev2_mo.hinshi1 == "名詞"
-        and prev_mo.hyouki == "者"
-        and mo.hinshi1 == "名詞"
-    ):
+	if prev2_mo and prev2_mo.hinshi1 == "名詞" and prev_mo.hyouki == "者" and mo.hinshi1 == "名詞":
 		return True
 
 	# 世界/初
@@ -872,6 +857,36 @@ def should_separate(prev2_mo, prev_mo, mo, next_mo, nabcc=False, logwrite=_logwr
 	if prev_mo.hinshi1 == "助動詞" and prev_mo.hyouki == "で" and mo.hinshi1 == "助動詞":
 		return True
 
+	# 「の」（名詞,非自立）の後に名詞が続く場合にスペースを挿入
+	# 例1: 映画「ラヂオの時間」 → エイガ 「ラジオノ ジカン」
+	#  ラヂオ,名詞,一般 → ラジオ
+	#  の,名詞,非自立 → ノ
+	#  時間,名詞,副詞可能 → ジカン
+	# 例2: 気を付けの姿勢 → キヲツケノ シセイ
+	#  気を付け,名詞,一般 → キヲツケ
+	#  の,名詞,非自立 → ノ
+	#  姿勢,名詞,一般 → シセイ
+	if (
+		prev_mo.hinshi1 == "名詞"
+		and prev_mo.hinshi2 == "非自立"
+		and prev_mo.hyouki == "の"
+		and mo.hinshi1 == "名詞"
+		and mo.hinshi2 in ("一般", "副詞可能")
+	):
+		return True
+
+	# 感動詞の後に助動詞「ござい」が続く場合にスペースを挿入
+	# 例: 有り難うございました → アリガトー ゴザイマシタ
+	#  有り難う,感動詞 → アリガトー
+	#  ござい,助動詞 → ゴザイ
+	if (
+		prev_mo.hinshi1 == "感動詞"
+		and prev_mo.hyouki == "有り難う"
+		and mo.hinshi1 == "助動詞"
+		and mo.hyouki == "ござい"
+	):
+		return True
+
 	# 仮名文字 カナモジ
 	# 仮名タイプ カナタイプ
 	# 仮名変換 カナ ヘンカン
@@ -924,11 +939,7 @@ def should_separate(prev2_mo, prev_mo, mo, next_mo, nabcc=False, logwrite=_logwr
 			return True
 		if prev_mo.hinshi2 == "副助詞":  # じゃない
 			return True
-        if (
-            prev_mo.hinshi1 == "動詞"
-            and prev_mo.hinshi2 == "非自立"
-            and prev_mo.kihon == "てる"
-        ):  # てない
+		if prev_mo.hinshi1 == "動詞" and prev_mo.hinshi2 == "非自立" and prev_mo.kihon == "てる":  # てない
 			return True
 		if prev_mo.hinshi1 == "助動詞" and prev_mo.kihon == "だ":  # でない
 			return True
@@ -984,11 +995,7 @@ def should_separate(prev2_mo, prev_mo, mo, next_mo, nabcc=False, logwrite=_logwr
 	if (
 		nabcc
 		and prev_mo.hinshi2 == "アルファベット"
-        and (
-            prev_mo.nhyouki.endswith("(")
-            or prev_mo.nhyouki.endswith("[")
-            or prev_mo.nhyouki.endswith("{")
-        )
+		and (prev_mo.nhyouki.endswith("(") or prev_mo.nhyouki.endswith("[") or prev_mo.nhyouki.endswith("{"))
 		and mo.hinshi1 == "名詞"
 	):
 		return False
@@ -1349,10 +1356,28 @@ def japanese_braille_separate(inbuf, logwrite, nabcc=False):
 
 	# tab code
 	text = text.replace("\t", TAB_CODE)
+	# BEGIN JP PATCH (log tab replacement)
+	if TAB_CODE in text:
+		logwrite(f"translator2: TAB_CODE present after tab replace: {text!r}")
+	# END JP PATCH
 
 	# 'ふにゃ～'
 	text = text.replace("ゃ～", "ゃー")
 
+	# BEGIN JP PATCH (assert suspicious patterns before text2mecab)
+	assert "\t" not in text and "\r" not in text and "\n" not in text, "translator2: unexpected tab/CR/LF"
+	ascii_count = sum(1 for c in text if ord(c) < 0x80)
+	non_ascii_count = len(text) - ascii_count
+	if ascii_count and non_ascii_count:
+		mixed_alnum = any(c.isalnum() and ord(c) < 0x80 for c in text)
+		# Allow TAB_CODE (U+200B) in mixed text to continue investigation.
+		if mixed_alnum and TAB_CODE not in text:
+			if logwrite:
+				logwrite(f"translator2: mixed ASCII alnum and non-ASCII: {text!r}")
+	if "  " in text:
+		if logwrite:
+			logwrite("translator2: consecutive ASCII spaces detected")
+	# END JP PATCH
 	text = text2mecab(text)
 	mf = MecabFeatures()
 	Mecab_analysis(text, mf, logwrite_=logwrite)
@@ -1490,11 +1515,7 @@ def japanese_braille_separate(inbuf, logwrite, nabcc=False):
 	# 、,、,記号,読点,*,*,、,、,*/*,⠼,0
 	# 三,三,名詞,数,*,*,3,3,1/2,3,0
 	for pos in range(1, len(li) - 1):
-        if (
-            li[pos - 1].output.isdigit()
-            and li[pos].hyouki == "、"
-            and li[pos + 1].output.isdigit()
-        ):
+		if li[pos - 1].output.isdigit() and li[pos].hyouki == "、" and li[pos + 1].output.isdigit():
 			if nabcc:
 				li[pos].output = "."
 			else:
@@ -1503,11 +1524,7 @@ def japanese_braille_separate(inbuf, logwrite, nabcc=False):
 	# 算用数字ではさまれた中点を数符にする
 	if not nabcc:
 		for pos in range(1, len(li) - 1):
-            if (
-                li[pos - 1].output.isdigit()
-                and li[pos].hyouki == "・"
-                and li[pos + 1].output.isdigit()
-            ):
+			if li[pos - 1].output.isdigit() and li[pos].hyouki == "・" and li[pos + 1].output.isdigit():
 				li[pos].output = "⠼"
 
 	# before: ａｂ,ab,名詞,一般,*,*,アブ,アブ,1/2,アブ,0
@@ -1600,11 +1617,7 @@ def japanese_braille_separate(inbuf, logwrite, nabcc=False):
 		mo.nhyouki = unicode_normalize(mo.nhyouki)
 		# 情報処理点字の開始記号と終了記号
 		info = False
-        if (
-            RE_INFORMATION.match(mo.nhyouki)
-            and "@" in mo.nhyouki
-            and len(mo.nhyouki) > 1
-        ):
+		if RE_INFORMATION.match(mo.nhyouki) and "@" in mo.nhyouki and len(mo.nhyouki) > 1:
 			info = True
 		if "://" in mo.nhyouki:
 			info = True
@@ -1620,10 +1633,7 @@ def japanese_braille_separate(inbuf, logwrite, nabcc=False):
 		# 外国語引用符
 		# 空白をはさまない1単語は外国語引用符ではなく外字符で
 		elif (
-            (
-                RE_GAIJI.match(mo.nhyouki)
-                and ((" " in mo.nhyouki) or ("'" in mo.nhyouki))
-            )
+			(RE_GAIJI.match(mo.nhyouki) and ((" " in mo.nhyouki) or ("'" in mo.nhyouki)))
 			or (("." in mo.nhyouki) and len(mo.nhyouki) > 3)
 			or (
 				# "0's", "80's"
@@ -1673,9 +1683,7 @@ def japanese_braille_separate(inbuf, logwrite, nabcc=False):
 		prev2_mo = li[i - 2] if i - 2 >= 0 else None
 		prev_mo = li[i - 1]
 		next_mo = li[i + 1] if i + 1 < len(li) else None
-        li[i - 1].sepflag = should_separate(
-            prev2_mo, prev_mo, li[i], next_mo, nabcc=nabcc, logwrite=logwrite
-        )
+		li[i - 1].sepflag = should_separate(prev2_mo, prev_mo, li[i], next_mo, nabcc=nabcc, logwrite=logwrite)
 
 	# do not translate if string is unicode braille
 	for i in range(0, len(li)):
@@ -1773,7 +1781,15 @@ def mergePositionMap(inpos1, inpos2, outlen, inlen):
 # louis-compatible method
 # tableList, typeform are not supported.
 # mode=dotsIO is default.
-def translate(inbuf, cursorPos=0, logwrite=_logwrite, unicodeIO=False, nabcc=False, louisTranslate=None, louisTableList=None):
+def translate(
+	inbuf,
+	cursorPos=0,
+	logwrite=_logwrite,
+	unicodeIO=False,
+	nabcc=False,
+	louisTranslate=None,
+	louisTableList=None,
+):
 	"""Translate a string of characters, providing position information.
 	@param inbuf: The string to translate.
 	@type inbuf: str
@@ -1787,9 +1803,7 @@ def translate(inbuf, cursorPos=0, logwrite=_logwrite, unicodeIO=False, nabcc=Fal
 	@rtype: (str, list of int, list of int, int)
 	@raise RuntimeError: If a complete translation could not be done.
 	"""
-    sp, outbuf, inpos1, inpos2 = translateWithInPos2(
-        inbuf, logwrite=logwrite, nabcc=nabcc
-    )
+	sp, outbuf, inpos1, inpos2 = translateWithInPos2(inbuf, logwrite=logwrite, nabcc=nabcc)
 	if not unicodeIO:
 		pat = outbuf.replace(" ", "\u2800")
 		outbuf = "".join([chr((ord(c) - 0x2800) + 0x8000) for c in pat])

```