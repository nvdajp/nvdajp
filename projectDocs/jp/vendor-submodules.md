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
* **オーバーレイ処理は廃止済み**（Phase 2 完了、2025-12-12）。日本語版固有ファイルは `source/` に直接配置。ビルドプロセスは `jtalkPrep` → `jtalkSync` → `source` の依存関係に簡素化。
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

* ベンダー更新フロー
  * ベンダーツリー更新時は、生成される DLL のハッシュ値を記録（検証用）
  * 別トピックブランチで実施し、差分がわかる形で PR 化

**現状の問題点と長期的な改善方針**（純 Python 化、nmake 依存の削減、パス解決の共通化など）については、`projectDocs/jp/miscdepsjp-overlay-strategy.md` の「改善計画」セクション（Phase 3-4）を参照してください。

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
  * x86 DLL: `miscDepsJp/include/python-jtalk/x86/libopenjtalk.dll`
  * MeCab 辞書: `miscDepsJp/include/python-jtalk/dic/`（アーキテクチャ非依存）
  * libmecab.dll: ソースビルド化済み（`miscDepsJp/include/libopenjtalk/mecab/src/Makefile.mak` と `miscDepsJp/include/python-jtalk/libopenjtalk/mecab/src/Makefile.mak` でビルド）。CFLAGSを静的/動的で分離してビルドする方式。MeCab と同じく GPL/LGPL/BSD（三条項）併記。
  * ビルド成果物の配置: DLL と辞書ファイルは `source/synthDrivers/jtalk` に直接配置される

**注意**: `miscDepsJp` およびその配下のベンダーツリーは、すべてメインリポジトリに統合されています。サブモジュールではないため、`git submodule update` は不要です。ベンダーツリーの更新が必要な場合は、通常のGit操作（`git pull`、`git merge`等）で対応します。

### 現在の実装状況

* **純 Python 化の進捗**
  * `copy_jtalk_core_files.py` は Phase 1完了後、削除済み（ファイルは `source/synthDrivers/jtalk` に直接配置されているため不要）
  * nmake は現在も使用中（内部実装の詳細として許容）
  * 長期的な改善方針については `projectDocs/jp/miscdepsjp-overlay-strategy.md` の Phase 4 を参照

### mecab 辞書ファイルの文字コード

synthDrivers/jtalk/dic へのパッケージングについて、特に文字コードの処理を説明する。

* miscDepsJp/jptools/jtalk/libopenjtalk は、もともとサブモジュール miscDepsJp/include/libopenjtalk（nishimotz/libopenjtalk）由来の内容をワークツリー側に持ってきたコピーである（PR #582 で subtree merge によりメインリポジトリに統合済み）。
* miscDepsJp/include/libopenjtalk/mecab/src/Makefile.mak の CFLAGS に /D CHARSET_SHIFT_JIS が入っており、これにより mecab-dict-index.exe はソースコードが Shift_JIS（CP932）の前提でビルドされる。
* miscDepsJp\jptools\jtalk\libopenjtalk\mecab-naist-jdic には EUC-JP の mecab テキスト辞書ファイルがある。これを make_jdic.py の convert_file が UTF-8 に変換する。
* mecab-dict-index が UTF-8 ファイルを入力して UTF-8 対応バイナリ辞書をビルドする。
* パッケージングされる synthDrivers/jtalk/dic 以下のファイルはバイナリ辞書も def ファイルなども UTF-8 ベースで統一される。
* CI のビルドステージなどで `scons jtalkSync` を実行すると、DIC_VERSION が無い（または UTF-8 記載が無い）場合は辞書を make_jdic.py で生成する。CI では後続のランチャー作成／JP スモークテストはビルドステージのキャッシュを利用する。
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

1. `jtalkPrep`: DLL チェック → 無ければ nmake でビルド → `source/synthDrivers/jtalk` に配置
2. `jtalkSync`: 辞書ファイルのビルドとコピー → `source/synthDrivers/jtalk` に配置
3. `source`, `dist` などのビルド

### ログ例（scons dist 実行時）

**DLL 存在時（再ビルドスキップ）**:

```text
jtalkPrep: using TARGET_ARCH=x86
jtalkPrep: looking for vendor DLL: miscDepsJp/include/python-jtalk/x86/libopenjtalk.dll
jtalkPrep: using existing DLL (build skipped)
jtalkPrep: payload -> source/synthDrivers/jtalk/libopenjtalk.dll
```

**DLL 不在時（自動ビルド）**:

```text
jtalkPrep: using TARGET_ARCH=x86
jtalkPrep: looking for vendor DLL: miscDepsJp/include/python-jtalk/x86/libopenjtalk.dll
jtalkPrep: DLL not found, attempting to build via nmake...
jtalkPrep: running nmake via vcvarsall.bat with arch=x86
[nmake の出力...]
jtalkPrep: build succeeded, DLL created at miscDepsJp/include/python-jtalk/x86/libopenjtalk.dll
jtalkPrep: payload -> source/synthDrivers/jtalk/libopenjtalk.dll
```

**注**: Phase 1.2で、x86 DLL も `miscDepsJp/include/python-jtalk/x86/libopenjtalk.dll` に統一されました。既存のDLLが古い場所にある場合は、自動的に新しい場所に移動されます。

### 手動で JTalk 関連のビルドだけ実行したい場合（通常は不要）

```powershell
# JTalk DLL のビルドと配置のみ実行
scons jtalkPrep

# 辞書ファイルのビルドとコピーのみ実行
scons jtalkSync

# このブランチは x86 がデフォルト
# x64 が必要な場合は TARGET_ARCH=x64 を指定（別ブランチ）
```

### クリーンアップ（scons -c）

`jtalkSync` で生成されるファイルは、`scons -c` で自動的に削除されます：

```powershell
# すべてのビルド成果物をクリーンアップ
scons -c

# jtalkSync 関連のファイルのみクリーンアップ
scons -c jtalkSync
```

**削除されるファイル**:
* `miscDepsJp/include/python-jtalk/libopenjtalk/mecab/src/mecab-dict-index.exe`
* `source/synthDrivers/jtalk/libmecab.dll`
* `source/synthDrivers/jtalk/libopenjtalk.dll`

**注意**: ファイルがロックされている場合（NVDA やデバッガーが実行中など）、削除に失敗することがあります。その場合は、該当プロセスを終了してから再実行してください。
