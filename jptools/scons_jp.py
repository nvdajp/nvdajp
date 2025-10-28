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

Aliases added:
- miscdepsjp: Runs jptools/setup_miscdeps_overlay.py and writes a stamp file.
- jpStageControllerClient: Stage controller client artifacts into jptools/nvdajpClient.
- jpControllerClient: Builds JP controller client zip using pack_controller_client.py.
- jpCertExtras: Sign extra JP DLLs using upstream signing logic.
- jpVerifySignatures: Run signtool verify and write a log under output/.

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



def _pack_jtalk_addon(target: list[Any], source: list[Any], env: Any) -> int:
    repo_root = Path.cwd()
    script = repo_root / "jptools" / "pack_jtalk_addon.py"
    if not script.exists():
        return 0
    from subprocess import run
    # Ensure VERSION is available for the packer (used for current date default)
    version = str(env.get("version", ""))
    run_env = os.environ.copy()
    if version:
        run_env["VERSION"] = version
    res = run([sys.executable, str(script)], env=run_env)
    if res.returncode != 0:
        return res.returncode
    # Stamp success
    stamp_path = Path(str(target[0]))
    stamp_path.parent.mkdir(parents=True, exist_ok=True)
    stamp_path.write_text("ok", encoding="utf-8")
    return 0


def _pack_kgs_addon(target: list[Any], source: list[Any], env: Any) -> int:
    repo_root = Path.cwd()
    script = repo_root / "jptools" / "pack_kgs_addon.py"
    if not script.exists():
        return 0
    from subprocess import run
    version = str(env.get("version", ""))
    cmd = [sys.executable, str(script)]
    if version:
        cmd += ["--version", version]
    res = run(cmd)
    if res.returncode != 0:
        return res.returncode
    stamp_path = Path(str(target[0]))
    stamp_path.parent.mkdir(parents=True, exist_ok=True)
    stamp_path.write_text("ok", encoding="utf-8")
    return 0


def _run_jp_tests(target: list[Any], source: list[Any], env: Any) -> int:
    """Run JP dictionary tests similarly to jptools/tests.cmd.
    - Compile ja .po to .mo using msgfmt
    - Run jpDicTest.py
    """
    repo_root = Path.cwd()
    msgfmt = repo_root / "miscDeps" / "tools" / "msgfmt.exe"
    po = repo_root / "source" / "locale" / "ja" / "LC_MESSAGES" / "nvda.po"
    mo = repo_root / "source" / "locale" / "ja" / "LC_MESSAGES" / "nvda.mo"
    from subprocess import run

    if msgfmt.exists() and po.exists():
        res = run([str(msgfmt), str(po), "-o", str(mo)])
        if res.returncode != 0:
            return res.returncode
    # Run jpDicTest.py from jptools directory
    test_script = repo_root / "jptools" / "jpDicTest.py"
    if test_script.exists():
        res = run([sys.executable, str(test_script)], cwd=str(test_script.parent))
        if res.returncode != 0:
            return res.returncode
    # Stamp success
    Path(str(target[0])).parent.mkdir(parents=True, exist_ok=True)
    Path(str(target[0])).write_text("ok", encoding="utf-8")
    return 0


def _run_jpchar_tests(target: list[Any], source: list[Any], env: Any) -> int:
    """Run JP char description tests similarly to jpchar/tests.cmd."""
    repo_root = Path.cwd()
    script = repo_root / "jpchar" / "checkCharDesc.py"
    from subprocess import run
    if script.exists():
        res = run([sys.executable, str(script)], cwd=str(script.parent))
        if res.returncode != 0:
            return res.returncode
    Path(str(target[0])).parent.mkdir(parents=True, exist_ok=True)
    Path(str(target[0])).write_text("ok", encoding="utf-8")
    return 0


def _sign_in_place(target: list[Any], source: list[Any], env: Any) -> int:
    """Sign a pre-existing file (source[0]) in-place using env["signExec"].
    Writes a small stamp file on success.

    - Expects signing to be configured in the environment (certFile/apiSigningToken),
      which is already wired by upstream sconstruct.
    - Follows the retry/selection behavior implemented in upstream signExec.
    """
    # Do not crash if signing is not configured; provide a helpful message.
    signExec = env.get("signExec")
    if not signExec:
        print("JP certprep skipped: signing not configured (set certFile or apiSigningToken)")
        return 0
    src = source[0]
    abspath = src.abspath
    # Ensure only PE images are passed through
    if not abspath.lower().endswith((".dll", ".exe")):
        print(f"JP certprep skipped non-PE file: {abspath}")
        return 0
    if not os.path.isfile(abspath):
        print(f"Warning: file not found for signing, skipping: {abspath}")
        return 0
    # Delegate to upstream signing action
    retval = signExec([src], source, env)
    if retval != 0:
        return retval
    # Stamp
    stamp_path = Path(str(target[0]))
    stamp_path.parent.mkdir(parents=True, exist_ok=True)
    stamp_path.write_text("ok", encoding="utf-8")
    return 0


