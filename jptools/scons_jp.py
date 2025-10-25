"""
Minimal JP-specific SCons helpers.

Goals (Step 1):
- Provide opt-in aliases that wrap existing pure-Python tools, without
  changing upstream targets or default build graph.
- Keep differences isolated under jptools/ and guard usage via aliases.

Terminology:
- "JP overlay": Copy of files from ``miscDepsJp/source`` into the repository
  ``source`` tree, executed by ``jptools/setup_miscdeps_overlay.py`` with
  CWD=``miscDepsJp``. The overlay is idempotent and required for JP builds.
  Cleaning (``scons -c``) removes the overlaid files that correspond to
  ``miscDepsJp/source`` (see Clean wiring below).

Deprecated:
- The legacy alias name ``jpPrep`` has been removed. Use ``miscdepsjp``.

Aliases added:
- miscdepsjp: Runs jptools/setup_miscdeps_overlay.py and writes a stamp file.
- controllerClient: Builds NVDA controller client zip using pack_controller_client.py.

These are intentionally light-weight and safe; wiring them into other
targets can be done in later phases when stable.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any


def _run_overlay_and_stamp(target: list[Any], source: list[Any], env: Any) -> int:
    repo_root = Path.cwd()
    script = repo_root / "jptools" / "setup_miscdeps_overlay.py"
    # Run the overlay copy script from miscDepsJp directory (historical behavior)
    misc_root = repo_root / "miscDepsJp"
    if not script.exists() or not misc_root.exists():
        # Nothing to do; succeed without error
        return 0
    # Execute the script using the same Python interpreter that runs SCons
    # The script expects cwd=miscDepsJp
    from subprocess import run

    res = run([sys.executable, str(script)], cwd=str(misc_root))
    if res.returncode != 0:
        return res.returncode
    # Write/update stamp
    stamp_path = Path(str(target[0]))
    stamp_path.parent.mkdir(parents=True, exist_ok=True)
    stamp_path.write_text("ok", encoding="utf-8")
    return 0


def _pack_controller_client(target: list[Any], source: list[Any], env: Any) -> int:
    repo_root = Path.cwd()
    script = repo_root / "jptools" / "pack_controller_client.py"
    if not script.exists():
        return 0
    from subprocess import run

    # Prefer explicit version from env; fallback to empty (script uses 'local').
    version = str(env.get("version", ""))
    out_path = Path(str(target[0]))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(script),
        "--version",
        version,
        "--client-root",
        str(repo_root / "jptools" / "nvdajpClient"),
        "--output",
        str(out_path),
    ]
    res = run(cmd)
    return res.returncode


def _compute_overlay_targets(repo_root: Path) -> list[str]:
    """Return absolute paths for files overlaid from miscDepsJp/source -> source.
    Used to attach Clean so that `scons -c` can remove overlay artifacts.
    """
    targets: list[str] = []
    src_root = repo_root / "miscDepsJp" / "source"
    dst_root = repo_root / "source"
    if not src_root.exists() or not dst_root.exists():
        return targets
    for root, _dirs, files in os.walk(src_root):
        r = Path(root)
        rel = r.relative_to(src_root)
        for f in files:
            targets.append(str((dst_root / rel / f).resolve()))
    return targets


def register_jp_builders(env: Any) -> None:
    """Register JP-specific aliases without affecting upstream targets."""
    repo_root = Path.cwd()
    # Alias: miscdepsjp (overlay stamp)
    stamp = env.File("miscDepsJp/_state/overlay.stamp")
    env.AlwaysBuild(stamp)
    env.Command(stamp, [], _run_overlay_and_stamp)
    env.Alias("miscdepsjp", stamp)
    # Ensure `scons -c` removes overlay files as well when cleaning miscdepsjp
    try:
        env.Clean(stamp, _compute_overlay_targets(repo_root))
    except Exception:
        pass

    # Alias: controllerClient (zip artifact)
    out_dir = str(env.get("outputDir", "output"))
    version = str(env.get("version", "local"))
    cc_zip = env.File(os.path.join(out_dir, f"nvda_{version}_controllerClientJp.zip"))
    env.Command(cc_zip, [], _pack_controller_client)
    env.Alias("controllerClient", cc_zip)

