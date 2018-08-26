rem usage:
rem > scons source
rem > cd jptools
rem > pack_jtalk_addon.cmd
cd ..\source
copy ..\jptools\jtalk_manifest.ini manifest.ini
7z a ..\jptools\nvdajp-jtalk.zip manifest.ini synthDrivers\nvdajp*.py synthDrivers\jtalk\*
del manifest.ini
cd ..\jptools
move nvdajp-jtalk.zip nvdajp-jtalk-180826.nvda-addon
