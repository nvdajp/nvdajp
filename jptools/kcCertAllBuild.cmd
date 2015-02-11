call jptools\findBackupFiles.cmd
call scons.bat -c
call jptools\setup-vc2013.cmd
call jptools\setupMiscDepsJp.cmd
call jptools\kcCertMiscDepsJp.cmd
call jptools\kcCertBuild.cmd
