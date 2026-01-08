# Diff for: `source\synthDrivers\oneCore.py`

**Source**: `F:\nvda\gh\beta\source\synthDrivers\oneCore.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\synthDrivers\oneCore.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\synthDrivers\\oneCore.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDrivers\\oneCore.py"
index 0b00add..e7f2323 100644
--- "a/F:\\nvda\\gh\\beta\\source\\synthDrivers\\oneCore.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDrivers\\oneCore.py"
@@ -247,6 +247,10 @@ def __init__(self):
 
 		self._wasCancelled = False
 		self._isProcessing = False
+		# BEGIN JP PATCH
+		# nvdajp: track speaking state for isSpeaking() method
+		self._isSpeaking = False
+		# END JP PATCH
 		# Initialize the voice to a sane default
 		self.voice = self._getDefaultVoice()
 		self._consecutiveSpeechFailures = 0
@@ -315,6 +319,10 @@ def speak(self, speechSequence: SpeechSequence) -> None:
 		if self._player:
 			self._player.open()
 		self._queueSpeech(text)
+		# BEGIN JP PATCH
+		# nvdajp: mark as speaking when speech is queued
+		self._isSpeaking = True
+		# END JP PATCH
 
 	def _queueSpeech(self, item: str) -> None:
 		self._queuedSpeech.append(item)
@@ -407,6 +415,10 @@ def _processQueue(self):
 				log.debug("Calling idle on audio player")
 			self._player.idle()
 			synthDoneSpeaking.notify(synth=self)
+			# BEGIN JP PATCH
+			# nvdajp: mark as not speaking when speech is done
+			self._isSpeaking = False
+			# END JP PATCH
 		while self._queuedSpeech:
 			item = self._queuedSpeech.pop(0)
 			if isinstance(item, tuple):
@@ -627,6 +639,13 @@ def pause(self, switch):
 		if self._player:
 			self._player.pause(switch)
 
+	# BEGIN JP PATCH
+	# nvdajp: provide isSpeaking() method to check if synthesizer is currently speaking
+	def isSpeaking(self):
+		return self._isSpeaking
+
+	# END JP PATCH
+
 
 # Alias to allow look up by name "SynthDriver"
 SynthDriver = OneCoreSynthDriver

```