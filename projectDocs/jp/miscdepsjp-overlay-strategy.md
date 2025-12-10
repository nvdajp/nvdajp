# miscDepsJp と JP overlay の現状と長期的な方針

## 概要

このドキュメントは、`miscDepsJp` フォルダと JP overlay 処理の現状の問題点と、長期的な改善方針を整理したものです。

### 基本方針（roadmap.mdと整合）

**roadmap.mdの基本方針に従う**:

- **本家版との差分を最小化**: 本家版の設計思想（`include/`と`miscDeps/include/`の使い分け）に従い、独自の仕組み（overlay処理、`miscDepsJp/source/`）を段階的に廃止
- **小さなPR単位で進める**: 各PRで必ず全テストが通過することを確認
- **段階的な検証を必須とする**: 各段階でビルド・型チェック・単体テスト・システムテストを通過確認
- **完了の定義を明確化**: テストが全て通過し、CIが安定して緑になるまで「完了」としない
- **問題が発生したら即座に停止**: テスト失敗や不安定な動作が見られたら、次の段階に進まずに問題を解決
- **安定版リリースの維持**: 2025.3.xjp安定版のリリース継続を維持し、リリースに影響を与える変更は段階的に実施

**改善の基本方針**: コピー処理を「統合」するだけでなく、積極的に「削減」し、ビルドプロセスを単純化することを目指します。本家版の設計思想に従い、`miscDepsJp`フォルダを段階的に廃止し、本家版と整合する構成に移行します。

**Pythonコードの配置方針**: Pythonコードに関しては、現状のJP overlayが完了した状態のファイル位置（`source/`配下）に必要なファイルが最初から置かれている状態を理想とする。これにより、overlay処理という中間段階を廃止し、本家版の設計思想（`source/`に直接配置）に整合する。

**重要**: これらの改善は、将来的な x64 移行をスムーズにするためにも重要です。複雑な構造を早い段階で簡素化することで、x64 対応時の作業量を大幅に削減できます。詳細は「改善計画」セクションを参照してください。

## 現状の構造

### リポジトリのフォルダ構成

日本語版リポジトリのルートには、以下の2つの主要なフォルダがあります：

```text
リポジトリルート/
├── source/           # 本家版（upstream）のソースコード
│   └── synthDrivers/
│       └── jtalk/    # 本家版の JTalk ドライバー（存在する場合）
└── miscDepsJp/       # 日本語版固有のフォルダ
    ├── include/      # ベンダーツリー
    ├── source/       # 日本語版固有のソースファイル（overlay のソース）
    └── jptools/      # テストとビルドツール
```

### 本家版の `source` フォルダ

- **役割**: 本家版（nvaccess/nvda）から取り込んだソースコードを保持
- **管理方法**: 通常の Git 操作で本家版からマージ・更新
- **内容**: NVDA 本体のソースコード（英語版のドライバー、コア機能など）

### miscDepsJp フォルダの構成

```text
miscDepsJp/
├── include/          # ベンダーツリー（python-jtalk、htsengineapi、libopenjtalk、libkuraji など）
│   └── python-jtalk/ # JTalk コアファイル（jtalkCore.py、mecab.py、text2mecab.py など）
├── source/           # 日本語版固有のソースファイル（overlay のソース）
│   └── synthDrivers/
│       └── jtalk/    # JTalk ドライバーと点訳エンジン
└── jptools/          # テストとビルドツール
```

### miscDepsJp の管理方法

**注**: `miscDepsJp`フォルダの管理方法（PR #492、PR #582での統合など）の詳細は、`projectDocs/jp/vendor-submodules.md`を参照してください。

**要点**: `miscDepsJp`フォルダ全体はPR #492でメインリポジトリに統合され、`miscDepsJp/include/*`配下のベンダーツリーはPR #582でgit subtree mergeによりメインリポジトリに統合されています。サブモジュールの更新操作（`git submodule update`）は不要です。

### `miscDepsJp/source` と本家版の `source/` の関係

- **`miscDepsJp/source`**: 日本語版固有のソースファイルを保持（overlay のソース）
- **本家版の `source/`**: 本家版のソースコードを保持（overlay のターゲット）
- **overlay 処理**: `miscDepsJp/source` の内容を本家版の `source/` にコピーして上書き
  - 同じパスのファイルがある場合、本家版のファイルが日本語版のファイルで上書きされる
  - 本家版に存在しないパスのファイルは新規に追加される
  - 本家版のファイルは Git で管理されているため、`git checkout` で復元可能

### 現在のコピー処理

**注**: ビルドプロセスの概要は`projectDocs/jp/vendor-submodules.md`を参照してください。以下は詳細なコピー処理の説明です。

