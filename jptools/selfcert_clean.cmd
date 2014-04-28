del /Q /F selfsigned.* .sconsign.dblite
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\bin\vcvars32.bat" /x86 /Release
color
certutil -delstore root selfsigned.spc
scons -c
