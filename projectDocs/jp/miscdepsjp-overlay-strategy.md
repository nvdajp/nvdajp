# miscDepsJp の現状と長期的な方針

## 概要

このドキュメントは、`miscDepsJp` フォルダの現状の問題点と、長期的な改善方針を整理したものです。

**注**: JP overlay 処理は Phase 2 で廃止されました（2025-12-12）。日本語版固有ファイルは `source/` に直接配置されています。

### 基本方針（roadmap.md と整合）

**roadmap.md の原則に従う**:

- 本家との差分を最小化（独自仕組みは段階的に廃止）
- 小さなPR単位・段階検証・完了定義を明確に
- 安定版リリースの継続を優先し、問題があれば停止して対処

**改善の方向性**:

- コピー処理は「統合」だけでなく「削減」して単純化する
- Python コードは最初から `source/` に置く形を理想とし、本家設計に揃える
- **基本方針との整合性**: この見直しは、以下の基本方針に完全に整合している：
  - ✅ **本家との差分を最小化**: 独自仕組みを廃止し、本家設計（`source/` に直接配置）に揃える
  - ✅ **コピー処理の削減**: ビルド時のコピー処理を最小化し、ビルドプロセスを簡素化
  - ✅ **小さなPR単位で進める**: Phase 1-2 で段階的に実施し、各段階で検証を行う
  - ✅ **安定版リリースの継続を優先**: 段階的な検証により、安定版リリースに影響を与えない範囲で実施できる
- 最初から `source/synthDrivers/jtalk` にあるべきファイルは、コピーではなく move（または Git で直接配置）してもよい。これにより、ビルド時のコピー処理自体が不要になる可能性がある
  - ベンダーツリー由来のファイル（`jtalkCore.py`, `mecab.py`, `text2mecab.py` など）: `miscDepsJp/include/python-jtalk` から move または Git で直接配置
  - 日本語版固有の JTalk ドライバー依存ファイル（`jtalkDir.py`, `jtalkDriver.py`, `translator1.py`, `translator2.py` など）: `miscDepsJp/source/synthDrivers/jtalk` から move または Git で直接配置（これらは日本語版固有のファイルなので、最初から `source/synthDrivers/jtalk` に配置するのが自然）
- **重要**: `miscDepsJp/include/python-jtalk` と `source/synthDrivers/jtalk` に Python ソースファイルを重複させなくても、NVDA のビルドやユニットテスト、jp smoke test は実行できる。NVDA のソースコードは `source/synthDrivers/jtalk` からインポートしており、テストコードも `source/synthDrivers/jtalk` を参照しているため、`miscDepsJp/include/python-jtalk` に Python ファイルを保持する必要はない
- **注**: ファイルを move する場合、`miscDepsJp/include/python-jtalk` から `source/synthDrivers/jtalk` に移動すると、ベンダーツリーからファイルがなくなる可能性がある。これは許容されるが、ベンダーツリーの更新や管理方法に影響を与える可能性があるため、注意が必要。ただし、`miscDepsJp/include/python-jtalk` はバイナリや辞書のビルド場所として残る意味がある。また、`miscDepsJp/source/synthDrivers/jtalk` から `source/synthDrivers/jtalk` に移動すると、`miscDepsJp/source` フォルダ自体が不要になる可能性がある

**重要**: これらの改善は、将来的な x64 移行をスムーズにするためにも重要です。複雑な構造を早い段階で簡素化することで、x64 対応時の作業量を大幅に削減できます。詳細は「改善計画」セクションを参照してください。

## 現状の構造

### リポジトリのフォルダ構成

日本語版リポジトリのルートには、以下の主要なフォルダがあります：

```text
リポジトリルート/
├── source/           # 本家版（upstream）のソースコード
│   └── synthDrivers/
│       └── jtalk/    # 日本語版固有のフォルダ
├── jptools/          # 日本語版固有のフォルダ
└── miscDepsJp/       # 日本語版固有のフォルダ
```

### 本家版の `source` フォルダ