def _sign_optional_path(target: list[Any], source: list[Any], env: Any, path: str) -> int:
    """Sign file at `path` if it exists; otherwise skip and write a stamp.

    This is tolerant of missing inputs so certprep can run before all payloads
    are present. Intended only for local convenience.
    """
    signExec = env.get("signExec")
    stamp_path = Path(str(target[0]))
    stamp_path.parent.mkdir(parents=True, exist_ok=True)
    if not signExec:
        print("JP certprep skipped: signing not configured (set certFile or apiSigningToken)")
        stamp_path.write_text("skip:no-sign-config", encoding="utf-8")
        return 0
    if not os.path.isfile(path):
        print(f"Warning: file not found for signing, skipping: {path}")
        stamp_path.write_text("skip:not-found", encoding="utf-8")
        return 0
    try:
        node = env.File(path)
        retval = signExec([node], [node], env)
        if retval != 0:
            return retval
    except Exception as e:
        print(f"Error: signing failed for {path}: {e}")
        return 1
    stamp_path.write_text("ok", encoding="utf-8")
    return 0

def _find_vcvarsall() -> str | None:
    """Find vcvarsall.bat in common Visual Studio install locations.
    Returns absolute path if found, None otherwise.
    """
    common_paths = [
        r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat",
        r"C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvarsall.bat",
        r"C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvarsall.bat",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\Build\vcvarsall.bat",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\VC\Auxiliary\Build\vcvarsall.bat",
    ]
    for p in common_paths:
        if Path(p).exists():
            return p
    return None


def _get_vcvarsall_env(vcvarsall_path: str, arch: str) -> dict[str, str] | None:
    """Call vcvarsall.bat and capture the resulting environment variables.
    Returns a copy of os.environ with MSVC environment added, or None on failure.
    """
    import subprocess
    import tempfile

    # Create a temporary batch file that calls vcvarsall and outputs env
    with tempfile.NamedTemporaryFile(mode="w", suffix=".bat", delete=False) as f:
        bat_path = f.name
        f.write(f'@echo off\n')
        f.write(f'call "{vcvarsall_path}" {arch} >nul\n')
        f.write(f'if errorlevel 1 exit /b 1\n')
        f.write(f'set\n')

    try:
        result = subprocess.run(
            [bat_path],
            capture_output=True,
            text=True,
            shell=True,
            check=False,
        )
        if result.returncode != 0:
            return None

        # Parse environment variables from output
        env = os.environ.copy()
        for line in result.stdout.splitlines():
            if "=" in line:
                key, _, value = line.partition("=")
                env[key] = value
        return env
    finally:
        try:
            os.unlink(bat_path)
        except Exception:
            pass




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


