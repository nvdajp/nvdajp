# Diff for: `source\gui\guiHelper.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\gui\guiHelper.py`  
**Current**: `F:\nvda\gh\alphajp\source\gui\guiHelper.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\guiHelper.py" "b/F:\\nvda\\gh\\alphajp\\source\\gui\\guiHelper.py"
index c7a603f194..ef1636cbb1 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\guiHelper.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\gui\\guiHelper.py"
@@ -53,7 +53,6 @@ def __init__(self, parent):
 	Any,
 	Generic,
 	Optional,
-	ParamSpec,
 	Type,
 	TypeVar,
 	Union,
@@ -484,16 +483,11 @@ class SIPABCMeta(wx.siplib.wrappertype, ABCMeta):
 	pass
 
 
-# TODO: Rewrite to use type parameter lists when upgrading to python 3.12 or later.
-_WxCallOnMain_P = ParamSpec("_WxCallOnMain_P")
-_WxCallOnMain_T = TypeVar("_WxCallOnMain_T")
-
-
-def wxCallOnMain(
-	function: Callable[_WxCallOnMain_P, _WxCallOnMain_T],
-	*args: _WxCallOnMain_P.args,
-	**kwargs: _WxCallOnMain_P.kwargs,
-) -> _WxCallOnMain_T:
+def wxCallOnMain[**P, T](
+	function: Callable[P, T],
+	*args: P.args,
+	**kwargs: P.kwargs,
+) -> T:
 	"""Call a non-thread-safe wx function in a thread-safe way.
 	Blocks current thread.
 
@@ -532,11 +526,7 @@ def functionWrapper():
 		return result
 
 
-# TODO: Rewrite to use type parameter lists when upgrading to python 3.12 or later.
-_AlwaysCallAfterP = ParamSpec("_AlwaysCallAfterP")
-
-
-def alwaysCallAfter(func: Callable[_AlwaysCallAfterP, Any]) -> Callable[_AlwaysCallAfterP, None]:
+def alwaysCallAfter[**P](func: Callable[P, Any]) -> Callable[P, None]:
 	"""Makes GUI updates thread-safe by running in the main thread.
 
 	Example:
@@ -549,7 +539,7 @@ def updateLabel(text):
 	"""
 
 	@wraps(func)
-	def wrapper(*args: _AlwaysCallAfterP.args, **kwargs: _AlwaysCallAfterP.kwargs) -> None:
+	def wrapper(*args: P.args, **kwargs: P.kwargs) -> None:
 		wx.CallAfter(func, *args, **kwargs)
 
 	return wrapper

```