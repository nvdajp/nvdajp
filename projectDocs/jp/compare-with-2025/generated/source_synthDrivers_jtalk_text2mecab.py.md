# Diff for: `source\synthDrivers\jtalk\text2mecab.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\synthDrivers\jtalk\text2mecab.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\synthDrivers\jtalk\text2mecab.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\text2mecab.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDrivers\\jtalk\\text2mecab.py"
index ca07e0a..8c5babf 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\text2mecab.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDrivers\\jtalk\\text2mecab.py"
@@ -46,7 +46,7 @@ def text2mecab_setup():
 			[re.compile("<"), "＜"],
 			[re.compile("="), "＝"],
 			[re.compile(">"), "＞"],
-            [re.compile("\?"), "？"],
+			[re.compile("\\?"), "？"],
 			[re.compile("@"), "＠"],
 			[re.compile("A"), "Ａ"],
 			[re.compile("B"), "Ｂ"],
@@ -118,7 +118,7 @@ def text2mecab_convert(s):
 	for p in predic:
 		try:
 			s = re.sub(p[0], p[1], s)
-        except:
+		except Exception:
 			pass
 	return s
 
@@ -127,4 +127,20 @@ def text2mecab(txt, CODE_=CODE):
 	text2mecab_setup()
 	txt = unicodedata.normalize("NFKC", txt)
 	txt = text2mecab_convert(txt)
+	# BEGIN JP PATCH (assert suspicious patterns before encoding)
+	# Detect mixed ASCII/non-ASCII or unusual whitespace patterns that may trigger crashes.
+	assert "\t" not in txt, "text2mecab: unexpected tab after conversion"
+	assert "\r" not in txt and "\n" not in txt, "text2mecab: unexpected newline after conversion"
+	ascii_count = sum(1 for c in txt if ord(c) < 0x80)
+	non_ascii_count = len(txt) - ascii_count
+	if ascii_count and non_ascii_count:
+		# Allow common punctuation but flag mixed alnum + non-ASCII as suspicious.
+		mixed_alnum = any(c.isalnum() and ord(c) < 0x80 for c in txt)
+		assert not mixed_alnum, "text2mecab: mixed ASCII alnum and non-ASCII"
+	# Detect repeated ASCII spaces (double-space) which showed crashes in x64.
+	assert "  " not in txt, "text2mecab: consecutive ASCII spaces detected"
+	# Detect ASCII control characters (excluding space) after conversion.
+	ctrl_chars = [c for c in txt if ord(c) < 0x20 and c != " "]
+	assert not ctrl_chars, f"text2mecab: ASCII control chars detected: {ctrl_chars!r}"
+	# END JP PATCH
 	return txt.encode(CODE_, "ignore")

```