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
  * `copy_jtalk_core_files.cmd` → `jptools/copy_jtalk_core_files.py` への置き換えは完了済み
  * nmake は現在も使用中（内部実装の詳細として許容）
  * 長期的な改善方針については `projectDocs/jp/miscdepsjp-overlay-strategy.md` の Phase 4 を参照

### mecab 辞書ファイルの文字コードと配置場所

synthDrivers/jtalk/dic へのパッケージングについて、特に文字コードの処理と複数のディレクトリの役割を説明する。

#### 辞書ファイルの配置場所と役割

ビルドプロセスでは、以下のディレクトリが使用されます：

1. **`miscDepsJp/include/libopenjtalk/mecab-naist-jdic/`** (UTF-8版)
   * **役割**: UTF-8変換済みの辞書ファイルの配置場所（Git管理対象）
   * **内容**: UTF-8 エンコーディングのテキスト辞書ファイル（`*.def`、`naist-jdic.csv`など、13個のファイル）
   * **用途**: リポジトリにコミットされているUTF-8版のソースファイル
   * **注意**: 実際にはUTF-8でエンコードされている。`THISDIR`のファイルをUTF-8に変換したものとほぼ一致（`char.def`のみバージョン管理情報行の有無で差異あり）

2. **`miscDepsJp/include/python-jtalk/libopenjtalk/mecab-naist-jdic/`** (ビルド用コピー)
   * **役割**: ビルドプロセスでコピーされた辞書ファイルの配置場所
   * **内容**: `miscDepsJp/include/libopenjtalk/mecab-naist-jdic/`からコピーされたファイル（13個のファイル）
   * **用途**: `jtalkPrep`やその他のビルドプロセスで使用される可能性がある

3. **`miscDepsJp/jptools/jtalk/libopenjtalk/mecab-naist-jdic/`** (THISDIR)
   * **役割**: ビルド用のソース辞書ファイルの配置場所（Git管理対象）
   * **内容**: EUC-JP エンコーディングのテキスト辞書ファイル（17個のファイル、追加ファイルあり）
   * **用途**: `make_jdic.py`がこのディレクトリからファイルを読み込んでUTF-8に変換
   * **注意**:
     * このディレクトリもリポジトリにコミットされている（ビルドプロセスでのコピーではない）
     * **Open JTalk由来の元のソース**（EUC-JP）。`char.def`には`$Id: char.def,v 1.2 2009-11-11 04:14:46 uratec Exp $;`というOpen JTalkのバージョン管理情報が含まれている
     * UTF-8に変換すると`miscDepsJp/include/libopenjtalk/mecab-naist-jdic/`のファイルとほぼ一致（実質的に同じ内容）

4. **`miscDepsJp/jptools/jtalk/libopenjtalk/mecab-naist-jdic/_temp/`** (TEMPDIR)
   * **役割**: 一時作業ディレクトリ
   * **内容**: UTF-8に変換されたテキスト辞書ファイル（`*.def`、`naist-jdic.csv`など）
   * **用途**: `mecab-dict-index.exe`がこのディレクトリを`-d`オプションで指定してバイナリ辞書をビルド
   * **注意**: ビルド後も残るが、再ビルド時に上書きされる

5. **`miscDepsJp/jptools/jtalk/libopenjtalk/mecab-naist-jdic/dic/`** (旧 OUTDIR)
   * **役割**: かつての出力先（現在は使わない）
   * **内容**: `make_jdic.py`はここへは出力しない（ビルドは直接 `source/synthDrivers/jtalk/dic` へ）
   * **注意**: `.def` は `_temp` にのみ存在し、ここにも `source/` にもコピーされない

6. **`source/synthDrivers/jtalk/dic/`** (dic_dst / 実際のOUTDIR)
   * **役割**: 最終的な配置先（実行時に使用される）
   * **内容**: `make_jdic.py`が直接生成するバイナリ辞書 (`sys.dic`、`unk.dic`、`char.bin`、`matrix.bin`) と `dicrc`、`DIC_VERSION`
   * **用途**: NVDA実行時にMeCabがこのディレクトリから辞書を読み込む

**注意**:

* `miscDepsJp/include/python-jtalk/dic/`は存在せず、実際には使用されていません（過去の名残）
* `jtalkSync`は辞書を `source/synthDrivers/jtalk/dic` で直接チェックし、足りなければ `make_jdic.py` を実行して同じ場所へ生成する（コピーは行わない）

#### ビルドフロー

1. **`make_jdic.py`の実行**:
   * `THISDIR`からEUC-JPファイルを読み込み
   * `TEMPDIR`にUTF-8変換して配置（`euc_files`リストの8種類の`.def`ファイルと`naist-jdic.csv`）
   * `mecab-dict-index.exe`を`TEMPDIR`を`-d`オプションで実行し、**`source/synthDrivers/jtalk/dic`に直接**バイナリ辞書を生成
   * **注意**: `.def`ファイルは`_temp`にのみ存在し、`source/`には出力されない
   * `dicrc`を`THISDIR`から`source/synthDrivers/jtalk/dic`にコピー（文字コード設定の変更は行わない）
   * `DIC_VERSION`を`source/synthDrivers/jtalk/dic`に作成（UTF-8ビルドであることを示す）

2. **`scons jtalkSync`の実行**:
   * `source/synthDrivers/jtalk/dic`を直接検査し、辞書が無い・UTF-8マークが無い場合のみ`make_jdic.py`を再実行
   * 辞書のコピー処理は行わず、「no copy needed」で完了する

#### 文字コードの統一

