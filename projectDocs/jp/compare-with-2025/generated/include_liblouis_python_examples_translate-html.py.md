# Diff for: `include\liblouis\python\examples\translate-html.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\include\liblouis\python\examples\translate-html.py`  
**Current**: `F:\nvda\gh\alphajp\include\liblouis\python\examples\translate-html.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\include\\liblouis\\python\\examples\\translate-html.py" "b/F:\\nvda\\gh\\alphajp\\include\\liblouis\\python\\examples\\translate-html.py"
index 307b74297b..2d57252fb8 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\include\\liblouis\\python\\examples\\translate-html.py"
+++ "b/F:\\nvda\\gh\\alphajp\\include\\liblouis\\python\\examples\\translate-html.py"
@@ -19,6 +19,7 @@
 """
 
 import textwrap
+
 import louis
 from lxml import html
 
@@ -37,4 +38,4 @@
                 outputFile.write(textwrap.fill(translation, lineLength))
                 outputFile.write("\n")
 
-print ("Done.")
+print("Done.")

```