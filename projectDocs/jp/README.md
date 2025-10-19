# NVDA 日本語版 ドキュメント ハブ（JP Docs Hub）

このフォルダは、日本語版に固有の運用・方針・進行中タスクを集約する着地点です。人間開発者向けの恒常情報は `readme-nvdajp.md` に、本家版の一般開発情報は `projectDocs/dev/createDevEnvironment.md` を参照してください。

## 目的と役割
- 日本語版固有の情報の入口（リンク集と短い要約）
- 進行中タスクのスコープと優先度の明示（長文の議論は Issue/PR へ）
- 作業の最短コマンドと禁則の共有（詳細手順は各ドキュメントへ誘導）

## 現状サマリ（2025-10 時点）
- Python は `3.11 x86` を維持（`x64/arm64` 切替は未実施）
- CI/ビルド基盤は本家版寄せを段階実施中（Step 1）
- 7z/nmake 依存は縮小中（アドオン梱包は Python 化済）

## ロードマップ（要約）
- Step 1: 3.11 x86 のまま CI/ビルド基盤を整合（Refs: `#539`, Part of `#530`）
- Step 2: Python 3.13 対応（依存の互換確認とCIマトリクス）
- Step 3: x64 ビルド対応の検討（日本語版固有モジュールの対応評価を含む）

## CI/ビルド クイックスタート
- 型チェックのみ（本家版寄せ・安全導入）: `.github/workflows/nvbeta-typecheck-311x86.yml`
- 日本語版フルビルド・配布系: `.github/workflows/testAndPublish.yml`
- ローカル最小ビルド例: `scons --help` を確認し、通常は `scons source dist launcher --all-cores`
- 単体/システムテスト: `ci/scripts/tests/unitTests.ps1`、`ci/scripts/tests/systemTests.ps1`

## ポリシー（抜粋）
- 本家版との差分は最小に保つ。差分は明示的な場所に集約する
- 可能な限り `SCons`/純 Python を優先し、`.cmd`/`7z`/`nmake` など外部依存は段階的に削減
- CI の前提（Python/ランナー/キャッシュ）は本家版に準拠する方針で段階導入
- 秘密情報（署名トークン等）は GitHub Secrets/Variables 経由。リポジトリへの直書き禁止
- 署名/配布はローカルで実施（CI は未署名）

## 関連ドキュメント
- 日本語版の恒常情報（人間向け）: `readme-nvdajp.md`
- 本家版の開発環境ガイド: `projectDocs/dev/createDevEnvironment.md`
- 日本語版のプロダクトビジョン: `projectDocs/product_vision.md`
- エージェント／自動化向けの運用ルール: `AGENTS.md`

## 進行中タスク（例）
- `#530`: 本家 2026.1 の日本語版へのマージ（サブタスクに Step 1〜3）
- `#539`: Step 1（3.11 x86 のままビルド基盤整合）

本READMEは短い要約とリンク集を維持し、詳細は各ファイルと Issue/PR 側で管理します。
