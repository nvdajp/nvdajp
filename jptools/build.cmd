@rem SET VERSION=2014.2jp
SET VERSION=jpbeta140502

SET DEBUG=
@rem SET DEBUG=nvdaHelperDebugFlags=noOptimize,RTC,debugCRT,symbols
@rem SET DEBUG=nvdaHelperDebugFlags=symbols

SET ARGS=publisher=nvdajp release=1 version=%VERSION% %DEBUG%
del /Q output\nvda_%VERSION%.exe
call scons.bat -c
call scons.bat source dist -j4 %ARGS%
call scons.bat user_docs -j4 %ARGS%
call scons.bat launcher %ARGS%

cd jptools
call buildControllerClient.cmd
cd ..
