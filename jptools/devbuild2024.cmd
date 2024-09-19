set VERSION=2024.4jp
del source\_buildVersion.py
venvUtils\venvCmd jptools\devbuild.cmd source version_build=99999 --all-cores
rununittests.bat
