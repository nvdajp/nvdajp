cd ..\miscDepsJp
cd include\jtalk\libopenjtalk\mecab
nmake /f Makefile.mak clean
cd ..\..\..\..
cd source\synthDrivers\jtalk
del /Q *.pyc
cd ..\..\..
cd ..\jptools



