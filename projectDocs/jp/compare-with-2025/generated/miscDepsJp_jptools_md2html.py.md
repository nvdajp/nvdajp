# Diff for: `miscDepsJp\jptools\md2html.py`

**Source**: `F:\nvda\gh\alphajp-251219\miscDepsJp\jptools\md2html.py`  
**Current**: `F:\nvda\gh\alphajp-260109\miscDepsJp\jptools\md2html.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\md2html.py" "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\md2html.py"
index 0f619ca..eec0c5b 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\miscDepsJp\\jptools\\md2html.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\miscDepsJp\\jptools\\md2html.py"
@@ -4,15 +4,15 @@
 
 import sys
 import markdown
-import codecs
+
 
 def convert_md_to_html(md_file, html_file):
 	"""Convert Markdown file to HTML file."""
-    with codecs.open(md_file, 'r', encoding='utf-8') as f:
+	with open(md_file, "r", encoding="utf-8") as f:
 		md_text = f.read()
 
 	# Convert Markdown to HTML with TOC extension
-    html = markdown.markdown(md_text, extensions=['toc'])
+	html = markdown.markdown(md_text, extensions=["toc"])
 
 	# Add HTML header and footer
 	html_doc = f"""<!DOCTYPE html>
@@ -32,9 +32,10 @@ def convert_md_to_html(md_file, html_file):
 </html>
 """
 
-    with codecs.open(html_file, 'w', encoding='utf-8') as f:
+	with open(html_file, "w", encoding="utf-8") as f:
 		f.write(html_doc)
 
+
 if __name__ == "__main__":
 	if len(sys.argv) < 3:
 		print("Usage: python md2html.py input.md output.html")

```