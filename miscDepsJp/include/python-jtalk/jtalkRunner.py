# jtalkRunner.py
# -*- coding: utf-8 -*-
# Japanese speech engine test module
# by Takuya Nishimoto
# http://ja.nishimotz.com/project:libopenjtalk
# Usage:
# > python jtalkRunner.py
# requires pyaudio (PortAudio wrapper)
# http://people.csail.mit.edu/hubert/pyaudio/

import os
import sys
import time
import wave
from pathlib import Path

try:
    import pyaudio
except Exception:
    pyaudio = None  # type: ignore
# import cProfile
# import pstats
# Calculate repo root (miscDepsJp's parent) and use miscDepsJp/source/synthDrivers/jtalk
# Long-term approach: Use REPO_ROOT environment variable to avoid depending on miscDepsJp folder structure
repo_root = os.environ.get('REPO_ROOT')
if repo_root:
    repo_root_path = Path(repo_root)
    if repo_root_path.is_dir():
        repo_root_path = repo_root_path.resolve()
        # Verify repo_root contains miscDepsJp (sanity check)
        if not (repo_root_path / "miscDepsJp").exists():
            repo_root = None
        else:
            repo_root = str(repo_root_path)
    else:
        repo_root = None
else:
    repo_root = None

# Fallback 1: Try to get repo root from PYTHONPATH environment variable
if repo_root is None:
    pythonpath = os.environ.get('PYTHONPATH', '')
    if pythonpath:
        for path_str in pythonpath.split(os.pathsep):
            if path_str:
                path = Path(path_str)
                if path.is_dir():
                    # Check if this path contains miscDepsJp/include/python-jtalk
                    if path_str.endswith("miscDepsJp/include/python-jtalk") or path_str.endswith("miscDepsJp\\include\\python-jtalk"):
                        # Go up two levels: miscDepsJp/include/python-jtalk -> miscDepsJp -> repo root
                        candidate = path.parent.parent
                        if (candidate / "miscDepsJp").exists():
                            repo_root = str(candidate.parent)
                            break

# Fallback 2: Use __file__-based calculation (depends on miscDepsJp folder structure)
if repo_root is None:
    script_dir = Path(__file__).resolve().parent
    # script_dir -> miscDepsJp/include/python-jtalk
    # ../.. -> miscDepsJp
    # ../.. -> repo root
    repo_root_path = (script_dir / ".." / ".." / "..").resolve()
    if (repo_root_path / "miscDepsJp").exists():
        repo_root = str(repo_root_path)
    else:
        repo_root = None

if repo_root is None:
    raise RuntimeError("Could not determine repo root")

repo_root_path = Path(repo_root)
jtalk_dir = JT_DIR = repo_root_path / "source" / "synthDrivers" / "jtalk"
JT_DIR_str = str(JT_DIR)
# Use source/synthDrivers/jtalk directly (files moved from miscDepsJp in Phase 1)
# Remove any existing occurrence to ensure correct import path
if JT_DIR_str in sys.path:
    sys.path.remove(JT_DIR_str)
sys.path.insert(0, JT_DIR_str)
import jtalkPrepare  # type: ignore
from jtalkCore import *  # type: ignore
from mecab import (  # type: ignore
    Mecab_initialize,
    Mecab_analysis,
    Mecab_print,
    Mecab_correctFeatures,
    Mecab_utf8_to_cp932,
    MecabFeatures,
)
from text2mecab import text2mecab  # type: ignore

JT_DLL = (JT_DIR / "libopenjtalk.dll").resolve()
# Ensure DLL directory is in search path
if hasattr(os, "add_dll_directory"):
    try:
        os.add_dll_directory(JT_DIR_str)
    except OSError:
        pass  # Ignore if already added or fails

voices = [
    {
        "id": "V1",
        "name": "m001",
        "lang": "ja",
        "samp_rate": 48000,
        "fperiod": 240,
        "lf0_base": 5.0,
        "pitch_bias": 0,
        "speaker_attenuation": 1.0,
        "htsvoice": str(jtalk_dir / "m001" / "m001.htsvoice"),
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
        "htsvoice": str(jtalk_dir / "mei" / "mei_happy.htsvoice"),
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
        "htsvoice": str(jtalk_dir / "lite" / "voice.htsvoice"),
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
        "lf0_base": 5.9,
        "pitch_bias": 0,
        "inflection_bias": 0,
        "speaker_attenuation": 0.8,
        "htsvoice": str(jtalk_dir / "tohokuf01" / "tohoku-f01-neutral.htsvoice"),
        "alpha": 0.54,
        "beta": 0.00,
        "espeak_variant": "f1",
    },
]


