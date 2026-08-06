# AGENTS.md — JP automation guidelines (minimal)

This document summarizes the rules automation agents/scripts must obey when working in this repository. Human-oriented guides live under `projectDocs/jp/`.

## Scope

- Target platform: Windows x64 with Python 3.13
- Out of scope: arm64, CI releases using secrets
- Related issues: #539 (workflow alignment)

## Principles

- Avoid destructive operations (no history rewrites or force pushes unless explicitly requested)
- Minimize diffs against upstream; mark JP-specific code with `# nvdajp` or `# BEGIN/END JP PATCH`
  - **Marking rules**:
    - **`# BEGIN JP PATCH` / `# END JP PATCH`**: Use for multi-line changes (3+ lines), function/class additions or modifications, configuration section additions
    - **`# nvdajp`**: Use for 1-2 line changes, import statements, single variable/constant additions, inline comments
  - **When marking is NOT needed**:
    - JP-specific new files (e.g., `jptools/*.ps1`, `jptools/runJpSmokeTests.ps1`, `jptools/scons_jp.py`)
    - Files under `source/synthDrivers/jtalk/` and `source/synthDrivers/haruka/` (JP-specific synthesizer drivers)
    - Files under `miscDepsJp/` (JP-specific overlay directory)
    - Files under `jptools/` (JP-specific tools directory)
  - **Note**: JP PATCH markers are only needed when modifying upstream files. JP-specific new files do not need these markers.
- Prefer SCons/pure Python tooling; auxiliary `.cmd` or `nmake` usage should be limited to JP-specific overlays
- Use `scons.bat` / `ensureuv.ps1` for builds and Python tooling; do not use the Windows `py` launcher
- Do not use SCons `--all-cores` by default (parallel builds can fail with JP targets such as `jtalkPrep`)
- Do not perform code-signing or releases in CI (no secrets). Official release builds happen locally.

## Quick commands

- Type check: `ci/scripts/tests/typeCheck.ps1`
- Lint (optional): `uv run ruff format --check && uv run ruff check`
- Build example: `scons.bat synthDriverHost32Runtime source` (see `readme-nvdajp.md`)

## CI & branching

- Base branch for PRs: `betajp`
- Required checks: `allTestsPass`, etc.
- Release/snapshot jobs stay disabled unless explicitly requested; avoid secrets.

## Commit & push policy

To reduce CI load and wait for completion:

1. **Group related changes into single commits**:
   - Include functional changes and their documentation updates in the same commit
   - Combine multiple small fixes into one commit (e.g., multiple documentation updates)
2. **Wait for CI completion**: Do not push until the previous push's CI has completed
3. **Limit push frequency**: Avoid frequent pushes; group changes and push only when CI is ready
4. **Clear commit messages**: When a commit includes multiple changes, describe all changes in the commit message
5. **Avoid frequent commits**: Do not commit intermediate work states; commit only when a unit of work is complete

## Aligning `testAndPublish.yml`

- Use upstream `testAndPublish.yml` verbatim; JP additions must:
  - Call helper scripts (`ci/scripts/...`) instead of embedding logic
  - Be wrapped with `# BEGIN/END JP PATCH` (only when modifying upstream files)
  - Stay focused on JP-only requirements (e.g., `beforeTests.ps1`, crowdin upload disabled)
  - **Note**: JP-specific new files do not need JP PATCH markers

## Actions usage

- Monitor: `gh run list -w .github/workflows/testAndPublish.yml -b betajp -L 3`
- View logs: `gh run view <runId> --job <jobId> --log`
- Rerun failures: `gh run rerun <runId> --failed`
- Key workflow: `.github/workflows/testAndPublish.yml` (includes `typeCheck`, unit/system tests, JP smoke tests)
- **PR CI monitoring**: `ci/scripts/monitor-pr-ci.ps1 -PrNumber <number>` (single check) or `-Watch` (continuous monitoring)
  - Automatically analyzes failures and provides specific advice
  - Detects common issues like JTalk/MeCab dictionary build problems, MSVC environment issues, etc.

## References

- JP landing page: `readme-nvdajp.md`
- JP Docs Hub: `projectDocs/jp/README.md`
- Roadmap: `projectDocs/jp/roadmap.md`
- Build system strategy: `projectDocs/jp/miscdepsjp-overlay-strategy.md`
- Upstream docs (when no JP diff exists):
  - `projectDocs/dev/readme.md`
  - `projectDocs/dev/createDevEnvironment.md`
  - `projectDocs/dev/contributing.md`
  - `projectDocs/dev/codingStandards.md`
  - `projectDocs/testing/readme.md`
  - `projectDocs/testing/automated.md`
  - `ci/README.md`
  - `projectDocs/translating/readme.md`

