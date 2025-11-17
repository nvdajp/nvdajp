# 日本語点字出力テーブル (ja-jp-comp6.utb)

開発者向けのメモです。`ja-jp-comp6.utb` が選択されたときは、liblouis を経由せず JP 独自の点訳エンジンを使います。

## エンジン切り替え

- `source/louisHelper.py` で最初のテーブル名が `ja-jp-comp6.utb` の場合、`synthDrivers.jtalk.translator2` を呼び出し、liblouis の `translate` は使わない。
- translator2 は MeCab で形態素解析を行い、日本語点字（第2種・6点コンピュータ点字）に従って出力を構成する。liblouis テーブルでは追従が難しい日本語固有の処理をここにまとめている。

## NABCC 設定と情報処理点字

- translator2 には `nabcc` フラグがあり、`NVDA 設定 → 点字 → カーソル位置の単語をコンピューター点字に展開する (expandAtCursor)` の値をそのまま渡している。
- `nabcc=True` のときは情報処理点字向けの記号付与や、外国語引用符を含む欧文の扱いを維持する。`nabcc=False` のときは文脈に応じて日本語点字へ寄せる。

## 位置マッピング

- translator2 は `(点字文字列, brailleToRawPos, rawToBraillePos, brailleCursorPos)` を返し、liblouis と同じ形で出力文字と原文の対応を持つ。カーソル位置や選択範囲を liblouis モードと同様に追従できる。
