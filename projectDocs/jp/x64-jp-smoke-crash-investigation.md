# x64 JP smoke test crash investigation (betajp-260102)

## Summary

x64 JP smoke tests crash in `mecab_sparse_tonode` / `mecab_sparse_tonode2` with an access violation.
This document captures the reproduction, observed triggers, and attempts tried so far.

## Environment

- Branch: `betajp-260102` (after merging nvaccess beta x64-only changes)
- Platform: Windows x64
- Python: 3.13 x64 (`.venv-x64`)
- Test entry points:
  - `jptools/runJpSmokeTests.ps1`
  - `jptools/checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests`

## Reproduction

### Full smoke test

```
.\jptools\runJpSmokeTests.ps1
```

Failure is an access violation at `mecab_sparse_tonode` (or `mecab_sparse_tonode2`).

### Minimal repro

Input `あab` crashes when `text2mecab` conversion is active.

When conversion is skipped via an environment variable, the minimal repro passes:

```
$env:NVDA_JP_TEXT2MECAB_SKIP_CONVERT="1"
```

Note: This is a debug-only toggle and not a fix.

## Observed failing inputs

From `__h2output.txt`:

- Test index 14:
  - `ヒロイノ カン  カンスージノ ニ` (Katakana with ASCII spaces)
  - Crash: access violation in `mecab_sparse_tonode(2)`

This indicates the issue is not limited to ASCII alnum mixed with kana.

## Attempts and results

### 1) `mecab_sparse_tonode2` (length-specified API)

- Added calls to `mecab_sparse_tonode2` when available.
- Result: crash still occurs.

### 2) Explicit `c_void_p` conversion for `mecab_new` return value

- Forced conversion of `mecab` pointer to `c_void_p`.
- Logged `mecab` type/value in `mecab_debug.log`.
- Result: pointer is a valid `c_void_p`, but crash still occurs.

### 3) `text2mecab` conversion toggles (debug-only)

Added temporary environment-variable switches to skip parts of conversion:

- `NVDA_JP_TEXT2MECAB_SKIP_CONVERT=1`
- `NVDA_JP_TEXT2MECAB_SKIP_ASCII_ALNUM=1`
- `NVDA_JP_TEXT2MECAB_SKIP_ASCII=1`

Results:

- Skipping all conversion avoids the minimal repro (`あab`).
- Skipping ASCII alnum conversion avoids the minimal repro.
- Full smoke test still crashes on Katakana + spaces even when ASCII conversion is skipped.

### 4) DLL mismatch check (x64)

Confirmed that `libmecab.dll` and `libopenjtalk.dll` are x64 and match vendor payload.

## Logs

- `source/synthDrivers/jtalk/mecab_debug.log`: detailed mecab input and pointer info
- `jpSmokeTests.console.log`: console output from smoke tests
- `__h2output.txt`: failing test index and text

## Current status

No functional fix found yet. The crash is reproducible in x64 and does not occur in x86.
The issue appears related to MeCab processing in x64, potentially input encoding/byte sequences
produced by `text2mecab`, but the precise trigger is still unclear.

## Next ideas (if continuing)

- Isolate minimal failing input for Katakana + spaces.
- Log full input byte sequences for the exact failing case.
- Consider moving `text2mecab` conversion into a C++ extension to reduce `ctypes` risk.
