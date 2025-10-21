@echo off
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%
set unitTestsPath=%here%\tests\unit
set testOutput=%here%\testOutput\unit
md %testOutput%

rem Ensure nvda-misc-deps (editable) is on sys.path by including the 'dev' group alongside 'unit-tests'
call uv run --with pylouis --group dev --group unit-tests --directory "%here%" -m xmlrunner discover -b -s "%unitTestsPath%" -t "%here%" --output-file "%testOutput%\unitTests.xml" %*


