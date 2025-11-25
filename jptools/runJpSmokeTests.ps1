<#
.SYNOPSIS
    Runs the JP braille / JTalk smoke tests locally with the same steps as CI.

.DESCRIPTION
    1. Optionally installs the minimal tooling (uv pip install scons pytest).
    2. Optionally runs "scons.bat miscdepsjp" to prepare the overlay.
    3. Sets PYTHONPATH so that python-jtalk + source/synthDrivers/jtalk are importable.
    4. Invokes "uv run python -m pytest miscDepsJp/jptools/test.py -k 'JpBrailleTests or JtalkTests'".

    Use -SkipInstall or -SkipOverlay if you already prepared the environment.
    Use -IncludeThreadSafety to include MeCab thread safety tests.
    Use -RunMecabAccessViolationTest to run the MeCab access violation reproduction script.
#>
[CmdletBinding()]
param(
    [switch]$SkipInstall,
    [switch]$SkipOverlay,
    [switch]$IncludeThreadSafety,
    [switch]$RunMecabAccessViolationTest
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
    Write-Host "Preparing miscDeps overlay via scons..." -ForegroundColor Cyan
    & "$repoRoot\scons.bat" miscdepsjp
}

$env:PYTHONPATH = "miscDepsJp\include\python-jtalk;miscDepsJp\source\synthDrivers\jtalk"
Write-Host "PYTHONPATH set to $($env:PYTHONPATH)" -ForegroundColor Cyan

if ($RunMecabAccessViolationTest) {
    Write-Host "Running MeCab access violation reproduction script..." -ForegroundColor Cyan
    uv run python miscDepsJp/jptools/reproduce_mecab_access_violation.py
} else {
    $testFilter = "JpBrailleTests or JtalkTests"
    if ($IncludeThreadSafety) {
        $testFilter = "JpBrailleTests or JtalkTests or MecabThreadSafetyTests"
        Write-Host "Running JP braille/JTalk smoke tests (including thread safety tests)..." -ForegroundColor Cyan
    } else {
        Write-Host "Running JP braille/JTalk smoke tests..." -ForegroundColor Cyan
    }
    uv run python -m pytest miscDepsJp/jptools/test.py -k $testFilter
}
