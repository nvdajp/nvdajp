#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
import shutil


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

MSVC_ENV_KEYS = (
    "PATH",
    "INCLUDE",
    "LIB",
    "LIBPATH",
    "VCINSTALLDIR",
    "VCTOOLSINSTALLDIR",
    "VSCMD_ARG_TGT_ARCH",
    "WINDOWSSDKDIR",
    "UNIVERSALCRTSDKDIR",
    "CL",
)


def _ensure_nmake_env() -> None:
    """Ensure MSVC build tools (cl/nmake) are on PATH for this process.
    Order of attempts:
    1) If 'cl' seems callable, do nothing.
    2) Use vswhere to locate Visual Studio and call vcvars32/VsDevCmd, import env.
    3) Fallback to JP's jptools/vcsetup.cmd and import env.
    """
    # 1) Fast path: if 'cl' is on PATH, assume VC environment is set.
    try:
        subprocess.run(["cl"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        return
    except FileNotFoundError:
        pass

    repo_root = Path(__file__).resolve().parents[1]

    def _capture_env_via_cmd(call_stmt: str, *, cwd: Path | None = None) -> dict[str, str] | None:
        try:
            out = subprocess.check_output(["cmd", "/c", f"{call_stmt} && set"], text=True, errors="ignore", cwd=str(cwd) if cwd else None)
        except Exception as e:
            print(f"::warning::Failed to initialize MSVC env via: {call_stmt} ({e})")
            return None
        env: dict[str, str] = {}
        for line in out.splitlines():
            if "=" not in line:
                continue
            key, val = line.split("=", 1)
            env[key] = val
        return env

    # 2) Try vswhere-driven activation (handles Enterprise/Professional/BuildTools and CI images)
    vswhere = Path(r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe")
    if vswhere.exists():
        try:
            install_path = subprocess.check_output(
                [
                    str(vswhere),
                    "-latest",
                    "-products",
                    "*",
                    "-requires",
                    "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
                    "-property",
                    "installationPath",
                    "-format",
                    "value",
                ],
                text=True,
                errors="ignore",
            ).strip()
        except Exception:
            install_path = ""

        if install_path:
            # First, try to directly find exact scripts using vswhere -find
            found: list[Path] = []
            for pattern in (
                r"VC\Auxiliary\Build\vcvars32.bat",
                r"VC\Auxiliary\Build\vcvarsall.bat",
                r"Common7\Tools\VsDevCmd.bat",
            ):
                try:
                    p = subprocess.check_output(
                        [str(vswhere), "-latest", "-products", "*", "-find", pattern, "-format", "value"],
                        text=True,
                        errors="ignore",
                    ).strip()
                except Exception:
                    p = ""
                if p:
                    found.append(Path(p))

            # Fallback to constructing from installationPath
            candidates = found or [
                Path(install_path) / "VC" / "Auxiliary" / "Build" / "vcvars32.bat",
                Path(install_path) / "VC" / "Auxiliary" / "Build" / "vcvarsall.bat",
                Path(install_path) / "Common7" / "Tools" / "VsDevCmd.bat",
            ]
            for script in candidates:
                if script.exists():
                    name = script.name.lower()
                    if name == "vsdevcmd.bat":
                        # Prefer x86 target tools for JP build toolchain
                        call = f"set VSCMD_ARG_TGT_ARCH=x86 && call \"{script}\" -no_logo"
                    elif name == "vcvarsall.bat":
                        call = f"call \"{script}\" x86"
                    else:
                        call = f"call \"{script}\""
                    envmap = _capture_env_via_cmd(call)
                    if envmap:
                        # Prefer build-related keys; update PATH/INCLUDE/LIB/LIBPATH and others.
                        updated = 0
                        for k in MSVC_ENV_KEYS:
                            if k in envmap:
                                os.environ[k] = envmap[k]
                                updated += 1
                        # Ensure 32-bit arch flag matches JP toolchain expectation
                        current_cl = os.environ.get("CL") or ""
                        if "/arch:ia32" not in current_cl.lower():
                            os.environ["CL"] = (current_cl + " /arch:IA32").strip()
                        else:
                            os.environ["CL"] = current_cl
                        print(f"[nonCertBuild] MSVC env imported via vswhere from {script.name} ({updated} vars)")
                        return

    # 3) Fallback to JP's repo-local vcsetup.cmd
    vcsetup = repo_root / "jptools" / "vcsetup.cmd"
    if not vcsetup.exists():
        print(f"::warning::VC setup script not found: {vcsetup}")
        return
    envmap = _capture_env_via_cmd(f"call \"{vcsetup}\" >nul", cwd=repo_root)
    if not envmap:
        return
    updated = 0
    for key in MSVC_ENV_KEYS:
        if key in envmap:
            os.environ[key] = envmap[key]
            updated += 1
    if updated:
        print(f"[nonCertBuild] MSVC env imported from vcsetup ({updated} vars)")
    else:
        print("::warning::vcsetup completed but no environment variables were imported")

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
    # Ensure nmake is available; if not, run local vcsetup (both CI and local)
    _ensure_nmake_env()
    _check_vs_version()

    # Run miscDepsJp jtalk prep/build/test (inline build-and-test.cmd)
    md_root = Path("miscDepsJp/jptools")
    run_cmd(["cmd", "/c", "clean.cmd"], cwd=md_root)
    run_cmd(["cmd", "/c", "copy_jtalk_core_files.cmd"], cwd=md_root)
    # Guard the environment again before build steps, in case it changed
    _ensure_nmake_env()
    # jtalk clean→build→install
    jtalk_dir = Path("miscDepsJp/include/jtalk")
    run_cmd(["cmd", "/c", "all-clean.cmd"], cwd=jtalk_dir)
    run_cmd(["cmd", "/c", "all-build.cmd"], cwd=jtalk_dir)
    run_cmd(["cmd", "/c", "all-install.cmd"], cwd=jtalk_dir)
    # jptools tests
    run_cmd(["cmd", "/c", "test.cmd"], cwd=md_root)

    # Setup overlay for miscDepsJp (no jtalk rebuild here; already built above)
    try:
        for p in jtalk_dir.glob("*.pyc"):
            p.unlink(missing_ok=True)  # type: ignore[arg-type]
    except Exception:
        pass

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

    # Overlay policy no longer removes espeak-data. Keep repo content as-is.

    # Run overlay script with CWD=miscDepsJp, script located in repo-root/jptools
    try:
        repo_root = Path(__file__).resolve().parents[1]
        overlay_script = repo_root / "jptools" / "setup_miscdeps_overlay.py"
        run_cmd([sys.executable, str(overlay_script)], cwd=Path("miscDepsJp"))
    except SystemExit:
        # Propagate normal exit
        pass


def _activation_candidates() -> list[str]:
    """Return possible activation call statements for MSVC env (x86)."""
    calls: list[str] = []
    vswhere = Path(r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe")
    def _add_if_exists(path: Path, args: str = ""):
        if path.exists():
            calls.append(f"call \"{path}\"{(' ' + args) if args else ''}")
    # Prefer vswhere -find to get exact bat paths
    if vswhere.exists():
        for pattern, args in (
            (r"VC\Auxiliary\Build\vcvars32.bat", ""),
            (r"VC\Auxiliary\Build\vcvarsall.bat", "x86"),
            (r"Common7\Tools\VsDevCmd.bat", "-no_logo"),
        ):
            try:
                p = subprocess.check_output(
                    [str(vswhere), "-latest", "-products", "*", "-find", pattern, "-format", "value"],
                    text=True,
                    errors="ignore",
                ).strip()
            except Exception:
                p = ""
            if p:
                _add_if_exists(Path(p), args)
    # Fallback to common install roots
    for edition in ("Enterprise", "Professional", "Community", "BuildTools"):
        root = Path(fr"C:\Program Files\Microsoft Visual Studio\2022\{edition}")
        _add_if_exists(root / "VC" / "Auxiliary" / "Build" / "vcvars32.bat")
        _add_if_exists(root / "VC" / "Auxiliary" / "Build" / "vcvarsall.bat", "x86")
        _add_if_exists(root / "Common7" / "Tools" / "VsDevCmd.bat", "-no_logo")
    return calls


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
    # Simple option handling without argparse to keep dependencies minimal
    prep_only = False
    if "--prep-only" in raw_args:
        raw_args.remove("--prep-only")
        prep_only = True
    if "--" in raw_args:
        sep = raw_args.index("--")
        forwarded_args = raw_args[sep + 1 :]
    else:
        forwarded_args = raw_args

    _prep_miscdepsjp()
    if prep_only:
        return 0
    _build_with_scons(forwarded_args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
