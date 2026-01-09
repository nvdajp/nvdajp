# Diff for: `source\updateCheck.py`

**Source**: `F:\nvda\gh\beta\source\updateCheck.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\updateCheck.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\updateCheck.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\updateCheck.py"
index c95eda7..c6c234f 100644
--- "a/F:\\nvda\\gh\\beta\\source\\updateCheck.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\updateCheck.py"
@@ -79,9 +79,10 @@
 	_deprecate.MovedSymbol("CERT_CHAIN_PARA", "winBindings.crypt32"),
 )
 
-
 #: The URL to use for update checks.
-_DEFAULT_CHECK_URL = "https://api.nvaccess.org/nvdaUpdateCheck"
+# BEGIN JP PATCH (Japanese update server URL)
+_DEFAULT_CHECK_URL = "https://www.nvda.jp/updateCheck/"
+# END JP PATCH
 #: The time to wait between checks.
 CHECK_INTERVAL = 86400  # 1 day
 #: The time to wait before retrying a failed check.

```