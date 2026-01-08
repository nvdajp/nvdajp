# Diff for: `miscDepsJp\jptools\mecabHarness.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\miscDepsJp\jptools\mecabHarness.py`  
**Current**: `F:\nvda\gh\alphajp-260109\miscDepsJp\jptools\mecabHarness.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\mecabHarness.py" "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\mecabHarness.py"
index 967c14f..29206d1 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\mecabHarness.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\mecabHarness.py"
@@ -10,6 +10,7 @@
 
 import json
 from pathlib import Path
+
 path = Path(__file__).parent.parent / "include" / "libkuraji" / "tests" / "mecabHarness.json"
 data = open(path, encoding="utf-8").read()
 tasks = json.loads(data)

```