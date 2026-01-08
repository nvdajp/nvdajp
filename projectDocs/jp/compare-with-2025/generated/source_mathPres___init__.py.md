# Diff for: `source\mathPres\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\mathPres\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\mathPres\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\mathPres\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\mathPres\\__init__.py"
index 6a9214f..5b738f9 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\mathPres\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\mathPres\\__init__.py"
@@ -82,12 +82,12 @@ def registerProvider(
 def initialize() -> None:
 	# Register builtin providers if a plugin hasn't registered others.
 	if not speechProvider or not brailleProvider or not interactionProvider:
-		from . import mathPlayer
+		from .MathCAT import MathCAT
 
 		try:
-			provider = mathPlayer.MathPlayer()
+			provider = MathCAT.MathCAT()
 		except:  # noqa: E722
-			log.warning("MathPlayer 4 not available")
+			log.warning("MathCAT not available.")
 		else:
 			registerProvider(
 				provider,

```