# Diff for: `tests\system\robot\automatedImageDescriptions.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\tests\system\robot\automatedImageDescriptions.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\system\robot\automatedImageDescriptions.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\system\\robot\\automatedImageDescriptions.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\robot\\automatedImageDescriptions.py"
index bfbd6b3..965071e 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\system\\robot\\automatedImageDescriptions.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\robot\\automatedImageDescriptions.py"
@@ -37,7 +37,7 @@ def NVDA_Caption():
 
 	# locate graph to generate caption
 	spy.emulateKeyPress("g")
-	spy.emulateKeyPress("NVDA+g")
+	spy.emulateKeyPress("NVDA+windows+,")
 	spy.wait_for_specific_speech(
 		"visual desk access non-visual desktop access non-visual desktop access non-visual desktop access non-visual desktop access non-visual desktop access non-visual",
 	)

```