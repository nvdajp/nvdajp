# NVDA 日本語版 ドキュメント ハブ（JP Docs Hub）

このフォルダは、日本語版に固有の運用・方針・進行中タスクを集約する着地点です。人間開発者向けの恒常情報は `readme-nvdajp.md` に、本家版の一般開発情報は `projectDocs/dev/createDevEnvironment.md` を参照してください。

## 目的と役割

* 日本語版固有の情報の入口（リンク集と短い要約）
* 進行中タスクのスコープと優先度の明示（長文の議論は Issue/PR へ）
* 作業の最短コマンドと禁則の共有（詳細手順は各ドキュメントへ誘導）

## ロードマップ（要約）

* CI/ビルド基盤を整合（Refs: `#539`, Part of `#530`）
* Python 3.13 x64 対応は別ブランチ（x64実験系）で管理。現ブランチは x86 を維持。

## CI/ビルド クイックスタート

* 型チェックのみ（本家版寄せ・安全導入）: `.github/workflows/nvbeta-typecheck.yml`
* 注: 3.13 x64 対応は別ブランチで実施。このブランチは x86 ビルドを維持。
* lint（ruff）は包括パイプラインにも追加（`lint` ジョブ）
* 日本語版フルビルド・配布系: `.github/workflows/testAndPublish.yml`
* ローカル最小ビルド例: `scons --help` を確認し、通常は `scons source dist launcher --all-cores`
* 単体/システムテスト: `ci/scripts/tests/unitTests.ps1`、`ci/scripts/tests/systemTests.ps1`
* **PR CI 監視**: `ci/scripts/monitor-pr-ci.ps1 -PrNumber <番号>` (単回) または `-Watch` (継続監視)
  * CI チェックの状態を確認し、失敗時に自動分析とアドバイスを提供

### Pre-commit のスキップ設定

`.pre-commit-config.yaml` の `ci` セクションでは、以下のフックが `pre-commit.ci` サービスでスキップされています：

* **`checkPo`**: PO ファイルのチェック（GitHub Actions の `checkPo` ジョブで実行）
* **`scons-source`**: Windows の scons スクリプトは Linux ベースの pre-commit.ci では実行不可
* **`checkPot`**: 翻訳文字列のチェック（GitHub Actions の `checkPot` ジョブで実行）
* **`unitTest`**: ユニットテスト（Python 環境が必要で、pre-commit.ci では設定不可）
* **`licenseCheck`**: ライセンス互換性チェック（テレメトリーに依存し、CI でブロックされる）
* **`pyright`**: 型チェック（pre-commit CI では動作しない）

これらのチェックは GitHub Actions のワークフロー（`.github/workflows/testAndPublish.yml`）で実行されるため、pre-commit.ci ではスキップされています。

### Pre-commit フックの詳細

`.pre-commit-config.yaml` で設定されているフックの一覧と説明：

#### 外部リポジトリのフック

* **pre-commit-hooks** (35-92行目): 基本チェック
  * `no-commit-to-branch`: 保護ブランチ（master, beta, rc）へのコミットを防止
  * `check-added-large-files`: 500KB 以上の大きなファイルの追加を検出（PO ファイル、TTF フォント、.dic、.sfd は除外）
  * `check-ast`: Python の構文チェック
  * `check-case-conflict`: 大文字小文字のみが異なるファイル名の衝突を検出（Windows ファイルシステム向け）
  * `check-merge-conflict`: マージコンフリクトの解決残り（`<<<<<<<`, `=======`, `>>>>>>>`）を検出
  * `debug-statements`: Python のデバッグ文（`breakpoint()` など）を検出
  * `trailing-whitespace`: 行末の空白を削除（**注意**: 現時点で nvdajp では無効化されています）
  * `end-of-file-fixer`: ファイル末尾の改行を1つに統一（**注意**: 現時点で nvdajp では無効化されています）
  * `fix-byte-order-marker`: UTF-8 BOM を削除（**注意**: 現時点で nvdajp では無効化されています）
  * `check-toml`, `check-yaml`, `check-xml`: 各形式のファイルの構文チェック
  * `check-vcs-permalinks`: バージョン管理システムへの永続的なリンクをチェック
  * `check-illegal-windows-names`: Windows の予約ファイル名（CON, PRN など）を検出
  * `name-tests-test`: テストファイルが `test_*.py` の命名規則に従っているかチェック

