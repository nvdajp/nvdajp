# Diff for: `source\utils\urlUtils.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\utils\urlUtils.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\utils\urlUtils.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\utils\\urlUtils.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\utils\\urlUtils.py"
index 6316907..eee0a51 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\utils\\urlUtils.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\utils\\urlUtils.py"
@@ -40,10 +40,18 @@ def isSamePageURL(targetURLOnPage: str, rootURL: str) -> bool:
 
 	validSchemes = ("http", "https", "file")
 	# Parse the URLs
+	try:
 		parsedTargetURLOnPage: ParseResult = urlparse(targetURLOnPage)
+	except ValueError:
+		log.debugWarning(f"Invalid target URL: {targetURLOnPage}", exc_info=True)
+		return False
 	if parsedTargetURLOnPage.scheme not in validSchemes:
 		return False
+	try:
 		parsedRootURL: ParseResult = urlparse(rootURL)
+	except ValueError:
+		log.debugWarning(f"Invalid root URL: {rootURL}", exc_info=True)
+		return False
 	if parsedRootURL.scheme not in validSchemes:
 		return False
 

```