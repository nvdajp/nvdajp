# Diff for: `tests\system\libraries\_chromeArgs.py`

**Source**: `F:\nvda\gh\beta\tests\system\libraries\_chromeArgs.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\system\libraries\_chromeArgs.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\system\\libraries\\_chromeArgs.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\_chromeArgs.py"
index 0f9c01f..d7abff5 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\system\\libraries\\_chromeArgs.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\_chromeArgs.py"
@@ -23,7 +23,11 @@ def getChromeArgs() -> str:
 		" --disable-notifications"  # prevent notifications that may interfere with automated tests.
 		" --no-experiments"  # Stable behavior is preferred.
 		" --no-default-browser-check"  # Don't bother to check if Chrome is the default browser.
-		" --lang=en-US"  # Set GUI lang to English to ensure tests pass on non-English systems. Must be supplied
+		# BEGIN JP PATCH (Japanese UI language and guest mode for local testing)
+		" --lang=ja-JP"  # Set GUI lang to Japanese.
+		" --guest"  # Run as guest. Skip profile chooser.
+		# END JP PATCH
+		# Original: " --lang=en-US"  # Set GUI lang to English to ensure tests pass on non-English systems. Must be supplied
 		# to the first Chrome process started.
 		" --disable-session-crashed-bubble"
 		# --disable-session-crashed-bubble: If chrome crashes, don't cause subsequent tests to fail.

```