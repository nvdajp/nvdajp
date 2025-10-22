#!/usr/bin/env python3
"""
Minimal unified/context-diff patch applier for Windows builds.

Usage:
  python jptools/apply_patch.py --inplace <target> <patchFile>

Notes:
- Supports unified diff hunks of the form:
    @@ -oldStart,oldLen +newStart,newLen @@
    <hunk lines starting with ' ', '+', '-'>
- Ignores leading diff headers until the first hunk.
- Preserves the target file's original newline convention (CRLF/LF).
- Exits with code 0 on success, non-zero on failure.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, List, Tuple


_HUNK_RE = re.compile(r"^@@ -(?P<oStart>\d+)(?:,(?P<oLen>\d+))? \+(?P<nStart>\d+)(?:,(?P<nLen>\d+))? @@")


def _detect_newline(text: str) -> str:
    # Prefer CRLF if present, else LF
    if "\r\n" in text:
        return "\r\n"
    return "\n"


def _split_lines_keepends(s: str) -> List[str]:
    return s.splitlines(keepends=True)


def _strip_end(line: str) -> str:
    return line.rstrip("\r\n")


def _parse_hunks(patch_lines: Iterable[str]) -> List[List[str]]:
    hunks: List[List[str]] = []
    cur: List[str] | None = None
    for ln in patch_lines:
        if ln.startswith("@@ "):
            if cur is not None:
                hunks.append(cur)
            cur = [ln]
        elif cur is not None:
            # hunk body continues until next hunk or EOF
            cur.append(ln)
    if cur is not None:
        hunks.append(cur)
    return hunks


def _apply_hunk(orig: List[str], out: List[str], hunk: List[str], oidx0: int) -> int:
    # hunk[0] contains @@ header
    m = _HUNK_RE.match(hunk[0])
    if not m:
        raise ValueError(f"Invalid hunk header: {hunk[0].rstrip()}")
    o_start = int(m.group("oStart"))
    # Convert to 0-based index
    o_target = o_start - 1

    # Copy unchanged lines up to the hunk start
    if o_target < oidx0:
        raise ValueError("Hunk applies before current origin index (overlap)")
    out.extend(orig[oidx0:o_target])
    oidx = o_target

    # Apply hunk body
    for body in hunk[1:]:
        if not body:
            continue
        tag = body[0]
        content = body[1:]
        if tag == ' ':
            # context line: must match
            if oidx >= len(orig) or _strip_end(orig[oidx]) != _strip_end(content):
                raise ValueError("Context does not match while applying hunk")
            out.append(orig[oidx])
            oidx += 1
        elif tag == '-':
            # removal: input must match; do not write
            if oidx >= len(orig) or _strip_end(orig[oidx]) != _strip_end(content):
                raise ValueError("Removal target does not match while applying hunk")
            oidx += 1
        elif tag == '+':
            # addition: write line (with newline added later)
            # Retain diff line ending neutrality; we'll rejoin with target newline
            out.append(content + "\n")
        else:
            # Unknown tag; treat as end of hunk
            raise ValueError(f"Unexpected hunk line tag: {tag}")
    return oidx


def apply_unified_diff(orig_text: str, diff_text: str) -> str:
    target_nl = _detect_newline(orig_text)
    orig_lines = _split_lines_keepends(orig_text)
    patch_lines = _split_lines_keepends(diff_text)
    hunks = _parse_hunks(patch_lines)
    if not hunks:
        # Try context diff style
        ctx_applied = _apply_context_diff(orig_text, patch_lines)
        if ctx_applied is not None:
            return ctx_applied
        # Nothing to do; return original
        return orig_text
    out: List[str] = []
    oidx = 0
    for h in hunks:
        oidx = _apply_hunk(orig_lines, out, h, oidx)
    # Copy the remainder
    out.extend(orig_lines[oidx:])
    # Normalize newlines to target file's convention
    joined = ''.join(out)
    if target_nl == "\r\n":
        joined = joined.replace("\r\n", "\n").replace("\n", "\r\n")
    return joined


def _apply_context_diff(orig_text: str, patch_lines: List[str]) -> Optional[str]:
    """Apply a simple context diff (*** / --- style) by replacing blocks.
    Only supports the form produced by our jtalk patches.
    """
    # Helper to parse range headers like "*** 69,75 ****" or "--- 69,79 ----"
    def parse_range(header: str) -> Tuple[int, int]:
        m = re.search(r"(\d+),(\d+)", header)
        if not m:
            raise ValueError(f"Invalid context diff range: {header.rstrip()}")
        start = int(m.group(1))
        end = int(m.group(2))
        length = end - start + 1
        return start, length

    def strip_prefixes(lines: List[str]) -> List[str]:
        out: List[str] = []
        for ln in lines:
            if not ln:
                continue
            tag = ln[0]
            if tag in (' ', '!', '+', '-', '\t'):
                out.append(ln[1:])
            else:
                out.append(ln)
        return out

    lines = list(patch_lines)
    orig = _split_lines_keepends(orig_text)
    out: List[str] = []
    oidx = 0
    i = 0
    changed = False
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('*** ') and ln.rstrip().endswith('****'):
            # old range
            old_header = ln
            i += 1
            old_body: List[str] = []
            # collect old body until new header starting with '--- ' and ending with '----'
            while i < len(lines) and not (lines[i].startswith('--- ') and lines[i].rstrip().endswith('----')):
                old_body.append(lines[i])
                i += 1
            if i >= len(lines):
                break
            new_header = lines[i]
            i += 1
            new_body: List[str] = []
            while i < len(lines) and not lines[i].startswith('***************') and not (lines[i].startswith('*** ') and lines[i].rstrip().endswith('****')):
                new_body.append(lines[i])
                i += 1
            # Apply replacement
            old_start, _old_len = parse_range(old_header)
            new_start, _new_len = parse_range(new_header)
            # Convert to 0-based index
            target_idx = old_start - 1
            if target_idx < oidx:
                # Overlapping or out of order; fallback fail
                raise ValueError("Context diff hunk overlap")
            # write unchanged until target
            out.extend(orig[oidx:target_idx])
            # Replace old block with new body (strip prefixes, preserve newlines)
            new_body_stripped = strip_prefixes(new_body)
            # Ensure all lines end with newline for joining later
            out.extend([ln if ln.endswith('\n') or ln.endswith('\r\n') else ln + '\n' for ln in new_body_stripped])
            # Advance origin index by length of old body (strip prefixes to count)
            old_len = len(strip_prefixes(old_body))
            oidx = target_idx + old_len
            changed = True
        else:
            i += 1
    if not changed:
        return None
    # Append remainder
    out.extend(orig[oidx:])
    # Preserve original newline convention
    nl = _detect_newline(orig_text)
    joined = ''.join(out)
    if nl == "\r\n":
        joined = joined.replace("\r\n", "\n").replace("\n", "\r\n")
    return joined


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inplace", action="store_true", help="Apply patch in-place to target file")
    ap.add_argument("target")
    ap.add_argument("patch")
    args = ap.parse_args(argv)

    target = Path(args.target)
    patch = Path(args.patch)
    if not target.exists():
        print(f"error: target not found: {target}")
        return 2
    if not patch.exists():
        print(f"error: patch not found: {patch}")
        return 2
    orig_text = target.read_text(encoding="utf-8", errors="ignore")
    diff_text = patch.read_text(encoding="utf-8", errors="ignore")
    try:
        new_text = apply_unified_diff(orig_text, diff_text)
    except Exception as e:
        print(f"error: failed to apply patch: {e}")
        return 1
    if args.inplace:
        target.write_text(new_text, encoding="utf-8", newline="")
    else:
        sys.stdout.write(new_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
