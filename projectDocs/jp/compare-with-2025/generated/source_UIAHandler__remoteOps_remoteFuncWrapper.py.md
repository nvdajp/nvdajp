# Diff for: `source\UIAHandler\_remoteOps\remoteFuncWrapper.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\UIAHandler\_remoteOps\remoteFuncWrapper.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\UIAHandler\_remoteOps\remoteFuncWrapper.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\UIAHandler\\_remoteOps\\remoteFuncWrapper.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\UIAHandler\\_remoteOps\\remoteFuncWrapper.py"
index f747511..da3dada 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\UIAHandler\\_remoteOps\\remoteFuncWrapper.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\UIAHandler\\_remoteOps\\remoteFuncWrapper.py"
@@ -1,26 +1,20 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2023-2024 NV Access Limited
+# Copyright (C) 2023-2025 NV Access Limited
 
 
-from __future__ import annotations
+from collections.abc import Callable
 from typing import (
 	Generator,
 	ContextManager,
-	Callable,
 	Concatenate,
-	ParamSpec,
-	TypeVar,
 )
 import functools
 import contextlib
 from . import builder
 
-
-_remoteFunc_self = TypeVar("_remoteFunc_self", bound=builder._RemoteBase)
-_remoteFunc_paramSpec = ParamSpec("_remoteFunc_paramSpec")
-_remoteFunc_return = TypeVar("_remoteFunc_return")
+_remoteFunc_self = builder._RemoteBase
 
 
 class _BaseRemoteFuncWrapper:
@@ -29,13 +23,13 @@ def generateArgsKwargsString(self, *args, **kwargs) -> str:
 		kwargsString = ", ".join(f"{key}={repr(val)}" for key, val in kwargs.items())
 		return f"({', '.join([argsString, kwargsString])})"
 
-	def _execRawFunc(
+	def _execRawFunc[**P, R](
 		self,
-		func: Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], _remoteFunc_return],
+		func: Callable[Concatenate[_remoteFunc_self, P], R],
 		funcSelf: _remoteFunc_self,
-		*args: _remoteFunc_paramSpec.args,
-		**kwargs: _remoteFunc_paramSpec.kwargs,
-	) -> _remoteFunc_return:
+		*args: P.args,
+		**kwargs: P.kwargs,
+	) -> R:
 		main = funcSelf.rob.getInstructionList("main")
 		main.addComment(
 			f"Entering {func.__qualname__}{self.generateArgsKwargsString(*args, **kwargs)}",
@@ -44,16 +38,16 @@ def _execRawFunc(
 		main.addComment(f"Exiting {func.__qualname__}")
 		return res
 
-	def __call__(
+	def __call__[**P, R](
 		self,
-		func: Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], _remoteFunc_return],
-	) -> Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], _remoteFunc_return]:
+		func: Callable[Concatenate[_remoteFunc_self, P], R],
+	) -> Callable[Concatenate[_remoteFunc_self, P], R]:
 		@functools.wraps(func)
 		def wrapper(
 			funcSelf: _remoteFunc_self,
-			*args: _remoteFunc_paramSpec.args,
-			**kwargs: _remoteFunc_paramSpec.kwargs,
-		) -> _remoteFunc_return:
+			*args: P.args,
+			**kwargs: P.kwargs,
+		) -> R:
 			return self._execRawFunc(func, funcSelf, *args, **kwargs)
 
 		return wrapper
@@ -65,40 +59,40 @@ class RemoteMethodWrapper(_BaseRemoteFuncWrapper):
 	def __init__(self, mutable: bool = False):
 		self._mutable = mutable
 
-	def _execRawFunc(
+	def _execRawFunc[**P, R](
 		self,
-		func: Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], _remoteFunc_return],
+		func: Callable[Concatenate[_remoteFunc_self, P], R],
 		funcSelf: _remoteFunc_self,
-		*args: _remoteFunc_paramSpec.args,
-		**kwargs: _remoteFunc_paramSpec.kwargs,
-	) -> _remoteFunc_return:
+		*args: P.args,
+		**kwargs: P.kwargs,
+	) -> R:
 		if self._mutable and not funcSelf._mutable:
 			raise RuntimeError(f"{funcSelf.__class__.__name__} is not mutable")
 		return super()._execRawFunc(func, funcSelf, *args, **kwargs)
 
 
 class RemoteContextManager(_BaseRemoteFuncWrapper):
-	def __call__(
+	def __call__[**P, R](
 		self,
 		func: Callable[
-			Concatenate[_remoteFunc_self, _remoteFunc_paramSpec],
-			Generator[_remoteFunc_return, None, None],
+			Concatenate[_remoteFunc_self, P],
+			Generator[R, None, None],
 		],
-	) -> Callable[Concatenate[_remoteFunc_self, _remoteFunc_paramSpec], ContextManager[_remoteFunc_return]]:
+	) -> Callable[Concatenate[_remoteFunc_self, P], ContextManager[R]]:
 		contextFunc = contextlib.contextmanager(func)
 		return super().__call__(contextFunc)
 
 	@contextlib.contextmanager
-	def _execRawFunc(
+	def _execRawFunc[**P, R](
 		self,
 		func: Callable[
-			Concatenate[_remoteFunc_self, _remoteFunc_paramSpec],
-			ContextManager[_remoteFunc_return],
+			Concatenate[_remoteFunc_self, P],
+			ContextManager[R],
 		],
 		funcSelf: _remoteFunc_self,
-		*args: _remoteFunc_paramSpec.args,
-		**kwargs: _remoteFunc_paramSpec.kwargs,
-	) -> Generator[_remoteFunc_return, None, None]:
+		*args: P.args,
+		**kwargs: P.kwargs,
+	) -> Generator[R, None, None]:
 		main = funcSelf.rob.getInstructionList("main")
 		main.addComment(
 			f"Entering context manager {func.__qualname__}{self.generateArgsKwargsString(*args, **kwargs)}",

```