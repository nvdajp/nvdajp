# ベンダーサブモジュール運用（方針・TODO）

## このブランチの対象

* **アーキテクチャ**: x86（32bit）
* **Python バージョン**: 3.11
* **ビルド環境**: Windows 10/11

## 目的

「本家版に寄せた最小構成」を維持しつつ、JP 固有のベンダーツリー（python‑jtalk など）の取り扱いを明確化する。

## 基本方針

* SCons が必要に応じて自動的にベンダーをビルド（nmake 等）。開発者・CI ともに `scons` コマンドのみを意識すればよい。
* DLL が既に存在する場合は再ビルドをスキップ（ビルド時間の短縮）。
* オーバーレイは SCons で行う（`jtalkPrep` + `miscdepsjp`）。YAML はスクリプト呼び出しのみ（最小）。
* ベンダーツリーの更新は通常のGit操作で行い、PR では差分を最小化する。

## 実装済み

* SCons でのオンデマンドビルド（`jtalkPrep` 拡張）
  * DLL 不在時: mecab/src の `Makefile.mak` を `nmake /f Makefile.mak MACHINE=x86` でビルド（このブランチは x86）
  * ビルド成功後、生成された DLL を payload に配置
  * DLL 存在時: 再ビルドをスキップし「build skipped」とログ出力
* 検証・ログ出力
  * `jtalkPrep` がアーキテクチャ・探索パス・ビルド有無をログ出力
  * エラー時は明確なメッセージ（MSVC 環境の案内）

## TODO（将来）

* 純 Python 化の検討
  * nmake への依存を削減するため、ビルドロジックの純 Python 化を検討
  * 現状は nmake の使用を許容（内部実装の詳細として隠蔽）
* ベンダー更新フロー
  * ベンダーツリー更新時は、生成される DLL のハッシュ値を記録（検証用）
  * 別トピックブランチで実施し、差分がわかる形で PR 化

**現状の問題点と長期的な改善方針**については、`projectDocs/jp/miscdepsjp-overlay-strategy.md` を参照してください。

### 既知の課題: *.py.txt の残存

* `miscDepsJp/source/synthDrivers/jtalk/` に `jtalkCore.py.txt` / `mecab.py.txt` / `text2mecab.py.txt` などのコピーが残存
* 現行ビルドは `miscDepsJp/include/python-jtalk/...` の `.py` 本体を参照しており `.py.txt` は未使用
* 方針: 参照がないことを確認のうえ `.py.txt` を削除（overlay 簡素化の一環）。削除後は x86 smoke test で影響確認

## 非目標

* YAML でのベンダービルドロジック（SCons に集約するため）
* YAML での複雑な同期・ミラー（robocopy 等）

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
  * x86: `miscDepsJp/include/python-jtalk/x86/libopenjtalk.dll`（Phase 1.2で統一済み）
  * x64: `miscDepsJp/include/python-jtalk/x64/libopenjtalk.dll`（将来のリファクタリング予定、別ブランチ）
  * MeCab 辞書: アーキ非依存のため共通
  * libmecab.dll: Phase 1.3でソースビルド化（`miscDepsJp/include/libopenjtalk/mecab/src/Makefile.mak` と vendor側 `miscDepsJp/include/python-jtalk/libopenjtalk/mecab/src/Makefile.mak` でビルド）。リポジトリに長く含まれていたバイナリDLLを削除し、CFLAGSを静的/動的で分離してビルドする方式に移行。MeCab と同じく GPL/LGPL/BSD（三条項）併記。

**注意**: `miscDepsJp` フォルダ全体は PR #492 でメインリポジトリに統合され、`miscDepsJp/include/*` 配下のベンダーツリー（python-jtalk等）は PR #582 で git subtree merge によりメインリポジトリに統合されています。サブモジュールの更新操作（`git submodule update`）は不要です。ベンダーツリーの更新が必要な場合は、通常のGit操作（`git pull`、`git merge`等）で対応します。

