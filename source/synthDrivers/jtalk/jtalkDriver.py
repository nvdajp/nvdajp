# jtalkDriver.py
# -*- coding: utf-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# speech engine nvdajp_jtalk
# Copyright (C) 2010-2019 Takuya Nishimoto (nishimotz.com)

from logHandler import log
import time


import queue as Queue


import os
import baseObject
import copy
import nvwave

_espeak = None  # from .. import _espeak
from .jtalkCore import *
from . import jtalkPrepare
from ..jtalk._nvdajp_unicode import unicode_normalize
from ..jtalk import _bgthread
import time
import watchdog
import config
from .jtalkDir import jtalk_dir, dic_dir, user_dics

DEBUG = False

RATE_BOOST_MULTIPLIER = 1.5

# math.log(150) = 5.0, math.log(350) = 5.9
_jtalk_voices = [
    {
        "id": "V1",
        "name": "m001",
        "lang": "ja",
        "samp_rate": 48000,
        "fperiod": 240,
        "lf0_base": 5.0,
        "pitch_bias": 0,
        "speaker_attenuation": 1.0,
        "htsvoice": os.path.join(jtalk_dir, "m001", "m001.htsvoice"),
        "alpha": 0.55,
        "beta": 0.00,
        "espeak_variant": "max",
    },
    {
        "id": "V2",
        "name": "mei",
        "lang": "ja",
        "samp_rate": 48000,
        "fperiod": 240,
        "lf0_base": 5.9,
        "pitch_bias": -25,
        "inflection_bias": -10,
        "speaker_attenuation": 0.8,
        "htsvoice": os.path.join(jtalk_dir, "mei", "mei_happy.htsvoice"),
        "alpha": 0.60,  # 0.55,
        "beta": 0.00,
        "espeak_variant": "f1",
    },
    {
        "id": "V3",
        "name": "lite",
        "lang": "ja",
        "samp_rate": 16000,
        "fperiod": 80,
        "lf0_base": 5.0,
        "pitch_bias": 0,
        "speaker_attenuation": 1.0,
        "htsvoice": os.path.join(jtalk_dir, "lite", "voice.htsvoice"),
        "alpha": 0.42,
        "beta": 0.00,
        "espeak_variant": "max",
    },
    {
        "id": "V4",
        "name": "tohoku-f01",
        "lang": "ja",
        "samp_rate": 48000,
        "fperiod": 240,
        "fperiod_bias": 0.75,
        "lf0_base": 5.9,
        "pitch_bias": 0,
        "inflection_bias": 0,
        "speaker_attenuation": 0.8,
        "htsvoice": os.path.join(jtalk_dir, "tohokuf01", "tohoku-f01-neutral.htsvoice"),
        "alpha": 0.54,
        "beta": 0.00,
        "espeak_variant": "f1",
    },
]
default_jtalk_voice = _jtalk_voices[3]  # V4
voice_args = None


class VoiceProperty(baseObject.AutoPropertyObject):
    def __init__(self):
        super(VoiceProperty, self).__init__()


# if samp_rate==16000: normal speed = 80samples period
fperiod = 240

# gain control
max_level = 32000
thres_level = 128
thres2_level = 128
speaker_attenuation = 1.0

logwrite = log.debug
lastIndex = None
currIndex = None
player = None
currentEngine = 0  # 1:espeak 2:jtalk
indexReachedFunc = None


def isSpeaking():
    return _bgthread.isSpeaking


def setSpeaking(b):
    _bgthread.isSpeaking = b


