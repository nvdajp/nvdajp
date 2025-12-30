# AGENTS.md — JP automation guidelines (minimal)

This document summarizes the rules automation agents/scripts must obey when working in this repository. Human-oriented guides live under `projectDocs/jp/`.

## Scope

* Target platform: Windows x86 with Python 3.11 (this branch: betajp-251206v4)
* Out of scope: arm64, CI releases using secrets
* Related issues: #539 (workflow alignment), #530 (2026.1 merge)
* Note: Java Access Bridge 32-bit is supported

## Principles

* Avoid destructive operations (no history rewrites or force pushes unless explicitly requested)
* Minimize diffs against upstream; mark JP-specific code with `# nvdajp` or `# BEGIN/END JP PATCH`
  * **Note**: JP PATCH markers are only needed when modifying upstream files. JP-specific new files (e.g., `jptools/*.ps1`, `jptools/runJpSmokeTests.ps1`) do not need these markers.
* Prefer SCons/pure Python tooling; auxiliary `.cmd` or `nmake` usage should be limited to JP-specific overlays
* Do not perform code-signing or releases in CI (no secrets). Official release builds happen locally.

## Quick commands

* Type check: `ci/scripts/tests/typeCheck.ps1`
* Lint (optional): `uv run ruff format --check && uv run ruff check`
* Build example: `scons source dist launcher --all-cores`

## CI & branching

* Base branch for PRs: `betajp` (protected; direct pushes forbidden)
* Required checks: `allTestsPass`, etc.
* Release/snapshot jobs stay disabled unless explicitly requested; avoid secrets.

## Aligning `testAndPublish.yml`

* Use upstream `testAndPublish.yml` verbatim; JP additions must:
  * Call helper scripts (`ci/scripts/...`) instead of embedding logic
  * Be wrapped with `# BEGIN/END JP PATCH` (only when modifying upstream files)
  * Stay focused on JP-only requirements (e.g., `beforeTests.ps1`, crowdin upload disabled)
  * **Note**: JP-specific new files do not need JP PATCH markers

## Actions usage

* Monitor: `gh run list -w .github/workflows/testAndPublish.yml -b betajp -L 3`
* View logs: `gh run view <runId> --job <jobId> --log`
* Rerun failures: `gh run rerun <runId> --failed`
* Key workflows: `.github/workflows/testAndPublish.yml`, `.github/workflows/nvbeta-typecheck.yml`
* **PR CI monitoring**: `ci/scripts/monitor-pr-ci.ps1 -PrNumber <number>` (single check) or `-Watch` (continuous monitoring)
  * Automatically analyzes failures and provides specific advice
  * Detects common issues like JTalk build architecture mismatches, MSVC environment problems, etc.

## References

* JP landing page: `readme-nvdajp.md`
* JP Docs Hub: `projectDocs/jp/README.md`
* Roadmap: `projectDocs/jp/roadmap.md`
* Build system strategy: `projectDocs/jp/miscdepsjp-overlay-strategy.md`
* Upstream docs (when no JP diff exists):
  * `projectDocs/dev/readme.md`
  * `projectDocs/dev/createDevEnvironment.md`
  * `projectDocs/dev/contributing.md`
  * `projectDocs/dev/codingStandards.md`
  * `projectDocs/testing/readme.md`
  * `projectDocs/testing/automated.md`
  * `ci/README.md`
  * `projectDocs/translating/readme.md`

---

## 日本語まとめ

このファイルは、自動化エージェント／スクリプトが守る最小限のルールを示します。人間向けの詳細は `projectDocs/jp/` を参照してください。

### スコープ

* 対象: Windows x86 + Python 3.11（このブランチ: betajp-251206v4）
* 除外: arm64、Secrets を使う配布系ジョブ
* 注記: Java Access Bridge 32-bit は対応済み

### 禁則と優先

* 履歴書き換えや force push は指示が無い限り禁止
* JP 固有差分は `# nvdajp`／`# BEGIN JP PATCH` で明示（**注**: 本家版ファイルを変更する場合のみ。日本語版固有の新規ファイルには不要）
* ビルドは SCons／純 Python を優先。`.cmd` や `nmake` は JP 独自処理のみ
* CI ではコードサインや Secrets 利用を行わない

### 最短コマンド

* 型チェック: `ci/scripts/tests/typeCheck.ps1`
* Lint（任意）: `uv run ruff format --check && uv run ruff check`
* ビルド: `scons source dist launcher --all-cores`

### CI とブランチ

* PR は `betajp` を base（保護ブランチ）
* 必須チェック: `allTestsPass` など
* 配布系ジョブはデフォルト無効／Secrets 不使用

### `testAndPublish.yml`

* 上流ファイルをそのまま使い、JP 追加はスクリプト呼び出し＋`# BEGIN/END JP PATCH` のみにする（**注**: 本家版ファイルを変更する場合のみ）
* `beforeTests.ps1` 呼び出し、crowdin upload 無効化など最小の JP 追加だけを維持
* 日本語版固有の新規ファイル（例: `jptools/runJpSmokeTests.ps1`）には JP PATCH マーカーは不要

### Actions 運用

* 監視: `gh run list -w .github/workflows/testAndPublish.yml -b betajp -L 3`
* ログ: `gh run view <runId> --job <jobId> --log`
* 再実行: `gh run rerun <runId> --failed`
* **PR CI 監視スクリプト**: `ci/scripts/monitor-pr-ci.ps1 -PrNumber <番号>` (単回チェック) または `-Watch` (継続監視)
  * 失敗を自動分析し、具体的なアドバイスを提供
  * JTalk ビルドのアーキテクチャ不一致、MSVC 環境の問題などを検出

### 参考

* `readme-nvdajp.md`, `projectDocs/jp/README.md`, `projectDocs/jp/roadmap.md`
* ビルドシステムの方針: `projectDocs/jp/miscdepsjp-overlay-strategy.md`
* 差分が無い場合は上流ドキュメントを参照
