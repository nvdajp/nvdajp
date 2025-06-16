@echo off
rem setupMiscDepsJp.cmd
rem 最適化版：all-cleanの重複実行を削減（3回→1回）

cd miscDepsJp
del /Q nvdajp-miscdep.7z
cd include\jtalk

rem jtalkのビルド処理（clean→build→install）
echo setupMiscDepsJp: Cleaning jtalk...
call all-clean.cmd
if errorlevel 1 goto :error

echo setupMiscDepsJp: Building jtalk...
call all-build.cmd
if errorlevel 1 goto :error

echo setupMiscDepsJp: Installing jtalk...
call all-install.cmd
if errorlevel 1 goto :error

rem 一時ファイルのクリーンアップ（all-cleanの一部処理を個別実行）
echo setupMiscDepsJp: Cleaning temporary files...
del /Q *.pyc
cd libopenjtalk\mecab-naist-jdic
rmdir /S /Q dic 2>nul
rmdir /S /Q _temp 2>nul
del /Q nvdajp-custom-dic.csv 2>nul
del /Q nvdajp-eng-dic.csv 2>nul
del /Q nvdajp-roma-dic.csv 2>nul
del /Q nvdajp-tankan-dic.csv 2>nul
cd ..\..\..\..

rem sourceディレクトリの処理
cd source\synthDrivers
rmdir /S /Q espeak-data 2>nul
cd ..\..

rem アーカイブと展開
echo setupMiscDepsJp: Creating archive...
7z a ..\nvdajp-miscdep.7z source
if errorlevel 1 goto :error

cd ..
echo setupMiscDepsJp: Extracting archive...
7z x -y nvdajp-miscdep.7z
if errorlevel 1 goto :error

del /Q nvdajp-miscdep.7z

rem 最終クリーンアップ（all-cleanの代わりに必要な処理のみ）
echo setupMiscDepsJp: Final cleanup...
cd miscDepsJp
cd include\jtalk
del /Q *.pyc 2>nul
del /Q libopenjtalk\lib\libopenjtalk.exp 2>nul
del /Q libopenjtalk\lib\libopenjtalk.lib 2>nul
cd ..\..
del /Q jptools\mecabHarness.pyc 2>nul
del /Q source\synthDrivers\jtalk\mecab.pyc 2>nul

echo setupMiscDepsJp: Completed successfully
goto :eof

:error
echo setupMiscDepsJp: Error occurred (errorlevel %errorlevel%)
exit /b 1