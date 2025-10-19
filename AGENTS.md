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

## 最短コマンド
- 型チェック: `ci/scripts/tests/typeCheck.ps1`（Pyright）
- Lint（推奨）: `uv run ruff format --check && uv run ruff check`
- ビルド例: `scons source dist launcher --all-cores`

## CI とブランチ
- PR の base は通常 `betajp`
- 型チェックのみの本家版寄せワークフロー: `.github/workflows/nvbeta-typecheck-311x86.yml`
- 日本語版の包括的ワークフロー: `.github/workflows/testAndPublish.yml`

## 参照
- 人間向けハブ: `projectDocs/jp/README.md`
- 本家版の開発環境: `projectDocs/dev/createDevEnvironment.md`
- 日本語版の概要: `readme-nvdajp.md`
