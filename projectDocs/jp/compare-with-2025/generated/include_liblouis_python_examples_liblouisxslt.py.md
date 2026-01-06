# Diff for: `include\liblouis\python\examples\liblouisxslt.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\include\liblouis\python\examples\liblouisxslt.py`  
**Current**: `F:\nvda\gh\alphajp\include\liblouis\python\examples\liblouisxslt.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\include\\liblouis\\python\\examples\\liblouisxslt.py" "b/F:\\nvda\\gh\\alphajp\\include\\liblouis\\python\\examples\\liblouisxslt.py"
index 2f1267b57c..5a1ec2b180 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\include\\liblouis\\python\\examples\\liblouisxslt.py"
+++ "b/F:\\nvda\\gh\\alphajp\\include\\liblouis\\python\\examples\\liblouisxslt.py"
@@ -14,21 +14,22 @@
 # dtbook2brldtbook.xsl in the same directory which simpy copies a dtbook
 # xml and translates all the text node into Braille.
 
-import louis
+from optparse import OptionParser
+
 import libxml2
 import libxslt
-import sys
-import getopt
-from optparse import OptionParser
+import louis
 
 nodeName = None
 
 emphasisMap = {
-    'plain_text' : louis.plain_text, 
-    'italic' : louis.italic, 
-    'underline' : louis.underline, 
-    'bold' : louis.bold, 
-    'computer_braille' : louis.computer_braille}
+    "plain_text": louis.plain_text,
+    "italic": louis.italic,
+    "underline": louis.underline,
+    "bold": louis.bold,
+    "computer_braille": louis.computer_braille,
+}
+
 
 def translate(ctx, str, translation_table, emphasis=None):
     global nodeName
@@ -42,8 +43,11 @@ def translate(ctx, str, translation_table, emphasis=None):
         pass
 
     typeform = len(str) * [emphasisMap[emphasis]] if emphasis else None
-    braille = louis.translate([translation_table], str.decode('utf-8'), typeform=typeform)[0]
-    return braille.encode('utf-8')
+    braille = louis.translate(
+        [translation_table], str.decode("utf-8"), typeform=typeform
+    )[0]
+    return braille.encode("utf-8")
+
 
 def xsltProcess(styleFile, inputFile, outputFile):
     """Transform an xml inputFile to an outputFile using the given styleFile"""
@@ -56,7 +60,11 @@ def xsltProcess(styleFile, inputFile, outputFile):
     doc.freeDoc()
     result.freeDoc()
 
-libxslt.registerExtModuleFunction("translate", "http://liblouis.org/liblouis", translate)
+
+libxslt.registerExtModuleFunction(
+    "translate", "http://liblouis.org/liblouis", translate
+)
+
 
 def main():
     usage = "Usage: %prog [options] styleFile inputFile outputFile"
@@ -66,5 +74,6 @@ def main():
         parser.error("incorrect number of arguments")
     xsltProcess(args[0], args[1], args[2])
 
+
 if __name__ == "__main__":
     main()

```