# JTalk ユーザー辞書（jtusr.dic）の設計とテスト

最終更新: 2026-07-05

## 概要

JTalk / 日本語点訳（translator2）は、システム辞書 `sys.dic` に加えて
MeCab ユーザー辞書をロードできる。この文書は、JP smoke tests で使う
テスト用ユーザー辞書（`miscDepsJp/jptools/jtusr.csv` → `jtusr.dic`）の
ビルド方法と設計上の制約を記録する。

## ビルド方法

- ソース: `miscDepsJp/jptools/jtusr.csv`（UTF-8）
- ビルダー: `miscDepsJp/jptools/build_userdic.py`
- ツール: `miscDepsJp/jptools/jtalk/libopenjtalk/mecab/src/mecab-dict-index.exe`
  （x64。`scons jtalkSync` がパッチ済み libopenjtalk mecab ソースからビルドして配置する）
- 出力: `miscDepsJp/jptools/jtusr.dic`（gitignore 済み。**リポジトリにはコミットしない**）

```
uv run python miscDepsJp\jptools\build_userdic.py
```

テスト実行時は `build_userdic.ensure_user_dic()` がプロセスごとに1回
再ビルドするため、手動で実行する必要はない。`jptools/runJpSmokeTests.ps1`
の既定フィルタは `JpBrailleTests or JtalkTests or MecabTests` で、
ユーザー辞書テスト（`MecabTests.test_user_dic_applied`）を含む。

## 設計上の制約（2026-07-04〜05 の調査で確定）

### 1. バイナリ互換性: 毎回ビルドし直す

MeCab はユーザー辞書ロード時に `Dictionary::isCompatible`
（`miscDepsJp/include/libopenjtalk/mecab/src/dictionary.h`）で
バージョン・文字コード・左右文脈テーブルサイズ（lsize/rsize）の一致を
検査する。現行 `sys.dic` は 1377/1377。

かつて `jtusrdic/mecab-dict-index.exe`（PE32 i386、削除済み）で作られた
辞書は lsize/rsize=1/1 で、現行ランタイムでは
`RuntimeError: mecab_new failed` になりロードできない。
このためユーザー辞書はコミットせず、常にその時点の辞書ディレクトリ
（`source/synthDrivers/jtalk/dic`、matrix.bin を含む）に対してビルドする。

### 2. 文脈IDとコストは明示必須

CSV の文脈ID欄を空にする自動割当は CRF モデルファイルを要求するが、
naist-jdic にはモデルがないためビルドできない。エントリは
`0,0`（BOS/EOS）+ コスト明示とする。これは `sys.dic` のカスタムエントリ
（`custom_dic_maker.py` / `eng_dic_maker.py` / `tankan_dic_maker.py`）と
同じ規約であり、読み・マスアケの既存挙動を保存する。

品詞別文脈IDへの移行はロードマップのタスク 2.8。有効化された
ユーザー辞書経路は、sys.dic を再ビルドせずに品詞別ID・コストを試せる
2.8 の実験サンドボックスとして使える（例: `1345,1345,3000` で
名詞,一般 として登録した場合、コスト設計をしないと候補に勝てないことを
確認済み）。

### 3. 分かち書きはハーネスと一致させる

JpBrailleTests（translator2）はユーザー辞書をロードした状態で
`libkuraji/tests/harness.json` の全ケースを検証する。ユーザー辞書の
見出し語がハーネスにも存在する場合、CSV 第16フィールド（点訳用
分かち書き）はハーネスの期待値と一致させること。
現在のサンプル語 `次世代型点字ピンディスプレイ` は harness.json に
`ジセダイガタテンジピン ディスプレイ` として存在するため、CSV も
これに合わせている。

## テストの構成

- `MecabTests.test_all`: 全ハーネスケースをユーザー辞書なし→ありの順に
  実行し、どちらも結果が変わらないことを検証する。
- `MecabTests.test_user_dic_applied`: サンプル語がベース辞書では複数
  形態素、ユーザー辞書ありでは1形態素（CSV の読み・分かち書き）になる
  ことを検証する。ロード失敗（非互換）と「ロードされたが選択されない」
  （文脈ID・コスト設定ミス）の両方を検出できる。
- `JpBrailleTests`: ユーザー辞書をロードした状態で translator2 を検証
  する（ユーザー辞書がハーネス結果を変えないことの検証を兼ねる）。

## NVDA 実行時のユーザー辞書（参考）

NVDA 本体は `jtalkDir.py` が configDir の `jtusr.dic` を検出して
ロードする（この仕組みは変更していない）。ユーザー辞書を実行時に
コンパイルする `jtusrdic` アドオンのソースは `miscDepsJp/jptools/jtusrdic`
にあるが、現在ビルド・配布はされていない。復活させる場合は
`scons jtalkSync` がビルドする x64 の `mecab-dict-index.exe` を
アドオンに同梱し、エントリは明示ID+コスト形式にする必要がある。
ユーザーが文脈ID欄を空のまま書いたエントリはビルドできない
（CRF モデル要求で失敗する）ため、`compileUserDic` 側で CSV を
事前検証して明確なエラーを出す実装を検討すること。
