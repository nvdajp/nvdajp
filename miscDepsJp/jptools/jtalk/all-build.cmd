rem build
cd ..\python-jtalk
call build.cmd

rem dic-build
cd ..\jtalk
cd libopenjtalk\mecab\src
nmake -f Makefile.mak all
cd ..\..\..
python make_jdic.py
@if not "%ERRORLEVEL%"=="0" goto onerror

exit /b 0

:onerror
exit /b -1
