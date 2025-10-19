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

## 既知の懸念（メモ）
- Python 3.13 への移行と x64 対応が、fast-diff-match-patch（DMP）依存の配布状況により同時対応になりうる。
  - 対応方針（今は実装せず記録のみ）
    - DMP 読み込み失敗時は difflib へ自動フォールバック（コード側で遅延 import/try-except）
    - CI では 3.13 x64 を先行検証、3.13 x86 は typeCheck/lint のみ等で段階導入
  - Phase 1 完了時点で再評価し、必要なら Phase 2 の計画に反映

## 参照
- JP Docs Hub: projectDocs/jp/README.md
- 上流開発環境: projectDocs/dev/createDevEnvironment.md
- エージェント向け: AGENTS.md

## 2026.1jp の先 — 目標状態（2026–2027）
目的: 日本語版を小さく安定に保ち、上流追従のコストとリスクを継続的に低減する。

- 上流差分（最小化）
  - 目標: 日本語版固有差分は「専用ディレクトリ＋パッチ最小」。恒常的な差分ファイル数 ≤ 50、差分行数 ≤ 2,000 を維持。
  - 運用: 四半期ごとに差分レポート（自動生成）を確認し、不要差分を削減。

- プラットフォーム戦略
  - x64: 既定。x86 は 2027.x で段階的非推奨（Security Fixes のみ）。
  - arm64: 技術プレビュー（CI でビルド・起動確認、配布は任意）。
  - Python: 「N と N-1」方針（例: 3.13 本線、3.12 併存→次サイクルで入替）。

- CI/品質（グリーン基準）
  - マトリクス: windows-2025 ランナー、3.13 x64（必須）、3.13 arm64（任意）。
  - 成果指標: 主要ジョブの成功率 ≥ 98%、中央値実行時間 ≤ 45 分、フレーク率 ≤ 1%。
  - ゲート: typeCheck/ruff/unit は必須、system tests は最小タグでも赤はマージ不可。

- リリース運用
  - スナップショット: 月次（自動デプロイ）。
  - マイナー: 四半期（上流 beta に同期）。
  - 署名/シンボル/VT: CI で自動、障害時はリトライと手動手順を明文化。

- アドオン互換性
  - API ポリシー: 2 マイナー後方互換を基本、破壊変更は 1 サイクル前に告知。
  - CI: 主要 JP アドオンをサンプル集合として起動テスト（任意）に組込み。
  - ガイド: x64/3.13 への移行ガイドを維持（ビルド・テスト方法、既知の落とし穴）。

- ドキュメント
  - readme-nvdajp.md は最小を維持、JP Docs Hub を常に最新に。
  - 重要決定は ADR として `projectDocs/jp/adr/` に 1 ページ記録。

- セキュリティ/コンプライアンス
  - 依存: uv.lock を配布物に添付、licensecheck をゲートに維持。
  - 秘密管理: 署名トークンは Org/Repo Secrets、権限は最小化・ローテーション記録。
  - SBOM/署名: 余力があれば SBOM 生成とアーティファクト署名を検討。

- ディプリケーション計画
  - x86 非推奨タイムラインを告知（例: 2026.x: Deprecated、2027.x: EOL）。
  - 代替手段（x64/arm64）と移行手順を明記。
