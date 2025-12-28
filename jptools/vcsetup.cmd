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
  set "VCVARS=vcvars64.bat"
  set "SET_CL_ARCH="
) else (
  set "VCVARS=vcvars32.bat"
  set "SET_CL_ARCH=1"
)

set "FOUND="

rem VS 2022: Search in BuildTools, Community, Professional, Enterprise order
for %%E in (BuildTools Community Professional Enterprise) do (
  if not defined FOUND (
    if exist "%ProgramFiles%\Microsoft Visual Studio\2022\%%E\VC\Auxiliary\Build\%VCVARS%" (
      set "FOUND=%ProgramFiles%\Microsoft Visual Studio\2022\%%E\VC\Auxiliary\Build\%VCVARS%"
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
