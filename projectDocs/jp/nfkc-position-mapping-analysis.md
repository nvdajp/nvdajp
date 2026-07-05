# NFKC 正規化によるポジションマッピングずれの分析と修正

## 解決済み (2026-07-04)

issue #117（三点リーダー）と #328（⑩以上の丸数字）は同一の根本原因であり、
NFKC 正規化を位置マップ付きで行うことで両方を解決した。

## 症状

* #117: 「ああ…こまった。」の点訳でポジションマッピングが不整合になり、
  テストケース（現 `miscDepsJp/include/libkuraji/tests/harness.json`）の
  `inpos2` / `inpos1` 期待値が無効化（`_inpos2` / `_inpos1`）されていた。
* #328: 「⑩あいうえお」で「あ」の位置のタッチカーソルキーを押すと
  「い」の位置にカーソルが移動する。①〜⑨では発生しない。

## 根本原因

点訳パイプライン（`source/synthDrivers/jtalk/translator2.py` の
`japanese_braille_separate`）は MeCab に渡す前に `text2mecab()` を呼び、
その中で NFKC 正規化が行われる。NFKC は一部の文字の文字数を変える:

* `…` (U+2026) → `...`（1文字 → 3文字）
* `⑩`〜`⑳`、`㉑`〜`㊿` → `10`〜`50`（1文字 → 2文字）。
  `①`〜`⑨` は 1文字 → 1文字なのでずれない（issue #328 のタイトル
  「⑩以上」と一致）。

一方、`morphs_to_string()` が作る `inpos2`（出力カナ → 入力テキストの
位置マップ）は形態素の表層文字数 `p += len(hyouki)` で位置を進めるが、
この表層は正規化「後」のテキスト由来である。呼び出し側
（`source/louisHelper.py` 経由の点字ディスプレイ処理）は `inpos2` を
元テキストの位置として使うため、正規化で文字数が変わった位置以降の
マッピングがすべてずれ、入力長を超える範囲外インデックスも発生していた
（`makeOutPos` が範囲チェックで黙って捨てるためクラッシュはしない）。

## 修正

* `_nvdajp_unicode.py` に `nfkc_normalize_with_map()` を追加。
  NFKC 正規化した文字列と、正規化後の各文字が元の文字列のどの位置に
  由来するかのマップ（nmap）を返す。
  * 結合文字と、NFKC で結合文字になる半角濁点・半濁点（U+FF9E/U+FF9F）は
    基底文字とまとめて正規化する（分割すると合成されず結果が変わるため）。
  * 連結結果が NFKC 安定でない場合は全体正規化にフォールバックし、
    位置は従来どおりの挙動とする。
* `japanese_braille_separate()` で `text2mecab()` の直前に位置マップ付きで
  正規化し（NFKC は冪等なので `text2mecab()` 内の再正規化では長さは
  変わらない）、`morphs_to_string()` の結果の `inpos2` を nmap で
  元テキストの位置に引き戻す。

これにより #117 で無効化されていた期待値
`inpos2 = [0,1,2,2,2,3,4,5,6,7]` がそのまま得られる。

## テスト

* `harness.json` の「ああ…こまった。」の `_inpos2` / `_inpos1` を有効化し、
  `inpos` / `outpos` も追加。
* 「⑩あいうえお」のケースを新規追加
  （outbuf `10 アイウエオ`、`inpos2 = [0,0,0,1,2,3,4,5]`）。
* 実行: `jptools\runJpSmokeTests.ps1 -SkipInstall -SkipOverlay -TestFilter "JpBrailleTests"`
  および `rununittests.bat -p "test_routing.py"` / `-p "test_louisHelper.py"`。

## 残課題（同族の未対応ケース）

`japanese_braille_separate()` には NFKC 以外にも長さが変わる事前置換が
残っており、これらは今回の位置マップの対象外（発生頻度が低いため）:

* CR/LF → 空白（`\r\n` 2文字 → 1文字）
* `あ゛` → `あ`（2文字 → 1文字）

必要になれば同じマップ機構（置換にも nmap を通す）に載せられる。
