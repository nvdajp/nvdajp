# Diff for: `tests\unit\test_remote\test_remoteClient.py`

**Source**: `F:\nvda\gh\beta\tests\unit\test_remote\test_remoteClient.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\unit\test_remote\test_remoteClient.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_remote\\test_remoteClient.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_remote\\test_remoteClient.py"
index e5df9c4..ce524b7 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_remote\\test_remoteClient.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_remote\\test_remoteClient.py"
@@ -9,8 +9,6 @@
 from _remoteClient.connectionInfo import ConnectionInfo, ConnectionMode
 from _remoteClient.protocol import RemoteMessageType
 from gui.message import ReturnCode
-from keyboardHandler import KeyboardInputGesture
-from utils.security import post_sessionLockStateChanged
 
 
 # Fake implementations for testing
@@ -21,14 +19,6 @@ def __init__(self):
 	def terminate(self):
 		pass
 
-	def setClipboardText(self, *a, **k): ...
-	def speak(self, *a, **k): ...
-	def cancelSpeech(self, *a, **k): ...
-	def pauseSpeech(self, *a, **k): ...
-	def beep(self, *a, **k): ...
-	def playWave(self, *a, **k): ...
-	def display(self, *a, **k): ...
-
 
 class FakeMenu:
 	def __init__(self):
@@ -42,7 +32,6 @@ def Check(self, value):
 			self.checked = value
 
 	def handleConnected(self, *args, **kwargs): ...
-	def handleConnecting(self, *a, **k): ...
 
 
 class FakeTransport:
@@ -242,60 +231,6 @@ def test_disconnect(self):
 			self.client.disconnect()
 		fakeControl.close.assert_called_once()
 
-	def test_lockWhileSendingKeys(self):
-		# the `onConnectedAsLeader` method is decorated with `alwaysCallAfter`.
-		# This causes issues here, so unwrap it.
-		with patch(
-			"_remoteClient.client.RemoteClient.onConnectedAsLeader",
-			rcClient.RemoteClient.onConnectedAsLeader.__wrapped__,
-		):
-			connInfo = ConnectionInfo(
-				hostname="localhost",
-				mode=ConnectionMode.LEADER,
-				key="abc",
-				port=4321,
-				insecure=False,
-			)
-			self.client.connect(connInfo)
-			self.client.leaderTransport.transportConnected.notify()
-			# Explicitly set to connected and act as though we have a follower.
-			# For this test, we don't need to run the TCP code,
-			# nor do we need to actually have a connected follower.
-			# However, these are prerequisites of being able to control a remote computer,
-			# so fake it.
-			self.client.leaderTransport.connected = True
-			self.client.leaderSession.followers = [""]
-			self.assertFalse(self.client.sendingKeys, "We should initially not be sending keys")
-			self.client.toggleRemoteKeyControl(KeyboardInputGesture.fromName("NVDA+alt+tab"))
-			self.assertTrue(self.client.sendingKeys, "We just explicitly switched to sending keys")
-			post_sessionLockStateChanged.notify(isNowLocked=True)
-			self.assertFalse(
-				self.client.sendingKeys,
-				"We should stop sending keys when switching to the lockscreen",
-			)
-			post_sessionLockStateChanged.notify(isNowLocked=False)
-			self.assertTrue(
-				self.client.sendingKeys,
-				"We should resume sending keys after returning from the lock screen",
-			)
-			# When returning control, Remote Access queries `inputCore.manager`
-			# since NVDA isn't running, this is `None`,
-			# but we don't care about these checks in this case.
-			# Thus, simply patch it out.
-			with patch("inputCore.manager"):
-				self.client.toggleRemoteKeyControl(KeyboardInputGesture.fromName("NVDA+alt+tab"))
-			self.assertFalse(self.client.sendingKeys, "We just explicitly stopped sending keys")
-			post_sessionLockStateChanged.notify(isNowLocked=True)
-			self.assertFalse(
-				self.client.sendingKeys,
-				"The session locking shouldn't do anything if we weren't sending keys",
-			)
-			post_sessionLockStateChanged.notify(isNowLocked=False)
-			self.assertFalse(
-				self.client.sendingKeys,
-				"We weren't sending keys before the latest session lock, so we shouldn't start when it's unlocked",
-			)
-
 
 if __name__ == "__main__":
 	unittest.main()

```