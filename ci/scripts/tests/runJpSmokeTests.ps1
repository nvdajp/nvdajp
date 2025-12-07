# CI wrapper for jpSmokeTests
# Runs JP braille / JTalk smoke tests in CI environment

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path .).Path
Set-Location $repoRoot

# Install pytest (required for smoke tests)
Write-Host "Installing pytest for smoke tests..." -ForegroundColor Cyan
uv pip install pytest

# Ensure jtalkPrep is done (creates miscDepsJp/source/synthDrivers/jtalk/ directory and DLL)
# Note: jtalkPrep is idempotent - if DLL already exists, it skips the build
# This ensures the directory structure exists even if cache doesn't include it
Write-Host "Ensuring JTalk DLL is prepared via scons jtalkPrep..." -ForegroundColor Cyan
& "$repoRoot\scons.bat" jtalkPrep

# Run smoke tests (skip install and overlay since we already have everything)
Write-Host "Running JP smoke tests in CI environment..." -ForegroundColor Cyan
& "$repoRoot\jptools\runJpSmokeTests.ps1" -SkipInstall -SkipOverlay

if ($LastExitCode -ne 0) {
    Write-Output "FAIL: JP smoke tests. See test results for more information." >> $env:GITHUB_STEP_SUMMARY
    Write-Output "testFailExitCode=$LastExitCode" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
}

exit $LastExitCode
