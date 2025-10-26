@echo off
REM Check for problematic VS 2022 versions using PowerShell to avoid CMD quoting issues
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$p=[Environment]::GetFolderPath('ProgramFilesX86')+'\Microsoft Visual Studio\Installer\vswhere.exe';" ^
  "if(Test-Path $p){ $v=& $p -format value -property catalog.productDisplayVersion -products * -version '[17.0,18.0)'; if($v -eq '17.14.8'){ exit 8 } else { exit 0 } } else { exit 0 }"
if "%ERRORLEVEL%"=="8" (
    echo Warning: VS 2022 v17.14.8 detected - known to cause LNK1120 build errors
    if "%GITHUB_ACTIONS%"=="true" (
        echo GitHub Actions environment - continuing with warning
        exit /b 0
    ) else (
        echo Please downgrade to v17.14.5 or use a different version
        exit /b 1
    )
)
exit /b 0
