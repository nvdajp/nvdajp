call miscDepsJp\include\python-jtalk\vcsetup.cmd
cd /d %~dp0
cd ..

cd miscDepsJp\jptools
call clean.cmd
cd ..\..

call jptools\setupMiscDepsJp.cmd

exit /b 0

:onerror
exit /b -1
