set SCONSOPTIONS=%* --silent

@rem set UPDATEVERSIONTYPE=nvdajpalpha
@rem 
@rem for /F "usebackq" %%t in (`python -c "from datetime import datetime as dt; print dt.now().strftime('%%y%%m%%d')+chr(dt.now().hour+97)"`) do set NOWDATE=%%t
@rem set VERSION=jpalpha_%NOWDATE%_noncert
@rem 
@rem set PUBLISHER=nvdajp
@rem 
call miscDepsJp\include\python-jtalk\vcsetup.cmd
cd /d %~dp0
cd ..

cd miscDepsJp\jptools
call clean.cmd
call build-and-test.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror
cd ..\..

call jptools\setupMiscDepsJp.cmd

python scons.py source user_docs launcher publisher=%PUBLISHER% release=1 version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% %SCONSOPTIONS%

@rem cd jptools
@rem call buildControllerClient.cmd
@rem @if not "%ERRORLEVEL%"=="0" goto onerror
@rem cd ..

exit /b 0

:onerror
exit /b -1
