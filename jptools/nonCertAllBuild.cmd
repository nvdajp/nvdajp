set SCONSOPTIONS=%* --silent

set UPDATEVERSIONTYPE=nvdajpalpha

for /F "usebackq" %%t in (`python -c "from datetime import datetime as dt; print dt.now().strftime('%%y%%m%%d')+chr(dt.now().hour+97)"`) do set NOWDATE=%%t
set VERSION=jpalpha_%NOWDATE%_noncert

set PUBLISHER=nvdajp

call miscDepsJp\include\python-jtalk\vcsetup.cmd
cd /d %~dp0
cd ..

cd miscDepsJp\jptools
call clean.cmd
call build-and-test.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror
cd ..\..

@rem python scons.py -c
call jptools\setupMiscDepsJp.cmd

python jptools\ensure_utf8_bom.py include\espeak\src\libespeak-ng\tr_languages.c
python scons.py source user_docs launcher publisher=%PUBLISHER% release=1 version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% %SCONSOPTIONS%

cd jptools
call buildControllerClient.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror
cd ..

exit /b 0

:onerror
exit /b -1
