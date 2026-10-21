# arpabet_to_kana.py
# Copyright (C) 2010-2026 Takuya Nishimoto
# License: BSD 3-Clause. See LICENSE.
#
# Rule-based conversion from CMUdict's ARPAbet phoneme transcriptions to
# katakana, following common English-loanword adaptation conventions.
# Used by eng_dic_maker.py to generate nvdajp-eng-dic.csv from
# eng-dic-source/cmudict-subset.dict, replacing the GPL-licensed
# bep-eng.dic that nvdajp itself uses (see eng-dic-source/README.md).
#
# This is a coarse approximation, not a full English-to-Japanese
# transliteration engine: it gets common IT vocabulary (e.g. "alt",
# "windows", "point") right, but historically-lexicalized loanwords
# whose conventional katakana does not track modern General American
# pronunciation (e.g. "character" -> traditionally "kyarakutaa", not
# derived from the CMUdict pronunciation) will differ from the
# established spelling. Such cases are handled as individual overrides
# in custom_dic_maker.py, not by further generalizing this module.

import re

VOWELS = {
    "AA": "ア", "AE": "ア", "AH": "ア", "AO": "オ",
    "EH": "エ", "IH": "イ", "IY": "イー", "UH": "ウ", "UW": "ウー",
    "ER": "アー",
    # diphthongs
    "AW": "アウ", "AY": "アイ", "EY": "エイ", "OW": "オウ", "OY": "オイ",
}

# Diphthong -> (vowel-key for combining with a preceding consonant, trailing mora).
# e.g. "shout" (SH AW1 T) -> consonant SH + "a" -> "シャ", then trailing "ウ" -> "シャウト".
DIPHTHONG_PARTS = {
    "AW": ("a", "ウ"), "AY": ("a", "イ"), "EY": ("e", "イ"),
    "OW": ("o", "ウ"), "OY": ("o", "イ"),
}

# consonant -> {a,i,u,e,o: combined kana, coda: kana when no following vowel}
CONSONANTS = {
    "P": {"a": "パ", "i": "ピ", "u": "プ", "e": "ペ", "o": "ポ", "coda": "プ"},
    "B": {"a": "バ", "i": "ビ", "u": "ブ", "e": "ベ", "o": "ボ", "coda": "ブ"},
    "T": {"a": "タ", "i": "ティ", "u": "トゥ", "e": "テ", "o": "ト", "coda": "ト"},
    "D": {"a": "ダ", "i": "ディ", "u": "ドゥ", "e": "デ", "o": "ド", "coda": "ド"},
    "K": {"a": "カ", "i": "キ", "u": "ク", "e": "ケ", "o": "コ", "coda": "ク"},
    "G": {"a": "ガ", "i": "ギ", "u": "グ", "e": "ゲ", "o": "ゴ", "coda": "グ"},
    "CH": {"a": "チャ", "i": "チ", "u": "チュ", "e": "チェ", "o": "チョ", "coda": "チ"},
    "JH": {"a": "ジャ", "i": "ジ", "u": "ジュ", "e": "ジェ", "o": "ジョ", "coda": "ジ"},
    "F": {"a": "ファ", "i": "フィ", "u": "フ", "e": "フェ", "o": "フォ", "coda": "フ"},
    "V": {"a": "ヴァ", "i": "ヴィ", "u": "ヴ", "e": "ヴェ", "o": "ヴォ", "coda": "ヴ"},
    "TH": {"a": "サ", "i": "シ", "u": "ス", "e": "セ", "o": "ソ", "coda": "ス"},
    "DH": {"a": "ザ", "i": "ジ", "u": "ズ", "e": "ゼ", "o": "ゾ", "coda": "ズ"},
    "S": {"a": "サ", "i": "シ", "u": "ス", "e": "セ", "o": "ソ", "coda": "ス"},
    "Z": {"a": "ザ", "i": "ジ", "u": "ズ", "e": "ゼ", "o": "ゾ", "coda": "ズ"},
    "SH": {"a": "シャ", "i": "シ", "u": "シュ", "e": "シェ", "o": "ショ", "coda": "シュ"},
    "ZH": {"a": "ジャ", "i": "ジ", "u": "ジュ", "e": "ジェ", "o": "ジョ", "coda": "ジュ"},
    "HH": {"a": "ハ", "i": "ヒ", "u": "フ", "e": "ヘ", "o": "ホ", "coda": "フ"},
    "M": {"a": "マ", "i": "ミ", "u": "ム", "e": "メ", "o": "モ", "coda": "ム"},
    "N": {"a": "ナ", "i": "ニ", "u": "ヌ", "e": "ネ", "o": "ノ", "coda": "ン"},
    "NG": {"a": "ンガ", "i": "ンギ", "u": "ング", "e": "ンゲ", "o": "ンゴ", "coda": "ング"},
    "L": {"a": "ラ", "i": "リ", "u": "ル", "e": "レ", "o": "ロ", "coda": "ル"},
    "R": {"a": "ラ", "i": "リ", "u": "ル", "e": "レ", "o": "ロ", "coda": ""},  # coda R: see below
    "W": {"a": "ワ", "i": "ウィ", "u": "ウ", "e": "ウェ", "o": "ウォ", "coda": "ウ"},
    "Y": {"a": "ヤ", "i": "イ", "u": "ユー", "e": "イェ", "o": "ヨ", "coda": "イ"},
}

