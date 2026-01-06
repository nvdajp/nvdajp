# Diff for: `source\md2html.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\md2html.py`  
**Current**: `F:\nvda\gh\alphajp\source\md2html.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\md2html.py" "b/F:\\nvda\\gh\\alphajp\\source\\md2html.py"
index cea5054711..01a39e065d 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\md2html.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\md2html.py"
@@ -163,9 +163,11 @@ def main(source: str, dest: str, lang: str = "en", docType: str | None = None):
 	isDevGuide = docType == "developerGuide"
 	isChanges = docType == "changes"
 	isKeyCommands = docType == "keyCommands"
+	# BEGIN JP PATCH (readmejp support)
 	isReadmejp = docType == "readmejp"
 	if docType and not any([isUserGuide, isDevGuide, isChanges, isKeyCommands, isReadmejp]):
 		raise ValueError(f"Unknown docType {docType}")
+	# END JP PATCH
 	with open(source, "r", encoding="utf-8") as mdFile:
 		mdStr = mdFile.read()
 
@@ -173,10 +175,14 @@ def main(source: str, dest: str, lang: str = "en", docType: str | None = None):
 		mdBuffer.write(mdStr)
 		title = _getTitle(mdBuffer, isKeyCommands)
 
-	if isUserGuide or isDevGuide or isReadmejp:
+	if isUserGuide or isDevGuide:
 		extraStylesheet = '<link rel="stylesheet" href="numberedHeadings.css">'
 	elif isChanges or isKeyCommands:
 		extraStylesheet = ""
+	# BEGIN JP PATCH (readmejp support)
+	elif isReadmejp:
+		extraStylesheet = '<link rel="stylesheet" href="numberedHeadings.css">'
+	# END JP PATCH
 	else:
 		raise ValueError(f"Unknown target type for {dest}")
 
@@ -215,7 +221,9 @@ def main(source: str, dest: str, lang: str = "en", docType: str | None = None):
 		"--docType",
 		help="Type of document",
 		action="store",
+		# BEGIN JP PATCH (readmejp support)
 		choices=["userGuide", "developerGuide", "changes", "keyCommands", "readmejp"],
+		# END JP PATCH
 	)
 	args.add_argument("source", help="Path to the markdown file")
 	args.add_argument("dest", help="Path to the resulting html file")

```