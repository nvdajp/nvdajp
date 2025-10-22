#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
import re


def run_cmd(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> None:
    where = f" (cwd={cwd})" if cwd else ""
    print(f"[nonCertBuild] run: {' '.join(cmd)}{where}")
    try:
        subprocess.run(cmd, check=True, cwd=str(cwd) if cwd else None, env=env)
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

    # Run miscDepsJp jtalk prep/build/test (inline build-and-test.cmd)
    md_root = Path("miscDepsJp/jptools")
    run_cmd(["cmd", "/c", "clean.cmd"], cwd=md_root)
    run_cmd(["cmd", "/c", "copy_jtalk_core_files.cmd"], cwd=md_root)
    # The original script invoked python-jtalk vcsetup; do so if it exists
    vcsetup = Path("miscDepsJp/include/python-jtalk/vcsetup.cmd")
    if vcsetup.exists():
        run_cmd(["cmd", "/c", str(vcsetup)])
    # Replace 'patch' invocations in makefiles at runtime to avoid external patch.exe
    _replace_patch_invocations()

    # jtalk clean→build→install
    jtalk_dir = Path("miscDepsJp/include/jtalk")
    run_cmd(["cmd", "/c", "all-clean.cmd"], cwd=jtalk_dir)
    run_cmd(["cmd", "/c", "all-build.cmd"], cwd=jtalk_dir)
    run_cmd(["cmd", "/c", "all-install.cmd"], cwd=jtalk_dir)
    _ensure_libopenjtalk_deployed()
    # python-jtalk clean
    pyjtalk_dir = Path("miscDepsJp/include/python-jtalk")
    run_cmd(["cmd", "/c", "clean.cmd"], cwd=pyjtalk_dir)
    # jptools tests
    run_cmd(["cmd", "/c", "test.cmd"], cwd=md_root)

    # Setup overlay for miscDepsJp (no jtalk rebuild here; already built above)
    try:
        for p in jtalk_dir.glob("*.pyc"):
            p.unlink(missing_ok=True)  # type: ignore[arg-type]
    except Exception:
        pass


def _replace_patch_invocations() -> None:
    """Rewrite 'patch <file> <diff>' lines in jtalk makefiles to use our Python applier.
    This keeps submodules unmodified in VCS; changes are runtime-only.
    """
    files = [
        Path("miscDepsJp/include/python-jtalk/lib/Makefile.mak"),
        Path("miscDepsJp/include/python-jtalk/all.mak"),
    ]
    for mf in files:
        if not mf.exists():
            continue
        content = mf.read_text(encoding="utf-8", errors="ignore")
        # Use absolute interpreter and script path to avoid issues with 'cd' inside makefiles
        py = sys.executable.replace("/", "\\")
        applier = str(Path.cwd() / "jptools" / "apply_patch.py").replace("/", "\\")
        pattern = re.compile(r"^[\t ]*patch\s+(\S+)\s+(\S+)$", re.MULTILINE)

        def _repl(m: re.Match[str]) -> str:
            f1, f2 = m.group(1), m.group(2)
            return f"\t\"{py}\" \"{applier}\" --inplace {f1} {f2}"

        new_content = pattern.sub(_repl, content)
        if new_content != content:
            mf.write_text(new_content, encoding="utf-8", newline="")

    # Remove large/mutable generated dictionary artifacts to keep workspace tidy
    naist_dic = Path("miscDepsJp/include/jtalk/libopenjtalk/mecab-naist-jdic")
    for rel in ["dic", "_temp"]:
        try:
            import shutil as _sh
            _sh.rmtree(naist_dic / rel, ignore_errors=True)
        except Exception:
            pass
    for pat in [
        "nvdajp-custom-dic.csv",
        "nvdajp-eng-dic.csv",
        "nvdajp-roma-dic.csv",
        "nvdajp-tankan-dic.csv",
    ]:
        try:
            (naist_dic / pat).unlink(missing_ok=True)  # type: ignore[arg-type]
        except Exception:
            pass

    # Ensure espeak-data is not overlaid
    espeak_data = Path("source/synthDrivers/espeak-data")
    try:
        import shutil as _sh
        _sh.rmtree(espeak_data, ignore_errors=True)
    except Exception:
        pass

    # Run overlay script from miscDepsJp as original script expects that CWD
    try:
        run_cmd([sys.executable, "jptools/setup_miscdeps_overlay.py"], cwd=Path("miscDepsJp"))
    except SystemExit:
        # Propagate normal exit
        pass


def _ensure_libopenjtalk_deployed() -> None:
    """Ensure libopenjtalk.dll is present where tests expect it.
    If missing, try to locate a built DLL and copy it into place.
    """
    target = Path("miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll")
    if target.exists():
        print(f"[nonCertBuild] libopenjtalk already present at {target}")
        return
    candidates = [
        Path("miscDepsJp/include/python-jtalk/libopenjtalk.dll"),
        Path("miscDepsJp/include/jtalk/lib/libopenjtalk.dll"),
        Path("miscDepsJp/include/jtalk/libopenjtalk.dll"),
    ]
    for c in candidates:
        print(f"[nonCertBuild] check candidate: {c} exists={c.exists()}")
        if c.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            print(f"[nonCertBuild] deploy libopenjtalk.dll from {c} -> {target}")
            import shutil as _sh

            _sh.copy2(c, target)
            return
    print("::warning::libopenjtalk.dll not found after install; tests may fail")


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

