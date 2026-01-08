# Diff for: `source\synthDrivers\jtalk\translator1.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\synthDrivers\jtalk\translator1.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\synthDrivers\jtalk\translator1.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\translator1.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDrivers\\jtalk\\translator1.py"
index 935a0cc..0dfdde6 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\translator1.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDrivers\\jtalk\\translator1.py"
@@ -475,10 +475,7 @@ def translateWithInPos(text, nabcc=False):
 		elif (
 			num
 			and (text[pos] in num_symbol_dic)
-            and (
-                (pos == len(text) - 1)
-                or (pos + 1 < len(text) and text[pos + 1].isdigit())
-            )
+			and ((pos == len(text) - 1) or (pos + 1 < len(text) and text[pos + 1].isdigit()))
 		):
 			retval += num_symbol_dic[text[pos]]
 			inPos.extend([pos] * len(num_symbol_dic[text[pos]]))

```