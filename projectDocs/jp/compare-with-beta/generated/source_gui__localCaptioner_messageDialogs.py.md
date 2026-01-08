# Diff for: `source\gui\_localCaptioner\messageDialogs.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\gui\_localCaptioner\messageDialogs.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\_localCaptioner\messageDialogs.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\_localCaptioner\\messageDialogs.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\_localCaptioner\\messageDialogs.py"
index c7a3e7c..86421d4 100644
--- "a/F:\\nvda\\gh\\beta\\source\\gui\\_localCaptioner\\messageDialogs.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\_localCaptioner\\messageDialogs.py"
@@ -4,46 +4,31 @@
 # For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
 
 from gui.message import MessageDialog, DefaultButton, ReturnCode, DialogType
-import gui
-from _localCaptioner.modelDownloader import ModelDownloader, ProgressCallback
+from _localCaptioner.modelDownloader import ModelDownloader
 import threading
 from threading import Thread
 import wx
 import ui
 import _localCaptioner
 
-
-class ImageDescDownloader:
 _downloadThread: Thread | None = None
-	isOpening: bool = False
-
-	def __init__(self):
-		self.downloadDict: dict[str, tuple[int, int]] = {}
-		self.modelDownloader: ModelDownloader | None = None
-		self._shouldCancel = False
-		self._progressDialog: wx.ProgressDialog | None = None
-		self.filesToDownload = [
-			"onnx/encoder_model_quantized.onnx",
-			"onnx/decoder_model_merged_quantized.onnx",
-			"config.json",
-			"vocab.json",
-			"preprocessor_config.json",
-		]
-
-	def onDownload(self, progressCallback: ProgressCallback) -> None:
-		self.modelDownloader = ModelDownloader()
-		(success, fail) = self.modelDownloader.downloadModelsMultithreaded(
-			filesToDownload=self.filesToDownload,
-			progressCallback=progressCallback,
-		)
-		if len(fail) == 0:
-			wx.CallAfter(self.openSuccessDialog)
+_failedFiles: list[str] = []
+
+
+def onDownload() -> None:
+	modelDownloader = ModelDownloader()
+	(successful, failed) = modelDownloader.downloadModelsMultithreaded()
+	if len(failed) == 0:
+		wx.CallAfter(openSuccessDialog)
 	else:
-			wx.CallAfter(self.openFailDialog)
+		# Store failed files for error message
+		global _failedFiles
+		_failedFiles = failed
+		wx.CallAfter(openFailDialog)
 
-	def openSuccessDialog(self) -> None:
-		confirmationButton = (DefaultButton.OK.value._replace(defaultFocus=True, fallbackAction=True),)
-		self._stopped()
+
+def openSuccessDialog() -> None:
+	confirmationButton = (DefaultButton.YES.value._replace(defaultFocus=True, fallbackAction=True),)
 
 	dialog = MessageDialog(
 		parent=None,
@@ -58,49 +43,52 @@ def openSuccessDialog(self) -> None:
 		buttons=confirmationButton,
 	)
 
-		if dialog.ShowModal() == ReturnCode.OK:
-			# load image desc after successful download
-			if not _localCaptioner.isModelLoaded():
-				_localCaptioner.toggleImageCaptioning()
+	if dialog.ShowModal() == ReturnCode.YES:
+		pass
 
-	def openFailDialog(self) -> None:
-		if self._shouldCancel:
-			return
 
+def openFailDialog() -> None:
+	global _failedFiles
 	confirmationButtons = (
-			DefaultButton.YES.value._replace(defaultFocus=True, fallbackAction=False),
-			DefaultButton.NO.value._replace(defaultFocus=False, fallbackAction=True),
+		DefaultButton.YES.value._replace(defaultFocus=True, fallbackAction=True),
+		DefaultButton.NO,
 	)
 