def _jtalk_speak(msg, index=None, prop=None):
    global currIndex, buff
    global currentEngine
    global lastIndex
    # log.info("index %r msg(%s) start" % (index, msg))
    if prop is None:
        return
    currIndex = index
    if prop.characterMode:
        fperiod_current = voice_args["fperiod"]
    else:
        fperiod_current = fperiod
    msg = unicode_normalize(msg)
    msg = jtalkPrepare.convert(msg)
    lw = None
    if DEBUG:
        lw = logwrite
    setSpeaking(True)
    currentEngine = 2
    if DEBUG:
        logwrite("p:%d i:%d msg:%s" % (prop.pitch, prop.inflection, msg))
    level = int(max_level * speaker_attenuation)
    la = 0.020 * (
        prop.inflection + voice_args.get("inflection_bias", 0)
    )  # 50 = original range
    ls = 0.015 * (prop.pitch - 50.0 + voice_args["pitch_bias"])  # 50 = no shift
    lo = ls + voice_args["lf0_base"] * (1 - la)
    if DEBUG:
        logwrite("lo:%f la:%f" % (lo, la))
    lastIndex = currIndex
    currIndex = None
    for t in msg.split():
        if DEBUG:
            logwrite("unicode (%s)" % t)
        s = text2mecab(t)
        if DEBUG:
            logwrite("utf-8 (%s)" % s.decode("utf-8", "ignore"))
        if not isSpeaking():
            libjt_refresh()
            return
        mf = MecabFeatures()
        Mecab_analysis(s, mf, logwrite_=logwrite)
        if DEBUG:
            Mecab_print(mf, logwrite)
        Mecab_correctFeatures(mf)
        if DEBUG:
            Mecab_print(mf, logwrite)
        ar = Mecab_splitFeatures(mf, CODE_="utf-8")
        for a in ar:
            if isSpeaking():
                if DEBUG:
                    Mecab_print(a, logwrite, CODE_="utf-8")
                Mecab_utf8_to_cp932(a)
                if DEBUG:
                    logwrite("Mecab_analysis done")
                libjt_synthesis(
                    a.feature,
                    a.size,
                    fperiod_=fperiod_current,
                    feed_func_=player.feed,  # player.feed() is called inside
                    is_speaking_func_=isSpeaking,
                    begin_thres_=thres_level,
                    end_thres_=thres2_level,
                    level_=level,
                    logwrite_=lw,
                    lf0_offset_=lo,
                    lf0_amp_=la,
                )
                libjt_refresh()
                if DEBUG:
                    logwrite("libjt_synthesis done")
            del a
        del mf
    player.idle()
    # log.info('player.idle done. lastIndex %r' % lastIndex)
    setSpeaking(False)
    currentEngine = 0


espeakMark = 10000


def _espeak_speak(msg, lang, index=None, prop=None):
    global currentEngine, lastIndex, espeakMark
    currentEngine = 1
    msg = str(msg)
    msg.translate({ord("\01"): None, ord("<"): "&lt;", ord(">"): "&gt;"})
    msg = '<voice xml:lang="%s">%s</voice>' % (lang, msg)
    msg += '<mark name="%d" />' % espeakMark
    _espeak.speak(msg)
    if hasattr(_espeak, "lastIndex"):
        while currentEngine == 1 and _espeak.lastIndex != espeakMark:
            time.sleep(0.1)
            watchdog.alive()
    time.sleep(0.4)
    watchdog.alive()
    lastIndex = index
    currentEngine = 0
    espeakMark += 1


# call from BgThread
def _speak(arg):
    msg, lang, index, prop = arg
    if DEBUG:
        logwrite("[" + lang + "]" + msg)
    if DEBUG:
        logwrite("_speak(%s)" % msg)
    if _espeak is None or lang == "ja":
        # log.info("_jtalk_speak")
        _jtalk_speak(msg, index, prop)
    else:
        _espeak_speak(msg, lang, index, prop)


indexCommands = []
lastIndexCommand = None


def _processIndexReached():
    global indexCommands
    flag = False
    indexCommandsNew = []
    for item in indexCommands:
        if indexReachedFunc and (lastIndex is None or item <= lastIndex):
            indexReachedFunc(item)
            flag = True
        else:
            indexCommandsNew.append(item)
    if flag:
        indexCommands = indexCommandsNew
        # log.info("lastIndex %r indexCommands %r" % (lastIndex, indexCommands))


# call from BgThread
def _updateSpeakIndex(index):
    global currIndex
    global lastIndex
    lastIndex = currIndex = index
    # log.info("lastIndex %r" % lastIndex)
    _processIndexReached()
    if not indexCommands:
        indexReachedFunc(None)


# call from nvdajp_jtalk.py
def updateIndex(index):
    global lastIndex
    lastIndex = index
    indexCommands.append(index)
    # log.info("index %r indexCommands %r" % (index, indexCommands))


def onJtalkDone():
    # log.info("onJtalkDone")
    _processIndexReached()


def onEspeakDone(index):
    # log.info("onEspeakDone %r" % index)
    _processIndexReached()


