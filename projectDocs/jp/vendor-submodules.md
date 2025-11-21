# ベンダーサブモジュール運用（方針・TODO）

目的: 「本家版に寄せた最小構成」を維持しつつ、JP 固有のベンダーツリー（python‑jtalk など）の取り扱いを明確化する。

## 基本方針

* SCons が必要に応じて自動的にベンダーをビルド（nmake 等）。開発者・CI ともに `scons` コマンドのみを意識すればよい。
* DLL が既に存在する場合は再ビルドをスキップ（ビルド時間の短縮）。
* オーバーレイは SCons で行う（`jtalkPrep` + `miscdepsjp`）。YAML はスクリプト呼び出しのみ（最小）。
* サブモジュールやベンダーツリーの更新は手動手順を明示し、PR では差分を最小化する。

## 実装済み

* SCons でのオンデマンドビルド（`jtalkPrep` 拡張）
  * DLL 不在時: 自動的に `nmake /f all.mak` を実行してビルド
  * TARGET_ARCH（x86/x64）に応じて `MACHINE=x64` を渡す
  * ビルド成功後、生成された DLL を payload に配置
  * DLL 存在時: 再ビルドをスキップし「build skipped」とログ出力
* 検証・ログ出力
  * `jtalkPrep` がアーキテクチャ・探索パス・ビルド有無をログ出力
  * エラー時は明確なメッセージ（MSVC 環境、サブモジュール取得の案内）

## TODO（将来）

* 純 Python 化の検討
  * nmake への依存を削減するため、ビルドロジックの純 Python 化を検討
  * 現状は nmake の使用を許容（内部実装の詳細として隠蔽）
* ベンダー更新フロー
  * サブモジュール更新時は、生成される DLL のハッシュ値を記録（検証用）
  * 別トピックブランチで実施し、差分がわかる形で PR 化

## 非目標

* YAML でのベンダービルドロジック（SCons に集約するため）
* YAML での複雑な同期・ミラー（robocopy / submodule 再展開等）

## 関連

* AGENTS.md（SCons/純 Python 優先、YAML は最小）
* projectDocs/jp/roadmap.md（目的・除外、CI の原則）

## python‑jtalk 運用

### 現在の動作

* **ビルド方法**: SCons が自動的にオンデマンドビルド
  * DLL 不在時: `jtalkPrep` が `nmake /f all.mak` を実行
  * DLL 存在時: 再ビルドスキップ（高速）
  * 開発者は `scons dist` だけを実行すればよい

* **レイアウト**
  * x64: `miscDepsJp/include/python-jtalk/x64/libopenjtalk.dll`
  * MeCab 辞書: アーキ非依存のため共通
  * libmecab.dll: payload `miscDepsJp/source/synthDrivers/jtalk/libmecab.dll` は PyPI `mecab-python3` 1.0.10 (`cp311` win_amd64 wheel) から採取した x64 DLL。MeCab と同じく GPL/LGPL/BSD（三条項）併記で、wheel の `COPYING` に明記

* **サブモジュール更新手順**
  * サブモジュール更新: `git submodule update --init --recursive`
  * 固定コミットへ: 該当ディレクトリで `git checkout <commit>`
  * DLL 削除（任意）: 既存 DLL を削除すれば次回ビルド時に自動再ビルド
  * 確認: `scons miscdepsjp` で自動ビルド＋overlay を確認
  * PR 提出: 小粒 PR でサブモジュール更新を記録

### 将来の TODO

* **純 Python 化**
  * copy_jtalk_core_files.cmd を Python スクリプト化
  * nmake の置き換えを検討（現状は内部実装の詳細として許容）

### mecab 辞書ファイルの文字コード

synthDrivers/jtalk/dic へのパッケージングについて、特に文字コードの処理を説明する。

* miscDepsJp/jptools/jtalk/libopenjtalk は、もともとサブモジュール miscDepsJp/include/libopenjtalk（nishimotz/libopenjtalk）由来の内容をワークツリー側に持ってきたコピーである。
* miscDepsJp/include/jtalk/libopenjtalk/mecab/src/Makefile.mak の CFLAGS に /D CHARSET_SHIFT_JIS が入っており、これにより mecab-dict-index.exe はソースコードが Shift_JIS（CP932）の前提でビルドされる。
* miscDepsJp\jptools\jtalk\libopenjtalk\mecab-naist-jdic には EUC-JP の mecab テキスト辞書ファイルがある。これを make_jdic.py の convert_file が UTF-8 に変換する。
* mecab-dict-index が UTF-8 ファイルを入力して UTF-8 対応バイナリ辞書をビルドする。
* パッケージングされる synthDrivers/jtalk/dic 以下のファイルはバイナリ辞書も def ファイルなども UTF-8 ベースで統一される。
* CI のビルドステージなどで `scons miscdepsjp` を実行すると、DIC_VERSION が無い（または UTF-8 記載が無い）辞書を make_jdic.py で生成し直し、その成果物をキャッシュして後続のランチャー作成／JP スモークテストに使う。
* mecab-dict-index.exe は `scons miscdepsjp` 実行時に nmake で毎回ビルド（TARGET_ARCH に応じて x64/x86）。make_jdic.py が参照するパスにも同一バイナリをコピーしているが、将来的には検索先を一本化して複製を廃止する予定。
* miscDepsJp/jptools/jtusrdic/mecab-dict-index.exe はユーザ辞書用の旧バイナリで、今後はビルド済みの exe を使う方式に移行する計画。

## 付録: 開発者の操作とログ例

### 通常のビルド（開発者が意識するコマンド）

```bash
# これだけでビルド完結（ベンダービルド・overlay・dist 作成すべて自動）
scons dist

# または
scons source user_docs launcher
```

**内部で自動実行される**（開発者は意識不要）:

1. `jtalkPrep`: DLL チェック → 無ければ nmake でビルド → payload に配置
2. `miscdepsjp`: overlay で `source/` に配置
3. `source`, `dist` などのビルド

### ログ例（scons dist 実行時）

**DLL 存在時（再ビルドスキップ）**:

```text
jtalkPrep: using TARGET_ARCH=x64
jtalkPrep: looking for vendor DLL: miscDepsJp/include/python-jtalk/x64/libopenjtalk.dll
jtalkPrep: using existing DLL (build skipped)
jtalkPrep: payload -> miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll
```

**DLL 不在時（自動ビルド）**:

```text
jtalkPrep: using TARGET_ARCH=x64
jtalkPrep: looking for vendor DLL: miscDepsJp/include/python-jtalk/x64/libopenjtalk.dll
jtalkPrep: DLL not found, attempting to build via nmake...
jtalkPrep: running nmake via vcvarsall.bat with arch=x64
[nmake の出力...]
jtalkPrep: build succeeded, DLL created at miscDepsJp/include/python-jtalk/x64/libopenjtalk.dll
jtalkPrep: payload -> miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll
```

### 手動で overlay だけ実行したい場合（通常は不要）

```bash
# overlay のみ実行（デバッグ用）
scons miscdepsjp

# x64 用
scons miscdepsjp TARGET_ARCH=x64
```
