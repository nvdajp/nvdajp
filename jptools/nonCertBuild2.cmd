set SCONSOPTIONS=%*

@if not "%VERSION%"=="" goto versionready
for /F "usebackq" %%t in (`jptools\nowdate.cmd`) do set NOWDATE=%%t
set VERSION=jpdev_%NOWDATE%
set PUBLISHER=nvdajpdev
set UPDATEVERSIONTYPE=nvdajpdev

:versionready
set OPTIONS=publisher=%PUBLISHER% version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% %SCONSOPTIONS%
call scons source %OPTIONS%
@if not "%ERRORLEVEL%"=="0" goto onerror
call scons user_docs %OPTIONS%
@if not "%ERRORLEVEL%"=="0" goto onerror
call scons dist %OPTIONS%
@if not "%ERRORLEVEL%"=="0" goto onerror
call scons launcher %OPTIONS% release=1
@if not "%ERRORLEVEL%"=="0" goto onerror

exit /b 0

:onerror
exit /b -1
