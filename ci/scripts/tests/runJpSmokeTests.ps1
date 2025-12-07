# CI wrapper for jpSmokeTests
# Runs JP braille / JTalk smoke tests in CI environment

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path .).Path
Set-Location $repoRoot

# Install pytest (required for smoke tests)
# Note: We skip overlay since it's already done in buildNVDA job, but we need pytest
Write-Host "Installing pytest for smoke tests..." -ForegroundColor Cyan
uv pip install pytest

# In CI, we skip overlay since it's already done in buildNVDA job
Write-Host "Running JP smoke tests in CI environment..." -ForegroundColor Cyan
& "$repoRoot\jptools\runJpSmokeTests.ps1" -SkipInstall -SkipOverlay

if ($LastExitCode -ne 0) {
    Write-Output "FAIL: JP smoke tests. See test results for more information." >> $env:GITHUB_STEP_SUMMARY
    Write-Output "testFailExitCode=$LastExitCode" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
}

exit $LastExitCode
