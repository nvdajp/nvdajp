# Diff for: `source\_remoteClient\client.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\_remoteClient\client.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\_remoteClient\client.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\client.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\client.py"
index 8d377f6..07b8b1c 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\client.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\client.py"
@@ -46,6 +46,7 @@ class RemoteClient:
 	followerSession: Optional[FollowerSession]
 	keyModifiers: Set[KeyModifier]
 	hostPendingModifiers: Set[KeyModifier]
+	hostPendingNonmodifier: KeyModifier | None
 	_connecting: bool
 	leaderTransport: Optional[RelayTransport]
 	followerTransport: Optional[RelayTransport]
@@ -59,6 +60,7 @@ def __init__(
 		log.info("Initializing NVDA Remote client")
 		self.keyModifiers = set()
 		self.hostPendingModifiers = set()
+		self.hostPendingNonmodifiers = None
 		self.localScripts = set()
 		self.localMachine = LocalMachine()
 		self.followerSession = None
@@ -524,6 +526,9 @@ def processKeyInput(
 		if not pressed and keyCode in self.hostPendingModifiers:
 			self.hostPendingModifiers.discard(keyCode)
 			return True
+		if not pressed and keyCode == self.hostPendingNonmodifier:
+			self.hostPendingNonmodifier = None
+			return True
 		gesture = KeyboardInputGesture(
 			self.keyModifiers,
 			keyCode[0],
@@ -540,6 +545,7 @@ def processKeyInput(
 			if script in self.localScripts:
 				wx.CallAfter(script, gesture)
 				return False
+		self.localMachine._dismissLocalBrailleMessage()
 		self.leaderTransport.send(
 			RemoteMessageType.KEY,
 			vk_code=vkCode,
@@ -590,6 +596,7 @@ def _switchToRemoteControl(self, gesture: KeyboardInputGesture | None) -> None:
 		self.setReceivingBraille(self.sendingKeys)
 		if gesture is not None:
 			self.hostPendingModifiers = gesture.modifiers
+			self.hostPendingNonmodifier = (gesture.vkCode, gesture.isExtended)
 		else:
 			self.hostPendingModifiers = set()
 		# Translators: Presented when sending keyboard keys from the controlling computer to the controlled computer.

```