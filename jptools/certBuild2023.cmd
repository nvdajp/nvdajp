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

rem Change to script directory (also switches drive)
cd /d %~dp0
rem Then go up to repository root
cd ..

rem Resolve signtool path (allow override)
if not defined SIGNTOOL set SIGNTOOL=C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe

rem JP PATCH: store certificate only (PFX unsupported). Ensure CERT_STORE default.
if not defined CERT_STORE set CERT_STORE=My

rem Prefer specific certificate by SHA1; else try auto-detect a valid trusted code signing cert
if not defined CERT_SHA1 if not defined CERT_NAME (
    for /f "usebackq delims=" %%T in (`pwsh -NoProfile -Command "$stores=@('Cert:\\CurrentUser\\My','Cert:\\LocalMachine\\My'); $c=Get-ChildItem $stores -CodeSigningCert -ErrorAction SilentlyContinue | Where-Object { $_.HasPrivateKey -and $_.NotBefore -lt (Get-Date) -and $_.NotAfter -gt (Get-Date) } | Sort-Object NotAfter -Descending; if(-not $c){ exit 2 }; $chain=New-Object System.Security.Cryptography.X509Certificates.X509Chain; $chain.ChainPolicy.RevocationMode='NoCheck'; $chain.ChainPolicy.RevocationFlag='EntireChain'; $chain.ChainPolicy.VerificationFlags='NoFlag'; $chosen=$null; foreach($cert in $c){ if($chain.Build($cert)){ $chosen=$cert; break } }; if($null -eq $chosen){ exit 3 }; $chosen.Thumbprint.Replace(' ','')"`) do set "CERT_SHA1=%%T"
    if not defined CERT_SHA1 (
        echo [ERROR] No trusted code signing certificate detected.>&2
        echo         Set CERT_SHA1 or CERT_NAME to select the correct certificate.>&2
        goto onerror
    )
)

echo Using signtool: %SIGNTOOL%
if defined CERT_SHA1 echo Using certificate (SHA1): !CERT_SHA1!
if defined CERT_NAME echo Using certificate (Name): !CERT_NAME!
echo Timestamp: !TIMESTAMP_URL!

set SCONSARGS=certFile=1 certTimestampServer=%TIMESTAMP_URL% version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% %SCONSOPTIONS%

rem JP PATCH: call SCons targets (JP additions included)
rem Ensure jtalk (libopenjtalk.dll) is built and JP overlay is applied
py -3 jptools\nonCertBuild.py --prep-only
@if not "%ERRORLEVEL%"=="0" echo [WARN] JP prep-only failed (%ERRORLEVEL%), continuing with fallback

rem Fallback: if libopenjtalk.dll was not produced, deploy prebuilt one
if not exist miscDepsJp\source\synthDrivers\jtalk\libopenjtalk.dll (
    if exist miscDepsJp\include\python-jtalk\libopenjtalk.dll (
        copy /Y miscDepsJp\include\python-jtalk\libopenjtalk.dll miscDepsJp\source\synthDrivers\jtalk\libopenjtalk.dll >nul
    )
)
rem Ensure overlay reflects the fallback copy as well
call scons.bat -Q miscdepsjp

call scons.bat certprep source user_docs launcher controllerClient jtalkAddon kgsAddon jpTests jpCharTests release=%RELEASE% publisher=%PUBLISHER% %SCONSARGS%
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
