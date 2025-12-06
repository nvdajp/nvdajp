# jtalkCore.py
# -*- coding: utf-8 -*-
# Copyright (C) 2013-2019 Takuya Nishimoto

try:
    from .mecab import *
except (ImportError, ValueError):
    from mecab import *

############################################

# htsengineapi/include/HTS_engine.h

hts_boolean = c_char
c_size_t_p = POINTER(c_size_t)
c_size_t_p_p = POINTER(c_size_t_p)
c_void_p_p = POINTER(c_void_p)


class HTS_Audio(Structure):
    _fields_ = [
        ("sampling_frequency", c_size_t),
        ("max_buff_size", c_size_t),
        ("buff", c_short_p),
        ("buff_size", c_size_t),
        ("audio_interface", c_void_p),
    ]


class HTS_ModelSet(Structure):
    _fields_ = [
        ("hts_voice_version", c_char_p),
        ("sampling_frequency", c_size_t),
        ("frame_period", c_size_t),
        ("num_voices", c_size_t),
        ("num_states", c_size_t),
        ("num_streams", c_size_t),
        ("stream_type", c_char_p),
        ("fullcontext_format", c_char_p),
        ("fullcontext_version", c_char_p),
        ("gv_off_context", c_void_p),  # HTS_Question *
        ("option", c_char_p_p),
        ("duration", c_void_p),  # HTS_Model *
        ("window", c_void_p),  # HTS_Window *
        ("stream", c_void_p_p),  # HTS_Model **
        ("gv", c_void_p_p),  # HTS_Model **
    ]


class HTS_Label(Structure):
    _fields_ = [
        ("head", c_void_p),  # HTS_LabelString *
        ("size", c_size_t),
    ]


HTS_Label_ptr = POINTER(HTS_Label)


class HTS_SStreamSet(Structure):
    _fields_ = [
        ("sstream", c_void_p),  # HTS_SStream *
        ("nstream", c_size_t),
        ("nstate", c_size_t),
        ("duration", c_size_t_p),
        ("total_state", c_size_t),
        ("total_frame", c_size_t),
    ]


class HTS_PStreamSet(Structure):
    _fields_ = [
        ("pstream", c_void_p),  # HTS_PStream *
        ("nstream", c_size_t),
        ("total_frame", c_size_t),
    ]


class HTS_GStream(Structure):
    _fields_ = [
        ("vector_length", c_size_t),
        ("par", c_double_p_p),
    ]


HTS_GStream_ptr = POINTER(HTS_GStream)


class HTS_GStreamSet(Structure):
    _fields_ = [
        ("total_nsample", c_size_t),
        ("total_frame", c_size_t),
        ("nstream", c_size_t),
        ("gstream", HTS_GStream_ptr),
        ("gspeech", c_double_p),
    ]


HTS_GStreamSet_ptr = POINTER(HTS_GStreamSet)


class HTS_Condition(Structure):
    _fields_ = [
        # global
        ("sampling_frequency", c_size_t),
        ("fperiod", c_size_t),
        ("audio_buff_size", c_size_t),
        ("stop", hts_boolean),
        ("volume", c_double),
        ("msd_threshold", c_double_p),
        ("gv_weight", c_double_p),
        # duration
        ("phoneme_alignment_flag", hts_boolean),
        ("speed", c_double),
        # spectrum
        ("stage", c_size_t),
        ("use_log_gain", hts_boolean),
        ("alpha", c_double),
        ("beta", c_double),
        # log F0
        ("additional_half_tone", c_double),
        # interpolation weights
        ("duration_iw", c_double_p),
        ("parameter_iw", c_double_p_p),
        ("gv_iw", c_double_p_p),
    ]


HTS_Condition_ptr = POINTER(HTS_Condition)


class HTS_Engine(Structure):
    _fields_ = [
        ("condition", HTS_Condition),
        ("audio", HTS_Audio),
        ("ms", HTS_ModelSet),
        ("label", HTS_Label),
        ("sss", HTS_SStreamSet),
        ("pss", HTS_PStreamSet),
        ("gss", HTS_GStreamSet),
        # 		("lf0_offset", c_double),
        # 		("lf0_amp", c_double),
    ]


HTS_Engine_ptr = POINTER(HTS_Engine)

############################################


class NJDNode(Structure):
    pass


class NJD(Structure):
    _fields_ = [
        ("head", POINTER(NJDNode)),
        ("tail", POINTER(NJDNode)),
    ]


NJD_ptr = POINTER(NJD)

############################################


