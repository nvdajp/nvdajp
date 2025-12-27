# nvdajp_jtalk.py
# -*- coding: utf-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2010 NVDA Contributors <http://www.nvda-project.org/>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
#
# Copyright (C) 2013 Masamitsu Misono (043.jp)
# Copyright (C) 2010-2021 Takuya Nishimoto (nishimotz.com)
# Released under GPL 2

from synthDriverHandler import SynthDriver, VoiceInfo
from collections import OrderedDict
from logHandler import log

try:
    from speech.commands import (
        IndexCommand,
        CharacterModeCommand,
        LangChangeCommand,
        PitchCommand,
        SpeechCommand,
    )
except ImportError:
    from speech import (
        IndexCommand,
        CharacterModeCommand,
        LangChangeCommand,
        PitchCommand,
        SpeechCommand,
    )
import synthDriverHandler
import languageHandler
from .jtalk import jtalkDriver
from .jtalk.jtalkDriver import VoiceProperty
from .jtalk._nvdajp_espeak import isJapaneseLang

try:
    from synthDriverHandler import synthIndexReached, synthDoneSpeaking
except ImportError:
    synthIndexReached = synthDoneSpeaking = None


class SynthDriver(SynthDriver):
    """A Japanese synth driver for NVDAjp."""

    name = "nvdajp_jtalk"
    description = "JTalk"
    supportedSettings = (
        SynthDriver.VoiceSetting(),
        SynthDriver.RateSetting(),
        SynthDriver.RateBoostSetting()
        if hasattr(SynthDriver, "RateBoostSetting")
        else synthDriverHandler.BooleanSynthSetting("rateBoost", _("Rate boos&t")),
        SynthDriver.PitchSetting(),
        SynthDriver.InflectionSetting(),
        SynthDriver.VolumeSetting(),
    )
    supportedCommands = {
        IndexCommand,
        CharacterModeCommand,
        LangChangeCommand,
        PitchCommand,
    }
    supportedNotifications = {synthIndexReached, synthDoneSpeaking}

    @classmethod
    def check(cls):
        return True

    def __init__(self):
        self.voice_id = "V4"
        self._volume = 100
        self._pitch = 50
        self._pitchOffset = 0
        self._inflection = 50
        self._rateBoost = False
        jtalkDriver.initialize(onIndexReached=self._onIndexReached)
        self.rate = 50
        self.speakingIndex = None
        self.finishedIndex = None

    def speak(self, speechSequence):
        spellState = False
        defaultLanguage = languageHandler.getLanguage()
        if defaultLanguage[:2] == "ja":
            defaultLanguage = "ja"
        lang = defaultLanguage
        currentLang = lang
        for item in speechSequence:
            if isinstance(item, str):
                p = VoiceProperty()
                p.pitch = min(max(self._pitch + self._pitchOffset, 0), 100)
                p.inflection = self._inflection
                p.characterMode = spellState
                msg = str(item)
                isMsgJp = isJapaneseLang(msg)
                lang = currentLang
                if isMsgJp:
                    lang = "ja"
                elif defaultLanguage != "ja" and not isMsgJp:
                    lang = defaultLanguage
                log.debug(
                    "lang:%s idx:%r pit:%d inf:%d chr:%d (%s)"
                    % (
                        lang,
                        self.speakingIndex,
                        p.pitch,
                        p.inflection,
                        p.characterMode,
                        msg,
                    )
                )
                jtalkDriver.speak(msg, lang, index=self.speakingIndex, voiceProperty_=p)
            elif isinstance(item, IndexCommand):
                # log.info("IndexCommand %r" % self.speakingIndex)
                jtalkDriver.updateIndex(item.index)
                self.speakingIndex = item.index
            elif isinstance(item, CharacterModeCommand):
                spellState = item.state
            elif isinstance(item, LangChangeCommand):
                lang = (item.lang if item.lang else defaultLanguage).replace("_", "-")
                if lang[:2] == "ja":
                    lang = "ja"
                currentLang = lang
            elif isinstance(item, PitchCommand):
                self._pitchOffset = item.offset
            elif isinstance(item, SpeechCommand):
                log.debugWarning("Unsupported speech command: %s" % item)
            else:
                log.error("Unknown speech: %s" % item)
        jtalkDriver.updateSpeakIndexWhenDone(self.speakingIndex)

    def cancel(self):
        jtalkDriver.stop()

    def pause(self, switch):
        jtalkDriver.pause(switch)

    def isSpeaking(self):
        return jtalkDriver.isSpeaking()

    def _get_rateBoost(self):
        return self._rateBoost

    def _set_rateBoost(self, enable):
        if enable == self._rateBoost:
            return
        rate = self.rate
        self._rateBoost = enable
        self.rate = rate

    def terminate(self):
        jtalkDriver.terminate()

    # The current rate; ranges between 0 and 100
    def _get_rate(self):
        return jtalkDriver.get_rate(self._rateBoost)

    def _set_rate(self, rate):
        jtalkDriver.set_rate(int(rate), self._rateBoost)

    def _get_pitch(self):
        return self._pitch

    def _set_pitch(self, pitch):
        self._pitch = int(pitch)

    def _get_volume(self):
        return self._volume

    def _set_volume(self, volume_):
        self._volume = int(volume_)
        jtalkDriver.set_volume(self._volume)
        return

    def _get_inflection(self):
        return self._inflection

    def _set_inflection(self, val):
        self._inflection = int(val)

    def _getAvailableVoices(self):
        log.debug("_getAvailableVoices called")
        voices = OrderedDict()
        for v in jtalkDriver._jtalk_voices:
            voices[v["id"]] = VoiceInfo(v["id"], v["name"], v["lang"])
        return voices

    def _get_voice(self):
        log.debug("_get_voice called")
        return self.voice_id

    def _set_voice(self, identifier):
        log.debug("_set_voice %s" % (identifier))
        rate = jtalkDriver.get_rate(self._rateBoost)
        for v in jtalkDriver._jtalk_voices:
            if v["id"] == identifier:
                if self.voice_id != identifier:
                    self.voice_id = identifier
                    jtalkDriver.terminate()
                    jtalkDriver.initialize(v, onIndexReached=self._onIndexReached)
                    jtalkDriver.set_rate(rate, self._rateBoost)
                    jtalkDriver.set_volume(self._volume)
                    return
        return

    def _get_lastIndex(self):
        if jtalkDriver.lastIndex is None:
            # log.debug("_get_lastIndex returns None")
            return None
        # log.debug("_get_lastIndex returns %d" % jtalkDriver.lastIndex)
        return jtalkDriver.lastIndex

    def _onIndexReached(self, index):
        self.finishedIndex = index
        if self.finishedIndex is None:
            # log.info("synthDoneSpeaking")
            if synthDoneSpeaking:
                synthDoneSpeaking.notify(synth=self)
        else:
            # log.info("synthIndexReached %r" % self.finishedIndex)
            if synthIndexReached:
                synthIndexReached.notify(synth=self, index=self.finishedIndex)
