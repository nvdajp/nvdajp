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

# Import shared VS utilities
# Note: We import directly since jptools is not a package
import importlib.util

_vs_utils_path = Path(__file__).parent / "vs_utils.py"
_vs_utils_spec = importlib.util.spec_from_file_location("vs_utils", _vs_utils_path)
if _vs_utils_spec and _vs_utils_spec.loader:
	_vs_utils = importlib.util.module_from_spec(_vs_utils_spec)
	_vs_utils_spec.loader.exec_module(_vs_utils)
	find_vcvarsall = _vs_utils.find_vcvarsall
else:
	# Fallback if import fails
	def find_vcvarsall() -> str | None:
		"""Fallback implementation if vs_utils cannot be imported."""
		editions = ["BuildTools", "Community", "Professional", "Enterprise"]
		base_path = Path(r"C:\Program Files\Microsoft Visual Studio\2022")
		for edition in editions:
			path = base_path / edition / "VC" / "Auxiliary" / "Build" / "vcvarsall.bat"
			if path.exists():
				return str(path)
		return None


def _repo_root(env: Any) -> Path:
	"""Return the NVDA repository root from SCons (``#``).

	Do not use ``Path.cwd()`` in Command actions: builders such as
	``synthDriverHost32Runtime`` use ``chdir=``, and parallel ``-j`` builds can
	leave cwd under ``runtime-builders/`` while ``jtalkPrep`` / ``source`` run.
	"""
	return Path(env.Dir("#").abspath)


def _copy_jtalk_core_files(repo_root: Path) -> int:
	"""Copy JTalk core Python files from miscDepsJp/include/python-jtalk to source/synthDrivers/jtalk.

	This function is now a no-op since files have been moved to source/synthDrivers/jtalk in Phase 1.
	Kept for backward compatibility with existing callers.
	"""
	# Files have been moved to source/synthDrivers/jtalk, so no copying is needed
	return 0


def _run_overlay_and_stamp(target: list[Any], source: list[Any], env: Any) -> int:
	# Overlay is no longer required (Phase 2: miscDepsJp/source is empty).
	# Keep the stamp for compatibility with existing dependencies.
	stamp_path = Path(str(target[0]))
	stamp_path.parent.mkdir(parents=True, exist_ok=True)
	stamp_path.write_text("ok", encoding="utf-8")
	return 0


def _pack_controller_client(target: list[Any], source: list[Any], env: Any) -> int:
	repo_root = _repo_root(env)
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
	repo_root = _repo_root(env)
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
	repo_root = _repo_root(env)
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
	repo_root = _repo_root(env)
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
		# Set PYTHONUTF8=1 to enable UTF-8 mode for console output (handles Unicode characters)
		env_vars = os.environ.copy()
		env_vars.setdefault("PYTHONUTF8", "1")
		res = run([sys.executable, str(test_script)], cwd=str(test_script.parent), env=env_vars)
		if res.returncode != 0:
			return res.returncode
	# Stamp success
	Path(str(target[0])).parent.mkdir(parents=True, exist_ok=True)
	Path(str(target[0])).write_text("ok", encoding="utf-8")
	return 0


