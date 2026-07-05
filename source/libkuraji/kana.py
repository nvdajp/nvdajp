# libkuraji kana-to-braille translation (translator1 stage)
# Copyright (C) 2026 Takuya Nishimoto
# License: BSD 3-Clause. See LICENSE.
#
# Clean-room implementation driven by tests/harness.json.
# Input is katakana text already segmented by the upstream stage
# (word wrapping / masuake); output is Unicode braille cells
# (U+2800..U+28FF) with U+0020 for blanks, plus a position map:
# for each output cell, the index of the (normalized) input character
# it came from.

import unicodedata
from typing import List, Tuple


def _cell(*dots: int) -> str:
    value = 0
    for dot in dots:
        value |= 1 << (dot - 1)
    return chr(0x2800 | value)


# --- base kana tables ------------------------------------------------

_VOWEL_DOTS = {
    "A": (1,),
    "I": (1, 2),
    "U": (1, 4),
    "E": (1, 2, 4),
    "O": (2, 4),
}

_ROW_EXTRA_DOTS = {
    "": (),
    "K": (6,),
    "S": (5, 6),
    "T": (3, 5),
    "N": (3,),
    "H": (3, 6),
    "M": (3, 5, 6),
    "R": (5,),
}

_ROW_KANA = {
    "": "アイウエオ",
    "K": "カキクケコ",
    "S": "サシスセソ",
    "T": "タチツテト",
    "N": "ナニヌネノ",
    "H": "ハヒフヘホ",
    "M": "マミムメモ",
    "R": "ラリルレロ",
}

# single kana -> cell string
KANA1 = {}
for _row, _kana in _ROW_KANA.items():
    for _v, _ch in zip("AIUEO", _kana):
        KANA1[_ch] = _cell(*(_VOWEL_DOTS[_v] + _ROW_EXTRA_DOTS[_row]))

KANA1.update(
    {
        "ヤ": _cell(3, 4),
        "ユ": _cell(3, 4, 6),
        "ヨ": _cell(3, 4, 5),
        "ワ": _cell(3),
        "ヰ": _cell(1, 2, 3),
        "ヱ": _cell(2, 3, 5),
        "ヲ": _cell(3, 5),
        "ン": _cell(3, 5, 6),
        "ッ": _cell(2),
        "ー": _cell(2, 5),
    }
)

_DAKUTEN = _cell(5)
_HANDAKUTEN = _cell(6)
_YOON = _cell(4)
_YOON_DAKU = _cell(4, 5)
_YOON_HANDAKU = _cell(4, 6)
_SPECIAL_26 = _cell(2, 6)  # gairaion prefix (fa/wi/tu etc.)
_SPECIAL_256 = _cell(2, 5, 6)  # gairaion voiced prefix (va etc.)

# voiced kana -> dakuten prefix + base cell
for _voiced, _base in {
    "ガギグゲゴ": "カキクケコ",
    "ザジズゼゾ": "サシスセソ",
    "ダヂヅデド": "タチツテト",
    "バビブベボ": "ハヒフヘホ",
    "ヴ": "ウ",
}.items():
    for _vc, _bc in zip(_voiced, _base):
        KANA1[_vc] = _DAKUTEN + KANA1[_bc]

for _vc, _bc in zip("パピプペポ", "ハヒフヘホ"):
    KANA1[_vc] = _HANDAKUTEN + KANA1[_bc]

# --- two-character kana (youon and gairaion) --------------------------

_SMALL_VOWEL = {"ャ": "A", "ュ": "U", "ョ": "O"}

