set PFX=..\..\kc\pfx\knowlec-key141016.pfx
set PWFILE=..\..\kc\pfx\knowlec-key-pass.txt
for /F "delims=" %%s in ('type %PWFILE%') do set PASSWORD=%%s
set TIMESERVER=http://timestamp.comodoca.com/authenticode
set DESC=nvdajp
set FILE1=source\synthDrivers\jtalk\libmecab.dll
set FILE2=source\synthDrivers\jtalk\libopenjtalk.dll
set FILE3=source\brailleDisplayDrivers\DirectBM.dll

signtool sign /f %PFX% /p %PASSWORD% /t %TIMESERVER% /d %DESC% %FILE1%
signtool sign /f %PFX% /p %PASSWORD% /t %TIMESERVER% /d %DESC% %FILE2%
signtool sign /f %PFX% /p %PASSWORD% /t %TIMESERVER% /d %DESC% %FILE3%
