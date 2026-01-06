# Diff for: `source\synthDrivers\jtalk\_nvdajp_spellchar.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\synthDrivers\jtalk\_nvdajp_spellchar.py`  
**Current**: `F:\nvda\gh\alphajp\source\synthDrivers\jtalk\_nvdajp_spellchar.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\_nvdajp_spellchar.py" "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\jtalk\\_nvdajp_spellchar.py"
index da6e6f0988..902cc0d92b 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\_nvdajp_spellchar.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\jtalk\\_nvdajp_spellchar.py"
@@ -127,6 +127,6 @@ def convert(msg):
 	for p in _dic:
 		try:
 			msg = re.sub(p[0], p[1], msg)
-        except:
+		except Exception:
 			pass
 	return msg

```