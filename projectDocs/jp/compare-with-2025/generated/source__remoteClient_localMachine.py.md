# Diff for: `source\_remoteClient\localMachine.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\_remoteClient\localMachine.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\_remoteClient\localMachine.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\localMachine.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\localMachine.py"
index 0f319cc..1e401b5 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\localMachine.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\localMachine.py"
@@ -18,12 +18,12 @@
 	not be used directly outside of the remote connection infrastructure.
 """
 
-import ctypes
 from enum import IntEnum, nonmember
 import os
-from typing import Any, Dict, List, Optional
+from typing import Any
 import winreg
 
+import winBindings.sas
 import api
 import braille
 from config.registry import RegistryKey
@@ -109,7 +109,7 @@ def __init__(self) -> None:
 		self.receivingBraille: bool = False
 		"""When True, braille output comes from remote"""
 
-		self._cachedSizes: Optional[List[int]] = None
+		self._cachedSizes: list[int] | None = None
 		"""Cached braille display sizes from remote machines"""
 
 		braille.decide_enabled.register(self.handleDecideEnabled)
@@ -188,7 +188,7 @@ def speak(
 		setSpeechCancelledToFalse()
 		wx.CallAfter(speech._manager.speak, sequence, priority)
 
-	def display(self, cells: List[int]) -> None:
+	def display(self, cells: list[int]) -> None:
 		"""Update the local braille display with cells from remote.
 
 		Safely writes braille cells from a remote machine to the local braille
@@ -206,12 +206,17 @@ def display(self, cells: List[int]) -> None:
 		if (
 			self.receivingBraille
 			and braille.handler.displaySize > 0
-			and len(cells) <= braille.handler.displaySize
+			and len(cells) <= braille.handler.displayDimensions.numCols
 		):
-			cells = cells + [0] * (braille.handler.displaySize - len(cells))
+			cells = cells + [0] * (braille.handler.displayDimensions.numCols - len(cells))
+			# Cache these cells in case we need them later
+			self._lastCells = cells
 			wx.CallAfter(braille.handler._writeCells, cells)
+		elif not self.receivingBraille and self._showingLocalUiMessage:
+			# Cache this cell array for after the local ui.message is dismissed
+			self._lastCells = cells
 
-	def brailleInput(self, **kwargs: Dict[str, Any]) -> None:
+	def brailleInput(self, **kwargs: dict[str, Any]) -> None:
 		"""Process braille input gestures from a remote machine.
 
 		Executes braille input commands locally using NVDA's input gesture system.
@@ -225,7 +230,7 @@ def brailleInput(self, **kwargs: Dict[str, Any]) -> None:
 		except inputCore.NoInputGestureAction:
 			pass
 
-	def setBrailleDisplaySize(self, sizes: List[int]) -> None:
+	def setBrailleDisplaySize(self, sizes: list[int]) -> None:
 		"""Cache remote braille display sizes for size negotiation.
 
 		:param sizes: List of display sizes (cells) from remote machines
@@ -258,9 +263,9 @@ def handleDecideEnabled(self) -> bool:
 
 	def sendKey(
 		self,
-		vk_code: Optional[int] = None,
-		extended: Optional[bool] = None,
-		pressed: Optional[bool] = None,
+		vk_code: int | None = None,
+		extended: bool | None = None,
+		pressed: bool | None = None,
 	) -> None:
 		"""Simulate a keyboard event on the local machine.
 
@@ -284,7 +289,7 @@ def sendSAS(self) -> None:
 		:note: SendSAS requires UI Access. If this fails, a warning is displayed.
 		"""
 		if self._canSendSAS():
-			ctypes.windll.sas.SendSAS(not isRunningOnSecureDesktop())
+			winBindings.sas.SendSAS(not isRunningOnSecureDesktop())
 		else:
 			# Translators: Message displayed when a remote computer tries to send control+alt+delete but UI Access is disabled.
 			ui.message(pgettext("remote", "Unable to trigger control+alt+delete"))

```