JP overlay 処理では、以下の複数のコピー処理が実行されます：

1. **`setup_miscdeps_overlay.py`** (`miscdepsjp` エイリアス内)
   - `miscDepsJp/source` → `source/`（本家版の `source` フォルダ）への全体コピー
   - これにより、`miscDepsJp/source/synthDrivers/jtalk` の内容が `source/synthDrivers/jtalk` に到達
   - **注意**: 本家版の `source/` に既存のファイルがある場合、日本語版のファイルで上書きされる

2. **`_copy_jtalk_core_files()`** (`miscdepsjp` エイリアス内)
   - `miscDepsJp/include/python-jtalk` → `source/synthDrivers/jtalk`（本家版の `source` フォルダ）への直接コピー
   - コピーされるファイル: `jtalkCore.py`, `mecab.py`, `text2mecab.py`
   - **注意**: これは本家版の `source/synthDrivers/jtalk` への直接コピー（overlay を経由しない）

3. **`jtalkPrep` エイリアス**
   - DLL のビルド（必要時）
   - `htsengineapi` と `libopenjtalk` を `miscDepsJp/include/python-jtalk` にコピー
   - DLL を `miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll` にコピー
   - この DLL は後続の overlay 処理で `source/synthDrivers/jtalk/libopenjtalk.dll` に到達

4. **`jtalkSync` エイリアス**
   - 辞書ファイルのビルドとコピー
     - `miscDepsJp/include/python-jtalk/dic` → `miscDepsJp/source/synthDrivers/jtalk/dic`
   - コアファイル（DLL、Python ファイル）を `miscDepsJp/include/python-jtalk` → `miscDepsJp/source/synthDrivers/jtalk` にコピー
     - コピーされるファイル: `libmecab.dll`, `libopenjtalk.dll`, `mecab.py`, `text2mecab.py`, `jtalkCore.py`
   - これらのファイルは後続の overlay 処理で `source/synthDrivers/jtalk` に到達

### 本家版の `source/` への overlay の影響

**基本的な方針**: overlay で上書きされる本家版のソースファイルは基本的にありません。`miscDepsJp/source` には主に日本語版固有のファイルが含まれており、本家版の `source/` に存在しないパスに配置されています。

**`miscDepsJp/source` の主な内容**:

- **`synthDrivers/jtalk/`**: 日本語版固有の JTalk ドライバーと点訳エンジン（本家版には存在しない）
- **`synthDrivers/nvdajp_jtalk.py`**: 日本語版固有の合成音声ドライバー（本家版には存在しない）
- **`brailleDisplayDrivers/DirectBM.dll`**: 日本語版固有の点字ディスプレイドライバー（本家版には存在しない）
- **`images/`**: 日本語版固有の画像ファイル（本家版には存在しない）
- **`typelibs/`**: 過去には `ia2.tlb` を overlay していたが、現在は本家版が直接配置する運用に変更済み（`projectDocs/jp/merge-issues-beta-2025-11.md` 参照）

**overlay 処理の動作**:

- **新規追加されるファイル**: `miscDepsJp/source` にのみ存在するファイルは、本家版の `source/` に新規追加される
- **上書きされるファイル**: 理論的には同じパスのファイルがある場合に上書きされるが、実際には `miscDepsJp/source` に本家版のソースファイルと重複するパスは基本的に存在しない
- **影響を受けないファイル**: `miscDepsJp/source` に存在しない本家版のファイルはそのまま残る

**注意**: 過去には `typelibs/ia2.tlb` を overlay していたが、本家版との差分を最小化する方針に基づき、本家版と同じ配置（`source/typelibs/ia2.tlb`）に変更されました。

**復元方法**: 万が一 overlay で上書きされたファイルを本家版の状態に戻す必要がある場合は、`git checkout -- source/<path>` を使用します。

### `source/synthDrivers/jtalk` への到達経路

本家版の `source/synthDrivers/jtalk` ディレクトリへのファイル到達には、以下の2つの経路があります：

1. **直接コピー経路** (`_copy_jtalk_core_files()`)
   - `miscDepsJp/include/python-jtalk` → `source/synthDrivers/jtalk`
   - 対象ファイル: `jtalkCore.py`, `mecab.py`, `text2mecab.py`
   - overlay を経由しない直接コピー

2. **間接コピー経路** (`jtalkSync` → `setup_miscdeps_overlay.py`)
   - `miscDepsJp/include/python-jtalk` → `miscDepsJp/source/synthDrivers/jtalk` (jtalkSync)
   - `miscDepsJp/source` → `source/`（本家版の `source` フォルダ）(overlay)
   - 対象ファイル: 辞書ファイル（`dic/` 配下）、DLL、Python ファイル（`jtalkCore.py`, `mecab.py`, `text2mecab.py` を含む）

