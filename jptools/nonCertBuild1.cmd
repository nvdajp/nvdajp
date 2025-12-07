rem Remove duplicate build step - let scons jtalkPrep handle it
rem The build step (build-and-test.cmd) is now handled by scons jtalkPrep
rem which is automatically invoked when scons source is run.
rem This avoids duplicate builds and aligns with vendor-submodules.md policy.

call jptools\check_vs_version.cmd
@if not "%ERRORLEVEL%"=="0" goto onerror

rem Copy JTalk core files only (no build - handled by scons jtalkPrep)
cd miscDepsJp\jptools
call copy_jtalk_core_files.cmd
cd ..\..

rem Setup overlay (no build - handled by scons miscdepsjp)
call jptools\setupMiscDepsJp.cmd

exit /b 0

:onerror
exit /b -1
