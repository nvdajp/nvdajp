set SCONSOPTIONS=%* --silent

call miscDepsJp\include\python-jtalk\vcsetup.cmd
cd /d %~dp0
cd ..




call jptools\setupMiscDepsJp.cmd

call jptools\kcCertBuild.cmd

exit /b 0

:onerror
exit /b -1
