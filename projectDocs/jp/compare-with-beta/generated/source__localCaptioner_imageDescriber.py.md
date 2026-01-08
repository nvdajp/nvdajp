# Diff for: `source\_localCaptioner\imageDescriber.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\_localCaptioner\imageDescriber.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\_localCaptioner\imageDescriber.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\_localCaptioner\\imageDescriber.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_localCaptioner\\imageDescriber.py"
index 1e19378..6a599da 100644
--- "a/F:\\nvda\\gh\\beta\\source\\_localCaptioner\\imageDescriber.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_localCaptioner\\imageDescriber.py"
@@ -123,10 +123,8 @@ def _doCaption(self) -> None:
 		imageData = _screenshotNavigator()
 
 		if not self.isModelLoaded:
-			from gui._localCaptioner.messageDialogs import openEnableOnceDialog
-
-			# Ask to enable image desc only in this session, No configuration modifications
-			wx.CallAfter(openEnableOnceDialog)
+			# Translators: Message when image description is not enabled
+			ui.message(pgettext("imageDesc", "image description is not enabled"))
 			return
 
 		if self.captionThread is not None and self.captionThread.is_alive():
@@ -165,10 +163,9 @@ def _loadModel(self, localModelDirPath: str | None = None) -> None:
 			)
 		except FileNotFoundError:
 			self.isModelLoaded = False
-			from gui._localCaptioner.messageDialogs import ImageDescDownloader
+			from gui._localCaptioner.messageDialogs import openDownloadDialog
 
-			descDownloader = ImageDescDownloader()
-			wx.CallAfter(descDownloader.openDownloadDialog)
+			wx.CallAfter(openDownloadDialog)
 		except Exception:
 			self.isModelLoaded = False
 			# Translators: error message when fail to load model

```