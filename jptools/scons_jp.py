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
- controllerClient: Builds NVDA controller client zip using pack_controller_client.py.
- certprep: Signs pre-existing JP DLLs using env["signExec"].
  Requires signing to be configured (e.g., `certFile` or `apiSigningToken`).
  Intended for local builds only; CI should not enable this.
- certBuild: Convenience alias that runs `certprep` + `source user_docs dist launcher`.

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
    # Sync built client artifacts from extras/controllerClient to jptools/nvdajpClient
    try:
        src_root = repo_root / "extras" / "controllerClient"
        dst_root = repo_root / "jptools" / "nvdajpClient"
        for arch in ("x86", "x64", "arm64"):
            s = src_root / arch
            d = dst_root / arch
            if not s.exists():
                continue
            d.mkdir(parents=True, exist_ok=True)
            for p in s.iterdir():
                if p.is_file():
                    (d / p.name).write_bytes(p.read_bytes())
    except Exception as e:
        # Non-fatal; packaging may still succeed if files already present
        print(f"Warning: Failed to sync controller client artifacts: {e}")
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
            nmake_machine = None  # x86 is default

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

                build_dir = vendor_base
                if not build_dir.exists():
                    print(f"ERROR: vendor source directory not found: {build_dir}")
                    print("  Ensure python-jtalk submodule is checked out.")
                    return 1

                # Build nmake command
                nmake_cmd = ["nmake", "/f", "all.mak"]
                if nmake_machine:
                    nmake_cmd.append(f"MACHINE={nmake_machine}")

                print(f"jtalkPrep: running: {' '.join(nmake_cmd)} in {build_dir}")
                result = run(nmake_cmd, cwd=str(build_dir))

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

    # Note: sourceDir -> miscdepsjp dependency is established in sconstruct.
    # dist -> sourceDir dependency is automatic (dist depends on sourceDir).
    # Therefore, the dependency chain dist -> sourceDir -> miscdepsjp -> jtalkPrep
    # is already established without additional wiring here.

    # Alias: controllerClient (zip artifact)
    out_dir = str(env.get("outputDir", "output"))
    version = str(env.get("version", "local"))
    cc_zip = env.File(os.path.join(out_dir, f"nvda_{version}_controllerClientJp.zip"))
    env.Command(cc_zip, [], _pack_controller_client)
    env.Alias("controllerClient", cc_zip)
    # Ensure controller client binaries are built before packaging JP zip.
    try:
        for arch in ("x86", "x64", "arm64"):
            dll = env.File(os.path.join("extras", "controllerClient", arch, "nvdaControllerClient.dll"))
            hdr = env.File(os.path.join("extras", "controllerClient", arch, "nvdaController.h"))
            env.Depends(cc_zip, [dll, hdr])
    except Exception as e:
        print(f"Warning: Could not set controller client dependencies: {e}")

    # Aliases: jtalkAddon / kgsAddon (package JP add-ons)
    jtalk_stamp = env.File("miscDepsJp/_state/addons/jtalkAddon.stamp")
    env.AlwaysBuild(jtalk_stamp)
    env.Command(jtalk_stamp, [], _pack_jtalk_addon)
    env.Alias("jtalkAddon", jtalk_stamp)

    kgs_stamp = env.File("miscDepsJp/_state/addons/kgsAddon.stamp")
    env.AlwaysBuild(kgs_stamp)
    env.Command(kgs_stamp, [], _pack_kgs_addon)
    env.Alias("kgsAddon", kgs_stamp)

    # Aliases: jpTests / jpCharTests
    jp_tests_stamp = env.File("miscDepsJp/_state/tests/jpTests.stamp")
    env.AlwaysBuild(jp_tests_stamp)
    env.Command(jp_tests_stamp, [], _run_jp_tests)
    env.Alias("jpTests", jp_tests_stamp)

    jp_char_tests_stamp = env.File("miscDepsJp/_state/tests/jpCharTests.stamp")
    env.AlwaysBuild(jp_char_tests_stamp)
    env.Command(jp_char_tests_stamp, [], _run_jpchar_tests)
    env.Alias("jpCharTests", jp_char_tests_stamp)

    # Alias: certprep (sign pre-existing JP DLLs in-place)
    # Note: This intentionally signs inputs which are later packaged into the dist.
    # It relies on upstream signExec (certFile/apiSigningToken) and remains a no-op
    # when signing is not configured (e.g., CI).
    def _signtarget(relpath: str) -> Any:
        src_path = str(repo_root / relpath)
        src_name = Path(src_path).name
        stamp = env.File(f"miscDepsJp/_state/sign/{src_name}.stamp")
        # Use an action that tolerates missing files and writes the stamp either way.
        def _cb(target, source, env, p=src_path):
            return _sign_optional_path(target, source, env, p)
        env.Command(stamp, [], _cb)
        # Ensure the JP overlay runs before signing so files exist in-place
        try:
            env.Depends(stamp, env.Alias("miscdepsjp"))
        except Exception as e:
            # Be conservative if alias lookup fails in early phases
            print(f"Warning: Could not establish dependency for {stamp}: {e}")
        return stamp

    sign_list = [
        # JP jtalk DLLs
        "source/synthDrivers/jtalk/libmecab.dll",
        "source/synthDrivers/jtalk/libopenjtalk.dll",
        # miscDeps runtime DLLs
        "miscDeps/python/brlapi-0.8.dll",
        "miscDeps/python/libgcc_s_dw2-1.dll",
        # braille driver binary shipped in miscDeps
        "miscDeps/source/brailleDisplayDrivers/lilli.dll",
        # wx widgets DLLs from the venv
        ".venv/Lib/site-packages/wx/wxbase32u_net_vc140.dll",
        ".venv/Lib/site-packages/wx/wxbase32u_vc140.dll",
        ".venv/Lib/site-packages/wx/wxmsw32u_core_vc140.dll",
        ".venv/Lib/site-packages/wx/wxmsw32u_html_vc140.dll",
        ".venv/Lib/site-packages/wx/wxmsw32u_stc_vc140.dll",
    ]
    certprep_stamps: list[Any] = []
    for rel in sign_list:
        certprep_stamps.append(_signtarget(rel))
    env.Alias("certprep", certprep_stamps)

    # If signing is enabled (certFile/apiSigningToken set), ensure ordering:
    #  miscdepsjp (overlay) -> certprep (sign DLLs in place) -> dist/launcher
    try:
        if env.get("certFile") or env.get("apiSigningToken"):
            env.Depends(env.Alias("certprep"), env.Alias("miscdepsjp"))
            # Run jtalkPrep before overlay/certprep so libopenjtalk.dll can be picked up
            env.Depends(env.Alias("certprep"), env.Alias("jtalkPrep"))
            env.Depends("dist", env.Alias("certprep"))
            env.Depends("launcher", env.Alias("certprep"))
    except Exception as e:
        # Be conservative if alias lookup fails during early phases
        print(f'Warning: Could not establish certprep ordering: {e}')

    # Alias: certBuild (convenience umbrella alias)
    # Use string targets/aliases so resolution happens after upstream defines them.
    env.Alias("certBuild", [env.Alias("certprep"), "source", "user_docs", "dist", "launcher"])
