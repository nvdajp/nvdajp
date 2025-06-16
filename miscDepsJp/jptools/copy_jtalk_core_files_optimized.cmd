@echo off
rem copy_jtalk_core_files_optimized.cmd
rem 重複実行を防ぐためのマーカーファイルを使用

set MARKER_FILE=.jtalk_core_files_copied
set FORCE_COPY=%1

if exist %MARKER_FILE% if not "%FORCE_COPY%"=="force" (
    echo copy_jtalk_core_files: Already copied. Skipping...
    goto :eof
)

echo copy_jtalk_core_files: Copying files...

xcopy /E /Y .\jtalk ..\include\jtalk
if errorlevel 1 goto :error

xcopy /E /Y ..\include\htsengineapi ..\include\python-jtalk\htsengineapi
if errorlevel 1 goto :error

xcopy /E /Y ..\include\libopenjtalk ..\include\python-jtalk\libopenjtalk
if errorlevel 1 goto :error

copy /Y ..\include\python-jtalk\jtalkCore.py ..\source\synthDrivers\jtalk\jtalkCore.py
if errorlevel 1 goto :error

copy /Y ..\include\python-jtalk\mecab.py ..\source\synthDrivers\jtalk\mecab.py
if errorlevel 1 goto :error

copy /Y ..\include\python-jtalk\text2mecab.py ..\source\synthDrivers\jtalk\text2mecab.py
if errorlevel 1 goto :error

copy /Y ..\include\python-jtalk\jtalkRunner.py .\jtalkRunner.py
if errorlevel 1 goto :error

rem マーカーファイルを作成
echo %date% %time% > %MARKER_FILE%
echo copy_jtalk_core_files: Completed successfully
goto :eof

:error
echo copy_jtalk_core_files: Error occurred during file copy
exit /b 1