**問題点**: `jtalkCore.py`, `mecab.py`, `text2mecab.py` は両方の経路でコピーされるため、重複が発生しています。

### 依存関係

```text
source → miscdepsjp → jtalkSync → jtalkPrep
```

## 現状の問題点

### 1. 複数のコピー処理が存在し、混乱を招く

- **問題**: 同じファイルが複数の場所からコピーされる
  - `_copy_jtalk_core_files()`: `miscDepsJp/include/python-jtalk` → `source/synthDrivers/jtalk`
  - `jtalkSync`: `miscDepsJp/include/python-jtalk` → `miscDepsJp/source/synthDrivers/jtalk`
  - 最終的に `miscDepsJp/source` → `source/` への overlay で `source/` に到達

- **影響**:
  - どの処理がどのファイルをコピーするか理解が困難
  - デバッグ時に原因特定が難しい
  - 新しい開発者が理解するのに時間がかかる

### 2. コピー処理の重複

- **問題**: `_copy_jtalk_core_files()` と `jtalkSync` でコアファイルが重複コピー
  - `jtalkCore.py`, `mecab.py`, `text2mecab.py` が両方でコピーされる
  - `_copy_jtalk_core_files()`: `miscDepsJp/include/python-jtalk` → `source/synthDrivers/jtalk` に直接コピー
  - `jtalkSync`: `miscDepsJp/include/python-jtalk` → `miscDepsJp/source/synthDrivers/jtalk` にコピーし、その後 overlay で `source/synthDrivers/jtalk` に到達

- **影響**:
  - 無駄な処理が発生
  - 保守性の低下
  - どちらの経路でファイルが到達したか理解が困難

### 3. 複雑な依存関係

- **問題**: `miscdepsjp` → `jtalkSync` → `jtalkPrep` の依存チェーンが複雑
  - 各エイリアスが異なる目的を持ち、相互に依存

- **影響**:
  - ビルドプロセスの理解が困難
  - エラー時の原因特定が難しい

### 4. 古いスクリプトの残存

- **現状**: `copy_jtalk_core_files.cmd` は `jptools/copy_jtalk_core_files.py` へ置き換え済み（`uv run python`／`python`で呼び出し）
- **影響**:
  - Python 化方針に整合
  - 引用符エスケープ問題を回避

### 5. miscDepsJp フォルダ構造への依存

- **問題**: 多くのスクリプトが `miscDepsJp` フォルダ構造に依存
  - `jtalkRunner.py`: `miscDepsJp/include/python-jtalk` から `repo_root` を推論
  - `runJpSmokeTests.ps1`: `miscDepsJp\source\synthDrivers\jtalk\libopenjtalk.dll` へのハードコード

- **影響**:
  - フォルダ構造の変更に弱い
  - 長期的な保守性の低下

### 6. patch.exe への依存

- **問題**: ビルドプロセスで `patch.exe`（通常は Git for Windows に含まれる）が必要
  - `miscDepsJp/include/python-jtalk/lib/Makefile.mak`: `HTS_gstream_ex.c` と `HTS_engine_ex.c` にパッチを適用
  - `miscDepsJp/include/python-jtalk/all.mak`: `jpcommon_label.c` にパッチを適用
  - `jptools/devbuild.cmd` と `jptools/certBuild2023.cmd`: `patch -v` で存在チェック

- **影響**:
  - 外部ツール（Git for Windows）への依存が発生
  - ビルド環境のセットアップが複雑化
  - CI環境での依存関係管理が煩雑
  - パッチファイルの管理と適用処理が分散

- **パッチ適用箇所**:
  1. `HTS_gstream_ex.patch`: `htsengineapi/lib/HTS_gstream.c` をコピーした `HTS_gstream_ex.c` に適用（関数シグネチャの拡張）
  2. `HTS_engine_ex.patch`: `htsengineapi/lib/HTS_engine.c` をコピーした `HTS_engine_ex.c` に適用（関数シグネチャの拡張）
  3. `jpcommon_label.patch`: `libopenjtalk/jpcommon/jpcommon_label.c` に適用（日本語版固有の変更）

## 改善計画

**重要**: これらの改善は、将来的な x64 移行をスムーズにするためにも重要です。複雑なコピー処理やフォルダ構造への依存が残っていると、x64 対応時にさらに複雑になり、作業量が増加する可能性があります。早い段階で構造を簡素化することで、x64 移行時の作業を大幅に削減できます。

### 現状の日本語版独自ファイルの構成

**overlay処理後の最終的な配置場所（`source/`配下）**:

