call jptools\nonCertBuild1.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror

call jptools\nonCertBuild2.cmd %*
@if not "%ERRORLEVEL%"=="0" goto onerror

exit /b 0

:onerror
exit /b -1
