# Diff for: `source\_remoteClient\urlHandler.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\_remoteClient\urlHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\_remoteClient\urlHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\urlHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\urlHandler.py"
index bd39535..6b572ee 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\urlHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\urlHandler.py"
@@ -25,8 +25,7 @@
 import sys
 import winreg
 
-
-_REGISTRY_KEY_PATH: str = r"SOFTWARE\Classes\nvdaremote"
+from config.registry import RegistryKey, _deleteKeyAndSubkeys
 
 
 def _createRegistryStructure(keyHandle: winreg.HKEYType, data: dict):
@@ -44,7 +43,7 @@ def _createRegistryStructure(keyHandle: winreg.HKEYType, data: dict):
 				try:
 					_createRegistryStructure(subkey, value)
 				finally:
-					winreg.CloseKey(subkey)
+					subkey.Close()
 			except WindowsError as e:
 				raise OSError(f"Failed to create registry subkey {name}: {e}")
 		else:
@@ -55,42 +54,13 @@ def _createRegistryStructure(keyHandle: winreg.HKEYType, data: dict):
 				raise OSError(f"Failed to set registry value {name}: {e}")
 
 
-def _deleteRegistryKeyRecursive(baseKey: int, subkeyPath: str):
-	"""Recursively deletes a registry key and all its subkeys.
-
-	:param baseKey: One of the HKEY_* constants from winreg
-	:param subkeyPath: Full registry path to the key to delete
-	:raises OSError: If deletion fails for reasons other than key not found
-	"""
-	try:
-		# Try to delete directly first
-		winreg.DeleteKey(baseKey, subkeyPath)
-	except WindowsError:
-		# If that fails, need to do recursive deletion
-		try:
-			with winreg.OpenKey(baseKey, subkeyPath, access=winreg.KEY_READ | winreg.KEY_WRITE) as key:
-				# Enumerate and delete all subkeys
-				while True:
-					try:
-						subkeyName = winreg.EnumKey(key, 0)
-						fullPath = f"{subkeyPath}\\{subkeyName}"
-						_deleteRegistryKeyRecursive(baseKey, fullPath)
-					except WindowsError:
-						break
-			# Now delete the key itself
-			winreg.DeleteKey(baseKey, subkeyPath)
-		except WindowsError as e:
-			if e.winerror != 2:  # ERROR_FILE_NOT_FOUND
-				raise OSError(f"Failed to delete registry key {subkeyPath}: {e}")
-
-
 def registerURLHandler():
 	"""Registers the nvdaremote:// URL protocol handler in the Windows Registry.
 
 	:raises OSError: If registration in the registry fails
 	"""
 	try:
-		with winreg.CreateKey(winreg.HKEY_CURRENT_USER, _REGISTRY_KEY_PATH) as key:
+		with winreg.CreateKey(winreg.HKEY_CURRENT_USER, RegistryKey.REMOTE_URL_HANDLER.value) as key:
 			_createRegistryStructure(key, URL_HANDLER_REGISTRY)
 	except OSError as e:
 		raise OSError(f"Failed to register URL handler: {e}")
@@ -102,8 +72,11 @@ def unregisterURLHandler():
 	:raises OSError: If unregistration from the registry fails
 	"""
 	try:
-		_deleteRegistryKeyRecursive(winreg.HKEY_CURRENT_USER, _REGISTRY_KEY_PATH)
-	except OSError as e:
+		_deleteKeyAndSubkeys(
+			winreg.HKEY_CURRENT_USER,
+			RegistryKey.REMOTE_URL_HANDLER.value,
+		)
+	except WindowsError as e:
 		raise OSError(f"Failed to unregister URL handler: {e}")
 
 

```