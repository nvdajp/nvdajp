# Diff for: `source\baseObject.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\baseObject.py`  
**Current**: `F:\nvda\gh\alphajp\source\baseObject.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\baseObject.py" "b/F:\\nvda\\gh\\alphajp\\source\\baseObject.py"
index 5c22123cb8..264c5a1166 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\baseObject.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\baseObject.py"
@@ -177,7 +177,6 @@ def invalidateCaches(cls):
 		# We use a list here, as invalidating the cache on an object may cause instances to disappear,
 		# which would in turn cause an exception due to the dictionary changing size during iteration.
 		for instance in list(cls.__instances):
-			if hasattr(instance, "invalidateCache"):
 			instance.invalidateCache()
 
 

```