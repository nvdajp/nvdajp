cd miscDepsJp
del /Q nvdajp-miscdep.7z
cd include\jtalk
call all-clean.cmd
call all-build.cmd
call all-install.cmd
call all-clean.cmd
del /Q *.pyc
cd libopenjtalk\mecab-naist-jdic
rmdir /S /Q dic
rmdir /S /Q _temp
del /Q nvdajp-custom-dic.csv
del /Q nvdajp-eng-dic.csv
del /Q nvdajp-roma-dic.csv
del /Q nvdajp-tankan-dic.csv
cd ..\..\..\..
cd source\synthDrivers
rmdir /S /Q espeak-data
cd ..\..
7z a -xr!.bzr* -xr!.git* -xr!_temp -xr!_pack*.cmd -xr!_push*.cmd -xr!*.obj -xr!*~ -xr!*.rst -xr!*.html -xr!include\jtalk\* -xr!include\python-jtalk\* -xr!jptools -xr!include\espeak\* -xr!include\AcrobatAccess\* -xr!include\ia2\* -xr!include\libMinHook\* -xr!source\brlapi.pyd -xr!source\configobj.py -xr!source\validate.py -xr!txt2tags.py -xr!installer\UAC.dll -xr!installer\waves\* -xr!tools\* -xr!uninstaller\* -xr!launcher\* -xr!source\images\nvda.ico -xr!source\waves\* -xr!appveyor.yml ..\nvdajp-miscdep.7z *
cd ..
7z x -y nvdajp-miscdep.7z
del /Q nvdajp-miscdep.7z

@rem cleanup

cd miscDepsJp
cd include\jtalk
call all-clean.cmd
del /Q *.pyc
del /Q libopenjtalk\lib\libopenjtalk.exp
del /Q libopenjtalk\lib\libopenjtalk.lib
cd ..\..
del /Q jptools\mecabHarness.pyc
del /Q source\synthDrivers\jtalk\mecab.pyc
del /Q source\synthDrivers\jtalk\dic\DIC_VERSION
del /Q source\synthDrivers\jtalk\dic\sys.dic
del /Q source\synthDrivers\jtalk\dic\unk.dic
del /Q source\synthDrivers\jtalk\libopenjtalk.dll
cd ..\jptools
call cleanMiscDepsJp.cmd
cd ..
