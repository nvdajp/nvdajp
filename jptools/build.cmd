@rem set VERSION=2014.3jp
set BUILDTYPE=jpbeta
set VERSION=%BUILDTYPE%140801
set PUBLISHER=nvdajp
set PAUSE=0
set CLEAN=1
set CLIENT=1

set DEBUG=
@rem set DEBUG=nvdaHelperDebugFlags=noOptimize,RTC,debugCRT,symbols
@rem set DEBUG=nvdaHelperDebugFlags=symbols

set ARGS=-j4 publisher=%PUBLISHER% release=1 version=%VERSION% %DEBUG%

del /Q output\nvda_%VERSION%.exe
@if not "%ERRORLEVEL%"=="0" goto onerror

@if "%CLEAN%"=="0" goto skip_clean
@if "%PAUSE%"=="1" pause
call scons.bat -c
@if not "%ERRORLEVEL%"=="0" goto onerror
:skip_clean

@if "%PAUSE%"=="1" pause
call scons.bat user_docs %ARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror

@if "%PAUSE%"=="1" pause
call scons.bat source\locale %ARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror

@if "%PAUSE%"=="1" pause
call scons.bat source\comInterfaces %ARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror

@if "%PAUSE%"=="1" pause
call scons.bat NVDAHelper %ARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror

@if "%PAUSE%"=="1" pause
call scons.bat source dist launcher %ARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror

@if "%CLIENT%"=="0" goto skip_client
@if "%PAUSE%"=="1" pause
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
