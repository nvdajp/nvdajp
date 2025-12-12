<#
.SYNOPSIS
    Builds NVDA JP with code signing and runs tests.

.DESCRIPTION
    This script wraps certBuild2023.cmd and runs unit tests and system tests.
    It sets up the environment variables and calls certBuild2023.cmd with appropriate parameters.

.PARAMETER VersionBuild
    Version build number. If not specified, certBuild2023.cmd will use its default (1).

.PARAMETER SConsOptions
    Additional SCons options to pass to certBuild2023.cmd (e.g., "--all-cores").
    Can be specified multiple times or as a space-separated string.

.PARAMETER SkipUnitTests
    Skip running unit tests.

.PARAMETER SkipSystemTests
    Skip running system tests.

.EXAMPLE
    .\jptools\certBuild2025.ps1
    Builds with default settings (version_build=1 from certBuild2023.cmd).

.EXAMPLE
    .\jptools\certBuild2025.ps1 -VersionBuild 123 --all-cores
    Builds with version_build=123 and --all-cores option.

.EXAMPLE
    .\jptools\certBuild2025.ps1 -SkipSystemTests
    Builds and runs unit tests only, skipping system tests.
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [int]$VersionBuild = 0,
    
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$SConsOptions = @(),
    
    [switch]$SkipUnitTests,
    [switch]$SkipSystemTests
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Determine repo root from script location
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

# Set up environment variables
# Load CERT_SHA1 from environment or optional env file to avoid committing secrets
$envScript = Join-Path $PSScriptRoot "certBuild2025Env.ps1"
if (-not $env:CERT_SHA1) {
    if (Test-Path $envScript) {
        . $envScript
    } else {
        Write-Error "CERT_SHA1 is not set. Set it in the environment or create certBuild2025Env.ps1 from certBuild2025Env.sample.ps1."
        exit 1
    }
}
if (-not $env:CERT_SHA1) {
    Write-Error "CERT_SHA1 is empty after loading the environment. Aborting."
    exit 1
}
$env:PYTHONUTF8 = "1"
$env:RELEASE = "1"

# Get NOWDATE from nowdate.cmd
$nowdateScript = Join-Path $PSScriptRoot "nowdate.cmd"
$nowdateOutput = & cmd /c $nowdateScript 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to get NOWDATE from nowdate.cmd"
    exit 1
}
$env:NOWDATE = ($nowdateOutput | Out-String).Trim()
$env:VERSION = "jpalpha_$env:NOWDATE"
$env:UPDATEVERSIONTYPE = "nvdajpalpha"
$env:PUBLISHER = "nvdajp"

# Build command arguments for certBuild2023.cmd
$scriptPath = Join-Path $PSScriptRoot "certBuild2023.cmd"
$buildArgs = @()

# Add version_build if specified
if ($VersionBuild -gt 0) {
    $buildArgs += "version_build=$VersionBuild"
}

# Add additional SCons options
$buildArgs += $SConsOptions

# Build the command line
$buildArgsString = $buildArgs -join " "

Write-Host "Building with certBuild2023.cmd..." -ForegroundColor Cyan
if ($buildArgsString) {
    Write-Host "Arguments: $buildArgsString" -ForegroundColor Gray
}

# Call certBuild2023.cmd directly (it handles its own directory changes)
# certBuild2023.cmd uses %* to receive all arguments, so we pass them as a single string
# Environment variables set in PowerShell are automatically inherited by cmd
$certBuildCmd = $scriptPath
$cmdArgs = if ($buildArgsString) { $buildArgsString } else { "" }

Write-Host "Environment variables:" -ForegroundColor Cyan
Write-Host "  VERSION=$env:VERSION" -ForegroundColor Gray
Write-Host "  PUBLISHER=$env:PUBLISHER" -ForegroundColor Gray
Write-Host "  RELEASE=$env:RELEASE" -ForegroundColor Gray
Write-Host "  NOWDATE=$env:NOWDATE" -ForegroundColor Gray

Write-Host "Executing: cmd /c `"$certBuildCmd $cmdArgs`"" -ForegroundColor Gray
& cmd /c "`"$certBuildCmd`" $cmdArgs"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Build failed with exit code $LASTEXITCODE"
    exit 1
}

# Run unit tests
if (-not $SkipUnitTests) {
    Write-Host "`nRunning unit tests..." -ForegroundColor Cyan
    $unitTestScript = Join-Path $repoRoot "rununittests.bat"
    if (Test-Path $unitTestScript) {
        & cmd /c $unitTestScript
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Unit tests failed with exit code $LASTEXITCODE"
            exit 1
        }
    } else {
        Write-Warning "rununittests.bat not found, skipping unit tests"
    }
}

# Run system tests
if (-not $SkipSystemTests) {
    $systemTestScript = Join-Path $repoRoot "runsystemtests.bat"
    if (-not (Test-Path $systemTestScript)) {
        Write-Warning "runsystemtests.bat not found, skipping system tests"
    } else {
        Write-Host "`nRunning system tests (Chrome)..." -ForegroundColor Cyan
        & cmd /c $systemTestScript "--include" "chrome"
        if ($LASTEXITCODE -ne 0) {
            Write-Error "System tests (Chrome) failed with exit code $LASTEXITCODE"
            exit 1
        }

        Write-Host "`nRunning system tests (NVDA)..." -ForegroundColor Cyan
        & cmd /c $systemTestScript "--include" "NVDA" "--exclude" "restarts_on_crash" "--exclude" "vscode" "--exclude" "symbols" "--exclude" "imageDescriptions"
        if ($LASTEXITCODE -ne 0) {
            Write-Error "System tests (NVDA) failed with exit code $LASTEXITCODE"
            exit 1
        }
    }
}

Write-Host "`nBuild and tests completed successfully!" -ForegroundColor Green
exit 0
