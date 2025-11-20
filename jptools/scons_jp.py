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

These are intentionally light-weight and safe; wiring them into other
targets can be done in later phases when stable.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
import shutil
from typing import Any


def _copy_jtalk_core_files(repo_root: Path) -> int:
	"""Copy JTalk core Python files from miscDepsJp/include/python-jtalk to source/synthDrivers/jtalk.

	This replicates the functionality of copy_jtalk_core_files.cmd.
	"""
	python_jtalk_dir = repo_root / "miscDepsJp" / "include" / "python-jtalk"
	jtalk_dest_dir = repo_root / "source" / "synthDrivers" / "jtalk"

	if not python_jtalk_dir.exists():
		print(f"Error: python-jtalk directory not found: {python_jtalk_dir}")
		return 1

	if not jtalk_dest_dir.exists():
		print(f"Error: jtalk destination directory not found: {jtalk_dest_dir}")
		return 1

	files_to_copy = [
		"jtalkCore.py",
		"mecab.py",
		"text2mecab.py",
	]

	import shutil
	missing_files: list[str] = []
	for filename in files_to_copy:
		src = python_jtalk_dir / filename
		dst = jtalk_dest_dir / filename
		if src.exists():
			shutil.copy2(src, dst)
			print(f"Copied {filename} to {dst}")
		else:
			print(f"Error: Source file not found: {src}")
			missing_files.append(filename)

	if missing_files:
		return 1

	return 0


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

    # Copy JTalk core files (equivalent to copy_jtalk_core_files.cmd)
    copy_result = _copy_jtalk_core_files(repo_root)
    if copy_result != 0:
        return copy_result

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

    # Run vcvarsall inside cmd.exe, then dump the environment (classic pattern).
    cmd = f'"{vcvarsall_path}" {arch} && echo __ENV_START__ && set'
    result = subprocess.run(
        ["cmd", "/s", "/c", cmd],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(f"  vcvarsall.bat failed with return code {result.returncode}")
        if result.stderr:
            print(f"  stderr: {result.stderr}")
        if result.stdout:
            print(f"  stdout: {result.stdout}")
        return None

    stdout = result.stdout or ""
    if "__ENV_START__" not in stdout:
        print("  Warning: __ENV_START__ marker not found in vcvarsall output")
        print(f"  vcvarsall stdout (first 500 chars): {stdout[:500]}")
        return None

    # Parse environment variables from output after __ENV_START__ marker
    env = os.environ.copy()
    env_section = False
    env_lines_found = 0
    for line in stdout.splitlines():
        if "__ENV_START__" in line:
            env_section = True
            continue
        if env_section and "=" in line:
            key, _, value = line.partition("=")
            env[key] = value
            env_lines_found += 1

    print(f"  vcvarsall: captured {env_lines_found} environment variables")

    # Verify nmake is in the PATH
    path = env.get("PATH", "")
    if "nmake" not in path.lower() and "vc\\tools" not in path.lower():
        print("  Warning: vcvarsall succeeded but PATH doesn't contain MSVC tools")
        print(f"  Original PATH: {os.environ.get('PATH', '')[:180]}...")
        print(f"  Captured PATH: {path[:180]}...")
        print(f"  vcvarsall stdout (first 500 chars): {stdout[:500]}")
        return None

    return env




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


    # Alias: jp_tests (run JP dictionary tests and JP char description tests)
    jp_tests_stamp = env.File("jptools/_state/jp_tests.stamp")
    env.AlwaysBuild(jp_tests_stamp)
    env.Command(jp_tests_stamp, [], _run_jp_tests)

    jpchar_tests_stamp = env.File("jpchar/_state/jpchar_tests.stamp")
    env.AlwaysBuild(jpchar_tests_stamp)
    env.Command(jpchar_tests_stamp, [], _run_jpchar_tests)

    env.Alias("jp_tests", [jp_tests_stamp, jpchar_tests_stamp])

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

        if arch in ("x64", "x86_64"):
            src_prebuilt = vendor_base / "x64" / "libopenjtalk.dll"
            nmake_machine = "x64"
        else:
            src_prebuilt = vendor_base / "libopenjtalk.dll"
            nmake_machine = "x86"  # Must pass explicitly (all.mak passes MACHINE=$(MACHINE) to lib/Makefile.mak)

        built_dll = src_prebuilt

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
                # If not, we'll run nmake via vcvarsall.bat in the same shell
                import subprocess
                try:
                    run(["nmake", "/?"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                    print(f"jtalkPrep: nmake found in PATH")
                    use_vcvarsall = False
                except (FileNotFoundError, subprocess.CalledProcessError):
                    print(f"jtalkPrep: nmake not in PATH, will use vcvarsall.bat")
                    vcvarsall = _find_vcvarsall()
                    if not vcvarsall:
                        print(f"ERROR: nmake not found and vcvarsall.bat not detected")
                        print(f"  Install Visual Studio with C++ Desktop Development workload")
                        print(f"  Or run from Visual Studio Developer Command Prompt")
                        return 1
                    print(f"jtalkPrep: found vcvarsall.bat: {vcvarsall}")
                    use_vcvarsall = True

                # Build nmake command - if using vcvarsall, wrap it in cmd /c call
                if use_vcvarsall:
                    # Run vcvarsall.bat and nmake in the same cmd.exe shell
                    # This ensures the environment variables are available to nmake
                    print(f"jtalkPrep: running nmake via vcvarsall.bat with arch={nmake_machine}")
                    # Use shell=True to avoid subprocess quote escaping issues
                    cmd_script = f'call "{vcvarsall}" {nmake_machine} && nmake /f all.mak MACHINE={nmake_machine}'
                    result = run(
                        cmd_script,
                        cwd=str(build_dir),
                        capture_output=False,  # Let output go to console for debugging
                        shell=True,  # Required to handle quotes in vcvarsall path correctly
                    )
                else:
                    nmake_cmd = ["nmake", "/f", "all.mak", f"MACHINE={nmake_machine}"]
                    print(f"jtalkPrep: running: {' '.join(nmake_cmd)} in {build_dir}")
                    result = run(nmake_cmd, cwd=str(build_dir))

                if result.returncode != 0:
                    print(f"ERROR: nmake failed with exit code {result.returncode}")
                    print("  Ensure MSVC environment is configured (ilammy/msvc-dev-cmd or vcvarsall.bat)")
                    return 1

                # Verify DLL was created
                if not built_dll.exists():
                    print(f"ERROR: nmake succeeded but DLL not found at {built_dll}")
                    print("  Check nmake output for errors")
                    return 1

                if src_prebuilt != built_dll:
                    src_prebuilt.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(built_dll, src_prebuilt)

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

    # Alias: jtalkSync (build/copy jtalk dictionay and python stubs into source/)
    def _sync_jtalk_assets(target: list[Any], source: list[Any], env: Any) -> int:
        repo_root = Path.cwd()
        vendor_base = repo_root / "miscDepsJp" / "include" / "python-jtalk"
        jtalk_dir = repo_root / "miscDepsJp" / "source" / "synthDrivers" / "jtalk"
        dic_src = vendor_base / "dic"
        dic_dst = jtalk_dir / "dic"
        # If vendor dic is missing, fall back to the already-present source dic
        source_dic = jtalk_dir / "dic"
        source_sys_dic = source_dic / "sys.dic"

        try:
            jtalk_dir.mkdir(parents=True, exist_ok=True)
            dic_dst.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"jtalkSync: failed to create destination dirs: {e}")
            return 1

        def _run_nmake(machine: str) -> int:
            import subprocess
            from subprocess import run

            try:
                run(["nmake", "/?"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                use_vcvarsall = False
            except (FileNotFoundError, subprocess.CalledProcessError):
                vcvarsall = _find_vcvarsall()
                if not vcvarsall:
                    print("jtalkSync: nmake not found and vcvarsall.bat not detected")
                    return 1
                use_vcvarsall = True
                cmd_script = f'call "{vcvarsall}" {machine} && nmake /f all.mak MACHINE={machine}'
                result = run(cmd_script, cwd=str(vendor_base), shell=True)
                return result.returncode
            cmd = ["nmake", "/f", "all.mak", f"MACHINE={machine}"]
            result = run(cmd, cwd=str(vendor_base))
            return result.returncode

        sys_dic = dic_src / "sys.dic"
        # Short-circuit: if source dic already has sys.dic, reuse it without building
        if not sys_dic.exists() and source_sys_dic.exists():
            print(f"jtalkSync: using existing source dic as fallback: {source_dic}")
            dic_src = source_dic
            sys_dic = dic_src / "sys.dic"
        # If the vendor dic is missing, attempt to build it; otherwise, if source already has built dic, reuse it.
        if not sys_dic.exists():
            # Prefer existing source dic if already present
            if source_dic.joinpath("sys.dic").exists():
                print(f"jtalkSync: using existing source dic as fallback: {source_dic}")
                dic_src = source_dic
                sys_dic = dic_src / "sys.dic"
            else:
                # Try to build mecab binary and dictionary via mecab-naist-jdic Makefile
                def _build_mecab_bin(machine: str) -> int:
                    base = vendor_base / "libopenjtalk" / "mecab"
                    makefile = base / "Makefile.mak"
                    if not makefile.exists():
                        print(f"jtalkSync: Makefile.mak not found for mecab bin build: {makefile}")
                        return 1
                    import subprocess
                    from subprocess import run
                    try:
                        run(["nmake", "/?"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                        use_vcvarsall = False
                    except (FileNotFoundError, subprocess.CalledProcessError):
                        vcvarsall = _find_vcvarsall()
                        if not vcvarsall:
                            print("jtalkSync: nmake not found and vcvarsall.bat not detected for mecab bin build")
                            return 1
                        use_vcvarsall = True
                        cmd_script = f'call "{vcvarsall}" {machine} && nmake /f Makefile.mak MACHINE={machine}'
                        result = run(cmd_script, cwd=str(base), shell=True)
                        return result.returncode
                    cmd = ["nmake", "/f", "Makefile.mak", f"MACHINE={machine}"]
                    result = run(cmd, cwd=str(base))
                    return result.returncode

                def _build_dic(machine: str) -> int:
                    base = vendor_base / "libopenjtalk" / "mecab-naist-jdic"
                    makefile = base / "Makefile.mak"
                    if not makefile.exists():
                        print(f"jtalkSync: Makefile.mak not found for dictionary build: {makefile}")
                        return 1
                    import subprocess
                    from subprocess import run
                    try:
                        run(["nmake", "/?"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                        use_vcvarsall = False
                    except (FileNotFoundError, subprocess.CalledProcessError):
                        vcvarsall = _find_vcvarsall()
                        if not vcvarsall:
                            print("jtalkSync: nmake not found and vcvarsall.bat not detected for dic build")
                            return 1
                        use_vcvarsall = True
                        cmd_script = f'call "{vcvarsall}" {machine} && nmake /f Makefile.mak MACHINE={machine}'
                        result = run(cmd_script, cwd=str(base), shell=True)
                        return result.returncode
                    cmd = ["nmake", "/f", "Makefile.mak", f"MACHINE={machine}"]
                    result = run(cmd, cwd=str(base))
                    return result.returncode

                arch = str(env.get("TARGET_ARCH", "x86")).lower()
                machine = "x64" if arch in ("x64", "x86_64") else "x86"

                print("jtalkSync: sys.dic missing; attempting to build python-jtalk (nmake all) and mecab dic")
                rc = _run_nmake(machine)
                if rc != 0:
                    print(f"jtalkSync: nmake (all.mak) failed with rc={rc}")
                    return rc

                # Build mecab binary (mecab-dict-index.exe) if missing
                mecab_bin = vendor_base / "libopenjtalk" / "mecab" / "src" / "mecab-dict-index.exe"
                if not mecab_bin.exists():
                    rc_bin = _build_mecab_bin(machine)
                    if rc_bin != 0:
                        print(f"jtalkSync: nmake (mecab) failed with rc={rc_bin}")
                        return rc_bin
                    if not mecab_bin.exists():
                        print(f"jtalkSync: mecab-dict-index.exe still missing after build: {mecab_bin}")
                        return 1

                # After all.mak and mecab bin, try explicit dic build if still missing
                if not sys_dic.exists():
                    rc_dic = _build_dic(machine)
                    if rc_dic != 0:
                        print(f"jtalkSync: nmake (mecab-naist-jdic) failed with rc={rc_dic}")
                        return rc_dic
                    # Dictionary build outputs to libopenjtalk/mecab-naist-jdic/dic
                    built_dic = vendor_base / "libopenjtalk" / "mecab-naist-jdic" / "dic"
                    if built_dic.joinpath("sys.dic").exists():
                        dic_src = built_dic
                        sys_dic = dic_src / "sys.dic"

                if not sys_dic.exists():
                    print(f"jtalkSync: sys.dic still missing after build; no fallback available")
                    return 1

        # Copy dictionary files
        try:
            if dic_src.resolve() == dic_dst.resolve():
                print(f"jtalkSync: dictionary source and destination are identical; skipping copy.")
            else:
                dic_files = [
                    "sys.dic",
                    "unk.dic",
                    "char.bin",
                    "matrix.bin",
                    "left-id.def",
                    "right-id.def",
                    "rewrite.def",
                    "pos-id.def",
                    "dicrc",
                    "DIC_VERSION",
                ]
                for name in dic_files:
                    src = dic_src / name
                    if src.exists():
                        shutil.copy2(src, dic_dst / name)
                print(f"jtalkSync: copied dictionary assets to {dic_dst}")
        except Exception as e:
            print(f"jtalkSync: failed to copy dictionary assets: {e}")
            return 1

        # Copy core python/jtalk files if present
        try:
            core_files = [
                "libmecab.dll",
                "libopenjtalk.dll",
                "mecab.py",
                "text2mecab.py",
                "jtalkCore.py",
            ]
            for name in core_files:
                src = vendor_base / name
                if src.exists():
                    shutil.copy2(src, jtalk_dir / name)
            # Also try arch-specific libopenjtalk if present (x64)
            arch = str(env.get("TARGET_ARCH", "x86")).lower()
            if arch in ("x64", "x86_64"):
                src64 = vendor_base / "x64" / "libopenjtalk.dll"
                if src64.exists():
                    shutil.copy2(src64, jtalk_dir / "libopenjtalk.dll")
            print(f"jtalkSync: copied core assets to {jtalk_dir}")
        except Exception as e:
            print(f"jtalkSync: failed to copy core assets: {e}")
            return 1

        stamp_path = Path(str(target[0]))
        stamp_path.parent.mkdir(parents=True, exist_ok=True)
        stamp_path.write_text("ok", encoding="utf-8")
        return 0

    jtalk_sync_stamp = env.File("miscDepsJp/_state/prep/jtalkSync.stamp")
    env.AlwaysBuild(jtalk_sync_stamp)
    env.Command(jtalk_sync_stamp, [], _sync_jtalk_assets)
    env.Alias("jtalkSync", jtalk_sync_stamp)

    try:
        env.Depends(env.Alias("miscdepsjp"), env.Alias("jtalkSync"))
    except Exception:
        pass

    # Note: Dependencies are already established in sconstruct:
    #   - sourceDir -> miscdepsjp (L403)
    #   - dist -> sourceDir (L567, dist depends on sourceDir in NVDADist)
    # This creates the dependency chain: dist -> sourceDir -> miscdepsjp -> jtalkPrep
    # No additional wiring needed here; using Dir/target objects (not Alias) is more robust.



    # Alias: controllerClient (zip artifact)
    out_dir = str(env.get("outputDir", "output"))
    version = str(env.get("version", "local"))
    cc_zip = env.File(os.path.join(out_dir, f"nvda_{version}_controllerClientJp.zip"))
    env.Command(cc_zip, [], _pack_controller_client)
    env.Alias("controllerClient", cc_zip)

    # Alias: jpAddons (build JP addons using existing packers)
    jtalk_addon_stamp = env.File("jptools/_state/jtalk_addon.stamp")
    env.AlwaysBuild(jtalk_addon_stamp)
    env.Command(jtalk_addon_stamp, [], _pack_jtalk_addon)

    kgs_addon_stamp = env.File("jptools/_state/kgs_addon.stamp")
    env.AlwaysBuild(kgs_addon_stamp)
    env.Command(kgs_addon_stamp, [], _pack_kgs_addon)

    env.Alias("jpAddons", [jtalk_addon_stamp, kgs_addon_stamp])

    # JP aliases required by certBuild2023.cmd (minimal safe wiring)
    # 1) Stage controller client artifacts (ensure client root exists)
    def _stage_controller_client(target: list[Any], source: list[Any], env: Any) -> int:
        repo_root = Path.cwd()
        client_root = repo_root / "jptools" / "nvdajpClient"
        try:
            client_root.mkdir(parents=True, exist_ok=True)
        except Exception:
            return 1
        stamp_path = Path(str(target[0]))
        stamp_path.parent.mkdir(parents=True, exist_ok=True)
        stamp_path.write_text("ok", encoding="utf-8")
        return 0

    jp_stage_stamp = env.File("jptools/_state/jp_stage_controller_client.stamp")
    env.AlwaysBuild(jp_stage_stamp)
    env.Command(jp_stage_stamp, [], _stage_controller_client)
    env.Alias("jpStageControllerClient", jp_stage_stamp)

    # 2) JP controller client zip (re-export existing alias for compatibility)
    try:
        env.Alias("jpControllerClient", env.Alias("controllerClient"))
    except Exception:
        pass

    # 3) JP cert extras (use upstream signExec to sign optional artifacts)
    def _cert_extras(target: list[Any], source: list[Any], env: Any) -> int:
        signExec = env.get("signExec")
        stamp_path = Path(str(target[0]))
        stamp_path.parent.mkdir(parents=True, exist_ok=True)
        if not signExec:
            stamp_path.write_text("skip:no-sign-config", encoding="utf-8")
            return 0
        # Discover candidate artifacts to sign (optional; skip if missing)
        repo_root = Path.cwd()
        candidates: list[Path] = []
        # Latest built installer under output/nvda_*.exe
        try:
            out_dir = repo_root / "output"
            if out_dir.exists():
                exe_candidates = sorted(out_dir.glob("nvda_*.exe"), key=lambda p: p.stat().st_mtime, reverse=True)
                if exe_candidates:
                    candidates.append(exe_candidates[0])
        except Exception:
            pass
        # Optional JP DLL payload (only if present)
        dll_path = repo_root / "miscDepsJp" / "source" / "synthDrivers" / "jtalk" / "libopenjtalk.dll"
        if dll_path.exists():
            candidates.append(dll_path)
        # Perform signing via upstream signExec
        for path in candidates:
            try:
                node = env.File(str(path))
                rc = signExec([node], [node], env)
                if rc != 0:
                    stamp_path.write_text(f"fail:{path}", encoding="utf-8")
                    return rc
            except Exception as e:
                stamp_path.write_text(f"error:{path}:{e}", encoding="utf-8")
                return 1
        stamp_path.write_text("ok", encoding="utf-8")
        return 0

    jp_cert_extras_stamp = env.File("output/_jp_cert_extras.stamp")
    env.AlwaysBuild(jp_cert_extras_stamp)
    env.Command(jp_cert_extras_stamp, [], _cert_extras)
    env.Alias("jpCertExtras", jp_cert_extras_stamp)

    # 4) JP verify signatures (use SIGNTOOL if available to verify installer)
    def _verify_signatures(target: list[Any], source: list[Any], env: Any) -> int:
        import subprocess
        stamp_path = Path(str(target[0]))
        stamp_path.parent.mkdir(parents=True, exist_ok=True)
        repo_root = Path.cwd()
        out_dir = repo_root / "output"
        try:
            exe = None
            if out_dir.exists():
                exe_candidates = sorted(out_dir.glob("nvda_*.exe"), key=lambda p: p.stat().st_mtime, reverse=True)
                if exe_candidates:
                    exe = exe_candidates[0]
            if not exe:
                print("jpVerifySignatures: skip (no installer found under output/)")
                stamp_path.write_text("skip:no-installer", encoding="utf-8")
                return 0
            signtool = os.environ.get("SIGNTOOL", "signtool")
            result = subprocess.run([signtool, "verify", "/pa", "/v", str(exe)], capture_output=True, text=True)
            content = [f"file={exe}", f"rc={result.returncode}"]
            if result.stdout:
                content.append(result.stdout)
            if result.stderr:
                content.append(result.stderr)
            text = "\n".join(content)
            # Keep backward-compatible stamp output
            stamp_path.write_text(text, encoding="utf-8")
            # And also write the historical per-installer verify log: output\\<name>_verify.log
            try:
                verify_log = out_dir / f"{exe.stem}_verify.log"
                verify_log.write_text(text, encoding="utf-8")
            except Exception:
                pass
            if result.returncode == 0:
                print(f"jpVerifySignatures: verified OK: {exe}")
                return 0
            else:
                print(f"jpVerifySignatures: verification FAILED (rc={result.returncode}): {exe}")
                print("  See output/_jp_verify_signatures.stamp or the *_verify.log for details.")
                return result.returncode
        except FileNotFoundError:
            print("jpVerifySignatures: skip (signtool not found). Ensure Windows SDK is installed or SIGNTOOL is set.")
            stamp_path.write_text("skip:no-signtool", encoding="utf-8")
            return 0
        except Exception as e:
            print(f"jpVerifySignatures: error while verifying: {e}")
            stamp_path.write_text(f"error:{e}", encoding="utf-8")
            return 1

    jp_verify_stamp = env.File("output/_jp_verify_signatures.stamp")
    env.AlwaysBuild(jp_verify_stamp)
    env.Command(jp_verify_stamp, [], _verify_signatures)
    env.Alias("jpVerifySignatures", jp_verify_stamp)
