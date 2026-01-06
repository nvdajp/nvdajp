# Diff for: `source\_remoteClient\client.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\_remoteClient\client.py`  
**Current**: `F:\nvda\gh\alphajp\source\_remoteClient\client.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\client.py" "b/F:\\nvda\\gh\\alphajp\\source\\_remoteClient\\client.py"
index 8d377f6c76..4691a226fa 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\client.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\_remoteClient\\client.py"
@@ -19,7 +19,7 @@
 from keyboardHandler import KeyboardInputGesture, canModifiersPerformAction
 from logHandler import log
 from gui.guiHelper import alwaysCallAfter
-from utils.security import isRunningOnSecureDesktop, post_sessionLockStateChanged
+from utils.security import isRunningOnSecureDesktop
 from gui.message import MessageDialog, DefaultButton, ReturnCode, DialogType
 import scriptHandler
 import winUser
@@ -51,7 +51,6 @@ class RemoteClient:
 	followerTransport: Optional[RelayTransport]
 	localControlServer: Optional[server.LocalRelayServer]
 	sendingKeys: bool
-	sdHandler: SecureDesktopHandler | None
 
 	def __init__(
 		self,
@@ -72,20 +71,14 @@ def __init__(
 		self.followerTransport = None
 		self.localControlServer = None
 		self.sendingKeys = False
-		self._wasSendingKeysBeforeLock: bool = False
-		try:
-			self.sdHandler = SecureDesktopHandler()
-		except RuntimeError:
-			log.error("Failed to initialise the secure desktop handler.", exc_info=True)
-			self.sdHandler = None
-		else:
-			if isRunningOnSecureDesktop():
-				connection = self.sdHandler.initializeSecureDesktop()
-				if connection:
-					self.connectAsFollower(connection)
-					self.followerSession.transport.connectedEvent.wait(
-						self.sdHandler.SD_CONNECT_BLOCK_TIMEOUT,
-					)
+		self.sdHandler = SecureDesktopHandler()
+		if isRunningOnSecureDesktop():
+			connection = self.sdHandler.initializeSecureDesktop()
+			if connection:
+				self.connectAsFollower(connection)
+				self.followerSession.transport.connectedEvent.wait(
+					self.sdHandler.SD_CONNECT_BLOCK_TIMEOUT,
+				)
 		core.postNvdaStartup.register(self.performAutoconnect)
 		inputCore.decide_handleRawKey.register(self.processKeyInput)
 
@@ -109,8 +102,7 @@ def performAutoconnect(self):
 		self.connect(conInfo)
 
 	def terminate(self):
-		if self.sdHandler is not None:
-			self.sdHandler.terminate()
+		self.sdHandler.terminate()
 		self.disconnect()
 		self.localMachine.terminate()
 		self.localMachine = None
@@ -284,8 +276,7 @@ def disconnectAsFollower(self):
 		self.followerSession.close()
 		self.followerSession = None
 		self.followerTransport = None
-		if self.sdHandler is not None:
-			self.sdHandler.followerSession = None
+		self.sdHandler.followerSession = None
 		if self.menu:
 			self.menu.handleConnected(ConnectionMode.FOLLOWER, False)
 		self._connecting = False
@@ -382,7 +373,6 @@ def onConnectedAsLeader(self):
 		configuration.writeConnectionToConfig(self.leaderSession.getConnectionInfo())
 		if self.menu:
 			self.menu.handleConnected(ConnectionMode.LEADER, True)
-		post_sessionLockStateChanged.register(self._sessionLockStateChangeHandler)
 		ui.message(
 			# Translators: Presented when connected to the remote computer.
 			_("Connected"),
@@ -398,7 +388,6 @@ def onDisconnectingAsLeader(self):
 			self.localMachine.isMuted = False
 		self.sendingKeys = False
 		self.keyModifiers = set()
-		post_sessionLockStateChanged.unregister(self._sessionLockStateChangeHandler)
 
 	@alwaysCallAfter
 	def onDisconnectedAsLeader(self):
@@ -413,8 +402,7 @@ def connectAsFollower(self, connectionInfo: ConnectionInfo):
 			transport=transport,
 			localMachine=self.localMachine,
 		)
-		if self.sdHandler is not None:
-			self.sdHandler.followerSession = self.followerSession
+		self.sdHandler.followerSession = self.followerSession
 		self.followerTransport = transport
 		transport.transportCertificateAuthenticationFailed.register(
 			self.onFollowerCertificateFailed,
@@ -583,28 +571,17 @@ def _switchToLocalControl(self) -> None:
 		if configuration.getRemoteConfig()["ui"]["muteOnLocalControl"] and not self.localMachine.isMuted:
 			self.toggleMute()
 
-	def _switchToRemoteControl(self, gesture: KeyboardInputGesture | None) -> None:
+	def _switchToRemoteControl(self, gesture: KeyboardInputGesture) -> None:
 		"""Switch to controlling the remote computer."""
 		self.sendingKeys = True
 		log.info("Remote key control enabled")
 		self.setReceivingBraille(self.sendingKeys)
-		if gesture is not None:
-			self.hostPendingModifiers = gesture.modifiers
-		else:
-			self.hostPendingModifiers = set()
+		self.hostPendingModifiers = gesture.modifiers
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