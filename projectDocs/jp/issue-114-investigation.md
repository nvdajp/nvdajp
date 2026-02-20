# Issue #114 調査: 点訳エンジンと JTalk 併用時の性能低下

## 参照

- https://github.com/nvdajp/nvdajp/issues/114

## 現象

JTalk で音声出力中に点字表示を同時に行うと、以下の症状が発生する：

- カーソルキーを連打したときに引っかかるようなもたつき
- Win+R「ファイル名を指定して実行」で下矢印を押しても、点字表示ありだとスピーチが即座に中断されず、複数回押す必要がある
- 長い文書の読み上げ時にも発生

## 原因

MeCab（形態素解析）は JTalk（音声）と点訳（点字）の両方で共有されており、スレッドロックで排他制御されていた。

**ロックの保持範囲が過剰だった**：

1. **JTalk**（バックグラウンドスレッド）:  
   `MecabFeatures()` 作成時にロック取得 → `Mecab_analysis` → `Mecab_correctFeatures` →  
   **`libjt_synthesis`（音声合成、数秒かかる可能性）** →  
   `del mf` でロック解放

2. **点訳**（メインスレッド）:  
   フォーカス移動などで点字更新 → `louisHelper.translate` → `translator2` →  
   `MecabFeatures()` でロック取得を待機

**結果**：JTalk が音声合成中にロックを保持している間、点字更新（メインスレッド）がブロックされ、  
キー入力の処理やスピーチ中断の処理が遅れるため、カーソル連打時の引っかかりやスピーチの中断遅れが発生していた。

## 修正方針

**ロックの保持時間を最小化**：MeCab DLL 呼び出し（`Mecab_analysis`, `Mecab_correctFeatures`）の間のみロックを保持する。

- `mecab_analyze_and_correct()` ヘルパーを追加
- ロックは `Mecab_analysis` と `Mecab_correctFeatures` 実行中のみ保持
- その後の `Mecab_splitFeatures`、`libjt_synthesis`（JTalk）、`mecab_to_morphs`（点訳）はロック外で実行

## 修正箇所

- `source/synthDrivers/jtalk/mecab.py`: `mecab_analyze_and_correct()` 追加
- `source/synthDrivers/jtalk/jtalkDriver.py`: 上記ヘルパーを使用
- `source/synthDrivers/jtalk/translator2.py`: 上記ヘルパーを使用

## ブランチ

`fix-issue-114-mecab-lock`
