# Diff for: `source\UIAHandler\_remoteOps\remoteTypes\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\UIAHandler\_remoteOps\remoteTypes\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\UIAHandler\_remoteOps\remoteTypes\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\UIAHandler\\_remoteOps\\remoteTypes\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\UIAHandler\\_remoteOps\\remoteTypes\\__init__.py"
index c5aa47a..0935493 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\UIAHandler\\_remoteOps\\remoteTypes\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\UIAHandler\\_remoteOps\\remoteTypes\\__init__.py"
@@ -1,15 +1,13 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2023-2024 NV Access Limited
+# Copyright (C) 2023-2025 NV Access Limited
 
 
 from __future__ import annotations
 from typing import (
 	Type,
-	Any,
 	Self,
-	ParamSpec,
 	Iterable,
 	Generic,
 	TypeVar,
@@ -40,11 +38,6 @@
 from .. import operation
 
 
-_remoteFunc_self = TypeVar("_remoteFunc_self", bound=builder._RemoteBase)
-_remoteFunc_paramSpec = ParamSpec("_remoteFunc_paramSpec")
-_remoteFunc_return = TypeVar("_remoteFunc_return")
-
-
 LocalTypeVar = TypeVar("LocalTypeVar")
 
 

```