_VOWEL_KEYS = {"AA": "a", "AE": "a", "AH": "a", "AO": "o", "EH": "e", "IH": "i", "IY": "i", "UH": "u", "UW": "u"}
_CMU_VOWEL_BASES = {
    "AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY", "IH", "IY", "OW", "OY", "UH", "UW",
}


def _strip_stress(phoneme):
    if phoneme and phoneme[-1].isdigit():
        return phoneme[:-1], phoneme[-1]
    return phoneme, None


_SMALL_KANA = set("ゃゅょぁぃぅぇぉャュョァィゥェォ")


def _split_morae(s):
    """Split a kana string into mora units, attaching small kana to the
    preceding character (standard Japanese mora-counting convention)."""
    morae = []
    for ch in s:
        if ch in _SMALL_KANA and morae:
            morae[-1] += ch
        else:
            morae.append(ch)
    return morae


def _find_spelled_vowels_for_aa(word, phonemes):
    """Align AA phonemes with spelled vowel clusters in word to detect 'o'."""
    if not word:
        return set()
    spelled_vowels = re.findall(r"[aeiouy]+", word.lower())
    cmu_vowels = []
    for idx, p in enumerate(phonemes):
        base, _ = _strip_stress(p)
        if base in _CMU_VOWEL_BASES:
            cmu_vowels.append((idx, base))

    aa_is_o = set()
    n_s = len(spelled_vowels)
    n_c = len(cmu_vowels)
    for v_i, (p_idx, base) in enumerate(cmu_vowels):
        if base == "AA":
            if n_s == n_c:
                s_v = spelled_vowels[v_i]
            else:
                s_i = int(round(v_i * n_s / max(1, n_c)))
                s_i = min(s_i, n_s - 1)
                s_v = spelled_vowels[s_i] if spelled_vowels else ""
            if "o" in s_v:
                aa_is_o.add(p_idx)
    return aa_is_o