# two kana -> cells; prefix cell maps to the first character,
# remaining cells map to the second character
KANA2 = {}
for _table, _prefix in (
    ({"キ": "K", "シ": "S", "チ": "T", "ニ": "N", "ヒ": "H", "ミ": "M", "リ": "R"}, _YOON),
    ({"ギ": "K", "ジ": "S", "ヂ": "T", "ビ": "H"}, _YOON_DAKU),
    ({"ピ": "H"}, _YOON_HANDAKU),
):
    for _kc, _row in _table.items():
        for _small, _v in _SMALL_VOWEL.items():
            KANA2[_kc + _small] = _prefix + _cell(
                *(_VOWEL_DOTS[_v] + _ROW_EXTRA_DOTS[_row])
            )


def _k2(pair: str, prefix: str, base: str) -> None:
    KANA2[pair] = prefix + KANA1[base]


# gairaion (special sounds); derived from the harness expectations
_k2("イェ", _YOON, "エ")
_k2("ウィ", _SPECIAL_26, "イ")
_k2("ウェ", _SPECIAL_26, "エ")
_k2("ウォ", _SPECIAL_26, "オ")
_k2("キェ", _YOON, "ケ")
_k2("シェ", _YOON, "セ")
_k2("ジェ", _YOON_DAKU, "セ")
_k2("チェ", _YOON, "テ")
_k2("ティ", _YOON, "チ")
_k2("ディ", _YOON_DAKU, "チ")
_k2("トゥ", _SPECIAL_26, "ツ")
_k2("ドゥ", _SPECIAL_256, "ツ")
_k2("ニェ", _YOON, "ネ")
_k2("ヒェ", _YOON, "ヘ")
_k2("ファ", _SPECIAL_26, "ハ")
_k2("フィ", _SPECIAL_26, "ヒ")
_k2("フェ", _SPECIAL_26, "ヘ")
_k2("フォ", _SPECIAL_26, "ホ")
_k2("ヴァ", _SPECIAL_256, "ハ")
_k2("ヴィ", _SPECIAL_256, "ヒ")
_k2("ヴェ", _SPECIAL_256, "ヘ")
_k2("ヴォ", _SPECIAL_256, "ホ")

# --- punctuation and symbols ------------------------------------------

# sentence punctuation: cell(s) followed by padding blanks unless at
# the end of the input
_SENTENCE_PUNCT = {
    "。": (_cell(2, 5, 6), 2),
    "？": (_cell(2, 6), 1),
    "！": (_cell(2, 3, 5), 1),
    "?": (_cell(2, 6), 1),
    "!": (_cell(2, 3, 5), 1),
    "、": (_cell(5, 6), 1),
    "・": (_cell(5), 1),
}

# enclosure marks
_ENCLOSURE = {
    "(": _cell(2, 3, 5, 6),
    ")": _cell(2, 3, 5, 6),
    "（": _cell(2, 3, 5, 6),
    "）": _cell(2, 3, 5, 6),
    "「": _cell(3, 6),
    "」": _cell(3, 6),
    "『": _cell(5, 6) + _cell(3, 6),
    "』": _cell(3, 6) + _cell(2, 3),
}
for _c in "[{“‘〔〈《【〝｛":
    _ENCLOSURE[_c] = _cell(5) + _cell(2, 3, 5, 6)
for _c in "]}”’〕〉》】〟｝":
    _ENCLOSURE[_c] = _cell(2, 3, 5, 6) + _cell(2)

# symbols in kana context
_SYMBOL = {
    ",": _cell(3),
    ".": _cell(2, 5, 6),
    "-": _cell(3, 6),
    ":": _cell(5) + _cell(2),
    "<": _cell(3, 5) * 2,
    "=": _cell(2, 5) * 2,
    ">": _cell(2, 6) * 2,
    "+": _cell(2, 6),
    "/": _cell(3, 4),
    "%": _cell(5, 6) + _cell(1, 2, 3, 4),
    "@": _cell(5, 6) + _cell(2, 4, 6),
    "#": _cell(5, 6) + _cell(1, 4, 6),
    "*": _cell(5, 6) + _cell(1, 6),
    "&": _cell(5, 6) + _cell(1, 2, 3, 4, 6),
}

