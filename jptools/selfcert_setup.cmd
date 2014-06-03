del /Q /F selfsigned.*
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\bin\vcvars32.bat" /x86 /Release
color
makecert -r -n "CN=selfsigned" -sv selfsigned.pvk selfsigned.cert
cert2spc selfsigned.cert selfsigned.spc
pvk2pfx -pvk selfsigned.pvk -spc selfsigned.spc -PFX selfsigned.pfx
certutil -addstore root selfsigned.spc
