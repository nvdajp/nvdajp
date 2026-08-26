setlocal enableextensions enabledelayedexpansion
set SCONSOPTIONS=%*
echo SCONSOPTIONS is %SCONSOPTIONS%

rem Build architecture (default to x64)
rem BUILD_ARCH is JP-specific environment variable for smoke test environment switching and MSVC setup
rem TARGET_ARCH is SCons environment variable and should not be set as OS environment variable
if not defined BUILD_ARCH set BUILD_ARCH=x64
echo BUILD_ARCH is %BUILD_ARCH%

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

rem Set Python UTF-8 mode for all Python commands (needed for JP tests and smoke tests)
set PYTHONUTF8=1

rem MeCab dictionary is built with CP932 (jtalkSync / dicrc). Match CI (testAndPublish.yml):
rem use console code page 932 so MeCab DLL path handling matches dictionary build.
rem PowerShell 7 defaults to UTF-8 (65001) and can break translator2 smoke tests without this.
chcp 932 >nul 2>&1

rem Timestamp server (override via env if needed)
rem Note: HTTP (not HTTPS) is intentional:
rem - Microsoft Authenticode spec uses HTTP 1.1 POST for timestamp requests
rem - Only hash values are sent (not original data), so encryption is less critical
rem - HTTP has lower overhead and better compatibility with existing tools
if defined TIMESERVER if not defined TIMESTAMP_URL set TIMESTAMP_URL=%TIMESERVER%
if not defined TIMESTAMP_URL set TIMESTAMP_URL=http://timestamp.digicert.com

cd /d %~dp0
cd ..

call jptools\vcsetup.cmd %BUILD_ARCH%
@if not "%ERRORLEVEL%"=="0" goto onerror

call jptools\check_vs_version.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror

nmake /?
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

rem Azure Key Vault signing is the default and only supported signing method.
rem Local certificate store signing (CERT_SHA1 / eToken) is retired.
if not defined AZURE_KV_SIGNING set AZURE_KV_SIGNING=1
echo Using Azure Key Vault code signing ^(AZURE_KV_SIGNING=%AZURE_KV_SIGNING%^)

rem Build SCons args; signing is driven by AZURE_KV_SIGNING (see scons_jp.py / SConstruct).
rem Note: Do not set certFile=1 for certificate store signing (JP-specific)
set SCONSARGS=release=%RELEASE% publisher=%PUBLISHER% version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% %SCONSOPTIONS%
if defined SKIP_SIGNING goto cert_signing_ready
if not "%AZURE_KV_SIGNING%"=="0" goto cert_signing_ready
echo [ERROR] Azure Key Vault signing is required (set AZURE_KV_SIGNING=1), or SKIP_SIGNING=1 to skip signing.
goto onerror
:cert_signing_ready
rem Build synthDriverHost32 runtime (32-bit Python for SAPI4/5) before launcher
powershell -ExecutionPolicy Bypass -File jptools\buildSynthDriverHost32.ps1
@if not "%ERRORLEVEL%"=="0" goto onerror
rem Force a clean JTalk dictionary rebuild before dist/launcher (match CI testAndPublish.yml).
rem dist copies sourceDir at build time; rebuilding after launcher would leave stale dic in the installer.
chcp 932 >nul 2>&1 && powershell -ExecutionPolicy Bypass -File jptools\forceJtalkDictionaryRebuild.ps1
@if not "%ERRORLEVEL%"=="0" goto onerror
chcp 932 >nul 2>&1 && powershell -ExecutionPolicy Bypass -File jptools\verifyJtalkDictionary.ps1
@if not "%ERRORLEVEL%"=="0" goto onerror
rem Build launcher (final target)
rem Note: dist copies sourceDir after jtalkSync; dictionary rebuild above ensures packaged dic is fresh.
call scons.bat launcher %SCONSARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror
rem Run JP smoke tests (JpBrailleTests and JtalkTests) after dictionary verify
chcp 932 >nul 2>&1 && powershell -ExecutionPolicy Bypass -File jptools\runJpSmokeTests.ps1 -SkipInstall -SkipOverlay
@if not "%ERRORLEVEL%"=="0" goto onerror
if not defined SKIP_SIGNING (
    call scons.bat jpVerifySignatures %SCONSARGS%
    @if not "%ERRORLEVEL%"=="0" goto onerror
) else (
    echo [INFO] Skipping signature verification (SKIP_SIGNING is set)
)
rem Build JP addons and controller client (independent from launcher)
call scons.bat jpAddons nvdaHelper\client jpStageControllerClient jpControllerClient %SCONSARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror
rem Run JP tests (dictionary and char description tests)
call scons.bat jp_tests %SCONSARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror

echo %UPDATEVERSIONTYPE% %VERSION%
exit /b 0

:onerror
echo nvdajp build error %ERRORLEVEL%
@if "%PAUSE%"=="1" pause
exit /b -1
