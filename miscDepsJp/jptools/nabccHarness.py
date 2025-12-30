# -*- coding: utf-8 -*-
# jptools/nabccHarness.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2014, 2023 Takuya Nishimoto
#
# For output field, blank should be 0x20 (not 0x2800).
# output の空白は 0x2800 ではなく 0x20 を使います
#
# The following means enabled lines
# "input": "オコナウ",
#
# The following means commenting out lines
# "_text": "行う",

import json
from pathlib import Path
path = Path(__file__).parent.parent / "include" / "libkuraji" / "tests" / "nabccHarness.json"
data = open(path, encoding="utf-8").read()
tests = json.loads(data)