# words spelled out for symbols in kana context
_LITERAL_SYMBOL = {
    # yuubin bangou (postal mark), spelled inside explanation signs
    "〒": "⠰⠶⠬⠒⠐⠧⠴ ⠐⠥⠴⠐⠪⠒⠶⠆",
}

# symbols spelled with surrounding blanks in kana context:
# (cells, blank before, blank after)
_SPACED_SYMBOL = {
    "→": (_cell(2, 5) * 2 + _cell(1, 3, 5), True, True),
    "←": (_cell(2, 4, 6) + _cell(2, 5) * 2, True, True),
    "※": (_cell(3, 5) * 2, False, True),
}

# shape and other symbols spelled as sign sequences
_SHAPE_SYMBOL = {
    "☆": _cell(5, 6) + _cell(2, 3, 4, 6) + _cell(2),
    "★": _cell(5, 6) + _cell(2, 3, 4, 6) + _cell(2, 3),
    "○": _cell(6) + _cell(1, 3, 5, 6) + _cell(2),
    "●": _cell(6) + _cell(1, 3, 5, 6) + _cell(2, 3),
    "◎": _cell(6) + _cell(1, 3, 5, 6) + _cell(2, 5, 6),
    "□": _cell(6) + _cell(1, 2, 5, 6) + _cell(2),
    "■": _cell(6) + _cell(1, 2, 5, 6) + _cell(2, 3),
    "△": _cell(6) + _cell(1, 5, 6) + _cell(2),
    "▲": _cell(6) + _cell(1, 5, 6) + _cell(2, 3),
    "▽": _cell(5, 6) + _cell(1, 5, 6) + _cell(2),
    "▼": _cell(5, 6) + _cell(1, 5, 6) + _cell(2, 3),
    "◇": _cell(4, 6) + _cell(1, 2, 3, 6) + _cell(2),
    "◆": _cell(4, 6) + _cell(1, 2, 3, 6) + _cell(2, 3),
    "×": _cell(5, 6) + _cell(1, 6) + _cell(2),
}

# --- digits and Latin -------------------------------------------------

_NUMERIC_SIGN = _cell(3, 4, 5, 6)
_DIGIT_CELLS = {
    "1": _cell(1),
    "2": _cell(1, 2),
    "3": _cell(1, 4),
    "4": _cell(1, 4, 5),
    "5": _cell(1, 5),
    "6": _cell(1, 2, 4),
    "7": _cell(1, 2, 4, 5),
    "8": _cell(1, 2, 5),
    "9": _cell(2, 4),
    "0": _cell(2, 4, 5),
}
_TSUNAGI = _cell(3, 6)  # first connector sign
_FOREIGN_SIGN = _cell(5, 6)
_CAPITAL_SIGN = _cell(6)

_LATIN_DOTS = {
    "a": (1,), "b": (1, 2), "c": (1, 4), "d": (1, 4, 5), "e": (1, 5),
    "f": (1, 2, 4), "g": (1, 2, 4, 5), "h": (1, 2, 5), "i": (2, 4),
    "j": (2, 4, 5), "k": (1, 3), "l": (1, 2, 3), "m": (1, 3, 4),
    "n": (1, 3, 4, 5), "o": (1, 3, 5), "p": (1, 2, 3, 4),
    "q": (1, 2, 3, 4, 5), "r": (1, 2, 3, 5), "s": (2, 3, 4),
    "t": (2, 3, 4, 5), "u": (1, 3, 6), "v": (1, 2, 3, 6),
    "w": (2, 4, 5, 6), "x": (1, 3, 4, 6), "y": (1, 3, 4, 5, 6),
    "z": (1, 3, 5, 6),
}
LATIN = {ch: _cell(*dots) for ch, dots in _LATIN_DOTS.items()}

