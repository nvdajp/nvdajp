# miscDepsJp と JP overlay の現状と長期的な方針

## 概要

このドキュメントは、`miscDepsJp` フォルダと JP overlay 処理の現状の問題点と、長期的な改善方針を整理したものです。

### 基本方針（roadmap.md と整合）

**roadmap.md の原則に従う**:

- 本家との差分を最小化（独自仕組みは段階的に廃止）
- 小さなPR単位・段階検証・完了定義を明確に
- 安定版リリースの継続を優先し、問題があれば停止して対処

**改善の方向性**:

- コピー処理は「統合」だけでなく「削減」して単純化する
- Python コードは最初から `source/` に置く形を理想とし、overlay という中間段階を廃止して本家設計に揃える

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

### miscDepsJp の管理方法の変遷

**過去（PR #492 以前）**:

- `miscDepsJp` フォルダ全体がサブモジュールとして管理されていた
- `miscDepsJp/include/*` 配下の各ベンダーツリー（python-jtalk、htsengineapi、libopenjtalk、libkuraji など）も個別のサブモジュールとして管理されていた
- 更新時は `git submodule update` が必要だった

**PR #492（miscDepsJp の統合）**:

- `miscDepsJp` フォルダ全体がメインリポジトリ（nvdajp/nvdajp）に統合された

**PR #582（miscDepsJp/include のサブモジュール化）**:

- `miscDepsJp/include/*` 配下のベンダーツリー（python-jtalk、htsengineapi、libopenjtalk、libkuraji など）が git subtree merge によりメインリポジトリに統合された
- サブモジュールではないため、`git submodule update` は不要
- ベンダーツリーの更新が必要な場合は、通常の Git 操作（`git pull`、`git merge` 等）で対応
- 一部のベンダーツリー（例: libopenjtalk）は、subtree として親リポジトリと紐付いている

**現在（PR #582 以降）**:

- `miscDepsJp` およびその配下のベンダーツリーは、すべてメインリポジトリに統合されている
- サブモジュールではないため、`git submodule update` は不要

**参考**: 詳細は `projectDocs/jp/vendor-submodules.md` を参照してください。

### `miscDepsJp/source` と本家版の `source/` の関係

- **`miscDepsJp/source`**: 日本語版固有のソースファイルを保持（overlay のソース）
- **本家版の `source/`**: 本家版のソースコードを保持（overlay のターゲット）
- **overlay 処理**: `miscDepsJp/source` の内容を本家版の `source/` にコピーして上書き
  - 同じパスのファイルがある場合、本家版のファイルが日本語版のファイルで上書きされる
  - 本家版に存在しないパスのファイルは新規に追加される
  - 本家版のファイルは Git で管理されているため、`git checkout` で復元可能

### 現在のコピー処理

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

- **問題**: ビルドで `patch.exe`（Git for Windows 同梱）に依存
  - `miscDepsJp/include/python-jtalk/lib/Makefile.mak`: `HTS_gstream_ex.c`, `HTS_engine_ex.c` へのパッチ
  - `miscDepsJp/include/python-jtalk/all.mak`: `jpcommon_label.c` へのパッチ
  - `jptools/certBuild2023.cmd`: `patch -v` で存在チェック（`devbuild.cmd`は削除済み、`nonCertBuild.py`で代替）
- **影響**:
  - 外部ツール依存でセットアップが煩雑
  - CI での依存管理が増える
  - パッチ適用箇所が分散しメンテが難しい

**パッチ適用箇所**:

1. `HTS_gstream_ex.patch`: `HTS_gstream_ex.c`
2. `HTS_engine_ex.patch`: `HTS_engine_ex.c`
3. `jpcommon_label.patch`: `jpcommon_label.c`

## 改善計画

**重要**: これらの改善は、将来的な x64 移行をスムーズにするためにも重要です。複雑なコピー処理やフォルダ構造への依存が残っていると、x64 対応時にさらに複雑になり、作業量が増加する可能性があります。早い段階で構造を簡素化することで、x64 移行時の作業を大幅に削減できます。

**基本方針**: コピー処理を「統合」するだけでなく、積極的に「削減」し、ビルドプロセスを単純化することを目指します。

**miscDepsJp フォルダと JP overlay 処理の将来**:

- 本家版との差分を最小化する方針（`projectDocs/jp/roadmap.md` 参照）に基づき検討する

**検証要件**: これらの改善はビルドシステムの根幹に関わる変更のため、品質保証の観点から、以下の全ての環境で検証が必要です：

- **リリースビルド**: 署名付きリリースビルドが正常に完了することを確認
- **ローカルの署名なしビルド**: `.\scons.bat dist` や `.\scons.bat source dist launcher` が正常に完了することを確認
- **ローカルのユニットテスト**: `rununittests.bat` や `jptools/runJpSmokeTests.ps1` が正常に実行されることを確認
- **Actions CI**: GitHub Actions の CI パイプライン（`.github/workflows/testAndPublish.yml`）が正常に完了することを確認

各 Phase の実装後は、これらの環境全てで動作確認を行い、問題が発生した場合は即座に修正する必要があります。

### Phase 1: コピー処理の統合と削減（短期・優先度高）

- **目標**: 重複するコピー処理を統合し、コピー処理の総数を削減
- **作業内容**:
  - `_copy_jtalk_core_files()` と `jtalkSync` のコアファイルコピーを統合
  - `_copy_jtalk_core_files()` を削除し、`jtalkSync` 経由の1つの経路に統一
  - `jtalkSync` でコピーしたファイルを `miscDepsJp/source/synthDrivers/jtalk` に配置し、overlay で `source/` に到達させる方式に統一
  - 古い `.cmd` スクリプトの削除
