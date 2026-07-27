# ベンダーツリー詳細メモ（辞書・文字コード）

この文書は、`projectDocs/jp/vendor-submodules.md` から分離した背景説明を保管するアーカイブである。
現行の運用方針や手順は正本を参照すること。

## 目的

* MeCab 辞書ビルドで扱う文字コードの背景を残す。
* 辞書生成時に使うディレクトリの役割を残す。
* `jtalkSync` と `make_jdic.py` の関係を残す。

## 文字コード（EUC-JP -> UTF-8）

* 元の NAIST 辞書や関連入力は EUC-JP 前提の構成が多い。
* 日本語版の現在フローでは、`jtalkSync` が辞書状態を検査し、必要時に `make_jdic.py` で再生成する。
* 再生成後は UTF-8 マーカー（`DIC_VERSION`）を基準に辞書の整合性を判定する。
* `make_jdic.py` は `DIC_VERSION` に `"nvdajp-jtalk-dic (utf-8)"` を書き込む。この "nvdajp" マーカーにより make_jdic 由来であることを示す（nmake は DIC_VERSION を作らない。2026-02 追加。詳細は `tab-character-analysis.md` §nmake 辞書の意図せぬ使用）。
* これにより、文字コード不一致をビルド時に自動検出し、必要時のみ再生成できる。

## ディレクトリ役割（THISDIR / TEMPDIR / OUTDIR の文脈）

`make_jdic.py` および関連スクリプトでは、次の役割分離で辞書を組み立てる。

* `THISDIR`:
  * スクリプト基準ディレクトリ。
  * 入力 CSV や補助辞書、生成スクリプトの相対参照基点。
* `TEMPDIR`（概念上の一時領域）:
  * 変換途中ファイルや中間生成物を置く領域。
  * 失敗時の切り分けと再実行性を担保する。
* `OUTDIR`:
  * `char.bin` / `sys.dic` などの最終生成物を置く出力先。
  * `jtalkSync` がこの成果物を検査し、`source/synthDrivers/jtalk/dic` へ同期する。

※ 実装上の具体パスは `miscDepsJp/jptools/jtalk/make_jdic.py` と `jptools/scons_jp.py` を参照すること。

## 実ビルドフローとの対応

ビルド依存は次である。

```text
jtalkPrep -> jtalkSync -> source
```

* `jtalkPrep`:
  * 必要な DLL（`libopenjtalk.dll` / `libmecab.dll`）を準備する。
* `jtalkSync`:
  * 既存辞書の状態を検査する。
  * UTF-8 条件を満たさない場合のみ `make_jdic.py` を起動して再生成する。
  * 生成結果を `source/synthDrivers/jtalk` へ反映する。
* `source`:
  * 反映済み成果物を含めて NVDA 本体側を構成する。

## 参照

* 正本: `projectDocs/jp/vendor-submodules.md`
* 実装: `jptools/scons_jp.py`
* 実装: `miscDepsJp/jptools/jtalk/make_jdic.py`
