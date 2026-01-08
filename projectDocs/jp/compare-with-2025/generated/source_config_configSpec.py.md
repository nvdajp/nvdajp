# Diff for: `source\config\configSpec.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\config\configSpec.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\config\configSpec.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\config\\configSpec.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\configSpec.py"
index bbd5982..e475b8c 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\config\\configSpec.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\configSpec.py"
@@ -13,7 +13,7 @@
 #: provide an upgrade step (@see profileUpgradeSteps.py). An upgrade step does not need to be added when
 #: just adding a new element to (or removing from) the schema, only when old versions of the config
 #: (conforming to old schema versions) will not work correctly with the new schema.
-latestSchemaVersion = 18
+latestSchemaVersion = 20
 
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
@@ -59,10 +60,9 @@
 	delayedCharacterDescriptions = boolean(default=false)
 	excludedSpeechModes = int_list(default=list())
 	trimLeadingSilence = boolean(default=true)
-	useWASAPIForSAPI4 = featureFlag(optionsEnum="BoolFlag", behaviorOfDefault="enabled")
 
 	[[__many__]]
-		capPitchChange = integer(default=0,min=-100,max=100)
+		capPitchChange = integer(default=30,min=-100,max=100)
 		sayCapForCapitals = boolean(default=false)
 		beepForCapitals = boolean(default=false)
 		useSpellingFunctionality = boolean(default=true)
@@ -103,9 +103,6 @@
 	wordWrap = boolean(default=true)
 	unicodeNormalization = featureFlag(optionsEnum="BoolFlag", behaviorOfDefault="disabled")
 	focusContextPresentation = option("changedContext", "fill", "scroll", default="changedContext")
-	nvdajpMessageTimeout = boolean(default=true) # obsolete (nvdajp)
-	japaneseBrailleSupport = boolean(default=true) # obsolete (nvdajp)
-	nvdajpComPort = integer(default=0) # obsolete (nvdajp)
 	interruptSpeechWhileScrolling = featureFlag(optionsEnum="BoolFlag", behaviorOfDefault="enabled")
 	speakOnRouting = boolean(default=false)
 	speakOnNavigatingByUnit = boolean(default=false)
@@ -131,6 +128,7 @@
 		reportKeyboardShortcuts = boolean(default=true)
 		reportObjectPositionInformation = boolean(default=true)
 		guessObjectPositionInformationWhenUnavailable = boolean(default=false)
+		reportMultiSelect = boolean(default=false)
 		reportTooltips = boolean(default=false)
 		reportHelpBalloons = boolean(default=true)
 		reportObjectDescriptions = boolean(default=True)
@@ -186,11 +184,6 @@
 
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
@@ -210,6 +203,13 @@
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
@@ -246,12 +246,16 @@
 	reportAlignment = boolean(default=false)
 	reportLineSpacing = boolean(default=false)
 	reportStyle = boolean(default=false)
-	reportSpellingErrors = boolean(default=true)
+	# Bitwise combination of none, some or all values of ReportSpellingErrors
+	# 1: Speech, 2: Sound, 4: Braille
+	reportSpellingErrors2 = integer(min=0, max=7, default=1)
 	reportPage = boolean(default=true)
 	reportLineNumber = boolean(default=False)
 	# 0: Off, 1: Speech, 2: Tones, 3: Both Speech and Tones
 	reportLineIndentation = integer(0, 3, default=0)
 	ignoreBlankLinesForRLI = boolean(default=False)
+	# Duration of indentation beeps, in milliseconds
+	indentToneDuration = integer(min=10, max=2000, default=40)
 	reportParagraphIndentation = boolean(default=False)
 	reportTables = boolean(default=true)
 	includeLayoutTables = boolean(default=False)
@@ -313,7 +317,9 @@
 	serverURL = string(default="")
 
 [inputComposition]
+	# BEGIN JP PATCH (Japanese input method default)
 	autoReportAllCandidates = boolean(default=False) # nvdajp
+	# END JP PATCH
 	announceSelectedCandidate = boolean(default=True)
 	alwaysIncludeShortCharacterDescriptionInCandidateName = boolean(default=True)
 	reportReadingStringChanges = boolean(default=True)
@@ -337,11 +343,13 @@
 	garbageHandler = boolean(default=false)
 	remoteClient = boolean(default=False)
 	externalPythonDependencies = boolean(default=False)
