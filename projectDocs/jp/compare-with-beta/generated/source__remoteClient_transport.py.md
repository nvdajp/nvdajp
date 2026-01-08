# Diff for: `source\_remoteClient\transport.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\_remoteClient\transport.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\_remoteClient\transport.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\transport.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\transport.py"
index 5ed6cfe..f220da7 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\transport.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\transport.py"
@@ -521,9 +521,6 @@ def parse(self, line: bytes) -> None:
 		except ValueError:
 			log.warn(f"Received message with invalid type: {obj!r}")
 			return
-		if messageType is RemoteMessageType.PING:
-			# No handling is required
-			return
 		del obj["type"]
 		extensionPoint = self.inboundHandlers.get(messageType)
 		if not extensionPoint:

```