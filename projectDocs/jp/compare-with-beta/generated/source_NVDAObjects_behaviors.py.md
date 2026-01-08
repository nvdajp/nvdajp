# Diff for: `source\NVDAObjects\behaviors.py`

**Source**: `F:\nvda\gh\beta\source\NVDAObjects\behaviors.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\behaviors.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\behaviors.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\behaviors.py"
index 870d001..74ccab1 100644
--- "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\behaviors.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\behaviors.py"
@@ -636,6 +636,18 @@ class KeyboardHandlerBasedTypedCharSupport(EnhancedTermTypedCharSupport):
 
 class CandidateItem(NVDAObject):
 	def getFormattedCandidateName(self, number, candidate):
+		# BEGIN JP PATCH
+		# nvdajp: use discriminant reading for candidate names when nvdajpEnableKeyEvents is enabled
+		import jpUtils
+
+		if config.conf["keyboard"]["nvdajpEnableKeyEvents"]:
+			fb = braille.handler.displaySize > 0
+			c = jpUtils.getDiscriminantReading(candidate, forBraille=fb)
+			log.debug("{number} {candidate} {c}".format(number=number, candidate=candidate, c=c))
+			if config.conf["language"]["announceCandidateNumber"]:
+				return _("{number} {candidate}").format(number=number, candidate=c)
+			return c
+		# END JP PATCH
 		if config.conf["inputComposition"]["alwaysIncludeShortCharacterDescriptionInCandidateName"]:
 			describedSymbols = []
 			for symbol in candidate:

```