<#
.SYNOPSIS
    Merges jptools/nvda-jp-patch.po into source/locale/ja/LC_MESSAGES/nvda.po

.DESCRIPTION
    This script merges JP-specific translations from jptools/nvda-jp-patch.po
    into source/locale/ja/LC_MESSAGES/nvda.po.
    
    The script:
    1. Validates that both files exist
    2. Extracts the JP section from nvda-jp-patch.po (including "# nvdajp from here" to "# end of nvdajp")
    3. If nvda.po already has a JP section (between "# nvdajp from here" and "# end of nvdajp"), replaces it
    4. If not, appends the JP section to the end of nvda.po

.PARAMETER PatchFile
    Path to the JP patch file. Default: jptools/nvda-jp-patch.po

.PARAMETER PoFile
    Path to the main Japanese translation file. Default: source/locale/ja/LC_MESSAGES/nvda.po

.EXAMPLE
    .\merge-jp-patch-po.ps1
    Merges jptools/nvda-jp-patch.po into source/locale/ja/LC_MESSAGES/nvda.po
#>
[CmdletBinding()]
param(
    [string]$PatchFile = "jptools\nvda-jp-patch.po",
    [string]$PoFile = "source\locale\ja\LC_MESSAGES\nvda.po"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

# Resolve paths
$patchPath = Join-Path $repoRoot $PatchFile
$poPath = Join-Path $repoRoot $PoFile

# Validate files exist
if (-not (Test-Path $patchPath)) {
    Write-Error "Patch file not found: $patchPath"
    exit 1
}

if (-not (Test-Path $poPath)) {
    Write-Error "Translation file not found: $poPath"
    exit 1
}

Write-Host "Reading patch file: $patchPath" -ForegroundColor Cyan
$patchLines = Get-Content $patchPath -Encoding UTF8

# Extract JP section (including "# nvdajp from here" and "# end of nvdajp")
$jpSection = @()
$inJpSection = $false

foreach ($line in $patchLines) {
    if ($line -match "^# nvdajp from here") {
        $inJpSection = $true
        $jpSection += $line
        continue
    }
    if ($line -match "^# end of nvdajp") {
        $jpSection += $line
        $inJpSection = $false
        break
    }
    if ($inJpSection) {
        $jpSection += $line
    }
}

if ($jpSection.Count -eq 0) {
    Write-Warning "No JP section found in patch file"
    exit 0
}

Write-Host "Found $($jpSection.Count) lines in JP section (including markers)" -ForegroundColor Green

# Read main PO file
Write-Host "Reading translation file: $poPath" -ForegroundColor Cyan
$poLines = Get-Content $poPath -Encoding UTF8

# Find existing JP section in PO file
$beginIndex = -1
$endIndex = -1

for ($i = 0; $i -lt $poLines.Count; $i++) {
    if ($poLines[$i] -match "^# nvdajp from here") {
        $beginIndex = $i
    }
    if ($poLines[$i] -match "^# end of nvdajp") {
        $endIndex = $i
        break
    }
}

if ($beginIndex -ge 0 -and $endIndex -ge 0 -and $endIndex -ge $beginIndex) {
    # Replace existing JP section
    Write-Host "Found existing JP section at lines $($beginIndex + 1)-$($endIndex + 1), replacing..." -ForegroundColor Yellow
    
    # Remove trailing empty lines before begin marker if any
    while ($beginIndex -gt 0 -and $poLines[$beginIndex - 1] -match '^\s*$') {
        $beginIndex--
    }
    
    # Build new content: lines before JP section + JP section + lines after JP section
    $beforeSection = if ($beginIndex -gt 0) { $poLines[0..($beginIndex - 1)] } else { @() }
    $afterSection = if ($endIndex -lt $poLines.Count - 1) { $poLines[($endIndex + 1)..($poLines.Count - 1)] } else { @() }
    
    # Remove trailing empty lines from before section
    while ($beforeSection.Count -gt 0 -and $beforeSection[-1] -match '^\s*$') {
        $beforeSection = $beforeSection[0..($beforeSection.Count - 2)]
    }
    
    # Combine: before + empty line + JP section + after
    $poLines = $beforeSection + @("") + $jpSection + $afterSection
    
    Write-Host "Replaced existing JP section with $($jpSection.Count) lines" -ForegroundColor Green
} else {
    # Append JP section to the end
    Write-Host "No existing JP section found, appending to end..." -ForegroundColor Yellow
    
    # Remove trailing empty lines from PO file
    while ($poLines.Count -gt 0 -and $poLines[-1] -match '^\s*$') {
        $poLines = $poLines[0..($poLines.Count - 2)]
    }
    
    # Append JP section
    $poLines += ""
    $poLines += $jpSection
    
    Write-Host "Appended $($jpSection.Count) lines to end of file" -ForegroundColor Green
}

# Write combined content
$outputContent = $poLines -join "`n"
[System.IO.File]::WriteAllText($poPath, $outputContent, [System.Text.Encoding]::UTF8)

Write-Host "Merge completed successfully!" -ForegroundColor Green
Write-Host "Updated file: $poPath" -ForegroundColor Cyan
