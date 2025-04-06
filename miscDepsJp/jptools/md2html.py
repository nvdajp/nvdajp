#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Convert Markdown to HTML

import sys
import markdown
import codecs

def convert_md_to_html(md_file, html_file):
    """Convert Markdown file to HTML file."""
    with codecs.open(md_file, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # Convert Markdown to HTML with TOC extension
    html = markdown.markdown(md_text, extensions=['toc'])

    # Add HTML header and footer
    html_doc = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>NVDA 日本語版 点訳テストケース</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1, h2, h3 {{ color: #333; }}
        .toc {{ background-color: #f8f8f8; padding: 10px; border: 1px solid #ddd; }}
    </style>
</head>
<body>
{html}
</body>
</html>
"""

    with codecs.open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_doc)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python md2html.py input.md output.html")
        sys.exit(1)

    md_file = sys.argv[1]
    html_file = sys.argv[2]
    convert_md_to_html(md_file, html_file)
    print(f"Converted {md_file} to {html_file}")
