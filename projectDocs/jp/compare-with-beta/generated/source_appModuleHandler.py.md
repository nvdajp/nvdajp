# Diff for: `source\appModuleHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\appModuleHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\appModuleHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\appModuleHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModuleHandler.py"
index 85b52b5..097e766 100644
--- "a/F:\\nvda\\gh\\beta\\source\\appModuleHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModuleHandler.py"
@@ -604,17 +604,9 @@ def __repr__(self):
 	def _get_appModuleName(self):
 		return self.__class__.__module__.split(".")[-1]
 
-	_liveForEver: bool = False
-	"""
-	Set to true when NVDA cannot get enough permissions to successfully verify if the process is dead.
-	E.g. Security software such as 1Password which blocks the SYNCHRONIZE access right.
-	"""
-
 	isAlive: bool
 
 	def _get_isAlive(self) -> bool:
-		if self._liveForEver:
-			return True
 		try:
 			return bool(winKernel.waitForSingleObject(self.processHandle, 0))
 		except OSError as e:
@@ -624,16 +616,6 @@ def _get_isAlive(self) -> bool:
 					f"Process handle {self.processHandle} for {self} is invalid, assuming process is dead.",
 				)
 				return False
-			elif e.winerror == winKernel.ERROR_ACCESS_DENIED:
-				# Although we opened the process asking for the SYNCHRONIZE access right,
-				# The process is refusing us the permission when waiting on the handle.
-				# This may be a protected process like 1Password.
-				# Currently there is no alternative way to check if the process is dead, so we must assume it stays alive for ever.
-				log.debugWarning(
-					f"Access denied waiting on Process handle {self.processHandle} for {self}, cannot verify dead, marking as living for ever.",
-				)
-				self._liveForEver = True
-				return True
 			raise
 
 	def terminate(self):

```