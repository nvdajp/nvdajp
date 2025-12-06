cd miscDepsJp
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
rem Prefer uv to run overlay within repo project; fallback to py/python
where uv >nul 2>&1
if %ERRORLEVEL% EQU 0 (
  rem Keep CWD in miscDepsJp (script expects this), but use repo root as uv project
  uv run --project .. python ..\jptools\setup_miscdeps_overlay.py
) else (
  where py >nul 2>&1
  if %ERRORLEVEL% EQU 0 (
    py -3 ..\jptools\setup_miscdeps_overlay.py
  ) else (
    python ..\jptools\setup_miscdeps_overlay.py
  )
)
cd ..

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
