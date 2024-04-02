SET ARGS=publisher=nvdajp release=1 version=%VERSION%
call scons nvdaHelper\client %ARGS%
cd jptools
cd nvdajpClient

copy ..\..\build\x86\client\nvdaController.h x86
copy ..\..\build\x86\client\nvdaControllerClient.dll x86
copy ..\..\build\x86\client\nvdaControllerClient.dll.pdb x86
copy ..\..\build\x86\client\nvdaControllerClient.exp x86
copy ..\..\build\x86\client\nvdaControllerClient.lib x86

copy ..\..\build\x86_64\client\nvdaController.h x64
copy ..\..\build\x86_64\client\nvdaControllerClient.dll x64
copy ..\..\build\x86_64\client\nvdaControllerClient.dll.pdb x64
copy ..\..\build\x86_64\client\nvdaControllerClient.exp x64
copy ..\..\build\x86_64\client\nvdaControllerClient.lib x64

copy ..\..\build\arm64\client\nvdaController.h arm64
copy ..\..\build\arm64\client\nvdaControllerClient.dll arm64
copy ..\..\build\arm64\client\nvdaControllerClient.dll.pdb arm64
copy ..\..\build\arm64\client\nvdaControllerClient.exp arm64
copy ..\..\build\arm64\client\nvdaControllerClient.lib arm64

SET OUTFILE=..\..\output\nvda_%VERSION%_controllerClientJp.zip
del /Q %OUTFILE%
7z a %OUTFILE% arm64 examples x64 x86 license.txt readme.html readmejp.txt
cd ..
cd ..
