set VERSION=2014.4jp-beta-141017
set PUBLISHER=nvdajp
set PFX=..\..\kc\pfx\knowlec-key141016.pfx
set PWFILE=..\..\kc\pfx\knowlec-key-pass.txt
for /F "delims=" %%s in ('type %PWFILE%') do set PASSWORD=%%s
set TIMESERVER=http://timestamp.comodoca.com/authenticode
scons source user_docs launcher certFile=%PFX% certPassword=%PASSWORD% certTimestampServer=%TIMESERVER% publisher=%PUBLISHER% release=1 version=%VERSION%
