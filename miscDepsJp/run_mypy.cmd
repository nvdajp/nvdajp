cd jptools
call copy_jtalk_core_files.cmd
mypy @"../mypy_jptools.txt"
cd ..
cd source\synthDrivers
mypy @"../../mypy_source_synthDrivers.txt"
cd ..\..
