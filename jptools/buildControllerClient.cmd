SET VERSION=nvdajp-client-140118
SET ARGS=publisher=nvdajp release=1 version=%VERSION%
cd ..
call scons.bat nvdaHelper\client %ARGS%
cd jptools
cd nvdajpClient
copy ..\..\build\x86\client\nvdaController.h client
copy ..\..\build\x86\client\nvdaControllerClient32.dll client
copy ..\..\build\x86\client\nvdaControllerClient32.exp client
copy ..\..\build\x86\client\nvdaControllerClient32.lib client
copy ..\..\build\x86_64\client\nvdaControllerClient64.dll client
copy ..\..\build\x86_64\client\nvdaControllerClient64.exp client
copy ..\..\build\x86_64\client\nvdaControllerClient64.lib client
del /Q %VERSION%.zip
7z a -xr!*~ -xr!.git* %VERSION%.zip client python
cd ..

