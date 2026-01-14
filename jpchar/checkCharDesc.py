# coding: UTF-8
# checkCharDesc.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2017,2023 Takuya Nishimoto, NVDA Japanese Team
# usage:
# > py -3 checkCharDesc.py

import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import _checkCharDesc as cc  # noqa: E402

ch = cc.read_chardesc_file(cc.CH_FILE)
ch = cc.read_characters_file(cc.CS_FILE)
ch = cc.add_katakana_prefix_to_characters(ch)
cc.find_desc_duplicate(ch, skipKeisen=True, skipEmoji=True)