- **役割**: 本家版（nvaccess/nvda）から取り込んだソースコードを保持
- **管理方法**: 通常の Git 操作で本家版からマージ・更新
- **内容**: NVDA 本体のソースコード（英語版のドライバー、コア機能など）

### miscDepsJp フォルダの構成

```text
miscDepsJp/
├── include/          # ベンダーツリー（python-jtalk、htsengineapi、libopenjtalk、libkuraji など）
│   └── python-jtalk/ # バイナリビルド場所（x86/libopenjtalk.dll、x64/libopenjtalk.dll など）
│                     # 辞書ビルド場所（dic/ など）
└── jptools/          # テストとビルドツール（一部のツールはリポジトリルートの jptools/ に移動済み）
```

**`miscDepsJp` の役割**:

- **ベンダーツリーの保持**: `miscDepsJp/include` にベンダーツリーのソースコードを保持
- **バイナリのビルド場所**: `jtalkPrep` で DLL をビルドし、`miscDepsJp/include/python-jtalk/x86/` や `miscDepsJp/include/python-jtalk/x64/` に配置
- **辞書ファイルのビルド場所**: `jtalkSync` で辞書ファイルをビルドし、`miscDepsJp/include/python-jtalk/dic/` に配置
- **ビルド成果物の配置**: ビルド成果物（DLL、辞書ファイル）は `miscDepsJp` でビルドし、その後 `source/synthDrivers/jtalk` に直接配置される

### jptools フォルダ

- **役割**: 日本語版固有のテストとビルドツールを保持
- **配置**:
  - リポジトリルート直下（`jptools/`）: 主要なビルドスクリプトとテストスクリプト
  - `miscDepsJp/jptools/`: 一部のツール（例: `jpBrailleRunner.py`、`jtusrdic/` など）
- **内容**:
  - リポジトリルートの `jptools/`: ビルドスクリプト（`scons_jp.py`、`nonCertBuild.py` など）、テストスクリプト（`runJpSmokeTests.ps1` など）
  - `miscDepsJp/jptools/`: 一部のテストツールとユーティリティ

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

### 現在のビルド処理

JTalk 関連のビルド処理は以下の通りです：

1. **`jtalkPrep` エイリアス**
   - DLL のビルド（必要時）
   - `htsengineapi` と `libopenjtalk` を `miscDepsJp/include/python-jtalk` にコピー
   - DLL を `source/synthDrivers/jtalk/libopenjtalk.dll` に直接配置

2. **`jtalkSync` エイリアス**
   - 辞書ファイルのビルドとコピー
     - `miscDepsJp/include/python-jtalk/dic` → `source/synthDrivers/jtalk/dic`
   - DLL を `miscDepsJp/include/python-jtalk` → `source/synthDrivers/jtalk` にコピー
     - コピーされるファイル: `libmecab.dll`, `libopenjtalk.dll`

### 依存関係

```text
source → jtalkSync → jtalkPrep
```

## 現状の問題点

### 1. miscDepsJp フォルダ構造への依存

- **問題**: 多くのスクリプトが `miscDepsJp` フォルダ構造に依存
  - `jtalkRunner.py`: `miscDepsJp/include/python-jtalk` から `repo_root` を推論
  - 一部のテストスクリプトが `miscDepsJp` のパスに依存

- **影響**:
  - フォルダ構造の変更に弱い
  - 長期的な保守性の低下

### 2. patch.exe への依存

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

- **リリースビルド**: 署名付きリリースビルドが正常に完了することを確認（`jptools/certBuild2025.ps1`）
- **ローカルの署名なしビルド**: `scons source dist launcher` や `scons source dist` が正常に完了することを確認
- **ローカルのユニットテスト**: `rununittests.bat` や `jptools/runJpSmokeTests.ps1` が正常に実行されることを確認
- **Actions CI**: GitHub Actions の CI パイプライン（`.github/workflows/testAndPublish.yml`）が正常に完了することを確認

各 Phase の実装後は、これらの環境全てで動作確認を行い、問題が発生した場合は即座に修正する必要があります。

### Phase 1: コピー処理の統合と削減（短期・優先度高）

