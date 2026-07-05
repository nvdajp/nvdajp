# libkuraji
# Copyright (C) 2019-2026 Takuya Nishimoto
# License: BSD 3-Clause. See LICENSE.

from .kana import translate_with_pos


def translate(text: str, nabcc: bool = False) -> str:
    """Translate kana text (translator2 output) into braille cells."""
    return translate_with_pos(text, nabcc=nabcc)[0]


__all__ = ["translate", "translate_with_pos"]
