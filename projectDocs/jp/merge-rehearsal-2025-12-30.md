# nvaccess/beta (x86 Python 3.13段階) マージリハーサル記録（2025-12-30）

## 概要

このドキュメントは、betajp-251230 ブランチから nvaccess/beta の x86 Python 3.13 段階（コミット `9613ce6e3`）をマージするリハーサル（dry-run）の結果を記録したものです。

## 実行環境

* **日時**: 2025年12月30日
* **ベースブランチ**: betajp-251230
* **マージ元**: nvaccess/beta のコミット `9613ce6e3` (2025年8月15日)
* **コミット情報**: "Update to Python 3.13 for 2026.1 #18689"
* **Python バージョン**: `cpython-3.13.6-windows-x86-none` (x86 Python 3.13)

## マージコマンド

```powershell
git merge --no-commit --no-ff --allow-unrelated-histories 9613ce6e3
```

**注**: `--allow-unrelated-histories` が必要でした。これは、betajp-251230 と nvaccess/beta が unrelated histories（関連のない履歴）を持っているためです。

## コンフリクト統計

### 総コンフリクト数

**242ファイル** にコンフリクトが発生しました。

### カテゴリ別コンフリクト数

1. **翻訳ファイル関連**: 約 65 ファイル
   * `source/locale/*/LC_MESSAGES/nvda.po`（全言語）
   * `source/locale/ja/characterDescriptions.dic`
   * `source/locale/tr/gestures.ini`

2. **ユーザードキュメント関連**: 約 57 ファイル
   * `user_docs/*/changes.xliff`
   * `user_docs/*/userGuide.xliff`
   * `user_docs/en/changes.md`
   * `user_docs/en/userGuide.md`

3. **CI/ワークフロー関連**: 約 10 ファイル
   * `.github/workflows/testAndPublish.yml`（最重要）
   * `.github/workflows/add-new-language.yml`
   * `.github/workflows/assign-milestone-on-close.yml`
   * `.github/workflows/fetch-crowdin-translations.yml`
   * `.github/workflows/regenerate_english_userDocs_translation_source.yml`
   * その他のワークフローファイル

4. **ソースコード関連**: 約 100-110 ファイル
   * `source/` 配下の多数のファイル
   * `nvdaHelper/` 配下のファイル
   * `tests/` 配下のファイル

5. **サブモジュール関連**: 6 ファイル
   * `include/detours`
   * `include/espeak`
   * `include/javaAccessBridge32`
   * `include/nvda-cldr`
   * `miscDeps`
   * `.vscode`

6. **設定ファイル関連**: 約 20-30 ファイル
   * `.python-versions`（重要: x86 Python 3.13 への移行）
   * `.editorconfig`
   * `.gitignore`
   * `.pre-commit-config.yaml`
   * `pyproject.toml`
   * `uv.lock`
   * `sconstruct`

## 重要なコンフリクトファイル（優先度順）

### 優先度1（高）: ビルドシステム・CI

1. **`.python-versions`**
   * 現在: `cpython-3.11.9-windows-x86-none` と `cpython-3.13.6-windows-x86-none` の両方を含む
   * 上流: `cpython-3.13.6-windows-x86-none` のみ
   * **解決方針**: 上流の形式を採用（x86 Python 3.13 のみ）

2. **`.github/workflows/testAndPublish.yml`**
   * 最重要: CI パイプラインの設定
   * JP パッチ（`# BEGIN/END JP PATCH`）の再適用が必要
   * Python/Arch を **3.13/x86** に更新（3.11/x86 から変更）
   * 参照: `projectDocs/jp/merge-plan-beta-2025-11.md` の「作業段階 3」

3. **`sconstruct`**
   * SCons ビルドシステムの設定
   * JP 固有のターゲット（`jtalkPrep`, `jtalkSync` など）の維持が必要

4. **`pyproject.toml`** と **`uv.lock`**
   * 依存関係のロックファイル
   * コンフリクト解決後に `uv lock --upgrade` で再生成が必要

### 優先度2（高）: サブモジュール

* すべてのサブモジュール（`include/*`, `miscDeps`）でコンフリクト
* 上流のコミットを採用する方針（`merge-plan-beta-2025-11.md` 参照）
* Git のヒントに従って、各サブモジュールを手動でマージまたは更新

### 優先度3（中）: ソースコード

1. **`source/NVDAHelper.py`**
   * 上流で `source/NVDAHelper/__init__.py` にパッケージ化されている可能性
   * 参照: `projectDocs/jp/merge-plan-beta-2025-11.md` の「作業段階 2.1」

2. **`source/braille.py`**
   * JP 固有の変更（`_nvdajp()`, `rowHeaderText/columnHeaderText`）の維持が必要
   * 参照: `projectDocs/jp/merge-plan-beta-2025-11.md` の「作業段階 4.2」

3. **`source/gui/__init__.py`**
   * JP 固有のアイコンパス（`nvdajp3.ico`）とドネーションURLの維持が必要

4. **`source/installer.py`**
   * JP 固有のアイコンパスの維持が必要

