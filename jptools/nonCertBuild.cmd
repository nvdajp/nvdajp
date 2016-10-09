set SCONSOPTIONS=%*

@rem test nmake and check errorlevel
cl
if "%ERRORLEVEL%" neq "9009" goto :done

if exist "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin\vcvars32.bat" goto x64
call "C:\Program Files\Microsoft Visual Studio 14.0\VC\bin\vcvars32.bat"
goto done
:x64
call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin\vcvars32.bat"
:done
SET CL=/arch:IA32 /D "_USING_V110_SDK71_"
call jptools\setupMiscDepsJp.cmd

for /F "usebackq" %%t in (`python -c "from datetime import datetime as dt; print dt.now().strftime('%%y%%m%%d')"`) do set NOWDATE=%%t
set VERSION=jpdev%NOWDATE%

set PUBLISHER=nvdajp
set PAUSE=0
set CLEAN=0
set CLIENT=1
set PROCESS=1
set RELEASE=1

@if "%RELEASE%"=="0" goto set_debug_option
set DEBUG=
goto endif_set_debug_option
:set_debug_option
set DEBUG=nvdaHelperDebugFlags=RTC,debugCRT
:endif_set_debug_option

set ARGS=-j%PROCESS% publisher=%PUBLISHER% release=%RELEASE% version=%VERSION% %DEBUG% %SCONSOPTIONS%

@if "%RELEASE%"=="0" goto del_snapshot
del /Q output\nvda_%VERSION%.exe
goto endif_del_snapshot
:del_snapshot
del /Q output\nvda_snapshot_%VERSION%.exe
:endif_del_snapshot
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
@rem @if not "%ERRORLEVEL%"=="0" goto onerror

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