def _morae_with_stress(phonemes, word=""):
    """Return a list of (mora_str, stress_or_None) pairs.

    stress is the ARPAbet stress digit ('0'/'1'/'2') of the vowel that
    produced the mora, assigned to the first mora of a multi-mora
    segment (long vowel, diphthong, or nasal-initial combo like NG).
    """
    stressed = [_strip_stress(p) for p in phonemes]
    bases = [b for b, _ in stressed]
    stresses = [s for _, s in stressed]
    aa_is_o_indices = _find_spelled_vowels_for_aa(word, phonemes)
    result = []
    i = 0
    n = len(bases)
    while i < n:
        ph = bases[i]
        # ER + IY0 after a vowel-ending mora: "アリー" contraction.
        # This must be checked BEFORE the vowel-lengthening ER rule below,
        # so that diary (AY1-ER0-IY0) -> "ダイ" + "アリー" instead of
        # "ダイーイー".  When ER is followed by IY0 (both unstressed, or
        # ER stressed + IY0 unstressed), the two vowels collapse to
        # "アリー" (matching ダイアリー, ファイアリー, バウアリー).
        # Also handles ER1+IY0 after vowel: hurry (HH-ER1-IY0) -> "ハ" + "リー".
        if (
            ph == "ER"
            and i + 1 < n
            and bases[i + 1] == "IY"
            and stresses[i + 1] == "0"
            and result
            and result[-1][0][-1] in "アイウエオ"
        ):
            result.append(("ア", None))
            result.append(("リー", stresses[i + 1]))
            i += 2
            continue
        if ph == "ER" and result and result[-1][0][-1] in "アイウエオー":
            # rhotic schwa directly after a vowel-ending mora (no
            # intervening consonant) is a lengthening, not a new
            # "ア" mora (e.g. "power" P-AW-ER: after the "ウ" from AW,
            # ER just lengthens to "パウー" instead of "パウアー").
            result.append(("ー", stresses[i]))
            i += 1
            continue
        if ph in VOWELS:
            # When ARPAbet AA (/ɑ/) is spelled with "o" in English orthography,
            # adapt to オ-row rather than ア-row (Phase 3).
            if ph == "AA" and i in aa_is_o_indices:
                kana = "オ"
            else:
                kana = VOWELS[ph]
            # Unstressed rhotic schwa (ER0) at word start is realized as
            # "ア" (one mora), not "アー" (two morae), matching established
            # loanword spellings: arena -> アリーナ, arise -> アライズ.
            if ph == "ER" and stresses[i] == "0" and not result:
                kana = "ア"
            morae = _split_morae(kana)
            for j, m in enumerate(morae):
                result.append((m, stresses[i] if j == 0 else None))
            i += 1
            continue
        if ph in CONSONANTS:
            nxt = bases[i + 1] if i + 1 < n else None
            # Sibilant + unstressed AH0 + Z (word-final or pre-boundary plurals:
            # offices, services, devices, places, pages, choices, sizes).
            # Plural "-es" after sibilants is /ɪz/ or /əz/ (AH0 Z in CMUdict).
            # Japanese loanwords adapt this as "シズ"/"ジズ"/"チズ", not "-サズ"/"-ジャズ".
            if (
                ph in ("S", "Z", "SH", "CH", "JH")
                and i + 2 < n
                and bases[i + 1] == "AH"
                and stresses[i + 1] == "0"
                and bases[i + 2] == "Z"
                and (i + 3 == n or bases[i + 3] not in _VOWEL_KEYS)
            ):
                i_row = {"S": "シ", "Z": "ジ", "SH": "シ", "CH": "チ", "JH": "ジ"}[ph]
                result.append((i_row, None))
                result.append(("ズ", None))
                i += 3
                continue
            # Suffix -tion / -sion (SH/ZH + AH0 + N) -> ション / ジョン:
            # English "-tion" / "-sion" (/ʃən/, /ʒən/) is adapted in Japanese
            # loanwords as ション / ジョン (option, action, section, function, version),
            # not coda + consonant (avoiding "-シュン"/"-ジュン").
            if (
                ph in ("SH", "ZH")
                and i + 2 < n
                and bases[i + 1] == "AH"
                and stresses[i + 1] == "0"
                and bases[i + 2] == "N"
                and (i + 3 == n or bases[i + 3] not in _VOWEL_KEYS)
            ):
                suffix = "ション" if ph == "SH" else "ジョン"
                result.append((suffix, None))
                i += 3
                continue
            # ER + IY0 contraction: when a rhotic schwa (stressed or
            # unstressed) is immediately followed by an unstressed /i/
            # (IY0), the two vowels collapse to a single "リー" mora,
            # matching established loanword spellings:
            #   gallery  /ˈɡæləri/  L-ER0-IY0 -> "ル" + "リー" (ガラリー)
            #   hurry    /ˈhʌri/    H-ER1-IY0 -> "ハ" + "リー" (ハリー)
            #   luxury   /ˈlʌkʃəri/ ZH-ER0-IY0 -> "ジュ" + "リー" (ラグジャリー)
            #   priory   /ˈpraɪəri/ R-AY1-ER0-IY0 -> R coda, "アリー" (プライアリー)
            # This must run BEFORE the generic consonant+ER rule, so that
            # C-ER-IY0 does not get consumed by C-ER -> "Cー" leaving IY0
            # as a bare "イー".
            if (
                nxt == "ER"
                and ph != "R"
                and i + 2 < n
                and bases[i + 2] == "IY"
                and stresses[i + 2] == "0"
            ):
                # If the previous mora ends in a vowel, this consonant is
                # the onset of the ER syllable -> combine C+ER, then "リー".
                # If the previous mora is a consonant coda (or no previous
                # mora) AND ER is unstressed (ER0), the consonant is a
                # coda and ER0+IY0 -> "リー".
                # But if ER is STRESSED (ER1), the consonant is always the
                # onset -> combine C+ER regardless (hurry HH-ER1-IY0 -> "ハリー").
                if (result and result[-1][0] and result[-1][0][-1] in "アイウエオ") or stresses[i + 1] != "0":
                    # consonant is onset of ER syllable
                    result.append((CONSONANTS[ph]["a"], stresses[i + 1]))
                    result.append(("リー", stresses[i + 2]))
                else:
                    # consonant coda + ER0 + IY0 -> "リー"
                    result.append((CONSONANTS[ph]["coda"], None))
                    result.append(("リー", stresses[i + 2]))
                i += 3
                continue
            # consonant + ER ("er/ar" rhotic vowel): combine as
            # consonant+a, then lengthen (e.g. "current" K-ER -> "カー",
            # not "ク" + bare "アー").
            if nxt == "ER" and ph != "R":
                result.append((CONSONANTS[ph]["a"], stresses[i + 1]))
                result.append(("ー", None))
                i += 2
                continue
            # T/D immediately followed by S/Z (adjacent, no vowel between)
            # is the English "-ts"/"-dz" affricate ending (lights, results,
            # insights, words...): a single "ツ"/"ズ" mora, not two separate
            # codas (avoids "insights" -> インサイトス instead of インサイツ).
            if ph == "T" and nxt == "S":
                result.append(("ツ", None))
                i += 2
                continue
            if ph == "D" and nxt == "Z":
                result.append(("ズ", None))
                i += 2
                continue
            # Velar nasal NG immediately followed by K is realized as "ンク"
            # (not "ング" + "ク") when K begins a new syllable marker, e.g.
            # "functions" -> ファンクションズ.  When K is followed by a vowel
            # (ING endings), it forms the syllable onset instead: "thinking"
            # /ˈθɪŋkɪŋ/ -> シンキング, "banking" /ˈbæŋkɪŋ/ -> バンキング.
            if ph == "NG" and nxt == "K":
                if i + 2 < n and bases[i + 2] in _VOWEL_KEYS:
                    result.append(("ン", None))
                    vowel = bases[i + 2]
                    kana = CONSONANTS["K"][_VOWEL_KEYS[vowel]]
                    morae = _split_morae(kana)
                    for j, m in enumerate(morae):
                        result.append((m, stresses[i + 2] if j == len(morae) - 1 else None))
                    # K + IY/UW are long vowels; lengthen the combined mora.
                    if vowel in ("IY", "UW"):
                        result.append(("ー", None))
                    i += 3
                    continue
                result.append(("ンク", None))
                i += 2
                continue
            # N/M + Y + UW/IY: palatalized consonant cluster (/nj/ -> ニュ,
            # /mj/ -> ミュ).  In English, N-Y-UW forms a /nj/ sound (as in
            # "monument" /ˈmɑnjumənt/, "new" /njuː/) which maps to ニュ in
            # Japanese loanwords, not "ン" + "ユー".  Similarly M-Y-UW
            # (as in "communicate" /kəˈmjuːnɪkeɪt/) maps to ミュ.
            # This must run BEFORE the consonant+IY/UW rule below.
            if (
                ph in ("N", "M")
                and nxt == "Y"
                and i + 2 < n
                and bases[i + 2] in ("UW", "IY")
            ):
                # Combine as palatal: N+Y+UW -> "ニュ"(+"ー" if UW/IY),
                # M+Y+UW -> "ミュ"(+"ー" if UW/IY)
                pal = {"N": "ニュ", "M": "ミュ"}[ph]
                result.append((pal, stresses[i + 2]))
                if bases[i + 2] in ("UW", "IY"):
                    result.append(("ー", None))
                i += 3
                continue
            # N/M + UW/IY (without explicit Y): in some CMUdict entries,
            # the /j/ is implicit (e.g. "new" = N UW1, not N Y UW1).
            # Map to ニュー/ニー or ミュー/ミー to match established
            # loanword spellings (new -> ニュー, music -> ミュージック).
            if (
                ph in ("N", "M")
                and nxt in ("UW", "IY")
                and not result
            ):
                pal = {"N": {"UW": "ニュー", "IY": "ニー"},
                        "M": {"UW": "ミュー", "IY": "ミー"}}[ph][nxt]
                result.append((pal, stresses[i + 1]))
                i += 2
                continue
            # Consonant + Y + UW/IY/UH: palatalized consonant cluster.
            # F+Y+UW -> "フュー" (fume, future, fusion, confuse),
            # B+Y+UW -> "ビュー" (beauty), V+Y+UW -> "ヴュー" (view),
            # P+Y+UH -> "ピュア" (pure), HH+Y+UW -> "ヒュー" (human),
            # K+Y+UH -> "キュア" (cure), G+Y+UW -> "ギュー" (argue),
            # T+Y+UW -> "チュー" (tune), D+Y+UW -> "ジュー" (duty).
            # This must run BEFORE the consonant+IY/UW rule below.
            if (
                ph == "F"
                and nxt == "Y"
                and i + 2 < n
                and bases[i + 2] in ("UW", "IY", "UH")
            ):
                result.append(("フュ", stresses[i + 2]))
                if bases[i + 2] in ("UW", "IY"):
                    result.append(("ー", None))
                i += 3
                continue
            if (
                ph in ("P", "B", "V", "HH", "K", "G")
                and nxt == "Y"
                and i + 2 < n
                and bases[i + 2] in ("UW", "IY", "UH")
            ):
                pal = CONSONANTS[ph]["i"] + "ュ"
                result.append((pal, stresses[i + 2]))
                if bases[i + 2] in ("UW", "IY"):
                    result.append(("ー", None))
                i += 3
                continue
            if (
                ph in ("T", "D")
                and nxt == "Y"
                and i + 2 < n
                and bases[i + 2] in ("UW", "IY", "UH")
            ):
                cons = "CH" if ph == "T" else "JH"
                vkey = {"UW": "u", "IY": "i", "UH": "u"}[bases[i + 2]]
                result.append((CONSONANTS[cons][vkey], stresses[i + 2]))
                if bases[i + 2] in ("UW", "IY"):
                    result.append(("ー", None))
                i += 3
                continue
            # R + AH0 + L/D: preserve the R as a ラ行 kana instead of
            # letting the schwa-sonorant rule swallow it (e.g. "herald"
            # HH-EH1-R-AH0-L-D -> "ヘラルド", not "ヘルド").  The R here
            # is an onset consonant, not a coda; the schwa between R and
            # the following sonorant is just the vowel of R's syllable.
            if (
                ph == "R"
                and nxt == "AH"
                and i + 1 < n
                and stresses[i + 1] == "0"
                and i + 2 < n
                and bases[i + 2] in ("L", "D", "N")
            ):
                result.append((CONSONANTS["R"]["a"], None))
                # Skip the schwa; the following consonant is handled next loop
                i += 2
                continue
            # consonant + IY/UW: these are inherently long vowels (unlike
            # IH/UH, which share the same combining key "i"/"u"), so the
            # combined mora must also lengthen (e.g. "reader" R-IY-D-ER ->
            # "リーダー", not "リダー").
            if nxt in ("IY", "UW"):
                result.append((CONSONANTS[ph][_VOWEL_KEYS[nxt]], stresses[i + 1]))
                result.append(("ー", None))
                i += 2
                continue
            if (
                ph == "R"
                and result
                and nxt not in _VOWEL_KEYS
                and nxt not in DIPHTHONG_PARTS
            ):
                # true coda /r/ (nothing vowel-like follows): lengthen.
                result.append(("ー", None))
                i += 1
                continue
            if nxt in DIPHTHONG_PARTS:
                vowel_key, trailing = DIPHTHONG_PARTS[nxt]
                combo = _split_morae(CONSONANTS[ph][vowel_key])
                for j, m in enumerate(combo):
                    result.append((m, None))
                result.append((trailing, stresses[i + 1]))
                i += 2
                continue
            # AH0 + M + Y + UW: when schwa-M is followed by Y+UW (as in
            # "communicate" K-AH0-M-Y-UW1-...), the M is the onset of the
            # /mjuː/ syllable, not a coda.  Combine as "ミュ"+"ー" instead
            # of "ム" + "ユー".  This must run BEFORE the schwa-sonorant
            # rule and the consonant+IY/UW rule.
            if (
                nxt == "AH"
                and i + 1 < n
                and stresses[i + 1] == "0"
                and i + 2 < n
                and bases[i + 2] == "M"
                and i + 3 < n
                and bases[i + 3] == "Y"
                and i + 4 < n
                and bases[i + 4] in ("UW", "IY")
            ):
                result.append((CONSONANTS[ph]["coda"], None))
                result.append(("ミュ", stresses[i + 4]))
                if bases[i + 4] in ("UW", "IY"):
                    result.append(("ー", None))
                i += 5
                continue
            # consonant + unstressed AH + L (schwa + dark L) maps to the
            # consonant's e-row kana + "ル" for a few frequent sonorants,
            # matching established loanword spellings:
            #   cancel /ˈkænsəl/ -> キャンセル
            #   camel  /ˈkæməl/  -> キャメル
            #   channel /ˈtʃænəl/ -> チャンネル
            # This must run before the generic syllabic-sonorant rule below.
            if (
                nxt == "AH"
                and i + 1 < n
                and stresses[i + 1] == "0"
                and i + 2 < n
                and bases[i + 2] == "L"
                and ph in ("S", "M", "N")
                and (i + 3 == n or bases[i + 3] not in _VOWEL_KEYS)
            ):
                e_row = {"S": "セ", "M": "メ", "N": "ネ"}[ph]
                result.append((e_row, None))
                result.append(("ル", None))
                i += 3
                continue
            # unstressed schwa immediately before a word-final (or
            # pre-consonant) sonorant is realized in English as a
            # syllabic consonant (e.g. "open" /oʊpn̩/): drop the schwa
            # mora and let the consonant surface on its own, instead of
            # combining consonant+schwa into a spurious extra mora
            # (avoids "open" -> オウパン, produces オウプン instead).
            #
            # Exception: when the current consonant and the following
            # sonorant are the same (N+AH+N, M+AH+M), dropping the schwa
            # produces consecutive ンン which is unnatural in Japanese
            # (e.g. "cannon" -> カンン instead of カナン).  In that case
            # let the normal consonant+vowel combination apply.
            if (
                nxt == "AH"
                and i + 1 < n
                and stresses[i + 1] == "0"
                and i + 2 < n
                and bases[i + 2] in ("N", "M", "L")
                and (i + 3 == n or bases[i + 3] not in _VOWEL_KEYS)
                and not (ph in ("N", "M") and bases[i + 2] == ph)
            ):
                result.append((CONSONANTS[ph]["coda"], None))
                i += 2  # skip this consonant and the schwa; sonorant handled next loop
                continue
            if nxt in _VOWEL_KEYS:
                # When ARPAbet AA (/ɑ/) is spelled with "o" in English orthography,
                # adapt to オ-row rather than ア-row (Phase 3).
                if nxt == "AA" and (i + 1) in aa_is_o_indices:
                    vkey = "o"
                else:
                    vkey = _VOWEL_KEYS[nxt]
                kana = CONSONANTS[ph][vkey]
                morae = _split_morae(kana)
                # the vowel's stress belongs to the last mora of the combo
                # (e.g. NG "ン" + "ガ": stress belongs to "ガ")
                for j, m in enumerate(morae):
                    result.append((m, stresses[i + 1] if j == len(morae) - 1 else None))
                i += 2
                continue
            # a short vowel (not the long IY/UW, ER, or a diphthong -
            # those are handled above and don't geminate the same way)
            # directly followed by a word-final voiceless stop is realized
            # with a geminate (small tsu): "input" IH-N-P-UH-T -> ...プ + ッ + ト
            # ("インプット"), "hot" HH-AA-T -> ホット, "stop" S-T-AA-P -> ストップ.
            # Medial clusters (e.g. option P+SH, action K+SH, project K+T)
            # do not geminate in Japanese loanwords.
            if (
                ph in ("P", "T", "K", "CH")
                and i > 0
                and bases[i - 1] in _VOWEL_KEYS
                and (i + 1 == n)
            ):
                result.append(("ッ", None))
            result.append((CONSONANTS[ph]["coda"], None))
            i += 1
            continue
        result.append(("？", None))
        i += 1
    return result


