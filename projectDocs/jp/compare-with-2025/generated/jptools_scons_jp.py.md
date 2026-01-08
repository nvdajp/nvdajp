# Diff for: `jptools\scons_jp.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\jptools\scons_jp.py`  
**Current**: `F:\nvda\gh\alphajp-260109\jptools\scons_jp.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\scons_jp.py" "b/F:\\nvda\\gh\\alphajp-260109\\jptools\\scons_jp.py"
index e85826e..2360488 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\scons_jp.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\jptools\\scons_jp.py"
@@ -20,6 +20,7 @@
 These are intentionally light-weight and safe; wiring them into other
 targets can be done in later phases when stable.
 """
+
 from __future__ import annotations
 
 import os
@@ -28,6 +29,28 @@
 import shutil
 from typing import Any
 
+# Import shared VS utilities
+# Note: We import directly since jptools is not a package
+import importlib.util
+
+_vs_utils_path = Path(__file__).parent / "vs_utils.py"
+_vs_utils_spec = importlib.util.spec_from_file_location("vs_utils", _vs_utils_path)
+if _vs_utils_spec and _vs_utils_spec.loader:
+	_vs_utils = importlib.util.module_from_spec(_vs_utils_spec)
+	_vs_utils_spec.loader.exec_module(_vs_utils)
+	find_vcvarsall = _vs_utils.find_vcvarsall
+else:
+	# Fallback if import fails
+	def find_vcvarsall() -> str | None:
+		"""Fallback implementation if vs_utils cannot be imported."""
+		editions = ["BuildTools", "Community", "Professional", "Enterprise"]
+		base_path = Path(r"C:\Program Files\Microsoft Visual Studio\2022")
+		for edition in editions:
+			path = base_path / edition / "VC" / "Auxiliary" / "Build" / "vcvarsall.bat"
+			if path.exists():
+				return str(path)
+		return None
+
 
 def _copy_jtalk_core_files(repo_root: Path) -> int:
 	"""Copy JTalk core Python files from miscDepsJp/include/python-jtalk to source/synthDrivers/jtalk.
@@ -73,13 +96,13 @@ def _pack_controller_client(target: list[Any], source: list[Any], env: Any) -> i
 	return res.returncode
 
 
-
 def _pack_jtalk_addon(target: list[Any], source: list[Any], env: Any) -> int:
 	repo_root = Path.cwd()
 	script = repo_root / "jptools" / "pack_jtalk_addon.py"
 	if not script.exists():
 		return 0
 	from subprocess import run
+
 	# Ensure VERSION is available for the packer (used for current date default)
 	version = str(env.get("version", ""))
 	run_env = os.environ.copy()
@@ -101,6 +124,7 @@ def _pack_kgs_addon(target: list[Any], source: list[Any], env: Any) -> int:
 	if not script.exists():
 		return 0
 	from subprocess import run
+
 	version = str(env.get("version", ""))
 	cmd = [sys.executable, str(script)]
 	if version:
@@ -132,7 +156,10 @@ def _run_jp_tests(target: list[Any], source: list[Any], env: Any) -> int:
 	# Run jpDicTest.py from jptools directory
 	test_script = repo_root / "jptools" / "jpDicTest.py"
 	if test_script.exists():
-        res = run([sys.executable, str(test_script)], cwd=str(test_script.parent))
+		# Set PYTHONUTF8=1 to enable UTF-8 mode for console output (handles Unicode characters)
+		env_vars = os.environ.copy()
+		env_vars.setdefault("PYTHONUTF8", "1")
+		res = run([sys.executable, str(test_script)], cwd=str(test_script.parent), env=env_vars)
 		if res.returncode != 0:
 			return res.returncode
 	# Stamp success
@@ -146,8 +173,12 @@ def _run_jpchar_tests(target: list[Any], source: list[Any], env: Any) -> int:
 	repo_root = Path.cwd()
 	script = repo_root / "jpchar" / "checkCharDesc.py"
 	from subprocess import run
+
 	if script.exists():
-        res = run([sys.executable, str(script)], cwd=str(script.parent))
+		# Set PYTHONUTF8=1 to enable UTF-8 mode for console output (handles Unicode characters)
+		env_vars = os.environ.copy()
+		env_vars.setdefault("PYTHONUTF8", "1")
+		res = run([sys.executable, str(script)], cwd=str(script.parent), env=env_vars)
 		if res.returncode != 0:
 			return res.returncode
 	Path(str(target[0])).parent.mkdir(parents=True, exist_ok=True)
@@ -174,7 +205,7 @@ def _sign_in_place(target: list[Any], source: list[Any], env: Any) -> int:
 	if not abspath.lower().endswith((".dll", ".exe")):
 		print(f"JP certprep skipped non-PE file: {abspath}")
 		return 0
-    if not os.path.isfile(abspath):
+	if not Path(abspath).is_file():
 		print(f"Warning: file not found for signing, skipping: {abspath}")
 		return 0
 	# Delegate to upstream signing action
@@ -201,7 +232,7 @@ def _sign_optional_path(target: list[Any], source: list[Any], env: Any, path: st
 		print("JP certprep skipped: signing not configured (set certFile or apiSigningToken)")
 		stamp_path.write_text("skip:no-sign-config", encoding="utf-8")
 		return 0
-    if not os.path.isfile(path):
+	if not Path(path).is_file():
 		print(f"Warning: file not found for signing, skipping: {path}")
 		stamp_path.write_text("skip:not-found", encoding="utf-8")
 		return 0
@@ -216,22 +247,16 @@ def _sign_optional_path(target: list[Any], source: list[Any], env: Any, path: st
 	stamp_path.write_text("ok", encoding="utf-8")
 	return 0
 
+
 def _find_vcvarsall() -> str | None:
 	"""Find vcvarsall.bat in common Visual Studio install locations.
 	Returns absolute path if found, None otherwise.
+	Currently supports Visual Studio 2022 only.
+	Search order: BuildTools, Community, Professional, Enterprise.
+
+	Note: This function delegates to jptools.vs_utils.find_vcvarsall() for shared logic.
 	"""
-    common_paths = [
-        r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat",
-        r"C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvarsall.bat",
-        r"C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvarsall.bat",
-        r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat",
-        r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\Build\vcvarsall.bat",
-        r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\VC\Auxiliary\Build\vcvarsall.bat",
-    ]
-    for p in common_paths:
-        if Path(p).exists():
-            return p
-    return None
+	return find_vcvarsall()
 
 
 def _get_vcvarsall_env(vcvarsall_path: str, arch: str) -> dict[str, str] | None:
@@ -289,8 +314,6 @@ def _get_vcvarsall_env(vcvarsall_path: str, arch: str) -> dict[str, str] | None:
 	return env
 
 
-
-
 def _compute_overlay_targets(repo_root: Path) -> list[str]:
 	"""Return absolute paths for files overlaid from miscDepsJp/source -> source.
 	Used to attach Clean so that `scons -c` can remove overlay artifacts.
@@ -316,6 +339,7 @@ def _filter_untracked(repo_root: Path, paths: list[str]) -> list[str]:
 	"""
 	# Lazy import to avoid unnecessary overhead when not cleaning
 	import subprocess
+
 	out: list[str] = []
 	for p in paths:
 		try:
@@ -335,20 +359,31 @@ def _filter_untracked(repo_root: Path, paths: list[str]) -> list[str]:
 	return out
 
 
-def register_jp_builders(env: Any, dist_target: Any | None = None) -> None:
+def register_jp_builders(env: Any, dist_target: Any | None = None, source_dir: Any | None = None) -> None:
 	"""Register JP-specific aliases without affecting upstream targets.
 
 	Args:
 		env: SCons environment
 		dist_target: Optional dist target node from sconstruct. If provided, jpCertExtras will depend on it
 					to ensure correct ordering in parallel builds (--all-cores).
+		source_dir: Optional source directory node from sconstruct. If provided, sourceDir will depend on
+					jtalkSync with the current TARGET_ARCH to ensure correct architecture-specific builds.
 	"""
-    # Allow TARGET_ARCH override from environment (takes priority) or existing env (fallback).
-    # This enables `set TARGET_ARCH=x64` then `scons.bat jtalkSync` for x64 payload/DLL switching.
-    env["TARGET_ARCH"] = str(os.environ.get("TARGET_ARCH", env.get("TARGET_ARCH", "x86"))).lower()
+	# Use BUILD_ARCH (JP-specific) to set TARGET_ARCH (SCons environment variable).
+	# BUILD_ARCH is an OS environment variable for JP-specific purposes (mainly smoke test environment switching).
+	# TARGET_ARCH is a SCons environment variable and should only be set via SCons, not OS environment.
+	# This refactoring ensures TARGET_ARCH follows SCons conventions while BUILD_ARCH handles JP-specific needs.
+	build_arch = str(os.environ.get("BUILD_ARCH", "")).lower()
+	if build_arch in ("x64", "x86_64"):
+		env["TARGET_ARCH"] = "x64"
+	elif build_arch == "x86":
+		env["TARGET_ARCH"] = "x86"
+	else:
+		# Fallback to existing SCons TARGET_ARCH (defaults to x64)
+		# Note: x86 builds are no longer supported
+		env["TARGET_ARCH"] = str(env.get("TARGET_ARCH", "x64")).lower()
 	# miscdepsjp alias removed in Phase 2 (miscDepsJp/source is empty, overlay is no-op)
 
-
 	# Alias: jp_tests (run JP dictionary tests and JP char description tests)
 	jp_tests_stamp = env.File("jptools/_state/jp_tests.stamp")
 	env.AlwaysBuild(jp_tests_stamp)
@@ -364,13 +399,13 @@ def register_jp_builders(env: Any, dist_target: Any | None = None) -> None:
 	def _ensure_jtalk_payload(target: list[Any], source: list[Any], env: Any) -> int:
 		"""Prepare JP jtalk payload for overlay with on-demand build.
 
-        - Resolve TARGET_ARCH (default x86)
+		- Resolve TARGET_ARCH (default x64, x86 builds are no longer supported)
 		- Locate vendor DLL under miscDepsJp/include/python-jtalk[/x86|x64]/libopenjtalk.dll
 		- If missing, attempt to build via nmake (requires MSVC environment)
 		- Write payload into source/synthDrivers/jtalk/libopenjtalk.dll (Phase 1: files moved)
 		"""
 		repo_root = Path.cwd()
-        arch = str(env.get("TARGET_ARCH", "x86")).lower()
+		arch = str(env.get("TARGET_ARCH", "x64")).lower()
 		vendor_base = repo_root / "miscDepsJp" / "include" / "python-jtalk"
 
 		if arch in ("x64", "x86_64"):
@@ -379,19 +414,15 @@ def _ensure_jtalk_payload(target: list[Any], source: list[Any], env: Any) -> int
 		else:
 			# x86 DLL is now in x86 subdirectory for consistency with x64
 			src_prebuilt = vendor_base / "x86" / "libopenjtalk.dll"
-            nmake_machine = "x86"  # Must pass explicitly (all.mak passes MACHINE=$(MACHINE) to lib/Makefile.mak)
+			nmake_machine = (
+				"x86"  # Must pass explicitly (all.mak passes MACHINE=$(MACHINE) to lib/Makefile.mak)
+			)
 
 		# all.mak builds DLL to vendor_base/libopenjtalk.dll, then we move it to arch-specific subdirectory
 		built_dll = vendor_base / "libopenjtalk.dll"
 
 		# Copy directly to source/synthDrivers/jtalk (Phase 1: files moved, no intermediate copy needed)
-        dst_payload = (
-            repo_root
-            / "source"
-            / "synthDrivers"
-            / "jtalk"
-            / "libopenjtalk.dll"
-        )
+		dst_payload = repo_root / "source" / "synthDrivers" / "jtalk" / "libopenjtalk.dll"
 
 		print(f"jtalkPrep: using TARGET_ARCH={arch}")
 		print(f"jtalkPrep: looking for vendor DLL: {src_prebuilt}")
@@ -402,6 +433,7 @@ def _ensure_jtalk_payload(target: list[Any], source: list[Any], env: Any) -> int
 			print(f"jtalkPrep: migrating DLL from old location: {old_dll_location} -> {src_prebuilt}")
 			try:
 				import shutil
+
 				src_prebuilt.parent.mkdir(parents=True, exist_ok=True)
 				shutil.move(str(old_dll_location), str(src_prebuilt))
 				print("jtalkPrep: DLL migrated successfully")
@@ -467,9 +499,15 @@ def _ensure_jtalk_payload(target: list[Any], source: list[Any], env: Any) -> int
 				# Check if nmake is available in PATH
 				# If not, we'll run nmake via vcvarsall.bat in the same shell
 				import subprocess
+
 				vcvarsall: str | None = None
 				try:
-                    run(["nmake", "/?"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
+					run(
+						["nmake", "/?"],
+						stdout=subprocess.DEVNULL,
+						stderr=subprocess.DEVNULL,
+						check=True,
+					)
 					print("jtalkPrep: nmake found in PATH")
 					use_vcvarsall = False
 				except (FileNotFoundError, subprocess.CalledProcessError):
@@ -488,9 +526,20 @@ def _ensure_jtalk_payload(target: list[Any], source: list[Any], env: Any) -> int
 				if use_vcvarsall:
 					assert vcvarsall is not None  # Type narrowing for type checker
 					clean_script = f'call "{vcvarsall}" {nmake_machine} && nmake /f all.mak clean MACHINE={nmake_machine}'
-                    run(clean_script, cwd=str(build_dir), shell=True, capture_output=True)
+					run(
+						clean_script,
+						cwd=str(build_dir),
+						shell=True,
+						capture_output=True,
+					)
 				else:
-                    clean_cmd = ["nmake", "/f", "all.mak", "clean", f"MACHINE={nmake_machine}"]
+					clean_cmd = [
+						"nmake",
+						"/f",
+						"all.mak",
+						"clean",
+						f"MACHINE={nmake_machine}",
+					]
 					run(clean_cmd, cwd=str(build_dir), capture_output=True)
 
 				# Build nmake command - if using vcvarsall, wrap it in cmd /c call
@@ -500,7 +549,9 @@ def _ensure_jtalk_payload(target: list[Any], source: list[Any], env: Any) -> int
 					assert vcvarsall is not None  # Type narrowing for type checker
 					print(f"jtalkPrep: running nmake via vcvarsall.bat with arch={nmake_machine}")
 					# Use shell=True to avoid subprocess quote escaping issues
-                    cmd_script = f'call "{vcvarsall}" {nmake_machine} && nmake /f all.mak MACHINE={nmake_machine}'
+					cmd_script = (
+						f'call "{vcvarsall}" {nmake_machine} && nmake /f all.mak MACHINE={nmake_machine}'
+					)
 					result = run(
 						cmd_script,
 						cwd=str(build_dir),
@@ -556,7 +607,11 @@ def _ensure_jtalk_payload(target: list[Any], source: list[Any], env: Any) -> int
 		Path(str(target[0])).write_text("ok", encoding="utf-8")
 		return 0
 
-    jtalk_prep_stamp = env.File("miscDepsJp/_state/prep/jtalkPrep.stamp")
+	# Use TARGET_ARCH in stamp filename to ensure rebuild when architecture changes
+	# This prevents x86/x64 DLL mismatches when switching architectures
+	arch = str(env.get("TARGET_ARCH", "x64")).lower()
+	arch_suffix = "x64" if arch in ("x64", "x86_64") else "x86"
+	jtalk_prep_stamp = env.File(f"miscDepsJp/_state/prep/jtalkPrep.{arch_suffix}.stamp")
 	env.AlwaysBuild(jtalk_prep_stamp)
 	env.Command(jtalk_prep_stamp, [], _ensure_jtalk_payload)
 	env.Alias("jtalkPrep", jtalk_prep_stamp)
@@ -603,7 +658,12 @@ def _run_nmake(machine: str) -> int:
 			from subprocess import run
 
 			try:
-                run(["nmake", "/?"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
+				run(
+					["nmake", "/?"],
+					stdout=subprocess.DEVNULL,
+					stderr=subprocess.DEVNULL,
+					check=True,
+				)
 				# nmake is available, use it directly
 				cmd = ["nmake", "/f", "all.mak", f"MACHINE={machine}"]
 				result = run(cmd, cwd=str(vendor_base))
@@ -632,8 +692,14 @@ def _build_mecab_bin(machine: str) -> int:
 				return 1
 			import subprocess
 			from subprocess import run
+
 			try:
-                run(["nmake", "/?"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
+				run(
+					["nmake", "/?"],
+					stdout=subprocess.DEVNULL,
+					stderr=subprocess.DEVNULL,
+					check=True,
+				)
 				# nmake is available, use it directly
 				cmd = ["nmake", "/f", "Makefile.mak", f"MACHINE={machine}"]
 				result = run(cmd, cwd=str(base))
@@ -649,6 +715,7 @@ def _build_mecab_bin(machine: str) -> int:
 
 		# If dictionary is missing or invalid, build it directly into source/synthDrivers/jtalk/dic
 		if should_rebuild_dic or not sys_dic.exists():
+
 			def _build_dic(machine: str) -> int:
 				base = vendor_base / "libopenjtalk" / "mecab-naist-jdic"
 				makefile = base / "Makefile.mak"
@@ -673,7 +740,9 @@ def _build_dic(machine: str) -> int:
 						print(f"jtalkSync: libmecab.dll still missing after build: {libmecab_dll}")
 						print("jtalkSync: warning: libmecab.dll build may have failed, but continuing...")
 					# make_jdic.py expects mecab-dict-index.exe under jptools/jtalk/libopenjtalk/mecab/src
-                    make_jdic_mecab_bin = builder_script_path.parent / "libopenjtalk" / "mecab" / "src" / "mecab-dict-index.exe"
+					make_jdic_mecab_bin = (
+						builder_script_path.parent / "libopenjtalk" / "mecab" / "src" / "mecab-dict-index.exe"
+					)
 					try:
 						make_jdic_mecab_bin.parent.mkdir(parents=True, exist_ok=True)
 						shutil.copy2(mecab_dict_index_bin, make_jdic_mecab_bin)
@@ -685,23 +754,31 @@ def _build_dic(machine: str) -> int:
 					env_vars = os.environ.copy()
 					env_vars.setdefault("PYTHONUTF8", "1")
 					print("jtalkSync: building dictionary with make_jdic.py (UTF-8).")
-                    result = run([python_exe, str(builder_script_path)], cwd=str(builder_script_path.parent), env=env_vars)
+					result = run(
+						[python_exe, str(builder_script_path)],
+						cwd=str(builder_script_path.parent),
+						env=env_vars,
+					)
 					return result.returncode
 
 				if not makefile.exists():
 					print(f"jtalkSync: Makefile.mak not found for dictionary build: {makefile}")
 					return 1
 
-                # BEGIN JP PATCH: Create dicrc to set config-charset=sjis for .def files
+				# Create dicrc to set config-charset=sjis for .def files
 				dicrc = base / "dicrc"
 				if not dicrc.exists():
 					# Use same format as existing dicrc (with spaces around =)
 					dicrc.write_text("config-charset = sjis\n", encoding="utf-8")
 					print("jtalkSync: created dicrc with config-charset = sjis")
-                # END JP PATCH
 
 				try:
-                    run(["nmake", "/?"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
+					run(
+						["nmake", "/?"],
+						stdout=subprocess.DEVNULL,
+						stderr=subprocess.DEVNULL,
+						check=True,
+					)
 					# nmake is available, use it directly
 					# Note: dicrc has config-charset=sjis, so mecab-dict-index should read .def files as SJIS.
 					# chcp 932 is a fallback for environments where dicrc config might not be respected.
@@ -709,8 +786,8 @@ def _build_dic(machine: str) -> int:
 					# If chcp fails, continue anyway (dicrc config should handle it)
 					cmd_script = (
 						'cmd /c "'
-                        'chcp 932 >nul 2>&1 || echo Warning: chcp 932 failed, relying on dicrc config && '
-                        f'nmake /f Makefile.mak MACHINE={machine}'
+						"chcp 932 >nul 2>&1 || echo Warning: chcp 932 failed, relying on dicrc config && "
+						f"nmake /f Makefile.mak MACHINE={machine}"
 						'"'
 					)
 					print("jtalkSync: building dictionary (dicrc config-charset=sjis, chcp 932 as fallback)")
@@ -727,11 +804,13 @@ def _build_dic(machine: str) -> int:
 					cmd_script = (
 						f'cmd /c "'
 						f'call "{vcvarsall}" {machine} && '
-                        f'chcp 932 >nul 2>&1 || echo Warning: chcp 932 failed, relying on dicrc config && '
-                        f'nmake /f Makefile.mak MACHINE={machine}'
+						f"chcp 932 >nul 2>&1 || echo Warning: chcp 932 failed, relying on dicrc config && "
+						f"nmake /f Makefile.mak MACHINE={machine}"
 						f'"'
 					)
-                    print("jtalkSync: building dictionary via vcvarsall (dicrc config-charset=sjis, chcp 932 as fallback)")
+					print(
+						"jtalkSync: building dictionary via vcvarsall (dicrc config-charset=sjis, chcp 932 as fallback)"
+					)
 					result = run(cmd_script, cwd=str(base), shell=True)
 					return result.returncode
 				# This code path should not be reached, but kept for safety
@@ -745,10 +824,12 @@ def _build_dic(machine: str) -> int:
 				result = run(cmd, cwd=str(base))
 				return result.returncode
 
-            arch = str(env.get("TARGET_ARCH", "x86")).lower()
+			arch = str(env.get("TARGET_ARCH", "x64")).lower()
 			machine = "x64" if arch in ("x64", "x86_64") else "x86"
 
-            print("jtalkSync: sys.dic missing or out of date; building python-jtalk (nmake all) and mecab dic")
+			print(
+				"jtalkSync: sys.dic missing or out of date; building python-jtalk (nmake all) and mecab dic"
+			)
 			rc = _run_nmake(machine)
 			if rc != 0:
 				print(f"jtalkSync: nmake (all.mak) failed with rc={rc}")
@@ -784,7 +865,7 @@ def _build_dic(machine: str) -> int:
 		# Copy core assets (DLLs only; Python files have been moved to source/synthDrivers/jtalk in Phase 1)
 		try:
 			# Copy libmecab.dll (built from source or fallback to existing)
-            arch = str(env.get("TARGET_ARCH", "x86")).lower()
+			arch = str(env.get("TARGET_ARCH", "x64")).lower()
 			machine = "x64" if arch in ("x64", "x86_64") else "x86"
 			# First, try to find built libmecab.dll from mecab/src directory
 			built_libmecab = vendor_base / "libopenjtalk" / "mecab" / "src" / "libmecab.dll"
@@ -807,7 +888,9 @@ def _build_dic(machine: str) -> int:
 					shutil.copy2(fallback_libmecab, jtalk_dir / "libmecab.dll")
 					print(f"jtalkSync: copied fallback libmecab.dll from {fallback_libmecab}")
 				else:
-                    print(f"jtalkSync: warning: libmecab.dll not found (expected at {built_libmecab} or {fallback_libmecab})")
+					print(
+						f"jtalkSync: warning: libmecab.dll not found (expected at {built_libmecab} or {fallback_libmecab})"
+					)
 			# Copy arch-specific libopenjtalk.dll (x86 or x64)
 			if arch in ("x64", "x86_64"):
 				src_dll = vendor_base / "x64" / "libopenjtalk.dll"
@@ -825,18 +908,50 @@ def _build_dic(machine: str) -> int:
 		stamp_path.write_text("ok", encoding="utf-8")
 		return 0
 
-    jtalk_sync_stamp = env.File("miscDepsJp/_state/prep/jtalkSync.stamp")
-    env.AlwaysBuild(jtalk_sync_stamp)
+	# Use TARGET_ARCH in stamp filename to ensure rebuild when architecture changes
+	# This prevents x86/x64 DLL mismatches when switching architectures
+	# Note: arch_suffix is already defined above for jtalkPrep
+	jtalk_sync_stamp = env.File(f"miscDepsJp/_state/prep/jtalkSync.{arch_suffix}.stamp")
+	# Remove AlwaysBuild: use dependency-based rebuild instead
 	# jtalkSync depends on jtalkPrep to avoid file lock conflicts when both try to build hts.mak
+	# Note: jtalkSync output files (sys.dic, libmecab.dll, libopenjtalk.dll) are not added here as
+	# explicit dependencies. jtalkSync first produces these files under miscDepsJp and then copies
+	# them into the source tree. The top-level 'source' target already depends on jtalkSync
+	# via env.Depends(source_dir, jtalk_sync_stamp) below, so adding the individual output files
+	# as dependencies on this stamp target would be redundant rather than preventing a circular dependency.
 	env.Command(jtalk_sync_stamp, [jtalk_prep_stamp], _sync_jtalk_assets)
 	env.Alias("jtalkSync", jtalk_sync_stamp)
 
+	# Set up sourceDir dependency on jtalkSync with current TARGET_ARCH
+	# This ensures that when TARGET_ARCH changes (x86 -> x64 -> x86), the correct
+	# architecture-specific stamp file is used, triggering rebuilds as needed.
+	if source_dir is not None:
+		env.Depends(source_dir, jtalk_sync_stamp)
+
 	# Register files generated by jtalkSync for cleanup (scons -c)
 	repo_root = Path.cwd()
 	vendor_base = repo_root / "miscDepsJp" / "include" / "python-jtalk"
 	mecab_src_dir = vendor_base / "libopenjtalk" / "mecab" / "src"
 	jtalk_dir = repo_root / "source" / "synthDrivers" / "jtalk"
-    # mecab-dict-index.exe (built by jtalkSync)
+	dic_dir = jtalk_dir / "dic"
+
+	# Clean up all .obj, .lib, and .exe files in mecab/src directory using glob
+	# This ensures that stale object files from previous builds (x86/x64) are removed
+	import glob
+
+	for pattern in ["*.obj", "*.lib", "*.exe"]:
+		for file_path in glob.glob(str(mecab_src_dir / pattern)):
+			env.Clean(jtalk_sync_stamp, file_path)
+
+	# Clean dictionary outputs so `scons -c jtalkSync` forces a rebuild on next run.
+	# Preserve license/docs files that should remain in the tree.
+	keep_dic_files = {"COPYING", "COPYING-bep-eng.txt", "dicrc"}
+	if dic_dir.exists():
+		for file_path in dic_dir.glob("*"):
+			if file_path.is_file() and file_path.name not in keep_dic_files:
+				env.Clean(jtalk_sync_stamp, str(file_path))
+
+	# mecab-dict-index.exe (built by jtalkSync) - already covered by glob above, but keep for clarity
 	mecab_dict_index = str(mecab_src_dir / "mecab-dict-index.exe")
 	env.Clean(jtalk_sync_stamp, mecab_dict_index)
 	# libmecab.dll (built by jtalkSync, then copied to source/synthDrivers/jtalk)
@@ -847,63 +962,18 @@ def _build_dic(machine: str) -> int:
 	# libopenjtalk.dll (copied to source/synthDrivers/jtalk by jtalkSync)
 	libopenjtalk_dll = str(jtalk_dir / "libopenjtalk.dll")
 	env.Clean(jtalk_sync_stamp, libopenjtalk_dll)
-    # mecab.lib (built by jtalkSync)
+	# mecab.lib (built by jtalkSync) - already covered by glob above, but keep for clarity
 	mecab_lib = str(mecab_src_dir / "mecab.lib")
 	env.Clean(jtalk_sync_stamp, mecab_lib)
-    # Object files generated by Makefile.mak (to prevent stale objects from causing rebuild issues)
-    # List from Makefile.mak: CORES + CORES_DLL + mecab-dict-index.obj
-    mecab_obj_files = [
-        "char_property.obj",
-        "connector.obj",
-        "context_id.obj",
-        "dictionary.obj",
-        "dictionary_compiler.obj",
-        "dictionary_generator.obj",
-        "dictionary_rewriter.obj",
-        "eval.obj",
-        "feature_index.obj",
-        "iconv_utils.obj",
-        "lbfgs.obj",
-        "learner.obj",
-        "learner_tagger.obj",
-        "libmecab.obj",
-        "mecab.obj",
-        "nbest_generator.obj",
-        "param.obj",
-        "string_buffer.obj",
-        "tagger.obj",
-        "tokenizer.obj",
-        "utils.obj",
-        "viterbi.obj",
-        "writer.obj",
-        "char_property_dll.obj",
-        "connector_dll.obj",
-        "context_id_dll.obj",
-        "dictionary_dll.obj",
-        "dictionary_compiler_dll.obj",
-        "dictionary_generator_dll.obj",
-        "dictionary_rewriter_dll.obj",
-        "eval_dll.obj",
-        "feature_index_dll.obj",
-        "iconv_utils_dll.obj",
-        "lbfgs_dll.obj",
-        "learner_dll.obj",
-        "learner_tagger_dll.obj",
-        "libmecab_dll.obj",
-        "mecab_dll.obj",
-        "nbest_generator_dll.obj",
-        "param_dll.obj",
-        "string_buffer_dll.obj",
-        "tagger_dll.obj",
-        "tokenizer_dll.obj",
-        "utils_dll.obj",
-        "viterbi_dll.obj",
-        "writer_dll.obj",
-        "mecab-dict-index.obj",
-    ]
-    for obj_file in mecab_obj_files:
-        obj_path = str(mecab_src_dir / obj_file)
-        env.Clean(jtalk_sync_stamp, obj_path)
+
+	# Clean up both x64 and x86 stamp files to ensure architecture switching works correctly
+	# This prevents stale stamp files from preventing rebuilds when switching architectures
+	prep_state_dir = repo_root / "miscDepsJp" / "_state" / "prep"
+	for arch_suffix_clean in ["x64", "x86"]:
+		jtalk_prep_stamp_clean = str(prep_state_dir / f"jtalkPrep.{arch_suffix_clean}.stamp")
+		jtalk_sync_stamp_clean = str(prep_state_dir / f"jtalkSync.{arch_suffix_clean}.stamp")
+		env.Clean(jtalk_sync_stamp, jtalk_prep_stamp_clean)
+		env.Clean(jtalk_sync_stamp, jtalk_sync_stamp_clean)
 
 	# Note: Dependencies are already established in sconstruct:
 	#   - sourceDir -> jtalkSync (L401)
@@ -912,12 +982,10 @@ def _build_dic(machine: str) -> int:
 	# This creates the dependency chain: dist -> sourceDir -> jtalkSync -> jtalkPrep
 	# No additional wiring needed here; using Dir/target objects (not Alias) is more robust.
 
-
-
 	# Alias: controllerClient (zip artifact)
 	out_dir = str(env.get("outputDir", "output"))
 	version = str(env.get("version", "local"))
-    cc_zip = env.File(os.path.join(out_dir, f"nvda_{version}_controllerClientJp.zip"))
+	cc_zip = env.File(str(Path(out_dir) / f"nvda_{version}_controllerClientJp.zip"))
 	env.Command(cc_zip, [], _pack_controller_client)
 	env.Alias("controllerClient", cc_zip)
 
@@ -961,13 +1029,24 @@ def _stage_controller_client(target: list[Any], source: list[Any], env: Any) ->
 					shutil.copy2(src_doc, dst_doc)
 					print(f"jpStageControllerClient: copied {doc_file}")
 			# Copy examples directory if it exists
+			# Note: preserve existing files (e.g., JP-specific test_*.py) and only copy/update files from extras/controllerClient/examples
 			src_examples = extras_client_dir / "examples"
 			if src_examples.exists():
 				dst_examples = client_root / "examples"
-                if dst_examples.exists():
-                    shutil.rmtree(dst_examples)
-                shutil.copytree(src_examples, dst_examples)
-                print("jpStageControllerClient: copied examples directory")
+				dst_examples.mkdir(parents=True, exist_ok=True)
+				# Copy files and subdirectories from src_examples, preserving existing files
+				for item in src_examples.iterdir():
+					src_item = item
+					dst_item = dst_examples / item.name
+					if src_item.is_dir():
+						if dst_item.exists():
+							shutil.rmtree(dst_item)
+						shutil.copytree(src_item, dst_item)
+						print(f"jpStageControllerClient: copied examples/{item.name}/")
+					else:
+						shutil.copy2(src_item, dst_item)
+						print(f"jpStageControllerClient: copied examples/{item.name}")
+				print("jpStageControllerClient: updated examples directory")
 		except Exception as e:
 			print(f"jpStageControllerClient: error: {e}")
 			return 1
@@ -984,7 +1063,9 @@ def _stage_controller_client(target: list[Any], source: list[Any], env: Any) ->
 	for arch in ["x86", "x64", "arm64"]:
 		# Add DLL as dependency (main artifact)
 		dll_path = extras_client_dir / arch / "nvdaControllerClient.dll"
-        if dll_path.exists() or not source_files:  # Include at least one file per arch for dependency tracking
+		if (
+			dll_path.exists() or not source_files
+		):  # Include at least one file per arch for dependency tracking
 			source_files.append(env.File(str(dll_path)))
 	# If no files exist yet, use empty list (will be created on first run)
 	if not source_files:
@@ -1033,20 +1114,35 @@ def _cert_extras(target: list[Any], source: list[Any], env: Any) -> int:
 				candidates.append(dll_path)
 			else:
 				missing_required.append(dll_path)
+		# Sign files in dist/lib/<version>/ (nvdaHelper*.dll, etc.)
+		# These files are copied from source/ to dist/ during dist build, but may lose signatures
+		# during the copy process. We sign them here to ensure they are signed before launcher build.
+		build_version = str(env.get("version", ""))
+		if build_version:
+			lib_version_dir = dist_dir / "lib" / build_version
+			if lib_version_dir.exists():
+				for pattern in ("**/*.dll", "**/*.exe"):
+					for path in lib_version_dir.glob(pattern):
+						if path.is_file():
+							candidates.append(path)
 		# Note: nvdaHelper*.dll files (IAccessible2proxy.dll, ISimpleDOM.dll, nvdaHelperRemote.dll,
 		# nvdaHelperRemoteLoader.exe, UIARemote.dll, nvdaHelperLocal.dll, nvdaHelperLocalWin10.dll)
-        # are signed during source build (see nvdaHelper/archBuild_sconscript) and should remain
-        # signed when copied to dist/ during dist build. They are NOT signed by jpCertExtras.
-        # If any of these files are unsigned in dist/, that indicates a build problem that should
-        # be fixed at the source build level, not worked around here.
+		# are signed during source build (see nvdaHelper/archBuild_sconscript), but may lose signatures
+		# when copied to dist/ during dist build. We sign them here in jpCertExtras to ensure
+		# they are signed before launcher build.
 		# Report missing required DLLs (must be in dist/, not source/)
 		if missing_required:
 			print("jpCertExtras: ERROR - Required DLLs not found in dist/:")
 			for dll_path in missing_required:
 				print(f"  {dll_path}")
 			print("jpCertExtras: These files must be present in dist/ before signing.")
-            print("jpCertExtras: Build order: jtalkSync (copies to source/) -> dist (copies to dist/) -> jpCertExtras (signs dist/)")
-            stamp_path.write_text(f"error:missing-dlls:{','.join(str(p.name) for p in missing_required)}", encoding="utf-8")
+			print(
+				"jpCertExtras: Build order: jtalkSync (copies to source/) -> dist (copies to dist/) -> jpCertExtras (signs dist/)"
+			)
+			stamp_path.write_text(
+				f"error:missing-dlls:{','.join(str(p.name) for p in missing_required)}",
+				encoding="utf-8",
+			)
 			return 1
 		# Perform signing via upstream signExec
 		signed_count = 0
@@ -1140,8 +1236,18 @@ def _verify_signatures(target: list[Any], source: list[Any], env: Any) -> int:
 		out_dir = repo_root / "output"
 		dist_dir = repo_root / "dist"
 
-        mode = str(env.get("JP_VERIFY_SIGNATURES_MODE", os.environ.get("JP_VERIFY_SIGNATURES_MODE", "fast"))).lower()
-        verbose = str(env.get("JP_VERIFY_SIGNATURES_VERBOSE", os.environ.get("JP_VERIFY_SIGNATURES_VERBOSE", "0"))).lower() in (
+		mode = str(
+			env.get(
+				"JP_VERIFY_SIGNATURES_MODE",
+				os.environ.get("JP_VERIFY_SIGNATURES_MODE", "fast"),
+			)
+		).lower()
+		verbose = str(
+			env.get(
+				"JP_VERIFY_SIGNATURES_VERBOSE",
+				os.environ.get("JP_VERIFY_SIGNATURES_VERBOSE", "0"),
+			)
+		).lower() in (
 			"1",
 			"true",
 			"yes",
@@ -1160,7 +1266,9 @@ def _verify_signatures(target: list[Any], source: list[Any], env: Any) -> int:
 			"wxmsw32u_stc_vc140.dll",
 		}
 
-        def _signtool_verify(signtool_path: str, file_path: Path, *, quiet: bool) -> subprocess.CompletedProcess[str]:
+		def _signtool_verify(
+			signtool_path: str, file_path: Path, *, quiet: bool
+		) -> subprocess.CompletedProcess[str]:
 			args = [signtool_path, "verify", "/pa"]
 			args.append("/q" if quiet else "/v")
 			return subprocess.run(args + [str(file_path)], capture_output=True, text=True)
@@ -1172,7 +1280,9 @@ def _format_signtool_output(result: subprocess.CompletedProcess[str]) -> str:
 				return f"{out}\n{err}"
 			return out or err or ""
 
-        def _verify_one(signtool_path: str, file_path: Path, *, allow_ignored: bool) -> tuple[bool, bool, str]:
+		def _verify_one(
+			signtool_path: str, file_path: Path, *, allow_ignored: bool
+		) -> tuple[bool, bool, str]:
 			result = _signtool_verify(signtool_path, file_path, quiet=True)
 			if result.returncode == 0:
 				return True, False, ""
@@ -1187,7 +1297,11 @@ def _verify_one(signtool_path: str, file_path: Path, *, allow_ignored: bool) ->
 		try:
 			exe: Path | None = None
 			if out_dir.exists():
-                exe_candidates = sorted(out_dir.glob("nvda_*.exe"), key=lambda p: p.stat().st_mtime, reverse=True)
+				exe_candidates = sorted(
+					out_dir.glob("nvda_*.exe"),
+					key=lambda p: p.stat().st_mtime,
+					reverse=True,
+				)
 				if exe_candidates:
 					exe = exe_candidates[0]
 			if not exe:
@@ -1238,36 +1352,13 @@ def _check(path: Path, *, allow_ignored: bool) -> None:
 					dist_dir / "uninstall.exe",
 				]
 				if build_version:
-                    helper_files_by_root = {
-                        # dist/lib/<version>/ contains x86 binaries, including local/UIA helpers.
-                        "lib": (
-                            "IAccessible2proxy.dll",
-                            "ISimpleDOM.dll",
-                            "UIARemote.dll",
-                            "nvdaHelperLocal.dll",
-                            "nvdaHelperLocalWin10.dll",
-                            "nvdaHelperRemote.dll",
-                            "windowsaccessbridge-32.dll",
-                        ),
-                        # dist/lib64/<version>/ and dist/libArm64/<version>/ contain remote helpers only.
-                        "lib64": (
-                            "IAccessible2proxy.dll",
-                            "ISimpleDOM.dll",
-                            "nvdaHelperRemote.dll",
-                            "nvdaHelperRemoteLoader.exe",
-                        ),
-                        "libArm64": (
-                            "IAccessible2proxy.dll",
-                            "ISimpleDOM.dll",
-                            "nvdaHelperRemote.dll",
-                            "nvdaHelperRemoteLoader.exe",
-                        ),
-                    }
-                    for root_name, helper_names in helper_files_by_root.items():
-                        version_dir = dist_dir / root_name / build_version
-                        if version_dir.exists():
-                            for helper_name in helper_names:
-                                critical_paths.append(version_dir / helper_name)
+					# Checking dist/lib/<version> recursively for any DLLs/EXEs (handles x86/x64/arm64 subdirs automatically)
+					lib_version_dir = dist_dir / "lib" / build_version
+					if lib_version_dir.exists():
+						for pattern in ("**/*.dll", "**/*.exe"):
+							for path in lib_version_dir.glob(pattern):
+								if path.is_file():
+									critical_paths.append(path)
 				for path in critical_paths:
 					_check(path, allow_ignored=False)
 			else:
@@ -1321,7 +1412,9 @@ def _check(path: Path, *, allow_ignored: bool) -> None:
 				print(f"jpVerifySignatures: OK ({mode})")
 			return 0
 		except FileNotFoundError:
-            print("jpVerifySignatures: skip (signtool not found). Ensure Windows SDK is installed or SIGNTOOL is set.")
+			print(
+				"jpVerifySignatures: skip (signtool not found). Ensure Windows SDK is installed or SIGNTOOL is set."
+			)
 			stamp_path.write_text("skip:no-signtool", encoding="utf-8")
 			return 0
 		except Exception as e:

```