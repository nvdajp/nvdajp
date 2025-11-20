# NVDA 日本語版 ドキュメント ハブ（JP Docs Hub）

このフォルダは、日本語版に固有の運用・方針・進行中タスクを集約する着地点です。人間開発者向けの恒常情報は `readme-nvdajp.md` に、本家版の一般開発情報は `projectDocs/dev/createDevEnvironment.md` を参照してください。

## 目的と役割

* 日本語版固有の情報の入口（リンク集と短い要約）
* 進行中タスクのスコープと優先度の明示（長文の議論は Issue/PR へ）
* 作業の最短コマンドと禁則の共有（詳細手順は各ドキュメントへ誘導）

## ロードマップ（要約）

* CI/ビルド基盤を整合（Refs: `#539`, Part of `#530`）
* Python 3.13 対応 x64 ビルド対応（日本語版固有モジュールの対応を含む）

## CI/ビルド クイックスタート

* 型チェックのみ（本家版寄せ・安全導入）: `.github/workflows/nvbeta-typecheck.yml`
* 包括パイプラインにも `typeCheck` ジョブを追加（3.13 x64／pyright）
* lint（ruff）は包括パイプラインにも追加（`lint` ジョブ）
* 日本語版フルビルド・配布系: `.github/workflows/testAndPublish.yml`
* ローカル最小ビルド例: `scons --help` を確認し、通常は `scons source dist launcher --all-cores`
* 単体/システムテスト: `ci/scripts/tests/unitTests.ps1`、`ci/scripts/tests/systemTests.ps1`
* **PR CI 監視**: `ci/scripts/monitor-pr-ci.ps1 -PrNumber <番号>` (単回) または `-Watch` (継続監視)
  * CI チェックの状態を確認し、失敗時に自動分析とアドバイスを提供

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
* 日本語版 CI/ビルド基盤: `projectDocs/jp/ci`
* エージェント／自動化向けの運用ルール: `AGENTS.md`

## 用語: JP オーバレイ（JP overlay）

* 定義: `miscDepsJp/source` 配下のファイルを、リポジトリ直下の `source/` にコピーして重ねる処理。
  * 実行スクリプト: `jptools/setup_miscdeps_overlay.py`（実行時の作業ディレクトリは `miscDepsJp/`）。
* 現在は特別な除外は設けず、`miscDepsJp/source` の内容をそのまま重ねます（ポリシーとして不要なファイルは配置しない）。
* いつ走るか:
  * `scons source` 実行時に、SCons が `miscdepsjp` エイリアスを依存として自動実行（`sconstruct` に設定）。
  * `miscdepsjp` エイリアスの明示実行でも可。
* 性質:
  * 冪等（同じファイルを繰り返し重ねても破綻しない）。
  * 日本語版のビルドでは前提となる処理（無効化すると正しくビルドできない）。
* クリーン:
  * `scons -c`（クリーン）で、オーバレイで `source/` にコピーしたファイルも削除されるよう Clean を配線済み。
  * 元の英語版ファイルへ「戻す」場合は、`git checkout -- source/<path>` など VCS 操作で復元する。

## 進行中タスク

* `#530`: 本家 2026.1 の日本語版へのマージ
* `#539`: merge nvaccess beta (3.13 x64)

本READMEは短い要約とリンク集を維持し、詳細は各ファイルと Issue/PR 側で管理します。
