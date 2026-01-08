# Diff for: `source\md2html.py`

**Source**: `F:\nvda\gh\beta\source\md2html.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\md2html.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\md2html.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\md2html.py"
index 6f96e3c..57a3c03 100644
--- "a/F:\\nvda\\gh\\beta\\source\\md2html.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\md2html.py"
@@ -186,8 +186,11 @@ def main(source: str, dest: str, lang: str = "en", docType: str | None = None):
 	isDevGuide = docType == "developerGuide"
 	isChanges = docType == "changes"
 	isKeyCommands = docType == "keyCommands"
-	if docType and not any([isUserGuide, isDevGuide, isChanges, isKeyCommands]):
+	# BEGIN JP PATCH (readmejp support)
+	isReadmejp = docType == "readmejp"
+	if docType and not any([isUserGuide, isDevGuide, isChanges, isKeyCommands, isReadmejp]):
 		raise ValueError(f"Unknown docType {docType}")
+	# END JP PATCH
 	with open(source, "r", encoding="utf-8") as mdFile:
 		mdStr = mdFile.read()
 
@@ -199,6 +202,10 @@ def main(source: str, dest: str, lang: str = "en", docType: str | None = None):
 		extraStylesheet = '<link rel="stylesheet" href="numberedHeadings.css">'
 	elif isChanges or isKeyCommands:
 		extraStylesheet = ""
+	# BEGIN JP PATCH (readmejp support)
+	elif isReadmejp:
+		extraStylesheet = '<link rel="stylesheet" href="numberedHeadings.css">'
+	# END JP PATCH
 	else:
 		raise ValueError(f"Unknown target type for {dest}")
 
@@ -237,7 +244,9 @@ def main(source: str, dest: str, lang: str = "en", docType: str | None = None):
 		"--docType",
 		help="Type of document",
 		action="store",
-		choices=["userGuide", "developerGuide", "changes", "keyCommands"],
+		# BEGIN JP PATCH (readmejp support)
+		choices=["userGuide", "developerGuide", "changes", "keyCommands", "readmejp"],
+		# END JP PATCH
 	)
 	args.add_argument("source", help="Path to the markdown file")
 	args.add_argument("dest", help="Path to the resulting html file")

```