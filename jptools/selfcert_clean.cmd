del /Q /F selfsigned.* .sconsign.dblite
call miscDepsJp\include\python-jtalk\vcsetup.cmd
color
certutil -delstore root selfsigned.spc
scons -c
