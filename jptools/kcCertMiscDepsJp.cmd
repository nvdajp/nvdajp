set PFX=..\..\kc\pfx\knowlec-key141016.pfx
set PWFILE=..\..\kc\pfx\knowlec-key-pass.txt
for /F "delims=" %%s in ('type %PWFILE%') do set PASSWORD=%%s
set TIMESERVER=http://timestamp.comodoca.com/authenticode
set DESC=nvdajp
set FILE1=source\synthDrivers\jtalk\libmecab.dll
set FILE2=source\synthDrivers\jtalk\libopenjtalk.dll
@rem set FILE3=source\brailleDisplayDrivers\DirectBM.dll

signtool sign /f %PFX% /p %PASSWORD% /t %TIMESERVER% /d %DESC% %FILE1%
timeout /T 3 /NOBREAK
signtool sign /f %PFX% /p %PASSWORD% /t %TIMESERVER% /d %DESC% %FILE2%
timeout /T 3 /NOBREAK
@rem signtool sign /f %PFX% /p %PASSWORD% /t %TIMESERVER% /d %DESC% %FILE3%
