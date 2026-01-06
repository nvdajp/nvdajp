# Diff for: `source\textUtils\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\textUtils\__init__.py`  
**Current**: `F:\nvda\gh\alphajp\source\textUtils\__init__.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\textUtils\\__init__.py" "b/F:\\nvda\\gh\\alphajp\\source\\textUtils\\__init__.py"
index 0f11c45722..d88ef05557 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\textUtils\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\textUtils\\__init__.py"
@@ -105,7 +105,7 @@ def encodedToStrOffsets(
 
 
 class WideStringOffsetConverter(OffsetConverter):
-	R"""
+	"""
 	Object that holds a string in both its decoded and its UTF-16 encoded form.
 	The object allows for easy conversion between offsets in str type strings,
 	and offsets in wide character (UTF-16) strings (that are aware of surrogate characters).
@@ -115,12 +115,8 @@ class WideStringOffsetConverter(OffsetConverter):
 	In UTF-16 encoded strings, 32-bit unicode characters (such as emoji)
 	are encoded as one high surrogate and one low surrogate character.
 	Therefore, they take not one, but two offsets in such a string.
-	This behavior is equivalent to how Python 2 unicode strings behave,
-	which are internally encoded as UTF-16.
 
 	For example: 😂 takes one offset in a Python 3 string.
-	However, in a Python 2 string or UTF-16 encoded wide string,
-	this character internally consists of two characters: \ud83d and \ude02.
 	"""
 
 	_encoding: str = WCHAR_ENCODING

```