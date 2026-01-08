# Diff for: `source\core.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\core.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\core.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\core.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\core.py"
index 02af36c..113b88a 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\core.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\core.py"
@@ -19,8 +19,8 @@
 import threading
 import os
 import time
-import ctypes
 from enum import Enum
+import winBindings.kernel32
 import logHandler
 import languageHandler
 import globalVars
@@ -322,9 +322,12 @@ def resetConfiguration(factoryDefaults=False):
 	import hwIo
 	import tones
 	import audio
+	import screenCurtain
 
 	log.debug("Terminating vision")
 	vision.terminate()
+	log.debug("Terminating Screen Curtain")
+	screenCurtain.terminate()
 	log.debug("Terminating braille")
 	braille.terminate()
 	log.debug("Terminating brailleInput")
@@ -388,6 +391,8 @@ def resetConfiguration(factoryDefaults=False):
 	# Vision
 	log.debug("initializing vision")
 	vision.initialize()
+	log.debug("initializing Screen Curtain")
+	screenCurtain.initialize()
 	log.debug("Reloading user and locale input gesture maps")
 	inputCore.manager.loadUserGestureMap()
 	inputCore.manager.loadLocaleGestureMap()
@@ -550,6 +555,7 @@ def _handleNVDAModuleCleanupBeforeGUIExit():
 	import globalPluginHandler
 	import watchdog
 	import _remoteClient
+	import _localCaptioner
 
 	try:
 		import updateCheck
@@ -568,6 +574,8 @@ def _handleNVDAModuleCleanupBeforeGUIExit():
 	# Terminating remoteClient causes it to clean up its menus, so do it here while they still exist
 	_terminate(_remoteClient)
 
+	_terminate(_localCaptioner)
+
 
 def _initializeObjectCaches():
 	"""
@@ -606,14 +614,13 @@ def _doLoseFocus():
 
 
 def _setUpWxApp() -> "wx.App":
-	import six
 	import wx
 
 	import config
 	import nvwave
 	import speech
 
-	log.info(f"Using wx version {wx.version()} with six version {six.__version__}")
+	log.info(f"Using wx version {wx.version()}")
 
 	# Disables wx logging in secure mode due to a security issue: GHSA-h7pp-6jqw-g3pj
 	# This is due to the wx.LogSysError dialog allowing a file explorer dialog to be opened.
@@ -642,7 +649,7 @@ def InitLocale(self):
 	def onQueryEndSession(evt):
 		if config.isAppX:
 			# Automatically restart NVDA on Windows Store update
-			ctypes.windll.kernel32.RegisterApplicationRestart(None, 0)
+			winBindings.kernel32.RegisterApplicationRestart(None, 0)
 
 	app.Bind(wx.EVT_QUERY_END_SESSION, onQueryEndSession)
 
@@ -784,7 +791,7 @@ def main():
 	speech.initialize()
 	import mathPres
 
-	log.debug("Initializing MathPlayer")
+	log.debug("Initializing math presentation")
 	mathPres.initialize()
 	timeSinceStart = time.time() - NVDAState.getStartTime()
 	if not globalVars.appArgs.minimal and timeSinceStart > 5:
@@ -808,6 +815,12 @@ def main():
 
 	log.debug("Initializing braille")
 	braille.initialize()
+
+	import screenCurtain
+
+	log.debug("Initializing Screen Curtain")
+	screenCurtain.initialize()
+
 	import vision
 
 	log.debug("Initializing vision")
@@ -827,9 +840,9 @@ def main():
 		wx.CallAfter(audioDucking.initialize)
 
 	from winAPI.messageWindow import _MessageWindow
-	import versionInfo
+	import buildVersion
 
-	messageWindow = _MessageWindow(versionInfo.name)
+	messageWindow = _MessageWindow(buildVersion.name)
 
 	# initialize wxpython localization support
 	wxLocaleObj = wx.Locale()
@@ -906,6 +919,10 @@ def main():
 
 	_remoteClient.initialize()
 
+	import _localCaptioner
+
+	_localCaptioner.initialize()
+
 	if globalVars.appArgs.install or globalVars.appArgs.installSilent:
 		import gui.installerGui
 
@@ -1081,6 +1098,7 @@ def _doPostNvdaStartupAction():
 	_terminate(keyboardHandler, name="keyboard handler")
 	_terminate(mouseHandler)
 	_terminate(inputCore)
+	_terminate(screenCurtain)
 	_terminate(vision)
 	_terminate(brailleInput)
 	_terminate(braille)

```