#### Pythonコード

1. **JTalkドライバー本体**（`source/synthDrivers/jtalk/`）:
   - `__init__.py`, `jtalkDriver.py`, `jtalkDir.py`, `jtalkPrepare.py`
   - `_bgthread.py`, `_nvdajp_espeak.py`, `_nvdajp_spellchar.py`, `_nvdajp_unicode.py`
   - `roma2kana.py`, `translator1.py`, `translator2.py`
   - **配置元**: `miscDepsJp/source/synthDrivers/jtalk/`（overlay処理でコピー）

2. **JTalkコアファイル**（`source/synthDrivers/jtalk/`）:
   - `jtalkCore.py`, `mecab.py`, `text2mecab.py`
   - **配置元**: `miscDepsJp/include/python-jtalk/`（`_copy_jtalk_core_files()`で直接コピー）

3. **JTalkドライバーエントリーポイント**（`source/synthDrivers/`）:
   - `nvdajp_jtalk.py`
   - **配置元**: `miscDepsJp/source/synthDrivers/`（overlay処理でコピー）

4. **点字翻訳ヘルパー**（`source/`）:
   - `louisHelper.py`（本家版に存在、日本語版で条件付きimportを追加）
   - **配置元**: 本家版の`source/louisHelper.py`に`# nvdajp`マーカーで条件付きimportを追加

#### DLLファイル

1. **libopenjtalk.dll**（`source/synthDrivers/jtalk/`）:
   - **配置元**: `miscDepsJp/include/python-jtalk/x86/libopenjtalk.dll` または `x64/libopenjtalk.dll`
   - **ビルド**: 必要時、`miscDepsJp/include/python-jtalk/all.mak`でnmakeビルド
   - **処理**: `jtalkPrep`エイリアスで`miscDepsJp/source/synthDrivers/jtalk/`にコピー後、overlay処理で`source/synthDrivers/jtalk/`に到達

2. **libmecab.dll**（`source/synthDrivers/jtalk/`）:
   - **配置元**: `miscDepsJp/include/python-jtalk/x86/libmecab.dll` または `x64/libmecab.dll`
   - **ビルド**: 必要時、`miscDepsJp/include/libopenjtalk/mecab/src/Makefile.mak`でnmakeビルド
   - **処理**: `jtalkSync`エイリアスで直接`source/synthDrivers/jtalk/`にコピー

3. **DirectBM.dll**（`source/brailleDisplayDrivers/`）:
   - **配置元**: `miscDepsJp/source/brailleDisplayDrivers/`（overlay処理でコピー）

#### 辞書などのデータファイル

1. **MeCab辞書**（`source/synthDrivers/jtalk/dic/`）:
   - `char.bin`, `matrix.bin`, `pos-id.def`, `left-id.def`, `right-id.def`, `rewrite.def`, `dicrc`
   - **配置元**: `miscDepsJp/include/libopenjtalk/mecab-naist-jdic/`から`make_jdic.py`でビルド
   - **処理**: `jtalkSync`エイリアスで`source/synthDrivers/jtalk/dic/`にコピー

2. **音声ファイル**（`source/synthDrivers/jtalk/`配下の各フォルダ）:
   - `lite/voice.htsvoice`
   - `m001/m001.htsvoice`
   - `mei/mei_happy.htsvoice`
   - `tohokuf01/tohoku-f01-neutral.htsvoice`
   - **配置元**: `miscDepsJp/source/synthDrivers/jtalk/`（overlay処理でコピー）

3. **設定ファイル**:
   - `mecabrc`（`source/synthDrivers/jtalk/`）
   - **配置元**: `miscDepsJp/include/python-jtalk/`（`_copy_jtalk_core_files()`で直接コピー）

#### ライセンス・ドキュメントファイル

1. **ライセンスファイル**（`source/synthDrivers/jtalk/`）:
   - `AUTHORS-libmecab.txt`, `BSD-libmecab.txt`, `COPYING-HTS_engine_API.txt`
   - `COPYING-libmecab.txt`, `COPYING-libopenjtalk.txt`, `GPL-libmecab.txt`, `LGPL-libmecab.txt`
   - `CREDIT-mei-normal.txt`
   - **配置元**: `miscDepsJp/source/synthDrivers/jtalk/`（overlay処理でコピー）

2. **画像ファイル**（`source/images/`）:
   - `nvdajp_cd.png`, `nvdajp.ico`, `nvdajp2.ico`, `nvdajp3.ico`
   - **配置元**: `miscDepsJp/source/images/`（overlay処理でコピー）

3. **タイプライブラリ**（`source/typelibs/`）:
   - **注**: タイプライブラリの詳細は`roadmap.md`のPhase 1.4.5を参照

