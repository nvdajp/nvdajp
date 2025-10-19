# 日本語版ロードマップ（2025-10）

目的: 上流との差分を最小化しながら、順序立てて基盤整合 → 言語/依存更新 → 64bit 対応を進める。

## Phase 1 — Build Infra Align on 3.11 x86（Issue #539, Part of #530）
- Scope
  - Python 3.11 x86 を維持したまま、上流CI/ビルド前提に寄せる
  - 外部依存（.cmd / 7z / nmake）を段階的に排除し、SCons/純Pythonへ
- Done（実績）
  - 型チェック専用ワークフロー追加: .github/workflows/nvbeta-typecheck-311x86.yml（PR #540）
  - アドオン梱包の 7z 依存排除: jptools/pack_*.py に置換（PR #540）
  - ドキュメント整理（最小README、JP Docs Hub、legacy保存）
- TODO（受け入れ基準＝All green + 外部依存縮小）
  - Lint（ruff）ジョブ追加・安定化
  - .python-versions を 3.11 x86 のみに固定（3.13 は次Phase）
  - testAndPublish の主要ジョブを段階的に windows-2025 へ
  - jptools/setupMiscDepsJp.cmd の 7z ラウンドトリップ除去（Python/SCons化）
  - SCons キャッシュ/引数の整合（ci/scripts/setSconsArgs.ps1 準拠）
  - ユニット/必要最小のシステムテストを安定緑（installerタグは除外可）

## Phase 2 — Python 3.13 対応（Part of #530）
- Scope
  - CI マトリクス（3.11 x86 / 3.13 x86）を導入、将来 x64 追加の前段
- Tasks
  - 依存互換性の確認・ピン更新（wxPython, brlapi など）
  - .python-versions に 3.13 を追加（3.11 と併存）
  - CI ジョブ分割（typeCheck / unit / docs / packaging）を上流構成へ近づける
- Exit
  - 主要ジョブが 3.11 / 3.13 の双方で緑

## Phase 3 — x64 ビルド対応（Part of #530）
- Scope
  - x64（将来 arm64）ビルドの追加、移行パス検証
- Tasks
  - JAB 64bit への切替、installer/launcher の x64 条件分岐
  - 設定移行（32→64）・アンインストーラ fix（上流取り込み反映）
  - 日本語版固有モジュール（jtalk 等）の x64 対応検証
  - アドオン互換性チェックとガイダンス
- Exit
  - x86/x64 の並行ビルドがCIで緑、配布準備可

## リスクとロールバック
- 依存更新でのビルド破綻 → ピン見直し/段階導入
- システムテストの不安定化 → タグ縮小・再試行の仕組み

## 参照
- JP Docs Hub: projectDocs/jp/README.md
- 上流開発環境: projectDocs/dev/createDevEnvironment.md
- エージェント向け: AGENTS.md

