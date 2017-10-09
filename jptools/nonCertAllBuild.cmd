set SCONSOPTIONS=%* --silent

set VERSION=2017.4jp
set UPDATEVERSIONTYPE=nvdajp

for /F "usebackq" %%t in (`python -c "from datetime import datetime as dt; print dt.now().strftime('%%y%%m%%d')+chr(dt.now().hour+97)"`) do set NOWDATE=%%t
set VERSION=%VERSION%-beta
set VERSION=%VERSION%-%NOWDATE%
set UPDATEVERSIONTYPE=%UPDATEVERSIONTYPE%beta

set PUBLISHER=nvdajp

call ..\miscDepsJp\include\python-jtalk\vcsetup.cmd

cd miscDepsJp\jptools
call clean.cmd
call build-and-test.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror
cd ..\..

@rem python scons.py -c
call jptools\setupMiscDepsJp.cmd

python scons.py source publisher=%PUBLISHER% release=1 version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% %SCONSOPTIONS%
@if not "%ERRORLEVEL%"=="0" goto onerror
python scons.py tests publisher=%PUBLISHER% release=1 version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% %SCONSOPTIONS%
@if not "%ERRORLEVEL%"=="0" goto onerror

call jptools\nonCertBuild.cmd

cd jptools
call buildControllerClient.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror
cd ..
:skip_client

exit /b 0

:onerror
echo nvdajp build error %ERRORLEVEL%
@if "%PAUSE%"=="1" pause
exit /b -1
