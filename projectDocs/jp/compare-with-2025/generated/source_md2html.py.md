# Diff for: `source\md2html.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\md2html.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\md2html.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\md2html.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\md2html.py"
index cea5054..57a3c03 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\md2html.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\md2html.py"
@@ -9,6 +9,7 @@
 import re
 import shutil
 from typing import Any
+from l2m4m import LaTeX2MathMLExtension
 
 _DEFAULT_EXTENSIONS_ORDERED = (
 	# Supports tables, HTML mixed with markdown, code blocks, custom attributes and more
@@ -23,6 +24,8 @@
 	"markdown_link_attr_modifier",
 	# Adds links to GitHub authors, issues and PRs
 	"mdx_gh_links",
+	# Converts LaTeX to MathML
+	LaTeX2MathMLExtension(),
 )
 """
 Default extensions to use for markdown conversion.
@@ -122,10 +125,28 @@ def _createAttributeFilter() -> dict[str, set[str]]:
 	# link rel and target is set by markdown_link_attr_modifier
 	allowedAttributes["a"].update({"rel", "target"})
 
+	if "math" not in allowedAttributes:
+		allowedAttributes["math"] = set()
+	allowedAttributes["math"].add("display")
+
 	return allowedAttributes
 
 
+def _attributeFilter(tag: str, attr: str, value: str) -> str | None:
+	# Specifying display=inline is redundant
+	if tag == "math" and attr == "display":
+		return value if value == "block" else None
+	return value
+
+
+def _createTagFilter() -> set[str]:
+	import nh3
+
+	return nh3.ALLOWED_TAGS | {"math", "mrow", "mfrac", "mi", "mn", "mo", "msub"}
+
+
 ALLOWED_ATTRIBUTES = _createAttributeFilter()
+ALLOWED_TAGS = _createTagFilter()
 
 
 def _generateSanitizedHTML(md: str, isKeyCommands: bool = False) -> str:
@@ -147,7 +168,9 @@ def _generateSanitizedHTML(md: str, isKeyCommands: bool = False) -> str:
 	# Sanitize html output from markdown to prevent XSS from translators
 	htmlOutput = nh3.clean(
 		htmlOutput,
+		tags=ALLOWED_TAGS,
 		attributes=ALLOWED_ATTRIBUTES,
+		attribute_filter=_attributeFilter,
 		# link rel is handled by markdown_link_attr_modifier
 		link_rel=None,
 		# Keep key command comments and similar
@@ -163,9 +186,11 @@ def main(source: str, dest: str, lang: str = "en", docType: str | None = None):
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
 
@@ -173,10 +198,14 @@ def main(source: str, dest: str, lang: str = "en", docType: str | None = None):
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
 
@@ -215,7 +244,9 @@ def main(source: str, dest: str, lang: str = "en", docType: str | None = None):
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