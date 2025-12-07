<#
.SYNOPSIS
    Runs the JP braille / JTalk smoke tests locally with the same steps as CI.

.DESCRIPTION
    1. Optionally installs the minimal tooling (uv pip install scons pytest).
    2. Optionally runs "scons.bat miscdepsjp" to prepare the overlay.
    3. Sets PYTHONPATH so that python-jtalk + source/synthDrivers/jtalk are importable.
    4. Invokes "uv run python -m pytest miscDepsJp/jptools/test.py -k 'JpBrailleTests or JtalkTests'".

    Use -SkipInstall or -SkipOverlay if you already prepared the environment.
    Use -TestFilter to run specific tests (e.g., "JpBrailleTests.test_pass2" or "JtalkTests").
    Use -TestIndices to run specific test cases by index (e.g., "11" or "11,12,13").

.EXAMPLE
    .\runJpSmokeTests.ps1 -SkipInstall -SkipOverlay -TestFilter "JpBrailleTests.test_pass2"
    Runs only the pass2 test (MeCab-related test).

.EXAMPLE
    .\runJpSmokeTests.ps1 -SkipInstall -TestFilter "test_pass2_tab_characters"
    Runs only test cases containing tab characters (useful for debugging tab character issues).

.EXAMPLE
    .\runJpSmokeTests.ps1 -SkipInstall -TestFilter "test_pass2_no_tab_characters"
    Runs only test cases NOT containing tab characters (useful for testing without tab character issues).

.EXAMPLE
    .\runJpSmokeTests.ps1 -SkipInstall -TestFilter "test_pass2_by_index" -TestIndices "11"
    Runs only test case at index 11 (0-based).
#>
[CmdletBinding()]
param(
    [switch]$SkipInstall,
    [switch]$SkipOverlay,
    [string]$TestFilter = "JpBrailleTests or JtalkTests",
    [int]$MaxTests = 0,
    [string]$TestIndices = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

if (-not $SkipInstall) {
    Write-Host "Installing uv dependencies (scons, pytest)..." -ForegroundColor Cyan
    uv pip install scons pytest
}

if (-not $SkipOverlay) {
    Write-Host "Preparing JTalk DLL via scons jtalkPrep..." -ForegroundColor Cyan
    & "$repoRoot\scons.bat" jtalkPrep
    Write-Host "Preparing miscDeps overlay via scons..." -ForegroundColor Cyan
    & "$repoRoot\scons.bat" miscdepsjp
}

$env:PYTHONPATH = "miscDepsJp\include\python-jtalk;miscDepsJp\source\synthDrivers\jtalk"
Write-Host "PYTHONPATH set to $($env:PYTHONPATH)" -ForegroundColor Cyan

# Set max tests environment variable if specified
if ($MaxTests -gt 0) {
    $env:JP_SMOKE_MAX_TESTS = $MaxTests.ToString()
    Write-Host "Limiting tests to $MaxTests" -ForegroundColor Cyan
}

# Set test indices environment variable if specified
if ($TestIndices -ne "") {
    $env:JP_SMOKE_TEST_INDICES = $TestIndices
    Write-Host "Running tests at indices: $TestIndices" -ForegroundColor Cyan
}

Write-Host "Running JP braille/JTalk smoke tests (filter: $TestFilter)..." -ForegroundColor Cyan
# pytest -k option uses expression matching, so we need to handle different formats
# Examples:
#   "test_pass2" -> matches any test_pass2
#   "JpBrailleTests and test_pass2" -> matches test_pass2 in JpBrailleTests
#   "JpBrailleTests" -> matches all tests in JpBrailleTests
if ($TestFilter -match "\.test_") {
    # If filter contains ".test_", split into class and method
    $parts = $TestFilter -split "\.test_"
    if ($parts.Length -eq 2) {
        $className = $parts[0]
        $methodName = "test_" + $parts[1]
        $pytestFilter = "$className and $methodName"
    } else {
        $pytestFilter = $TestFilter
    }
} else {
    $pytestFilter = $TestFilter
}
uv run python -m pytest miscDepsJp/jptools/test.py -k "$pytestFilter"
