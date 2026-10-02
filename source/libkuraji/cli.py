# libkuraji command line interface
# Copyright (C) 2026 Takuya Nishimoto
# License: BSD 3-Clause. See LICENSE.

import argparse
import json
import sys
from typing import List

from .kana import translate_with_pos
from .limits import InputTooLongError


def has_kanji(text: str) -> bool:
    """Return True if the text contains any Kanji (CJK Unified Ideographs)."""
    return any(0x4E00 <= ord(c) <= 0x9FCF or 0x3400 <= ord(c) <= 0x4DBF for c in text)


def make_out_pos(in_pos: List[int], in_len: int, out_len: int) -> List[int]:
    """Reconstruct outPos (input index -> output index mapping) from inPos."""
    out_pos = [-1] * in_len
    for p in range(out_len - 1, -1, -1):
        if in_pos[p] < len(out_pos):
            out_pos[in_pos[p]] = p
    prev = 0
    for p in range(in_len):
        if out_pos[p] == -1:
            out_pos[p] = prev
        else:
            prev = out_pos[p]
    return out_pos


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="kuraji",
        description="Translate Japanese text into braille.",
    )
    parser.add_argument("text", nargs="*", help="text to translate; reads stdin if omitted")
    parser.add_argument("--nabcc", action="store_true", help="use NABCC output mode")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-k", "--kana", action="store_true", help="force kana-only translation (disable MeCab)")
    group.add_argument("-j", "--kanji", action="store_true", help="force mixed Kanji/Kana translation (requires MeCab)")

    parser.add_argument("-p", "--positions", action="store_true", help="output position mapping JSON")
    args = parser.parse_args(argv)

    # Check if MeCab analyzer support is available
    has_mecab = False
    from . import translator2
    if translator2.mecab_initialized:
        has_mecab = True
    else:
        try:
            import fugashi  # noqa: F401
            has_mecab = True
        except ImportError:
            pass

    if args.kanji and not has_mecab:
        print(
            "Error: Mixed-text translation requires MeCab. Please run 'pip install libkuraji[integration]' to install it.",
            file=sys.stderr,
        )
        return 1

    lines = args.text if args.text else (line.rstrip("\n") for line in sys.stdin)

    for line in lines:
        try:
            use_kanji = False
            if args.kanji:
                use_kanji = True
            elif not args.kana and has_kanji(line):
                if has_mecab:
                    use_kanji = True
                else:
                    print(
                        "Error: Input contains Kanji but MeCab is not installed. "
                        "Please run 'pip install libkuraji[integration]' to install it, "
                        "or use -k/--kana to force kana-only translation.",
                        file=sys.stderr,
                    )
                    return 1

            if use_kanji:
                from . import translate_kanji
                # translate_kanji returns (outbuf, inPos, outPos, cursorPos)
                cells, in_pos, out_pos, _ = translate_kanji(line, nabcc=args.nabcc, unicodeIO=True)
            else:
                cells, in_pos = translate_with_pos(line, nabcc=args.nabcc)
                out_pos = make_out_pos(in_pos, len(line), len(cells))

            if args.positions:
                out_data = {
                    "text": line,
                    "braille": cells,
                    "inPos": in_pos,
                    "outPos": out_pos,
                }
                print(json.dumps(out_data, ensure_ascii=False))
            else:
                print(cells)
        except InputTooLongError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
