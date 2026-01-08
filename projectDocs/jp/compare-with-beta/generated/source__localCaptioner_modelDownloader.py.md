# Diff for: `source\_localCaptioner\modelDownloader.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\_localCaptioner\modelDownloader.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\_localCaptioner\modelDownloader.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_localCaptioner\\modelDownloader.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_localCaptioner\\modelDownloader.py"
index 476b91d..80e1a54 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_localCaptioner\\modelDownloader.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_localCaptioner\\modelDownloader.py"
@@ -136,8 +136,8 @@ def constructDownloadUrl(
 		model = modelName.strip("/")
 		ref = resolvePath.strip("/")
 		filePath = filePath.lstrip("/")
-
-		return f"{base}/{model}/{ref}/{filePath}"
+		url = f"{base}/{model}/{ref}/{filePath}"
+		return url
 
 	def _getRemoteFileSize(self, url: str) -> int:
 		"""
@@ -151,7 +151,7 @@ def _getRemoteFileSize(self, url: str) -> int:
 
 		try:
 			# Use HEAD request with automatic redirect following
-			response = self.session.head(url, timeout=10, allow_redirects=True)
+			response = self.session.head(url, timeout=30, allow_redirects=True)
 			response.raise_for_status()
 		except Exception as e:
 			if not self.cancelRequested:
@@ -163,7 +163,7 @@ def _getRemoteFileSize(self, url: str) -> int:
 
 		try:
 			# If HEAD doesn't work, try GET with range header to get just 1 byte
-			response = self.session.get(url, headers={"Range": "bytes=0-0"}, timeout=10, allow_redirects=True)
+			response = self.session.get(url, headers={"Range": "bytes=0-0"}, timeout=30, allow_redirects=True)
 		except Exception as e:
 			if not self.cancelRequested:
 				log.warning(f"Failed to get remote file size (GET) for {url}: {e}")
@@ -419,7 +419,6 @@ def _performSingleDownload(
 		try:
 			# Determine total file size
 			total = self._calculateTotalSize(response, resumePos)
-
 			if total > 0:
 				log.debug(f"Total file size: {total:,} bytes")
 
@@ -437,7 +436,8 @@ def _performSingleDownload(
 				return False, message
 
 			# Verify download integrity
-			return self._verifyDownloadIntegrity(localPath, fileName, total, progressCallback, threadId)
+			result = self._verifyDownloadIntegrity(localPath, fileName, total, progressCallback, threadId)
+			return result
 
 		finally:
 			response.close()
@@ -480,7 +480,7 @@ def _getDownloadResponse(self, url: str, resumePos: int, localPath: str, threadI
 			url,
 			headers=headers,
 			stream=True,
-			timeout=10,
+			timeout=30,
 			allow_redirects=True,
 		)
 
@@ -499,7 +499,7 @@ def _getDownloadResponse(self, url: str, resumePos: int, localPath: str, threadI
 
 			# Make new request without range header
 			response.close()
-			response = self.session.get(url, stream=True, timeout=10, allow_redirects=True)
+			response = self.session.get(url, stream=True, timeout=30, allow_redirects=True)
 
 		response.raise_for_status()
 		return response
@@ -732,16 +732,17 @@ def downloadModelsMultithreaded(
 					self.activeFutures.discard(future)
 
 				try:
-					ok, msg = future.result()
+					# Use a short timeout to avoid blocking indefinitely
+					ok, msg = future.result(timeout=1.0)
 					if ok:
 						successful.append(filePath)
 						log.debug(f"successful {filePath=}")
 					else:
 						failed.append(filePath)
-						log.debug(f"failed: {filePath} - {msg}")
+						log.warning(f"Download failed: {filePath} - {msg}")
 				except Exception as err:
 					failed.append(filePath)
-					log.debug(f"failed: {filePath} – {err}")
+					log.error(f"Download exception: {filePath} – {err}", exc_info=True)
 
 		# Summary
 		if not self.cancelRequested:

```