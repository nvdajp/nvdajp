@echo off
rem Setup MSVC build environment persistently. Usage: vcsetup.cmd [x64|x86]
rem Defaults to x86.
rem Currently supports Visual Studio 2022 only.

set "ARCH=%~1"
if /I "%ARCH%"=="x64" (
  set "SET_CL_ARCH="
  rem For x64 builds, always set up environment to ensure x64 tools are used
  rem (x86 cl might be available from previous x86 build)
  goto :setup_vcvars
)

set "SET_CL_ARCH=1"
rem Fast path for x86: check if both cl and nmake are already available
cl >nul 2>&1
if ERRORLEVEL 9009 goto :cl_not_found

nmake /? >nul 2>&1
if ERRORLEVEL 9009 goto :nmake_not_found
goto :done

:cl_not_found
goto :setup_vcvars

:nmake_not_found
goto :setup_vcvars

:setup_vcvars

if /I "%ARCH%"=="x64" (
  set "VCVARS=vcvars64.bat"
) else (
  set "VCVARS=vcvars32.bat"
)

rem Use shared Python module for VS path detection (jptools/vs_utils.py)
rem This ensures consistency with scons_jp.py and runJpSmokeTests.ps1
rem Note: %~dp0 is jptools/ directory, so find_vcvars.py is in the same directory
set "FOUND="
rem Try to use Python from virtual environment if available (.venv\Scripts\python.exe)
if exist "%~dp0..\.venv\Scripts\python.exe" (
  for /f "delims=" %%P in ('"%~dp0..\.venv\Scripts\python.exe" "%~dp0find_vcvars.py" %ARCH% 2^>nul') do (
    set "FOUND=%%P"
  )
)
rem Fallback to system Python if virtual environment Python failed
if not defined FOUND (
  for /f "delims=" %%P in ('python "%~dp0find_vcvars.py" %ARCH% 2^>nul') do (
    set "FOUND=%%P"
  )
)

if not defined FOUND (
  rem Fallback to direct search if Python call fails
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
rem Call vcvars script with full path (call command handles spaces correctly)
rem Show output for debugging (remove >nul 2>&1 to see errors)
call "%FOUND%" 2>&1
set "VCVARS_EXIT=%ERRORLEVEL%"
rem Use goto-based conditional to avoid () block variable expansion issues with enabledelayedexpansion
if "%VCVARS_EXIT%" equ "0" goto :vcvars_exit_ok
echo [ERROR] Failed to execute vcvars script: "%FOUND%" (exit code: %VCVARS_EXIT%) >&2
exit /b 1
:vcvars_exit_ok
rem Verify nmake is available after vcvars
nmake /? >nul 2>&1
set "NMAKE_CHECK=%ERRORLEVEL%"
rem Use goto-based conditional to avoid () block variable expansion issues
if "%NMAKE_CHECK%" neq "9009" goto :nmake_check_ok
echo [ERROR] nmake not found after vcvars execution. PATH may not be set correctly. >&2
exit /b 1
:nmake_check_ok
if defined SET_CL_ARCH (
  SET CL=/arch:IA32
)
echo [vcsetup] after vcvars

:done
exit /b 0
