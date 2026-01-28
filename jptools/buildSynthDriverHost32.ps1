<#
.SYNOPSIS
    Builds and optionally signs the synthDriverHost32 runtime (32-bit Python for SAPI4/5).
.DESCRIPTION
    Used by certBuild2023.cmd and certBuild2025.ps1. Reads CERT_SHA1, CERT_NAME, SKIP_SIGNING from environment.
#>
[CmdletBinding()]
param(
    [switch]$SkipSigning
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$synthDriverHost32Dir = Join-Path $repoRoot "runtime-builders\synthDriverHost32"
$synthDriverHost32Dest = Join-Path $repoRoot "source\lib\x86\synthDriverHost-runtime"

# Build
Write-Host "Building synthDriverHost32 runtime..." -ForegroundColor Cyan
$savedUvPython = $env:UV_PYTHON
$savedVirtualEnv = $env:VIRTUAL_ENV
$env:UV_PYTHON = ""
$env:VIRTUAL_ENV = ""

try {
    & uv run --no-active --directory $synthDriverHost32Dir python setup-runtime.py --dest-dir $synthDriverHost32Dest
    if ($LASTEXITCODE -ne 0) {
        Write-Error "synthDriverHost32 runtime build failed with exit code $LASTEXITCODE"
        exit 1
    }
    Write-Host "synthDriverHost32 runtime built successfully" -ForegroundColor Green
} finally {
    $env:UV_PYTHON = $savedUvPython
    $env:VIRTUAL_ENV = $savedVirtualEnv
}

# Sign (unless skipped)
$doSign = -not $SkipSigning -and -not $env:SKIP_SIGNING
if (-not $doSign) {
    Write-Host "Skipping synthDriverHost32 signing (SkipSigning or SKIP_SIGNING)" -ForegroundColor Yellow
    exit 0
}

Write-Host "Signing synthDriverHost32 runtime files..." -ForegroundColor Cyan
$signtool = $env:SIGNTOOL
if (-not $signtool) {
    $cmd = Get-Command signtool -ErrorAction SilentlyContinue
    if ($cmd) { $signtool = $cmd.Source }
}
if (-not $signtool) {
    $kitsBase = "C:\Program Files (x86)\Windows Kits\10\bin"
    if (Test-Path $kitsBase) {
        $kitsDirs = Get-ChildItem $kitsBase -Directory | Sort-Object Name -Descending
        foreach ($kitDir in $kitsDirs) {
            $p = Join-Path $kitDir.FullName "x64\signtool.exe"
            if (Test-Path $p) { $signtool = $p; break }
            $p = Join-Path $kitDir.FullName "x86\signtool.exe"
            if (Test-Path $p) { $signtool = $p; break }
        }
    }
}
if (-not $signtool) {
    Write-Warning "signtool not found, skipping synthDriverHost32 signing"
    exit 0
}

$signArgs = @("sign", "/fd", "SHA256")
if ($env:CERT_SHA1) {
    $certStore = if ($env:CERT_STORE) { $env:CERT_STORE } else { "My" }
    $signArgs += @("/s", $certStore, "/sha1", $env:CERT_SHA1)
    if ($env:CERT_MACHINE_STORE) { $signArgs += "/sm" }
} elseif ($env:CERT_NAME) {
    $certStore = if ($env:CERT_STORE) { $env:CERT_STORE } else { "My" }
    $signArgs += @("/s", $certStore, "/n", $env:CERT_NAME)
    if ($env:CERT_MACHINE_STORE) { $signArgs += "/sm" }
} else {
    $signArgs += "/a"
}
if ($env:TIMESTAMP_URL) {
    $signArgs += @("/tr", $env:TIMESTAMP_URL, "/td", "SHA256")
} elseif ($env:TIMESERVER) {
    $signArgs += @("/tr", $env:TIMESERVER, "/td", "SHA256")
} else {
    $signArgs += @("/tr", "http://timestamp.digicert.com", "/td", "SHA256")
}

$filesToSign = Get-ChildItem -Path $synthDriverHost32Dest -Recurse -Include "*.exe", "*.dll" -File
foreach ($file in $filesToSign) {
    Write-Host "  Signing: $($file.Name)" -ForegroundColor Gray
    $fileSignArgs = $signArgs + @($file.FullName)
    $signed = $false
    for ($retry = 0; $retry -lt 3; $retry++) {
        & $signtool $fileSignArgs 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) { $signed = $true; break }
        Start-Sleep -Seconds 1
    }
    if (-not $signed) {
        Write-Error "Failed to sign $($file.FullName) after 3 attempts"
        exit 1
    }
}
Write-Host "synthDriverHost32 runtime files signed successfully ($($filesToSign.Count) files)" -ForegroundColor Green
