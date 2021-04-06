set SCONSOPTIONS=%* --silent

call miscDepsJp\include\python-jtalk\vcsetup.cmd
cd /d %~dp0
cd ..




call jptools\setupMiscDepsJp.cmd

@rem set PATH="C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64";%PATH%

call jptools\kcCertBuild.cmd

exit /b 0

:onerror
exit /b -1
