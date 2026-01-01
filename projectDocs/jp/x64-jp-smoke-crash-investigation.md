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

Additional minimal repro:

- `a\u200ba` (fullwidth a + ZWSP + fullwidth a) reliably crashes on x64.
  - `text2mecab` converts ASCII `a` to fullwidth (`U+FF41`) and uses `U+200B` as TAB substitute.
  - Bytes passed to MeCab: `EF BD 81 E2 80 8B EF BD 81`.

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

- Forced conversion of `mecab` pointer to `c_void_p` in `Mecab_initialize` and `Mecab_analysis`.
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

### 5) `mecab_sparse_tonode2` removal

- Removed `mecab_sparse_tonode2` calls (attempt #1 failed).
- Current code uses only `mecab_sparse_tonode`.
- Result: crash still occurs.

### 6) PageHeap (gflags)

- Enabled PageHeap for `.venv-x64\Scripts\python.exe` and re-ran `runJpSmokeTests.ps1`.
- Result: crash still occurs in `mecab_sparse_tonode`.
- No new actionable stack info observed.
- PageHeap was disabled after the run.

### 7) Native DLL logging (`libmecab.dll`)

- Added a debug log in `mecab_sparse_tonode` (C++).
- Log file: `%TEMP%\mecab_debug_native.log`
- Minimal repro input: `a\u200ba`
- Logged bytes: `EF BD 81 E2 80 8B EF BD 81`
  - `EF BD 81` = U+FF41 (fullwidth "a")
  - `E2 80 8B` = U+200B (ZWSP)

### 8) CDB stack capture (x64)

- Ran `cdb` with the minimal repro and confirmed the crash occurs inside libmecab:
  - Crash site: `libmecab!MeCab::Connector::cost` (access violation read).
  - Stack: `Connector::cost` -> `connect<0>` -> `Viterbi::viterbi` -> `Viterbi::analyze`
    -> `TaggerImpl::parseToNode` -> `mecab_sparse_tonode`.
- `libmecab.dll` loaded from:
  - `source/synthDrivers/jtalk/libmecab.dll`
- Symbols:
  - Private PDB was loaded from the debugger cache
    (`C:\ProgramData\dbg\sym\libmecab.pdb\...`), so function names resolved.
- Line numbers are not shown (likely inline `Connector::cost`).

### 9) Connector bounds logging (C++)

- Added bounds logging in `Connector::cost` and `Viterbi::connect`:
  - `%TEMP%\mecab_connector_cost.log`
  - `%TEMP%\mecab_connect_bounds.log`
- Observed out-of-range attributes during minimal repro:
  - `rcAttr=0 lcAttr=33763 lsize=1377 rsize=1377`
  - Additional invalid rcAttr values (e.g., `13860`) were also observed.

### 10) Token attribute logging (C++)

- Added a log when `lcAttr`/`rcAttr` are unusually large.
- `%TEMP%\mecab_token_attrs.log` shows an abnormal token from `sys.dic`:
  - `lcAttr=33763 rcAttr=35458 posid=65535 ... dic_ver=102 dic_type=0 charset=utf-8`
- Suggests dictionary/charset mismatch rather than a single input byte issue.

### 9) Workaround attempt: map ZWSP to SPACE in char.def

- Added explicit mapping in `miscDepsJp/jptools/jtalk/libopenjtalk/mecab-naist-jdic/char.def`:
  - `0x200B SPACE` (placed after the general punctuation range).
- Rationale: keep `U+200B` within matrix bounds to avoid invalid `rcAttr/lcAttr`.
- Requires `scons jtalkSync` to regenerate the dictionary.

### 10) Workaround attempt: sanitize ZWSP before MeCab call

- Added a safety shim in `miscDepsJp/include/python-jtalk/libopenjtalk/mecab/src/mecab.cpp`:
  - Replace UTF-8 `E2 80 8B` (ZWSP) with `E3 80 80` (U+3000 ideographic space)
  - This keeps UTF-8 byte length stable and avoids shifting.
- Rationale: avoid invalid `rcAttr/lcAttr` leading to `Connector::cost` OOB access.
- Added a debug log in the same file to confirm the sanitizer is invoked:
  - `%TEMP%\mecab_zwsp_sanitize.log`

### 11) Dictionary rebuild workflow (jtalkSync)

- `scons -c jtalkSync` updated to clean dictionary outputs (`source/synthDrivers/jtalk/dic/*`).
- Rebuild uses `make_jdic.py` and writes `DIC_VERSION` with `utf-8`.
- `output/_logs/make_jdic.log` holds the dictionary build log.

### 12) Workaround: clamp out-of-range attrs in `Connector::cost`

- Added clamping in `Connector::cost` to avoid OOB access in the connection matrix:
  - If `rcAttr` or `lcAttr` is out of range, log and clamp to last valid index.
  - If `lsize`/`rsize` are zero, log and return `rNode->wcost`.
- This avoids access violations but is not a root-cause fix.

### 13) Assert softening in `translator2.py`

- JP-only debug asserts on mixed ASCII/non-ASCII and consecutive ASCII spaces
  were converted to log messages to allow smoke tests to complete.

## Logs

- `source/synthDrivers/jtalk/mecab_debug.log`: detailed mecab input and pointer info
- `jpSmokeTests.console.log`: console output from smoke tests
- `__h2output.txt`: failing test index and text
- `%TEMP%\mecab_debug_native.log`: native MeCab input byte log
- `%TEMP%\mecab_connector_cost.log`: out-of-range connector access
- `%TEMP%\mecab_connect_bounds.log`: out-of-range connect bounds
- `%TEMP%\mecab_token_attrs.log`: suspicious token attribute logs

## Current status

Crash still occurs without the workaround. With the clamp workaround, x64 JP smoke tests
complete successfully. Logs show out-of-range `rcAttr/lcAttr` values originating from tokens
read from `sys.dic`, suggesting a charset/format mismatch between dictionary and `libmecab.dll`
(UTF-8 dictionary vs Shift-JIS-compiled MeCab).

## Considerations

- Crash site is inside MeCab (`Connector::cost`) and not at the Python/C boundary.
- `rcAttr/lcAttr` being out of range is the most plausible direct cause of the access violation.
- UTF-8 specific input patterns (e.g., U+200B or fullwidth ASCII sequences from `text2mecab`)
  are likely to produce invalid context IDs or category mappings.
- `betajp` (Shift-JIS dependent) was stable on x64, while `betajp-260102` (UTF-8 direction)
  crashes in x64; the issue appears tied to UTF-8 input + 64-bit path rather than x64 alone.
- Rolling back to Shift-JIS would remove the immediate failure, but increases long-term drift
  from upstream (x64-only + Python 3.13 + UTF-8 direction).
- Current build shows `CHARSET_SHIFT_JIS` in MeCab compilation flags, while the dictionary is
  UTF-8 (`DIC_VERSION`), which likely explains the out-of-range attributes.

## Additional hypothesis (UTF-8 vs Shift-JIS build mismatch)

Based on recent logs, the most consistent explanation is a charset mismatch:

- `libmecab.dll` is built with `CHARSET_SHIFT_JIS` while the dictionary is UTF-8.
- Abnormal tokens show `posid=65535` (0xFFFF) and out-of-range `lcAttr/rcAttr`, which
  is consistent with incorrect decoding of dictionary fields.

If correct, the root fix is to align MeCab and the dictionary on UTF-8:

1. Switch MeCab build flags from `CHARSET_SHIFT_JIS` to UTF-8 (Makefile.mak and related settings).
2. Rebuild `libmecab.dll` and `mecab-dict-index.exe` with UTF-8 flags.
3. Regenerate the dictionary (make_jdic.py).
4. Re-run smoke tests and confirm `lcAttr/rcAttr` are in range.

The current clamp workaround can remain for diagnosis, but the goal is to remove it once
UTF-8 builds are confirmed stable.

## Suggested direction (summary)

- Short term: keep `betajp` as a stable line (Shift-JIS dependent).
- Mid/long term: solve UTF-8 + x64 crash on `betajp-260102` (or a new branch) and carry
  forward the investigation rather than reverting.

## Related docs

- `projectDocs/jp/tab_character_analysis.md` (TAB replacement and ZWSP crash context)
- `projectDocs/jp/troubleshooting_runjp_smoke_tests.md` (x64 smoke test execution details)
- `projectDocs/jp/roadmap.md` (stage 2/3 migration context)

## Next ideas (if continuing)

### 6) Explicit `c_void_p` conversion in `Mecab_initialize`

**Hypothesis**: `mecab_new` may return `int` instead of `c_void_p` on x64, even with `restype = c_void_p`.
This causes 4-byte `int` to be treated as 8-byte pointer, leading to access violation.

**Implementation**:
- In `Mecab_initialize`, explicitly convert `mecab_new` return value to `c_void_p`.
- In `Mecab_analysis`, ensure `mecab` is `c_void_p` before calling `mecab_sparse_tonode`.
- Added debug logging to track `mecab` type and value.

**Result**:
- Logs confirm `mecab_new` returns `int` and is converted to `c_void_p`.
- `mecab` is correctly stored as `c_void_p` with valid pointer values (e.g., `2396795524128`, `2325409559904`).
- **Crash still occurs** with access violation at `mecab_sparse_tonode`.
- Error pointer values (e.g., `0x0000022E189DD00A`) show lower 4 bytes as `0xD00A` (`\r\n`), suggesting pointer corruption or incorrect memory access.

**Status**: Attempted, but crash persists. Pointer conversion is working, but the underlying issue remains.

### Other ideas

- Isolate minimal failing input for Katakana + spaces.
- Log full input byte sequences for the exact failing case.
- Compare `betajp` branch implementation (known working) with current branch.
- Consider moving `text2mecab` conversion into a C++ extension to reduce `ctypes` risk.
