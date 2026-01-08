# Diff for: `source\_remoteClient\session.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\_remoteClient\session.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\_remoteClient\session.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\session.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\session.py"
index ba613f9..d068b30 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\session.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\session.py"
@@ -315,8 +315,8 @@ def __init__(
 			RemoteMessageType.SET_DISPLAY_SIZE,
 			self.setDisplaySize,
 		)
-		braille.filter_displaySize.register(
-			self.localMachine.handleFilterDisplaySize,
+		braille.filter_displayDimensions.register(
+			self.localMachine._handleFilterDisplayDimensions,
 		)
 		self.transport.registerInbound(
 			RemoteMessageType.BRAILLE_INPUT,
@@ -396,7 +396,7 @@ def handleTransportDisconnected(self) -> None:
 	def handleClientDisconnected(self, client: dict[str, Any]) -> None:
 		super().handleClientDisconnected(client)
 		if client["connection_type"] == connectionInfo.ConnectionMode.LEADER.value:
-			log.info("Leader client disconnected: %r", client)
+			log.info(f"Leader client disconnected: {client!r}")
 			del self.leaders[client["id"]]
 		elif client["connection_type"] == connectionInfo.ConnectionMode.FOLLOWER.value:
 			self.followers.discard(client["id"])
@@ -407,7 +407,7 @@ def setDisplaySize(self, sizes: list[int] | None = None) -> None:
 		self.leaderDisplaySizes = (
 			sizes if sizes else [info.get("braille_numCells", 0) for info in self.leaders.values()]
 		)
-		log.debug("Setting follower display size to: %r", self.leaderDisplaySizes)
+		log.debug(f"Setting follower display size to: {self.leaderDisplaySizes!r}")
 		self.localMachine.setBrailleDisplaySize(self.leaderDisplaySizes)
 
 	def handleBrailleInfo(
@@ -590,17 +590,14 @@ def handleClientDisconnected(self, client: dict[str, Any] | None = None):
 	def sendBrailleInfo(
 		self,
 		display: braille.BrailleDisplayDriver | None = None,
-		displaySize: int | None = None,
+		displayDimensions: braille.DisplayDimensions | None = None,
 	) -> None:
 		if display is None:
 			display = braille.handler.display
-		if displaySize is None:
-			displaySize = braille.handler.displaySize
-		log.debug(
-			"Sending braille info to follower - display: %s, size: %d",
-			display.name if display else "None",
-			displaySize if displaySize else 0,
-		)
+		if displayDimensions is None:
+			displayDimensions = braille.handler.displayDimensions
+		displaySize = displayDimensions.numCols
+		log.debug(f"Sending braille info to follower - display: {display.name}, width: {displaySize}")
 		self.transport.send(
 			type=RemoteMessageType.SET_BRAILLE_INFO,
 			name=display.name,
@@ -617,7 +614,16 @@ def handleDecideExecuteGesture(
 		:return: False if gesture was processed and sent, True otherwise
 		:note: Extracts gesture details and script info before sending
 		"""
+		# Import late to avoid circular import
+		from globalCommands import commands
+
 		if isinstance(gesture, (braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture)):
+			if self.localMachine._showingLocalUiMessage and gesture.script in (
+				commands.script_braille_routeTo,
+				commands.script_braille_scrollBack,
+				commands.script_braille_scrollForward,
+			):
+				return True
 			dict = {
 				key: gesture.__dict__[key]
 				for key in gesture.__dict__
@@ -658,6 +664,7 @@ def handleDecideExecuteGesture(
 				dict["space"] = gesture.space
 			if hasattr(gesture, "routingIndex") and "routingIndex" not in dict:
 				dict["routingIndex"] = gesture.routingIndex
+			self.localMachine._dismissLocalBrailleMessage()
 			self.transport.send(type=RemoteMessageType.BRAILLE_INPUT, **dict)
 			return False
 		else:

```