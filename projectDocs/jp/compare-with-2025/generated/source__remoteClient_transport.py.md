# Diff for: `source\_remoteClient\transport.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\_remoteClient\transport.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\_remoteClient\transport.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\transport.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\transport.py"
index 3062011..5ed6cfe 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\transport.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\transport.py"
@@ -234,8 +234,7 @@ def registerOutbound(
 	def unregisterOutbound(self, messageType: RemoteMessageType) -> None:
 		"""Unregister an extension point from a message type.
 
-		Args:
-			messageType (RemoteMessageType): The message type to unregister the extension point from
+		:param messageType (RemoteMessageType): The message type to unregister the extension point from
 		"""
 		self.outboundHandlers[messageType].unregister()
 		del self.outboundHandlers[messageType]
@@ -522,6 +521,9 @@ def parse(self, line: bytes) -> None:
 		except ValueError:
 			log.warn(f"Received message with invalid type: {obj!r}")
 			return
+		if messageType is RemoteMessageType.PING:
+			# No handling is required
+			return
 		del obj["type"]
 		extensionPoint = self.inboundHandlers.get(messageType)
 		if not extensionPoint:

```