class JPCommonNode(Structure):
    pass


JPCommonNode_ptr = POINTER(JPCommonNode)
JPCommonNode._fields_ = [
    ("pron", c_char_p),
    ("pos", c_char_p),
    ("ctype", c_char_p),
    ("cform", c_char_p),
    ("acc", c_int),
    ("chain_flag", c_int),
    ("prev", JPCommonNode_ptr),
    ("next", JPCommonNode_ptr),
]


class JPCommonLabelBreathGroup(Structure):
    pass


JPCommonLabelBreathGroup_ptr = POINTER(JPCommonLabelBreathGroup)


class JPCommonLabelAccentPhrase(Structure):
    pass


JPCommonLabelAccentPhrase_ptr = POINTER(JPCommonLabelAccentPhrase)


class JPCommonLabelWord(Structure):
    pass


JPCommonLabelWord_ptr = POINTER(JPCommonLabelWord)


class JPCommonLabelMora(Structure):
    pass


JPCommonLabelMora_ptr = POINTER(JPCommonLabelMora)


class JPCommonLabelPhoneme(Structure):
    pass


JPCommonLabelPhoneme_ptr = POINTER(JPCommonLabelPhoneme)

# jpcommon/jpcommon.h
class JPCommonLabel(Structure):
    _fields_ = [
        ("size", c_int),
        ("feature", c_char_p_p),
        ("breath_head", JPCommonLabelBreathGroup_ptr),
        ("breath_tail", JPCommonLabelBreathGroup_ptr),
        ("accent_head", JPCommonLabelAccentPhrase_ptr),
        ("accent_tail", JPCommonLabelAccentPhrase_ptr),
        ("word_head", JPCommonLabelWord_ptr),
        ("word_tail", JPCommonLabelWord_ptr),
        ("mora_head", JPCommonLabelMora_ptr),
        ("mora_tail", JPCommonLabelMora_ptr),
        ("phoneme_head", JPCommonLabelPhoneme_ptr),
        ("phoneme_tail", JPCommonLabelPhoneme_ptr),
        ("short_pause_flag", c_int),
    ]


JPCommonLabel_ptr = POINTER(JPCommonLabel)


class JPCommon(Structure):
    _fields_ = [
        ("head", JPCommonNode_ptr),
        ("tail", JPCommonNode_ptr),
        ("label", JPCommonLabel_ptr),
    ]


JPCommon_ptr = POINTER(JPCommon)

#############################################

FNLEN = 1000
FILENAME = c_char * FNLEN
FILENAME_ptr = POINTER(FILENAME)
FILENAME_ptr_ptr = POINTER(FILENAME_ptr)

libjt = None
njd = NJD()
jpcommon = JPCommon()
engine = HTS_Engine()


def libjt_version():
    if libjt is None:
        return "libjt version none"
    return libjt.jt_version()


