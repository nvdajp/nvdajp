uv run python -c "import sys; sys.path.insert(0, '../../../jptools'); from scons_jp import _copy_jtalk_core_files; from pathlib import Path; exit(_copy_jtalk_core_files(Path('../../../').resolve()))"
@if not "%ERRORLEVEL%"=="0" goto onerror

call ..\include\python-jtalk\vcsetup.cmd
cd /d %~dp0
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

exit /b 0

:onerror
exit /b -1
