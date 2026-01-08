# Diff for: `miscDepsJp\jptools\harness.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\miscDepsJp\jptools\harness.py`  
**Current**: `F:\nvda\gh\alphajp-260109\miscDepsJp\jptools\harness.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\harness.py" "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\harness.py"
index a0acd66..9eb95f7 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\harness.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\harness.py"
@@ -11,6 +11,7 @@
 
 import json
 from pathlib import Path
+
 path = Path(__file__).parent.parent / "include" / "libkuraji" / "tests" / "harness.json"
 data = open(path, encoding="utf-8").read()
 tests = json.loads(data)

```