#### ビルドプロセスでの処理フロー

1. **`miscdepsjp`エイリアス**:
   - `setup_miscdeps_overlay.py`: `miscDepsJp/source/` → `source/`への全体コピー
   - `_copy_jtalk_core_files()`: `miscDepsJp/include/python-jtalk/` → `source/synthDrivers/jtalk/`への直接コピー

2. **`jtalkPrep`エイリアス**:
   - DLLのビルド（必要時）
   - `htsengineapi`と`libopenjtalk`を`miscDepsJp/include/python-jtalk`にコピー
   - DLLを`miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll`にコピー（後続のoverlay処理で`source/synthDrivers/jtalk/libopenjtalk.dll`に到達）

3. **`jtalkSync`エイリアス**:
   - 辞書ファイルのビルドとコピー
   - `libmecab.dll`のビルドとコピー（直接`source/synthDrivers/jtalk/`にコピー）
   - `libopenjtalk.dll`のコピー（直接`source/synthDrivers/jtalk/`にコピー）

**注**: 現状では、複数のコピー処理が混在しており、overlay処理と直接コピーが併用されている。Phase 2（overlay処理の廃止）により、すべてのファイルが直接`source/`に配置されるようになる。

### 本家版の設計思想との整合性

**本家版のフォルダ構成**:

- `miscDeps/`: サードパーティのベンダーコード（ヘッダー、Python拡張モジュール、バイナリ、ツール）
- `source/`: NVDA本体のソースコード（ドライバーを含む）

**本家版に最初からjtalkとtranslator2があった場合の想定構成**:

- `miscDeps/include/python-jtalk/`: JTalkのコアファイル（jtalkCore.py、mecab.py、text2mecab.pyなど）
- `source/synthDrivers/jtalk/`: JTalkドライバー本体

**日本語版の現在の構成との比較**:

- ✅ **ベンダーコードの配置**: `miscDepsJp/include/` = 本家版の`miscDeps/include/`に対応（設計思想は一致）
- ✅ **ドライバーの配置**: `source/synthDrivers/jtalk/` = 本家版の想定構成と一致
- ⚠️ **問題点**: `miscDepsJp/source/`という中間フォルダとoverlay処理が存在（本家版にはない独自の仕組み）

**本家版の`include/`と`miscDeps/include/`の使い分け**:

本家版では、以下のように使い分けている：

- **`include/`**: 大きなサブモジュールを個別に管理
  - 各サブモジュールが独立したリポジトリとして管理されている（liblouis、espeak、sonic、ia2、javaAccessBridge32、w3c-aria-practices、detours、nsis、wil、nvda-cldr、nvda-mathcatなど）
  - `.gitmodules`で個別に定義されている
  - 例: `[submodule "include/liblouis"]`、`[submodule "include/espeak"]`など

- **`miscDeps/include/`**: 小さなファイル（IDLファイルなど）をまとめて管理
  - `miscDeps`全体が1つのサブモジュール（`nvda-misc-deps`リポジトリ）として管理されている
  - `.gitmodules`で`[submodule "miscDeps"]`として定義されている
  - `miscDeps/include/`にはIDLファイル（AcrobatAccess、ISimpleDOM、mathPlayer）が配置されている
  - `miscDeps/python/`、`miscDeps/source/`、`miscDeps/tools/`も同じサブモジュール内に含まれている

**使い分けの基準**:

- **`include/`に配置**: 大きなサブモジュール（個別にサブモジュールとして管理する必要がある）
- **`miscDeps/include/`に配置**: 小さなファイル（IDLファイルなど）で、`miscDeps`サブモジュール内にまとめて管理

**日本語版への適用**:

- **`miscDepsJp/include/`の内容**: python-jtalk、htsengineapi、libopenjtalk、libkurajiなどは、本家版の基準では「大きなサブモジュール」に該当する可能性がある
- **統合の選択肢**:
  1. **`includejp/`にトップレベルフォルダとして配置（推奨）**: 本家版の`include/`と同様の方式で、トップレベルに`includejp/`フォルダを作成
     - 本家版の`include/`と並列に配置されるため、構成が明確
     - 本家版の`include/`との競合を避けられる
     - 本家版の`miscDeps/`サブモジュールとの競合も避けられる
     - 例: `includejp/python-jtalk/`、`includejp/libopenjtalk/`、`includejp/libkuraji/`など
  2. **`include/`に個別サブモジュールとして配置**: 本家版の`include/`と同様の方式（例: `include/python-jtalk`、`include/libopenjtalk`など）
     - 本家版の`include/`との競合を避ける必要がある
  3. **`miscDeps/include/`に統合**: 本家版の`miscDeps/include/`と同様の方式
     - 本家版の`miscDeps/`サブモジュールとの競合を避ける必要がある
     - 本家版の基準では「小さなファイル」向けのため、適切ではない可能性がある

