<#
.SYNOPSIS
    Builds NVDA JP with code signing and runs tests.

.DESCRIPTION
    This script wraps certBuild2023.cmd and runs unit tests and system tests.
    It sets up the environment variables and calls certBuild2023.cmd with appropriate parameters.

.PARAMETER VersionBuild
    Version build number. If not specified, SCons default (usually 0) is used.

.PARAMETER SConsOptions
    Additional SCons options to pass to certBuild2023.cmd (e.g., "--all-cores").
    Can be specified multiple times or as a space-separated string.

.PARAMETER SkipUnitTests
    Skip running unit tests.

.PARAMETER SkipSystemTests
    Skip running system tests.

.PARAMETER SkipSignTest
    Skip signtool test (useful for RDP sessions where certificate access may be restricted).

.PARAMETER SkipSigning
    Skip code signing entirely (useful for RDP sessions where certificate access may be restricted).

.EXAMPLE
    .\jptools\certBuild2025.ps1
    Builds with SCons default settings.

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

    [string]$LogPath = "",

    [switch]$SkipUnitTests,
    [switch]$SkipSystemTests,
    [switch]$SkipSignTest,
    [switch]$SkipSigning
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Determine repo root from script location
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

# Set up environment variables
# Load CERT_SHA1 from environment or optional env file to avoid committing secrets
# Skip if SkipSigning is specified
$useAzureKvSigning = $env:AZURE_KV_SIGNING -and $env:AZURE_KV_SIGNING -ne "0"
if (-not $SkipSigning) {
    if ($useAzureKvSigning) {
        Write-Host "Using Azure Key Vault code signing (AZURE_KV_SIGNING)" -ForegroundColor Cyan
        $env:AZURE_KV_SIGNING = "1"
        $env:CERT_SHA1 = ""
        $env:CERT_NAME = ""
    } else {
    $envScript = Join-Path $PSScriptRoot "certBuild2025Env.ps1"
    if (-not $env:CERT_SHA1) {
        if (Test-Path $envScript) {
            . $envScript
        } else {
            Write-Error "CERT_SHA1 is not set. Set it in the environment, create certBuild2025Env.ps1 from certBuild2025Env.sample.ps1, or set AZURE_KV_SIGNING=1."
            exit 1
        }
    }
    if (-not $env:CERT_SHA1) {
        Write-Error "CERT_SHA1 is empty after loading the environment. Aborting."
        exit 1
    }
    }
} else {
    # Clear CERT_SHA1 and CERT_NAME to ensure signing is skipped
    $env:CERT_SHA1 = ""
    $env:CERT_NAME = ""
    # Set SKIP_SIGNING to allow certBuild2023.cmd to skip certificate validation
    $env:SKIP_SIGNING = "1"
    Write-Host "Skipping code signing (SkipSigning specified)" -ForegroundColor Yellow
}
$env:PYTHONUTF8 = "1"
$env:RELEASE = "1"

# Test signtool with a dummy file before building
# This ensures signing environment is properly configured
if ($SkipSignTest) {
    Write-Host "Skipping signtool test (SkipSignTest specified)" -ForegroundColor Yellow
} elseif ($useAzureKvSigning) {
    Write-Host "Skipping signtool test (Azure Key Vault signing)" -ForegroundColor Yellow
} else {
    Write-Host "Testing signtool with dummy file..." -ForegroundColor Cyan
    $msgfmtPath = Join-Path $repoRoot "miscDeps" "tools" "msgfmt.exe"
    if (-not (Test-Path $msgfmtPath)) {
        Write-Warning "msgfmt.exe not found at $msgfmtPath, skipping signtool test"
    } else {
    # Find signtool (similar to certBuild2023.cmd)
    $signtool = $env:SIGNTOOL
    if (-not $signtool) {
        $signtool = Get-Command signtool -ErrorAction SilentlyContinue
        if ($signtool) {
            $signtool = $signtool.Source
        }
    }
    if (-not $signtool) {
        # Try Windows Kits
        $kitsBase = "C:\Program Files (x86)\Windows Kits\10\bin"
        if (Test-Path $kitsBase) {
            $kitsDirs = Get-ChildItem $kitsBase -Directory | Sort-Object Name -Descending
            foreach ($kitDir in $kitsDirs) {
                $signtoolX64 = Join-Path $kitDir.FullName "x64\signtool.exe"
                $signtoolX86 = Join-Path $kitDir.FullName "x86\signtool.exe"
                if (Test-Path $signtoolX64) {
                    $signtool = $signtoolX64
                    break
                } elseif (Test-Path $signtoolX86) {
                    $signtool = $signtoolX86
                    break
                }
            }
        }
    }
    if ($signtool) {
        # Copy msgfmt.exe to temp directory and sign it
        $tempDir = $env:TEMP
        $tempMsgfmt = Join-Path $tempDir "msgfmt_test.exe"
        Write-Host "  Copying $msgfmtPath to $tempMsgfmt" -ForegroundColor Gray
        Copy-Item -Path $msgfmtPath -Destination $tempMsgfmt -Force
        try {
            # Build signtool command similar to certBuild2023.cmd
            $signArgs = @("sign", "/fd", "SHA256")
            if ($env:CERT_SHA1) {
                $certStore = $env:CERT_STORE
                if (-not $certStore) {
                    $certStore = "My"
                }
                $signArgs += @("/s", $certStore, "/sha1", $env:CERT_SHA1)
                if ($env:CERT_MACHINE_STORE) {
                    $signArgs += "/sm"
                }
            } elseif ($env:CERT_NAME) {
                $certStore = $env:CERT_STORE
                if (-not $certStore) {
                    $certStore = "My"
                }
                $signArgs += @("/s", $certStore, "/n", $env:CERT_NAME)
                if ($env:CERT_MACHINE_STORE) {
                    $signArgs += "/sm"
                }
            } else {
                # Fallback to automatic selection
                $signArgs += "/a"
            }
            if ($env:TIMESTAMP_URL) {
                $signArgs += @("/tr", $env:TIMESTAMP_URL, "/td", "SHA256")
            } elseif ($env:TIMESERVER) {
                $signArgs += @("/tr", $env:TIMESERVER, "/td", "SHA256")
            } else {
                # Use HTTP (not HTTPS) for timestamp server:
                # - Microsoft Authenticode specification uses HTTP 1.1 POST for timestamp requests
                # - Only hash values are sent (not original data), so encryption is less critical
                # - HTTP has lower overhead and better compatibility with existing tools
                $signArgs += @("/tr", "http://timestamp.digicert.com", "/td", "SHA256")
            }
            $signArgs += $tempMsgfmt
            Write-Host "  Running: $signtool $($signArgs -join ' ')" -ForegroundColor Gray
            & $signtool $signArgs
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  signtool test completed successfully" -ForegroundColor Green
            } else {
                Write-Error "signtool test failed with exit code $LASTEXITCODE. Code signing environment is not properly configured."
                Write-Error "Please ensure CERT_SHA1 or CERT_NAME is set correctly, and the certificate is accessible."
                exit 1
            }
        } finally {
            # Clean up temp file
            if (Test-Path $tempMsgfmt) {
                Remove-Item -Path $tempMsgfmt -Force -ErrorAction SilentlyContinue
            }
        }
    } else {
        Write-Warning "signtool not found, skipping test"
    }
    }
}

