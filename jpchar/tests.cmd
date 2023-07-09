cd jpchar
py checkCharDesc.py > __checkchardesc_log.txt
cd ..

exit /b 0

:onerror
echo error %ERRORLEVEL%
exit /b -1
