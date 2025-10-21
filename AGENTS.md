# AGENTS.md — 日本語版向けエージェント手引き（最小）

このファイルは、リポジトリ内で自動化エージェント／スクリプトが守る最小限のルールと最短手順を示します。詳細な説明は人間向けドキュメントを参照してください。

## スコープ（Step 1）

- 目的: 3.11 x86 を維持したまま「本家版寄りのCI/ビルド基盤」に整合
- 除外: x64/arm64 切替、Java Access Bridge 64bit、Python 3.13 への移行
- 関連: Issue #539（Step 1）、Issue #530（本家版 2026.1 マージ全体）

## 禁則と優先

- 破壊的操作を避ける（履歴の書換は明示指示時のみ）
- 本家版との差分は最小化し、差分は明示的な場所に集約
- 可能な限り SCons / 純 Python を優先（.cmd / 7z / nmake 依存は削減）
- コードサイニング/配布は CI で行わない（Secrets を使用しない）。正式リリースはローカルで実施

## 最短コマンド

- 型チェック: `ci/scripts/tests/typeCheck.ps1`（Pyright）
- Lint（推奨）: `uv run ruff format --check && uv run ruff check`
- ビルド例: `scons source dist launcher --all-cores`

## CI とブランチ

- PR の base は通常 `betajp`
- `betajp` は日本語版の安定ブランチ。直接 push・試行錯誤は禁止。作業は必ずトピックブランチ→Pull Request（PR）で行うこと。
- ブランチ保護（推奨）: `betajp` に対して PR レビュー必須＋ステータスチェック必須（`allTestsPass`、`NVAccess Beta Aligned TypeCheck (3.11 x86)` など）。
- CIでの配布系ジョブ（release 等）はデフォルト無効（フラグや条件で明示的に有効化）とし、Secrets を必要とする運用は避ける。

## testAndPublish の上流追従（方針）

- 目的: 本家 `testAndPublish.yml` をそのまま取り込み、JP 固有は最小パッチの注入に限定する。
- 原則:
  - JP 固有の前処理・後処理は `ci/scripts/` のスクリプトへ寄せる（YAML にはスクリプト呼び出しの1行だけ残す）。
  - YAML 側の JP 追加は `# BEGIN JP PATCH` / `# END JP PATCH` のマーカーで囲う。
  - 上流更新時はファイル丸ごと置換 → JP パッチ（最小）を再適用。
- 実務メモ:
  - `beforeTests.ps1` で `testOutput/` 配下を作成。
  - installer/system tests は共通スクリプト（`installNVDA.ps1` / `tests/systemTests.ps1`）。
  - 単体テストは `rununittests.bat` で `uv --group dev --group unit-tests` を使用（`miscDeps` を sys.path に含める）。

## Actions 運用

- 監視: `gh run list -w .github/workflows/testAndPublish.yml -b betajp -L 3`
- 失敗調査: `gh run view <runId> --log`、またはチェックランのアノテーションを参照。
- 再実行: `gh run rerun <runId> --failed`
- 型チェックのみの本家版寄せワークフロー: `.github/workflows/nvbeta-typecheck-311x86.yml`
- 日本語版の包括的ワークフロー: `.github/workflows/testAndPublish.yml`

## 参照

- 人間向けハブ: `projectDocs/jp/README.md`
- 本家版の開発環境: `projectDocs/dev/createDevEnvironment.md`
- 日本語版の概要: `readme-nvdajp.md`
