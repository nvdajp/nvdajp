# 日本語版ロードマップ（2025-10）

目的: 本家版との差分を最小化しながら、順序立てて基盤整合 → 言語/依存更新 → 64bit 対応を進める。

## 2026.1jp 以後の目標

日本語版を小さく安定に保ち、本家版追従のコストとリスクを継続的に低減する。SConsを唯一のビルド・オーケストレーターにする。

- 本家版との差分（最小化）
  - 目標: 日本語版固有差分は「専用ディレクトリ＋パッチ最小」。恒常的な差分ファイル数 ≤ 50、差分行数 ≤ 2,000 を維持。
  - 運用: 四半期ごとに差分レポート（自動生成）を確認し、不要差分を削減。

- プラットフォーム戦略
  - 本家版に合わせる

- CI/品質（グリーン基準）
  - 可能な限り本家版に合わせる

- リリース運用
  - 可能な限り本家版に合わせる
  - 正式リリースの署名/配布はローカル実施（CI は未署名の検証用ビルドのみ）

- アドオン互換性
  - 本家版に合わせる

- ドキュメント
  - readme-nvdajp.md は最小を維持、JP Docs Hub を常に最新に。
  - 重要決定は ADR として `projectDocs/jp/adr/` に 1 ページ記録。

- セキュリティ/コンプライアンス
  - 可能な限り本家版に合わせる

- ディプリケーション計画
  - 可能な限り本家版に合わせる
  - 32bit版 NVDA 日本語版は本家版と同様に 2025.3 系で終了

## Phase 1 : 基盤整合と安定化

- Windows 32bit / Python 3.11 x86 を基盤とし、本家版との差分を最小化
- \.python-versions を 3.11 x86 のみに固定
- CI を SCons で成立させ、.cmd 経由を可能な範囲で排除
- SCons キャッシュ/引数の整合（ci/scripts/setSconsArgs.ps1 準拠）
- Lint（ruff）ジョブ追加・安定化
- 7z ラウンドトリップ除去（Python化）
- ユニット/必要最小のシステムテストを安定して通す（installer タグは最小構成で運用可）
- testAndPublish の主要ジョブを windows-2025 へ（後述: ランナー移行計画）
- 上流追従容易化: testAndPublish.yml は上流原本を優先し、JP 固有はスクリプト呼び出しの最小パッチに集約

## Phase 2 : Python 3.13 対応（Part of #530）

- Scope
  - 3.13 x64 を必須とし、3.11 x86 はEOLまで保守
- Tasks
  - 新しいワークフローを 3.13 x64 に切替（ファイル名は nvbeta-typecheck.yml 等に簡素化可）。
  - 依存互換性の確認・ピン更新（wxPython, brlapi など）
  - .python-versions に 3.13 を追加（3.11 と併存）
  - CI ジョブ分割（typeCheck / unit / docs / packaging）を本家版構成へ近づける
- Exit
  - 3.13 x64 が安定して緑、3.11 x86 は EOL（2025.3）まで緑を維持
- 補足（運用）
  - 目的: x64 を既定化に向け安定、3.13 を実用レベルへ（配布は段階導入）
  - CI マトリクス: 3.13 x64（必須）/ 3.11 x86（EOL まで保守用）/ 3.13 x86（typeCheck・lint のみ任意）
  - DMP フォールバック: fast-diff-match-patch が利用不可の場合は difflib へ自動退避
  - 主要 JP アドオン（jtalk/kgs）を x64 で起動確認（任意）

### 既知の懸念

- Python 3.13 への移行と x64 対応が、fast-diff-match-patch（DMP）依存の配布状況により同時対応になりうる。
  - 対応方針（今は実装せず記録のみ）
    - DMP 読み込み失敗時は difflib へ自動フォールバック（コード側で遅延 import/try-except）
    - CI では 3.13 x64 を先行検証、3.13 x86 は typeCheck/lint のみ等で段階導入
  - Phase 1 完了時点で再評価し、必要なら Phase 2 の計画に反映

## Phase 3 : x64 ビルド対応（Part of #530）

- Scope
  - x64（将来 arm64）ビルドの追加、移行パス検証
