set JTDIR=%appdata%\nvda\synthDrivers
mkdir %JTDIR%
copy ..\source\synthDrivers\nvdajp_jtalk.py %JTDIR%
mkdir %JTDIR%\jtalk
copy ..\source\synthDrivers\jtalk\* %JTDIR%\jtalk
mkdir %JTDIR%\jtalk\dic
copy ..\source\synthDrivers\jtalk\dic\* %JTDIR%\jtalk\dic
mkdir %JTDIR%\jtalk\lite
copy ..\source\synthDrivers\jtalk\lite\* %JTDIR%\jtalk\lite
mkdir %JTDIR%\jtalk\m001
copy ..\source\synthDrivers\jtalk\m001\* %JTDIR%\jtalk\m001
mkdir %JTDIR%\jtalk\mei
copy ..\source\synthDrivers\jtalk\mei\* %JTDIR%\jtalk\mei
