echo nonCertAllBuild: Starting complete non-certified build...

call "%~dp0nonCertBuild1.cmd"
@if not "%ERRORLEVEL%"=="0" goto onerror

call "%~dp0nonCertBuild2.cmd" %*
@if not "%ERRORLEVEL%"=="0" goto onerror

echo nonCertAllBuild: All builds completed successfully

exit /b 0

:onerror
exit /b -1
