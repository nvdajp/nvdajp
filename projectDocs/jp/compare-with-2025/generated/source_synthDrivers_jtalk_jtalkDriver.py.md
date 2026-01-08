# Diff for: `source\synthDrivers\jtalk\jtalkDriver.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\synthDrivers\jtalk\jtalkDriver.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\synthDrivers\jtalk\jtalkDriver.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\jtalkDriver.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDrivers\\jtalk\\jtalkDriver.py"
index d626c1e..2610359 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\jtalk\\jtalkDriver.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDrivers\\jtalk\\jtalkDriver.py"
@@ -6,24 +6,44 @@
 
 from logHandler import log
 import time
-
+from typing import Any, Callable, Optional, cast
 
 import queue as Queue
 
 
-import os
 import baseObject
 import copy
 import nvwave
-
-_espeak = None  # from .. import _espeak
-from .jtalkCore import *
-from . import jtalkPrepare
-from ..jtalk._nvdajp_unicode import unicode_normalize
-from ..jtalk import _bgthread
-import watchdog
-import config
-from .jtalkDir import jtalk_dir, dic_dir, user_dics
+from pathlib import Path
+
+_espeak: Optional[Any] = None  # from .. import _espeak
+from .jtalkCore import (  # noqa: E402
+	libjt_initialize,
+	libjt_load,
+	libjt_refresh,
+	libjt_set_alpha,
+	libjt_set_beta,
+	libjt_set_on_done,
+	libjt_synthesis,
+	libjt_version,
+)
+from .mecab import (  # noqa: E402
+	mecab,
+	Mecab_analysis,
+	Mecab_correctFeatures,
+	Mecab_initialize,
+	MecabFeatures,
+	Mecab_print,
+	Mecab_splitFeatures,
+	Mecab_utf8_to_cp932,
+)
+from .text2mecab import text2mecab  # noqa: E402
+from . import jtalkPrepare  # noqa: E402
+from ..jtalk._nvdajp_unicode import unicode_normalize  # noqa: E402
+from ..jtalk import _bgthread  # noqa: E402
+import watchdog  # noqa: E402
+import config  # noqa: E402
+from .jtalkDir import jtalk_dir, dic_dir, user_dics  # noqa: E402
 
 DEBUG = False
 
@@ -40,7 +60,7 @@
 		"lf0_base": 5.0,
 		"pitch_bias": 0,
 		"speaker_attenuation": 1.0,
-        "htsvoice": os.path.join(jtalk_dir, "m001", "m001.htsvoice"),
+		"htsvoice": str(jtalk_dir / "m001" / "m001.htsvoice"),
 		"alpha": 0.55,
 		"beta": 0.00,
 		"espeak_variant": "max",
@@ -55,7 +75,7 @@
 		"pitch_bias": -25,
 		"inflection_bias": -10,
 		"speaker_attenuation": 0.8,
-        "htsvoice": os.path.join(jtalk_dir, "mei", "mei_happy.htsvoice"),
+		"htsvoice": str(jtalk_dir / "mei" / "mei_happy.htsvoice"),
 		"alpha": 0.60,  # 0.55,
 		"beta": 0.00,
 		"espeak_variant": "f1",
@@ -69,7 +89,7 @@
 		"lf0_base": 5.0,
 		"pitch_bias": 0,
 		"speaker_attenuation": 1.0,
-        "htsvoice": os.path.join(jtalk_dir, "lite", "voice.htsvoice"),
+		"htsvoice": str(jtalk_dir / "lite" / "voice.htsvoice"),
 		"alpha": 0.42,
 		"beta": 0.00,
 		"espeak_variant": "max",
@@ -85,14 +105,14 @@
 		"pitch_bias": 0,
 		"inflection_bias": 0,
 		"speaker_attenuation": 0.8,