def _run_jpchar_tests(target: list[Any], source: list[Any], env: Any) -> int:
	"""Run JP char description tests similarly to jpchar/tests.cmd."""
	repo_root = _repo_root(env)
	script = repo_root / "jpchar" / "checkCharDesc.py"
	from subprocess import run

	if script.exists():
		# Set PYTHONUTF8=1 to enable UTF-8 mode for console output (handles Unicode characters)
		env_vars = os.environ.copy()
		env_vars.setdefault("PYTHONUTF8", "1")
		res = run([sys.executable, str(script)], cwd=str(script.parent), env=env_vars)
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
	if not Path(abspath).is_file():
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
	if not Path(path).is_file():
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
	Currently supports Visual Studio 2022 only.
	Search order: BuildTools, Community, Professional, Enterprise.

	Note: This function delegates to jptools.vs_utils.find_vcvarsall() for shared logic.
	"""
	return find_vcvarsall()


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


def register_jp_builders(env: Any, dist_target: Any | None = None, source_dir: Any | None = None) -> None:
	"""Register JP-specific aliases without affecting upstream targets.

	Args:
		env: SCons environment
		dist_target: Optional dist target node from sconstruct. If provided, jpCertExtras will depend on it
					to ensure correct ordering in parallel builds (--all-cores).
		source_dir: Optional source directory node from sconstruct. If provided, sourceDir will depend on
					jtalkSync with the current TARGET_ARCH to ensure correct architecture-specific builds.
	"""
	# Use BUILD_ARCH (JP-specific) to set TARGET_ARCH (SCons environment variable).
	# BUILD_ARCH is an OS environment variable for JP-specific purposes (mainly smoke test environment switching).
	# TARGET_ARCH is a SCons environment variable and should only be set via SCons, not OS environment.
	# This refactoring ensures TARGET_ARCH follows SCons conventions while BUILD_ARCH handles JP-specific needs.
	build_arch = str(os.environ.get("BUILD_ARCH", "")).lower()
	if build_arch in ("x64", "x86_64"):
		env["TARGET_ARCH"] = "x64"
	elif build_arch == "x86":
		env["TARGET_ARCH"] = "x86"
	else:
		# Fallback to existing SCons TARGET_ARCH (defaults to x64)
		# Note: x86 builds are no longer supported
		env["TARGET_ARCH"] = str(env.get("TARGET_ARCH", "x64")).lower()
	# miscdepsjp alias removed in Phase 2 (miscDepsJp/source is empty, overlay is no-op)

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

		- Resolve TARGET_ARCH (default x64, x86 builds are no longer supported)
		- Locate vendor DLL under miscDepsJp/include/python-jtalk[/x86|x64]/libopenjtalk.dll
		- If missing, attempt to build via nmake (requires MSVC environment)
		- Write payload into source/synthDrivers/jtalk/libopenjtalk.dll (Phase 1: files moved)
		"""
		repo_root = _repo_root(env)
		arch = str(env.get("TARGET_ARCH", "x64")).lower()
		vendor_base = repo_root / "miscDepsJp" / "include" / "python-jtalk"

		if arch in ("x64", "x86_64"):
			src_prebuilt = vendor_base / "x64" / "libopenjtalk.dll"
			nmake_machine = "x64"
		else:
			# x86 DLL is now in x86 subdirectory for consistency with x64
			src_prebuilt = vendor_base / "x86" / "libopenjtalk.dll"
			nmake_machine = (
				"x86"  # Must pass explicitly (all.mak passes MACHINE=$(MACHINE) to lib/Makefile.mak)
			)

		# all.mak builds DLL to vendor_base/libopenjtalk.dll, then we move it to arch-specific subdirectory
		built_dll = vendor_base / "libopenjtalk.dll"

		# Copy directly to source/synthDrivers/jtalk (Phase 1: files moved, no intermediate copy needed)
		dst_payload = repo_root / "source" / "synthDrivers" / "jtalk" / "libopenjtalk.dll"

		print(f"jtalkPrep: using TARGET_ARCH={arch}")
		print(f"jtalkPrep: looking for vendor DLL: {src_prebuilt}")

		# Migrate existing DLL from old location (vendor_base/libopenjtalk.dll) to new location (x86 subdirectory)
		old_dll_location = vendor_base / "libopenjtalk.dll"
		if arch not in ("x64", "x86_64") and old_dll_location.exists() and not src_prebuilt.exists():
			print(f"jtalkPrep: migrating DLL from old location: {old_dll_location} -> {src_prebuilt}")
			try:
				import shutil

				src_prebuilt.parent.mkdir(parents=True, exist_ok=True)
				shutil.move(str(old_dll_location), str(src_prebuilt))
				print("jtalkPrep: DLL migrated successfully")
			except Exception as e:
				print(f"Warning: failed to migrate DLL: {e}")
				print("  Will attempt to build new DLL")

		# If DLL does not exist, attempt to build via nmake
		if not src_prebuilt.exists():
			print("jtalkPrep: DLL not found, attempting to build via nmake...")
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
					# Preserve .gitkeep if it exists (for Git tracking of empty directories)
					gitkeep_path = hts_dst / ".gitkeep"
					gitkeep_exists = gitkeep_path.exists()
					if hts_dst.exists():
						shutil.rmtree(str(hts_dst))
					shutil.copytree(str(hts_src), str(hts_dst))
					# Restore .gitkeep if it was present (for Git tracking of empty directories)
					if gitkeep_exists:
						try:
							gitkeep_path.touch()
						except OSError as e:
							print(f"Warning: Could not restore .gitkeep at {gitkeep_path}: {e}")
				else:
					print(f"Warning: htsengineapi source not found at {hts_src}")

				if lib_src.exists():
					print(f"jtalkPrep: copying libopenjtalk from {lib_src} to {lib_dst}")
					# Preserve .gitkeep if it exists (for Git tracking of empty directories)
					gitkeep_path = lib_dst / ".gitkeep"
					gitkeep_exists = gitkeep_path.exists()
					if lib_dst.exists():
						shutil.rmtree(str(lib_dst))
					shutil.copytree(str(lib_src), str(lib_dst))
					# Restore .gitkeep if it was present (for Git tracking of empty directories)
					if gitkeep_exists:
						try:
							gitkeep_path.touch()
						except OSError as e:
							print(f"Warning: Could not restore .gitkeep at {gitkeep_path}: {e}")
				else:
					print(f"Warning: libopenjtalk source not found at {lib_src}")

				# Check if nmake is available in PATH
				# If not, we'll run nmake via vcvarsall.bat in the same shell
				import subprocess

				vcvarsall: str | None = None
				try:
					run(
						["nmake", "/?"],
						stdout=subprocess.DEVNULL,
						stderr=subprocess.DEVNULL,
						check=True,
					)
					print("jtalkPrep: nmake found in PATH")
					use_vcvarsall = False
				except (FileNotFoundError, subprocess.CalledProcessError):
					print("jtalkPrep: nmake not in PATH, will use vcvarsall.bat")
					vcvarsall = _find_vcvarsall()
					if not vcvarsall:
						print("ERROR: nmake not found and vcvarsall.bat not detected")
						print("  Install Visual Studio with C++ Desktop Development workload")
						print("  Or run from Visual Studio Developer Command Prompt")
						return 1
					print(f"jtalkPrep: found vcvarsall.bat: {vcvarsall}")
					use_vcvarsall = True

				# Clean before building to avoid architecture mismatches
				print(f"jtalkPrep: cleaning build artifacts for arch={nmake_machine}")
				if use_vcvarsall:
					assert vcvarsall is not None  # Type narrowing for type checker
					clean_script = f'call "{vcvarsall}" {nmake_machine} && nmake /f all.mak clean MACHINE={nmake_machine}'
					run(
						clean_script,
						cwd=str(build_dir),
						shell=True,
						capture_output=True,
					)
				else:
					clean_cmd = [
						"nmake",
						"/f",
						"all.mak",
						"clean",
						f"MACHINE={nmake_machine}",
					]
					run(clean_cmd, cwd=str(build_dir), capture_output=True)

				# Build nmake command - if using vcvarsall, wrap it in cmd /c call
				if use_vcvarsall:
					# Run vcvarsall.bat and nmake in the same cmd.exe shell
					# This ensures the environment variables are available to nmake
					assert vcvarsall is not None  # Type narrowing for type checker
					print(f"jtalkPrep: running nmake via vcvarsall.bat with arch={nmake_machine}")
					# Use shell=True to avoid subprocess quote escaping issues
					cmd_script = (
						f'call "{vcvarsall}" {nmake_machine} && nmake /f all.mak MACHINE={nmake_machine}'
					)
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

				# Verify DLL was created by all.mak (it copies to vendor_base/libopenjtalk.dll)
				if not built_dll.exists():
					print(f"ERROR: nmake succeeded but DLL not found at {built_dll}")
					print("  Check nmake output for errors")
					return 1

				# Move built DLL to architecture-specific subdirectory
				src_prebuilt.parent.mkdir(parents=True, exist_ok=True)
				shutil.move(str(built_dll), str(src_prebuilt))
				print(f"jtalkPrep: build succeeded, DLL created at {src_prebuilt}")

			except FileNotFoundError as e:
				print("ERROR: nmake not found in PATH")
				print(f"  {e}")
				print("  Ensure MSVC environment is configured before running SCons:")
				print("    - CI: use ilammy/msvc-dev-cmd action")
				print("    - Local: run vcvarsall.bat or Visual Studio Developer Command Prompt")
				print("    - certBuild2023.cmd: add vcvarsall.bat call before SCons")
				return 1
			except Exception as e:
				print(f"ERROR: failed to build vendor DLL: {e}")
				return 1
		else:
			print("jtalkPrep: using existing DLL (build skipped)")

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

	# Use TARGET_ARCH in stamp filename to ensure rebuild when architecture changes
	# This prevents x86/x64 DLL mismatches when switching architectures
	arch = str(env.get("TARGET_ARCH", "x64")).lower()
	arch_suffix = "x64" if arch in ("x64", "x86_64") else "x86"
	jtalk_prep_stamp = env.File(f"miscDepsJp/_state/prep/jtalkPrep.{arch_suffix}.stamp")
	env.AlwaysBuild(jtalk_prep_stamp)
	env.Command(jtalk_prep_stamp, [], _ensure_jtalk_payload)
	env.Alias("jtalkPrep", jtalk_prep_stamp)

	# Alias: jtalkSync (build/copy jtalk dictionary and DLLs into source/)
	def _sync_jtalk_assets(target: list[Any], source: list[Any], env: Any) -> int:
		repo_root = _repo_root(env)
		vendor_base = repo_root / "miscDepsJp" / "include" / "python-jtalk"
		# Copy directly to source/synthDrivers/jtalk (Phase 1: files moved, no intermediate copy needed)
		jtalk_dir = repo_root / "source" / "synthDrivers" / "jtalk"
		dic_dst = jtalk_dir / "dic"
		builder_script_path = repo_root / "miscDepsJp" / "jptools" / "jtalk" / "make_jdic.py"

		def _dic_state(dic_dir: Path) -> tuple[bool, bool, bool]:
			"""Return (has_sys_dic, has_utf8_version, has_valid_codepage).
			Must have DIC_VERSION with 'nvdajp' (from make_jdic) to ensure custom entries (一人→ヒトリ, etc.).
			"""
			sys_dic_path = dic_dir / "sys.dic"
			if not sys_dic_path.exists():
				return False, False, False

			# Check DIC_VERSION (must be UTF-8 and from make_jdic with nvdajp custom entries)
			has_utf8 = False
			version_file = dic_dir / "DIC_VERSION"
			if not version_file.exists():
				print(f"jtalkSync: DIC_VERSION missing for {dic_dir}; will rebuild via make_jdic.py.")
			else:
				try:
					version_text = version_file.read_text(encoding="utf-8").lower()
					if "nvdajp" not in version_text:
						print(
							f"jtalkSync: dictionary at {dic_dir} not from make_jdic (no 'nvdajp' in DIC_VERSION); rebuilding for custom entries.",
						)
					elif "utf-8" in version_text or "utf8" in version_text:
						has_utf8 = True
					else:
						print(
							f"jtalkSync: dictionary at {dic_dir} not marked UTF-8 (version={version_text.strip()}); rebuilding.",
						)
				except Exception as e:
					print(f"jtalkSync: failed to read DIC_VERSION at {version_file}: {e}")

			# Check DIC_CODEPAGE (must match UTF-8 make_jdic output; not console chcp)
			has_valid_cp = False
			cp_file = dic_dir / "DIC_CODEPAGE"
			if not cp_file.exists():
				print(f"jtalkSync: DIC_CODEPAGE missing for {dic_dir}; will rebuild.")
			else:
				try:
					cp_text = cp_file.read_text(encoding="utf-8").strip().lower()
					if cp_text in ("utf-8", "utf8", "932"):
						has_valid_cp = True
					else:
						print(f"jtalkSync: DIC_CODEPAGE is {cp_text} (expected utf-8); rebuilding.")
				except Exception as e:
					print(f"jtalkSync: failed to read DIC_CODEPAGE at {cp_file}: {e}")

			return True, has_utf8, has_valid_cp

		def _parse_dic_pin(pin_path: Path) -> dict[str, str]:
			pin: dict[str, str] = {}
			for line in pin_path.read_text(encoding="utf-8").splitlines():
				line = line.strip()
				if not line or line.startswith("#") or "=" not in line:
					continue
				key, _, value = line.partition("=")
				pin[key.strip()] = value.strip()
			return pin

		def _sync_prebuilt_dic(repo_root: Path, dic_dst: Path) -> int:
			"""Fetch a pinned, checksum-verified prebuilt dictionary release from
			nishimotz/libkuraji-jtalk-dic instead of building locally.

			See projectDocs/jp/vendor-submodules.md ("辞書のビルド時取得（方針転換）"):
			this is an explicit exception to the "no build-time external fetch"
			principle for the JTalk vendor area. A checksum mismatch fails the
			build; it never falls back to a local build silently.

			Note: the prebuilt dictionary omits bep-eng.dic (GPL, incompatible
			with libkuraji-jtalk-dic's BSD 3-Clause license). This does not
			affect braille output (replace_alphabet_morphs always restores the
			original Latin spelling), only JTalk's spoken pronunciation of some
			English words.
			"""
			import hashlib
			import urllib.request
			import zipfile

			pin_path = repo_root / "miscDepsJp" / "jptools" / "jtalk-dic-version.txt"
			if not pin_path.exists():
				print(f"jtalkSync: jtalkDicSource=prebuilt but pin file not found: {pin_path}")
				return 1
			pin = _parse_dic_pin(pin_path)
			required = {"repo", "tag", "asset", "sha256"}
			if not required.issubset(pin):
				print(f"jtalkSync: pin file {pin_path} missing required keys: {required - set(pin)}")
				return 1

			marker_path = dic_dst / "PREBUILT_SOURCE"
			marker_expected = f"repo={pin['repo']}\ntag={pin['tag']}\nsha256={pin['sha256']}\n"
			if (
				marker_path.exists()
				and marker_path.read_text(encoding="utf-8") == marker_expected
				and (dic_dst / "sys.dic").exists()
			):
				print(f"jtalkSync: prebuilt dictionary already up to date (tag={pin['tag']}); skipping fetch.")
				return 0

			url = f"https://github.com/{pin['repo']}/releases/download/{pin['tag']}/{pin['asset']}"
			print(f"jtalkSync: fetching prebuilt dictionary from {url}")
			zip_path = dic_dst.parent / pin["asset"]
			try:
				urllib.request.urlretrieve(url, str(zip_path))
			except Exception as e:
				print(f"jtalkSync: failed to download prebuilt dictionary: {e}")
				return 1

			digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
			if digest != pin["sha256"]:
				print(
					f"jtalkSync: checksum mismatch for {pin['asset']}: "
					f"expected {pin['sha256']}, got {digest}. Aborting (no local-build fallback).",
				)
				zip_path.unlink(missing_ok=True)
				return 1

			# Clear only the files the base dictionary build produces; leave
			# static license files (COPYING, COPYING-bep-eng.txt) untouched.
			for name in ("sys.dic", "unk.dic", "matrix.bin", "char.bin", "dicrc", "DIC_VERSION"):
				(dic_dst / name).unlink(missing_ok=True)
			with zipfile.ZipFile(zip_path) as zf:
				zf.extractall(dic_dst)
			zip_path.unlink(missing_ok=True)

			try:
				(dic_dst / "DIC_CODEPAGE").write_text("utf-8", encoding="utf-8")
			except Exception as e:
				print(f"jtalkSync: warning: failed to write DIC_CODEPAGE: {e}")
			marker_path.write_text(marker_expected, encoding="utf-8")

			print(f"jtalkSync: prebuilt dictionary installed (tag={pin['tag']}, sha256={digest}).")
			print(
				"jtalkSync: note: the prebuilt dictionary omits bep-eng.dic (GPL); "
				"see projectDocs/jp/vendor-submodules.md.",
			)
			return 0

		def _fetch_prebuilt_tool(repo_root: Path, dest_path: Path) -> int:
			"""Fetch the pinned, checksum-verified mecab-dict-index.exe release
			asset from nishimotz/libkuraji-jtalk-dic, instead of relying on it
			being produced as a side effect of jtalkPrep's unrelated
			libopenjtalk.dll build (unreliable when that build is cache-skipped).

			This binary is unsigned; the checksum is the only integrity check.
			A checksum mismatch fails the build; no local-build fallback.
			"""
			import hashlib
			import urllib.request

			pin_path = repo_root / "miscDepsJp" / "jptools" / "jtalk-dic-version.txt"
			if not pin_path.exists():
				print(f"jtalkSync: pin file not found: {pin_path}")
				return 1
			pin = _parse_dic_pin(pin_path)
			required = {"repo", "tag", "tool_asset", "tool_sha256"}
			if not required.issubset(pin):
				print(f"jtalkSync: pin file {pin_path} missing required keys: {required - set(pin)}")
				return 1

			marker_path = dest_path.parent / "PREBUILT_SOURCE"
			marker_expected = f"repo={pin['repo']}\ntag={pin['tag']}\nsha256={pin['tool_sha256']}\n"
			if (
				marker_path.exists()
				and marker_path.read_text(encoding="utf-8") == marker_expected
				and dest_path.exists()
			):
				print(f"jtalkSync: prebuilt mecab-dict-index.exe already up to date (tag={pin['tag']}).")
				return 0

			url = f"https://github.com/{pin['repo']}/releases/download/{pin['tag']}/{pin['tool_asset']}"
			print(f"jtalkSync: fetching mecab-dict-index.exe from {url}")
			try:
				dest_path.parent.mkdir(parents=True, exist_ok=True)
				urllib.request.urlretrieve(url, str(dest_path))
			except Exception as e:
				print(f"jtalkSync: failed to download mecab-dict-index.exe: {e}")
				return 1

			digest = hashlib.sha256(dest_path.read_bytes()).hexdigest()
			if digest != pin["tool_sha256"]:
				print(
					f"jtalkSync: checksum mismatch for {pin['tool_asset']}: "
					f"expected {pin['tool_sha256']}, got {digest}. Aborting (no local-build fallback).",
				)
				dest_path.unlink(missing_ok=True)
				return 1

			marker_path.write_text(marker_expected, encoding="utf-8")
			print(f"jtalkSync: mecab-dict-index.exe installed (tag={pin['tag']}, sha256={digest}).")
			return 0

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
				run(
					["nmake", "/?"],
					stdout=subprocess.DEVNULL,
					stderr=subprocess.DEVNULL,
					check=True,
				)
				# nmake is available, use it directly
				cmd = ["nmake", "/f", "all.mak", f"MACHINE={machine}"]
				result = run(cmd, cwd=str(vendor_base))
				return result.returncode
			except (FileNotFoundError, subprocess.CalledProcessError):
				vcvarsall = _find_vcvarsall()
				if not vcvarsall:
					print("jtalkSync: nmake not found and vcvarsall.bat not detected")
					return 1
				cmd_script = f'call "{vcvarsall}" {machine} && nmake /f all.mak MACHINE={machine}'
				result = run(cmd_script, cwd=str(vendor_base), shell=True)
				return result.returncode

		dic_source = str(env.get("jtalkDicSource", "local")).lower()
		if dic_source == "prebuilt":
			rc_prebuilt = _sync_prebuilt_dic(repo_root, dic_dst)
			if rc_prebuilt != 0:
				return rc_prebuilt
			sys_dic = dic_dst / "sys.dic"
			should_rebuild_dic = False
		else:
			sys_dic = dic_dst / "sys.dic"
			has_dic, is_utf8_dic, is_valid_cp = _dic_state(dic_dst)
			should_rebuild_dic = not (has_dic and is_utf8_dic and is_valid_cp)
			if should_rebuild_dic:
				print("jtalkSync: dictionary missing or not UTF-8; rebuilding via make_jdic.py.")
				print(f"jtalkSync: repo_root={repo_root!r} builder_script_path.exists()={builder_script_path.exists()!r}")

		def _build_mecab_bin(machine: str) -> int:
			# Makefile.mak is in src subdirectory
			base = vendor_base / "libopenjtalk" / "mecab" / "src"
			makefile = base / "Makefile.mak"
			if not makefile.exists():
				print(f"jtalkSync: Makefile.mak not found for mecab bin build: {makefile}")
				return 1
			import subprocess
			from subprocess import run

			try:
				run(
					["nmake", "/?"],
					stdout=subprocess.DEVNULL,
					stderr=subprocess.DEVNULL,
					check=True,
				)
				# nmake is available, use it directly
				cmd = ["nmake", "/f", "Makefile.mak", f"MACHINE={machine}"]
				result = run(cmd, cwd=str(base))
				return result.returncode
			except (FileNotFoundError, subprocess.CalledProcessError):
				vcvarsall = _find_vcvarsall()
				if not vcvarsall:
					print("jtalkSync: nmake not found and vcvarsall.bat not detected for mecab bin build")
					return 1
				cmd_script = f'call "{vcvarsall}" {machine} && nmake /f Makefile.mak MACHINE={machine}'
				result = run(cmd_script, cwd=str(base), shell=True)
				return result.returncode

		# jptools/build_userdic.py needs mecab-dict-index.exe under
		# jptools/jtalk/libopenjtalk/mecab/src/ to build the user dictionary
		# (jtusr.dic). This is independent of where the base dictionary comes
		# from, so ensure it unconditionally rather than only as a side effect
		# of the local dictionary build below.
		if builder_script_path.exists():
			make_jdic_mecab_bin = (
				builder_script_path.parent / "libopenjtalk" / "mecab" / "src" / "mecab-dict-index.exe"
			)
			if not make_jdic_mecab_bin.exists():
				if dic_source == "prebuilt":
					# Fetch the tool from the same pinned release as the
					# dictionary, rather than depending on jtalkPrep's
					# unrelated libopenjtalk.dll build (which may be
					# cache-skipped and not produce this side artifact).
					rc_tool = _fetch_prebuilt_tool(repo_root, make_jdic_mecab_bin)
					if rc_tool != 0:
						return rc_tool
				else:
					mecab_src_dir = vendor_base / "libopenjtalk" / "mecab" / "src"
					mecab_dict_index_bin = mecab_src_dir / "mecab-dict-index.exe"
					arch_for_tool = str(env.get("TARGET_ARCH", "x64")).lower()
					machine_for_tool = "x64" if arch_for_tool in ("x64", "x86_64") else "x86"
					if not mecab_dict_index_bin.exists():
						rc_tool = _build_mecab_bin(machine_for_tool)
						if rc_tool != 0:
							print(f"jtalkSync: nmake (mecab-dict-index tool) failed with rc={rc_tool}")
							return rc_tool
					if mecab_dict_index_bin.exists():
						try:
							make_jdic_mecab_bin.parent.mkdir(parents=True, exist_ok=True)
							shutil.copy2(mecab_dict_index_bin, make_jdic_mecab_bin)
							print(f"jtalkSync: copied mecab-dict-index.exe to {make_jdic_mecab_bin} (for build_userdic.py)")
						except Exception as e:
							print(f"jtalkSync: failed to copy mecab-dict-index.exe for build_userdic.py: {e}")
					else:
						print(
							f"jtalkSync: warning: mecab-dict-index.exe still missing after build: {mecab_dict_index_bin}; "
							"build_userdic.py's jtusr.dic build will be skipped.",
						)

		# If dictionary is missing or invalid, build it directly into source/synthDrivers/jtalk/dic
		if should_rebuild_dic or not sys_dic.exists():

			def _build_dic(machine: str) -> int:
				base = vendor_base / "libopenjtalk" / "mecab-naist-jdic"
				makefile = base / "Makefile.mak"
				mecab_dict_index_bin = vendor_base / "libopenjtalk" / "mecab" / "src" / "mecab-dict-index.exe"
				import subprocess
				from subprocess import run

				if builder_script_path.exists():
					mecab_src_dir = vendor_base / "libopenjtalk" / "mecab" / "src"
					mecab_dict_index_bin = mecab_src_dir / "mecab-dict-index.exe"
					libmecab_dll = mecab_src_dir / "libmecab.dll"
					rc_bin = _build_mecab_bin(machine)
					if rc_bin != 0:
						print(f"jtalkSync: nmake (mecab) failed with rc={rc_bin}")
						return rc_bin
					if not mecab_dict_index_bin.exists():
						print(
							f"jtalkSync: mecab-dict-index.exe still missing after build: {mecab_dict_index_bin}",
						)
						return 1
					if not libmecab_dll.exists():
						print(f"jtalkSync: libmecab.dll still missing after build: {libmecab_dll}")
						print("jtalkSync: warning: libmecab.dll build may have failed, but continuing...")
					# make_jdic.py expects mecab-dict-index.exe under jptools/jtalk/libopenjtalk/mecab/src
					make_jdic_mecab_bin = (
						builder_script_path.parent / "libopenjtalk" / "mecab" / "src" / "mecab-dict-index.exe"
					)
					try:
						make_jdic_mecab_bin.parent.mkdir(parents=True, exist_ok=True)
						shutil.copy2(mecab_dict_index_bin, make_jdic_mecab_bin)
						print(f"jtalkSync: copied mecab-dict-index.exe to {make_jdic_mecab_bin}")
					except Exception as e:
						print(f"jtalkSync: failed to copy mecab-dict-index.exe to make_jdic path: {e}")
						return 1
					python_exe = sys.executable or "python"
					env_vars = os.environ.copy()
					env_vars.setdefault("PYTHONUTF8", "1")
					print("jtalkSync: building dictionary with make_jdic.py (UTF-8).")
					result = run(
						[python_exe, str(builder_script_path)],
						cwd=str(builder_script_path.parent),
						env=env_vars,
					)
					return result.returncode

				if not makefile.exists():
					print(f"jtalkSync: Makefile.mak not found for dictionary build: {makefile}")
					return 1

				# Ensure dicrc sets config-charset=utf-8 for .def files
				dicrc = base / "dicrc"
				desired_dicrc_line = "config-charset = utf-8\n"
				need_update_dicrc = True
				if dicrc.exists():
					try:
						dicrc_text = dicrc.read_text(encoding="utf-8").lower()
						if "config-charset = utf-8" in dicrc_text:
							need_update_dicrc = False
					except Exception:
						pass
				if need_update_dicrc:
					# Keep minimal content for deterministic behavior in CI/local.
					dicrc.write_text(desired_dicrc_line, encoding="utf-8")
					print("jtalkSync: wrote dicrc with config-charset = utf-8")

				try:
					run(
						["nmake", "/?"],
						stdout=subprocess.DEVNULL,
						stderr=subprocess.DEVNULL,
						check=True,
					)
					# nmake is available, use it directly.
					result = run(["nmake", "/f", "Makefile.mak", f"MACHINE={machine}"], cwd=str(base))
					return result.returncode
				except (FileNotFoundError, subprocess.CalledProcessError):
					vcvarsall = _find_vcvarsall()
					if not vcvarsall:
						print("jtalkSync: nmake not found and vcvarsall.bat not detected for dic build")
						return 1
					cmd_script = (
						f'cmd /c "'
						f'call "{vcvarsall}" {machine} && '
						f"nmake /f Makefile.mak MACHINE={machine}"
						f'"'
					)
					print("jtalkSync: building dictionary via vcvarsall")
					result = run(cmd_script, cwd=str(base), shell=True)
					return result.returncode
				# This code path should not be reached, but kept for safety
				cmd = ["nmake", "/f", "Makefile.mak", f"MACHINE={machine}"]
				print("jtalkSync: building dictionary")
				result = run(cmd, cwd=str(base))
				return result.returncode

			arch = str(env.get("TARGET_ARCH", "x64")).lower()
			machine = "x64" if arch in ("x64", "x86_64") else "x86"

			print(
				"jtalkSync: sys.dic missing or out of date; building python-jtalk (nmake all) and mecab dic",
			)
			rc = _run_nmake(machine)
			if rc != 0:
				print(f"jtalkSync: nmake (all.mak) failed with rc={rc}")
				return rc

			# Build mecab binary (mecab-dict-index.exe) and libmecab.dll if missing
			mecab_src_dir = vendor_base / "libopenjtalk" / "mecab" / "src"
			mecab_dict_index_bin = mecab_src_dir / "mecab-dict-index.exe"
			libmecab_dll = mecab_src_dir / "libmecab.dll"
			rc_bin = _build_mecab_bin(machine)
			if rc_bin != 0:
				print(f"jtalkSync: nmake (mecab) failed with rc={rc_bin}")
				return rc_bin
			if not mecab_dict_index_bin.exists():
				print(f"jtalkSync: mecab-dict-index.exe still missing after build: {mecab_dict_index_bin}")
				return 1
			if not libmecab_dll.exists():
				print(f"jtalkSync: libmecab.dll still missing after build: {libmecab_dll}")
				print("jtalkSync: warning: libmecab.dll build may have failed, but continuing...")

			# After all.mak and mecab bin, try explicit dic build if still missing or needs rebuild
			rc_dic = _build_dic(machine)
			if rc_dic != 0:
				print(f"jtalkSync: nmake/make_jdic (mecab-naist-jdic) failed with rc={rc_dic}")
				return rc_dic

			# Write DIC_CODEPAGE marker (UTF-8 dictionary from make_jdic.py; not console code page)
			try:
				(dic_dst / "DIC_CODEPAGE").write_text("utf-8", encoding="utf-8")
			except Exception as e:
				print(f"jtalkSync: warning: failed to write DIC_CODEPAGE: {e}")

			sys_dic = dic_dst / "sys.dic"

		if not sys_dic.exists():
			print("jtalkSync: sys.dic still missing after build; no fallback available")
			return 1
		print(f"jtalkSync: dictionary ready at {dic_dst} (no copy needed).")

		# Copy core assets (DLLs only; Python files have been moved to source/synthDrivers/jtalk in Phase 1)
		try:
			# Copy libmecab.dll (built from source or fallback to existing)
			arch = str(env.get("TARGET_ARCH", "x64")).lower()
			machine = "x64" if arch in ("x64", "x86_64") else "x86"
			# First, try to find built libmecab.dll from mecab/src directory
			built_libmecab = vendor_base / "libopenjtalk" / "mecab" / "src" / "libmecab.dll"
			if not built_libmecab.exists():
				# Build libmecab.dll if it doesn't exist
				print("jtalkSync: libmecab.dll not found, building...")
				rc_bin = _build_mecab_bin(machine)
				if rc_bin != 0:
					print(f"jtalkSync: nmake (mecab) failed with rc={rc_bin}")
					# Continue anyway, will try fallback
				elif not built_libmecab.exists():
					print(f"jtalkSync: libmecab.dll still missing after build: {built_libmecab}")
			if built_libmecab.exists():
				shutil.copy2(built_libmecab, jtalk_dir / "libmecab.dll")
				print(f"jtalkSync: copied built libmecab.dll from {built_libmecab}")
			else:
				# Fallback to existing libmecab.dll (if present, e.g., from PyPI wheel)
				fallback_libmecab = vendor_base / "libmecab.dll"
				if fallback_libmecab.exists():
					shutil.copy2(fallback_libmecab, jtalk_dir / "libmecab.dll")
					print(f"jtalkSync: copied fallback libmecab.dll from {fallback_libmecab}")
				else:
					print(
						f"jtalkSync: warning: libmecab.dll not found (expected at {built_libmecab} or {fallback_libmecab})",
					)
			# Copy arch-specific libopenjtalk.dll (x86 or x64)
			if arch in ("x64", "x86_64"):
				src_dll = vendor_base / "x64" / "libopenjtalk.dll"
			else:
				src_dll = vendor_base / "x86" / "libopenjtalk.dll"
			if src_dll.exists():
				shutil.copy2(src_dll, jtalk_dir / "libopenjtalk.dll")
			print(f"jtalkSync: copied core assets to {jtalk_dir}")
		except Exception as e:
			print(f"jtalkSync: failed to copy core assets: {e}")
			return 1

		stamp_path = Path(str(target[0]))
		stamp_path.parent.mkdir(parents=True, exist_ok=True)
		stamp_path.write_text("ok", encoding="utf-8")
		return 0

	# Use TARGET_ARCH in stamp filename to ensure rebuild when architecture changes
	# This prevents x86/x64 DLL mismatches when switching architectures
	# Note: arch_suffix is already defined above for jtalkPrep
	jtalk_sync_stamp = env.File(f"miscDepsJp/_state/prep/jtalkSync.{arch_suffix}.stamp")
	# AlwaysBuild: CI cache/stamp caused stale dictionary (一人→1ニン). Always rebuild for correctness.
	# jtalkSync depends on jtalkPrep to avoid file lock conflicts when both try to build hts.mak
	# Note: jtalkSync output files (sys.dic, libmecab.dll, libopenjtalk.dll) are not added here as
	# explicit dependencies. jtalkSync first produces these files under miscDepsJp and then copies
	# them into the source tree. The top-level 'source' target already depends on jtalkSync
	# via env.Depends(source_dir, jtalk_sync_stamp) below, so adding the individual output files
	# as dependencies on this stamp target would be redundant rather than preventing a circular dependency.
	env.AlwaysBuild(jtalk_sync_stamp)
	env.Command(jtalk_sync_stamp, [jtalk_prep_stamp], _sync_jtalk_assets)
	env.Alias("jtalkSync", jtalk_sync_stamp)

	# Set up sourceDir dependency on jtalkSync with current TARGET_ARCH
	# This ensures that when TARGET_ARCH changes (x86 -> x64 -> x86), the correct
	# architecture-specific stamp file is used, triggering rebuilds as needed.
	if source_dir is not None:
		env.Depends(source_dir, jtalk_sync_stamp)

	# Register files generated by jtalkSync for cleanup (scons -c)
	repo_root_clean = _repo_root(env)
	vendor_base = repo_root_clean / "miscDepsJp" / "include" / "python-jtalk"
	mecab_src_dir = vendor_base / "libopenjtalk" / "mecab" / "src"
	jtalk_dir = repo_root_clean / "source" / "synthDrivers" / "jtalk"
	dic_dir = jtalk_dir / "dic"

	# Clean up all .obj, .lib, and .exe files in mecab/src directory using glob
	# This ensures that stale object files from previous builds (x86/x64) are removed
	import glob

	for pattern in ["*.obj", "*.lib", "*.exe"]:
		for file_path in glob.glob(str(mecab_src_dir / pattern)):
			env.Clean(jtalk_sync_stamp, file_path)

	# Clean dictionary outputs so `scons -c jtalkSync` forces a rebuild on next run.
	# Preserve license/docs files that should remain in the tree.
	keep_dic_files = {"COPYING", "COPYING-bep-eng.txt", "dicrc"}
	if dic_dir.exists():
		for file_path in dic_dir.glob("*"):
			if file_path.is_file() and file_path.name not in keep_dic_files:
				env.Clean(jtalk_sync_stamp, str(file_path))

	# mecab-dict-index.exe (built by jtalkSync) - already covered by glob above, but keep for clarity
	mecab_dict_index = str(mecab_src_dir / "mecab-dict-index.exe")
	env.Clean(jtalk_sync_stamp, mecab_dict_index)
	# libmecab.dll (built by jtalkSync, then copied to source/synthDrivers/jtalk)
	built_libmecab_dll = str(mecab_src_dir / "libmecab.dll")
	env.Clean(jtalk_sync_stamp, built_libmecab_dll)
	libmecab_dll = str(jtalk_dir / "libmecab.dll")
	env.Clean(jtalk_sync_stamp, libmecab_dll)
	# libopenjtalk.dll (copied to source/synthDrivers/jtalk by jtalkSync)
	libopenjtalk_dll = str(jtalk_dir / "libopenjtalk.dll")
	env.Clean(jtalk_sync_stamp, libopenjtalk_dll)
	# mecab.lib (built by jtalkSync) - already covered by glob above, but keep for clarity
	mecab_lib = str(mecab_src_dir / "mecab.lib")
	env.Clean(jtalk_sync_stamp, mecab_lib)

	# Clean up both x64 and x86 stamp files to ensure architecture switching works correctly
	# This prevents stale stamp files from preventing rebuilds when switching architectures
	prep_state_dir = repo_root_clean / "miscDepsJp" / "_state" / "prep"
	for arch_suffix_clean in ["x64", "x86"]:
		jtalk_prep_stamp_clean = str(prep_state_dir / f"jtalkPrep.{arch_suffix_clean}.stamp")
		jtalk_sync_stamp_clean = str(prep_state_dir / f"jtalkSync.{arch_suffix_clean}.stamp")
		env.Clean(jtalk_sync_stamp, jtalk_prep_stamp_clean)
		env.Clean(jtalk_sync_stamp, jtalk_sync_stamp_clean)

	# Note: Dependencies are already established in sconstruct:
	#   - sourceDir -> jtalkSync (L401)
	#   - pot -> jtalkSync (L724)
	#   - dist -> sourceDir (L567, dist depends on sourceDir in NVDADist)
	# This creates the dependency chain: dist -> sourceDir -> jtalkSync -> jtalkPrep
	# No additional wiring needed here; using Dir/target objects (not Alias) is more robust.

	# Alias: controllerClient (zip artifact)
	out_dir = str(env.get("outputDir", "output"))
	version = str(env.get("version", "local"))
	cc_zip = env.File(str(Path(out_dir) / f"nvda_{version}_controllerClientJp.zip"))
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
	# 1) Stage controller client artifacts (copy from extras/controllerClient to jptools/nvdajpClient)
	def _stage_controller_client(target: list[Any], source: list[Any], env: Any) -> int:
		repo_root = _repo_root(env)
		client_root = repo_root / "jptools" / "nvdajpClient"
		extras_client_dir = repo_root / "extras" / "controllerClient"
		try:
			client_root.mkdir(parents=True, exist_ok=True)
			# Copy files from extras/controllerClient to jptools/nvdajpClient
			# This mirrors the behavior of buildControllerClient.cmd
			for arch in ["x86", "x64", "arm64"]:
				src_arch_dir = extras_client_dir / arch
				dst_arch_dir = client_root / arch
				if src_arch_dir.exists():
					dst_arch_dir.mkdir(parents=True, exist_ok=True)
					# Copy DLL, header, lib, exp files
					for pattern in ["*.dll", "*.h", "*.lib", "*.exp", "*.pdb"]:
						for src_file in src_arch_dir.glob(pattern):
							dst_file = dst_arch_dir / src_file.name
							shutil.copy2(src_file, dst_file)
							print(f"jpStageControllerClient: copied {src_file.name} to {dst_arch_dir}")
			# Copy documentation files if they exist
			for doc_file in ["license.txt", "readme.html", "readmejp.txt"]:
				src_doc = extras_client_dir / doc_file
				if src_doc.exists():
					dst_doc = client_root / doc_file
					shutil.copy2(src_doc, dst_doc)
					print(f"jpStageControllerClient: copied {doc_file}")
			# Copy examples directory if it exists
			# Note: preserve existing files (e.g., JP-specific test_*.py) and only copy/update files from extras/controllerClient/examples
			src_examples = extras_client_dir / "examples"
			if src_examples.exists():
				dst_examples = client_root / "examples"
				dst_examples.mkdir(parents=True, exist_ok=True)
				# Copy files and subdirectories from src_examples, preserving existing files
				for item in src_examples.iterdir():
					src_item = item
					dst_item = dst_examples / item.name
					if src_item.is_dir():
						if dst_item.exists():
							shutil.rmtree(dst_item)
						shutil.copytree(src_item, dst_item)
						print(f"jpStageControllerClient: copied examples/{item.name}/")
					else:
						shutil.copy2(src_item, dst_item)
						print(f"jpStageControllerClient: copied examples/{item.name}")
				print("jpStageControllerClient: updated examples directory")
		except Exception as e:
			print(f"jpStageControllerClient: error: {e}")
			return 1
		stamp_path = Path(str(target[0]))
		stamp_path.parent.mkdir(parents=True, exist_ok=True)
		stamp_path.write_text("ok", encoding="utf-8")
		return 0

	jp_stage_stamp = env.File("jptools/_state/jp_stage_controller_client.stamp")
	# Depend on extras/controllerClient files to ensure they are built before copying
	# This makes the copy step run only when source files change
	extras_client_dir = _repo_root(env) / "extras" / "controllerClient"
	source_files = []
	for arch in ["x86", "x64", "arm64"]:
		# Add DLL as dependency (main artifact)
		dll_path = extras_client_dir / arch / "nvdaControllerClient.dll"
		if (
			dll_path.exists() or not source_files
		):  # Include at least one file per arch for dependency tracking
			source_files.append(env.File(str(dll_path)))
	# If no files exist yet, use empty list (will be created on first run)
	if not source_files:
		env.AlwaysBuild(jp_stage_stamp)
	env.Command(jp_stage_stamp, source_files, _stage_controller_client)
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
		repo_root = _repo_root(env)
		candidates: list[Path] = []
		# Note: We intentionally do not sign output/nvda_*.exe here.
		# The installer is signed as part of the launcher target via AddPostAction(env["signExec"]).
		# Required JP DLL payload in dist/ (must be signed before launcher is built)
		# NOTE: We sign files in dist/, not source/, because:
		# 1. jtalkSync copies DLLs to source/synthDrivers/jtalk/
		# 2. dist build copies files from source/ to dist/ (unsigned)
		# 3. jpCertExtras signs files in dist/ (this step)
		# 4. launcher builds installer from dist/ (includes signed DLLs)
		dist_dir = repo_root / "dist"
		required_dlls = ["libopenjtalk.dll", "libmecab.dll"]
		missing_required = []
		if not dist_dir.exists():
			print("jpCertExtras: ERROR - dist/ directory does not exist")
			print("jpCertExtras: dist/ must be built before jpCertExtras can sign DLLs")
			print("jpCertExtras: Build order: jtalkSync -> dist -> jpCertExtras -> launcher")
			stamp_path.write_text("error:dist-not-built", encoding="utf-8")
			return 1
		dist_jtalk_dir = dist_dir / "synthDrivers" / "jtalk"
		for dll_name in required_dlls:
			dll_path = dist_jtalk_dir / dll_name
			if dll_path.exists():
				candidates.append(dll_path)
			else:
				missing_required.append(dll_path)

		# Sign critical EXEs in dist/ (certificate store builds).
		# These were previously signed as part of NVDADistGenerator, but that introduces implicit
		# dependencies on dist/*.exe which are side effects, not SCons targets, and can fail under -j2.
		for exe_name in [
			"nvda_noUIAccess.exe",
			"nvda_uiAccess.exe",
			"nvda_slave.exe",
			"l10nUtil.exe",
			"uninstall.exe",
		]:
			exe_path = dist_dir / exe_name
			if exe_path.exists():
				candidates.append(exe_path)
		# Sign files in dist/lib/<version>/ (nvdaHelper*.dll, etc.)
		# These files are copied from source/ to dist/ during dist build, but may lose signatures
		# during the copy process. We sign them here to ensure they are signed before launcher build.
		build_version = str(env.get("version", ""))
		if build_version:
			lib_version_dir = dist_dir / "lib" / build_version
			if lib_version_dir.exists():
				for pattern in ("**/*.dll", "**/*.exe"):
					for path in lib_version_dir.glob(pattern):
						if path.is_file():
							candidates.append(path)
		# Note: nvdaHelper*.dll files (IAccessible2proxy.dll, ISimpleDOM.dll, nvdaHelperRemote.dll,
		# nvdaHelperRemoteLoader.exe, UIARemote.dll, nvdaHelperLocal.dll, nvdaHelperLocalWin10.dll)
		# are signed during source build (see nvdaHelper/archBuild_sconscript), but may lose signatures
		# when copied to dist/ during dist build. We sign them here in jpCertExtras to ensure
		# they are signed before launcher build.
		# Report missing required DLLs (must be in dist/, not source/)
		if missing_required:
			print("jpCertExtras: ERROR - Required DLLs not found in dist/:")
			for dll_path in missing_required:
				print(f"  {dll_path}")
			print("jpCertExtras: These files must be present in dist/ before signing.")
			print(
				"jpCertExtras: Build order: jtalkSync (copies to source/) -> dist (copies to dist/) -> jpCertExtras (signs dist/)",
			)
			stamp_path.write_text(
				f"error:missing-dlls:{','.join(str(p.name) for p in missing_required)}",
				encoding="utf-8",
			)
			return 1
		# Perform signing via upstream signExec
		signed_count = 0
		for path in candidates:
			try:
				print(f"jpCertExtras: signing {path}")
				node = env.File(str(path))
				rc = signExec([node], [node], env)
				if rc != 0:
					print(f"jpCertExtras: ERROR - signing failed for {path} (rc={rc})")
					stamp_path.write_text(f"fail:{path}", encoding="utf-8")
					return rc
				signed_count += 1
				print(f"jpCertExtras: successfully signed {path}")
			except Exception as e:
				print(f"jpCertExtras: ERROR - exception while signing {path}: {e}")
				stamp_path.write_text(f"error:{path}:{e}", encoding="utf-8")
				return 1
		if signed_count > 0:
			print(f"jpCertExtras: signed {signed_count} file(s)")
		else:
			print("jpCertExtras: no files to sign")
		stamp_path.write_text("ok", encoding="utf-8")
		return 0

	jp_cert_extras_stamp = env.File("output/_jp_cert_extras.stamp")
	env.AlwaysBuild(jp_cert_extras_stamp)
	# Order after dist without using dist as a Command source.
	# Using dist as source inherits NVDADist signExec File nodes (e.g. dist/l10nUtil.exe)
	# as implicit dependencies; those are side effects, not SCons targets, and fail under -j2.
	env.Command(jp_cert_extras_stamp, [], _cert_extras)
	if dist_target is not None:
		env.Depends(jp_cert_extras_stamp, dist_target)
	else:
		env.Depends(jp_cert_extras_stamp, env.Dir("dist"))
	env.Alias("jpCertExtras", jp_cert_extras_stamp)

	# launcher depends on jpCertExtras; wired in sconstruct after launcher is defined
	# (register_jp_builders runs before launcher exists, so Depends cannot be set here).

	# Clean up old version directories in dist/lib/, dist/lib64/, dist/libArm64/
	# to prevent signature verification failures from old unsigned files.
	# These directories are created by py2exe with version-specific names (e.g., dist/lib/{version}/),
	# and old versions may remain after repeated builds if not explicitly cleaned.
	try:
		current_version = str(env.get("version", ""))
		if current_version and dist_target is not None:
			repo_root = _repo_root(env)
			dist_dir = repo_root / "dist"
			old_version_dirs = []
			for lib_subdir in ["lib", "lib64", "libArm64"]:
				lib_dir = dist_dir / lib_subdir
				if lib_dir.exists():
					for version_dir in lib_dir.iterdir():
						if version_dir.is_dir() and version_dir.name != current_version:
							# This is an old version directory that should be cleaned
							old_version_dirs.append(str(version_dir))
			if old_version_dirs:
				# Add old version directories to clean targets
				# This ensures scons -c removes old version directories that may contain unsigned files
				# Use dist_target (same pattern as sconstruct L775: env.Clean(dist, _overlay_files))
				env.Clean(dist_target, old_version_dirs)
	except Exception:
		# If version is not available, dist_target is None, or cleanup setup fails, that's okay
		# (env.Clean(dist, dist) in sconstruct L570 should still clean the entire dist directory)
		pass

	# 4) JP verify signatures (use SIGNTOOL if available to verify installer and dist files)
	# Default is a fast check of critical artifacts; for a full scan use jpVerifySignaturesAll.
	def _verify_signatures(target: list[Any], source: list[Any], env: Any) -> int:
		import subprocess

		stamp_path = Path(str(target[0]))
		stamp_path.parent.mkdir(parents=True, exist_ok=True)
		repo_root = _repo_root(env)
		out_dir = repo_root / "output"
		dist_dir = repo_root / "dist"

		mode = str(
			env.get(
				"JP_VERIFY_SIGNATURES_MODE",
				os.environ.get("JP_VERIFY_SIGNATURES_MODE", "fast"),
			),
		).lower()
		verbose = str(
			env.get(
				"JP_VERIFY_SIGNATURES_VERBOSE",
				os.environ.get("JP_VERIFY_SIGNATURES_VERBOSE", "0"),
			),
		).lower() in (
			"1",
			"true",
			"yes",
			"on",
		)
		ignored_files = {
			"msgfmt.exe",
			"lilli.dll",
			"brlapi-0.8.dll",
			"libgcc_s_dw2-1.dll",
			"wxbase32u_net_vc140.dll",
			"wxbase32u_vc140.dll",
			"wxmsw32u_aui_vc140.dll",
			"wxmsw32u_core_vc140.dll",
			"wxmsw32u_html_vc140.dll",
			"wxmsw32u_stc_vc140.dll",
		}

		def _signtool_verify(
			signtool_path: str,
			file_path: Path,
			*,
			quiet: bool,
		) -> subprocess.CompletedProcess[str]:
			args = [signtool_path, "verify", "/pa"]
			args.append("/q" if quiet else "/v")
			return subprocess.run(args + [str(file_path)], capture_output=True, text=True)

		def _format_signtool_output(result: subprocess.CompletedProcess[str]) -> str:
			out = (result.stdout or "").strip()
			err = (result.stderr or "").strip()
			if out and err:
				return f"{out}\n{err}"
			return out or err or ""

		def _verify_one(
			signtool_path: str,
			file_path: Path,
			*,
			allow_ignored: bool,
		) -> tuple[bool, bool, str]:
			result = _signtool_verify(signtool_path, file_path, quiet=True)
			if result.returncode == 0:
				return True, False, ""
			file_name = file_path.name
			is_ignored = allow_ignored and (file_name in ignored_files)
			detail = ""
			if verbose or not is_ignored:
				detail_result = _signtool_verify(signtool_path, file_path, quiet=False)
				detail = _format_signtool_output(detail_result)
			return False, is_ignored, detail

		try:
			exe: Path | None = None
			if out_dir.exists():
				exe_candidates = sorted(
					out_dir.glob("nvda_*.exe"),
					key=lambda p: p.stat().st_mtime,
					reverse=True,
				)
				if exe_candidates:
					exe = exe_candidates[0]
			if not exe:
				print("jpVerifySignatures: skip (no installer found under output/)")
				stamp_path.write_text("skip:no-installer", encoding="utf-8")
				return 0

			signtool = os.environ.get("SIGNTOOL", "signtool")

			if mode not in ("fast", "all"):
				print(f"jpVerifySignatures: unknown mode {mode!r}, falling back to 'fast'")
				mode = "fast"

			failures: list[str] = []
			ignored_failures: list[str] = []
			checked = 0
			verified = 0

			def _check(path: Path, *, allow_ignored: bool) -> None:
				nonlocal checked, verified
				checked += 1
				if not path.exists():
					failures.append(f"missing:{path}")
					return
				ok, is_ignored, detail = _verify_one(signtool, path, allow_ignored=allow_ignored)
				if ok:
					verified += 1
					return
				if is_ignored:
					ignored_failures.append(str(path))
					if detail and verbose:
						ignored_failures.append(detail)
					return
				failures.append(str(path))
				if detail:
					failures.append(detail)

			if mode == "fast":
				build_version = str(env.get("version", ""))
				critical_paths: list[Path] = [
					exe,
					dist_dir / "synthDrivers" / "jtalk" / "libopenjtalk.dll",
					dist_dir / "synthDrivers" / "jtalk" / "libmecab.dll",
					dist_dir / "nvda_noUIAccess.exe",
					dist_dir / "nvda_uiAccess.exe",
					dist_dir / "nvda_slave.exe",
					dist_dir / "l10nUtil.exe",
					dist_dir / "uninstall.exe",
				]
				if build_version:
					# Checking dist/lib/<version> recursively for any DLLs/EXEs (handles x86/x64/arm64 subdirs automatically)
					lib_version_dir = dist_dir / "lib" / build_version
					if lib_version_dir.exists():
						for pattern in ("**/*.dll", "**/*.exe"):
							for path in lib_version_dir.glob(pattern):
								if path.is_file():
									critical_paths.append(path)
				for path in critical_paths:
					_check(path, allow_ignored=False)
			else:
				_check(exe, allow_ignored=False)
				if dist_dir.exists():
					dist_files: list[Path] = []
					for pattern in ("**/*.exe", "**/*.dll"):
						dist_files.extend(dist_dir.glob(pattern))
					dist_files = [p for p in dist_files if p.is_file()]
					dist_files.sort(key=str)
					for dist_file in dist_files:
						_check(dist_file, allow_ignored=True)
				else:
					failures.append("missing:dist/")

			summary_lines = [
				f"mode={mode}",
				f"installer={exe}",
				f"checked={checked}",
				f"verified={verified}",
				f"ignored={len(ignored_failures)}",
			]
			if failures:
				summary_lines.append("FAILED")
			else:
				summary_lines.append("OK")

			details_lines: list[str] = []
			if failures:
				details_lines.append("Failures:")
				details_lines.extend(f"  {line}" for line in failures)
			if ignored_failures and verbose:
				details_lines.append("Ignored failures (verbose):")
				details_lines.extend(f"  {line}" for line in ignored_failures)

			text = "\n".join(summary_lines + details_lines) + "\n"
			stamp_path.write_text(text, encoding="utf-8")
			try:
				verify_log = out_dir / f"{exe.stem}_verify_log.txt"
				verify_log.write_text(text, encoding="utf-8")
			except Exception:
				pass

			if failures:
				print(f"jpVerifySignatures: FAILED ({mode})")
				print("  See output/_jp_verify_signatures*.stamp or the *_verify_log.txt for details.")
				return 1
			if ignored_failures and not verbose:
				print(f"jpVerifySignatures: OK ({mode}) with {len(ignored_failures)} ignored failure(s)")
			else:
				print(f"jpVerifySignatures: OK ({mode})")
			return 0
		except FileNotFoundError:
			print(
				"jpVerifySignatures: skip (signtool not found). Ensure Windows SDK is installed or SIGNTOOL is set.",
			)
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

	verify_all_env = env.Clone(JP_VERIFY_SIGNATURES_MODE="all")
	jp_verify_all_stamp = verify_all_env.File("output/_jp_verify_signatures_all.stamp")
	verify_all_env.AlwaysBuild(jp_verify_all_stamp)
	verify_all_env.Command(jp_verify_all_stamp, [], _verify_signatures)
	env.Alias("jpVerifySignaturesAll", jp_verify_all_stamp)

	return jp_cert_extras_stamp


def register_jp_launcher_deps(env: Any, launcher: Any, jp_cert_extras_stamp: Any) -> None:
	"""Ensure launcher waits for jpCertExtras when signing is enabled.

	Must be called from sconstruct after the launcher target is created.
	"""
	try:
		signExec = env.get("signExec")
		certFile = env.get("certFile")
		apiSigningToken = env.get("apiSigningToken")
		if signExec or certFile or apiSigningToken:
			env.Depends(launcher, jp_cert_extras_stamp)
	except Exception:
		pass
