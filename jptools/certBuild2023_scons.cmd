@echo off
rem JP helper: build signed NVDA via SCons using the certBuild2023 alias.
rem - Keeps the original jptools\certBuild2023.cmd unchanged.
rem - Signing uses SCons' signExec (certFile/apiSigningToken or CERT_* store vars).
rem - Any additional arguments are forwarded to SCons.

setlocal enableextensions enabledelayedexpansion

set REPO_DIR=%~dp0\..
pushd "%REPO_DIR%"

rem Try to initialize MSVC (optional best-effort). Falls back gracefully.
set "_VCVARS_COMMUNITY=%ProgramFiles%\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat"
set "_VCVARS_PRO=%ProgramFiles%\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvarsall.bat"
set "_VCVARS_ENT=%ProgramFiles%\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvarsall.bat"
if exist "%_VCVARS_COMMUNITY%" call "%_VCVARS_COMMUNITY%" x86 >nul 2>&1
if not defined VSCMD_VER if exist "%_VCVARS_PRO%" call "%_VCVARS_PRO%" x86 >nul 2>&1
if not defined VSCMD_VER if exist "%_VCVARS_ENT%" call "%_VCVARS_ENT%" x86 >nul 2>&1

rem Default parallelism
set "_SCONS_ARGS=--all-cores"

rem Forward all user-provided args to SCons as-is.
set "_FORWARD=%*"

echo === JP certBuild2023 (SCons) ===
echo PWD: %CD%
echo SCons args: %_SCONS_ARGS% %_FORWARD%

rem Ensure uv / venv setup and run SCons via the repository helper
call scons.bat certBuild2023 signExtras=1 %_SCONS_ARGS% %_FORWARD%
set ERR=%ERRORLEVEL%
if not "%ERR%"=="0" goto :onerror

echo.
echo Done. See output\sign-extras-manifest.txt and output\sign-extras-verify.log
popd
exit /b 0

:onerror
echo ERROR: SCons certBuild2023 failed with code %ERR% >&2
popd
exit /b %ERR%

