# unicodeutil.py (NFKC normalization with position maps)
# -*- coding: utf-8 -*-
# Copyright (C) 2026 Takuya Nishimoto
# License: BSD 3-Clause. See LICENSE.
# Originally _nvdajp_unicode.py in NVDA Japanese (nvdajp); relicensed
# by the copyright holder.

import unicodedata


def nfkc_normalize_with_map(s: str) -> tuple[str, list[int]]:
	"""Return the NFKC-normalized string together with a map from each
	normalized character back to its position in the original string.
	NFKC changes the character count for some characters, e.g.
	U+2026 HORIZONTAL ELLIPSIS -> "..." and U+2469 CIRCLED NUMBER TEN -> "10",
	which would break braille position mapping (nvdajp issues #117, #328).
	"""
	out: list[str] = []
	nmap: list[int] = []
	i = 0
	n = len(s)
	while i < n:
		j = i + 1
		# Normalize combining characters, and the halfwidth voiced/semi-voiced
		# sound marks (U+FF9E/U+FF9F, which NFKC turns into combining
		# characters), together with their base character; normalizing them
		# separately would prevent composition and change the result.
		while j < n and (unicodedata.combining(s[j]) or s[j] in "\uff9e\uff9f"):
			j += 1
		seg = unicodedata.normalize("NFKC", s[i:j])
		out.append(seg)
		nmap.extend([i] * len(seg))
		i = j
	result = "".join(out)
	if unicodedata.normalize("NFKC", result) != result:
		# The concatenation of per-segment results is not NFKC-stable.
		# Fall back to whole-string normalization and keep the legacy
		# position behavior (positions in the normalized string, with the
		# tail clamped to the last character of the original string).
		result = unicodedata.normalize("NFKC", s)
		nmap = [min(p, n - 1) for p in range(len(result))]
	return (result, nmap)


# characters folded before NFKC normalization
_PRE_NFKC_MAP = str.maketrans(
	{
		" ": " ",  # no-break space
		" ": " ",  # en space
		" ": " ",  # em space
		" ": " ",  # three-per-em space
		" ": " ",  # four-per-em space
		" ": " ",  # six-per-em space
		" ": " ",  # figure space
		" ": " ",  # punctuation space
		" ": " ",  # thin space
		" ": " ",  # hair space
		# ​ (zero width space) is kept: used as the tab placeholder
		"‎": "",  # left-to-right mark
		"‏": "",  # right-to-left mark
		"�": "",  # replacement character
		# converted to fullwidth by Mecab_text2mecab(); NFKC cannot restore it
		"．": ".",  # fullwidth full stop
	}
)

# characters folded after NFKC normalization
_POST_NFKC_MAP = str.maketrans(
	{
		"−": "-",  # minus sign
		"¥": "\\",  # yen sign
		"〜": "~",  # wave dash
		# accented Latin letters folded to ASCII
		"À": "A", "Á": "A", "Â": "A", "Ä": "A", "Å": "A", "Æ": "AE",
		"Ç": "C", "È": "E", "É": "E", "Ê": "E", "Ë": "E",
		"Ì": "I", "Í": "I", "Î": "I", "Ï": "I", "Ñ": "N",
		"Ò": "O", "Ó": "O", "Ô": "O", "Ö": "O", "Ø": "O",
		"Ù": "U", "Ú": "U", "Û": "U", "Ü": "U", "Ý": "Y",
		"à": "a", "á": "a", "â": "a", "ä": "a", "å": "a", "æ": "ae",
		"ç": "c", "è": "e", "é": "e", "ê": "e", "ë": "e",
		"ì": "i", "í": "i", "î": "i", "ï": "i", "ñ": "n",
		"ò": "o", "ó": "o", "ô": "o", "ö": "o", "ø": "o",
		"ù": "u", "ú": "u", "û": "u", "ü": "u", "ý": "y", "ÿ": "y",
		"Œ": "OE", "œ": "oe", "Ÿ": "Y",
	}
)


def unicode_normalize(s: str) -> str:
	if s.isascii():
		# every folded character is non-ASCII and NFKC is the identity
		# for ASCII, so nothing to do
		return s
	s = unicodedata.normalize("NFKC", s.translate(_PRE_NFKC_MAP))
	return s.translate(_POST_NFKC_MAP)
