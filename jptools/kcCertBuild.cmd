@rem begin newdirectbm
set DIRECTBM=c:\kgs\dev\DirectBM.dll
copy /Y %DIRECTBM% source\brailleDisplayDrivers
@rem end newdirectbm

set VERSION=2015.3jp
for /F "usebackq" %%t in (`python -c "from datetime import datetime as dt; print dt.now().strftime('%%y%%m%%d')"`) do set NOWDATE=%%t
set VERSION=%VERSION%-beta-%NOWDATE%
set PUBLISHER=nvdajp
set PFX=..\..\kc\pfx\knowlec-key141016.pfx
set PWFILE=..\..\kc\pfx\knowlec-key-pass.txt
for /F "delims=" %%s in ('type %PWFILE%') do set PASSWORD=%%s
set TIMESERVER=http://timestamp.comodoca.com/authenticode
scons source user_docs launcher certFile=%PFX% certPassword=%PASSWORD% certTimestampServer=%TIMESERVER% publisher=%PUBLISHER% release=1 version=%VERSION%
