<#
.SYNOPSIS
    Runs the JP braille / JTalk smoke tests locally with the same steps as CI.

.DESCRIPTION
    1. Optionally installs the minimal tooling (uv pip install scons pytest).
    2. Optionally runs "scons.bat miscdepsjp" to prepare the overlay.
    3. Sets PYTHONPATH so that python-jtalk + source/synthDrivers/jtalk are importable.
    4. Invokes "uv run python -m pytest miscDepsJp/jptools/test.py -k 'JpBrailleTests or JtalkTests'".

    Use -SkipInstall or -SkipOverlay if you already prepared the environment.
#>
[CmdletBinding()]
param(
    [switch]$SkipInstall,
    [switch]$SkipOverlay
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

Write-Host "Running JP braille/JTalk smoke tests..." -ForegroundColor Cyan
uv run python -m pytest miscDepsJp/jptools/test.py -k "JpBrailleTests or JtalkTests"
