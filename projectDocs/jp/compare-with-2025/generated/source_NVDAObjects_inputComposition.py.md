# Diff for: `source\NVDAObjects\inputComposition.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\inputComposition.py`  
**Current**: `F:\nvda\gh\alphajp\source\NVDAObjects\inputComposition.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\inputComposition.py" "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\inputComposition.py"
index a889533b27..78c1310c53 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\inputComposition.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\inputComposition.py"
@@ -189,11 +189,11 @@ def reportNewText(self, oldString, newString, forceNewText=False):
 				queueHandler.queueFunction(
 					queueHandler.eventQueue, braille.handler.message, newTextForBraille
 				)
-			if (
-				config.conf["keyboard"]["speakTypedCharacters"] != TypingEcho.OFF.value
-				or config.conf["keyboard"]["speakTypedWords"] != TypingEcho.OFF.value
+		if (
+			config.conf["keyboard"]["speakTypedCharacters"] != TypingEcho.OFF.value
+			or config.conf["keyboard"]["speakTypedWords"] != TypingEcho.OFF.value
 				or isCandidate
-			):
+		):
 				queueHandler.queueFunction(
 					queueHandler.eventQueue,
 					speech.speakText,

```