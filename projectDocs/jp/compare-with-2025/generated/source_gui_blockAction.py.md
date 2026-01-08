# Diff for: `source\gui\blockAction.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\gui\blockAction.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\blockAction.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\blockAction.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\blockAction.py"
index 008ade6..21fbe4a 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\blockAction.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\blockAction.py"
@@ -39,6 +39,14 @@ def _isRemoteAccessDisabled() -> bool:
 	return not remoteRunning()
 
 
+def _isScreenCurtainEnabled() -> bool:
+	"""Whether screen curtain functionality is **enabled**."""
+	# Import late to avoid circular import
+	from screenCurtain import screenCurtain
+
+	return screenCurtain is not None and screenCurtain.enabled
+
+
 @dataclass
 class _Context:
 	blockActionIf: Callable[[], bool]
@@ -86,6 +94,11 @@ class Context(_Context, Enum):
 		# Translators: Reported when an action cannot be performed because Remote Access functionality is disabled.
 		pgettext("remote", "Action unavailable when Remote Access is disabled"),
 	)
+	SCREEN_CURTAIN = (
+		lambda: _isScreenCurtainEnabled(),
+		# Translators: Reported when an action cannot be performed because screen curtain is enabled.
+		_("Action unavailable while screen curtain is enabled"),
+	)
 
 
 def when(*contexts: Context):

```