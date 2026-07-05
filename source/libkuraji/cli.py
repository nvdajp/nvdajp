# libkuraji command line interface
# Copyright (C) 2026 Takuya Nishimoto
# License: BSD 3-Clause. See LICENSE.

import argparse
import sys

from .kana import translate_with_pos


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="kuraji",
        description="Translate kana text (one line per input) into Japanese braille.",
    )
    parser.add_argument("text", nargs="*", help="text to translate; reads stdin if omitted")
    parser.add_argument("--nabcc", action="store_true", help="use NABCC output mode")
    args = parser.parse_args(argv)

    lines = args.text if args.text else (line.rstrip("\n") for line in sys.stdin)
    for line in lines:
        cells, _ = translate_with_pos(line, nabcc=args.nabcc)
        print(cells)
    return 0


if __name__ == "__main__":
    sys.exit(main())
