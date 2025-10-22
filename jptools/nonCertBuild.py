#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path


def run_cmd(cmd: list[str]) -> None:
    print(f"[nonCertBuild] run: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        # Propagate the exit code for CI to fail fast
        sys.exit(e.returncode or 1)
    except FileNotFoundError as e:
        print(f"::error::Command not found: {cmd[0]} ({e})")
        sys.exit(127)


def _is_ci() -> bool:
    return os.environ.get("GITHUB_ACTIONS") == "true"


def _check_vs_version() -> None:
    """Replicates jptools/check_vs_version.cmd in Python.
    Warn on VS 2022 v17.14.8. Fail only outside CI.
    """
    vswhere = r"C:\\Program Files (x86)\\Microsoft Visual Studio\\Installer\\vswhere.exe"
    if not Path(vswhere).exists():
        # Not critical; just return.
        return
    try:
        # Get product display versions for VS 2022 range [17.0,18.0)
        out = subprocess.check_output(
            [
                vswhere,
                "-format",
                "value",
                "-property",
                "catalog.productDisplayVersion",
                "-products",
                "*",
                "-version",
                "[17.0,18.0)",
            ],
            text=True,
            errors="ignore",
        )
    except Exception:
        return
    for line in out.splitlines():
        ver = line.strip()
        if ver == "17.14.8":
            print("Warning: VS 2022 v17.14.8 detected - known to cause LNK1120 build errors")
            if _is_ci():
                print("GitHub Actions environment - continuing with warning")
            else:
                print("Please downgrade to v17.14.5 or use a different version")
                sys.exit(1)


def _prep_miscdepsjp() -> None:
    """Replicates nonCertBuild1.cmd steps in Python.
    Keeps underlying module .cmd scripts, but removes top-level .cmd dependency.
    """
    # Only run VS environment setup locally; CI sets up MSVC via ilammy/msvc-dev-cmd
    if not _is_ci():
        vcsetup = Path("miscDepsJp/include/python-jtalk/vcsetup.cmd")
        if vcsetup.exists():
            run_cmd(["cmd", "/c", str(vcsetup)])
    _check_vs_version()

    # Run miscDepsJp jtalk prep/build/test
    md_root = Path("miscDepsJp/jptools")
    run_cmd(["cmd", "/c", str(md_root / "clean.cmd")])
    run_cmd(["cmd", "/c", str(md_root / "copy_jtalk_core_files.cmd")])
    run_cmd(["cmd", "/c", str(md_root / "build-and-test.cmd")])

    # Setup overlay for miscDepsJp
    setup_overlay = Path("jptools/setupMiscDepsJp.cmd")
    if setup_overlay.exists():
        run_cmd(["cmd", "/c", str(setup_overlay)])


def _nowdate() -> str:
    # Generate same format as jptools/nowdate.py without importing it (to avoid side effects)
    from datetime import datetime as _dt
    return _dt.now().strftime("%y%m%d") + chr(_dt.now().hour + 97)


def _build_with_scons(forwarded_args: list[str]) -> None:
    # Derive defaults when VERSION is not set
    env = os.environ
    version = env.get("VERSION")
    publisher = env.get("PUBLISHER")
    updateVersionType = env.get("UPDATEVERSIONTYPE")
    if not version:
        version = f"jpdev_{_nowdate()}"
        # Match nonCertBuild2.cmd defaults for dev builds
        publisher = publisher or "nvdajpdev"
        updateVersionType = updateVersionType or "nvdajpdev"

    # Compose SCons options
    options = [
        f"publisher={publisher or 'nvdajp'}",
        f"version={version}",
        f"updateVersionType={updateVersionType or ''}".rstrip("="),
        "release=1",
    ]
    # Forward args from caller (after -- separator)
    scons_args = options + forwarded_args

    # Build targets in the same order as nonCertBuild2.cmd
    for target in ("source", "user_docs", "dist", "launcher"):
        run_cmd(["scons", target] + scons_args)


def main() -> int:
    # Ensure we run from the repository root
    repo_root = Path(__file__).resolve().parents[1]
    os.chdir(repo_root)

    # Parse args; only forward ones after "--" to SCons
    raw_args = sys.argv[1:]
    if "--" in raw_args:
        sep = raw_args.index("--")
        forwarded_args = raw_args[sep + 1 :]
    else:
        forwarded_args = raw_args

    _prep_miscdepsjp()
    _build_with_scons(forwarded_args)
    return 0


if __name__ == "__main__":
    sys.exit(main())

