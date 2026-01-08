# Diff for: `source\config\configSpec.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\config\configSpec.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\config\configSpec.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\config\\configSpec.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\configSpec.py"
index 3696b6f..e475b8c 100644
--- "a/F:\\nvda\\gh\\beta\\source\\config\\configSpec.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\configSpec.py"
@@ -29,6 +29,19 @@
 	showWelcomeDialogAtStartup = boolean(default=true)
 	preventDisplayTurningOff = boolean(default=true)
 
+# BEGIN JP PATCH (Japanese language settings)
+[language]
+	jpKatakanaPitchChange = integer(default=-20,min=-100,max=100)
+	halfShapePitchChange = integer(default=20,min=-100,max=100)
+	jpPhoneticReadingLatin = boolean(default=false)
+	jpPhoneticReadingKana = boolean(default=false)
+	announceCandidateNumber = boolean(default=false)
+	jpAnsiEditbox = boolean(default=true)
+	jpAnnounceNewLine = boolean(default=false)
+	openDocFileByMSHTA = boolean(default=false)
+	alwaysSpeakMathInEnglish = boolean(default=false)
+# END JP PATCH
+
 # Speech settings
 [speech]
 	# The synthesizer to use
@@ -69,9 +82,9 @@
 [braille]
 	display = string(default=auto)
 	mode = option("followCursors", "speechOutput", default="followCursors")
-	translationTable = string(default=auto)
-	inputTable = string(default=auto)
-	expandAtCursor = boolean(default=true)
+	translationTable = string(default=ja-jp-comp6.utb) # was en-ueb-g1.ctb (nvdajp)
+	inputTable = string(default=en-ueb-g1.ctb)
+	expandAtCursor = boolean(default=false) # was true (nvdajp)
 	showCursor = boolean(default=true)
 	cursorBlink = boolean(default=true)
 	cursorBlinkRate = integer(default=500,min=200,max=2000)
@@ -190,6 +203,13 @@
 	alertForSpellingErrors = boolean(default=True)
 	handleInjectedKeys= boolean(default=true)
 	multiPressTimeout = integer(default=500, min=100, max=20000)
+	# BEGIN JP PATCH (Japanese keyboard settings)
+	nvdajpEnableKeyEvents = boolean(default=true) #nvdajp
+	nvdajpImeBeep = boolean(default=false) #nvdajp
+	useNonConvertAsNVDAModifierKey = boolean(default=true) #nvdajp
+	useConvertAsNVDAModifierKey = boolean(default=false) #nvdajp
+	useEscapeAsNVDAModifierKey = boolean(default=false) #nvdajp
+	# END JP PATCH
 
 [virtualBuffers]
 	maxLineLength = integer(default=100)
@@ -297,7 +317,9 @@
 	serverURL = string(default="")
 
 [inputComposition]
-	autoReportAllCandidates = boolean(default=True)
+	# BEGIN JP PATCH (Japanese input method default)
+	autoReportAllCandidates = boolean(default=False) # nvdajp
+	# END JP PATCH
 	announceSelectedCandidate = boolean(default=True)
 	alwaysIncludeShortCharacterDescriptionInCandidateName = boolean(default=True)
 	reportReadingStringChanges = boolean(default=True)

```