- **削減効果**:
  - コピー処理の経路を2つから1つに削減（直接コピー経路を削除）
  - コピー処理の実行箇所を1箇所に集約
- **x64 移行への影響**:
  - コピー処理が1箇所に集約されていれば、x64 対応時にアーキテクチャ別の処理を追加するだけで済む
  - 重複処理が残っていると、x64 対応時に複数箇所を修正する必要がある

### Phase 2: 中間コピー段階の削減と overlay 処理の廃止（中期・優先度高）

- **目標**: `miscDepsJp/source` への中間コピーを削減し、直接 `source/` への配置に変更。overlay 処理自体を廃止することを検討
- **作業内容**:
  - `jtalkSync` のコピー先を `miscDepsJp/source/synthDrivers/jtalk` から `source/synthDrivers/jtalk` に直接変更
  - `miscDepsJp/source` へのコピーを削減し、overlay 処理を廃止
  - 直接コピーでも SCons の依存関係管理により冪等性は保証される
  - 直接コピーでも `env.Clean()` を配線することでクリーン処理は容易
- **削減効果**:
  - コピー処理の段階を2段階（`jtalkSync` → overlay）から1段階（直接配置）に削減
  - overlay 処理自体が不要になり、ビルドプロセスが大幅に簡素化
  - ビルド時間の短縮
- **overlay 処理の利点の再評価**:
  - **冪等性**: `setup_miscdeps_overlay.py` はタイムスタンプとサイズを比較してスキップするだけだが、SCons 自体が依存関係を管理しているため、直接コピーでも冪等性は保証される
  - **クリーン処理の容易さ**: SConstruct で `env.Clean()` を配線しているが、直接コピーでも同じように配線できる（`_compute_overlay_targets()` と同様のファイルリスト計算を直接コピーでも実装可能）
  - **結論**: overlay 処理を残すことの利点は実際には存在しないか、または直接コピーでも同じ利点を得られる
- **既存の実装例**:
  - `_copy_jtalk_core_files()` は既に直接コピーを実装しており、overlay を経由していない。これは overlay が不要であることの証拠

### Phase 3: 依存関係の明確化とエイリアスの統合（中期）

- **目標**: 依存関係を明確にし、エイリアスを統合してビルドプロセスを単純化
- **作業内容**:
  - 各エイリアスの役割を明確化
  - Phase 2 で overlay 処理が廃止されれば、`miscdepsjp` エイリアス自体が不要になる可能性
  - `jtalkSync` を直接 `source/` にコピーするように変更し、依存関係を単純化
  - 依存関係のドキュメント化
  - エラーメッセージの改善
- **単純化効果**:
  - overlay 処理が廃止されれば、`miscdepsjp` エイリアスを削除できる
  - エイリアスの数を削減し、ビルドプロセスの理解を容易にする
  - 依存関係の複雑さを削減（`source → miscdepsjp → jtalkSync → jtalkPrep` から `source → jtalkSync → jtalkPrep` に簡素化）

### Phase 4: フォルダ構造への依存削減と直接参照の検討（長期）

- **目標**: `miscDepsJp` フォルダ構造への依存を削減し、より統合的な方式への移行を検討
- **作業内容**:
  - 環境変数（`REPO_ROOT`）の活用
  - パス解決の共通ユーティリティ化
  - 設定ファイルからの取得（将来的に検討）
  - **直接参照方式の検討**: コピーではなく、`miscDepsJp/include` から直接参照する方式への移行を検討
    - Python の `sys.path` や `PYTHONPATH` を活用した直接参照
    - シンボリックリンクの活用（Windows の制約を考慮）
    - ビルド時のパス解決の改善
  - **注意**: Phase 2 で overlay 処理が廃止され、`jtalkSync` が直接 `source/` にコピーするようになれば、`miscDepsJp/source` フォルダ自体が不要になる可能性がある
- **削減効果**:
  - コピー処理自体を削減または排除する可能性
  - `miscDepsJp/source` フォルダが不要になれば、フォルダ構造がさらに簡素化される
  - ビルドプロセスの大幅な単純化
- **x64 移行への影響**:
  - フォルダ構造への依存が強いと、x64 対応時のパス変更（例: `x86/`, `x64/` サブディレクトリの追加）が困難になる
  - 環境変数や共通ユーティリティを使用することで、x64 対応時の変更箇所を最小化できる
  - 直接参照方式であれば、x64 対応時にパス解決ロジックを変更するだけで済む可能性がある
  - ロードマップの Phase 1.2（DLL パス構造の統一）と連携して実施することで、x64 対応の前提条件を整備できる

### Phase 5: 純 Python 化とビルドプロセスの最終的な単純化（長期）

- **目標**: `.cmd` スクリプトを完全に Python 化し、ビルドプロセスを最終的に単純化
- **作業内容**:
  - `copy_jtalk_core_files.cmd` の Python 化（既に `_copy_jtalk_core_files()` として実装済み）
  - 残存する `.cmd` スクリプトの削除
  - nmake 依存の削減（将来的に検討）
  - ビルドプロセスの最終的な見直しと単純化

## 関連ドキュメント

- `projectDocs/jp/vendor-submodules.md` - ベンダーツリーの運用方針
- `projectDocs/jp/README.md` - JP overlay の定義
- `readme-nvdajp.md` - SCons ビルドターゲットの説明
- `projectDocs/jp/roadmap.md` - 長期的なロードマップ