# ASCII symbols inside a computer braille context (opened with dot-6
# quote mark, i.e. the two-cell sign U+2820 U+2826)
_COMPUTER_SYMBOL = {
    ".": _cell(2, 5, 6),
    ",": _cell(2),
    "@": _cell(2, 4, 6),
    "-": _cell(3, 6),
    "'": _cell(3),
    ":": _cell(5) + _cell(2),
    ";": _cell(2, 3),
    "?": _cell(5) + _cell(2, 3, 6),
    "!": _cell(2, 3, 5),
    "/": _cell(3, 4),
    "\\": _cell(1, 2, 4, 6),
    "_": _cell(5) + _cell(3, 6),
    "~": _cell(5) + _cell(1, 4),
    "&": _cell(1, 2, 3, 4, 6),
    "#": _cell(1, 4, 6),
    "+": _cell(3, 4, 6),
    "$": _cell(1, 4, 5, 6),
    "%": _cell(1, 2, 4, 5, 6),
    "*": _cell(1, 6),
    "|": _cell(1, 2, 5, 6),
    "^": _cell(4, 5),
    "<": _cell(3, 5) * 2,
    ">": _cell(2, 6) * 2,
    "=": _cell(2, 5) * 2,
    "{": _cell(1, 2, 6),
    "}": _cell(3, 4, 5),
    "[": _cell(1, 2, 3, 5, 6),
    "]": _cell(2, 3, 4, 5, 6),
}

# ASCII symbols inside a foreign-language quote (plain quote mark)
_QUOTE_SYMBOL = dict(_COMPUTER_SYMBOL)
_QUOTE_SYMBOL.update(
    {
        "?": _cell(2, 3, 6),
        "%": _cell(5, 6) + _cell(1, 2, 3, 4),
        "*": _cell(3, 5) * 2,
        "+": _cell(2, 6),
    }
)

# --- Cyrillic and Greek letters ---------------------------------------
# Lowercase letters map to international braille patterns; capitals add
# dot 7 (see U+2840 range).

_CYRILLIC_DOTS = {
    "а": (1,), "б": (1, 2), "в": (2, 4, 5, 6), "г": (1, 2, 4, 5),
    "д": (1, 4, 5), "е": (1, 5), "ж": (2, 4, 5), "з": (1, 3, 5, 6),
    "и": (2, 4), "й": (1, 2, 3, 4, 6), "к": (1, 3), "л": (1, 2, 3),
    "м": (1, 3, 4), "н": (1, 3, 4, 5), "о": (1, 3, 5), "п": (1, 2, 3, 4),
    "р": (1, 2, 3, 5), "с": (2, 3, 4), "т": (2, 3, 4, 5), "у": (1, 3, 6),
    "ф": (1, 2, 4), "х": (1, 2, 5), "ц": (1, 4), "ч": (1, 2, 3, 4, 5),
    "ш": (1, 5, 6), "щ": (1, 3, 4, 6), "ъ": (1, 2, 3, 5, 6),
    "ы": (2, 3, 4, 6), "ь": (2, 3, 4, 5, 6), "э": (2, 4, 6),
    "ю": (1, 2, 5, 6), "я": (1, 2, 4, 6), "ё": (1, 6),
    "ѣ": (3, 4, 5), "ѫ": (2, 4, 6),
}

_GREEK_DOTS = {
    "α": (1,), "β": (1, 2), "γ": (1, 2, 4, 5), "δ": (1, 4, 5),
    "ε": (1, 5), "ζ": (1, 3, 5, 6), "η": (1, 5, 6), "θ": (1, 4, 5, 6),
    "ι": (2, 4), "κ": (1, 3), "λ": (1, 2, 3), "μ": (1, 3, 4),
    "ν": (1, 3, 4, 5), "ξ": (1, 3, 4, 6), "ο": (1, 3, 5),
    "π": (1, 2, 3, 4), "ρ": (1, 2, 3, 5), "σ": (2, 3, 4), "ς": (2, 3, 4),
    "τ": (2, 3, 4, 5), "υ": (1, 3, 6), "φ": (1, 2, 4),
    "χ": (1, 2, 3, 4, 6), "ψ": (1, 3, 4, 5, 6), "ω": (2, 4, 5, 6),
}