def pa_play(data, samp_rate=16000):
    if pyaudio is None:
        return
    p = pyaudio.PyAudio()
    stream = p.open(
        format=p.get_format_from_width(2), channels=1, rate=samp_rate, output=True,
    )
    size = len(data)
    pos = 0  # byte count
    while pos < size:
        a = stream.get_write_available() * 2
        o = data[pos : pos + a]
        stream.write(o)
        pos += a
    time.sleep(float(size) / 2 / samp_rate)
    stream.close()
    p.terminate()


do_print = False


def __print(s):
    # Write to mecab_debug.log file only (not to console)
    # This ensures MeCab logs are only stored in logfile, not printed to console
    try:
        # Calculate path to mecab_debug.log relative to repo root
        if repo_root:
            debug_log_path = Path(repo_root) / "source" / "synthDrivers" / "jtalk" / "mecab_debug.log"
        else:
            # Fallback: use current directory
            debug_log_path = Path("source") / "synthDrivers" / "jtalk" / "mecab_debug.log"
        debug_log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(debug_log_path, "a", encoding="utf-8", errors="replace") as f:
            f.write(str(s) + "\n")
            f.flush()
    except Exception:
        # Logging is best-effort only. Failures must not interfere with normal operation.
        pass
    # Note: do_print flag is kept for backward compatibility, but MeCab logs are always written to file
    if do_print:
        print(s.encode("cp932", "ignore"))


def print_code(msg):
    s = ""
    for c in msg:
        s += "%04x " % ord(c)
    print(s)


count = 0


def do_synthesis(
    msg, voice_args, do_play, do_write, do_log, fperiod, pitch=50, inflection=50, vol=50,
):
    global count
    msg = jtalkPrepare.convert(msg)
    s = text2mecab(msg)
    __print("utf-8: (%s)" % s.decode("utf-8", "ignore"))
    mf = MecabFeatures()
    Mecab_analysis(s, mf)
    Mecab_print(mf, __print)
    Mecab_correctFeatures(mf)
    ar = [mf]  # ar = Mecab_splitFeatures(mf)
    __print("array size %d" % len(ar))
    max_level = int(326.67 * int(vol) + 100)  # 100..32767
    level = int(max_level * voice_args["speaker_attenuation"])
    lf0_amp = 0.020 * inflection  # 50 = original range
    ls = 0.015 * (pitch - 50.0 + voice_args["pitch_bias"])  # 50 = no shift
    lf0_offset = ls + voice_args["lf0_base"] * (1 - lf0_amp)
    for a in ar:
        count += 1
        __print("feature size %d" % a.size)
        Mecab_print(a, __print)
        Mecab_utf8_to_cp932(a)
        if do_write:
            w = "_test%d.jt.wav" % count
        else:
            w = None
        if do_log:
            l = "_test%d.jtlog" % count
        else:
            l = None
        data = libjt_synthesis(
            a.feature,
            a.size,
            begin_thres_=32,
            end_thres_=32,
            level_=level,
            fperiod_=fperiod,
            lf0_offset_=lf0_offset,
            lf0_amp_=lf0_amp,
            logwrite_=__print,
            jtlogfile_=l,
            jtwavfile_=w,
        )
        if data:
            __print("data size %d" % len(data))
            if do_play:
                pa_play(data, samp_rate=voice_args["samp_rate"])
            if do_write:
                w = wave.Wave_write("_test%d.wav" % count)
                w.setparams(
                    (
                        1,
                        2,
                        voice_args["samp_rate"],
                        len(data) / 2,
                        "NONE",
                        "not compressed",
                    ),
                )
                w.writeframes(data)
                w.close()
        libjt_refresh()
        del a
    del mf


def main(do_play=False, do_write=True, do_log=False):
    njd = NJD()
    jpcommon = JPCommon()
    engine = HTS_Engine()
    libjt_initialize(JT_DLL)
    v = voices[3]
    libjt_load(v["htsvoice"])
    libjt_set_alpha(v["alpha"])
    libjt_set_beta(v["beta"])
    print("alpha:%f beta:%f" % (libjt_get_alpha(), libjt_get_beta()))
    # print('GV-weight 0-0:%f' % (libjt_get_gv_interpolation_weight(0, 0),))
    # libjt_set_beta(0.40)
    # libjt_set_gv_interpolation_weight(0, 0, 2)
    # libjt_set_gv_interpolation_weight(0, 1, 2)
    Mecab_initialize(__print, JT_DIR_str, str(JT_DIR / "dic"))

    msgs = [
        "welcome to nvda",
        "テンキーのinsertキーとメインのinsertキーの両方がnvdaキーとして動作します。",
    ]
    fperiod = v["fperiod"]
    for s in msgs:
        do_synthesis(s, v, do_play, do_write, do_log, fperiod, pitch=50, inflection=50)
    return 0


if __name__ == "__main__":
    do_print = True
    main(do_play=False, do_write=True)
    # prof = cProfile.run("main(do_play=True)", '_cprof.prof')
    # p = pstats.Stats('_cprof.prof')
    # p.strip_dirs()
    # p.sort_stats('time', 'calls')
    # p.print_stats()
