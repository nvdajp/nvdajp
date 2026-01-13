<#
.SYNOPSIS
    Finds which test cases cause crashes by running each test individually.

.DESCRIPTION
    This script runs each test case individually to identify which ones cause Windows fatal exceptions.
    Results are saved to a markdown file.

.PARAMETER SkipInstall
    Skip installing uv dependencies.

.PARAMETER SkipOverlay
    Skip running scons miscdepsjp overlay.

.PARAMETER StartIndex
    Start index for test cases (0-based). Default: 0.

.PARAMETER EndIndex
    End index for test cases (0-based, exclusive). Default: all tests.

.PARAMETER OutputFile
    Output markdown file path. Default: "crashing_tests_report.md"

.EXAMPLE
    .\findCrashingTests.ps1 -SkipInstall -StartIndex 0 -EndIndex 20
    Tests test cases 0-19 individually.
#>
[CmdletBinding()]
param(
    [switch]$SkipInstall,
    [switch]$SkipOverlay,
    [int]$StartIndex = 0,
    [int]$EndIndex = -1,
    [string]$OutputFile = "crashing_tests_report.md"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

if (-not $SkipInstall) {
    Write-Host "Installing uv dependencies (scons)..." -ForegroundColor Cyan
    uv pip install scons
}

if (-not $SkipOverlay) {
    Write-Host "Preparing miscDeps overlay via scons..." -ForegroundColor Cyan
    & "$repoRoot\scons.bat" miscdepsjp
}

$env:PYTHONPATH = "miscDepsJp\include\python-jtalk;miscDepsJp\source\synthDrivers\jtalk"

# First, get the total number of test cases and build index mapping
Write-Host "Counting total test cases..." -ForegroundColor Cyan
$countScript = @"
import sys
import os
import json
jptools_dir = os.path.join('miscDepsJp', 'jptools')
sys.path.insert(0, jptools_dir)
from harness import tests
from nabccHarness import tests as nabcc_tests
tests.extend(nabcc_tests)
# Build mapping: valid_test_index -> original_test_index
valid_to_original = {}
original_to_valid = {}
valid_idx = 0
for orig_idx, t in enumerate(tests):
    if 'input' in t:
        valid_to_original[valid_idx] = orig_idx
        original_to_valid[orig_idx] = valid_idx
        valid_idx += 1
result = {
    'total_valid': len(valid_to_original),
    'valid_to_original': valid_to_original,
    'original_to_valid': original_to_valid
}
print(json.dumps(result))
"@
$mappingJson = uv run python -c $countScript 2>&1
$mapping = $mappingJson | ConvertFrom-Json
$totalTests = $mapping.total_valid
Write-Host "Total test cases: $totalTests" -ForegroundColor Cyan

if ($EndIndex -eq -1) {
    $EndIndex = [int]$totalTests
}

$results = @()
$crashingTests = @()
$passedTests = @()
$failedTests = @()

Write-Host "Testing indices $StartIndex to $($EndIndex - 1)..." -ForegroundColor Cyan

for ($idx = $StartIndex; $idx -lt $EndIndex; $idx++) {
    Write-Host "Testing index $idx..." -ForegroundColor Yellow

    # Convert valid index to original index
    if (-not $mapping.valid_to_original.PSObject.Properties.Name -contains $idx.ToString()) {
        Write-Host "  Index $idx is out of range, skipping..." -ForegroundColor Red
        continue
    }
    $originalIdx = $mapping.valid_to_original.$idx

    # Get test case info
    $infoScript = @"
import sys
import os
import json
jptools_dir = os.path.join('miscDepsJp', 'jptools')
sys.path.insert(0, jptools_dir)
from harness import tests
from nabccHarness import tests as nabcc_tests
tests.extend(nabcc_tests)
if $originalIdx < len(tests) and 'input' in tests[$originalIdx]:
    test = tests[$originalIdx]
    info = {
        'original_index': $originalIdx,
        'text': test.get('text', ''),
        'input': test.get('input', ''),
        'has_tab': '\t' in test.get('text', '')
    }
    print(json.dumps(info, ensure_ascii=False))
else:
    print(json.dumps({'error': 'Index out of range'}, ensure_ascii=False))
"@

    $testInfoJson = uv run python -c $infoScript 2>&1 | Where-Object { $_ -notmatch '^WARNING|^ERROR' }
    try {
        $testInfo = $testInfoJson | ConvertFrom-Json
    } catch {
        Write-Host "  Failed to parse test info JSON, skipping..." -ForegroundColor Red
        Write-Host "  JSON output: $testInfoJson" -ForegroundColor Gray
        continue
    }

    if ($testInfo.PSObject.Properties.Name -contains 'error') {
        Write-Host "  Index $idx (original $originalIdx) is out of range, skipping..." -ForegroundColor Red
        continue
    }

    $testText = $testInfo.text
    if ($testText.Length -gt 50) {
        $testText = $testText.Substring(0, 50) + "..."
    }
    Write-Host "  Test: $testText (original index: $originalIdx)" -ForegroundColor Gray

    # Run the test using original index
    $env:JP_SMOKE_TEST_INDICES = $originalIdx.ToString()
    # The JpBrailleTests.test_pass2 unittest reads JP_SMOKE_TEST_INDICES to select
    # which individual test case to run, replacing the old pytest-style
    # test_pass2_by_index helper. No additional per-index test method is required.
    $unittestOutput = uv run python -m unittest miscDepsJp.jptools.test.JpBrailleTests.test_pass2 -v 2>&1
    $exitCode = $LASTEXITCODE

    $result = [PSCustomObject]@{
        Index = $idx
        OriginalIndex = $testInfo.original_index
        Text = $testInfo.text
        Input = $testInfo.input
        HasTab = $testInfo.has_tab
        Status = "Unknown"
        ExitCode = $exitCode
    }

    # Check for Windows fatal exception
    $outputStr = $unittestOutput -join "`n"
    if ($outputStr -match "Windows fatal exception" -or $exitCode -ne 0) {
        if ($outputStr -match "Windows fatal exception") {
            $result.Status = "CRASH"
            $crashingTests += $result
            Write-Host "  CRASH detected!" -ForegroundColor Red
        } else {
            $result.Status = "FAILED"
            $failedTests += $result
            Write-Host "  Failed (exit code: $exitCode)" -ForegroundColor Yellow
        }
    } else {
        $result.Status = "PASSED"
        $passedTests += $result
        Write-Host "  Passed" -ForegroundColor Green
    }

    $results += $result

    # Small delay to avoid overwhelming the system
    Start-Sleep -Milliseconds 100
}

# Generate markdown report
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$mdContent = @"
# Crashing Tests Report

Generated: $timestamp

## Summary

- Total tests run: $($results.Count)
- Crashed: $($crashingTests.Count)
- Failed: $($failedTests.Count)
- Passed: $($passedTests.Count)

## Crashed Tests (Windows Fatal Exception)

"@

if ($crashingTests.Count -eq 0) {
    $mdContent += "No crashes detected in the tested range.`n`n"
} else {
    $mdContent += "| Index | Original Index | Text | Input | Has Tab |`n"
    $mdContent += "|-------|----------------|------|-------|---------|`n"
    foreach ($test in $crashingTests) {
        $textEscaped = $test.Text -replace '\|', '\|' -replace '\n', ' '
        $inputEscaped = $test.Input -replace '\|', '\|'
        $mdContent += "| $($test.Index) | $($test.OriginalIndex) | ``$textEscaped`` | ``$inputEscaped`` | $($test.HasTab) |`n"
    }
    $mdContent += "`n"
}

$mdContent += @"
## Failed Tests (Non-Crash Errors)

"@

if ($failedTests.Count -eq 0) {
    $mdContent += "No failures detected in the tested range.`n`n"
} else {
    $mdContent += "| Index | Original Index | Text | Input | Has Tab | Exit Code |`n"
    $mdContent += "|-------|----------------|------|-------|---------|-----------|`n"
    foreach ($test in $failedTests) {
        $textEscaped = $test.Text -replace '\|', '\|' -replace '\n', ' '
        $inputEscaped = $test.Input -replace '\|', '\|'
        $mdContent += "| $($test.Index) | $($test.OriginalIndex) | ``$textEscaped`` | ``$inputEscaped`` | $($test.HasTab) | $($test.ExitCode) |`n"
    }
    $mdContent += "`n"
}

$mdContent += @"
## All Test Results

| Index | Original Index | Text | Input | Has Tab | Status |
|-------|----------------|------|-------|---------|--------|
"@

foreach ($test in $results) {
    $textEscaped = $test.Text -replace '\|', '\|' -replace '\n', ' '
    $inputEscaped = $test.Input -replace '\|', '\|'
    $mdContent += "| $($test.Index) | $($test.OriginalIndex) | ``$textEscaped`` | ``$inputEscaped`` | $($test.HasTab) | $($test.Status) |`n"
}

$mdContent | Out-File -FilePath $OutputFile -Encoding UTF8
Write-Host "`nReport saved to: $OutputFile" -ForegroundColor Cyan
Write-Host "Crashed: $($crashingTests.Count), Failed: $($failedTests.Count), Passed: $($passedTests.Count)" -ForegroundColor Cyan
