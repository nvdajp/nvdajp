@rem usage:
@rem > cd jptools
@rem > pack_kgs_addon.cmd
cd ..\source
copy ..\jptools\kgs_manifest.ini manifest.ini
7z a ..\jptools\_kgs.zip manifest.ini brailleDisplayDrivers\kgs.py brailleDisplayDrivers\kgsbn46.py brailleDisplayDrivers\brailleMemo.py brailleDisplayDrivers\DirectBM.dll
del manifest.ini
cd ..\jptools
move _kgs.zip kgsbraille-2.0.0.nvda-addon
