# Diff for: `source\systemUtils.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\systemUtils.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\systemUtils.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\systemUtils.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\systemUtils.py"
index 37a8988..cb8156d 100644
--- "a/F:\\nvda\\gh\\beta\\source\\systemUtils.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\systemUtils.py"
@@ -150,7 +150,7 @@ def execElevated(path, params=None, wait=False, handleAlreadyElevated=False):
 
 	if params is not None:
 		params = subprocess.list2cmdline(params)
-	sei = winBindings.shell32.SHELLEXECUTEINFO(lpFile=path, lpParameters=params, nShow=winUser.SW_HIDE)
+	sei = shellapi.SHELLEXECUTEINFO(lpFile=path, lpParameters=params, nShow=winUser.SW_HIDE)
 	# IsUserAnAdmin is apparently deprecated so may not work above Windows 8
 	if not handleAlreadyElevated or not winBindings.shell32.IsUserAnAdmin():
 		sei.lpVerb = "runas"
@@ -232,13 +232,17 @@ def __init__(self, func: Callable[..., _execAndPumpResT], *args, **kwargs) -> No
 		self.threadExc: Exception | None = None
 		self.start()
 		time.sleep(0.1)
+		# BEGIN JP PATCH
 		threadHandle = ctypes.wintypes.HANDLE()
 		threadHandle.value = winBindings.kernel32.OpenThread(0x100000, False, self.ident)
+		if not threadHandle.value:
+			raise ctypes.WinError()
 		msg = ctypes.wintypes.MSG()
 		while user32.MsgWaitForMultipleObjects(1, ctypes.byref(threadHandle), False, -1, 255) == 1:
 			while user32.PeekMessage(ctypes.byref(msg), None, 0, 0, 1):
 				user32.TranslateMessage(ctypes.byref(msg))
 				user32.DispatchMessage(ctypes.byref(msg))
+		# END JP PATCH
 		if self.threadExc:
 			raise self.threadExc
 

```