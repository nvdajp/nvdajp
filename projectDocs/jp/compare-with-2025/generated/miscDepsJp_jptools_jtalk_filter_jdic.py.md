# Diff for: `miscDepsJp\jptools\jtalk\filter_jdic.py`

**Source**: `F:\nvda\gh\alphajp-251219\miscDepsJp\jptools\jtalk\filter_jdic.py`  
**Current**: `F:\nvda\gh\alphajp-260109\miscDepsJp\jptools\jtalk\filter_jdic.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtalk\\filter_jdic.py" "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\jtalk\\filter_jdic.py"
index deb4e88..0e3b4e0 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\jtalk\\filter_jdic.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\jtalk\\filter_jdic.py"
@@ -566,21 +566,9 @@ def filter_jdic(s):
 	elif a[0] == "太安万侶" and a[11] == "オオノヤスマロ" and len(a) == 15:
 		a.append("オオノ ヤスマロ")
 		s = ",".join(a)
-    elif (
-        a[0] == "上"
-        and a[4] == "名詞"
-        and a[5] == "接尾"
-        and a[11] == "ジョウ"
-        and len(a) == 15
-    ):
-        s = ""
-    elif (
-        a[0] == "上"
-        and a[4] == "名詞"
-        and a[5] == "非自立"
-        and a[11] == "ジョウ"
-        and len(a) == 15
-    ):
+	elif a[0] == "上" and a[4] == "名詞" and a[5] == "接尾" and a[11] == "ジョウ" and len(a) == 15:
+		s = ""
+	elif a[0] == "上" and a[4] == "名詞" and a[5] == "非自立" and a[11] == "ジョウ" and len(a) == 15:
 		s = ""
 	elif a[0] == "傀儡" and a[12] == "クグツ" and len(a) == 15:
 		s = ""

```