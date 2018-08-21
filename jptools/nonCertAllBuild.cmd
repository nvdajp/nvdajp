set SCONSOPTIONS=%* --silent

set VERSION=2018.3jp
set UPDATEVERSIONTYPE=nvdajp

@for /F "usebackq" %%t in (`nowdate.cmd`) do set NOWDATE=%%t
set VERSION=%VERSION%-beta
set VERSION=%VERSION%-%NOWDATE%
set VERSION=%VERSION%-noncert
set UPDATEVERSIONTYPE=%UPDATEVERSIONTYPE%beta

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
