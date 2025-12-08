rem Remove duplicate build step - let scons jtalkPrep handle it
rem The build step (build-and-test.cmd) is now handled by scons jtalkPrep
rem which is automatically invoked when scons source is run.
rem This avoids duplicate builds and aligns with vendor-submodules.md policy.

call jptools\check_vs_version.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror

rem Copy JTalk core files only (no build - handled by scons jtalkPrep)
rem Use Python function instead of .cmd script
uv run python -c "import sys; sys.path.insert(0, 'jptools'); from scons_jp import _copy_jtalk_core_files; from pathlib import Path; exit(_copy_jtalk_core_files(Path('.').resolve()))"
@if not "%ERRORLEVEL%"=="0" goto onerror

rem Setup overlay (no build - handled by scons miscdepsjp)
call jptools\setupMiscDepsJp.cmd

exit /b 0

:onerror
exit /b -1
