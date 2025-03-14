# mecabHarness.py
# -*- coding: utf-8 -*-
# Japanese text processor test module
# by Takuya Nishimoto

# tasks: 要素2は音声合成の読み、(もしあれば)要素3は点訳用のカナ表記
# 点訳の表記と分かち書きは、規則で処理できないものを
# Mecab 辞書の第13フィールドに追加している。
# 要素3のスラッシュは形態素の区切り、スペースは形態素内のマスアケ

import json
from pathlib import Path
path = Path(__file__).parent.parent / "include" / "libkuraji" / "tests" / "mecabHarness.json"
data = open(path, encoding="utf-8").read()
tasks = json.loads(data)