def _filter_untracked(repo_root: Path, paths: list[str]) -> list[str]:
    """Return only files not tracked by git. Tracked files must not be cleaned.

    This ensures that `scons -c` does not delete repository-tracked sources
    that happen to be overlay destinations.
    """
    # Lazy import to avoid unnecessary overhead when not cleaning
    import subprocess
    out: list[str] = []
    for p in paths:
        try:
            subprocess.run(
                ["git", "ls-files", "--error-unmatch", p],
                cwd=str(repo_root),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            # Tracked -> do not clean
        except subprocess.CalledProcessError:
            out.append(p)  # Untracked -> safe to clean
        except Exception:
            # Be conservative on unexpected errors
            pass
    return out


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
        files = _compute_overlay_targets(repo_root)
        files = _filter_untracked(repo_root, files)
        if files:
            env.Clean(stamp, files)
    except Exception:
        pass


    # Alias: jtalkPrep (ensure JP jtalk payload is present before overlay)
    def _ensure_jtalk_payload(target: list[Any], source: list[Any], env: Any) -> int:
        """Prepare JP jtalk payload for overlay with on-demand build.

        - Resolve TARGET_ARCH (default x86)
        - Locate vendor DLL under miscDepsJp/include/python-jtalk[/x64]/libopenjtalk.dll
        - If missing, attempt to build via nmake (requires MSVC environment)
        - Write payload into miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll
        """
        repo_root = Path.cwd()
        arch = str(env.get("TARGET_ARCH", "x86")).lower()
        vendor_base = repo_root / "miscDepsJp" / "include" / "python-jtalk"

        if arch == "x64":
            src_prebuilt = vendor_base / "x64" / "libopenjtalk.dll"
            nmake_machine = "x64"
        else:
            src_prebuilt = vendor_base / "libopenjtalk.dll"
            nmake_machine = "x86"  # Must pass explicitly (all.mak passes MACHINE=$(MACHINE) to lib/Makefile.mak)

        dst_payload = (
            repo_root
            / "miscDepsJp"
            / "source"
            / "synthDrivers"
            / "jtalk"
            / "libopenjtalk.dll"
        )

        print(f"jtalkPrep: using TARGET_ARCH={arch}")
        print(f"jtalkPrep: looking for vendor DLL: {src_prebuilt}")

        # If DLL does not exist, attempt to build via nmake
        if not src_prebuilt.exists():
            print(f"jtalkPrep: DLL not found, attempting to build via nmake...")
            try:
                from subprocess import run
                import shutil

                build_dir = vendor_base
                if not build_dir.exists():
                    print(f"ERROR: vendor source directory not found: {build_dir}")
                    print("  Ensure python-jtalk submodule is checked out.")
                    return 1

                # Copy vendor files from miscDepsJp/include into python-jtalk
                # (as done in copy_jtalk_core_files.cmd)
                misc_include = repo_root / "miscDepsJp" / "include"
                hts_src = misc_include / "htsengineapi"
                hts_dst = build_dir / "htsengineapi"
                lib_src = misc_include / "libopenjtalk"
                lib_dst = build_dir / "libopenjtalk"

                if hts_src.exists():
                    print(f"jtalkPrep: copying htsengineapi from {hts_src} to {hts_dst}")
                    if hts_dst.exists():
                        shutil.rmtree(str(hts_dst))
                    shutil.copytree(str(hts_src), str(hts_dst))
                else:
                    print(f"Warning: htsengineapi source not found at {hts_src}")

                if lib_src.exists():
                    print(f"jtalkPrep: copying libopenjtalk from {lib_src} to {lib_dst}")
                    if lib_dst.exists():
                        shutil.rmtree(str(lib_dst))
                    shutil.copytree(str(lib_src), str(lib_dst))
                else:
                    print(f"Warning: libopenjtalk source not found at {lib_src}")

                # Check if nmake is available in PATH
                # If not, try to setup MSVC environment by calling vcvarsall.bat
                import subprocess
                nmake_env = os.environ.copy()
                try:
                    run(["nmake", "/?"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                except (FileNotFoundError, subprocess.CalledProcessError):
                    print(f"jtalkPrep: nmake not in PATH, attempting to setup MSVC environment...")
                    vcvarsall = _find_vcvarsall()
                    if vcvarsall:
                        print(f"jtalkPrep: found vcvarsall.bat: {vcvarsall}")
                        nmake_env = _get_vcvarsall_env(vcvarsall, "x86")
                        if not nmake_env:
                            print(f"ERROR: failed to setup MSVC environment via vcvarsall.bat")
                            print(f"  Run from Visual Studio Developer Command Prompt instead")
                            return 1
                    else:
                        print(f"ERROR: nmake not found and vcvarsall.bat not detected")
                        print(f"  Install Visual Studio with C++ Desktop Development workload")
                        print(f"  Or run from Visual Studio Developer Command Prompt")
                        return 1

                # Build nmake command
                # Always pass MACHINE (all.mak requires it, even for x86)
                nmake_cmd = ["nmake", "/f", "all.mak", f"MACHINE={nmake_machine}"]

                print(f"jtalkPrep: running: {' '.join(nmake_cmd)} in {build_dir}")
                result = run(nmake_cmd, cwd=str(build_dir), env=nmake_env)

                if result.returncode != 0:
                    print(f"ERROR: nmake failed with exit code {result.returncode}")
                    print("  Ensure MSVC environment is configured (ilammy/msvc-dev-cmd or vcvarsall.bat)")
                    return 1

                # Verify DLL was created
                if not src_prebuilt.exists():
                    print(f"ERROR: nmake succeeded but DLL not found at {src_prebuilt}")
                    print("  Check nmake output for errors")
                    return 1

                print(f"jtalkPrep: build succeeded, DLL created at {src_prebuilt}")

            except FileNotFoundError as e:
                print(f"ERROR: nmake not found in PATH")
                print(f"  {e}")
                print(f"  Ensure MSVC environment is configured before running SCons:")
                print(f"    - CI: use ilammy/msvc-dev-cmd action")
                print(f"    - Local: run vcvarsall.bat or Visual Studio Developer Command Prompt")
                print(f"    - certBuild2023.cmd: add vcvarsall.bat call before SCons")
                return 1
            except Exception as e:
                print(f"ERROR: failed to build vendor DLL: {e}")
                return 1
        else:
            print(f"jtalkPrep: using existing DLL (build skipped)")

        # Copy DLL to payload location
        try:
            dst_payload.parent.mkdir(parents=True, exist_ok=True)
            data = src_prebuilt.read_bytes()
            dst_payload.write_bytes(data)
            print(f"jtalkPrep: payload -> {dst_payload}")
        except Exception as e:
            print(f"ERROR: jtalkPrep payload copy failed: {e}")
            return 1

        Path(str(target[0])).parent.mkdir(parents=True, exist_ok=True)
        Path(str(target[0])).write_text("ok", encoding="utf-8")
        return 0

    jtalk_prep_stamp = env.File("miscDepsJp/_state/prep/jtalkPrep.stamp")
    env.AlwaysBuild(jtalk_prep_stamp)
    env.Command(jtalk_prep_stamp, [], _ensure_jtalk_payload)
    env.Alias("jtalkPrep", jtalk_prep_stamp)

    # Ensure overlay runs after jtalkPrep so fallback payload is included
    try:
        env.Depends(env.Alias("miscdepsjp"), env.Alias("jtalkPrep"))
    except Exception:
        pass

    # Note: Dependencies are already established in sconstruct:
    #   - sourceDir -> miscdepsjp (L403)
    #   - dist -> sourceDir (L567, dist depends on sourceDir in NVDADist)
    # This creates the dependency chain: dist -> sourceDir -> miscdepsjp -> jtalkPrep
    # No additional wiring needed here; using Dir/target objects (not Alias) is more robust.

    # Alias: jpControllerClient (zip artifact)
    out_dir = str(env.get("outputDir", "output"))
    version = str(env.get("version", "local"))
    cc_zip = env.File(os.path.join(out_dir, f"nvda_{version}_controllerClientJp.zip"))
    env.Command(cc_zip, [], _pack_controller_client)
    env.Alias("jpControllerClient", cc_zip)

    # Alias: jpStageControllerClient (copy built client files into nvdajpClient tree)
    def _stage_controller_client(target: list[Any], source: list[Any], env: Any) -> int:
        from pathlib import Path
        import shutil

        repo_root = Path.cwd()
        # Where NVDA places built controller client per-arch
        build_root = repo_root / "build"
        # Destination used by jptools/pack_controller_client.py
        client_root = repo_root / "jptools" / "nvdajpClient"

        # (dest_arch, build_arch)
        arch_map = (
            ("x86", "x86"),
            ("x64", "x86_64"),
            ("arm64", "arm64"),
        )

        files = (
            "nvdaController.h",
            "nvdaControllerClient.dll",
            "nvdaControllerClient.pdb",
            "nvdaControllerClient.exp",
            "nvdaControllerClient.lib",
        )

        copied_any = False
        for dest_arch, build_arch in arch_map:
            src_dir = build_root / build_arch / "client"
            dst_dir = client_root / dest_arch
            try:
                dst_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass
            for name in files:
                src = src_dir / name
                dst = dst_dir / name
                try:
                    if src.exists():
                        shutil.copy2(str(src), str(dst))
                        copied_any = True
                    else:
                        # Tolerate missing files (e.g., arch not built)
                        continue
                except Exception as e:
                    print(f"Warning: failed to copy {src} -> {dst}: {e}")
                    # Keep going; staging is best-effort
                    continue

        # Write/update stamp
        stamp_path = Path(str(target[0]))
        stamp_path.parent.mkdir(parents=True, exist_ok=True)
        stamp_path.write_text("ok" if copied_any else "skip:no-files", encoding="utf-8")
        return 0

    stage_stamp = env.File("miscDepsJp/_state/controllerClient/stage.stamp")
    env.AlwaysBuild(stage_stamp)
    env.Command(stage_stamp, [], _stage_controller_client)
    env.Alias("jpStageControllerClient", stage_stamp)
    # Ensure packaging waits for staging if both are invoked together
    try:
        env.Depends(cc_zip, stage_stamp)
    except Exception:
        pass

    # Aliases: JP add-ons (packaging)
    jtalk_stamp = env.File("miscDepsJp/_state/addons/jtalk.stamp")
    env.AlwaysBuild(jtalk_stamp)
    env.Command(jtalk_stamp, [], _pack_jtalk_addon)
    kgs_stamp = env.File("miscDepsJp/_state/addons/kgs.stamp")
    env.AlwaysBuild(kgs_stamp)
    env.Command(kgs_stamp, [], _pack_kgs_addon)
    env.Alias("jtalkAddon", jtalk_stamp)
    env.Alias("kgsAddon", kgs_stamp)
    env.Alias("jpAddons", [jtalk_stamp, kgs_stamp])

    # Alias: jpCertExtras — sign extra PE files outside of core SCons graph.
    # This mirrors legacy certBuild2023.cmd behavior but is tolerant to missing files
    # and skips if signing is not configured.
    extra_paths: list[str] = [
        # JP synth driver payloads
        os.path.join("source", "synthDrivers", "jtalk", "libmecab.dll"),
        os.path.join("source", "synthDrivers", "jtalk", "libopenjtalk.dll"),
        # miscDeps DLLs
        os.path.join("miscDeps", "python", "brlapi-0.8.dll"),
        os.path.join("miscDeps", "python", "libgcc_s_dw2-1.dll"),
        os.path.join("miscDeps", "source", "brailleDisplayDrivers", "lilli.dll"),
        # wxWidgets DLLs in venv (names used in legacy scripts)
        os.path.join(".venv", "Lib", "site-packages", "wx", "wxbase32u_net_vc140.dll"),
        os.path.join(".venv", "Lib", "site-packages", "wx", "wxbase32u_vc140.dll"),
        os.path.join(".venv", "Lib", "site-packages", "wx", "wxmsw32u_core_vc140.dll"),
        os.path.join(".venv", "Lib", "site-packages", "wx", "wxmsw32u_html_vc140.dll"),
        os.path.join(".venv", "Lib", "site-packages", "wx", "wxmsw32u_stc_vc140.dll"),
    ]

    cert_stamps = []
    for p in extra_paths:
        stamp = env.File(os.path.join("miscDepsJp", "_state", "cert", f"{Path(p).name}.stamp"))
        env.AlwaysBuild(stamp)
        # Bind the path value at definition time via default arg
        # Use SCons action signature names (target, source, env) to match keyword invocation.
        env.Command(stamp, [], lambda target, source, env, _p=p: _sign_optional_path(target, source, env, _p))
        cert_stamps.append(stamp)
    env.Alias("jpCertExtras", cert_stamps)

    # Alias: jpVerifySignatures — verify authenticode signatures with signtool
    def _verify_signatures(target: list[Any], source: list[Any], env: Any) -> int:
        import subprocess
        from pathlib import Path

        repo_root = Path.cwd()
        out_dir = repo_root / str(env.get("outputDir", "output"))
        version = str(env.get("version", "local"))
        log_path = out_dir / f"nvda_{version}_verify.log"
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

        signtool = os.getenv("SIGNTOOL") or "signtool"
        patterns = [
            out_dir.glob("*.exe"),
            (repo_root / "dist").rglob("*.exe"),
            (repo_root / "dist").rglob("*.dll"),
        ]

        files: list[Path] = []
        for it in patterns:
            try:
                files.extend([p for p in it if p.is_file()])
            except Exception:
                continue

        rc = 0
        with open(log_path, "w", encoding="utf-8") as log:
            for f in sorted(set(files)):
                try:
                    res = subprocess.run([signtool, "verify", "/pa", str(f)], capture_output=True, text=True)
                    if res.returncode != 0:
                        rc = res.returncode or 1
                    log.write(f"## {f}\n")
                    if res.stdout:
                        log.write(res.stdout)
                    if res.stderr:
                        log.write(res.stderr)
                    log.write("\n")
                except FileNotFoundError:
                    # signtool missing; fail with clear message
                    with open(log_path, "a", encoding="utf-8") as l2:
                        l2.write("signtool not found in PATH. Set SIGNTOOL env or install Windows SDK.\n")
                    return 1
                except Exception as e:
                    with open(log_path, "a", encoding="utf-8") as l2:
                        l2.write(f"Error verifying {f}: {e}\n")
                    rc = rc or 1

        # Stamp
        stamp_path = Path(str(target[0]))
        stamp_path.parent.mkdir(parents=True, exist_ok=True)
        stamp_path.write_text("ok" if rc == 0 else "fail", encoding="utf-8")
        return rc

    verify_stamp = env.File("miscDepsJp/_state/verify/signatures.stamp")
    env.AlwaysBuild(verify_stamp)
    env.Command(verify_stamp, [], _verify_signatures)
    env.Alias("jpVerifySignatures", verify_stamp)
