set RELEASE=1
set VERSION=jpalpha
set UPDATEVERSIONTYPE=nvdajp
for /F "usebackq" %%t in (`jptools\nowdate.cmd`) do set NOWDATE=%%t
set VERSION=%VERSION%_%NOWDATE%
set UPDATEVERSIONTYPE=%UPDATEVERSIONTYPE%alpha
set PUBLISHER=nvdajp
copy c:\work\kc\pfx\knowlec-key-pass-2018.txt jptools\secret
del source\_buildVersion.py*
call jptools\kcCertAllBuild.cmd
