@scons source user_docs launcher certFile=%PFX% certPassword=%PASSWORD% certTimestampServer=%TIMESERVER% publisher=%PUBLISHER% version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% %SCONSOPTIONS%
@if not "%ERRORLEVEL%"=="0" goto onerror

exit /b 0

:onerror
exit /b -1
