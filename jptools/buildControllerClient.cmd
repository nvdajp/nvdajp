SET ARGS=publisher=nvdajp release=1 version=%VERSION%
call scons nvdaHelper\client %ARGS%
cd jptools
cd nvdajpClient

copy ..\..\build\x86\client\nvdaController.h client\x86
copy ..\..\build\x86\client\nvdaControllerClient.dll client\x86
copy ..\..\build\x86\client\nvdaControllerClient.dll.pdb client\x86
copy ..\..\build\x86\client\nvdaControllerClient.exp client\x86
copy ..\..\build\x86\client\nvdaControllerClient.lib client\x86

copy ..\..\build\x86_64\client\nvdaController.h client\x64
copy ..\..\build\x86_64\client\nvdaControllerClient.dll client\x64
copy ..\..\build\x86_64\client\nvdaControllerClient.dll.pdb client\x64
copy ..\..\build\x86_64\client\nvdaControllerClient.exp client\x64
copy ..\..\build\x86_64\client\nvdaControllerClient.lib client\x64

copy ..\..\build\arm64\client\nvdaController.h client\arm64
copy ..\..\build\arm64\client\nvdaControllerClient.dll client\arm64
copy ..\..\build\arm64\client\nvdaControllerClient.dll.pdb client\arm64
copy ..\..\build\arm64\client\nvdaControllerClient.exp client\arm64
copy ..\..\build\arm64\client\nvdaControllerClient.lib client\arm64

SET OUTFILE=..\..\output\nvda_%VERSION%_controllerClientJp.zip
del /Q %OUTFILE%
7z a %OUTFILE% client python license.txt readme.html readmejp.txt
cd ..
cd ..
