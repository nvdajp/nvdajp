echo nonCertBuild2: Starting non-certified build with scons...
set SCONSOPTIONS=%*

cd /d %~dp0
cd ..

@if not "%VERSION%"=="" goto versionready
echo nonCertBuild2: Setting development version...
for /F "usebackq" %%t in (`jptools\nowdate.cmd`) do set NOWDATE=%%t
set VERSION=jpdev_%NOWDATE%
set PUBLISHER=nvdajpdev
set UPDATEVERSIONTYPE=nvdajpdev

:versionready
echo nonCertBuild2: Building with VERSION=%VERSION%
set OPTIONS=publisher=%PUBLISHER% version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% %SCONSOPTIONS%
set OPTIONS=%OPTIONS% release=1

echo nonCertBuild2: Building source...
call scons.bat source %OPTIONS%
@if not "%ERRORLEVEL%"=="0" goto onerror

echo nonCertBuild2: Building user documentation...
call scons.bat user_docs %OPTIONS%
@if not "%ERRORLEVEL%"=="0" goto onerror

echo nonCertBuild2: Building distribution...
call scons.bat dist %OPTIONS%
@if not "%ERRORLEVEL%"=="0" goto onerror

echo nonCertBuild2: Building launcher...
call scons.bat launcher %OPTIONS%
@if not "%ERRORLEVEL%"=="0" goto onerror

echo nonCertBuild2: Build completed successfully

exit /b 0

:onerror
exit /b -1
