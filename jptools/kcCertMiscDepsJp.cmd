set PFX=..\..\kc\pfx\knowlec-key151019.pfx
set PWFILE=..\..\kc\pfx\knowlec-key-pass.txt
for /F "delims=" %%s in ('type %PWFILE%') do set PASSWORD=%%s
set TIMESERVER=http://timestamp.comodoca.com/authenticode
set FILE1=source\synthDrivers\jtalk\libmecab.dll
set FILE2=source\synthDrivers\jtalk\libopenjtalk.dll
signtool sign /f %PFX% /p %PASSWORD% /t %TIMESERVER% %FILE1%
signtool verify /pa %FILE1%
timeout /T 5 /NOBREAK
signtool sign /f %PFX% /p %PASSWORD% /t %TIMESERVER% %FILE2%
signtool verify /pa %FILE2%
timeout /T 5 /NOBREAK

