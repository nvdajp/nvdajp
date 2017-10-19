python scons.py tests
@if not "%ERRORLEVEL%"=="0" goto onerror

exit /b 0

:onerror
echo error %ERRORLEVEL%
exit /b -1
