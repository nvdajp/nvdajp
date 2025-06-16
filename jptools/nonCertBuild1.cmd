echo nonCertBuild1: Starting non-certified build process...

call miscDepsJp\include\python-jtalk\vcsetup.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror

cd /d %~dp0
cd ..

cd miscDepsJp\jptools
echo nonCertBuild1: Cleaning previous build...
call clean.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror

echo nonCertBuild1: Copying jtalk core files...
call copy_jtalk_core_files.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror

echo nonCertBuild1: Building and testing...
call build-and-test.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror

cd ..\..

echo nonCertBuild1: Setting up miscDepsJp...
call jptools\setupMiscDepsJp.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror

echo nonCertBuild1: Build completed successfully

exit /b 0

:onerror
exit /b -1
