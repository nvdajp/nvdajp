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

1. **Phase 1: 基盤整備**（`merge-plan-beta-2025-11.md` の「作業段階 1-2」）
   - サブモジュールの更新
   - ビルドシステムの更新

2. **Phase 2: CI/ワークフロー**（`merge-plan-beta-2025-11.md` の「作業段階 3」）
   - `testAndPublish.yml` の更新
   - JP パッチの最小化

3. **Phase 3: ソースコード**（`merge-plan-beta-2025-11.md` の「作業段階 4」）
   - JP 固有変更の再適用
   - テストの更新

4. **Phase 4: 翻訳ファイル**（`merge-plan-beta-2025-11.md` の「作業段階 6」）
   - `nvda.po` のマージ
   - JP 固有翻訳の維持

## 参照

- 詳細なマージ計画: `projectDocs/jp/merge-plan-beta-2025-11.md`
- コンフリクト記録（2025-11）: `projectDocs/jp/merge-conflicts-detailed-2025-11.md`
- 問題点まとめ: `projectDocs/jp/merge-issues-beta-2025-11.md`
- ロードマップ: `projectDocs/jp/roadmap.md`

