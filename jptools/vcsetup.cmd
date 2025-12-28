@echo off
rem Setup MSVC build environment persistently. Usage: vcsetup.cmd [x64|x86]
rem Defaults to x86.
rem Currently supports Visual Studio 2022 only.

rem Fast path: check if cl is already available
cl >nul 2>&1
if "%ERRORLEVEL%" neq "9009" (
  rem cl is available, MSVC environment already configured
  goto :done
)

set "ARCH=%~1"
if /I "%ARCH%"=="x64" (
  set "SET_CL_ARCH="
) else (
  set "SET_CL_ARCH=1"
)

rem Use shared Python module for VS path detection (jptools/vs_utils.py)
rem This ensures consistency with scons_jp.py and runJpSmokeTests.ps1
rem Note: %~dp0 is jptools/ directory, so find_vcvars.py is in the same directory
set "FOUND="
for /f "delims=" %%P in ('python "%~dp0find_vcvars.py" %ARCH% 2^>nul') do (
  set "FOUND=%%P"
)

if not defined FOUND (
  rem Fallback to direct search if Python call fails
  if /I "%ARCH%"=="x64" (
    set "VCVARS=vcvars64.bat"
  ) else (
    set "VCVARS=vcvars32.bat"
  )
  for %%E in (BuildTools Community Professional Enterprise) do (
    if not defined FOUND (
      if exist "%ProgramFiles%\Microsoft Visual Studio\2022\%%E\VC\Auxiliary\Build\%VCVARS%" (
        set "FOUND=%ProgramFiles%\Microsoft Visual Studio\2022\%%E\VC\Auxiliary\Build\%VCVARS%"
      )
    )
  )
)

if not defined FOUND (
  echo [ERROR] Could not locate Visual Studio 2022 vcvars script for %ARCH%>&2
  exit /b 1
)

echo [vcsetup] Using: "%FOUND%"
call "%FOUND%"
if defined SET_CL_ARCH (
  SET CL=/arch:IA32
)
echo [vcsetup] after vcvars

:done
exit /b 0
