# Diff for: `source\_remoteClient\localMachine.py`

**Source**: `F:\nvda\gh\beta\source\_remoteClient\localMachine.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\_remoteClient\localMachine.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\localMachine.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\localMachine.py"
index 7e1f827..1e401b5 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_remoteClient\\localMachine.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\localMachine.py"
@@ -98,24 +98,6 @@ class LocalMachine:
 	    - :mod:`transport` - Network transport layer
 	"""
 
-	_receivingBraille: bool
-	"""Internal storage for :attr:`receivingBraille`."""
-
-	@property
-	def receivingBraille(self) -> bool:
-		"""When True, braille output comes from remote"""
-		return self._receivingBraille
-
-	@receivingBraille.setter
-	def receivingBraille(self, val: bool):
-		self._receivingBraille = val
-		# Let the braille handler know that whether it's enabled has changed.
-		# This needs to be blocking,
-		# otherwise there is a race condition between
-		# our handling of `ui.message`,
-		# and the braille handler clearing the message buffer.
-		braille.handler._refreshEnabled(block=True)
-
 	def __init__(self) -> None:
 		"""Initialize the local machine controller.
 
@@ -124,24 +106,13 @@ def __init__(self) -> None:
 		self.isMuted: bool = False
 		"""When True, most remote commands will be ignored"""
 
-		self.receivingBraille = False
+		self.receivingBraille: bool = False
+		"""When True, braille output comes from remote"""
 
 		self._cachedSizes: list[int] | None = None
 		"""Cached braille display sizes from remote machines"""
 
-		self._showingLocalUiMessage: bool = False
-		"""Whether we're currently showing a `ui.message` while showing remote braille."""
-
-		self._oldReceivingBraille: bool = False
-		"""Cached value of `self.receivingBraille` for when we show a `ui.message`."""
-
-		self._lastCells: list[int] = []
-		"""Cached cells for display when we return from controling the local computer, or displaying a `ui.message`."""
-
 		braille.decide_enabled.register(self.handleDecideEnabled)
-		braille._pre_showBrailleMessage.register(self._handleShowBrailleMessage)
-		braille._post_dismissBrailleMessage.register(self._handleDismissBrailleMessage)
-		braille._decide_disabledIncludesMessages.register(self._handleDecideDisabledIncludesMessages)
 
 	def terminate(self) -> None:
 		"""Clean up resources when the local machine controller is terminated.
@@ -150,9 +121,6 @@ def terminate(self) -> None:
 		    ensure proper cleanup when the remote connection ends.
 		"""
 		braille.decide_enabled.unregister(self.handleDecideEnabled)
-		braille._pre_showBrailleMessage.unregister(self._handleShowBrailleMessage)
-		braille._post_dismissBrailleMessage.unregister(self._handleDismissBrailleMessage)
-		braille._decide_disabledIncludesMessages.unregister(self._handleDecideDisabledIncludesMessages)
 
 	def playWave(self, fileName: str) -> None:
 		"""Play a wave file on the local machine.
@@ -269,61 +237,30 @@ def setBrailleDisplaySize(self, sizes: list[int]) -> None:
 		"""
 		self._cachedSizes = sizes
 
-	def _handleFilterDisplayDimensions(self, value: braille.DisplayDimensions) -> braille.DisplayDimensions:
-		"""Filter the local display dimensions based on remote display dimensions.
-
-		Determines the optimal display dimensions when sharing braille output by
-		finding the smallest positive width among local and remote displays.
+	def handleFilterDisplaySize(self, value: int) -> int:
+		"""Filter the local display size based on remote display sizes.
 
-		.. note::
-			We can currently only support a single line of braille,
-			as sending display dimensions would require changing the Remote Access protocol.
+		Determines the optimal display size when sharing braille output by
+		finding the smallest positive size among local and remote displays.
 
-		:param value: Local display dimensions
-		:return: The negotiated display dimensions to use.
+		:param value: Local display size in cells
+		:return: The negotiated display size to use
 		"""
 		if not self._cachedSizes:
-			# We cannot support multiline displays without breaking the Remote Access protocol,
-			# so always force numRows to 1.
-			return value._replace(numRows=1)
-		# There is no point storing the number of rows if we are always going to set it to 1.
-		sizes = self._cachedSizes + [value.numCols]
+			return value
+		sizes = self._cachedSizes + [value]
 		try:
-			return braille.DisplayDimensions(numRows=1, numCols=min(i for i in sizes if i > 0))
+			return min(i for i in sizes if i > 0)
 		except ValueError:
-			return value._replace(numRows=1)
+			return value
 
 	def handleDecideEnabled(self) -> bool:
 		"""Determine if the local braille display should be enabled.
 
 		:return: False if receiving remote braille, True otherwise
 		"""
-		return not self.receivingBraille or self._showingLocalUiMessage
-
-	def _handleDecideDisabledIncludesMessages(self) -> bool:
-		"""Determine if the local display being disabled should exclude ui.message.
-
-		:return: ``True`` if we should block UI messages; ``False`` if we should let them show.
-		"""
 		return not self.receivingBraille
 
-	def _handleShowBrailleMessage(self) -> None:
-		"""Prepare to display a local `ui.message`."""
-		self._oldReceivingBraille, self.receivingBraille = self.receivingBraille, False
-		self._showingLocalUiMessage = True
-
-	def _handleDismissBrailleMessage(self) -> None:
-		"""Handle returning from showing a local `ui.message`."""
-		self._showingLocalUiMessage = False
-		self.receivingBraille = self._oldReceivingBraille
-		self.display(self._lastCells)
-
-	def _dismissLocalBrailleMessage(self) -> None:
-		"""Dismiss a local ``ui.message``, if one is being shown."""
-		if not self._showingLocalUiMessage:
-			return
-		braille.handler._dismissMessage()
-
 	def sendKey(
 		self,
 		vk_code: int | None = None,

```