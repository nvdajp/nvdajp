# -*- coding: utf-8 -*-
# Usage
# > cd source
# > python ..\jptools\louisRunner.py
#
# @return: A tuple of:
#   the translated string,
#   a list of input positions for each position in the output,
#   a list of output positions for each position in the input, and
#   the position of the cursor in the output.
# @rtype: (str, list of int, list of int, int)

import sys

sys.path.append(r"..\source")
from louis import *  # noqa: F403
from nabcc2dots import nabcc2dots

print(version())  # noqa: F405
print

t = translate([b"louis/tables/en-us-g2.ctb"], "Hello world!", cursorPos=5)  # noqa: F405
print(t)
print(nabcc2dots(t[0]))
print
#   'Hello world!'
# (u',hello _w6',
#  # 0  1  2  3  4  5  6  7  8  9 10 11
#   [0, 0, 1, 2, 3, 4, 5, 6, 6,11      ],
#   [1, 2, 3, 4, 5, 6, 7, 7, 7, 7, 7, 9],
#  6)

t = translate([b"louis/tables/en-us-g1.utb"], "C++", cursorPos=0)  # noqa: F405
print(t)
print(nabcc2dots(t[0]))
print

t = translate([b"louis/tables/UEBC-g1.utb"], "C++", cursorPos=0)  # noqa: F405
print(t)
print(nabcc2dots(t[0]))
print

t = translate([b"louis/tables/UEBC-g1.utb"], "C++", cursorPos=0, mode=compbrlAtCursor)  # noqa: F405
print(t)
print(nabcc2dots(t[0]))
print

t = translate([b"louis/tables/UEBC-g1.utb"], "c++", cursorPos=0, mode=compbrlAtCursor)  # noqa: F405
print(t)
print(nabcc2dots(t[0]))

# convert from Unicode braille pattern to dotsIO
s = "".join([unichr(c) for c in range(0x2800, 0x2840)])  # noqa: F405
t = translate([b"louis/tables/nvdajp.ctb"], s, mode=dotsIO | pass1Only)  # noqa: F405
print(t)
print("".join([unichr((ord(c) & 0xFF) + 0x2800) for c in t[0]]).encode("utf-8"))  # noqa: F405
print
# (u'\u8000\u8001\u8002\u8003\u8004\u8005\u8006\u8007\u8008\u8009\u800a\u800b\u800c\u800d\u800e\u800f\u8010\u8011\u8012\u8013\u8014\u8015\u8016\u8017\u8018\u8019\u801a\u801b\u801c\u801d\u801e\u801f\u8020\u8021\u8022\u8023\u8024\u8025\u8026\u8027\u8028\u8029\u802a\u802b\u802c\u802d\u802e\u802f\u8030\u8031\u8032\u8033\u8034\u8035\u8036\u8037\u8038\u8039\u803a\u803b\u803c\u803d\u803e\u803f', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63], 0)

t = translate([b"louis/tables/en-us-g2.ctb"], "Hello world!", cursorPos=5, mode=dotsIO | pass1Only)  # noqa: F405
print(t)
print("".join([unichr((ord(c) & 0xFF) + 0x2800) for c in t[0]]).encode("utf-8"))  # noqa: F405
print
# (u',hello _w6', [0, 0, 1, 2, 3, 4, 5, 6, 6, 11], [1, 2, 3, 4, 5, 6, 7, 7, 7, 7, 7, 9], 6)
