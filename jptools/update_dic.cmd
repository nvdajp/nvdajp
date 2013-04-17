cd c:\work\nvda\miscdep\include\jtalk
call setenv-x86.cmd
call all-build.cmd
call all-install.cmd
python mecabRunner.py > c:\work\nvda\jp2013.1\jptools\__mecab_test.txt
cd c:\work\nvda\jp2013.1\jptools
copy c:\work\nvda\miscdep\source\synthDrivers\jtalk\dic\* c:\work\nvda\jp2013.1\source\synthDrivers\jtalk\dic
python jpBrailleRunner.py