-		dialog = MessageDialog(
-			parent=None,
-			# Translators: title of dialog when fail to download
-			title=pgettext("imageDesc", "Download failed"),
+	# Build error message with failed files
+	failedFilesStr = ", ".join(_failedFiles) if _failedFiles else "unknown files"
 	message = pgettext(
 		"imageDesc",
 		# Translators: label of dialog when fail to download image captioning
 		"Image captioning download failed. Would you like to retry?",
-			),
+	)
+	if _failedFiles:
+		message += f"\n\nFailed files: {failedFilesStr}"
+
+	dialog = MessageDialog(
+		parent=None,
+		# Translators: title of dialog when fail to download
+		title=pgettext("imageDesc", "Download failed"),
+		message=message,
 		dialogType=DialogType.WARNING,
 		buttons=confirmationButtons,
 	)
 
 	if dialog.ShowModal() == ReturnCode.YES:
-			self.doDownload()
-		else:
-			self._stopped()
+		global _downloadThread
+		_downloadThread = threading.Thread(target=onDownload, name="ModelDownloadMainThread", daemon=False)
+		_downloadThread.start()
 
-	def openDownloadDialog(self) -> None:
-		if ImageDescDownloader._downloadThread is not None and ImageDescDownloader._downloadThread.is_alive():
+
+def openDownloadDialog() -> None:
+	global _downloadThread
+	if _downloadThread is not None and _downloadThread.is_alive():
 		# Translators: message when image captioning is still downloading
 		ui.message(pgettext("imageDesc", "image captioning is still downloading, please wait..."))
 		return
-		if ImageDescDownloader.isOpening:
-			return
 
 	confirmationButtons = (
-			DefaultButton.YES.value._replace(defaultFocus=True, fallbackAction=False),
-			DefaultButton.NO.value._replace(defaultFocus=False, fallbackAction=True),
+		DefaultButton.YES.value._replace(defaultFocus=True, fallbackAction=True),
+		DefaultButton.NO,
 	)
 
 	dialog = MessageDialog(
@@ -115,57 +103,10 @@ def openDownloadDialog(self) -> None:
 		dialogType=DialogType.WARNING,
 		buttons=confirmationButtons,
 	)
-		ImageDescDownloader.isOpening = True
 
 	if dialog.ShowModal() == ReturnCode.YES:
-			self._progressDialog = wx.ProgressDialog(
-				# Translators: The title of the dialog displayed while downloading image descriptioner.
-				pgettext("imageDesc", "Downloading Image Descriptioner"),
-				# Translators: The progress message indicating that a connection is being established.
-				pgettext("imageDesc", "Connecting"),
-				style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE,
-				parent=gui.mainFrame,
-			)
-			self.doDownload()
-		else:
-			ImageDescDownloader.isOpening = False
-
-	def doDownload(self):
-		def progressCallback(
-			fileName: str,
-			downloadedBytes: int,
-			totalBytes: int,
-			_percentage: float,
-		) -> None:
-			"""Callback function to capture progress data."""
-			self.downloadDict[fileName] = (downloadedBytes, totalBytes)
-			downloadedSum = sum(d for d, _ in self.downloadDict.values())
-			totalSum = sum(t for _, t in self.downloadDict.values())
-			ratio = downloadedSum / totalSum if totalSum > 0 else 0.0
-			totalProgress = int(ratio * 100)
-			# update progress when downloading all files to prevent premature stop
-			if len(self.downloadDict) == len(self.filesToDownload):
-				# Translators: The progress message indicating that a download is in progress.
-				cont, skip = self._progressDialog.Update(totalProgress, pgettext("imageDesc", "downloading"))
-				if not cont:
-					self._shouldCancel = True
-					self._stopped()
-
-		ImageDescDownloader._downloadThread = threading.Thread(
-			target=self.onDownload,
-			name="ModelDownloadMainThread",
-			daemon=False,
-			args=(progressCallback,),
-		)
-		ImageDescDownloader._downloadThread.start()
-
-	def _stopped(self):
-		self.modelDownloader.requestCancel()
-		ImageDescDownloader._downloadThread = None
-		self._progressDialog.Hide()
-		self._progressDialog.Destroy()
-		self._progressDialog = None
-		ImageDescDownloader.isOpening = False
+		_downloadThread = threading.Thread(target=onDownload, name="ModelDownloadMainThread", daemon=False)
+		_downloadThread.start()
 
 
 def openEnableOnceDialog() -> None:

```