---

## 日本語まとめ

このファイルは、自動化エージェント／スクリプトが守る最小限のルールを示します。人間向けの詳細は `projectDocs/jp/` を参照してください。

### スコープ

- 対象: Windows x64 + Python 3.13
- 除外: arm64、Secrets を使う配布系ジョブ

### 禁則と優先

- 履歴書き換えや force push は指示が無い限り禁止
- JP 固有差分は `# nvdajp`／`# BEGIN JP PATCH` で明示
  - **マーキングルール**:
    - **`# BEGIN JP PATCH` / `# END JP PATCH`**: 複数行の変更（3行以上）、関数・クラスの追加・修正、設定セクションの追加に使用
    - **`# nvdajp`**: 1-2行の変更、import文の追加、単一の変数・定数の追加、インラインコメントに使用
  - **マーキング不要な場合**:
    - 日本語版固有の新規ファイル（例: `jptools/*.ps1`, `jptools/runJpSmokeTests.ps1`, `jptools/scons_jp.py`）
    - `source/synthDrivers/jtalk/` および `source/synthDrivers/haruka/` 配下のファイル（日本語版固有のシンセサイザードライバー）
    - `miscDepsJp/` 配下のファイル（日本語版固有のオーバレイディレクトリ）
    - `jptools/` 配下のファイル（日本語版固有のツールディレクトリ）
  - **注**: 本家版ファイルを変更する場合のみマーキングが必要。日本語版固有の新規ファイルには不要
- ビルドは SCons／純 Python を優先。`.cmd` や `nmake` は JP 独自処理のみ
- ビルドと Python 実行は `scons.bat`／`ensureuv.ps1` を使う。Windows の `py` ランチャーは使わない
- SCons の `--all-cores` はデフォルトで使わない（`jtalkPrep` など JP ターゲットで並列ビルドが失敗することがある）
- CI ではコードサインや Secrets 利用を行わない

### 最短コマンド

- 型チェック: `ci/scripts/tests/typeCheck.ps1`
- Lint（任意）: `uv run ruff format --check && uv run ruff check`
- ビルド: `scons.bat synthDriverHost32Runtime source`（詳細は `readme-nvdajp.md`）

### CI とブランチ

- PR は `betajp` を base
- 必須チェック: `allTestsPass` など
- 配布系ジョブはデフォルト無効／Secrets 不使用

### コミット・push 方針

CI負荷軽減と完了待ちのため：

1. **関連する変更を1つのコミットにまとめる**:
   - 機能的な変更とそのドキュメント更新を同じコミットに含める
   - 複数の小さな修正を1つのコミットにまとめる（例: 複数のドキュメント更新）
2. **CI完了を待つ**: 前回のpushのCIが完了するまで、次のpushを控える
3. **push頻度を制限**: 頻繁なpushを避け、変更をまとめてからpushする
4. **コミットメッセージを明確に**: 1つのコミットに複数の変更を含める場合は、コミットメッセージで全ての変更を説明する
5. **頻繁なコミットを避ける**: 作業中の一時的な状態はコミットせず、完成した単位でコミットする

### `testAndPublish.yml`

- 上流ファイルをそのまま使い、JP 追加はスクリプト呼び出し＋`# BEGIN/END JP PATCH` のみにする（**注**: 本家版ファイルを変更する場合のみ）
- `beforeTests.ps1` 呼び出し、crowdin upload 無効化など最小の JP 追加だけを維持
- 日本語版固有の新規ファイル（例: `jptools/runJpSmokeTests.ps1`）には JP PATCH マーカーは不要

### Actions 運用

- 監視: `gh run list -w .github/workflows/testAndPublish.yml -b betajp -L 3`
- ログ: `gh run view <runId> --job <jobId> --log`
- 再実行: `gh run rerun <runId> --failed`
- **PR CI 監視スクリプト**: `ci/scripts/monitor-pr-ci.ps1 -PrNumber <番号>` (単回チェック) または `-Watch` (継続監視)
  - 失敗を自動分析し、具体的なアドバイスを提供
  - JTalk 辞書ビルドや MSVC 環境の問題などを検出

### 参考

- `readme-nvdajp.md`, `projectDocs/jp/README.md`, `projectDocs/jp/roadmap.md`
- ビルドシステムの方針: `projectDocs/jp/miscdepsjp-overlay-strategy.md`
- 差分が無い場合は上流ドキュメントを参照

---

### Workspace 共通ルール

- このフォルダ（`betajp`）は `betajp` ブランチの**優先作業場**です。
- マルチルートワークスペース共通の方針（ブランチ⇄フォルダ対応、共通運用規則）は `f:\nvda\gh\AGENTS.md` を参照してください。
