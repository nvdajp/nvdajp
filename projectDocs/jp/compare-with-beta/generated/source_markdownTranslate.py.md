# Diff for: `source\markdownTranslate.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\markdownTranslate.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\markdownTranslate.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\markdownTranslate.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\markdownTranslate.py"
index 0e9e333..341ead6 100644
--- "a/F:\\nvda\\gh\\beta\\source\\markdownTranslate.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\markdownTranslate.py"
@@ -4,7 +4,6 @@
 # See the file COPYING for more details.
 
 from typing import Generator
-from collections.abc import Iterable
 import tempfile
 import os
 import contextlib
@@ -30,7 +29,6 @@
 re_postTableHeaderLine = re.compile(r"^(\|\s*-+\s*)+\|$")
 re_tableRow = re.compile(r"^(\|)(.+)(\|)$")
 re_translationID = re.compile(r"^(.*)\$\(ID:([0-9a-f-]+)\)(.*)$")
-re_inlineMarkdownLintComment = re.compile(r"^(.*?)(?:\s*<!-- markdownlint.*-->)(\s*)$")
 
 
 def prettyPathString(path: str) -> str:
@@ -90,18 +88,6 @@ def getRawGithubURLForPath(filePath: str) -> str:
 	return f"{RAW_GITHUB_REPO_URL}/{commitID}/{relativePath}"
 
 
-def preprocessMarkdownLines(mdLines: Iterable[str]) -> Iterable[str]:
-	"""
-	Preprocess markdown lines such as removing inline markdown lint comments.\
-	:param mdLines: The markdown lines to preprocess
-	:returns: The preprocessed markdown lines
-	"""
-	for mdLine in mdLines:
-		# #18982: Remove markdown lint comments completely - not needed for intermediate markdown or final html.
-		mdLine = re_inlineMarkdownLintComment.sub(r"\1\2", mdLine)
-		yield mdLine
-
-
 def skeletonizeLine(mdLine: str) -> str | None:
 	prefix = ""
 	suffix = ""
@@ -143,7 +129,7 @@ def generateSkeleton(mdPath: str, outputPath: str) -> Result_generateSkeleton:
 		open(mdPath, "r", encoding="utf8") as mdFile,
 		open(outputPath, "w", encoding="utf8", newline="") as outputFile,
 	):
-		for mdLine in preprocessMarkdownLines(mdFile.readlines()):
+		for mdLine in mdFile.readlines():
 			res.numTotalLines += 1
 			skelLine = skeletonizeLine(mdLine)
 			if skelLine:
@@ -199,9 +185,7 @@ def updateSkeleton(
 		newMdFile = stack.enter_context(open(newMdPath, "r", encoding="utf8"))
 		origSkelFile = stack.enter_context(open(origSkelPath, "r", encoding="utf8"))
 		outputFile = stack.enter_context(open(outputPath, "w", encoding="utf8", newline=""))
-		origMdLines = preprocessMarkdownLines(origMdFile.readlines())
-		newMdLines = preprocessMarkdownLines(newMdFile.readlines())
-		mdDiff = difflib.ndiff(list(origMdLines), list(newMdLines))
+		mdDiff = difflib.ndiff(origMdFile.readlines(), newMdFile.readlines())
 		origSkelLines = iter(origSkelFile.readlines())
 		for mdDiffLine in mdDiff:
 			if mdDiffLine.startswith("?"):
@@ -277,10 +261,7 @@ def generateXliff(
 		outputFile.write(f"<skeleton>\n{xmlEscape(skelContent)}\n</skeleton>\n")
 		res.numTranslatableStrings = 0
 		for lineNo, (mdLine, skelLine) in enumerate(
-			zip_longest(
-				preprocessMarkdownLines(mdFile.readlines()),
-				skelContent.splitlines(keepends=True),
-			),
+			zip_longest(mdFile.readlines(), skelContent.splitlines(keepends=True)),
 			start=1,
 		):
 			mdLine = mdLine.rstrip()
@@ -380,10 +361,7 @@ def translateXliff(
 			raise ValueError("No skeleton found in xliff file")
 		skeletonContent = skeletonNode.text.strip()
 		for lineNo, (skelLine, pretranslatedLine) in enumerate(
-			zip_longest(
-				skeletonContent.splitlines(),
-				preprocessMarkdownLines(pretranslatedMdFile.readlines()),
-			),
+			zip_longest(skeletonContent.splitlines(), pretranslatedMdFile.readlines()),
 			start=1,
 		):
 			skelLine = skelLine.rstrip()
@@ -504,13 +482,7 @@ def ensureMarkdownFilesMatch(path1: str, path2: str, allowBadAnchors: bool = Fal
 	with contextlib.ExitStack() as stack:
 		file1 = stack.enter_context(open(path1, "r", encoding="utf8"))
 		file2 = stack.enter_context(open(path2, "r", encoding="utf8"))
-		for lineNo, (line1, line2) in enumerate(
-			zip_longest(
-				preprocessMarkdownLines(file1.readlines()),
-				preprocessMarkdownLines(file2.readlines()),
-			),
-			start=1,
-		):
+		for lineNo, (line1, line2) in enumerate(zip_longest(file1.readlines(), file2.readlines()), start=1):
 			line1 = line1.rstrip()
 			line2 = line2.rstrip()
 			if line1 != line2:

```