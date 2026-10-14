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
- Do not add machine-specific absolute paths (drive letters such as `f:\`, user-profile paths) to tracked documentation. Keep local environment notes outside the repository.

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
