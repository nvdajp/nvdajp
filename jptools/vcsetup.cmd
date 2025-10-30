@echo off
rem Setup MSVC build environment persistently. Usage: vcsetup.cmd [x64|x86]
rem Defaults to x86.

set "ARCH=%~1"
if /I "%ARCH%"=="x64" (
  set "VCVARS=vcvars64.bat"
  set "VS2015_ARG=amd64"
) else (
  set "VCVARS=vcvars32.bat"
  set "VS2015_ARG=x86"
)

set "FOUND="
set "NEED_ARCH_ARG="

rem VS 2022
for %%E in (BuildTools Community Professional Enterprise) do if not defined FOUND if exist "%ProgramFiles%\Microsoft Visual Studio\2022\%%E\VC\Auxiliary\Build\%VCVARS%" (
  set "FOUND=%ProgramFiles%\Microsoft Visual Studio\2022\%%E\VC\Auxiliary\Build\%VCVARS%"
  set "NEED_ARCH_ARG="
)

rem VS 2019
if not defined FOUND for %%E in (BuildTools Community Professional Enterprise) do if not defined FOUND if exist "%ProgramFiles(x86)%\Microsoft Visual Studio\2019\%%E\VC\Auxiliary\Build\%VCVARS%" (
  set "FOUND=%ProgramFiles(x86)%\Microsoft Visual Studio\2019\%%E\VC\Auxiliary\Build\%VCVARS%"
  set "NEED_ARCH_ARG="
)

rem VS 2017
if not defined FOUND for %%E in (BuildTools Community Professional Enterprise) do if not defined FOUND if exist "%ProgramFiles(x86)%\Microsoft Visual Studio\2017\%%E\VC\Auxiliary\Build\%VCVARS%" (
  set "FOUND=%ProgramFiles(x86)%\Microsoft Visual Studio\2017\%%E\VC\Auxiliary\Build\%VCVARS%"
  set "NEED_ARCH_ARG="
)

rem VS 2015 fallbacks
if not defined FOUND if /I "%VCVARS%"=="vcvars32.bat" if exist "%ProgramFiles(x86)%\Microsoft Visual Studio 14.0\VC\bin\vcvars32.bat" (
  set "FOUND=%ProgramFiles(x86)%\Microsoft Visual Studio 14.0\VC\bin\vcvars32.bat"
  set "NEED_ARCH_ARG="
)
if not defined FOUND if exist "%ProgramFiles(x86)%\Microsoft Visual Studio 14.0\VC\vcvarsall.bat" (
  set "FOUND=%ProgramFiles(x86)%\Microsoft Visual Studio 14.0\VC\vcvarsall.bat"
  set "NEED_ARCH_ARG=1"
)

if not defined FOUND (
  echo [ERROR] Could not locate Visual Studio vcvars script for %ARCH%>&2
  exit /b 1
)

echo [vcsetup] Using: "%FOUND%"

if defined NEED_ARCH_ARG (
  call "%FOUND%" %VS2015_ARG%
) else (
  call "%FOUND%"
)

echo [vcsetup] after vcvars

exit /b 0
