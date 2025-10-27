"""
JP: SCons integration scaffold for certBuild2023.

Phase A (safe): generate a manifest of files that would be additionally
signed for a JP signed build, without performing any signing.

Outputs:
- output/sign-extras-manifest.txt: newline-separated absolute paths that
  exist in the current workspace and match the candidate patterns.

This module is intentionally conservative and side-effect free.
Future phases may add an opt-in signing action reusing env["signExec"].
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List
import os


def _candidates_worktree() -> Iterable[Path]:
    """Yield candidate files to sign (worktree paths), if they exist.

    Mirrors jptools/certBuild2023.cmd targets in a non-destructive way.
    Only yields files that currently exist to avoid errors.
    """
    repo = Path.cwd()
    patterns: List[Path] = []

    # JP synth drivers (built/overlay in source tree)
    patterns += [
        repo / "source" / "synthDrivers" / "jtalk" / "libmecab.dll",
        repo / "source" / "synthDrivers" / "jtalk" / "libopenjtalk.dll",
    ]

    # miscDeps runtime dlls used by NVDA
    patterns += [
        repo / "miscDeps" / "python" / "brlapi-0.8.dll",
        repo / "miscDeps" / "python" / "libgcc_s_dw2-1.dll",
        repo / "miscDeps" / "source" / "brailleDisplayDrivers" / "lilli.dll",
    ]

    # wx runtime DLLs from venv (optional, only if present)
    wx = repo / ".venv" / "Lib" / "site-packages" / "wx"
    for stem in (
        "wxbase32u_net_vc140.dll",
        "wxbase32u_vc140.dll",
        "wxmsw32u_core_vc140.dll",
        "wxmsw32u_html_vc140.dll",
        "wxmsw32u_stc_vc140.dll",
    ):
        patterns.append(wx / stem)

    for p in patterns:
        if p.is_file():
            yield p.resolve()


def _write_manifest(out_file: Path, files: Iterable[Path]) -> None:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with out_file.open("w", encoding="utf-8") as f:
        for p in files:
            f.write(str(p) + os.linesep)


def scons_action_generate_manifest(target, source, env):  # SCons action API
    """SCons action: write sign extras manifest under output/.

    target[0] is the manifest path.
    """
    try:
        out = Path(str(target[0]))
        files = list(_candidates_worktree())
        _write_manifest(out, files)
        print(f"[jp] wrote sign manifest: {out} ({len(files)} entries)")
        return 0
    except Exception as e:
        print(f"[jp] error generating sign manifest: {e}")
        return 1