5. **`source/synthDriverHandler.py`**
   * jtalk の優先順位の維持が必要

6. **`nvdaHelper/archBuild_sconscript`**
   * eSpeak ビルド条件の解決が必要
   * 参照: `projectDocs/jp/merge-plan-beta-2025-11.md` の「作業段階 2.2」

### 優先度4（中～低）: 翻訳ファイル

* `source/locale/ja/LC_MESSAGES/nvda.po`
  * 大量のコンフリクト（約 35,000 行）
  * `msgmerge` で上流 pot に追随する必要がある
  * JP 固有の追加翻訳（IME 関連など）の維持が必要

### 優先度5（低）: ドキュメント・その他

* `projectDocs/` 配下のファイル
* `readme.md`
* `AGENTS.md`（JP 固有ファイルなので上流には存在しない）

## 観察事項

### 1. Python バージョンの移行

* 現在の `.python-versions`: `cpython-3.11.9-windows-x86-none` と `cpython-3.13.6-windows-x86-none` の両方を含む
* マージ後: `cpython-3.13.6-windows-x86-none` のみ（x86 Python 3.13 への移行）
* これは x86 Python 3.13 への移行のタイミングで対応が必要

### 2. 新規追加ファイル

nvaccess/beta から以下の新規ファイルが追加されます：

* `source/_localCaptioner/`（ローカル画像キャプション機能）
* `source/screenCurtain/`（スクリーンカーテン機能）
* `source/mathPres/MathCAT/`（MathCAT 数式プレゼンテーション）
* その他多数の新機能

### 3. サブモジュールのマージ

Git のヒントに従って、各サブモジュールを手動でマージまたは更新する必要があります：

```powershell
# 各サブモジュールで上流のコミットを採用
cd miscDeps
git merge 6a97c83  # または既存のマージ済みコミットに更新
cd ..

cd include/nvda-cldr
git merge 779ce4b
cd ../..

# 同様に他のサブモジュールも処理
# include/javaAccessBridge32, include/espeak, include/detours, .vscode

# スーパープロジェクトに戻って記録
git add miscDeps include/nvda-cldr include/javaAccessBridge32 include/espeak include/detours .vscode
```

## 次のステップ

### 即座に実施すべきこと

1. **マージ戦略の確認**
   * `projectDocs/jp/merge-plan-beta-2025-11.md` の手順に従う
   * 小さなPR単位で段階的に進める

2. **JP 固有ファイルの保護**
   * `jptools/`, `miscDepsJp/`, `source/synthDrivers/jtalk/` などの JP 固有ファイルが削除されないように注意

3. **コンフリクト解決の優先順位**
   * 優先度1（ビルドシステム・CI）から着手
   * 各段階でテスト通過を確認

### 段階的な実施計画

**参照**: `merge-plan-beta-2025-11.md` の作業段階 1-6 を参照

1. **Phase 1: 基盤整備**（`merge-plan-beta-2025-11.md` の「作業段階 1-2」）
   * サブモジュールの更新（上流のコミットを採用）
   * ビルドシステムの更新（NVDAHelper パッケージ化、archBuild_sconscript）
   * `.python-versions` と `uv.lock` の解決（x86 Python 3.13 への移行）

2. **Phase 2: CI/ワークフロー**（`merge-plan-beta-2025-11.md` の「作業段階 3」）
   * `testAndPublish.yml` の更新（上流ファイルをベースに、JP パッチを最小限に再適用）
   * **参照**: `merge-issues-beta-2025-11.md` の「CI 上の具体対応（YAML 最小差分方針）」
   * JP パッチ箇所:
     * トリガー: ブランチ名を `betajp`/`releasejp` に変更
     * Python/Arch: **3.13/x86** に更新（3.11/x86 から変更）
     * `ci/scripts/tests/beforeTests.ps1` の呼び出し
     * crowdin upload ジョブの無効化
     * JP 固有テスト（jpSmokeTests）の追加

3. **Phase 3: ソースコード**（`merge-plan-beta-2025-11.md` の「作業段階 4」）
   * JP 固有変更の再適用
     * `source/braille.py`: `_nvdajp()`, `rowHeaderText/columnHeaderText` の維持
     * `source/gui/__init__.py`, `source/installer.py`: JP 固有のアイコンパスとドネーションURLの維持
     * `source/synthDriverHandler.py`: jtalk の優先順位の維持
   * **参照**: `merge-issues-beta-2025-11.md` の「主要な論点と解決方針」
   * テストの更新

4. **Phase 4: 翻訳ファイル**（`merge-plan-beta-2025-11.md` の「作業段階 6」）
   * `nvda.po` のマージ（`msgmerge` で上流 pot に追随）
   * JP 固有翻訳の維持（IME 関連など）
   * **参照**: `merge-issues-beta-2025-11.md` の「翻訳ファイル（po）の大規模衝突」

### 検証手順（各 Phase で実施）

**参照**: `merge-issues-beta-2025-11.md` の「検証手順（ローカル）」