def libjt_initialize(JT_DLL):
    global libjt, njd, jpcommon, engine

    if libjt is None:
        libjt = cdll.LoadLibrary(JT_DLL)
    libjt.jt_version.restype = c_char_p

    # argtypes & restype

    libjt.NJD_initialize.argtypes = [NJD_ptr]
    libjt.NJD_refresh.argtypes = [NJD_ptr]
    libjt.NJD_clear.argtypes = [NJD_ptr]
    libjt.mecab2njd.argtypes = [NJD_ptr, FEATURE_ptr_array_ptr, c_int]
    libjt.njd_set_pronunciation.argtypes = [NJD_ptr]
    libjt.njd_set_digit.argtypes = [NJD_ptr]
    libjt.njd_set_accent_phrase.argtypes = [NJD_ptr]
    libjt.njd_set_accent_type.argtypes = [NJD_ptr]
    libjt.njd_set_unvoiced_vowel.argtypes = [NJD_ptr]
    libjt.njd_set_long_vowel.argtypes = [NJD_ptr]
    libjt.njd2jpcommon.argtypes = [JPCommon_ptr, NJD_ptr]

    libjt.JPCommon_initialize.argtypes = [JPCommon_ptr]
    libjt.JPCommon_clear.argtypes = [JPCommon_ptr]
    libjt.JPCommon_refresh.argtypes = [JPCommon_ptr]
    libjt.JPCommon_make_label.argtypes = [JPCommon_ptr]
    libjt.JPCommon_get_label_size.argtypes = [JPCommon_ptr]
    libjt.JPCommon_get_label_size.argtypes = [JPCommon_ptr]
    libjt.JPCommon_get_label_feature.argtypes = [JPCommon_ptr]
    libjt.JPCommon_get_label_feature.restype = c_char_p_p
    libjt.JPCommon_get_label_size.argtypes = [JPCommon_ptr]

    libjt.HTS_Engine_initialize.argtypes = [HTS_Engine_ptr]
    libjt.HTS_Engine_load.argtypes = [HTS_Engine_ptr, FILENAME_ptr_ptr, c_int]
    libjt.HTS_Engine_set_sampling_frequency.argtypes = [HTS_Engine_ptr, c_size_t]
    libjt.HTS_Engine_set_fperiod.argtypes = [HTS_Engine_ptr, c_size_t]
    libjt.HTS_Engine_set_audio_buff_size.argtypes = [HTS_Engine_ptr, c_int]
    libjt.HTS_Engine_get_nsamples.argtypes = [HTS_Engine_ptr]
    libjt.HTS_Engine_get_generated_speech.argtypes = [HTS_Engine_ptr, c_int]
    libjt.HTS_Engine_clear.argtypes = [HTS_Engine_ptr]
    libjt.HTS_Engine_refresh.argtypes = [HTS_Engine_ptr]
    libjt.HTS_Engine_synthesize_from_strings_ex.argtypes = [
        HTS_Engine_ptr,
        c_char_p_p,
        c_size_t,
        c_double,
        c_double,
    ]
    libjt.HTS_Engine_synthesize_from_strings_ex.restype = hts_boolean

    libjt.HTS_Engine_set_speed.argtypes = [HTS_Engine_ptr, c_double]
    libjt.HTS_Engine_add_half_tone.argtypes = [HTS_Engine_ptr, c_double]
    libjt.HTS_Engine_set_volume.argtypes = [HTS_Engine_ptr, c_double]

    # MSD threshold
    libjt.HTS_Engine_set_msd_threshold.argtypes = [HTS_Engine_ptr, c_size_t, c_double]
    libjt.HTS_Engine_get_msd_threshold.argtypes = [HTS_Engine_ptr, c_size_t]
    libjt.HTS_Engine_get_msd_threshold.restypes = c_double

    # GV weight
    libjt.HTS_Engine_set_gv_weight.argtypes = [HTS_Engine_ptr, c_size_t, c_double]
    libjt.HTS_Engine_get_gv_weight.argtypes = [HTS_Engine_ptr, c_size_t]
    libjt.HTS_Engine_get_gv_weight.restypes = c_double

    # alpha
    libjt.HTS_Engine_set_alpha.argtypes = [HTS_Engine_ptr, c_double]
    libjt.HTS_Engine_get_alpha.argtypes = [HTS_Engine_ptr]
    libjt.HTS_Engine_get_alpha.restype = c_double

    # beta
    libjt.HTS_Engine_set_beta.argtypes = [HTS_Engine_ptr, c_double]
    libjt.HTS_Engine_get_beta.argtypes = [HTS_Engine_ptr]
    libjt.HTS_Engine_get_beta.restype = c_double

    # interpolation weight for duration
    libjt.HTS_Engine_set_duration_interpolation_weight.argtypes = [
        HTS_Engine_ptr,
        c_size_t,
        c_double,
    ]
    libjt.HTS_Engine_get_duration_interpolation_weight.argtypes = [
        HTS_Engine_ptr,
        c_size_t,
    ]
    libjt.HTS_Engine_get_duration_interpolation_weight.restype = c_double

    # interpolation weight for parameter
    libjt.HTS_Engine_set_parameter_interpolation_weight.argtypes = [
        HTS_Engine_ptr,
        c_size_t,
        c_size_t,
        c_double,
    ]
    libjt.HTS_Engine_get_parameter_interpolation_weight.argtypes = [
        HTS_Engine_ptr,
        c_size_t,
        c_size_t,
    ]
    libjt.HTS_Engine_get_parameter_interpolation_weight.restype = c_double

    # interpolation weight for GV
    libjt.HTS_Engine_set_gv_interpolation_weight.argtypes = [
        HTS_Engine_ptr,
        c_size_t,
        c_size_t,
        c_double,
    ]
    libjt.HTS_Engine_get_gv_interpolation_weight.argtypes = [
        HTS_Engine_ptr,
        c_size_t,
        c_size_t,
    ]
    libjt.HTS_Engine_get_gv_interpolation_weight.restype = c_double

    libjt.jt_speech_prepare.argtypes = [c_double_p, c_size_t, c_short, c_short, c_short]
    libjt.jt_speech_prepare.restype = c_int
    libjt.jt_speech_ptr.argtypes = []
    libjt.jt_speech_ptr.restype = c_short_p
    libjt.jt_save_logs.argtypes = [c_char_p, HTS_Engine_ptr, NJD_ptr]
    libjt.jt_save_riff.argtypes = [c_char_p, HTS_Engine_ptr]

    # initialize

    libjt.NJD_initialize(njd)
    libjt.JPCommon_initialize(jpcommon)
    libjt.HTS_Engine_initialize(engine)


