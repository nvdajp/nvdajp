cd c:\work\nvda\miscdep\include\jtalk
call setenv-x86.cmd
call all-build.cmd
call all-install.cmd
python mecabRunner.py > c:\work\nvda\nvdajp\jptools\__mecab_test.txt
cd c:\work\nvda\nvdajp\jptools
copy c:\work\nvda\miscdep\source\synthDrivers\jtalk\dic\* c:\work\nvda\nvdajp\source\synthDrivers\jtalk\dic
python jpBrailleRunner.py
