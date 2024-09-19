@rem usage:
@rem del source\_buildVersion.py
@rem jptools\devbuild.cmd
@rem example: jptools\devbuild.cmd source dist launcher user_docs pot symbolsArchive -j12

set SCONSARGS=%*

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

exit /b 0

:onerror
echo build error %ERRORLEVEL%
exit /b -1
