@rem usage:
@rem > cd jptools
@rem > pack_kgs_addon.cmd
cd ..\source
set KGSVERSION=%nowdate%
@rem set KGSVERSION=2.0
py ..\jptools\kgs_manifest.py %KGSVERSION% manifest.ini
7z a ..\jptools\_kgs.zip manifest.ini brailleDisplayDrivers\kgs.py brailleDisplayDrivers\brailleMemo.py brailleDisplayDrivers\DirectBM.dll
del manifest.ini
cd ..\jptools
move _kgs.zip kgsbraille-%KGSVERSION%.nvda-addon
