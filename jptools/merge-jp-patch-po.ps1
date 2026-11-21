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

$utf8NoBom = New-Object System.Text.UTF8Encoding $false
$jpText = $jpSection -join "`n"

# Read main PO file preserving original line endings outside the JP section
Write-Host "Reading translation file: $poPath" -ForegroundColor Cyan
$poContent = [System.IO.File]::ReadAllText($poPath, $utf8NoBom)

$jpBlockRegex = [regex]'(?ms)^# nvdajp from here\r?\n.*?^# end of nvdajp'
$match = $jpBlockRegex.Match($poContent)

if ($match.Success) {
    Write-Host "Found existing JP section, replacing..." -ForegroundColor Yellow

    $beforeSection = $poContent.Substring(0, $match.Index) -replace '(?:\r?\n[ \t]*)+$', ''
    $afterSection = $poContent.Substring($match.Index + $match.Length)

    if ($beforeSection.Length -gt 0) {
        $outputContent = $beforeSection + "`n`n" + $jpText + $afterSection
    } else {
        $outputContent = $jpText + $afterSection
    }

    Write-Host "Replaced existing JP section with $($jpSection.Count) lines" -ForegroundColor Green
} else {
    # Append JP section to the end
    Write-Host "No existing JP section found, appending to end..." -ForegroundColor Yellow

    $trimmedContent = $poContent -replace '(?:\r?\n[ \t]*)+$', ''
    if ($trimmedContent.Length -gt 0) {
        $outputContent = $trimmedContent + "`n`n" + $jpText
    } else {
        $outputContent = $jpText
    }

    Write-Host "Appended $($jpSection.Count) lines to end of file" -ForegroundColor Green
}

# Write combined content (UTF-8 without BOM)
[System.IO.File]::WriteAllText($poPath, $outputContent, $utf8NoBom)

Write-Host "Merge completed successfully!" -ForegroundColor Green
Write-Host "Updated file: $poPath" -ForegroundColor Cyan
