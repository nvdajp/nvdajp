@rem test nmake and check errorlevel
cl
if "%ERRORLEVEL%" neq "9009" goto :done

if exist "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\bin\vcvars32.bat" goto x64
call "C:\Program Files\Microsoft Visual Studio 12.0\VC\bin\vcvars32.bat"
goto done
:x64
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\bin\vcvars32.bat"
:done
SET CL=/arch:IA32 /D "_USING_V110_SDK71_"
@rem call jptools\findBackupFiles.cmd
call scons.bat -c
call jptools\setupMiscDepsJp.cmd
call jptools\kcCertMiscDepsJp.cmd
call jptools\kcCertBuild.cmd
