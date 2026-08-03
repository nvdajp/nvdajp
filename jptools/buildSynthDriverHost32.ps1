<#
.SYNOPSIS
    Builds and optionally signs the synthDriverHost32 runtime (32-bit Python for SAPI4/5).
.DESCRIPTION
    Used by certBuild2023.cmd and certBuild2025.ps1.
    Signing uses Azure Key Vault (AZURE_KV_SIGNING). Reads SKIP_SIGNING from environment.
#>
[CmdletBinding()]
param(
    [switch]$SkipSigning
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$synthDriverHost32Dir = Join-Path $repoRoot "runtime-builders\synthDriverHost32"
$synthDriverHost32Dest = Join-Path $repoRoot "source\lib\x86\synthDriverHost-runtime"

# Ensure parent directory exists (py2exe in setup-runtime.py does mkdir(destdir) and fails if source\lib\x86 is missing)
$destParent = Split-Path -Parent $synthDriverHost32Dest
if (-not (Test-Path -LiteralPath $destParent)) {
    New-Item -ItemType Directory -Path $destParent -Force | Out-Null
}

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

# Azure Key Vault signing is the only supported signing method.
$signScript = Join-Path $repoRoot "ci\scripts\signAzureKV.ps1"

$filesToSign = Get-ChildItem -Path $synthDriverHost32Dest -Recurse -Include "*.exe", "*.dll" -File
foreach ($file in $filesToSign) {
    Write-Host "  Signing: $($file.Name)" -ForegroundColor Gray
    & pwsh -NoProfile -ExecutionPolicy Bypass -File $signScript -FileToSign $file.FullName
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to sign $($file.FullName) with Azure Key Vault"
        exit 1
    }
}
Write-Host "synthDriverHost32 runtime files signed successfully ($($filesToSign.Count) files)" -ForegroundColor Green
