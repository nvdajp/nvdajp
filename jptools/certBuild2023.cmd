setlocal enableextensions enabledelayedexpansion
set SCONSOPTIONS=%*
if not defined SCONSOPTIONS (
    set SCONSOPTIONS=version_build=1 --all-cores
)
echo SCONSOPTIONS is %SCONSOPTIONS%

if "%NOWDATE%"=="" set NOWDATE=250101a
echo NOWDATE is %NOWDATE%
if "%VERSION%"=="" set VERSION=jpalpha_%NOWDATE%
echo VERSION is %VERSION%
if "%UPDATEVERSIONTYPE%"=="" set UPDATEVERSIONTYPE=nvdajpalpha
echo UPDATEVERSIONTYPE is %UPDATEVERSIONTYPE%
if "%PUBLISHER%"=="" set PUBLISHER=nvdajp
echo PUBLISHER is %PUBLISHER%
if "%RELEASE%"=="" set RELEASE=1
echo RELEASE is %RELEASE%

rem Timestamp server (override via env if needed)
if defined TIMESERVER if not defined TIMESTAMP_URL set TIMESTAMP_URL=%TIMESERVER%
if not defined TIMESTAMP_URL set TIMESTAMP_URL=http://timestamp.digicert.com

cd /d %~dp0
cd ..

call jptools\vcsetup.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror

call jptools\check_vs_version.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror

nmake /?
@if not "%ERRORLEVEL%"=="0" goto onerror

patch -v
@if not "%ERRORLEVEL%"=="0" goto onerror

rem Ensure signtool is discoverable for SCons (verify/sign)
if not defined SIGNTOOL (
    for /f "usebackq delims=" %%S in (`where signtool 2^>NUL`) do set "SIGNTOOL=%%S"
)
if not defined SIGNTOOL (
    for /f "usebackq delims=" %%D in (`pwsh -NoProfile -Command "$base='C:\\Program Files (x86)\\Windows Kits\\10\\bin'; if(Test-Path $base){ Get-ChildItem $base -Directory | Sort-Object Name -Descending | ForEach-Object { $p=Join-Path $_.FullName 'x64\signtool.exe'; if(Test-Path $p){ $p; break }; $p=Join-Path $_.FullName 'x86\signtool.exe'; if(Test-Path $p){ $p; break } } }"`) do set "SIGNTOOL=%%D"
)
if not defined SIGNTOOL (
    echo [WARN] signtool not found in PATH or Windows Kits. Verification may be skipped.
)

set SCONSARGS=release=%RELEASE% publisher=%PUBLISHER% certFile=1 certTimestampServer=%TIMESTAMP_URL% version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% %SCONSOPTIONS%
call scons.bat jtalkPrep miscdepsjp jpCertExtras %SCONSARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror
call scons.bat source user_docs launcher jpAddons nvdaHelper\client jpStageControllerClient jpControllerClient %SCONSARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror
call scons.bat jpVerifySignatures %SCONSARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror

set PYTHONUTF8=1
call jptools\tests.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror
call jpchar\tests.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror

echo %UPDATEVERSIONTYPE% %VERSION%
exit /b 0

:onerror
echo nvdajp build error %ERRORLEVEL%
@if "%PAUSE%"=="1" pause
exit /b -1