- Tasks
  - nvbeta-typecheck.yml は削除。testAndPublish.yml に本家版と同等の typeCheck ジョブを持たせる。
  - JAB 64bit への切替、installer/launcher の x64 条件分岐
  - 設定移行（32→64）・アンインストーラ fix（本家版の取り込みを反映）
  - 日本語版固有モジュール（jtalk 等）の x64 対応検証
  - アドオン互換性チェックとガイダンス
- 手順
  - 先行診断: dry-run マージで衝突箇所を棚卸し（pyproject、sconstruct、workflows、installer/launcher、source 配下）
  - 先にワークフローと SCons の構造差分を合わせる（コード差分より先）
  - 段階マージ: ワークフロー → ビルド（SCons/installer） → ランタイム（source） → ドキュメント
  - 差分の集約・削減: 日本語版固有変更は明示ディレクトリへ寄せ、恒常差分を減らす
- Exit
  - x86/x64 の並行ビルドがCIで緑、配布準備可

## リスクとロールバック

- 依存更新でのビルド破綻 → ピン見直し/段階導入
- システムテストの不安定化 → タグ縮小・再試行の仕組み

## ランナー移行計画（windows-2025）

- 方針: 本家版と整合させるため、windows-2025 へ段階移行。影響の小さいジョブから先行し、安定確認後に固定。
- 移行順序（Phase 1 内で実施）
  - フェーズ1-A（低リスク先行）
    - 対象: typeCheck（pyright）、checkPo、checkPot、licenseCheck
    - 方針: 直ちに windows-2025 へ。3 連続グリーンで固定
  - フェーズ1-B（ビルド要所）
    - 対象: buildNVDA、createLauncher、createSymbols
    - 方針: SCons MSVC 設定キャッシュ（SCONS_CACHE_MSVC_CONFIG）を有効化してから 2025 へ。
      2 連続グリーン＋成果物検証（launcher 起動・symbols 生成）で固定
  - フェーズ1-C（最後に移行）
    - 対象: unitTests → systemTests の順
    - 方針: unitTests を先に 2025 へ。systemTests はタグを限定（例: startupShutdown）で試行→安定後に拡大
- 受け入れ基準（各段）
  - 2〜3 連続グリーン（ジョブ特性に応じて調整）
  - 成果物の基本動作確認（launcher 起動、symbols 正常作成/アップロード）
  - 実行時間が顕著に悪化しない（悪化時はキャッシュ/並列度を見直し）
- ロールバック/安全策
  - 一時的にランナーをマトリクス化（windows-2022/2025 並走）して比較
  - 不安定な場合は該当ジョブのみ即座に元のランナーへ戻す
  - systemTests はタグ縮小・再試行の運用でフレークを抑制

## ゲート（判断ポイント）

- Gate A（Phase 2 中間）: 3.13 x64 で unit + 最小 system が安定緑 → installer/署名/シンボル確認へ
- Gate B（Phase 2 完了）: 3.13 x64 が配布可能、3.11 x86 は EOL まで保守可能 → Phase 3 へ
- Gate C（Phase 3 開始前）: dry-run マージ結果と衝突一覧の承認 → 実マージ・段階導入へ

## 現在の作業キュー（Step 1, refs #539）

- PR #548（ドラフト）: CI 安定化フォローアップ（unit / license / translator）
  - unit tests: `nvda-misc-deps`（editable）をテスト実行環境へ組み込み（rununittests.bat の `uv --group dev --group unit-tests`）
  - license check: `testOutput/license` 事前作成＋結果をアーティファクトへ
  - translator comments: ログ（translationCheckResults.log）をアーティファクトへ
  - system tests: インストーラ導入前に `beforeTests.ps1` を実行（ディレクトリ作成）

## 運用ルール（ブランチ/PR）

- `betajp` は安定ブランチ（直接 push 禁止）。すべてトピックブランチ→PR で変更。
- ブランチ保護: `allTestsPass` / TypeCheck を必須チェックに設定。
- testAndPublish.yml は「上流置換 → JP パッチ再適用」の手順で保守。

## 参照

- JP Docs Hub: projectDocs/jp/README.md
- 本家版開発環境: projectDocs/dev/createDevEnvironment.md
- エージェント向け: AGENTS.md
