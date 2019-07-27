@rem usage:
@rem > cd jptools
@rem > pack_kgs_addon.cmd
cd ..\source
py ..\jptools\kgs_manifest.py %nowdate% manifest.ini
7z a ..\jptools\_kgs.zip manifest.ini brailleDisplayDrivers\kgs.py brailleDisplayDrivers\kgsbn46.py brailleDisplayDrivers\brailleMemo.py brailleDisplayDrivers\DirectBM.dll
del manifest.ini
cd ..\jptools
move _kgs.zip kgsbraille-%nowdate%.nvda-addon
