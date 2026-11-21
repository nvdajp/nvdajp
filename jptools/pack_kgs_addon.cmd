@rem usage:
@rem > cd jptools
@rem > pack_kgs_addon.cmd [--version VERSION]
@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
if not defined VERSION if defined KGSVERSION set "VERSION=%KGSVERSION%"
if not defined VERSION if defined nowdate set "VERSION=%nowdate%"
where uv >nul 2>nul
if %errorlevel% equ 0 (
	uv run --no-active python "%SCRIPT_DIR%pack_kgs_addon.py" %*
) else (
	py "%SCRIPT_DIR%pack_kgs_addon.py" %*
)
exit /b %errorlevel%
