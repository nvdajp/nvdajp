# Diff for: `source\NVDAObjects\IAccessible\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\NVDAObjects\IAccessible\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\IAccessible\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\IAccessible\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\__init__.py"
index 5e6e77d..57728ac 100644
--- "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\IAccessible\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\__init__.py"
@@ -650,6 +650,13 @@ def findOverlayClasses(self, clsList):
 			from . import mscandui
 
 			mscandui.findExtraOverlayClasses(self, clsList)
+		# BEGIN JP PATCH
+		# nvdajp: ATOK support
+		elif windowClassName[:5] in ("ATOK2", "ATOK3"):
+			from . import atok
+
+			atok.findExtraOverlayClasses(self, clsList)
+		# END JP PATCH
 		elif (
 			windowClassName == "GeckoPluginWindow"
 			and self.event_objectID == 0

```