def speak(msg, lang, index=None, voiceProperty_=None):
    # log.info("index(%r) msg(%s) lang(%s)" % (index, msg, lang))
    # if msg is None and lang is None:
    # 	import tones
    # 	tones.beep(440, 10)
    # 	_bgthread.execWhenDone(_updateSpeakIndex, index, mustBeAsync=True)
    # 	return
    msg = msg.strip()
    if len(msg) == 0:
        return
    if voiceProperty_ is None:
        return
    arg = [msg, lang, index, copy.deepcopy(voiceProperty_)]
    _bgthread.execWhenDone(_speak, arg, mustBeAsync=True)


def updateSpeakIndexWhenDone(index):
    # import tones
    # tones.beep(440, 10)
    _bgthread.execWhenDone(_updateSpeakIndex, index, mustBeAsync=True)


def stop():
    global currentEngine
    if indexReachedFunc:
        for item in indexCommands:
            indexReachedFunc(item)

        indexCommands.clear()

        indexReachedFunc(None)
    if currentEngine == 1:
        _espeak.stop()
        currentEngine = 0
        return
    # Kill all speech from now.
    # We still want parameter changes to occur, so requeue them.
    params = []
    stop_task_count = 0  # for log.info()
    try:
        while True:
            item = _bgthread.bgQueue.get_nowait()  # [func, args, kwargs]
            if item[0] != _speak:
                params.append(item)
            else:
                stop_task_count = stop_task_count + 1
            _bgthread.bgQueue.task_done()
    except Queue.Empty:
        # Let the exception break us out of this loop, as queue.empty() is not reliable anyway.
        pass
    for item in params:
        _bgthread.bgQueue.put(item)
    setSpeaking(False)
    if DEBUG:
        logwrite("stop: %d task(s) stopping" % stop_task_count)
    player.stop()
    lastIndex = None


def pause(switch):
    if currentEngine == 1:
        _espeak.pause(switch)
    elif currentEngine == 2:
        player.pause(switch)


def initialize(voice=default_jtalk_voice, onIndexReached=None):
    global player, voice_args
    global speaker_attenuation
    global indexReachedFunc
    indexReachedFunc = onIndexReached
    voice_args = voice
    speaker_attenuation = voice_args["speaker_attenuation"]
    if _espeak:
        if not _espeak.espeakDLL:
            try:
                _espeak.initialize(indexCallback=onEspeakDone)
            except TypeError:
                _espeak.initialize()
            log.debug("jtalk using eSpeak version %s" % _espeak.info())
        _espeak.setVoiceByLanguage("en")
        _espeak.setVoiceAndVariant(variant=voice["espeak_variant"])
    if not player:
        player = nvwave.WavePlayer(
            channels=1,
            samplesPerSec=voice_args["samp_rate"],
            bitsPerSample=16,
            outputDevice=config.conf["audio"]["outputDevice"],
        )
    if not _bgthread.bgThread:
        _bgthread.initialize()
    if not mecab:
        lw = logwrite if DEBUG else None
        Mecab_initialize(lw, jtalk_dir, dic_dir, user_dics)
    jtalkPrepare.setup()

    jt_dll = os.path.join(jtalk_dir, "libopenjtalk.dll")
    log.debug("jt_dll %s" % jt_dll)
    libjt_initialize(jt_dll)
    libjt_set_on_done(onJtalkDone)
    log.debug(libjt_version())

    if os.path.isfile(voice_args["htsvoice"]):
        libjt_load(voice_args["htsvoice"])
        # log.info("loaded " + voice_args['htsvoice'])
    else:
        log.error("load error " + voice_args["htsvoice"])
    libjt_set_alpha(voice_args["alpha"])
    libjt_set_beta(voice_args["beta"])


def terminate():
    global player
    stop()
    _bgthread.terminate()
    player.close()
    player = None
    if _espeak:
        _espeak.terminate()


rate_percent = 50


def get_rate(rateBoost):
    return rate_percent


def set_rate(rate, rateBoost):
    global fperiod, rate_percent
    rate_percent = rate
    if voice_args["samp_rate"] == 16000:
        fperiod = int(80 - int(rate) / 2)  # 80..30
    if voice_args["samp_rate"] == 48000:
        fperiod = int(240 - 1.5 * int(rate))  # 240..90
    if not rateBoost:
        fperiod = int(fperiod * RATE_BOOST_MULTIPLIER)
    fperiod = int(fperiod * voice_args.get("fperiod_bias", 1))


def set_volume(vol):
    global max_level, thres_level, thres2_level
    max_level = int(326.67 * int(vol) + 100)  # 100..32767
    thres_level = 128
    thres2_level = 128