**結論**: 日本語版のフォルダ構成は本家版の設計思想と基本的に一致しているが、`miscDepsJp/source/`とoverlay処理は本家版にはない独自の仕組み。`miscDepsJp/include/`を`includejp/`のようなトップレベルのフォルダにする方が、本家版の構成に整合する。Phase 1.5.2（overlay処理の廃止）により、本家版の設計思想により近い構成になる。

### miscDepsJpフォルダを残す必然性について

**現在のmiscDepsJpフォルダの構成**:

- `miscDepsJp/include/`: ベンダーツリー（python-jtalk、htsengineapi、libopenjtalk、libkurajiなど）
- `miscDepsJp/source/`: 日本語版固有のソースファイル（overlayのソース）
- `miscDepsJp/jptools/`: テストとビルドツール

**本家版の設計思想に従った場合の想定構成**:

- `miscDeps/include/python-jtalk/`: JTalkのコアファイル（現在の`miscDepsJp/include/python-jtalk/`に対応）
- `source/synthDrivers/jtalk/`: JTalkドライバー本体（現在はoverlayで配置）
- `ci/scripts/`または`jptools/`: テストとビルドツール（現在の`miscDepsJp/jptools/`に対応）

**miscDepsJpフォルダを残す必然性**:

- ⚠️ **現時点では必要**: Phase 2（overlay処理の廃止）が完了するまでは、`miscDepsJp/source/`がoverlayのソースとして機能しているため必要
- ⚠️ **Phase 2完了後も一時的に必要**: `miscDepsJp/include/`と`miscDepsJp/jptools/`が残るため、完全な廃止には追加の移行作業が必要
- ✅ **長期的には不要**: 本家版の設計思想に完全に従うなら、以下の移行が可能：
  - `miscDepsJp/include/` → `miscDeps/include/`に統合
  - `miscDepsJp/jptools/` → `ci/scripts/`や`jptools/`に移動
  - `miscDepsJp/source/` → Phase 2で廃止されれば不要

**有力な廃止候補フォルダ（優先順位順）**:

1. **`miscDepsJp/source/`（最優先・Phase 2で廃止予定）**
   - **理由**: overlay処理の廃止により不要になる
   - **移行先**: 内容は直接`source/`に配置（Phase 2で実現）
   - **影響範囲**: overlay処理全体、`miscdepsjp`エイリアス
   - **実現時期**: Phase 2（overlay処理の廃止）完了時

2. **`miscDepsJp/jptools/`（Phase 2完了後に検討）**
   - **理由**: トップレベルの`jptools/`に統合可能（過去にはmiscDepsJpはサブモジュールだったが、今は親プロジェクトに統合されているため）
   - **移行先**: トップレベルの`jptools/`に統合
   - **影響範囲**: テスト関連ツール（`test.py`、`jpBrailleRunner.py`など）、辞書関連ツール（`jtalk/`、`jtusrdic/`）
   - **実現時期**: Phase 2完了後

3. **`miscDepsJp/include/`（長期的な改善として検討）**
   - **理由**: 本家版の設計思想に従うなら`miscDeps/include/`に統合可能
   - **移行先**: `miscDeps/include/`に統合
   - **影響範囲**: ベンダーツリー全体（python-jtalk、htsengineapi、libopenjtalk、libkurajiなど）
   - **実現時期**: 長期的な改善（本家版の`miscDeps/`との競合を避ける必要があるため慎重に検討）

**移行の優先順位**:

1. **Phase 2（overlay処理の廃止）**: 最優先。`miscDepsJp/source/`を廃止し、直接`source/`に配置する方式に変更
2. **`miscDepsJp/jptools/`の移行**: Phase 2完了後、トップレベルの`jptools/`に統合を検討（過去にはmiscDepsJpはサブモジュールだったが、今は親プロジェクトに統合されているため、統合は可能）
3. **`miscDepsJp/include/`の統合**: 長期的な改善として、`miscDeps/include/`への統合を検討（本家版との差分を最小化する観点から）

**`miscDepsJp/jptools/`のトップレベル`jptools/`への統合について**:

- ✅ **統合の可能性**: 過去にはmiscDepsJpはサブモジュールだったが、PR #492で親プロジェクトに統合されているため、`miscDepsJp/jptools/`をトップレベルの`jptools/`に統合することは技術的に可能
- ✅ **既存の`jptools/`との関係**: トップレベルの`jptools/`には既に多くのJP固有のツールが配置されている（`scons_jp.py`、`runJpSmokeTests.ps1`、`nonCertBuild.py`など）
- ⚠️ **統合時の注意点**:
  - `miscDepsJp/jptools/`内のテスト関連ツール（`test.py`、`jpBrailleRunner.py`など）とトップレベルの`jptools/`内のツールとの競合を避ける
  - パス参照の更新が必要（例: `runJpSmokeTests.ps1`が`miscDepsJp/jptools/test.py`を参照している場合）
  - 辞書関連ツール（`jtalk/`、`jtusrdic/`）の配置場所を検討

### 具体的な方針案（roadmap.mdのPhase 1.5以降）

**方針案の全体像**:

本家版の設計思想に従い、`miscDepsJp`フォルダを段階的に廃止し、以下の構成に移行する：

```text
リポジトリルート/
├── include/              # 本家版の大きなサブモジュール
├── includejp/            # 日本語版の大きなベンダーツリー（新規）
│   ├── python-jtalk/
│   ├── libopenjtalk/
│   └── htsengineapi/
├── miscDeps/             # 本家版の小さな依存関係（サブモジュール）
├── source/               # NVDA本体のソースコード（直接配置）
│   └── synthDrivers/
│       └── jtalk/        # overlay処理廃止後、直接配置
├── jptools/              # 日本語版のビルド・テストツール（統合後）
└── ci/scripts/           # CIスクリプト
```

**段階的な移行計画**:

#### Phase 1.5.1: コピー処理の統合と削減（roadmap.md Phase 1.5.1に対応）

**目標**: 重複するコピー処理を統合し、コピー処理の総数を削減

**作業内容**:

1. `_copy_jtalk_core_files()` と `jtalkSync` のコアファイルコピーを統合
2. `_copy_jtalk_core_files()` を削除し、`jtalkSync` 経由の1つの経路に統一
3. 古い `.cmd` スクリプトの削除
4. **`patch.exe` への依存の排除**:
   - **方針**: サブモジュールをやめたため、パッチ済みファイルを直接リポジトリに含める（推奨）
     - ベンダーツリーは既に PR #582 で git subtree merge によりメインリポジトリに統合済み（`vendor-submodules.md` 参照）
     - サブモジュールを使わないため、元のベンダーリポジトリを参照する必要がない
     - パッチ済みファイル（`HTS_gstream_ex.c`、`HTS_engine_ex.c`、`jpcommon_label.c`）をリポジトリに直接含めることで、ビルド時のパッチ適用処理が不要になる
   - **作業内容**:
     - パッチ済みファイルを適切な場所（`miscDepsJp/include/python-jtalk/lib/`、`miscDepsJp/include/python-jtalk/jpcommon/` など）に配置
     - `Makefile.mak` と `all.mak` から `patch` コマンド呼び出しを削除し、パッチ済みファイルを直接使用するように変更
     - `jptools/devbuild.cmd` と `jptools/certBuild2023.cmd` から `patch -v` チェックを削除
     - パッチファイル（`.patch`）は履歴保持のため残すか、ドキュメント化して削除
   - **代替案（非推奨）**: Pythonスクリプトでパッチ処理を代替（`difflib` や `unidiff` を使用）する方法もあるが、サブモジュールをやめた現状では不要な複雑さを追加することになる

**検証要件**: リリースビルド、ローカルの署名なしビルド、ローカルのユニットテスト、Actions CI の全てで検証が必要

#### Phase 1.5.2: overlay処理の廃止（roadmap.md Phase 1.5.2に対応）

**目標**: `miscDepsJp/source` への中間コピーを削減し、直接 `source/` への配置に変更。overlay処理自体を廃止

**作業内容**:

1. `jtalkSync` のコピー先を `miscDepsJp/source/synthDrivers/jtalk` から `source/synthDrivers/jtalk` に直接変更
2. `miscDepsJp/source` へのコピーを削減し、overlay処理を廃止
3. `miscdepsjp` エイリアスを削除（overlay処理が不要になるため）
4. **注**: タイプライブラリの上書き廃止は`roadmap.md`のPhase 1.4.5で実施予定

**検証要件**: リリースビルド、ローカルの署名なしビルド、ローカルのユニットテスト、Actions CI の全てで検証が必要

**削減効果**:

- コピー処理の段階を2段階（`jtalkSync` → overlay）から1段階（直接配置）に削減
- overlay処理自体が不要になり、ビルドプロセスが大幅に簡素化
- ビルド時間の短縮

**overlay処理の利点の再評価**:

- **冪等性**: SCons自体が依存関係を管理しているため、直接コピーでも冪等性は保証される
- **クリーン処理**: 直接コピーでも`env.Clean()`を配線できる
- **結論**: overlay処理を残すことの利点は実際には存在しないか、または直接コピーでも同じ利点を得られる
- **既存の実装例**: `_copy_jtalk_core_files()`は既に直接コピーを実装しており、overlayを経由していない。これはoverlayが不要であることの証拠

#### Phase 1.5.3: `miscDepsJp/include/`を`includejp/`に移行（Phase 1.5.2完了後）

**目標**: 本家版の`include/`と並列に配置し、構成を明確化

**作業内容**:

1. `miscDepsJp/include/` → `includejp/`に移動
2. パス参照の更新（`miscDepsJp/include/` → `includejp/`）
3. SConsビルドスクリプトの更新
4. テストスクリプトの更新

**検証要件**: リリースビルド、ローカルの署名なしビルド、ローカルのユニットテスト、Actions CI の全てで検証が必要

#### Phase 1.5.4: `miscDepsJp/jptools/`をトップレベルの`jptools/`に統合（Phase 1.5.3完了後）

**目標**: テストとビルドツールをトップレベルの`jptools/`に統合

**作業内容**:

1. `miscDepsJp/jptools/`の内容をトップレベルの`jptools/`に移動
2. パス参照の更新（例: `runJpSmokeTests.ps1`が`miscDepsJp/jptools/test.py`を参照している場合）
3. 辞書関連ツール（`jtalk/`、`jtusrdic/`）の配置場所を検討・整理

**検証要件**: ローカルのユニットテスト、jpSmokeTest、Actions CI の全てで検証が必要

#### Phase 1.5.5: `miscDepsJp`フォルダの完全廃止（Phase 1.5.4完了後）

**目標**: `miscDepsJp`フォルダを完全に廃止し、本家版と整合する構成に移行

**作業内容**:

1. `miscDepsJp`フォルダの残存ファイルを確認・整理
2. 不要になったファイル・フォルダを削除
3. ドキュメントの更新

**検証要件**: リリースビルド、ローカルの署名なしビルド、ローカルのユニットテスト、Actions CI の全てで検証が必要

**各Phaseの実施原則**:

- **小さなPR単位で進める**: 各Phaseをさらに小さなPRに分割し、各PRで必ず全テストが通過することを確認
- **段階的な検証を必須とする**: 各PRでビルド・型チェック・単体テスト・システムテストを通過確認
- **完了の定義を明確化**: テストが全て通過し、CIが安定して緑になるまで「完了」としない
- **問題が発生したら即座に停止**: テスト失敗や不安定な動作が見られたら、次のPhaseに進まずに問題を解決
- **安定版リリースの維持**: 2025.3.xjp安定版のリリース継続を維持し、リリースに影響を与える変更は段階的に実施

**roadmap.mdとの対応関係**:

- タイプライブラリの上書き廃止については、`roadmap.md`のPhase 1.4.5を参照してください。
- 使用されていない古い`.cmd`スクリプトの削除については、`roadmap.md`のPhase 1.4.6を参照してください。
- Phase 1.5.3以降（`includejp/`への移行、`jptools/`の統合、`miscDepsJp`フォルダの完全廃止）は、roadmap.mdのPhase 1.5の範囲外ですが、本家版の設計思想に従った長期的な改善として記載しています
- **注**: roadmap.mdのPhase 1.5は簡潔に記載されており、詳細な計画はこのドキュメント（`miscdepsjp-overlay-strategy.md`）に集約されています

**miscDepsJp フォルダと JP overlay 処理の将来**:

- 本家版との差分を最小化する方針（`projectDocs/jp/roadmap.md` 参照）に基づき検討する

**検証要件**: これらの改善はビルドシステムの根幹に関わる変更のため、品質保証の観点から、以下の全ての環境で検証が必要です：

- **リリースビルド**: 署名付きリリースビルドが正常に完了することを確認
- **ローカルの署名なしビルド**: `.\scons.bat dist` や `.\scons.bat source dist launcher` が正常に完了することを確認
- **ローカルのユニットテスト**: `rununittests.bat` や `jptools/runJpSmokeTests.ps1` が正常に実行されることを確認
- **Actions CI**: GitHub Actions の CI パイプライン（`.github/workflows/testAndPublish.yml`）が正常に完了することを確認

各 Phase の実装後は、これらの環境全てで動作確認を行い、問題が発生した場合は即座に修正する必要があります。

## 関連ドキュメント

- `projectDocs/jp/vendor-submodules.md` - ベンダーツリーの運用方針
- `projectDocs/jp/README.md` - JP overlay の定義
- `readme-nvdajp.md` - SCons ビルドターゲットの説明
- `projectDocs/jp/roadmap.md` - 長期的なロードマップ