def arpabet_to_kana(phonemes, word=""):
    """Convert a list of ARPAbet phonemes (e.g. ['P', 'AW1', 'ER0']) to katakana.

    First-pass approximation only: does not model gemination (soku-on)
    for consonant clusters, nor does it distinguish rhotic vs
    non-rhotic vowel-R sequences beyond the simple "coda R lengthens
    the previous vowel" rule.
    """
    raw = "".join(m for m, _ in _morae_with_stress(phonemes, word=word))
    # Collapse consecutive long-vowel morae into one.  The ARPAbet rules
    # can produce sequences like "フェーー" for "fairer" (EH + coda R + ER)
    # because both the coda R and the following rhotic schwa add a "ー".
    # Japanese loanwords never write two long-vowel marks in a row.
    while "ーー" in raw:
        raw = raw.replace("ーー", "ー")
    return raw


# nvdajp's existing custom dic entries (e.g. custom_dic_maker.py's
# "vaiorin"/"vitamin" entries) keep "ヴ"-series kana in the braille
# transcription but substitute the "バ"-series (voiced bilabial stop)
# for speech: Open JTalk's phoneme table does define a genuine /v/
# for "ヴ" (see jpcommon_rule_utf_8.h), but the shipped HTS voice
# models were trained on native Japanese phoneme inventories and
# render /v/ poorly, so nvdajp has historically avoided it in speech.
_V_TO_B = {"ヴァ": "バ", "ヴィ": "ビ", "ヴェ": "ベ", "ヴォ": "ボ", "ヴ": "ブ"}


