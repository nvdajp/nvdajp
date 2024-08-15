@echo off
rem runlint [<output file>]
rem Lints the entire repository
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%
set scriptsDir=%here%\venvUtils

if "%1" NEQ "" set ruffArgs=--output-file=%1 --output-format=junit
call "%scriptsDir%\venvCmd.bat" ruff check --fix --exclude=include,source/comInterfaces,miscDepsJp,miscDeps/python/ftdi2.py,source/NVDAObjects/UIA/__init__.py %ruffArgs%
if ERRORLEVEL 1 exit /b %ERRORLEVEL%
