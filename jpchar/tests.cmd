cd jpchar
set PYTHONUTF8=1
py checkCharDesc.py > __checkchardesc_log.txt
cd ..

exit /b 0

:onerror
echo error %ERRORLEVEL%
exit /b -1