-        "htsvoice": os.path.join(jtalk_dir, "tohokuf01", "tohoku-f01-neutral.htsvoice"),
+		"htsvoice": str(jtalk_dir / "tohokuf01" / "tohoku-f01-neutral.htsvoice"),
 		"alpha": 0.54,
 		"beta": 0.00,
 		"espeak_variant": "f1",
 	},
 ]
 default_jtalk_voice = _jtalk_voices[3]  # V4
-voice_args = None
+voice_args: Optional[dict[str, Any]] = None
 
 
 class VoiceProperty(baseObject.AutoPropertyObject):
@@ -101,20 +121,20 @@ def __init__(self):
 
 
 # if samp_rate==16000: normal speed = 80samples period
-fperiod = 240
+fperiod: int = 240
 
 # gain control
-max_level = 32000
-thres_level = 128
-thres2_level = 128
-speaker_attenuation = 1.0
+max_level: int = 32000
+thres_level: int = 128
+thres2_level: int = 128
+speaker_attenuation: float = 1.0
 
-logwrite = log.debug
-lastIndex = None
-currIndex = None
-player = None
-currentEngine = 0  # 1:espeak 2:jtalk
-indexReachedFunc = None
+logwrite: Callable[[str], None] = log.debug
+lastIndex: Optional[int] = None
+currIndex: Optional[int] = None
+player: Optional[nvwave.WavePlayer] = None
+currentEngine: int = 0  # 1:espeak 2:jtalk
+indexReachedFunc: Optional[Callable[[Optional[int]], None]] = None
 
 
 def isSpeaking():
@@ -126,12 +146,16 @@ def setSpeaking(b):
 
 
 def _jtalk_speak(msg, index=None, prop=None):
-    global currIndex, buff
+	global currIndex
 	global currentEngine
 	global lastIndex
+	global voice_args
+	global player
 	# log.info("index %r msg(%s) start" % (index, msg))
 	if prop is None:
 		return
+	assert voice_args is not None  # Type narrowing for type checkers
+	assert player is not None  # Type narrowing for type checkers
 	currIndex = index
 	if prop.characterMode:
 		fperiod_current = voice_args["fperiod"]
@@ -147,9 +171,7 @@ def _jtalk_speak(msg, index=None, prop=None):
 	if DEBUG:
 		logwrite("p:%d i:%d msg:%s" % (prop.pitch, prop.inflection, msg))
 	level = int(max_level * speaker_attenuation)
-    la = 0.020 * (
-        prop.inflection + voice_args.get("inflection_bias", 0)
-    )  # 50 = original range
+	la = 0.020 * (prop.inflection + voice_args.get("inflection_bias", 0))  # 50 = original range
 	ls = 0.015 * (prop.pitch - 50.0 + voice_args["pitch_bias"])  # 50 = no shift
 	lo = ls + voice_args["lf0_base"] * (1 - la)
 	if DEBUG:
@@ -204,11 +226,13 @@ def _jtalk_speak(msg, index=None, prop=None):
 	currentEngine = 0
 
 
-espeakMark = 10000
+espeakMark: int = 10000
 
 
 def _espeak_speak(msg, lang, index=None, prop=None):
 	global currentEngine, lastIndex, espeakMark
+	assert _espeak is not None  # Type narrowing for type checkers
+	assert lastIndex is not None  # Type narrowing for type checkers
 	currentEngine = 1
 	msg = str(msg)
 	msg.translate({ord("\01"): None, ord("<"): "&lt;", ord(">"): "&gt;"})
@@ -240,8 +264,8 @@ def _speak(arg):
 		_espeak_speak(msg, lang, index, prop)
 
 
-indexCommands = []
-lastIndexCommand = None
+indexCommands: list[int] = []
+lastIndexCommand: Optional[int] = None
 
 
 def _processIndexReached():
@@ -263,6 +287,7 @@ def _processIndexReached():
 def _updateSpeakIndex(index):
 	global currIndex
 	global lastIndex
+	assert indexReachedFunc is not None  # Type narrowing for type checkers
 	lastIndex = currIndex = index
 	# log.info("lastIndex %r" % lastIndex)
 	_processIndexReached()
