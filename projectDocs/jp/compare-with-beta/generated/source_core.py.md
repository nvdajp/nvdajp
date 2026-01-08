# Diff for: `source\core.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\core.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\core.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\core.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\core.py"
index 113b88a..33d62bc 100644
--- "a/F:\\nvda\\gh\\beta\\source\\core.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\core.py"
@@ -322,12 +322,9 @@ def resetConfiguration(factoryDefaults=False):
 	import hwIo
 	import tones
 	import audio
-	import screenCurtain
 
 	log.debug("Terminating vision")
 	vision.terminate()
-	log.debug("Terminating Screen Curtain")
-	screenCurtain.terminate()
 	log.debug("Terminating braille")
 	braille.terminate()
 	log.debug("Terminating brailleInput")
@@ -391,8 +388,6 @@ def resetConfiguration(factoryDefaults=False):
 	# Vision
 	log.debug("initializing vision")
 	vision.initialize()
-	log.debug("initializing Screen Curtain")
-	screenCurtain.initialize()
 	log.debug("Reloading user and locale input gesture maps")
 	inputCore.manager.loadUserGestureMap()
 	inputCore.manager.loadLocaleGestureMap()
@@ -791,7 +786,7 @@ def main():
 	speech.initialize()
 	import mathPres
 
-	log.debug("Initializing math presentation")
+	log.debug("Initializing MathPlayer")
 	mathPres.initialize()
 	timeSinceStart = time.time() - NVDAState.getStartTime()
 	if not globalVars.appArgs.minimal and timeSinceStart > 5:
@@ -815,12 +810,6 @@ def main():
 
 	log.debug("Initializing braille")
 	braille.initialize()
-
-	import screenCurtain
-
-	log.debug("Initializing Screen Curtain")
-	screenCurtain.initialize()
-
 	import vision
 
 	log.debug("Initializing vision")
@@ -1098,7 +1087,6 @@ def _doPostNvdaStartupAction():
 	_terminate(keyboardHandler, name="keyboard handler")
 	_terminate(mouseHandler)
 	_terminate(inputCore)
-	_terminate(screenCurtain)
 	_terminate(vision)
 	_terminate(brailleInput)
 	_terminate(braille)

```