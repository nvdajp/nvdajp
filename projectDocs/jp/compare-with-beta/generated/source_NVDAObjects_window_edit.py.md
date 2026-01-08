# Diff for: `source\NVDAObjects\window\edit.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\NVDAObjects\window\edit.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\window\edit.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\window\\edit.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\window\\edit.py"
index a334597..143f49e 100644
--- "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\window\\edit.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\window\\edit.py"
@@ -618,11 +618,59 @@ def _getLineNumFromOffset(self, offset):
 		else:
 			return watchdog.cancellableSendMessage(self.obj.windowHandle, winUser.EM_LINEFROMCHAR, offset, 0)
 
+	# BEGIN JP PATCH
+	# nvdajp: workaround for ANSI edit controls (legacy applications)
+	def _needsWorkAroundEncoding(self):
+		"""Check if ANSI encoding workaround is needed for this edit control.
+		This is for legacy ANSI applications that use Shift-JIS encoding.
+		"""
+		return config.conf["language"]["jpAnsiEditbox"] and (not self.obj.isWindowUnicode)
+
+	def _startEndInBytesToStartEndInUnicodeChars(self, start, end):
+		"""Convert byte positions to Unicode character positions for ANSI edit controls.
+		This is needed because ANSI edit controls work with byte positions,
+		but NVDA works with Unicode character positions.
+		"""
+		# start/end in bytes to start/end in unicode chars
+		story_text = self._getStoryText()
+		start_new = end_new = -1
+		bytepos = 0
+		for charpos, ch in enumerate(story_text):
+			cb = len(ch.encode("mbcs", "replace"))
+			if bytepos == start:
+				start_new = charpos
+			if bytepos == end:
+				end_new = charpos
+				break
+			bytepos += cb
+		if end_new == -1:
+			end_new = len(story_text)
+		return (start_new, end_new)
+
+	# END JP PATCH
+
 	def _getLineOffsets(self, offset):
+		# BEGIN JP PATCH
+		# nvdajp: workaround for ANSI edit controls
+		if self._needsWorkAroundEncoding():
+			# offset in unicode chars to offset in bytes
+			s = self._getStoryText()[0:offset]
+			offset = len(s.encode("mbcs", "replace"))
+		# END JP PATCH
 		lineNum = self._getLineNumFromOffset(offset)
 		start = watchdog.cancellableSendMessage(self.obj.windowHandle, winUser.EM_LINEINDEX, lineNum, 0)
 		length = watchdog.cancellableSendMessage(self.obj.windowHandle, winUser.EM_LINELENGTH, offset, 0)
 		end = start + length
+		# BEGIN JP PATCH
+		# nvdajp: convert byte positions back to Unicode character positions
+		if self._needsWorkAroundEncoding():
+			start_new, end_new = self._startEndInBytesToStartEndInUnicodeChars(start, end)
+			log.debug(
+				"offset %d lineNum %d start %d length %d end %d start_new %d end_new %d"
+				% (offset, lineNum, start, length, end, start_new, end_new)
+			)
+			return (start_new, end_new)
+		# END JP PATCH
 		# If we just seem to get invalid line info, calculate manually
 		if (
 			start <= 0

```