* **add-trailing-comma** (94-100行目): 関数引数やリスト項目の末尾にカンマを追加
  * Ruff がインデント/改行のフォーマットを保持するために必要

* **ruff** (102-110行目): Python の lint と format
  * `ruff`: コードの lint（`--fix` で自動修正）
  * `ruff-format`: コードのフォーマット

* **pyright** (112-116行目): 型チェック
  * Python の静的型チェック（pre-commit.ci ではスキップ）

* **uv-lock** (118-124行目): uv ロックファイルの検証
  * `uv.lock` ファイルが `pyproject.toml` と整合しているか確認

* **markdownlint-cli2** (126-131行目): Markdown の lint
  * Markdown ファイルの構文とスタイルをチェック（`--fix` で自動修正）
  * **注意**: 現時点で nvdajp では無効化されています（JP PATCH でコメントアウト）

#### ローカルフック

* **checkPo** (135-139行目): PO ファイルのチェック
  * `source/l10nUtil.py checkPo` を実行して翻訳ファイルのエラーを検出
  * pre-commit.ci ではスキップ（GitHub Actions で実行）

* **scons-source** (140-145行目): C/C++ ファイルのビルド
  * `scons source --all-cores` を実行して C/C++ ファイルが正しくビルドできるか確認
  * pre-commit.ci ではスキップ（Windows の scons スクリプトは Linux では実行不可）

* **checkPot** (146-152行目): 翻訳文字列のチェック
  * `scons checkPot --all-cores` を実行して翻訳文字列の整合性を確認
  * pre-commit.ci ではスキップ（GitHub Actions で実行）

* **unitTest** (153-158行目): ユニットテスト実行
  * `rununittests.bat` を実行してユニットテストを実行
  * pre-commit.ci ではスキップ（Python 環境が必要で設定不可）

* **licenseCheck** (159-165行目): ライセンス互換性チェック
  * `runlicensecheck.bat` を実行して pip 依存関係のライセンス互換性を確認
  * pre-commit.ci ではスキップ（テレメトリーに依存し、CI でブロックされる）

## ポリシー（抜粋）

* 本家版との差分は最小に保つ。差分は明示的な場所に集約する
* 可能な限り `SCons`/純 Python を優先し、`.cmd`/`7z`/`nmake` など外部依存は段階的に削減
* CI の前提（Python/ランナー/キャッシュ）は本家版に準拠する方針で段階導入
* 秘密情報（署名トークン等）は GitHub Secrets/Variables 経由。リポジトリへの直書き禁止
* 署名/配布はローカルで実施（CI は未署名）

## 開発方針（本家版準拠）

日本語版のコードも本家版の開発方針に準拠することを推奨します。詳細は `projectDocs/dev/codingStandards.md` を参照してください。

### 優先度の高い改善点

* **型ヒント**: すべての新規コードに PEP 484 形式の型ヒントを追加
* **ログ**: `print` の代わりに `logHandler.log` を使用
* **Docstring**: Sphinx 形式の docstring を追加（公開関数・クラス・メソッド）

### その他の推奨事項

* グローバル変数の削減（関数の引数として渡す、またはクラスにカプセル化）
* 単体テストの追加（統合テストに加えて）
* 後方互換性の考慮（`projectDocs/dev/deprecations.md` 参照）

詳細は `projectDocs/dev/codingStandards.md`、`projectDocs/dev/contributing.md` を参照してください。

## 関連ドキュメント

