rem all-clean
del *.pyc

cd ..\python-jtalk
call clean.cmd
cd ..\jtalk

cd libopenjtalk\mecab\src
nmake -f Makefile.mak clean
cd ..\..\..

cd libopenjtalk\mecab-naist-jdic
rmdir /S /Q dic
rmdir /S /Q _temp
del nvdajp-custom-dic.csv
del nvdajp-eng-dic.csv
del nvdajp-roma-dic.csv
del nvdajp-tankan-dic.csv
cd ..\..
