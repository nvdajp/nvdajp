@rem usage:
@rem > cd jptools
@rem > pack_kgs_addon.cmd
set DIRECTBM=c:\kgs\dev\DirectBM.dll
cd ..\source
copy /Y %DIRECTBM% brailleDisplayDrivers
copy ..\jptools\kgs_manifest.ini manifest.ini
7z a ..\jptools\_kgs.zip manifest.ini brailleDisplayDrivers\kgs.py brailleDisplayDrivers\DirectBM.dll
del manifest.ini
cd ..\jptools
move _kgs.zip kgsbraille-1.9.3.nvda-addon
