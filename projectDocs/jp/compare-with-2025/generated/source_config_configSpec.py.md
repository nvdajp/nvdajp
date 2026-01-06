# Diff for: `source\config\configSpec.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\config\configSpec.py`  
**Current**: `F:\nvda\gh\alphajp\source\config\configSpec.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\config\\configSpec.py" "b/F:\\nvda\\gh\\alphajp\\source\\config\\configSpec.py"
index bbd5982bfa..225bb97078 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\config\\configSpec.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\config\\configSpec.py"
@@ -13,7 +13,7 @@
 #: provide an upgrade step (@see profileUpgradeSteps.py). An upgrade step does not need to be added when
 #: just adding a new element to (or removing from) the schema, only when old versions of the config
 #: (conforming to old schema versions) will not work correctly with the new schema.
-latestSchemaVersion = 18
+latestSchemaVersion = 19
 
 #: The configuration specification string
 #: @type: String
@@ -29,7 +29,7 @@
 	showWelcomeDialogAtStartup = boolean(default=true)
 	preventDisplayTurningOff = boolean(default=true)
 
-# nvdajp
+# BEGIN JP PATCH (Japanese language settings)
 [language]
 	jpKatakanaPitchChange = integer(default=-20,min=-100,max=100)
 	halfShapePitchChange = integer(default=20,min=-100,max=100)
@@ -40,6 +40,7 @@
 	jpAnnounceNewLine = boolean(default=false)
 	openDocFileByMSHTA = boolean(default=false)
 	alwaysSpeakMathInEnglish = boolean(default=false)
+# END JP PATCH
 
 # Speech settings
 [speech]
@@ -103,9 +104,6 @@
 	wordWrap = boolean(default=true)
 	unicodeNormalization = featureFlag(optionsEnum="BoolFlag", behaviorOfDefault="disabled")
 	focusContextPresentation = option("changedContext", "fill", "scroll", default="changedContext")
-	nvdajpMessageTimeout = boolean(default=true) # obsolete (nvdajp)
-	japaneseBrailleSupport = boolean(default=true) # obsolete (nvdajp)
-	nvdajpComPort = integer(default=0) # obsolete (nvdajp)
 	interruptSpeechWhileScrolling = featureFlag(optionsEnum="BoolFlag", behaviorOfDefault="enabled")
 	speakOnRouting = boolean(default=false)
 	speakOnNavigatingByUnit = boolean(default=false)
@@ -131,6 +129,7 @@
 		reportKeyboardShortcuts = boolean(default=true)
 		reportObjectPositionInformation = boolean(default=true)
 		guessObjectPositionInformationWhenUnavailable = boolean(default=false)
+		reportMultiSelect = boolean(default=false)
 		reportTooltips = boolean(default=false)
 		reportHelpBalloons = boolean(default=true)
 		reportObjectDescriptions = boolean(default=True)
@@ -186,11 +185,6 @@
 
 #Keyboard settings
 [keyboard]
-	nvdajpEnableKeyEvents = boolean(default=true) #nvdajp
-	nvdajpImeBeep = boolean(default=false) #nvdajp
-	useNonConvertAsNVDAModifierKey = boolean(default=true) #nvdajp
-	useConvertAsNVDAModifierKey = boolean(default=false) #nvdajp
-	useEscapeAsNVDAModifierKey = boolean(default=false)
 	# NVDAModifierKeys: Integer value combining single-bit value:
 	# 1: CapsLock
 	# 2: NumpadInsert
@@ -210,6 +204,13 @@
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
@@ -246,7 +247,9 @@
 	reportAlignment = boolean(default=false)
 	reportLineSpacing = boolean(default=false)
 	reportStyle = boolean(default=false)
-	reportSpellingErrors = boolean(default=true)
+	# Bitwise combination of none, some or all values of ReportSpellingErrors
+	# 1: Speech, 2: Sound
+	reportSpellingErrors2 = integer(min=0, max=3, default=1)
 	reportPage = boolean(default=true)
 	reportLineNumber = boolean(default=False)
 	# 0: Off, 1: Speech, 2: Tones, 3: Both Speech and Tones
@@ -313,7 +316,9 @@
 	serverURL = string(default="")
 
 [inputComposition]
+	# BEGIN JP PATCH (Japanese input method default)
 	autoReportAllCandidates = boolean(default=False) # nvdajp
+	# END JP PATCH
 	announceSelectedCandidate = boolean(default=True)
 	alwaysIncludeShortCharacterDescriptionInCandidateName = boolean(default=True)
 	reportReadingStringChanges = boolean(default=True)
@@ -337,6 +342,7 @@
 	garbageHandler = boolean(default=false)
 	remoteClient = boolean(default=False)
 	externalPythonDependencies = boolean(default=False)
+	bdDetect = boolean(default=False)
 
 [uwpOcr]
 	language = string(default="")

```