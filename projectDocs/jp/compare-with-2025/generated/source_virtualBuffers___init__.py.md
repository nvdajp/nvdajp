# Diff for: `source\virtualBuffers\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\virtualBuffers\__init__.py`  
**Current**: `F:\nvda\gh\alphajp\source\virtualBuffers\__init__.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\virtualBuffers\\__init__.py" "b/F:\\nvda\\gh\\alphajp\\source\\virtualBuffers\\__init__.py"
index fc6b20cf4e..f9efc93b9a 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\virtualBuffers\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\virtualBuffers\\__init__.py"
@@ -1,41 +1,30 @@
-# -*- coding: UTF-8 -*-
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2007-2023 NV Access Limited, Peter Vágner, Cyrille Bougot
+# Copyright (C) 2007-2025 NV Access Limited, Peter Vágner, Cyrille Bougot
 
 import time
 import threading
 import ctypes
-import collections  # noqa: F401
-import itertools  # noqa: F401
 from typing import (
 	Optional,
 	Dict,
 )
 import weakref
 import wx
-import review  # noqa: F401
 import NVDAHelper
 import XMLFormatting
 import scriptHandler
 from scriptHandler import script
-import speech  # noqa: F401
-import NVDAObjects  # noqa: F401
 import api
 import controlTypes
 import textInfos.offsets
 import config
-import cursorManager  # noqa: F401
 import browseMode
-import gui  # noqa: F401
-import eventHandler  # noqa: F401
 import braille
 import queueHandler
 from logHandler import log
 import ui
-import aria  # noqa: F401
-import treeInterceptorHandler  # noqa: F401
 import watchdog
 from abc import abstractmethod
 import documentBase
@@ -284,7 +273,7 @@ def _getStoryLength(self):
 	def _getTextRange(self, start, end):
 		if start == end:
 			return ""
-		return NVDAHelper.VBuf_getTextInRange(self.obj.VBufHandle, start, end, False) or ""
+		return NVDAHelper.localLib.VBuf_getTextInRange(self.obj.VBufHandle, start, end, False) or ""
 
 	def _getPlaceholderAttribute(self, attrs, placeholderAttrsKey):
 		"""Gets the placeholder attribute to be used.
@@ -336,7 +325,7 @@ def _normalizeCommand(self, command: XMLFormatting.CommandsT) -> XMLFormatting.C
 		return command
 
 	def _getFieldsInRange(self, start: int, end: int) -> textInfos.TextInfo.TextWithFieldsT:
-		text = NVDAHelper.VBuf_getTextInRange(self.obj.VBufHandle, start, end, True)
+		text = NVDAHelper.localLib.VBuf_getTextInRange(self.obj.VBufHandle, start, end, True)
 		if not text:
 			return [""]
 		commandList = XMLFormatting.XMLTextParser().parse(text)
@@ -570,7 +559,8 @@ def _loadBuffer(self):
 		try:
 			if log.isEnabledFor(log.DEBUG):
 				startTime = time.time()
-			self.VBufHandle = NVDAHelper.localLib.VBuf_createBuffer(
+			self.VBufHandle = NVDAHelper.localLib.VBufRemote_bufferHandle_t()
+			self.VBufHandle.value = NVDAHelper.localLib.VBuf_createBuffer(
 				self.rootNVDAObject.appModule.helperLocalBindingHandle,
 				self.rootDocHandle,
 				self.rootID,
@@ -631,7 +621,7 @@ def unloadBuffer(self):
 			try:
 				watchdog.cancellableExecute(
 					NVDAHelper.localLib.VBuf_destroyBuffer,
-					ctypes.byref(ctypes.c_int(self.VBufHandle)),
+					ctypes.byref(self.VBufHandle),
 				)
 			except WindowsError:
 				pass

```