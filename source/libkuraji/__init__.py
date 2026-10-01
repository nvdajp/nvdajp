# libkuraji
# Copyright (C) 2019-2026 Takuya Nishimoto
# License: BSD 3-Clause. See LICENSE.

from .kana import translate_with_pos
from .limits import InputTooLongError


def translate(text: str, nabcc: bool = False) -> str:
    """Translate kana text (translator2 output) into braille cells."""
    return translate_with_pos(text, nabcc=nabcc)[0]


def initialize(analyzer=None, logwrite=None):
    """Initialize the morphological analyzer for mixed-text (Kanji/Kana) translation.

    If analyzer is None, a default JTalkDicAnalyzer (which uses fugashi and
    automatically downloads the JTalk dictionary if needed) will be used.
    """
    if analyzer is None:
        try:
            from .jtalk_dic import make_analyzer
            analyzer = make_analyzer()
        except ImportError as e:
            raise ImportError(
                "The default analyzer requires 'fugashi' and dictionary dependencies. "
                "Please run 'pip install libkuraji[integration]' to install them, "
                "or pass a custom analyzer instance."
            ) from e
    from . import translator2
    translator2.initialize(analyzer=analyzer, logwrite=logwrite)


def translate_kanji(
    text: str, cursorPos: int = 0, nabcc: bool = False, **kwargs
) -> tuple[str, list[int], list[int], int]:
    """Translate mixed Kanji/Kana Japanese text, returning braille and position maps.

    If the analyzer has not been initialized, it will be automatically initialized
    with the default JTalkDicAnalyzer.

    Keyword arguments are forwarded to ``translator2.translate``. Notable options:

    * ``unicodeIO`` (bool, default ``False``): If ``True``, return Unicode braille
      (U+2800..U+28FF, blanks as U+0020), matching the CLI and liblouis
      ``dotsIO | ucBrl``. If ``False``, return liblouis ``dotsIO`` cells
      (U+8000..U+80FF, blanks as U+2800), the inherited nvdajp translator2
      default. See ``docs/encoding.md``.
    """
    from . import translator2
    if not translator2.mecab_initialized:
        initialize()
    return translator2.translate(text, cursorPos=cursorPos, nabcc=nabcc, **kwargs)


def terminate():
    """Terminate the morphological analyzer and clean up resources."""
    from . import translator2
    translator2.terminate()


__all__ = [
    "translate",
    "translate_with_pos",
    "initialize",
    "translate_kanji",
    "terminate",
    "InputTooLongError",
]