- **目標**: 重複するコピー処理を統合し、コピー処理の総数を削減。テストの依存関係を変更することで、中間コピー段階をスキップして直接 `source/` への配置に移行
- **作業内容**:
  - **ファイルの移動**: 最初から `source/synthDrivers/jtalk` にあるべきファイルをコピー元から移動する。これにより、ビルド時のコピー処理自体が不要になる
    - **ベンダーツリー由来のファイル**（`jtalkCore.py`, `mecab.py`, `text2mecab.py` など）: `miscDepsJp/include/python-jtalk` から `source/synthDrivers/jtalk` に移動
    - **日本語版固有の JTalk ドライバー依存ファイル**（`jtalkDir.py`, `jtalkDriver.py`, `jtalkPrepare.py`, `translator1.py`, `translator2.py` など）: `miscDepsJp/source/synthDrivers/jtalk` から `source/synthDrivers/jtalk` に移動
  - **テストの依存関係を変更**（優先）: ユニットテストや jp smoke test が最初から `source/synthDrivers/jtalk` に直接依存するように変更
    - `jptools/runJpSmokeTests.ps1` の PYTHONPATH を `source/synthDrivers/jtalk` に変更
    - `miscDepsJp/jptools/jpBrailleRunner.py` などのテストスクリプトが `source/synthDrivers/jtalk` からインポートするように変更
    - ただし辞書やDLLなどビルドが必要なものは miscDepsJP で従来の処理を行い、リポジトリルートの `source/synthDrivers` および `source/synthDrivers/jtalk` にコピーする処理を残す
- **削減効果**:
  - Python ファイルのコピー処理が不要になる（ファイルを move したため）
  - 辞書やDLLなどビルドが必要なもののコピー処理は残るが、経路を2つから1つに削減（直接コピー経路を削除）
  - コピー処理の実行箇所を1箇所に集約（辞書やDLLのコピー処理のみ）
  - コピー処理の段階を2段階（`jtalkSync` → overlay）から1段階（直接配置）に削減
  - overlay 処理自体が不要になり、ビルドプロセスが大幅に簡素化
  - ビルド時間の短縮
- **x64 移行への影響**:
  - コピー処理が1箇所に集約されていれば、x64 対応時にアーキテクチャ別の処理を追加するだけで済む
  - 重複処理が残っていると、x64 対応時に複数箇所を修正する必要がある
- **検証要件**: 上記の「検証要件」セクションを参照。各 Phase の実装後は、これらの環境全てで動作確認を行い、問題が発生した場合は即座に修正する必要があります。

**注**: テストの依存関係を最初に変更することで、`miscDepsJp/source/synthDrivers/jtalk` への中間コピーが不要になり、Phase 1 と Phase 2 を統合して一気に直接コピー方式に移行できます。これにより、コピー処理の削減をより効率的に実施できます。

**注意**: ベンダーツリーの更新が必要な場合は、`source/synthDrivers` からベンダーツリーに書き戻す必要がある。ベンダーツリーの扱いはリファクタリング完了後に再検討する。

**実施状況（2025-12-12）**:

- Python ファイルと話者モデルを `source/synthDrivers/jtalk` に移動し、`_copy_jtalk_core_files()` は no-op 化済み
- テスト依存を `source/synthDrivers/jtalk` 直接参照に統一（`runJpSmokeTests.ps1` は `miscDepsJp/include/python-jtalk` を `PYTHONPATH` に追加し、`jtalkRunner.py` を参照）
- `jtalkPrep`/`jtalkSync` は DLL・辞書を直接 `source/synthDrivers/jtalk` へ配置するよう更新
- 検証結果: `jptools/runJpSmokeTests.ps1 -SkipInstall -SkipJtalkSync`、`scons.bat dist --all-cores`、`scons.bat launcher --all-cores` をローカル x86 で成功

### Phase 2: 依存関係の明確化とエイリアスの統合（中期）