@@ -272,7 +297,7 @@ def _updateSpeakIndex(index):
 
 # call from nvdajp_jtalk.py
 def updateIndex(index):
-    global lastIndex
+	global lastIndex, indexCommands
 	lastIndex = index
 	indexCommands.append(index)
 	# log.info("index %r indexCommands %r" % (index, indexCommands))
@@ -311,7 +336,10 @@ def updateSpeakIndexWhenDone(index):
 
 
 def stop():
-    global currentEngine
+	global currentEngine, indexCommands, lastIndex
+	assert _espeak is not None  # Type narrowing for type checkers
+	assert _bgthread.bgQueue is not None  # Type narrowing for type checkers
+	assert player is not None  # Type narrowing for type checkers
 	if indexReachedFunc:
 		for item in indexCommands:
 			indexReachedFunc(item)
@@ -348,6 +376,8 @@ def stop():
 
 
 def pause(switch):
+	assert _espeak is not None  # Type narrowing for type checkers
+	assert player is not None  # Type narrowing for type checkers
 	if currentEngine == 1:
 		_espeak.pause(switch)
 	elif currentEngine == 2:
@@ -360,6 +390,7 @@ def initialize(voice=default_jtalk_voice, onIndexReached=None):
 	global indexReachedFunc
 	indexReachedFunc = onIndexReached
 	voice_args = voice
+	assert voice_args is not None  # Type narrowing for type checkers
 	speaker_attenuation = voice_args["speaker_attenuation"]
 	if _espeak:
 		if not _espeak.espeakDLL:
@@ -371,11 +402,12 @@ def initialize(voice=default_jtalk_voice, onIndexReached=None):
 		_espeak.setVoiceByLanguage("en")
 		_espeak.setVoiceAndVariant(variant=voice["espeak_variant"])
 	if not player:
+		audio_config = cast(dict[str, Any], config.conf["audio"])
 		player = nvwave.WavePlayer(
 			channels=1,
 			samplesPerSec=voice_args["samp_rate"],
 			bitsPerSample=16,
-            outputDevice=config.conf["audio"]["outputDevice"],
+			outputDevice=str(audio_config["outputDevice"]),
 		)
 	if not _bgthread.bgThread:
 		_bgthread.initialize()
@@ -384,13 +416,13 @@ def initialize(voice=default_jtalk_voice, onIndexReached=None):
 		Mecab_initialize(lw, jtalk_dir, dic_dir, user_dics)
 	jtalkPrepare.setup()
 
-    jt_dll = os.path.join(jtalk_dir, "libopenjtalk.dll")
+	jt_dll = str(jtalk_dir / "libopenjtalk.dll")
 	log.debug("jt_dll %s" % jt_dll)
 	libjt_initialize(jt_dll)
 	libjt_set_on_done(onJtalkDone)
 	log.debug(libjt_version())
 
-    if os.path.isfile(voice_args["htsvoice"]):
+	if Path(voice_args["htsvoice"]).is_file():
 		libjt_load(voice_args["htsvoice"])
 		# log.info("loaded " + voice_args['htsvoice'])
 	else:
@@ -403,13 +435,14 @@ def terminate():
 	global player
 	stop()
 	_bgthread.terminate()
+	assert player is not None  # Type narrowing for type checkers
 	player.close()
 	player = None
 	if _espeak:
 		_espeak.terminate()
 
 
-rate_percent = 50
+rate_percent: int = 50
 
 
 def get_rate(rateBoost):
@@ -418,6 +451,8 @@ def get_rate(rateBoost):
 
 def set_rate(rate, rateBoost):
 	global fperiod, rate_percent
+	global voice_args
+	assert voice_args is not None  # Type narrowing for type checkers
 	rate_percent = rate
 	if voice_args["samp_rate"] == 16000:
 		fperiod = int(80 - int(rate) / 2)  # 80..30

```