# Get NOWDATE from nowdate.cmd
$nowdateScript = Join-Path $PSScriptRoot "nowdate.cmd"
$nowdateOutput = & cmd /c $nowdateScript 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to get NOWDATE from nowdate.cmd"
    exit 1
}
$env:NOWDATE = ($nowdateOutput | Out-String).Trim()
if (-not $env:VERSION) {
    $env:VERSION = "jpalpha_$env:NOWDATE"
}
if (-not $env:UPDATEVERSIONTYPE) {
    $env:UPDATEVERSIONTYPE = "nvdajpalpha"
}
if (-not $env:PUBLISHER) {
    $env:PUBLISHER = "nvdajp"
}

# Optional logging: tee output of invoked cmd/bat into a file.
if ($LogPath -eq "") {
    $outputDir = Join-Path $repoRoot "output"
    New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
    $LogPath = Join-Path $outputDir ("{0}_certBuild2025.log" -f $env:VERSION)
}
Write-Host "Logging cmd output to: $LogPath" -ForegroundColor Cyan

# Build command arguments for certBuild2023.cmd
$scriptPath = Join-Path $PSScriptRoot "certBuild2023.cmd"
$buildArgs = @()

# Add version_build if specified
if ($VersionBuild -gt 0) {
    $buildArgs += "version_build=$VersionBuild"
}

# Add additional SCons options
$buildArgs += $SConsOptions

# Default to -j1 if no parallel build option is specified
# Check if user explicitly specified -j, --num-jobs, or --all-cores
$hasParallelOption = $false
foreach ($arg in $SConsOptions) {
    if ($arg -match '^-j(\d+)?$|^--num-jobs=|^--all-cores') {
        $hasParallelOption = $true
        break
    }
}
if (-not $hasParallelOption) {
    $buildArgs += "-j1"
}

# Build the command line
$buildArgsString = $buildArgs -join " "

# synthDriverHost32 is built and signed inside certBuild2023.cmd via jptools\buildSynthDriverHost32.ps1

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
if ($cmdArgs) {
    cmd /c "`"$certBuildCmd`" $cmdArgs" 2>&1 | Tee-Object -FilePath $LogPath -Append
} else {
    cmd /c "`"$certBuildCmd`"" 2>&1 | Tee-Object -FilePath $LogPath -Append
}
if ($LASTEXITCODE -ne 0) {
    Write-Error "Build failed with exit code $LASTEXITCODE"
    exit 1
}

# Run unit tests
if (-not $SkipUnitTests) {
    Write-Host "`nRunning unit tests..." -ForegroundColor Cyan
    $unitTestScript = Join-Path $repoRoot "rununittests.bat"
    if (Test-Path $unitTestScript) {
        cmd /c $unitTestScript 2>&1 | Tee-Object -FilePath $LogPath -Append
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
        cmd /c $systemTestScript "--include" "chrome" 2>&1 | Tee-Object -FilePath $LogPath -Append
        if ($LASTEXITCODE -ne 0) {
            Write-Error "System tests (Chrome) failed with exit code $LASTEXITCODE"
            exit 1
        }

        Write-Host "`nRunning system tests (NVDA)..." -ForegroundColor Cyan
        cmd /c $systemTestScript "--include" "NVDA" "--exclude" "restarts_on_crash" "--exclude" "vscode" "--exclude" "symbols" "--exclude" "imageDescriptions" 2>&1 | Tee-Object -FilePath $LogPath -Append
        if ($LASTEXITCODE -ne 0) {
            Write-Error "System tests (NVDA) failed with exit code $LASTEXITCODE"
            exit 1
        }
    }
}

Write-Host "`nBuild and tests completed successfully!" -ForegroundColor Green
exit 0
