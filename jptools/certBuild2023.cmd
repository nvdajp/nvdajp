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

rem Auto-detect a valid code signing cert from Windows cert store when not explicitly specified
rem Preference: CurrentUser\My, then LocalMachine\My. Exclude self-signed.
rem Skip certificate detection if SKIP_SIGNING is set
if not defined SKIP_SIGNING if not defined CERT_SHA1 if not defined CERT_NAME (
    for /f "usebackq tokens=1,2 delims=;" %%A in (`pwsh -NoProfile -Command ^
        "$now=Get-Date; "^ 
        "function FindCert([string]\$root){ "^ 
        "  Get-ChildItem -Path \$root -ErrorAction SilentlyContinue | Where-Object { "^ 
        "    \$_.HasPrivateKey -and \$_.NotAfter -gt \$now -and \$_.NotBefore -le \$now -and "^ 
        "    (\$_.EnhancedKeyUsageList | Where-Object { \$_.ObjectId -eq '1.3.6.1.5.5.7.3.3' }) -and "^ 
        "    \$_.Issuer -ne \$_.Subject "^ 
        "  } | Sort-Object NotAfter -Descending | Select-Object -First 1 "^ 
        "}; "^ 
        "\$cert=FindCert 'Cert:\\CurrentUser\\My'; \$scope='USER'; if(-not \$cert){ \$cert=FindCert 'Cert:\\LocalMachine\\My'; \$scope='MACHINE' } ; "^ 
        "if(\$cert){ \$tp=(\$cert.Thumbprint -replace ' ','').ToUpper(); if(\$tp -match '^[0-9A-F]{40}$'){ Write-Output (\"\$scope;\" + \$tp) } } "
    `) do (
        set "_CERT_SCOPE=%%A"
        set "_CERT_THUMB=%%B"
    )
    if defined _CERT_THUMB (
        set CERT_STORE=My
        set CERT_SHA1=!_CERT_THUMB!
        if /I "!_CERT_SCOPE!"=="MACHINE" set CERT_MACHINE_STORE=1
        echo Using certificate from store: scope=!_CERT_SCOPE! sha1=!_CERT_THUMB!
    ) else (
        echo [INFO] No suitable code signing certificate found in store.
    )
    set _CERT_SCOPE=
    set _CERT_THUMB=
)

rem Validate CERT_SHA1 (must be exactly 40 hex chars). If invalid, clear it.
if defined CERT_SHA1 (
    for /f "usebackq delims=" %%V in (`pwsh -NoProfile -Command ^
        "$v=$env:CERT_SHA1; if($v -match '^[0-9A-Fa-f]{40}$'){ 'OK' }"`) do set "__SHA1_OK=%%V"
    if not defined __SHA1_OK (
        echo [WARN] Ignoring invalid CERT_SHA1 value: %CERT_SHA1%
        set CERT_SHA1=
    )
    set __SHA1_OK=
)

rem Build SCons args; enable signing only when a valid store cert is selected
rem Note: Do not set certFile=1 for certificate store signing (JP-specific)
rem SConstruct will detect CERT_SHA1/CERT_NAME from environment and use certificate store signing
set SCONSARGS=release=%RELEASE% publisher=%PUBLISHER% version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% %SCONSOPTIONS%
if defined CERT_SHA1 set SCONSARGS=%SCONSARGS% certTimestampServer=%TIMESTAMP_URL%
if defined CERT_NAME if not defined CERT_SHA1 set SCONSARGS=%SCONSARGS% certTimestampServer=%TIMESTAMP_URL%
if not defined SKIP_SIGNING if not defined CERT_SHA1 if not defined CERT_NAME if not defined ALLOW_AUTO_SIGN (
    echo [ERROR] No valid code signing certificate found. Set CERT_SHA1 or CERT_NAME, or set ALLOW_AUTO_SIGN=1 to allow automatic selection.
    goto onerror
)
rem Build synthDriverHost32 runtime (32-bit Python for SAPI4/5) before launcher
powershell -ExecutionPolicy Bypass -File jptools\buildSynthDriverHost32.ps1
@if not "%ERRORLEVEL%"=="0" goto onerror
rem Build launcher (final target)
rem Note: we only invoke the "launcher" target here and rely on the SCons dependency chain
rem (launcher -> dist -> source -> jtalkSync -> jtalkPrep, and launcher -> jpCertExtras)
rem to run intermediate targets such as jtalkSync and jtalkPrep. This reduces redundant
rem scons.bat invocations and jtalkSync executions, but assumes that SCons' dependency
rem tracking is correctly configured; this script does not independently verify that
rem jtalkSync actually executed.
call scons.bat launcher %SCONSARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror
rem Run JP smoke tests (JpBrailleTests and JtalkTests) after the launcher build completes
rem Note: the launcher build ensures jtalkSync runs via its dependency chain when needed, so DLLs
rem and dictionaries should be up to date
powershell -ExecutionPolicy Bypass -File jptools\runJpSmokeTests.ps1 -SkipInstall -SkipOverlay
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
