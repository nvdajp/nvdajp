# Diff for: `miscDepsJp\jptools\nabccHarness.py`

**Source**: `F:\nvda\gh\alphajp-251219\miscDepsJp\jptools\nabccHarness.py`  
**Current**: `F:\nvda\gh\alphajp-260109\miscDepsJp\jptools\nabccHarness.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\nabccHarness.py" "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\nabccHarness.py"
index b94fd1d..840553e 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\nabccHarness.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\nabccHarness.py"
@@ -16,6 +16,7 @@
 
 import json
 from pathlib import Path
+
 path = Path(__file__).parent.parent / "include" / "libkuraji" / "tests" / "nabccHarness.json"
 data = open(path, encoding="utf-8").read()
 tests = json.loads(data)

```