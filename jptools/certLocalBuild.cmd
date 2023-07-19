set RELEASE=1
set VERSION=2023.1jp
set UPDATEVERSIONTYPE=nvdajp
set PUBLISHER=nvdajp
copy c:\work\shuaruta\pfx\shuaruta-key-pass-2022.txt jptools\secret
copy c:\work\shuaruta\pfx\shuaruta-key220824.pfx jptools\secret
del source\_buildVersion.py*
call jptools\certAllBuild.cmd
