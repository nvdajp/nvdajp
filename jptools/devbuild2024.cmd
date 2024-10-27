set VERSION=2024.4jp
set VERSION_BUILD=99999
del source\_buildVersion.py
call venvUtils\venvCmd jptools\devbuild.cmd source version_build=%VERSION_BUILD% --all-cores
@if not "%ERRORLEVEL%"=="0" goto onerror
call rununittests.bat
exit /b 0
:onerror
echo error %ERRORLEVEL%
exit /b -1
