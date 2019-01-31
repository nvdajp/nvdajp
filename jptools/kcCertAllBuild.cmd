set SCONSOPTIONS=%* --silent

set PFX=jptools\secret\knowlec-key181024c.pfx
set PWFILE=jptools\secret\knowlec-key-pass-2018.txt
@for /F "delims=" %%s in ('type %PWFILE%') do @set PASSWORD=%%s
del /Q %PWFILE%
set TIMESERVER=http://timestamp.comodoca.com/authenticode

call miscDepsJp\include\python-jtalk\vcsetup.cmd
cd /d %~dp0
cd ..

set VERIFYLOG=output\nvda_%VERSION%_verify.log
del /Q %VERIFYLOG%

call jptools\setupMiscDepsJp.cmd

set FILE1=source\synthDrivers\jtalk\libmecab.dll
@signtool sign /fd sha256 /f %PFX% /p %PASSWORD% /t %TIMESERVER% %FILE1%
signtool verify /pa %FILE1% >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror
timeout /T 5 /NOBREAK

set FILE2=source\synthDrivers\jtalk\libopenjtalk.dll
@signtool sign /fd sha256 /f %PFX% /p %PASSWORD% /t %TIMESERVER% %FILE2%
signtool verify /pa %FILE2% >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror
timeout /T 5 /NOBREAK

call jptools\kcCertBuild.cmd

signtool verify /pa dist\lib\%VERSION%\*.dll >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror
signtool verify /pa dist\lib64\%VERSION%\*.dll >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror
signtool verify /pa dist\libArm64\%VERSION%\*.dll >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror
signtool verify /pa dist\*.exe >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror
signtool verify /pa output\nvda_%VERSION%.exe >> %VERIFYLOG%
@if not "%ERRORLEVEL%"=="0" goto onerror

cd jptools
call buildControllerClient.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror
cd ..
:skip_client

echo %UPDATEVERSIONTYPE% %VERSION%
exit /b 0

:onerror
echo nvdajp build error %ERRORLEVEL%
@if "%PAUSE%"=="1" pause
exit /b -1
