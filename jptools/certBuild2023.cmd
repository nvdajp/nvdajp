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

cd miscDepsJp\jptools
call copy_jtalk_core_files.cmd
call build-and-test.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror
cd ..\..

call jptools\setupMiscDepsJp.cmd

rem Resolve signtool path (allow override)
if not defined SIGNTOOL set SIGNTOOL=C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe

rem Build signing args similar to NVDA build\prepare.cmd
if not defined CERT_STORE set CERT_STORE=My
set "SIGN_ARGS=/fd SHA256 /td SHA256 /tr !TIMESTAMP_URL!"

rem Prefer specific certificate by SHA1 or Name; else try auto-detect a valid trusted code signing cert
if defined CERT_SHA1 (
    set "SIGN_ARGS=!SIGN_ARGS! /s !CERT_STORE! /sha1 !CERT_SHA1!"
    if defined CERT_MACHINE_STORE set "SIGN_ARGS=!SIGN_ARGS! /sm"
) else if defined CERT_NAME (
    set "SIGN_ARGS=!SIGN_ARGS! /s !CERT_STORE! /n !CERT_NAME!"
    if defined CERT_MACHINE_STORE set "SIGN_ARGS=!SIGN_ARGS! /sm"
) else (
    for /f "usebackq delims=" %%T in (`pwsh -NoProfile -Command "$stores=@('Cert:\\CurrentUser\\My','Cert:\\LocalMachine\\My'); $c=Get-ChildItem $stores -CodeSigningCert -ErrorAction SilentlyContinue | Where-Object { $_.HasPrivateKey -and $_.NotBefore -lt (Get-Date) -and $_.NotAfter -gt (Get-Date) } | Sort-Object NotAfter -Descending; if(-not $c){ exit 2 }; $chain=New-Object System.Security.Cryptography.X509Certificates.X509Chain; $chain.ChainPolicy.RevocationMode='NoCheck'; $chain.ChainPolicy.RevocationFlag='EntireChain'; $chain.ChainPolicy.VerificationFlags='NoFlag'; $chosen=$null; foreach($cert in $c){ if($chain.Build($cert)){ $chosen=$cert; break } }; if($null -eq $chosen){ exit 3 }; $chosen.Thumbprint.Replace(' ','')"`) do set "CERT_SHA1=%%T"
    if not defined CERT_SHA1 (
        echo [ERROR] No trusted code signing certificate detected.>&2
        echo         Set CERT_SHA1 or CERT_NAME to select the correct certificate.>&2
        goto onerror
    )
    set "SIGN_ARGS=!SIGN_ARGS! /s !CERT_STORE! /sha1 !CERT_SHA1!"
)

rem Ensure /sm is set if CERT_MACHINE_STORE requested
if defined CERT_MACHINE_STORE (
    echo !SIGN_ARGS! | findstr /i /c:" /sm" >nul || set "SIGN_ARGS=!SIGN_ARGS! /sm"
)

echo Using signtool: %SIGNTOOL%
if defined CERT_SHA1 echo Using certificate (SHA1): !CERT_SHA1!
if defined CERT_NAME echo Using certificate (Name): !CERT_NAME!
echo Timestamp: !TIMESTAMP_URL!

call :sign_one source\synthDrivers\jtalk\libmecab.dll
@if not "%ERRORLEVEL%"=="0" goto onerror

call :sign_one source\synthDrivers\jtalk\libopenjtalk.dll
@if not "%ERRORLEVEL%"=="0" goto onerror

call :sign_one miscDeps\python\brlapi-0.8.dll
@if not "%ERRORLEVEL%"=="0" goto onerror

call :sign_one miscDeps\python\libgcc_s_dw2-1.dll
@if not "%ERRORLEVEL%"=="0" goto onerror

call :sign_one miscDeps\source\brailleDisplayDrivers\lilli.dll
@if not "%ERRORLEVEL%"=="0" goto onerror

call :sign_one .venv\Lib\site-packages\wx\wxbase32u_net_vc140.dll
@if not "%ERRORLEVEL%"=="0" goto onerror

call :sign_one .venv\Lib\site-packages\wx\wxbase32u_vc140.dll
@if not "%ERRORLEVEL%"=="0" goto onerror

call :sign_one .venv\Lib\site-packages\wx\wxmsw32u_core_vc140.dll
@if not "%ERRORLEVEL%"=="0" goto onerror

call :sign_one .venv\Lib\site-packages\wx\wxmsw32u_html_vc140.dll
@if not "%ERRORLEVEL%"=="0" goto onerror

call :sign_one .venv\Lib\site-packages\wx\wxmsw32u_stc_vc140.dll
@if not "%ERRORLEVEL%"=="0" goto onerror

set SCONSARGS=certFile=1 certTimestampServer=%TIMESTAMP_URL% version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% %SCONSOPTIONS%

call scons.bat source user_docs launcher release=%RELEASE% publisher=%PUBLISHER% %SCONSARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror

cd jptools
call pack_jtalk_addon.cmd
call pack_kgs_addon.cmd
cd ..
call jptools\buildControllerClient.cmd %SCONSARGS%
set PYTHONUTF8=1
call jptools\tests.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror
call jpchar\tests.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror

set VERIFYLOG=output\nvda_%VERSION%_verify.log
del /Q %VERIFYLOG%

"%SIGNTOOL%" verify /pa output\*.exe >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror

for /r "dist" %%i in (*.dll *.exe) do (
    "%SIGNTOOL%" verify /pa "%%i" >> %VERIFYLOG%
    @if not "%ERRORLEVEL%"=="0" goto onerror
)
for /r "dist\synthDrivers\jtalk" %%i in (*.dll *.exe) do (
    "%SIGNTOOL%" verify /pa "%%i" >> %VERIFYLOG%
    @if not "%ERRORLEVEL%"=="0" goto onerror
)
for /r "dist\lib" %%i in (*.dll *.exe) do (
    "%SIGNTOOL%" verify /pa "%%i" >> %VERIFYLOG%
    @if not "%ERRORLEVEL%"=="0" goto onerror
)
for /r "dist\lib64" %%i in (*.dll *.exe) do (
    "%SIGNTOOL%" verify /pa "%%i" >> %VERIFYLOG%
    @if not "%ERRORLEVEL%"=="0" goto onerror
)
for /r "dist\libArm64" %%i in (*.dll *.exe) do (
    "%SIGNTOOL%" verify /pa "%%i" >> %VERIFYLOG%
    @if not "%ERRORLEVEL%"=="0" goto onerror
)

echo %UPDATEVERSIONTYPE% %VERSION%
exit /b 0

:onerror
echo nvdajp build error %ERRORLEVEL%
@if "%PAUSE%"=="1" pause
exit /b -1

rem Subroutine: sign one file with retries and pause
:sign_one
setlocal enableextensions enabledelayedexpansion
set "_FILE=%~1"
if not exist "%_FILE%" (
    echo [ERROR] File not found: %_FILE%>&2
    endlocal & exit /b 1
)
set "_TRIES=0"
:_try_sign
set /a _TRIES+=1 >nul
echo Signing "!_FILE!" (try !_TRIES!)
"%SIGNTOOL%" sign !SIGN_ARGS! "!_FILE!"
if "%ERRORLEVEL%"=="0" (
    timeout /T 5 /NOBREAK >nul
    endlocal & exit /b 0
)
if %_TRIES% LSS 3 (
    timeout /T 1 /NOBREAK >nul
    goto _try_sign
)
echo [ERROR] signtool sign failed for %_FILE%>&2
endlocal & exit /b 1
