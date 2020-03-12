set SCONSOPTIONS=%* --silent

call miscDepsJp\include\python-jtalk\vcsetup.cmd
cd /d %~dp0
cd ..

cd miscDepsJp\jptools
call clean.cmd
call build-and-test.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror
cd ..\..

call jptools\setupMiscDepsJp.cmd

@if not "%VERSION%"=="" goto versionready
for /F "usebackq" %%t in (`jptools\nowdate.cmd`) do set NOWDATE=%%t
set VERSION=jpdev_%NOWDATE%
set PUBLISHER=nvdajpdev
set UPDATEVERSIONTYPE=nvdajpdev

:versionready
py scons.py source user_docs launcher publisher=%PUBLISHER% release=1 version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% %SCONSOPTIONS%

exit /b 0

:onerror
exit /b -1