* `miscDepsJp/jptools/jtalk/libopenjtalk/mecab-naist-jdic/`（THISDIR）は、**Open JTalk由来の元のソース**（EUC-JP）で、リポジトリにコミットされている（Git管理対象）。`char.def`には`$Id: char.def,v 1.2 2009-11-11 04:14:46 uratec Exp $;`というOpen JTalkのバージョン管理情報が含まれている。
* `miscDepsJp/include/libopenjtalk/mecab-naist-jdic/`は、もともとサブモジュール（nishimotz/libopenjtalk）由来の内容で、PR #582 で subtree merge によりメインリポジトリに統合済み。このディレクトリに辞書ファイルがコミットされている（Git管理対象）。**実際にはUTF-8でエンコードされている**。`THISDIR`のファイルをUTF-8に変換したものとほぼ一致（実質的に同じ内容）。
* `make_jdic.py`は`THISDIR`（EUC-JP）からファイルを読み込み、UTF-8に変換してビルドする。
* `miscDepsJp/include/libopenjtalk/mecab/src/Makefile.mak`の CFLAGS に /D CHARSET_SHIFT_JIS が入っており、これにより mecab-dict-index.exe はソースコードが Shift_JIS（CP932）の前提でビルドされる。
* `miscDepsJp/jptools/jtalk/libopenjtalk/mecab-naist-jdic/`には EUC-JP の mecab テキスト辞書ファイルがある。これを make_jdic.py の convert_file が UTF-8 に変換する。
* mecab-dict-index が UTF-8 ファイルを入力して UTF-8 対応バイナリ辞書をビルドする。
* パッケージングされる synthDrivers/jtalk/dic 以下のファイルはバイナリ辞書も def ファイルなども UTF-8 ベースで統一される。
* CI のビルドステージなどで `scons jtalkSync` を実行すると、DIC_VERSION が無い（または UTF-8 記載が無い）場合は辞書を make_jdic.py で生成する。CI では後続のランチャー作成／JP スモークテストはビルドステージのキャッシュを利用する。
* miscDepsJp/jptools/jtusrdic/mecab-dict-index.exe はいずれ廃止して、ビルドし直したバイナリを使うようにする予定。

#### mecab-dict-index.exe の辞書フォーマット仕様（仮説）

これは暫定的なメモで、さらに確認が必要。

`mecab-dict-index.exe`は、システム辞書とユーザー辞書で異なるCSVフォーマットを期待します：

**システム辞書（NAIST-JDIC形式）**:

* **フィールド数**: 13フィールド（カンマ区切り）
* **形式**: `表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音`
* **例**: `naist-jdic.csv`（`make_jdic.py`でビルドされるシステム辞書）

**ユーザー辞書（簡易形式）**:

* **フィールド数**: 5フィールド（カンマ区切り）
* **形式**: `表層形,左文脈ID,右文脈ID,コスト,品詞情報（カンマ区切り）`
* **実装**: `miscDepsJp/include/libopenjtalk/mecab/src/dictionary.cpp`の215-216行目で`tokenizeCSV(line.get(), col, 5)`と`CHECK_DIE(n == 5)`により5フィールド形式を強制
* **例**: `jtusr.csv`（ユーザー辞書ソース）は5フィールド形式である必要がある

**注意事項**:

* ユーザー辞書のCSVファイルがNAIST-JDIC形式（13フィールド）の場合、`mecab-dict-index.exe`は`dictionary.cpp:216`で`format error`を出力し、ビルドに失敗する
* ユーザー辞書をビルドする際は、`-u`オプションで指定するCSVファイルが5フィールド形式であることを確認する必要がある
* システム辞書の`naist-jdic.csv`は13フィールド形式だが、`mecab-dict-index.exe`は`-d`オプションでシステム辞書をビルドする際は13フィールド形式を正しく処理する（`dictionary.cpp`の実装が異なる処理パスを使用）

**参考実装**:

* `miscDepsJp/include/libopenjtalk/mecab/src/dictionary.cpp:215-216`: ユーザー辞書ビルド時の5フィールドチェック
* `miscDepsJp/jptools/userdicBuilder.cmd`: ユーザー辞書ビルドコマンド例（`-u`オプション使用）
* `miscDepsJp/jptools/jtusrdic/__init__.py:72-74`: ユーザー辞書ビルド処理（`-u`オプション使用）

#### 過去の実装との比較と現状の課題

**過去の実装（`.cmd`ファイルとMakefile）**:

* `all-install.cmd`: `copy libopenjtalk\mecab-naist-jdic\dic\*` で全ファイルをコピー
* `Makefile.mak`: 明示的に8つのファイルをコピー（`char.bin`、`matrix.bin`、`sys.dic`、`unk.dic`、`left-id.def`、`right-id.def`、`rewrite.def`、`pos-id.def`）

**現在の実装**:

* `make_jdic.py`: `euc_files`（8種類の`.def`ファイル）を`TEMPDIR`にUTF-8変換して配置し、`mecab-dict-index.exe`が`TEMPDIR`から読み込んでバイナリ辞書を生成するが、`.def`ファイル自体は`OUTDIR`にコピーされない
* `jptools/scons_jp.py`: `dic_files`リストに列挙された10個のファイルのみをコピー

**実装上の注意点**:

* `OUTDIR`には`mecab-dict-index.exe`が生成したバイナリ辞書ファイル（`sys.dic`、`unk.dic`、`char.bin`、`matrix.bin`）と、`make_jdic.py`がコピーした`dicrc`と`DIC_VERSION`のみが存在する
* `.def`ファイル（`char.def`、`feature.def`、`matrix.def`、`unk.def`など）は`OUTDIR`に存在しないため、`dic_files`リストにも含まれていない
* 過去の`all-install.cmd`では`dic\*`で全ファイルをコピーしていたが、実際には`OUTDIR`に`.def`ファイルが存在しない場合はコピーされなかった可能性がある

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