_LETTER_CELLS = {}
for _dots_map in (_CYRILLIC_DOTS, _GREEK_DOTS):
    for _ch, _dots in _dots_map.items():
        _LETTER_CELLS[_ch] = _cell(*_dots)
        _upper = _ch.upper()
        if _upper != _ch:
            # capital letters carry dot 7
            _LETTER_CELLS[_upper] = chr(ord(_cell(*_dots)) | 0x40)

_FOREIGN_OPEN = _cell(2, 3, 6)  # inner cell of the quote mark
_FOREIGN_CLOSE = _cell(3, 5, 6)

# kana requiring a connector sign right after a digit run
_TSUNAGI_KANA = set("アイウエオラリルレロ")

# letters confusable with digits (a-j) need a foreign sign after numbers
_DIGIT_LIKE_LETTERS = set("abcdefghij")

# --- NABCC (North American Braille Computer Code) ---------------------
# In NABCC mode every ASCII character maps directly to one cell:
# lowercase letters use the standard patterns, capitals add dot 7,
# digits are "dropped" (lowered) patterns without a numeric sign.

_NABCC_DIGIT_DOTS = {
    "1": (2,), "2": (2, 3), "3": (2, 5), "4": (2, 5, 6), "5": (2, 6),
    "6": (2, 3, 5), "7": (2, 3, 5, 6), "8": (2, 3, 6), "9": (3, 5),
    "0": (3, 5, 6),
}

_NABCC_SYMBOL_DOTS = {
    ",": (6,), ";": (5, 6), ":": (1, 5, 6), ".": (4, 6),
    "!": (2, 3, 4, 6), '"': (5,), "'": (3,), "(": (1, 2, 3, 5, 6),
    ")": (2, 3, 4, 5, 6), "-": (3, 6), "_": (4, 5, 6), "<": (1, 2, 6),
    "=": (1, 2, 3, 4, 5, 6), ">": (3, 4, 5), "%": (1, 4, 6),
    "+": (3, 4, 6), "~": (4, 5), "`": (4,), "&": (1, 2, 3, 4, 6),
    "$": (1, 2, 4, 6), "?": (1, 4, 5, 6), "{": (2, 4, 6),
    "[": (2, 4, 6, 7), "}": (1, 2, 4, 5, 6), "]": (1, 2, 4, 5, 6, 7),
    "^": (4, 5, 7), "@": (4, 7), "#": (3, 4, 5, 6), "\\": (1, 2, 5, 6, 7),
    "|": (1, 2, 5, 6), "/": (3, 4), "*": (1, 6),
}

NABCC = {" ": " "}
for _ch, _dots in _NABCC_DIGIT_DOTS.items():
    NABCC[_ch] = _cell(*_dots)
for _ch, _dots in _NABCC_SYMBOL_DOTS.items():
    NABCC[_ch] = _cell(*_dots)
for _ch, _braille in LATIN.items():
    NABCC[_ch] = _braille
    NABCC[_ch.upper()] = chr(ord(_braille) | 0x40)  # capital: dot 7

# number punctuation: index by "inside quote/computer context"
_NUMBER_COMMA = {False: _cell(3), True: _cell(2)}
_NUMBER_POINT = {False: _cell(2), True: _cell(2, 5, 6)}


def _is_braille(ch: str) -> bool:
    return 0x2800 <= ord(ch) <= 0x28FF


def _is_latin(ch: str) -> bool:
    return ("a" <= ch <= "z") or ("A" <= ch <= "Z")


def _is_digit(ch: str) -> bool:
    return "0" <= ch <= "9"


