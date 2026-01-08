# Diff for: `miscDepsJp\include\python-jtalk\jtalkPrepare.py`

**Source**: `F:\nvda\gh\alphajp-251219\miscDepsJp\include\python-jtalk\jtalkPrepare.py`  
**Current**: `F:\nvda\gh\alphajp-260109\miscDepsJp\include\python-jtalk\jtalkPrepare.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\include\\python-jtalk\\jtalkPrepare.py" "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\include\\python-jtalk\\jtalkPrepare.py"
index 8741eb9..6113f06 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\include\\python-jtalk\\jtalkPrepare.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\include\\python-jtalk\\jtalkPrepare.py"
@@ -23,7 +23,7 @@ def convert(msg):
     for p in predic:
         try:
             msg = re.sub(p[0], p[1], msg)
-        except:
+        except Exception:
             pass
     msg = msg.lower()
     return msg

```