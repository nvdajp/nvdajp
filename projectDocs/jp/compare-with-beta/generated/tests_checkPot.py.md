# Diff for: `tests\checkPot.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\tests\checkPot.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\checkPot.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\checkPot.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\checkPot.py"
index f04efd9..c67747c 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\checkPot.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\checkPot.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2017-2025 NV Access Limited, Ethan Holliger, Dinesh Kaushal, Leonard de Ruijter,
+# Copyright (C) 2017-2023 NV Access Limited, Ethan Holliger, Dinesh Kaushal, Leonard de Ruijter,
 # Joseph Lee, Julien Cochuyt, Łukasz Golonka, Cyrille Bougot
 # This file may be used under the terms of the GNU General Public License, version 2 or later.
 # For more details see: https://www.gnu.org/licenses/gpl-2.0.html
@@ -136,8 +136,8 @@ def checkPot(fileName):
 					# 	"keys are passed to the application"
 					msgid = ""
 					for line in pot:
-						if line.startswith("msgstr ") or line.startswith("msgid_plural"):
-							# This begins the translated or plural message, so msgid has ended.
+						if line.startswith("msgstr "):
+							# This begins the translated message, so msgid has ended.
 							break
 						msgid += getStringFromLine(line)
 				else:

```