def kana_speech_safe(kana):
    """Replace "ヴ"-series kana with "バ"-series for the speech field,
    matching nvdajp's existing convention (see comment above)."""
    for v, b in _V_TO_B.items():
        kana = kana.replace(v, b)
    return kana


def arpabet_to_accent(phonemes, word=""):
    """Rough heuristic accent-position guess, as "position/moraCount".

    Places the accent drop immediately after the mora carrying English
    primary stress (stress digit '1'); if that mora is the last one,
    reports heiban (position 0, no drop). This is a coarse heuristic,
    NOT a substitute for native-speaker/dictionary verification -
    Japanese loanword accent does not always track English stress this
    directly (e.g. words ending in "-ン" are frequently heiban
    regardless of English stress position).
    """
    morae = _morae_with_stress(phonemes, word=word)
    total = len(morae)
    primary = next((i for i, (_, s) in enumerate(morae) if s == "1"), None)
    if primary is None or primary == total - 1:
        position = 0
    else:
        position = primary + 1
    return f"{position}/{total}"


if __name__ == "__main__":
    import sys

    for line in sys.stdin:
        line = line.strip()
        if not line or line.startswith(";;;"):
            continue
        parts = line.split()
        word, phonemes = parts[0], parts[1:]
        braille = arpabet_to_kana(phonemes, word=word)
        speech = kana_speech_safe(braille)
        accent = arpabet_to_accent(phonemes, word=word)
        print(f"{word}\t{' '.join(phonemes)}\tbraille={braille}\tspeech={speech}\taccent={accent}")
