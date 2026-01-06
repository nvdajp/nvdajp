# Diff for: `jptools\nonCertBuild.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\jptools\nonCertBuild.py`  
**Current**: `F:\nvda\gh\alphajp\jptools\nonCertBuild.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\nonCertBuild.py" "b/F:\\nvda\\gh\\alphajp\\jptools\\nonCertBuild.py"
index 50a76ffe0b..33bef55863 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\jptools\\nonCertBuild.py"
+++ "b/F:\\nvda\\gh\\alphajp\\jptools\\nonCertBuild.py"
@@ -17,6 +17,7 @@ def run_cmd(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | No
 		print(f"::error::Command not found: {cmd[0]} ({e})")
 		sys.exit(127)
 
+
 MSVC_ENV_KEYS = (
 	"PATH",
 	"INCLUDE",
@@ -49,7 +50,12 @@ def _ensure_nmake_env() -> None:
 
 	def _capture_env_via_cmd(call_stmt: str, *, cwd: Path | None = None) -> dict[str, str] | None:
 		try:
-            out = subprocess.check_output(["cmd", "/c", f"{call_stmt} && set"], text=True, errors="ignore", cwd=str(cwd) if cwd else None)
+			out = subprocess.check_output(
+				["cmd", "/c", f"{call_stmt} && set"],
+				text=True,
+				errors="ignore",
+				cwd=str(cwd) if cwd else None,
+			)
 		except Exception as e:
 			print(f"::warning::Failed to initialize MSVC env via: {call_stmt} ({e})")
 			return None
@@ -114,11 +120,11 @@ def _capture_env_via_cmd(call_stmt: str, *, cwd: Path | None = None) -> dict[str
 					name = script.name.lower()
 					if name == "vsdevcmd.bat":
 						# Prefer x86 target tools for JP build toolchain
-                        call = f"set VSCMD_ARG_TGT_ARCH=x86 && call \"{script}\" -no_logo"
+						call = f'set VSCMD_ARG_TGT_ARCH=x86 && call "{script}" -no_logo'
 					elif name == "vcvarsall.bat":
-                        call = f"call \"{script}\" x86"
+						call = f'call "{script}" x86'
 					else:
-                        call = f"call \"{script}\""
+						call = f'call "{script}"'
 					envmap = _capture_env_via_cmd(call)
 					if envmap:
 						# Prefer build-related keys; update PATH/INCLUDE/LIB/LIBPATH and others.
@@ -133,7 +139,9 @@ def _capture_env_via_cmd(call_stmt: str, *, cwd: Path | None = None) -> dict[str
 							os.environ["CL"] = (current_cl + " /arch:IA32").strip()
 						else:
 							os.environ["CL"] = current_cl
-                        print(f"[nonCertBuild] MSVC env imported via vswhere from {script.name} ({updated} vars)")
+						print(
+							f"[nonCertBuild] MSVC env imported via vswhere from {script.name} ({updated} vars)"
+						)
 						return
 
 	# 3) Fallback to JP's repo-local vcsetup.cmd
@@ -141,7 +149,7 @@ def _capture_env_via_cmd(call_stmt: str, *, cwd: Path | None = None) -> dict[str
 	if not vcsetup.exists():
 		print(f"::warning::VC setup script not found: {vcsetup}")
 		return
-    envmap = _capture_env_via_cmd(f"call \"{vcsetup}\" >nul", cwd=repo_root)
+	envmap = _capture_env_via_cmd(f'call "{vcsetup}" >nul', cwd=repo_root)
 	if not envmap:
 		return
 	updated = 0
@@ -154,6 +162,7 @@ def _capture_env_via_cmd(call_stmt: str, *, cwd: Path | None = None) -> dict[str
 	else:
 		print("::warning::vcsetup completed but no environment variables were imported")
 
+
 def _is_ci() -> bool:
 	return os.environ.get("GITHUB_ACTIONS") == "true"
 
@@ -224,6 +233,7 @@ def _prep_miscdepsjp() -> None:
 	for rel in ["dic", "_temp"]:
 		try:
 			import shutil as _sh
+
 			_sh.rmtree(naist_dic / rel, ignore_errors=True)
 		except Exception:
 			pass
@@ -247,9 +257,11 @@ def _activation_candidates() -> list[str]:
 	"""Return possible activation call statements for MSVC env (x86)."""
 	calls: list[str] = []
 	vswhere = Path(r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe")
+
 	def _add_if_exists(path: Path, args: str = ""):
 		if path.exists():
-            calls.append(f"call \"{path}\"{(' ' + args) if args else ''}")
+			calls.append(f'call "{path}"{(" " + args) if args else ""}')
+
 	# Prefer vswhere -find to get exact bat paths
 	if vswhere.exists():
 		for pattern, args in (
@@ -269,7 +281,7 @@ def _add_if_exists(path: Path, args: str = ""):
 				_add_if_exists(Path(p), args)
 	# Fallback to common install roots
 	for edition in ("Enterprise", "Professional", "Community", "BuildTools"):
-        root = Path(fr"C:\Program Files\Microsoft Visual Studio\2022\{edition}")
+		root = Path(rf"C:\Program Files\Microsoft Visual Studio\2022\{edition}")
 		_add_if_exists(root / "VC" / "Auxiliary" / "Build" / "vcvars32.bat")
 		_add_if_exists(root / "VC" / "Auxiliary" / "Build" / "vcvarsall.bat", "x86")
 		_add_if_exists(root / "Common7" / "Tools" / "VsDevCmd.bat", "-no_logo")
@@ -279,6 +291,7 @@ def _add_if_exists(path: Path, args: str = ""):
 def _nowdate() -> str:
 	# Generate same format as jptools/nowdate.py without importing it (to avoid side effects)
 	from datetime import datetime as _dt
+
 	return _dt.now().strftime("%y%m%d") + chr(_dt.now().hour + 97)
 
 
@@ -304,15 +317,19 @@ def _build_with_scons(forwarded_args: list[str]) -> None:
 	# Forward args from caller (after -- separator)
 	scons_args = options + forwarded_args
 
-    # Build targets in the same order as nonCertBuild2.cmd
+	# Build launcher (final target)
+	# Note: we only invoke the "launcher" target here and rely on the SCons dependency chain
+	# (launcher -> dist -> source -> jtalkSync -> jtalkPrep) to run intermediate targets
+	# such as jtalkSync and jtalkPrep. This reduces redundant scons.bat invocations and
+	# jtalkSync executions, and relies on SCons' dependency tracking and build verification
+	# (a failed or skipped jtalkSync causes the SCons build, and thus this script, to fail).
 	# Use scons.bat (which uses uv run SCons) to ensure it works in CI environments
 	repo_root = Path(__file__).resolve().parents[1]
 	scons_bat = repo_root / "scons.bat"
 	if not scons_bat.exists():
 		print(f"Error: scons.bat not found at {scons_bat}")
 		sys.exit(1)
-    for target in ("source", "user_docs", "dist", "launcher"):
-        run_cmd([str(scons_bat), target] + scons_args)
+	run_cmd([str(scons_bat), "launcher"] + scons_args)
 
 
 def main() -> int:

```