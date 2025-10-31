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

rem Auto-detect a valid code signing cert from Windows cert store when not explicitly specified
rem Preference: CurrentUser\My, then LocalMachine\My. Exclude self-signed.
if not defined CERT_SHA1 if not defined CERT_NAME (
    for /f "usebackq tokens=1,2" %%A in (`pwsh -NoProfile -Command ^
        "$now=Get-Date; "^
        "function FindCert([string]\$root){ "^
        "  Get-ChildItem -Path \$root -ErrorAction SilentlyContinue | Where-Object { "^
        "    \$_.HasPrivateKey -and \$_.NotAfter -gt \$now -and \$_.NotBefore -le \$now -and "^
        "    (\$_.EnhancedKeyUsageList | Where-Object { \$_.ObjectId -eq '1.3.6.1.5.5.7.3.3' }) -and "^
        "    \$_.Issuer -ne \$_.Subject "^
        "  } | Sort-Object NotAfter -Descending | Select-Object -First 1 "^
        "}; "^
        "\$cert=FindCert 'Cert:\\CurrentUser\\My'; \$scope='USER'; if(-not \$cert){ \$cert=FindCert 'Cert:\\LocalMachine\\My'; \$scope='MACHINE' } ; "^
        "if(\$cert){ Write-Output (\"\$scope \" + (\$cert.Thumbprint -replace ' ','').ToUpper()) } "
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

rem Build SCons args; enable signing only when a valid store cert is selected
set SCONSARGS=release=%RELEASE% publisher=%PUBLISHER% version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% %SCONSOPTIONS%
if defined CERT_SHA1 set SCONSARGS=%SCONSARGS% certFile=1 certTimestampServer=%TIMESTAMP_URL%
if defined CERT_NAME if not defined CERT_SHA1 set SCONSARGS=%SCONSARGS% certFile=1 certTimestampServer=%TIMESTAMP_URL%
if not defined CERT_SHA1 if not defined CERT_NAME if not defined ALLOW_AUTO_SIGN (
    echo [ERROR] No valid code signing certificate found. Set CERT_SHA1 or CERT_NAME, or set ALLOW_AUTO_SIGN=1 to allow automatic selection.
    goto onerror
)
call scons.bat jtalkPrep miscdepsjp jpCertExtras %SCONSARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror
call scons.bat source user_docs launcher jpAddons nvdaHelper\client jpStageControllerClient jpControllerClient %SCONSARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror
call scons.bat jpVerifySignatures %SCONSARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror

set PYTHONUTF8=1
call scons.bat jp_tests %SCONSARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror

echo %UPDATEVERSIONTYPE% %VERSION%
exit /b 0

:onerror
echo nvdajp build error %ERRORLEVEL%
@if "%PAUSE%"=="1" pause
exit /b -1
