# nvaccess/beta マージリハーサル記録（2025-12-27）

## 概要

このドキュメントは、betajp-251227 ブランチから nvaccess/beta をマージするリハーサル（dry-run）の結果を記録したものです。

## 実行環境

- **日時**: 2025年12月27日
- **ベースブランチ**: betajp-251227
- **マージ元**: nvaccess/beta
- **nvaccess/beta の最新コミット**: `1cee6d93c` (Pass 0 instead of None to VBuf_getControlFieldNodeWithIdentifier #19365)

## マージコマンド

```powershell
git merge --no-commit --no-ff --allow-unrelated-histories nvaccess/beta
```

**注**: `--allow-unrelated-histories` が必要でした。これは、betajp-251227 と nvaccess/beta が unrelated histories（関連のない履歴）を持っているためです。

## コンフリクト統計

### 総コンフリクト数

**436ファイル** にコンフリクトが発生しました。

### カテゴリ別コンフリクト数

1. **CI/ワークフロー関連**: 約 10-15 ファイル
   - `.github/workflows/testAndPublish.yml`（最重要）
   - `.github/workflows/add-new-language.yml`
   - `.github/workflows/assign-milestone-on-close.yml`
   - `.github/workflows/fetch-crowdin-translations.yml`
   - その他のワークフローファイル

2. **サブモジュール関連**: 約 10 ファイル
   - `include/detours`
   - `include/espeak`
   - `include/ia2`
   - `include/javaAccessBridge32`
   - `include/liblouis`
   - `include/nvda-cldr`
   - `include/nvda-mathcat`
   - `include/sonic`
   - `include/w3c-aria-practices`
   - `include/wil`
   - `miscDeps`
   - `.vscode`

3. **ソースコード関連**: 約 200-250 ファイル
   - `source/` 配下の多数のファイル
   - `nvdaHelper/` 配下のファイル
   - `tests/` 配下のファイル

4. **翻訳ファイル関連**: 約 100-150 ファイル
   - `source/locale/*/LC_MESSAGES/nvda.po`（全言語）
   - `user_docs/*/changes.xliff`
   - `user_docs/*/userGuide.xliff`

5. **設定ファイル関連**: 約 20-30 ファイル
   - `.python-versions`
   - `.editorconfig`
   - `.gitignore`
   - `.pre-commit-config.yaml`
   - `pyproject.toml`
   - `uv.lock`
   - `sconstruct`

6. **ドキュメント関連**: 約 30-40 ファイル
   - `projectDocs/` 配下のファイル
   - `readme.md`
   - `AGENTS.md`
   - `CODE_OF_CONDUCT.md`

## 重要なコンフリクトファイル（優先度順）

### 優先度1（高）: ビルドシステム・CI

1. **`.github/workflows/testAndPublish.yml`**
   - 最重要: CI パイプラインの設定
   - JP パッチ（`# BEGIN/END JP PATCH`）の再適用が必要
   - 参照: `projectDocs/jp/merge-plan-beta-2025-11.md` の「作業段階 3」

2. **`sconstruct`**
   - SCons ビルドシステムの設定
   - JP 固有のターゲット（`jtalkPrep`, `jtalkSync` など）の維持が必要

3. **`.python-versions`**
   - Python バージョン指定
   - 現在: `cpython-3.11.9-windows-x86-none` (betajp-251227)
   - 上流: `cpython-3.13.9-windows-x86_64-none` (nvaccess/beta)
   - **注意**: x64 移行のタイミングで更新が必要

4. **`uv.lock`**
   - 依存関係のロックファイル
   - コンフリクト解決後に `uv lock --upgrade` で再生成が必要

### 優先度2（高）: サブモジュール

- すべてのサブモジュール（`include/*`, `miscDeps`）でコンフリクト
- 上流のコミットを採用する方針（`merge-plan-beta-2025-11.md` 参照）

### 優先度3（中）: ソースコード

1. **`source/braille.py`**
   - JP 固有の変更（`_nvdajp()`, `rowHeaderText/columnHeaderText`）の維持が必要
   - 参照: `merge-plan-beta-2025-11.md` の「作業段階 4.2」

2. **`source/gui/__init__.py`**
   - JP 固有のアイコンパス（`nvdajp3.ico`）とドネーションURLの維持が必要

3. **`source/installer.py`**
   - JP 固有のアイコンパスの維持が必要

4. **`source/synthDriverHandler.py`**
   - jtalk の優先順位の維持が必要

5. **`nvdaHelper/archBuild_sconscript`**
   - eSpeak ビルド条件の解決が必要
   - 参照: `merge-plan-beta-2025-11.md` の「作業段階 2.2」

### 優先度4（中～低）: 翻訳ファイル

- `source/locale/ja/LC_MESSAGES/nvda.po`
  - 大量のコンフリクト（約 35,000 行）
  - `msgmerge` で上流 pot に追随する必要がある
  - JP 固有の追加翻訳（IME 関連など）の維持が必要

### 優先度5（低）: ドキュメント・その他

- `projectDocs/` 配下のファイル
- `readme.md`
- `AGENTS.md`（JP 固有ファイルなので上流には存在しない）

## 観察事項

### 1. 大量の削除ファイル

マージリハーサルで、以下の JP 固有ファイルが削除対象として検出されました：

- `jptools/` 配下の多くのファイル（JP 固有のビルドツール）
- `miscDepsJp/` 配下の多くのファイル（JP 固有の依存関係）
- `source/synthDrivers/jtalk/` 配下のファイル（JP 固有の JTalk ドライバー）
- `source/jp*.py`（JP 固有のユーティリティ）

**注意**: これらは実際には削除すべきではありません。マージ時に適切に保護する必要があります。

### 2. 新規追加ファイル

nvaccess/beta から以下の新規ファイルが追加されます：

- `source/_localCaptioner/`（ローカル画像キャプション機能）
- `source/screenCurtain/`（スクリーンカーテン機能）
- `source/mathPres/MathCAT/`（MathCAT 数式プレゼンテーション）
- その他多数の新機能

### 3. Python 3.13 x64 への移行

- `.python-versions` が `cpython-3.13.9-windows-x86_64-none` に変更
- これは x64 移行のタイミングで対応が必要

## 次のステップ

### 即座に実施すべきこと

1. **マージ戦略の確認**
   - `projectDocs/jp/merge-plan-beta-2025-11.md` の手順に従う
   - 小さなPR単位で段階的に進める

2. **JP 固有ファイルの保護**
   - `jptools/`, `miscDepsJp/`, `source/synthDrivers/jtalk/` などの JP 固有ファイルが削除されないように注意

3. **コンフリクト解決の優先順位**
   - 優先度1（ビルドシステム・CI）から着手
   - 各段階でテスト通過を確認

### 段階的な実施計画

**参照**: `merge-plan-beta-2025-11.md` の作業段階 1-6 を参照

1. **Phase 1: 基盤整備**（`merge-plan-beta-2025-11.md` の「作業段階 1-2」）
   - サブモジュールの更新（上流のコミットを採用）
   - ビルドシステムの更新（NVDAHelper パッケージ化、archBuild_sconscript）
   - `.python-versions` と `uv.lock` の解決（**注意**: x64 移行のタイミングで更新）

2. **Phase 2: CI/ワークフロー**（`merge-plan-beta-2025-11.md` の「作業段階 3」）
   - `testAndPublish.yml` の更新（上流ファイルをベースに、JP パッチを最小限に再適用）
   - **参照**: `merge-issues-beta-2025-11.md` の「CI 上の具体対応（YAML 最小差分方針）」
   - JP パッチ箇所:
     - トリガー: ブランチ名を `betajp`/`releasejp` に変更
     - Python/Arch: 現在は 3.11/x86 を維持（x64 移行時に対応）
     - `ci/scripts/tests/beforeTests.ps1` の呼び出し
     - crowdin upload ジョブの無効化
     - JP 固有テスト（jpSmokeTests）の追加

3. **Phase 3: ソースコード**（`merge-plan-beta-2025-11.md` の「作業段階 4」）
   - JP 固有変更の再適用
     - `source/braille.py`: `_nvdajp()`, `rowHeaderText/columnHeaderText` の維持
     - `source/gui/__init__.py`, `source/installer.py`: JP 固有のアイコンパスとドネーションURLの維持
     - `source/synthDriverHandler.py`: jtalk の優先順位の維持
   - **参照**: `merge-issues-beta-2025-11.md` の「主要な論点と解決方針」
   - テストの更新

4. **Phase 4: 翻訳ファイル**（`merge-plan-beta-2025-11.md` の「作業段階 6」）
   - `nvda.po` のマージ（`msgmerge` で上流 pot に追随）
   - JP 固有翻訳の維持（IME 関連など）
   - **参照**: `merge-issues-beta-2025-11.md` の「翻訳ファイル（po）の大規模衝突」

### 検証手順（各 Phase で実施）

**参照**: `merge-issues-beta-2025-11.md` の「検証手順（ローカル）」

- 型チェック: `ci/scripts/tests/typeCheck.ps1`
- Lint: `uv run ruff format --check && uv run ruff check`
- 最小ビルド: `scons source --all-cores`
- 単体テスト: `rununittests.bat`（`uv --group unit-tests` 使用）
- System tests: `ci/scripts/tests/systemTests.ps1`（要 `ci/scripts/tests/beforeTests.ps1`）
- JP smoke tests: `jptools/runJpSmokeTests.ps1 -SkipInstall -SkipOverlay`

## 2025年11月の記録との比較

### 参考になる点

**`projectDocs/jp/merge-plan-beta-2025-11.md` と `projectDocs/jp/merge-conflicts-detailed-2025-11.md` は非常に参考になります**：

1. **重要なファイルの解決方針が詳細に記載されている**
   - `testAndPublish.yml`（作業段階 3）: 上流ファイルをベースに、JP パッチを最小限に再適用する戦略
   - `source/braille.py`（作業段階 4.2）: JP 固有の `_nvdajp()` や `rowHeaderText/columnHeaderText` の維持方法
   - `source/gui/__init__.py`, `source/installer.py`（作業段階 4.3）: JP 固有のアイコンパスとドネーションURLの維持方法
   - `source/synthDriverHandler.py`（作業段階 4.4）: jtalk の優先順位の維持方法
   - `nvdaHelper/archBuild_sconscript`（作業段階 2.2）: eSpeak ビルド条件の解決方法

2. **段階的な解決手順が明確**
   - 作業段階 1-6 に分かれており、依存関係を考慮した順序が明確
   - 各段階での検証方法も記載されている

3. **コンフリクトの詳細な記録**
   - `merge-conflicts-detailed-2025-11.md` には、各コンフリクトファイルの具体的な内容が記録されている
   - 特に `testAndPublish.yml` の22箇所のコンフリクト位置が記録されている

### 違いと注意点

1. **規模の違い**
   - **2025年11月**: 17ファイルのコンフリクト（通常のマージ）
   - **2025年12月27日**: 436ファイルのコンフリクト（unrelated histories のマージ）
   - 今回の方が規模が大きいが、**重要なファイルのコンフリクトパターンは類似している**

2. **Python バージョンの違い**
   - **2025年11月**: Python 3.13 x64 への移行を前提（PR #573）
   - **2025年12月27日**: 現在は Python 3.11 x86 を維持（x64 移行は今後の目標）
   - `.python-versions` の解決方針は、x64 移行のタイミングで適用する必要がある

3. **解決済みの項目**
   - PR #573 で多くの作業が完了している（作業段階 1-5）
   - ただし、今回の unrelated histories マージでは、これらの解決済み項目も再度確認が必要

### 推奨される活用方法

1. **`merge-plan-beta-2025-11.md` を主要な参照として使用**
   - 各作業段階の解決方針を参照
   - 特に作業段階 3（CI/ワークフロー）と作業段階 4（ソースコード）は重要

2. **`merge-conflicts-detailed-2025-11.md` で具体的なコンフリクト内容を確認**
   - 重要なファイル（`testAndPublish.yml`, `source/braille.py` など）のコンフリクトパターンを参照
   - ただし、行番号は変わっている可能性があるため、内容のパターンを参考にする

3. **段階的な解決手順に従う**
   - 小さなPR単位で進める
   - 各段階でテスト通過を確認
   - 品質保証原則に従う

## 参照ドキュメント

### 主要な参照（優先度順）

1. **`projectDocs/jp/merge-plan-beta-2025-11.md`** - **最重要**
   - 段階的な解決手順（作業段階 1-6）
   - 各コンフリクトファイルの具体的な解決方法
   - 検証手順と完了条件

2. **`projectDocs/jp/merge-issues-beta-2025-11.md`** - **重要**
   - 主要な論点と解決方針が簡潔にまとまっている
   - CI 上の具体対応（YAML 最小差分方針）
   - 検証手順（ローカル）
   - 各問題点に対する具体的な解決方針
   - **特に有用な情報**:
     - CI 行列とトリガーの整合方針
     - nvdaHelper 構成変更の解決方針
     - Braille 表示ロジックの JP 拡張の維持方法
     - 翻訳ファイル（po）の大規模衝突の解決方針
     - IAccessible2Lib/ia2.tlb の配置変更（JP 独自オーバーレイの削除）

3. **`projectDocs/jp/merge-conflicts-detailed-2025-11.md`** - **参考**
   - 具体的なコンフリクト内容の記録
   - 各コンフリクトファイルの行番号と内容
   - 特に `testAndPublish.yml` の22箇所のコンフリクト位置

4. **`projectDocs/jp/merge-issues-beta-2025-11.meta.md`** - **参考**
   - コンフリクト検出コマンド（PowerShell）
   - 再現性のための情報
   - 今回のリハーサルでも同様のコマンドが使用可能
   - **有用なコマンド例**:
     - `rg -n "^(<<<<<<<|=======|>>>>>>>)" -S` - すべてのコンフリクトマーカー行を一覧
     - ファイルごとの最初の衝突位置を要約するスクリプト
     - 個別ファイル（workflow）の衝突だけ確認するコマンド

### その他の参照

- ロードマップ: `projectDocs/jp/roadmap.md`
- エージェント向け: `AGENTS.md`
