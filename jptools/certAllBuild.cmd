set SCONSOPTIONS=%*

set TIMESERVER=http://timestamp.comodoca.com/

call miscDepsJp\include\python-jtalk\vcsetup.cmd
cd /d %~dp0
cd ..

set VERIFYLOG=output\nvda_%VERSION%_verify.log
del /Q %VERIFYLOG%

call jptools\setupMiscDepsJp.cmd

set SIGNTOOL="C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64\signtool.exe"

set FILE1=source\synthDrivers\jtalk\libmecab.dll
%SIGNTOOL% sign /a /fd SHA256 /tr %TIMESERVER% /td SHA256 %FILE1%
%SIGNTOOL% verify /pa %FILE1% >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror
timeout /T 5 /NOBREAK

set FILE2=source\synthDrivers\jtalk\libopenjtalk.dll
%SIGNTOOL% sign /a /fd SHA256 /tr %TIMESERVER% /td SHA256 %FILE2%
%SIGNTOOL% verify /pa %FILE2% >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror
timeout /T 5 /NOBREAK

@scons source user_docs launcher release=1 certTimestampServer=%TIMESERVER% publisher=%PUBLISHER% version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% --silent %SCONSOPTIONS%
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
