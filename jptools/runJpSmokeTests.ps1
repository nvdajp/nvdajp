<#
.SYNOPSIS
    Runs the JP braille / JTalk smoke tests locally with the same steps as CI.

.DESCRIPTION
    1. Optionally syncs all dependencies (uv sync) to set up the NVDA build environment.
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
    Write-Host "Syncing NVDA dependencies..." -ForegroundColor Cyan
    & "$repoRoot\ensureuv.ps1" sync
    Write-Host "Installing pytest for JP smoke tests..." -ForegroundColor Cyan
    & "$repoRoot\ensureuv.ps1" pip install pytest
}

if (-not $SkipOverlay) {
    Write-Host "Preparing miscDeps overlay via scons..." -ForegroundColor Cyan
    & "$repoRoot\scons.bat" miscdepsjp
}

$env:PYTHONPATH = "miscDepsJp\include\python-jtalk;miscDepsJp\source\synthDrivers\jtalk"
Write-Host "PYTHONPATH set to $($env:PYTHONPATH)" -ForegroundColor Cyan

Write-Host "Running JP braille/JTalk smoke tests..." -ForegroundColor Cyan
uv run python -m pytest miscDepsJp/jptools/test.py -k "JpBrailleTests or JtalkTests"
