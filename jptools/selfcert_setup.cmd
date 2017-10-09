del /Q /F selfsigned.*
call miscDepsJp\include\python-jtalk\vcsetup.cmd
color
makecert -r -n "CN=selfsigned" -sv selfsigned.pvk selfsigned.cert
cert2spc selfsigned.cert selfsigned.spc
pvk2pfx -pvk selfsigned.pvk -spc selfsigned.spc -PFX selfsigned.pfx
certutil -addstore root selfsigned.spc
