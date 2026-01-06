# Diff for: `source\gui\message.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\gui\message.py`  
**Current**: `F:\nvda\gh\alphajp\source\gui\message.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\message.py" "b/F:\\nvda\\gh\\alphajp\\source\\gui\\message.py"
index 30d036e207..3c3e58470d 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\message.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\gui\\message.py"
@@ -1,4 +1,3 @@
-# -*- coding: UTF-8 -*-
 # A part of NonVisual Desktop Access (NVDA)
 # Copyright (C) 2006-2025 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Mesar Hameed, Joseph Lee,
 # Thomas Stivers, Babbage B.V., Accessolutions, Julien Cochuyt
@@ -14,7 +13,7 @@
 from collections.abc import Callable, Collection
 from enum import Enum, IntEnum, auto
 from functools import partialmethod, singledispatchmethod, wraps
-from typing import Any, Literal, NamedTuple, Optional, Self, TypeAlias
+from typing import Any, Literal, NamedTuple, Optional, Self
 
 import core
 import extensionPoints
@@ -177,8 +176,7 @@ class Payload:
 	"""Payload of information to pass to message dialog callbacks."""
 
 
-# TODO: Change to type statement when Python 3.12 or later is in use.
-_Callback_T: TypeAlias = Callable[[Payload], Any]
+type _Callback_T = Callable[[Payload], Any]
 
 
 class _Missing_Type:
@@ -222,7 +220,7 @@ class EscapeCode(IntEnum):
 	"""
 
 
-wxArtID: TypeAlias = int
+type wxArtID = int
 
 
 class DialogType(Enum):

```