* 日本語版の恒常情報（人間向け）: `readme-nvdajp.md`
* 本家版の開発環境ガイド: `projectDocs/dev/createDevEnvironment.md`
* 本家版のプロダクトビジョン: `projectDocs/product_vision.md`
* 日本語点字出力テーブル: `projectDocs/jp/braille-ja-jp-comp6.md`
* **日本語入力メソッド（IME/TSF）の実装**: `projectDocs/jp/japanese-input-method-implementation.md`
* 日本語版 CI/ビルド基盤: `projectDocs/jp/ci`
* **miscDepsJp と JP overlay の現状と方針**: `projectDocs/jp/miscdepsjp-overlay-strategy.md`
* **コード署名を考慮したビルド依存関係**: `projectDocs/jp/code-signing-dependencies.md`
* **ビルドアーキテクチャ環境変数の方針**: `projectDocs/jp/build-architecture-environment-variables.md`
* TODO: **署名ビルドの冗長実行とログ運用**: `projectDocs/jp/todo_build_script_redundancy_and_logging.md`
* エージェント／自動化向けの運用ルール: `AGENTS.md`

## 用語集

### JP オーバレイ（JP overlay）

* **定義**: `miscDepsJp/source` 配下のファイルを、リポジトリ直下の `source/` にコピーして重ねる処理。
  * 実行スクリプト: `jptools/setup_miscdeps_overlay.py`（実行時の作業ディレクトリは `miscDepsJp/`）。
* **実行方法**:
  * `scons source` 実行時に、SCons が `miscdepsjp` エイリアスを依存として自動実行（`sconstruct` に設定）。
  * `miscdepsjp` エイリアスの明示実行でも可。
* **性質**:
  * 冪等（同じファイルを繰り返し重ねても破綻しない）。
  * 日本語版のビルドでは前提となる処理（無効化すると正しくビルドできない）。
  * 現在は特別な除外は設けず、`miscDepsJp/source` の内容をそのまま重ねます（ポリシーとして不要なファイルは配置しない）。
* **クリーン**:
  * `scons -c`（クリーン）で、オーバレイで `source/` にコピーしたファイルも削除されるよう Clean を配線済み。
  * 元の英語版ファイルへ「戻す」場合は、`git checkout -- source/<path>` など VCS 操作で復元する。

**現状の問題点と長期的な改善方針**については、`projectDocs/jp/miscdepsjp-overlay-strategy.md` を参照してください。

### ベンダーツリー（Vendor Tree）

* **定義**: 外部リポジトリから取り込んだコードを保持するディレクトリ。
* **現在の構成**: `miscDepsJp/include/` 配下に配置（python-jtalk、htsengineapi、libopenjtalk、libkuraji など）。
* **管理方法**: `miscDepsJp` フォルダ全体は PR #492 でメインリポジトリに統合され、`miscDepsJp/include/*` 配下のベンダーツリーは PR #582 で git subtree merge によりメインリポジトリに統合。サブモジュールではないため、`git submodule update` は不要。
* **更新方法**: 通常のGit操作（`git pull`、`git merge`等）で対応。

### SCons ターゲット

* **`scons jtalkPrep`**: JTalk DLLのビルドとペイロードへの配置を行う。DLLが存在する場合は再ビルドをスキップ。
* **`scons miscdepsjp`**: 日本語版固有のファイルを `source/` ディレクトリにオーバーレイする。`jtalkPrep` に依存。
* **`scons source`**: NVDA本体のビルド。`miscdepsjp` が自動的に実行される。

詳細は `projectDocs/jp/vendor-submodules.md` を参照してください。

## 進行中タスク

* `#530`: 本家 2026.1 の日本語版へのマージ
* `#539`: merge nvaccess beta（注: 3.13 x64 対応は別ブランチで実施）

本READMEは短い要約とリンク集を維持し、詳細は各ファイルと Issue/PR 側で管理します。
