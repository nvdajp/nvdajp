@echo off
setlocal EnableExtensions EnableDelayedExpansion
rem runlint [<output dir>]
rem Lints and formats all python files
set hereOrig=%~dp0
set here=%hereOrig%
if #%hereOrig:~-1%# == #\# set here=%hereOrig:~0,-1%

set ruffCheckArgs=
set ruffFormatArgs=
set ruffExcludeArgs=--exclude=include,source/comInterfaces,miscDepsJp,miscDeps/python/ftdi2.py,source/NVDAObjects/UIA/__init__.py
rem Allow uv to download and use a managed Python if system 3.13 is unavailable
set UV_PYTHON_PREFERENCE=managed
if "%1" NEQ "" set ruffCheckArgs=--output-file=%1/PR-lint.xml --output-format=junit
if "%1" NEQ "" set ruffFormatArgs=--diff
rem First try project-managed env; if it fails (e.g. locked .venv), fallback to uvx
call uv run --group lint --directory "%here%" ruff check --fix %ruffExcludeArgs% %ruffCheckArgs%
set ERR=%ERRORLEVEL%
if NOT %ERR%==0 (
    echo Falling back to uvx for ruff check
    call uvx --python 3.13 ruff==0.12.7 check --fix %ruffExcludeArgs% %ruffCheckArgs%
    if ERRORLEVEL 1 exit /b %ERRORLEVEL%
)
if "%1" NEQ "" (
    call uv run --group lint --directory "%here%" ruff format %ruffExcludeArgs% %ruffFormatArgs% > %1/lint-diff.diff
    set ERR=%ERRORLEVEL%
    if NOT %ERR%==0 (
        echo Falling back to uvx for ruff format
        call uvx --python 3.13 ruff==0.12.7 format %ruffExcludeArgs% %ruffFormatArgs% > %1/lint-diff.diff
        if ERRORLEVEL 1 exit /b %ERRORLEVEL%
    )
) else (
    call uv run --group lint --directory "%here%" ruff format %ruffExcludeArgs% %ruffFormatArgs%
    set ERR=%ERRORLEVEL%
    if NOT %ERR%==0 (
        echo Falling back to uvx for ruff format
        call uvx --python 3.13 ruff==0.12.7 format %ruffExcludeArgs% %ruffFormatArgs%
        if ERRORLEVEL 1 exit /b %ERRORLEVEL%
    )
)
rem Run pyright for type checking
if ERRORLEVEL 1 exit /b %ERRORLEVEL%

if "%1" NEQ "" (
    call uv run --group lint --directory "%here%" pyright > %1/pyright-output.txt
    set ERR=%ERRORLEVEL%
    if NOT %ERR%==0 (
        echo Falling back to uvx for pyright
        call uvx --python 3.13 pyright==1.1.403 > %1/pyright-output.txt
        if ERRORLEVEL 1 exit /b %ERRORLEVEL%
    )
) else (
    call uv run --group lint --directory "%here%" pyright
    set ERR=%ERRORLEVEL%
    if NOT %ERR%==0 (
        echo Falling back to uvx for pyright
        call uvx --python 3.13 pyright==1.1.403
        if ERRORLEVEL 1 exit /b %ERRORLEVEL%
    )
)
endlocal