def libjt_load(VOICE):
    global libjt, engine
    fn_buf = create_string_buffer(VOICE.encode("mbcs"))
    fn_buf_ptr = cast(byref(fn_buf), FILENAME_ptr)
    fn_buf_ptr_ptr = cast(byref(fn_buf_ptr), FILENAME_ptr_ptr)
    libjt.HTS_Engine_load(engine, fn_buf_ptr_ptr, 1)


def libjt_refresh():
    libjt.HTS_Engine_refresh(engine)
    libjt.JPCommon_refresh(jpcommon)
    libjt.NJD_refresh(njd)


def libjt_clear():
    libjt.NJD_clear(njd)
    libjt.JPCommon_clear(jpcommon)
    libjt.HTS_Engine_clear(engine)


libjt_on_done = None


def libjt_set_on_done(func):
    global libjt_on_done
    libjt_on_done = func


def libjt_synthesis(
    feature,
    size,
    fperiod_=80,
    feed_func_=None,
    is_speaking_func_=None,
    begin_thres_=32,
    end_thres_=32,
    level_=32767,
    logwrite_=None,
    lf0_offset_=0.0,
    lf0_amp_=1.0,
    jtlogfile_=None,
    jtwavfile_=None,
):
    if feature is None or size is None:
        return None
    if logwrite_:
        logwrite_("libjt_synthesis start.")
    libjt.HTS_Engine_set_fperiod(engine, fperiod_)
    libjt.mecab2njd(njd, feature, size)
    libjt.njd_set_pronunciation(njd)
    libjt.njd_set_digit(njd)
    libjt.njd_set_accent_phrase(njd)
    libjt.njd_set_accent_type(njd)
    libjt.njd_set_unvoiced_vowel(njd)
    libjt.njd_set_long_vowel(njd)
    libjt.njd2jpcommon(jpcommon, njd)
    libjt.JPCommon_make_label(jpcommon)
    if is_speaking_func_ and not is_speaking_func_():
        libjt_refresh()
        return None
    s = libjt.JPCommon_get_label_size(jpcommon)
    buf = None
    if s > 2:
        f = libjt.JPCommon_get_label_feature(jpcommon)
        ret = libjt.HTS_Engine_synthesize_from_strings_ex(
            engine, f, s, lf0_offset_, lf0_amp_
        )
        if ord(ret) == 0:
            libjt_refresh()
            return None
        if jtlogfile_:
            libjt.jt_save_logs(jtlogfile_, engine, njd)
        if jtwavfile_:
            libjt.jt_save_riff(jtwavfile_, engine)
        if is_speaking_func_ and not is_speaking_func_():
            libjt_refresh()
            return None
        gsp = engine.gss.gspeech
        gtn = engine.gss.total_nsample
        ns = libjt.jt_speech_prepare(gsp, gtn, begin_thres_, end_thres_, level_)
        speech_ptr = libjt.jt_speech_ptr()
        byte_count = ns * sizeof(c_short)
        buf = string_at(speech_ptr, byte_count)
        if feed_func_:
            try:
                feed_func_(buf)
            except (WindowsError, RuntimeError):
                pass
        if libjt_on_done:
            libjt_on_done()
    if logwrite_:
        logwrite_("libjt_synthesis done.")
    return buf


def libjt_set_alpha(d):
    global libjt, engine
    libjt.HTS_Engine_set_alpha(engine, d)


def libjt_get_alpha():
    global libjt, engine
    return libjt.HTS_Engine_get_alpha(engine)


def libjt_set_beta(d):
    global libjt, engine
    libjt.HTS_Engine_set_beta(engine, d)


def libjt_get_beta():
    global libjt, engine
    return libjt.HTS_Engine_get_beta(engine)


def libjt_set_gv_interpolation_weight(a, b, d):
    global libjt, engine
    libjt.HTS_Engine_set_gv_interpolation_weight(engine, a, b, d)


def libjt_get_gv_interpolation_weight(a, b):
    global libjt, engine
    return libjt.HTS_Engine_get_gv_interpolation_weight(engine, a, b)
