set VERSION=2015.4jp
set UPDATEVERSIONTYPE=nvdajp
for /F "usebackq" %%t in (`python -c "from datetime import datetime as dt; print dt.now().strftime('%%y%%m%%d')"`) do set NOWDATE=%%t

set VERSION=%VERSION%-beta-%NOWDATE%
set UPDATEVERSIONTYPE=%UPDATEVERSIONTYPE%beta

set PUBLISHER=nvdajp
set PFX=..\..\kc\pfx\knowlec-key151019.pfx
set PWFILE=..\..\kc\pfx\knowlec-key-pass.txt
for /F "delims=" %%s in ('type %PWFILE%') do set PASSWORD=%%s
set TIMESERVER=http://timestamp.comodoca.com/authenticode
scons source user_docs launcher certFile=%PFX% certPassword=%PASSWORD% certTimestampServer=%TIMESERVER% publisher=%PUBLISHER% release=1 version=%VERSION% updateVersionType=%UPDATEVERSIONTYPE% 

signtool verify /pa dist\lib\*.dll >> jptools\__verify_log
signtool verify /pa dist\lib64\*.dll >> jptools\__verify_log
signtool verify /pa dist\*.exe >> jptools\__verify_log
signtool verify /pa output\nvda_%VERSION%.exe >> jptools\__verify_log

copy output\nvda_%VERSION%.exe %HOME%\Dropbox\Public