### 将来の TODO

* **純 Python 化**
  * copy_jtalk_core_files.cmd → `jptools/copy_jtalk_core_files.py` への置き換えは完了済み
  * nmake の置き換えを検討（現状は内部実装の詳細として許容）

### mecab 辞書ファイルの文字コード

synthDrivers/jtalk/dic へのパッケージングについて、特に文字コードの処理を説明する。

* miscDepsJp/jptools/jtalk/libopenjtalk は、もともとサブモジュール miscDepsJp/include/libopenjtalk（nishimotz/libopenjtalk）由来の内容をワークツリー側に持ってきたコピーである（PR #582 で subtree merge によりメインリポジトリに統合済み）。
* miscDepsJp/include/libopenjtalk/mecab/src/Makefile.mak の CFLAGS に /D CHARSET_SHIFT_JIS が入っており、これにより mecab-dict-index.exe はソースコードが Shift_JIS（CP932）の前提でビルドされる。
* miscDepsJp\jptools\jtalk\libopenjtalk\mecab-naist-jdic には EUC-JP の mecab テキスト辞書ファイルがある。これを make_jdic.py の convert_file が UTF-8 に変換する。
* mecab-dict-index が UTF-8 ファイルを入力して UTF-8 対応バイナリ辞書をビルドする。
* パッケージングされる synthDrivers/jtalk/dic 以下のファイルはバイナリ辞書も def ファイルなども UTF-8 ベースで統一される。
* CI のビルドステージなどで `scons miscdepsjp` を実行すると、DIC_VERSION が無い（または UTF-8 記載が無い）場合は辞書を make_jdic.py で生成する。CI では後続のランチャー作成／JP スモークテストはビルドステージのキャッシュを利用する。
* miscDepsJp/jptools/jtusrdic/mecab-dict-index.exe はいずれ廃止して、ビルドし直したバイナリを使うようにする予定。

## 付録: 開発者の操作とログ例

### 通常のビルド（開発者が意識するコマンド）

```powershell
# これだけでビルド完結（ベンダービルド・overlay・dist 作成すべて自動）
scons.bat dist

# または
scons.bat source user_docs launcher
```

**内部で自動実行される**（開発者は意識不要）:

1. `jtalkPrep`: DLL チェック → 無ければ nmake でビルド → payload に配置
2. `miscdepsjp`: overlay で `source/` に配置
3. `source`, `dist` などのビルド

### ログ例（scons dist 実行時）

**DLL 存在時（再ビルドスキップ）**:

```text
jtalkPrep: using TARGET_ARCH=x86
jtalkPrep: looking for vendor DLL: miscDepsJp/include/python-jtalk/x86/libopenjtalk.dll
jtalkPrep: using existing DLL (build skipped)
jtalkPrep: payload -> miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll
```

**DLL 不在時（自動ビルド）**:

```text
jtalkPrep: using TARGET_ARCH=x86
jtalkPrep: looking for vendor DLL: miscDepsJp/include/python-jtalk/x86/libopenjtalk.dll
jtalkPrep: DLL not found, attempting to build via nmake...
jtalkPrep: running nmake via vcvarsall.bat with arch=x86
[nmake の出力...]
jtalkPrep: build succeeded, DLL created at miscDepsJp/include/python-jtalk/x86/libopenjtalk.dll
jtalkPrep: payload -> miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll
```

**注**: Phase 1.2で、x86 DLL も `miscDepsJp/include/python-jtalk/x86/libopenjtalk.dll` に統一されました。既存のDLLが古い場所にある場合は、自動的に新しい場所に移動されます。

### 手動で overlay だけ実行したい場合（通常は不要）

```powershell
# overlay のみ実行（デバッグ用）
scons miscdepsjp

# このブランチは x86 がデフォルト
# x64 が必要な場合は TARGET_ARCH=x64 を指定（別ブランチ）
```