+	bdDetect = boolean(default=False)
 
 [uwpOcr]
 	language = string(default="")
 	autoRefresh = boolean(default=false)
 	autoRefreshInterval = integer(default=1500, min=100)
+	autoSayAllOnResult = boolean(default=false)
 
 [editableText]
 	caretMoveTimeoutMs = integer(min=0, max=2000, default=100)
@@ -383,6 +391,174 @@
 	[[ui]]
 		confirmDisconnectAsFollower = boolean(default=True)
 		muteOnLocalControl = boolean(default=False)
+
+[math]
+	[[speech]]
+		# LearningDisability, Blindness, LowVision
+    	impairment = string(default="Blindness")
+		# any known language code and sub-code -- could be en-uk, etc
+    	language = string(default="Auto")
+		# Any known speech style (falls back to ClearSpeak)
+    	speechStyle = string(default="ClearSpeak")
+		# Terse, Medium, Verbose
+    	verbosity = string(default="Medium")
+		# Change from text speech rate (%)
+    	mathRate = integer(default=100)
+		# Change from normal pause length (%)
+    	pauseFactor = integer(default=100)
+		# make a sound when starting/ending math speech -- None, Beep
+    	speechSound = string(default="None")
+		# NOTE: not currently working in MathCAT
+    	subjectArea = string(default="General")
+		# SpellOut (H 2 0), AsCompound (Water) -- not implemented, Off (H sub 2 O)
+    	chemistry = string(default="SpellOut")
+		# Verbose, Brief, SuperBrief
+		mathSpeak = string(default="Verbose")
+
+		[[speech.speechOverrides]]
+			# word to say as a prefix/postfix for capital letters; empty string leaves it calling AT with Unicode fallback
+			capitalLetters = string(default="")
+			# word used as override (not implemented)
+			leftParen = string(default="")
+			# word used as override (not implemented)
+			rightParen = string(default="")
+
+		# see ClearSpeak speak for meanings
+		[[speech.ClearSpeak]]
+			# SayCaps or use pitch
+			capitalLetters = string(default="Auto")
+			# Valid values: AbsEnd, Cardinality, Determinant, Auto
+			absoluteValue = string(default="Auto")
+			# Valid values: Ordinal, Over, FracOver, General, EndFrac, GeneralEndFrac, OverEndFrac, Per, Auto
+			fractions = string(default="Auto")
+			# Valid values: Ordinal, OrdinalPower, AfterPower, Auto
+			exponents = string(default="Auto")
+			# Valid values: PosNegSqRoot, RootEnd, PosNegSqRootEnd, Auto
+			roots = string(default="Auto")
+			# Valid values: Auto, None
+			functions = string(default="Auto")
+			# Valid values: TrigInverse, ArcTrig, Auto
+			trig = string(default="Auto")
+			# Valid values: LnAsNaturalLog, Auto
+			log = string(default="Auto")
+			# Valid values: MoreImpliedTimes , None, Auto
+			impliedTimes = string(default="Auto")
+			# Valid values: Speak, SpeakNestingLevel, Silent, CoordPoint, Interval, Auto
+			paren = string(default="Auto")
+			# Valid values: SpeakColNum, SilentColNum, EndMatrix, Vector, EndVector, Combinatorics, Auto
+			matrix = string(default="Auto")
+			# Valid values: Case, Constraint, Equation, Line, None, Row, Step, Auto
+			multiLineLabel = string(default="Auto")
+			# Valid values: None, Auto
+			multiLineOverview = string(default="Auto")
+			# Valid values: Long, Short
+			multiLinePausesBetweenColumns = string(default="Short")
+			# Valid values: woAll, SilentBracket, Auto
+			sets = string(default="Auto")
+			# Valid values: By, Cross, Auto
+			multSymbolX = string(default="Auto")
+			# Valid values: Dot, Auto
+			multSymbolDot = string(default="Auto")
+			# Valid values: Delta, Auto
+			triangleSymbol = string(default="Auto")
+			# Valid values: AndSoOn, Auto
+			ellipses = string(default="Auto")
+			# Valid values: SuchThat, Divides, Given, Auto
+			verticalLine = string(default="Auto")
+			# Valid values: Belongs, Element, Member, Auto
+			setMemberSymbol = string(default="Auto")
+			# Valid values: Angle, Length, Auto
+			prime = string(default="Auto")
+			# Valid values: ChoosePermute, Auto
+			combinationPermutation = string(default="Auto")
+			# Valid values: Bar, Conjugate, Mean, Auto
+			bar = string(default="Auto")
+
+	[[navigation]]
+		# Valid values: Enhanced, Simple, Character
+		navMode = string(default="Enhanced")
+		# remember previous value and use it
+		resetNavMode = boolean(default=false)
+		# speak the expression or give a description/overview
+		overview = boolean(default=false)
+		# remember previous value and use it
+		resetOverview = boolean(default=true)
+		# Terse, Medium, Full (words to say for nav command)
+		navVerbosity = string(default="Medium")
+		# Auto zoom out of 2D exprs (use shift-arrow to force zoom out if unchecked)
+		autoZoomOut = boolean(default=true)
+		# MathML, LaTeX, ASCIIMath
+		copyAs = string(default="MathML")
+
+	[[braille]]
+		# Any supported Braille code (such as UEB) or "Auto"
+		brailleCode = string(default="Auto")
+		# Highlight with dots 7 & 8 the current nav node -- values are Off, FirstChar, EndPoints, All
+		brailleNavHighlight = string(default="EndPoints")
+		# true/false
+		useSpacesAroundAllOperators = boolean(default=false)
+
+		[[braille.nemeth]]
+			# Nemeth defines the typeforms: Bold, Italic, SansSerif, and Script. That leaves out DoubleStruck (Blackboard Bold)
+			# Here we provide an option to specify a transcriber-defined typeform changes, with the default mapping DoubleStruck to Italic
+			# first transcriber-defined typeform prefix indicator
+			sansSerif = string(default="⠠⠨")
+			bold = string(default="⠸")
+			doubleStruck = string(default="⠨")
+			script = string(default="⠈")
+			italic = string(default="⠨")
+
+		[[braille.UEB]]
+		   	# Grade1/Grade2 -- assumed starting mode UEB braille (Grade1 assumes we are in G1 passage mode)
+			startMode = string(default="Grade2")
+			# true/false
+			useSpacesAroundAllOperators = string(default=false)
+
+			# UEB Guide to Technical Material (https://iceb.org/Guidelines_for_Technical_Material_2008-10.pdf)
+			#   says to normally treat Fraktur and DoubleStruck as Script
+			# Here we provide an option to specify a transcriber-defined typeform prefix indicator instead
+			# Note: here are prefixes for 1st - 5th: "⠈⠼", "⠘⠼", "⠸⠼", "⠐⠼", "⠨⠼"
+			doubleStruck = string(default="⠈")
+			fraktur  = string(default="⠈")
+			sansSerif = string(default="⠈⠼")
+			greekVariant = string(default="⠨")
+
+		[[braille.vietnam]]
+			# drop digits down a row in simple numeric fractions
+			useDropNumbers = boolean(default=false)
+			# The guideline is being revised -- current guidance is to follow UEB for alternative scripts
+			# UEB Guide to Technical Material (https://iceb.org/Guidelines_for_Technical_Material_2008-10.pdf)
+			#   says to normally treat Fraktur and DoubleStruck as Script
+			# Here we provide an option to specify a transcriber-defined typeform prefix indicator instead
+			# Note: here are prefixes for 1st - 5th: "⠈⠼", "⠘⠼", "⠸⠼", "⠐⠼", "⠨⠼"
+			doubleStruck = string(default="⠈")
+			fraktur = string(default="⠈")
+			# first transcriber-defined typeform prefix indicator
+			sansSerif = string(default="⠈⠼")
+			# default to Greek
+			greekVariant = string(default="⠸")
+
+		[[braille.LaTeX]]
+			# Use the short form for the latex (e.g., "~a" instead of "\alpha")
+			useShortName = boolean(default=false)
+
+
+	[[other]]
+		# [default]
+		decimalSeparators = string(default=".")
+		# [default -- includes two forms of non-breaking spaces]
+		blockSeparators = string(default=", \u00a0\u202f")
+		# Auto, '.', ',', Custom
+		decimalSeparator = string(default="Auto")
+
+[automatedImageDescriptions]
+	enable = boolean(default=false)
+	defaultModel = string(default="Xenova/vit-gpt2-image-captioning")
+
+[screenCurtain]
+	enabled = boolean(default=false)
+	warnOnLoad = boolean(default=true)
+	playToggleSounds = boolean(default=true)
 """
 
 #: The configuration specification

```