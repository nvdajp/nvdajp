@rem usage:
@rem set VERSION=2024.4jp
@rem jptools\devbuild.cmd source dist launcher user_docs pot symbolsArchive version_build=99999 -j12

@echo off
setlocal enabledelayedexpansion

rem Usage:
rem set VERSION=2024.4jp
rem jptools\devbuild.cmd source dist launcher user_docs pot symbolsArchive version_build=99999 -j12

rem Delete source_buildVersion.py if it exists
if exist "source_buildVersion.py" (
    del "source_buildVersion.py" || (
        echo Failed to delete source_buildVersion.py
        exit /b 1
    )
)

rem Set default VERSION if not defined
if not defined VERSION (
    set "VERSION=2024.4jp"
)

rem Initialize variables
set "SCONSARGS="
set "version_build_set=false"

rem Parse arguments
for %%A in (%*) do (
    echo %%A | findstr /b /c:"version_build=" >nul
    if not errorlevel 1 (
        set "version_build=%%A"
        set "version_build_set=true"
    ) else (
        set "SCONSARGS=!SCONSARGS! %%A"
    )
)

rem Append version_build if not set
if "!version_build_set!"=="false" (
    set "SCONSARGS=!SCONSARGS! version_build=99999"
) else (
    echo version_build=!version_build!
)

rem Continue with the rest of your script using !SCONSARGS!
echo Final SCONSARGS: !SCONSARGS!

endlocal

call miscDepsJp\include\python-jtalk\vcsetup.cmd
cd /d %~dp0
cd ..

@rem nmakeがない場合はエラー
nmake /?
@if not "%ERRORLEVEL%"=="0" goto onerror

@rem patchがない場合はエラー
patch -v
@if not "%ERRORLEVEL%"=="0" goto onerror

cd miscDepsJp\jptools
call copy_jtalk_core_files.cmd
cd ..\include\jtalk
call all-clean.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror

call all-build.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror

call all-install.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror

cd ..\python-jtalk
call clean.cmd
cd ..\..\jptools
call test.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror

cd ..\..

call jptools\setupMiscDepsJp.cmd

call scons.bat %SCONSARGS%
@if not "%ERRORLEVEL%"=="0" goto onerror

call rununittests.bat
@if not "%ERRORLEVEL%"=="0" goto onerror

exit /b 0

:onerror
echo build error %ERRORLEVEL%
exit /b -1