- **目標**: 依存関係を明確にし、エイリアスを統合してビルドプロセスを単純化
- **作業内容**:
  - Phase 1 で JTalk 関連の Python ファイルと話者モデルは `source/synthDrivers/jtalk` に移動済み
  - `miscDepsJp/source` の以下のファイルも `source` に移動して overlay 処理を不要とする
    - `brailleDisplayDrivers/DirectBM.dll`（点字ディスプレイドライバー。移動は可能だが x86 バイナリである点に注意）
    - `images/` 配下の画像ファイル（`nvdajp.ico`, `nvdajp_cd.png` など）
    - `synthDrivers/nvdajp_jtalk.py`（日本語版固有の合成音声ドライバー）
    - `synthDrivers/jtalk/` 配下の一部ファイル（`_bgthread.py`, `_nvdajp_espeak.py`, `_nvdajp_spellchar.py`, `_nvdajp_unicode.py`, `roma2kana.py` など）
    - ライセンスファイルなど
    - `DirectBM.dll` を移動する場合は x86 バイナリであることを明記し、`kgs_addon` のビルドスクリプト（`jptools/scons_jp.py` 内 `kgs_addon` 関連）で期待される配置を崩さないように調整する
    - `.gitignore` の設定: `DirectBM.dll` は既に Git で管理される設定（`!source/brailleDisplayDrivers/DirectBM.dll`）があるため、移動後も問題なく管理される。移動後は `.gitignore` の 13行目（`!miscDepsJp/source/brailleDisplayDrivers/DirectBM.dll`）を削除し、12行目（`!source/brailleDisplayDrivers/DirectBM.dll`）を維持する
  - **エラーメッセージの改善**: ビルドエラー時のメッセージを改善し、原因特定を容易にする
  - **`miscdepsjp` エイリアスの削除**: `miscDepsJp/source` が空になったため、エイリアスを削除し、依存関係を `source → jtalkSync → jtalkPrep` に簡素化
  - **依存関係の整理とドキュメント化**: 依存関係を更新して文書化

**実施状況（2025-12-12）**: ✅ **完了**

- `miscDepsJp/source` の全ファイルを `source/` に移動し、overlay 処理を不要化
- `miscdepsjp` エイリアスを削除し、`sconstruct` の依存関係を `sourceDir → jtalkSync`、`pot → jtalkSync` に変更
- `jptools/runJpSmokeTests.ps1` の `miscdepsjp` 呼び出しを削除し、`jtalkSync` に変更
- `jptools/scons_jp.py` の `_run_overlay_and_stamp()` を no-op 化（`miscDepsJp/source` が空のため）
- 依存関係チェーンを `source → jtalkSync → jtalkPrep` に簡素化
- 検証結果: ローカル x86 で `scons.bat dist`、`scons.bat launcher`、`jptools/runJpSmokeTests.ps1 -SkipInstall -SkipJtalkSync` が成功

### Phase 3: フォルダ構造への依存削減と参照方式の簡素化（長期）

- **前提**: Phase 2 完了により、`miscDepsJp/source` は空になり、overlay/`miscdepsjp` エイリアスは廃止済み。現在、`miscDepsJp` に残るのはベンダーツリー（include）とビルド成果物置き場のみ。
- **目標**: `miscDepsJp/include` への依存を薄型化し、パス解決を共通化して x64 移行時の変更箇所を最小化する
- **作業内容**:
  - 環境変数 `REPO_ROOT` を用いたパス解決の共通ユーティリティ化（テスト／ビルドスクリプトで共通利用）
  - 直接参照の検討対象を「辞書・DLL」に限定し、`sys.path`/`PYTHONPATH` やシンボリックリンク活用を将来の選択肢として評価（Python ソースは既に `source/` に集約済み）
  - 設定ファイル経由の取得は優先度低で「将来検討」とし、まず共通ユーティリティ化で対応
- **削減効果**:
  - `miscDepsJp/source` 廃止後のフォルダ構造をさらに簡素化し、パス解決ロジックを一元化
  - x64 移行時のパス変更を最小限にし、辞書・DLL 参照の切替箇所を限定
- **検証の観点（直接参照を試す場合）**:
  - jp smoke test / launcher / `scons dist` が成功すること
  - `kgs_addon` など既存ビルドスクリプトの期待パスを壊さないこと

### Phase 4: 純 Python 化とビルドプロセスの最終的な単純化（長期）

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