def _normalize(text: str) -> str:
    """Fold halfwidth katakana (with voiced marks) into fullwidth."""
    if not any("｡" <= ch <= "ﾟ" for ch in text):
        return text
    chars: List[str] = []
    for ch in text:
        if 0xFF61 <= ord(ch) <= 0xFF9F:
            norm = unicodedata.normalize("NFKC", ch)
            if norm in ("゙", "゚") and chars:
                merged = unicodedata.normalize("NFKC", chars[-1] + norm)
                if len(merged) == 1:
                    chars[-1] = merged
                    continue
            chars.extend(norm)
        else:
            chars.append(ch)
    return "".join(chars)


# first characters of two-character kana sequences
_KANA2_FIRST = frozenset(key[0] for key in KANA2)


def translate_with_pos(text: str, nabcc: bool = False) -> Tuple[str, List[int]]:
    """Translate kana text into braille; return (cells, input positions)."""
    norm = _normalize(text)
    out: List[str] = []  # cell strings; joined at the end
    pos: List[int] = []  # one entry per cell
    # quote context: None (kana), "computer" (dot-6 quote), "quote"
    context = None
    latin_active = False  # a foreign sign is still in effect (kana context)
    i = 0
    n = len(norm)
    out_append = out.append
    pos_append = pos.append
    pos_extend = pos.extend

    def emit(cells: str, index: int) -> None:
        out_append(cells)
        if len(cells) == 1:
            pos_append(index)
        else:
            pos_extend((index,) * len(cells))

    def prev_char() -> str:
        return norm[i - 1] if i > 0 else ""

    def after_digits() -> bool:
        """True when the last meaningful character was a digit
        (skipping over a number-internal period or comma)."""
        j = i - 1
        while j >= 0 and norm[j] in ".,":
            j -= 1
        return j >= 0 and _is_digit(norm[j])

    while i < n:
        ch = norm[i]

        # fast path: kana (the common case)
        two = norm[i : i + 2] if ch in _KANA2_FIRST else ""
        if two in KANA2 or ch in KANA1:
            if latin_active:
                latin_active = False
            if i > 0 and _is_latin(norm[i - 1]):
                emit(_TSUNAGI, i - 1)
            if two in KANA2:
                cells = KANA2[two]
                emit(cells[0], i)
                emit(cells[1:], i + 1)
                i += 2
            else:
                emit(KANA1[ch], i)
                i += 1
            continue

        if ch == " ":
            emit(" ", i)
            latin_active = False
            i += 1
            continue

        if _is_braille(ch):
            if ch == _FOREIGN_OPEN:
                context = "computer" if prev_char() == _CAPITAL_SIGN else "quote"
            elif ch == _FOREIGN_CLOSE:
                context = None
            emit(" " if ch == "⠀" else ch, i)
            i += 1
            continue

        if nabcc and ch.isascii() and ch in NABCC:
            emit(NABCC[ch], i)
            i += 1
            continue

        if _is_digit(ch) or (
            ch == "'" and context is None and i + 1 < n and _is_digit(norm[i + 1])
        ):
            latin_active = False
            # numeric sign, unless a literal numeric sign cell precedes
            if not (out and out[-1].endswith(_NUMERIC_SIGN)):
                emit(_NUMERIC_SIGN, i)
            if ch == "'":
                # year abbreviation: apostrophe becomes dot 3 in a number
                emit(_cell(3), i)
                i += 1
            while i < n:
                c = norm[i]
                if _is_digit(c):
                    emit(_DIGIT_CELLS[c], i)
                    i += 1
                elif c == "," and (i + 1 >= n or _is_digit(norm[i + 1])):
                    emit(_NUMBER_COMMA[context is not None], i)
                    i += 1
                elif c == "." and i + 1 < n and _is_digit(norm[i + 1]):
                    emit(_NUMBER_POINT[context is not None], i)
                    i += 1
                else:
                    break
            if context is None and i < n:
                nxt = norm[i]
                needs_tsunagi = nxt in _TSUNAGI_KANA
                if not needs_tsunagi and nxt in "ワヰヱヲ":
                    # wa-row kana: connector only when a-row kana follow
                    # in the same word (Tenyaku Tebiki ch.4-4 1, remark 1)
                    j = i + 1
                    while j < n and norm[j] not in (" ", "　"):
                        if norm[j] in "アイウエオ":
                            needs_tsunagi = True
                            break
                        j += 1
                if needs_tsunagi:
                    emit(_TSUNAGI, i - 1)
            continue

        if _is_latin(ch):
            start = i
            j = i
            while j < n and _is_latin(norm[j]):
                j += 1
            run = norm[i:j]
            first = run[0].lower()
            if context is None:
                if not latin_active:
                    emit(_FOREIGN_SIGN, start)
                latin_active = True
            elif first in _DIGIT_LIKE_LETTERS and (
                _is_digit(prev_char())
                or (context == "computer" and after_digits())
            ):
                # separate digit-like letters from a preceding number
                emit(_FOREIGN_SIGN, start)
            if len(run) > 1 and run.isupper():
                emit(_CAPITAL_SIGN * 2, start)
                for k, c in enumerate(run):
                    emit(LATIN[c.lower()], start + k)
            else:
                for k, c in enumerate(run):
                    if c.isupper():
                        emit(_CAPITAL_SIGN, start + k)
                    emit(LATIN[c.lower()], start + k)
            i = j
            continue

        if context is not None:
            table = _COMPUTER_SYMBOL if context == "computer" else _QUOTE_SYMBOL
            if ch in table:
                emit(table[ch], i)
                i += 1
                continue

        # kana context from here on
        if ch == "/" and latin_active:
            # a slash does not end the foreign sign's scope
            emit(_SYMBOL["/"], i)
            i += 1
            continue

        if ch == "," and latin_active:
            # comma between Latin items; the foreign sign scope ends
            emit(_cell(2), i)
            latin_active = False
            i += 1
            continue

        latin_active = False

        if ch in _SENTENCE_PUNCT:
            cells, pad = _SENTENCE_PUNCT[ch]
            emit(cells, i)
            if i + 1 < n:
                emit(" " * pad, i)
            i += 1
            continue

        if ch in _LITERAL_SYMBOL:
            emit(_LITERAL_SYMBOL[ch], i)
            i += 1
            continue

        if ch in _LETTER_CELLS:
            emit(_LETTER_CELLS[ch], i)
            i += 1
            continue

        if ch in _SPACED_SYMBOL:
            cells, before, after = _SPACED_SYMBOL[ch]
            if before and out and not out[-1].endswith(" "):
                emit(" ", i)
            emit(cells, i)
            if after and i + 1 < n:
                emit(" ", i)
            i += 1
            continue

        if ch in _SHAPE_SYMBOL:
            emit(_SHAPE_SYMBOL[ch], i)
            i += 1
            continue

        if ch in _ENCLOSURE:
            emit(_ENCLOSURE[ch], i)
            i += 1
            continue

        if ch in _SYMBOL:
            emit(_SYMBOL[ch], i)
            i += 1
            continue

        if ch in (" ", "　"):
            emit(" ", i)
            i += 1
            continue

        # unknown character: emit a placeholder cell so that the
        # 1-input-char-to-1-output-cell position mapping is preserved
        # for scripts outside this translator's coverage (e.g. Hebrew).
        # translator2 replaces "□" with a space in its final output.
        emit("□", i)
        i += 1

    return "".join(out), pos


def translateWithInPos(text: str, nabcc: bool = False) -> Tuple[str, List[int]]:
    """Compatibility alias matching the historical NVDAJP entry point name."""
    return translate_with_pos(text, nabcc=nabcc)
