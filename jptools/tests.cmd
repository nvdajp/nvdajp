@rem scons tests checkPot publisher=%PUBLISHER% release=1 version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% %SCONSOPTIONS%
@rem @if not "%ERRORLEVEL%"=="0" goto onerror

@rem Ensure Japanese translation (.mo) exists for tests
@rem Compile nvda.po -> nvda.mo so gettext can load translations
miscDeps\tools\msgfmt.exe source\locale\ja\LC_MESSAGES\nvda.po -o source\locale\ja\LC_MESSAGES\nvda.mo
@if not "%ERRORLEVEL%"=="0" goto onerror

cd jptools
set PYTHONUTF8=1
py jpDicTest.py > __jpdictest_log.txt
@if not "%ERRORLEVEL%"=="0" goto onerror
cd ..

exit /b 0

:onerror
echo error %ERRORLEVEL%
exit /b -1
