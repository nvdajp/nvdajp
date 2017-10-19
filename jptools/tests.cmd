python scons.py tests checkPot publisher=%PUBLISHER% release=1 version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% %SCONSOPTIONS%
@if not "%ERRORLEVEL%"=="0" goto onerror

cd jptools
python jpDicTest.py > __jpdictest_log.txt
cd ..

exit /b 0

:onerror
echo error %ERRORLEVEL%
exit /b -1
