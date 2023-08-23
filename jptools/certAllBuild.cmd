set SCONSOPTIONS=%*

if "%APPVEYOR_PROJECT_SLUG%"=="nvdajp" (
    echo appveyor build
    set PFX=jptools\secret\shuaruta-key220824.pfx
    set PWFILE=jptools\secret\shuaruta-key-pass-2022.txt
    for /F "delims=" %%s in ('type %PWFILE%') do @set PASSWORD=%%s
    del /Q %PWFILE%
    set TIMESERVER=http://timestamp.comodoca.com/rfc3161
) else (
    set TIMESERVER=http://timestamp.comodoca.com/
)

call miscDepsJp\include\python-jtalk\vcsetup.cmd
cd /d %~dp0
cd ..

set VERIFYLOG=output\nvda_%VERSION%_verify.log
del /Q %VERIFYLOG%

call jptools\setupMiscDepsJp.cmd

set SIGNTOOL="C:\Program Files (x86)\Windows Kits\10\bin\10.0.22000.0\x64\signtool.exe"

set FILE1=source\synthDrivers\jtalk\libmecab.dll
if "%APPVEYOR_PROJECT_SLUG%"=="nvdajp" (
    %SIGNTOOL% sign /f %PFX% /p %PASSWORD% /fd SHA256 /tr %TIMESERVER% /td SHA256 %FILE1%
) else (
    %SIGNTOOL% sign /a /fd SHA256 /tr %TIMESERVER% /td SHA256 %FILE1%
)
%SIGNTOOL% verify /pa %FILE1% >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror
timeout /T 5 /NOBREAK

set FILE2=source\synthDrivers\jtalk\libopenjtalk.dll
if "%APPVEYOR_PROJECT_SLUG%"=="nvdajp" (
    %SIGNTOOL% sign /f %PFX% /p %PASSWORD% /fd SHA256 /tr %TIMESERVER% /td SHA256 %FILE2%
) else (
    %SIGNTOOL% sign /a /fd SHA256 /tr %TIMESERVER% /td SHA256 %FILE2%
)
%SIGNTOOL% verify /pa %FILE2% >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror
timeout /T 5 /NOBREAK

if "%APPVEYOR_PROJECT_SLUG%"=="nvdajp" (
    scons source user_docs launcher release=1 certFile=%PFX% certPassword=%PASSWORD% certTimestampServer=%TIMESERVER% publisher=%PUBLISHER% version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% --silent %SCONSOPTIONS%
) else (
    scons source user_docs launcher release=1 certTimestampServer=%TIMESERVER% publisher=%PUBLISHER% version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% --silent %SCONSOPTIONS%
)
@if not "%ERRORLEVEL%"=="0" goto onerror

%SIGNTOOL% verify /pa dist\lib\%VERSION%\*.dll >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror
%SIGNTOOL% verify /pa dist\lib64\%VERSION%\*.dll >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror
%SIGNTOOL% verify /pa dist\libArm64\%VERSION%\*.dll >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror
%SIGNTOOL% verify /pa dist\*.exe >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror
%SIGNTOOL% verify /pa output\nvda_%VERSION%.exe >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror

echo %UPDATEVERSIONTYPE% %VERSION%
exit /b 0

:onerror
echo nvdajp build error %ERRORLEVEL%
@if "%PAUSE%"=="1" pause
exit /b -1
