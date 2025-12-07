# CI wrapper for jpSmokeTests
# Runs JP braille / JTalk smoke tests in CI environment

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path .).Path
Set-Location $repoRoot

# Install pytest (required for smoke tests)
Write-Host "Installing pytest for smoke tests..." -ForegroundColor Cyan
uv pip install pytest

# Check if DLL exists in cache, if not run jtalkPrep
# Note: jtalkPrep is idempotent - if DLL already exists, it skips the build
$dllPath = Join-Path $repoRoot "miscDepsJp\source\synthDrivers\jtalk\libopenjtalk.dll"
if (Test-Path $dllPath) {
    Write-Host "JTalk DLL found in cache, skipping jtalkPrep" -ForegroundColor Green
} else {
    Write-Host "JTalk DLL not found in cache, running jtalkPrep..." -ForegroundColor Yellow
    & "$repoRoot\scons.bat" jtalkPrep
}

# Run smoke tests (skip install and overlay since we already have everything)
Write-Host "Running JP smoke tests in CI environment..." -ForegroundColor Cyan
& "$repoRoot\jptools\runJpSmokeTests.ps1" -SkipInstall -SkipOverlay

if ($LastExitCode -ne 0) {
    Write-Output "FAIL: JP smoke tests. See test results for more information." >> $env:GITHUB_STEP_SUMMARY
    Write-Output "testFailExitCode=$LastExitCode" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
}

exit $LastExitCode
