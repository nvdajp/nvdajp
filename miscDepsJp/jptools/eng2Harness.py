# -*- coding: utf-8 -*-
# jptools/eng2Harness.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023,2026 NVDA Japanese Team
#
# eng2Harness: 英語2級点字（UEB/US Grade 2）用テストケース。
# 各ケースは text（原文）, input（カナ・外国語引用符付き）, output（1級）, ueb_g2, us_g2 を持つ。
# 期待値のスキップ: "_output" / "_ueb_g2" / "_us_g2" は未実装・既知の失敗用（その検証をスキップ）。
# 規約の詳細は projectDocs/jp/braille-ja-jp-comp6.md の「既知の失敗・スキップ規約」を参照。

import json
from pathlib import Path

path = Path(__file__).parent.parent / "include" / "libkuraji" / "tests" / "eng2Harness.json"
data = open(path, encoding="utf-8").read()
eng2_tests = json.loads(data)
