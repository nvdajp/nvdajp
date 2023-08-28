set SCONSOPTIONS=%*

set TIMESERVER=http://timestamp.comodoca.com/

call miscDepsJp\include\python-jtalk\vcsetup.cmd
cd /d %~dp0
cd ..

call jptools\setupMiscDepsJp.cmd

set SIGNTOOL="C:\Program Files (x86)\Windows Kits\10\bin\10.0.22000.0\x64\signtool.exe"

%SIGNTOOL% sign /a /fd SHA256 /tr %TIMESERVER% /td SHA256 source\synthDrivers\jtalk\libmecab.dll
timeout /T 5 /NOBREAK

%SIGNTOOL% sign /a /fd SHA256 /tr %TIMESERVER% /td SHA256 source\synthDrivers\jtalk\libopenjtalk.dll
timeout /T 5 /NOBREAK

call scons.bat source user_docs launcher release=1 certTimestampServer=%TIMESERVER% publisher=%PUBLISHER% version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% --silent %SCONSOPTIONS%
@if not "%ERRORLEVEL%"=="0" goto onerror

set VERIFYLOG=output\nvda_%VERSION%_verify.log
del /Q %VERIFYLOG%

%SIGNTOOL% verify /pa output\*.exe >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror

%SIGNTOOL% verify /pa dist\*.exe >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror

for /r "dist\synthDrivers\jtalk" %%i in (*.dll *.exe) do (
    %SIGNTOOL% verify /pa "%%i" >> %VERIFYLOG%
    @if not "%ERRORLEVEL%"=="0" goto onerror
)
for /r "dist\lib" %%i in (*.dll *.exe) do (
    if "%%~nxi" neq "Microsoft.UI.UIAutomation.dll" (
        %SIGNTOOL% verify /pa "%%i" >> %VERIFYLOG%
        @if not "%ERRORLEVEL%"=="0" goto onerror
    )
)
for /r "dist\lib64" %%i in (*.dll *.exe) do (
    %SIGNTOOL% verify /pa "%%i" >> %VERIFYLOG%
    @if not "%ERRORLEVEL%"=="0" goto onerror
)
for /r "dist\libArm64" %%i in (*.dll *.exe) do (
    %SIGNTOOL% verify /pa "%%i" >> %VERIFYLOG%
    @if not "%ERRORLEVEL%"=="0" goto onerror
)

echo %UPDATEVERSIONTYPE% %VERSION%
exit /b 0

:onerror
echo nvdajp build error %ERRORLEVEL%
@if "%PAUSE%"=="1" pause
exit /b -1
