# Diff for: `source\_remoteClient\client.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\_remoteClient\client.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\_remoteClient\client.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\client.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\client.py"
index 07b8b1c..4691a22 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\client.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\client.py"
@@ -19,7 +19,7 @@
 from keyboardHandler import KeyboardInputGesture, canModifiersPerformAction
 from logHandler import log
 from gui.guiHelper import alwaysCallAfter
-from utils.security import isRunningOnSecureDesktop, post_sessionLockStateChanged
+from utils.security import isRunningOnSecureDesktop
 from gui.message import MessageDialog, DefaultButton, ReturnCode, DialogType
 import scriptHandler
 import winUser
@@ -46,13 +46,11 @@ class RemoteClient:
 	followerSession: Optional[FollowerSession]
 	keyModifiers: Set[KeyModifier]
 	hostPendingModifiers: Set[KeyModifier]
-	hostPendingNonmodifier: KeyModifier | None
 	_connecting: bool
 	leaderTransport: Optional[RelayTransport]
 	followerTransport: Optional[RelayTransport]
 	localControlServer: Optional[server.LocalRelayServer]
 	sendingKeys: bool
-	sdHandler: SecureDesktopHandler | None
 
 	def __init__(
 		self,
@@ -60,7 +58,6 @@ def __init__(
 		log.info("Initializing NVDA Remote client")
 		self.keyModifiers = set()
 		self.hostPendingModifiers = set()
-		self.hostPendingNonmodifiers = None
 		self.localScripts = set()
 		self.localMachine = LocalMachine()
 		self.followerSession = None
@@ -74,13 +71,7 @@ def __init__(
 		self.followerTransport = None
 		self.localControlServer = None
 		self.sendingKeys = False
-		self._wasSendingKeysBeforeLock: bool = False
-		try:
 		self.sdHandler = SecureDesktopHandler()
-		except RuntimeError:
-			log.error("Failed to initialise the secure desktop handler.", exc_info=True)
-			self.sdHandler = None
-		else:
 		if isRunningOnSecureDesktop():
 			connection = self.sdHandler.initializeSecureDesktop()
 			if connection:
@@ -111,7 +102,6 @@ def performAutoconnect(self):
 		self.connect(conInfo)
 
 	def terminate(self):
-		if self.sdHandler is not None:
 		self.sdHandler.terminate()
 		self.disconnect()
 		self.localMachine.terminate()
@@ -286,7 +276,6 @@ def disconnectAsFollower(self):
 		self.followerSession.close()
 		self.followerSession = None
 		self.followerTransport = None
-		if self.sdHandler is not None:
 		self.sdHandler.followerSession = None
 		if self.menu:
 			self.menu.handleConnected(ConnectionMode.FOLLOWER, False)
@@ -384,7 +373,6 @@ def onConnectedAsLeader(self):
 		configuration.writeConnectionToConfig(self.leaderSession.getConnectionInfo())
 		if self.menu:
 			self.menu.handleConnected(ConnectionMode.LEADER, True)
-		post_sessionLockStateChanged.register(self._sessionLockStateChangeHandler)
 		ui.message(
 			# Translators: Presented when connected to the remote computer.
 			_("Connected"),
@@ -400,7 +388,6 @@ def onDisconnectingAsLeader(self):
 			self.localMachine.isMuted = False
 		self.sendingKeys = False
 		self.keyModifiers = set()
-		post_sessionLockStateChanged.unregister(self._sessionLockStateChangeHandler)
 
 	@alwaysCallAfter
 	def onDisconnectedAsLeader(self):
@@ -415,7 +402,6 @@ def connectAsFollower(self, connectionInfo: ConnectionInfo):
 			transport=transport,
 			localMachine=self.localMachine,
 		)
-		if self.sdHandler is not None:
 		self.sdHandler.followerSession = self.followerSession
 		self.followerTransport = transport
 		transport.transportCertificateAuthenticationFailed.register(
@@ -526,9 +512,6 @@ def processKeyInput(
 		if not pressed and keyCode in self.hostPendingModifiers:
 			self.hostPendingModifiers.discard(keyCode)
 			return True
-		if not pressed and keyCode == self.hostPendingNonmodifier:
-			self.hostPendingNonmodifier = None
-			return True
 		gesture = KeyboardInputGesture(
 			self.keyModifiers,
 			keyCode[0],
@@ -545,7 +528,6 @@ def processKeyInput(
 			if script in self.localScripts:
 				wx.CallAfter(script, gesture)
 				return False
-		self.localMachine._dismissLocalBrailleMessage()
 		self.leaderTransport.send(
 			RemoteMessageType.KEY,
 			vk_code=vkCode,
@@ -589,29 +571,17 @@ def _switchToLocalControl(self) -> None:
 		if configuration.getRemoteConfig()["ui"]["muteOnLocalControl"] and not self.localMachine.isMuted:
 			self.toggleMute()
 
-	def _switchToRemoteControl(self, gesture: KeyboardInputGesture | None) -> None:
+	def _switchToRemoteControl(self, gesture: KeyboardInputGesture) -> None:
 		"""Switch to controlling the remote computer."""
 		self.sendingKeys = True
 		log.info("Remote key control enabled")
 		self.setReceivingBraille(self.sendingKeys)
-		if gesture is not None:
 		self.hostPendingModifiers = gesture.modifiers
-			self.hostPendingNonmodifier = (gesture.vkCode, gesture.isExtended)
-		else:
-			self.hostPendingModifiers = set()
 		# Translators: Presented when sending keyboard keys from the controlling computer to the controlled computer.
 		ui.message(pgettext("remote", "Controlling remote computer"))
 		if self.localMachine.isMuted:
 			self.toggleMute()
 
-	def _sessionLockStateChangeHandler(self, isNowLocked: bool):
-		if isNowLocked and self.sendingKeys:
-			self._wasSendingKeysBeforeLock = True
-			self._switchToLocalControl()
-		elif not isNowLocked and self._wasSendingKeysBeforeLock:
-			self._wasSendingKeysBeforeLock = False
-			self._switchToRemoteControl(None)
-
 	def releaseKeys(self):
 		"""Release all pressed keys on the remote machine.
 

```