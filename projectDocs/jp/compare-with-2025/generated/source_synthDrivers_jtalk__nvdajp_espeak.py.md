# Diff for: `source\synthDrivers\jtalk\_nvdajp_espeak.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\synthDrivers\jtalk\_nvdajp_espeak.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\synthDrivers\jtalk\_nvdajp_espeak.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\_nvdajp_espeak.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDrivers\\jtalk\\_nvdajp_espeak.py"
index 3a8c2cc..ea09101 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\_nvdajp_espeak.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDrivers\\jtalk\\_nvdajp_espeak.py"
@@ -5,34 +5,24 @@
 from logHandler import log
 import re
 from ._nvdajp_unicode import unicode_normalize
-
-try:
 from speech.commands import CharacterModeCommand
-except:
-    from speech import CharacterModeCommand
-
-
-basestring = str
+from typing import Any, Optional
 
 _logwrite = log.debug
 
 
-def isJapaneseLang(msg):
+def isJapaneseLang(msg: str) -> bool:
 	for i in msg:
 		c = ord(i)
-        if (
-            (0x3000 <= c <= 0x9FFF)
-            or (0xF900 <= c <= 0xFAFF)
-            or (0xFF00 <= c <= 0xFFEF)
-        ):
+		if (0x3000 <= c <= 0x9FFF) or (0xF900 <= c <= 0xFAFF) or (0xFF00 <= c <= 0xFFEF):
 			return True
 	return False
 
 
-kanadic = None
+kanadic: Optional[list[list[Any]]] = None
 
 
-def load_kanadic():
+def load_kanadic() -> list[list[Any]]:
 	return [
 		[re.compile("キュ"), "cu"],
 		[re.compile("キョ"), "co"],
@@ -197,7 +187,7 @@ def load_kanadic():
 	]
 
 
-def replaceJapanese(msg):
+def replaceJapanese(msg: str) -> str:
 	if not translator2.mecab_initialized:
 		translator2.initialize()
 	msg = translator2.japanese_braille_separate(msg, _logwrite)[0]
@@ -208,25 +198,25 @@ def replaceJapanese(msg):
 	for p in kanadic:
 		try:
 			msg = re.sub(p[0], p[1], msg)
-        except:
+		except Exception:
 			pass
 	return msg
 
 
-def replaceJapaneseFromSpeechSequence(speechSequence):
+def replaceJapaneseFromSpeechSequence(speechSequence: list[Any]) -> list[Any]:
 	# we don't want to use CharacterMode for replaced Japanese text
-    a = []
-    charmode = False
+	a: list[Any] = []
+	charmode: bool = False
 	for item in speechSequence:
-        disableCharMode = False
-        if isinstance(item, basestring):
+		disableCharMode: bool = False
+		if isinstance(item, str):
 			item = unicode_normalize(item)
 			if isJapaneseLang(item):
 				item = replaceJapanese(item)
 				if charmode:
 					disableCharMode = True
 		elif isinstance(item, CharacterModeCommand):
-            cmstate = item.state
+			pass  # cmstate: bool = item.state  # unused
 		if disableCharMode:
 			a.append(CharacterModeCommand(False))
 			a.append(item)

```