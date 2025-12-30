@echo off
rem Setup MSVC build environment persistently. Usage: vcsetup.cmd [x64|x86]
rem Defaults to x86.
rem Currently supports Visual Studio 2022 only.

rem #region agent log
python "%~dp0debug_log.py" "debug-session" "run1" "A" "vcsetup.cmd:6" "vcsetup.cmd entry" "{\"arch\":\"%~1\"}" >nul 2>&1
rem #endregion

set "ARCH=%~1"
if /I "%ARCH%"=="x64" (
  set "SET_CL_ARCH="
  rem For x64 builds, always set up environment to ensure x64 tools are used
  rem (x86 cl might be available from previous x86 build)
  goto :setup_vcvars
)

set "SET_CL_ARCH=1"
rem Fast path for x86: check if both cl and nmake are already available
rem Note: Use "call :check_tool" pattern to correctly capture ERRORLEVEL
rem because python logging calls reset ERRORLEVEL

cl >nul 2>&1
if ERRORLEVEL 9009 goto :cl_not_found
rem #region agent log
python "%~dp0debug_log.py" "debug-session" "run1" "A" "vcsetup.cmd:20" "cl found, checking nmake" "{}" >nul 2>&1
rem #endregion

nmake /? >nul 2>&1
if ERRORLEVEL 9009 goto :nmake_not_found
rem #region agent log
python "%~dp0debug_log.py" "debug-session" "run1" "A" "vcsetup.cmd:25" "Fast path: both cl and nmake available" "{}" >nul 2>&1
rem #endregion
goto :done

:cl_not_found
rem #region agent log
python "%~dp0debug_log.py" "debug-session" "run1" "A" "vcsetup.cmd:30" "Fast path failed: cl not found" "{}" >nul 2>&1
rem #endregion
goto :setup_vcvars

:nmake_not_found
rem #region agent log
python "%~dp0debug_log.py" "debug-session" "run1" "A" "vcsetup.cmd:35" "Fast path failed: nmake not found" "{}" >nul 2>&1
rem #endregion
goto :setup_vcvars

:setup_vcvars

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
rem #region agent log
python "%~dp0debug_log.py" "debug-session" "run1" "A,B" "vcsetup.cmd:63" "Before vcvars call" "{\"found\":\"%FOUND%\",\"path\":\"%PATH%\"}" >nul 2>&1
rem #endregion
rem Call vcvars script with full path (call command handles spaces correctly)
rem Show output for debugging (remove >nul 2>&1 to see errors)
call "%FOUND%" 2>&1
set "VCVARS_EXIT=%ERRORLEVEL%"
rem #region agent log
python "%~dp0debug_log.py" "debug-session" "run1" "A,B" "vcsetup.cmd:67" "After vcvars call" "{\"exit_code\":\"%VCVARS_EXIT%\",\"path\":\"%PATH%\"}" >nul 2>&1
rem #endregion
rem #region agent log
python "%~dp0debug_log.py" "debug-session" "run1" "F" "vcsetup.cmd:99" "Before VCVARS_EXIT check" "{\"vcvars_exit\":\"%VCVARS_EXIT%\"}" >nul 2>&1
rem #endregion
if "%VCVARS_EXIT%" neq "0" (
  echo [ERROR] Failed to execute vcvars script: "%FOUND%" (exit code: %VCVARS_EXIT%) >&2
  rem #region agent log
  python "%~dp0debug_log.py" "debug-session" "run1" "F" "vcsetup.cmd:104" "VCVARS_EXIT neq 0, exiting with error" "{\"vcvars_exit\":\"%VCVARS_EXIT%\"}" >nul 2>&1
  rem #endregion
  exit /b 1
)
rem #region agent log
python "%~dp0debug_log.py" "debug-session" "run1" "F" "vcsetup.cmd:109" "VCVARS_EXIT check passed" "{\"vcvars_exit\":\"%VCVARS_EXIT%\"}" >nul 2>&1
rem #endregion
rem Verify nmake is available after vcvars
rem #region agent log
python "%~dp0debug_log.py" "debug-session" "run1" "D" "vcsetup.cmd:73" "Before nmake check" "{\"path\":\"%PATH%\"}" >nul 2>&1
rem #endregion
nmake /? >nul 2>&1
set "NMAKE_CHECK=%ERRORLEVEL%"
rem #region agent log
python "%~dp0debug_log.py" "debug-session" "run1" "D" "vcsetup.cmd:74" "After nmake check" "{\"exit_code\":\"%NMAKE_CHECK%\",\"path\":\"%PATH%\"}" >nul 2>&1
rem #endregion
if "%NMAKE_CHECK%" equ "9009" (
  echo [ERROR] nmake not found after vcvars execution. PATH may not be set correctly. >&2
  rem #region agent log
  python "%~dp0debug_log.py" "debug-session" "run1" "C,D,E" "vcsetup.cmd:75" "nmake not found error" "{\"path\":\"%PATH%\"}" >nul 2>&1
  rem #endregion
  exit /b 1
)
if defined SET_CL_ARCH (
  SET CL=/arch:IA32
)
echo [vcsetup] after vcvars
rem #region agent log
python "%~dp0debug_log.py" "debug-session" "run1" "C" "vcsetup.cmd:81" "vcsetup.cmd exit" "{\"path\":\"%PATH%\",\"cl\":\"%CL%\"}" >nul 2>&1
rem #endregion

:done
rem #region agent log
python "%~dp0debug_log.py" "debug-session" "run1" "A" "vcsetup.cmd:84" "vcsetup.cmd done (fast path)" "{\"path\":\"%PATH%\"}" >nul 2>&1
rem #endregion
exit /b 0
