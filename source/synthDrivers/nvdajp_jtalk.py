# nvdajp_jtalk.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2010 NVDA Contributors <http://www.nvda-project.org/>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
#
# Copyright (C) 2013 Masamitsu Misono (043.jp)
# Copyright (C) 2010-2021 Takuya Nishimoto (nishimotz.com)
# Released under GPL 2

from synthDriverHandler import SynthDriver as BaseSynthDriver, VoiceInfo
from collections import OrderedDict
from logHandler import log
from autoSettingsUtils.driverSetting import BooleanDriverSetting

from speech.commands import (
	BreakCommand,
	IndexCommand,
	CharacterModeCommand,
	LangChangeCommand,
	PitchCommand,
	SpeechCommand,
)
from speech.types import SpeechSequence
import languageHandler
from .jtalk import jtalkDriver
from .jtalk.jtalkDriver import VoiceProperty
from synthDriverHandler import synthIndexReached, synthDoneSpeaking


def isJapaneseLang(msg: str) -> bool:
	"""Return True if msg contains characters typically used in Japanese
	text: CJK symbols/kana/ideographs (U+3000-U+9FFF), CJK compatibility
	ideographs (U+F900-U+FAFF), or halfwidth/fullwidth forms (U+FF00-U+FFEF).
	Moved from the removed _nvdajp_espeak module."""
	for i in msg:
		c = ord(i)
		if (0x3000 <= c <= 0x9FFF) or (0xF900 <= c <= 0xFAFF) or (0xFF00 <= c <= 0xFFEF):
			return True
	return False


class SynthDriver(BaseSynthDriver):
	"""A Japanese synth driver for NVDAjp."""

	name = "nvdajp_jtalk"
	description = "JTalk"
	supportedSettings = (
		BaseSynthDriver.VoiceSetting(),
		BaseSynthDriver.RateSetting(),
		BaseSynthDriver.RateBoostSetting()
		if hasattr(BaseSynthDriver, "RateBoostSetting")
		else BooleanDriverSetting("rateBoost", _("Rate boos&t")),
		BaseSynthDriver.PitchSetting(),
		BaseSynthDriver.InflectionSetting(),
		BaseSynthDriver.VolumeSetting(),
	)
	supportedCommands = {
		BreakCommand,
		IndexCommand,
		CharacterModeCommand,
		LangChangeCommand,
		PitchCommand,
	}
	supportedNotifications = {synthIndexReached, synthDoneSpeaking}

	@classmethod
	def check(cls) -> bool:  # type: ignore[override]
		return True

	def __init__(self) -> None:
		self.voice_id = "V4"
		self._volume = 100
		self._pitch = 50
		self._pitchOffset = 0
		self._inflection = 50
		self._rateBoost = False
		jtalkDriver.initialize(onIndexReached=self._onIndexReached)
		self.rate = 50
		self.speakingIndex: int | None = None
		self.finishedIndex: int | None = None

	def speak(self, speechSequence: SpeechSequence) -> None:
		spellState = False
		defaultLanguage = languageHandler.getLanguage()
		if defaultLanguage[:2] == "ja":
			defaultLanguage = "ja"
		lang = defaultLanguage
		currentLang = lang
		for item in speechSequence:
			if isinstance(item, str):
				p = VoiceProperty()
				p.pitch = min(max(self._pitch + self._pitchOffset, 0), 100)  # type: ignore[attr-defined]
				p.inflection = self._inflection  # type: ignore[attr-defined]
				p.characterMode = spellState  # type: ignore[attr-defined]
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
						p.pitch,  # type: ignore[attr-defined]
						p.inflection,  # type: ignore[attr-defined]
						p.characterMode,  # type: ignore[attr-defined]
						msg,
					),
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
			elif isinstance(item, BreakCommand):
				jtalkDriver.speak_break(item.time)
			elif isinstance(item, SpeechCommand):
				log.debugWarning("Unsupported speech command: %s" % item)
			else:
				log.error("Unknown speech: %s" % item)
		if self.speakingIndex is not None:
			jtalkDriver.updateSpeakIndexWhenDone(self.speakingIndex)

	def cancel(self) -> None:
		jtalkDriver.stop()

	def pause(self, switch: bool) -> None:
		jtalkDriver.pause(switch)

	def isSpeaking(self) -> bool:
		return jtalkDriver.isSpeaking()

	def _get_rateBoost(self) -> bool:
		return self._rateBoost

	def _set_rateBoost(self, enable: bool) -> None:
		if enable == self._rateBoost:
			return
		rate = self.rate
		self._rateBoost = enable
		self.rate = rate

	def terminate(self) -> None:
		jtalkDriver.terminate()

	# The current rate; ranges between 0 and 100
	def _get_rate(self) -> int:
		return jtalkDriver.get_rate(self._rateBoost)

	def _set_rate(self, value: int) -> None:
		jtalkDriver.set_rate(int(value), self._rateBoost)

	def _get_pitch(self) -> int:
		return self._pitch

	def _set_pitch(self, value: int) -> None:
		self._pitch = int(value)

	def _get_volume(self) -> int:
		return self._volume

	def _set_volume(self, value: int) -> None:
		self._volume = int(value)
		jtalkDriver.set_volume(self._volume)

	def _get_inflection(self) -> int:  # type: ignore[override]
		return self._inflection

	def _set_inflection(self, value: int) -> None:
		self._inflection = int(value)

	def _getAvailableVoices(self) -> OrderedDict[str, VoiceInfo]:
		log.debug("_getAvailableVoices called")
		voices: OrderedDict[str, VoiceInfo] = OrderedDict()
		for v in jtalkDriver._jtalk_voices:
			voices[v["id"]] = VoiceInfo(v["id"], v["name"], v["lang"])
		return voices

	def _get_voice(self) -> str:
		log.debug("_get_voice called")
		return self.voice_id

	def _set_voice(self, value: str) -> None:
		log.debug("_set_voice %s" % (value))
		rate = jtalkDriver.get_rate(self._rateBoost)
		for v in jtalkDriver._jtalk_voices:
			if v["id"] == value:
				if self.voice_id != value:
					self.voice_id = value
					jtalkDriver.terminate()
					jtalkDriver.initialize(v, onIndexReached=self._onIndexReached)
					jtalkDriver.set_rate(rate, self._rateBoost)
					jtalkDriver.set_volume(self._volume)
					return
		return

	def _get_lastIndex(self) -> int | None:
		if jtalkDriver.lastIndex is None:
			# log.debug("_get_lastIndex returns None")
			return None
		# log.debug("_get_lastIndex returns %d" % jtalkDriver.lastIndex)
		return jtalkDriver.lastIndex

	def _onIndexReached(self, index: int | None) -> None:
		self.finishedIndex = index
		if self.finishedIndex is None:
			# log.info("synthDoneSpeaking")
			if synthDoneSpeaking:
				synthDoneSpeaking.notify(synth=self)
		else:
			# log.info("synthIndexReached %r" % self.finishedIndex)
			if synthIndexReached:
				synthIndexReached.notify(synth=self, index=self.finishedIndex)
