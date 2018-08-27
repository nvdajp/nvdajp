rem usage:
rem > scons source
rem > cd jptools
rem > set NOWDATE=180827a
rem > pack_jtalk_addon.cmd
cd ..\source
py ..\jptools\jtalk_manifest.py %nowdate% manifest.ini
7z a ..\jptools\nvdajp-jtalk.zip manifest.ini synthDrivers\nvdajp*.py synthDrivers\jtalk\*
del manifest.ini
cd ..\jptools
move nvdajp-jtalk.zip nvdajp-jtalk-%nowdate%.nvda-addon
