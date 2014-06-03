rem usage:
rem > scons source
rem > cd jptools
rem > pack_kgs_addon.cmd
cd ..\source
copy ..\jptools\kgs_manifest.ini manifest.ini
7z a ..\jptools\nvdajp-kgs.zip manifest.ini brailleDisplayDrivers\kgs.py brailleDisplayDrivers\DirectBM.dll
del manifest.ini
cd ..\jptools
move nvdajp-kgs.zip nvdajp-kgs-130521.nvda-addon
