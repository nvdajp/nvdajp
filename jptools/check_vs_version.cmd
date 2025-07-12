@echo off
REM Check for problematic VS 2022 versions
for /f "tokens=*" %%i in ('"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe" -format value -property catalog.productDisplayVersion -products "*" -version [17.0^,18.0^)') do (
    if "%%i"=="17.14.8" (
        echo Error: VS 2022 v17.14.8 detected - known to cause LNK1120 build errors
        echo Please downgrade to v17.14.5 or use a different version
        exit /b 1
    )
)
exit /b 0