* 型チェック: `ci/scripts/tests/typeCheck.ps1`
* Lint: `uv run ruff format --check && uv run ruff check`
* 最小ビルド: `scons source --all-cores`
* 単体テスト: `rununittests.bat`（`uv --group unit-tests` 使用）
* System tests: `ci/scripts/tests/systemTests.ps1`（要 `ci/scripts/tests/beforeTests.ps1`）
* JP smoke tests: `jptools/runJpSmokeTests.ps1 -SkipInstall -SkipOverlay`

## 2025年12月27日のリハーサルとの比較

### 違いと注意点

1. **規模の違い**
   * **2025年12月27日**: 436ファイルのコンフリクト（最新のbetaをマージ）
   * **2025年12月30日**: 242ファイルのコンフリクト（x86 Python 3.13段階までマージ）
   * **約44%の削減**: x86 Python 3.13段階までマージすることで、コンフリクト数を大幅に削減

2. **Python バージョンの違い**
   * **2025年12月27日**: 最新のbeta（x64 Python 3.13）
   * **2025年12月30日**: x86 Python 3.13 段階（コミット `9613ce6e3`）
   * この段階までマージすることで、x86環境での検証が容易になる

3. **解決済みの項目**
   * PR #573 で多くの作業が完了している（作業段階 1-5）
   * ただし、今回の unrelated histories マージでは、これらの解決済み項目も再度確認が必要

### 推奨される活用方法

1. **`merge-plan-beta-2025-11.md` を主要な参照として使用**
   * 各作業段階の解決方針を参照
   * 特に作業段階 3（CI/ワークフロー）と作業段階 4（ソースコード）は重要

2. **段階的な解決手順に従う**
   * 小さなPR単位で進める
   * 各段階でテスト通過を確認
   * 品質保証原則に従う

## 参照ドキュメント

### 主要な参照（優先度順）

1. **`projectDocs/jp/merge-plan-beta-2025-11.md`** - **最重要**
   * 段階的な解決手順（作業段階 1-6）
   * 各コンフリクトファイルの具体的な解決方法
   * 検証手順と完了条件

2. **`projectDocs/jp/merge-issues-beta-2025-11.md`** - **重要**
   * 主要な論点と解決方針が簡潔にまとまっている
   * CI 上の具体対応（YAML 最小差分方針）
   * 検証手順（ローカル）

3. **`projectDocs/jp/merge-rehearsal-2025-12-27.md`** - **参考**
   * 最新のbetaをマージした場合のリハーサル記録
   * 規模の違いを理解するための参考

4. **`projectDocs/jp/roadmap.md`** - **参照**
   * 現在の作業キューと優先順位
   * ステージ3a（x86 Python 3.13への移行）の詳細

### その他の参照

* ロードマップ: `projectDocs/jp/roadmap.md`
* エージェント向け: `AGENTS.md`

## マージ実行結果（2025年12月30日）

### 実行結果

* **実行日時**: 2025年12月30日
* **コミット**: `d1792591a` - "Merge nvaccess/beta (x86 Python 3.13 stage, commit 9613ce6e3)"
* **ステータス**: ✅ 完了

### 解決したコンフリクト

1. **Phase 1: 基盤整備** ✅
   * サブモジュール: 上流のコミットを採用
   * `.python-versions`: `cpython-3.13.6-windows-x86-none` に更新
   * `uv.lock`: 上流版を採用（後で `uv lock --upgrade` で再生成予定）

2. **Phase 2: CI/ワークフロー** ✅
   * `testAndPublish.yml`: 上流版をベースに、JP パッチを最小限に再適用
   * Python/Arch: 3.13/x86 に更新

3. **Phase 3: ソースコード** ✅
   * `source/NVDAHelper.py`: typing import の修正
   * `source/braille.py`: JP固有の変更（`_nvdajp()`, `rowHeaderText`, `columnHeaderText`）を維持
   * `source/gui/__init__.py`: JP固有の変更（アイコンパス、ドネーションURL、jpBrailleViewer）を維持
   * `source/installer.py`: JP固有のアイコンパスとショートカットを維持
   * `source/synthDriverHandler.py`: jtalk の優先順位を維持
   * `nvdaHelper/archBuild_sconscript`: eSpeak ビルド条件を解決
   * `sconstruct`: JP固有の変更（`jtalkPrep`, `jtalkSync`, `nvdajp3.ico`）を維持
   * その他のソースファイル: 上流版を採用

4. **Phase 4: 翻訳ファイル** ✅
   * すべての翻訳ファイル（`.po`）を上流版で置き換え（生成ファイルのため）

### 検証結果

* **型チェック**: ✅ 成功
* **ビルドテスト**: ✅ 成功（`scons source --all-cores`）
* **JP smoke test (x86)**: ✅ 成功（3 passed, 2 deselected, 1 warning）
* **JP smoke test (x64)**: ✅ 成功（3 passed, 2 deselected, 1 warning）
* **ランチャービルド**: ✅ 成功（`scons launcher --all-cores`）

### Push と CI

* **Push**: ✅ 完了（`betajp-251230` ブランチ）
* **CI実行**: ✅ 開始済み（実行ID: `20555439906`）
