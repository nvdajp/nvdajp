# Signs a single file or a list of files with AzureSignTool + Azure Key Vault (GlobalSign HSM).
# Invoked from SCons signExecAzureKv or jptools/buildSynthDriverHost32.ps1.
#
# Authentication (first match wins):
#   1. AZURE_KV_ACCESS_TOKEN  - pre-issued token (GitHub Actions OIDC)
#   2. az account get-access-token  - local `az login` session
#
# Key Vault settings (defaults match shuaruta/code-signing):
#   AZURE_KEY_VAULT_URI, CERT_NAME (certificate name in Key Vault)

# A part of NVDA Japanese fork (nvdajp)
# SPDX-License-Identifier: GPL-2.0-or-later

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$FileToSign = $env:NVDA_SIGN_FILE,

    [Parameter(Mandatory = $false)]
    [string]$FileList
)

$ErrorActionPreference = "Stop"

function Initialize-SigningEnvironment {
    if ([string]::IsNullOrEmpty($env:USERPROFILE)) {
        $env:USERPROFILE = [Environment]::GetFolderPath("UserProfile")
    }
    if ([string]::IsNullOrEmpty($env:ProgramFiles)) {
        $env:ProgramFiles = [Environment]::GetEnvironmentVariable("ProgramFiles", "Machine")
    }
    if ([string]::IsNullOrEmpty($env:ProgramFiles)) {
        $env:ProgramFiles = "C:\Program Files"
    }
    if ([string]::IsNullOrEmpty(${env:ProgramFiles(x86)})) {
        $pf86 = [Environment]::GetEnvironmentVariable("ProgramFiles(x86)", "Machine")
        if ($pf86) {
            Set-Item -Path "Env:ProgramFiles(x86)" -Value $pf86
        }
    }
}

function Join-SigningPath {
    param(
        [string]$Parent,
        [string]$Child
    )
    if ([string]::IsNullOrEmpty($Parent)) {
        return $null
    }
    return Join-Path $Parent $Child
}

function Initialize-SigningToolPath {
    Initialize-SigningEnvironment
    $extraPaths = @(
        (Join-SigningPath $env:USERPROFILE ".dotnet\tools")
        (Join-SigningPath $env:ProgramFiles "dotnet")
        (Join-SigningPath $env:ProgramFiles "Microsoft SDKs\Azure\CLI2\wbin")
    )
    if (${env:ProgramFiles(x86)}) {
        $extraPaths += @(
            (Join-SigningPath ${env:ProgramFiles(x86)} "dotnet")
            (Join-SigningPath ${env:ProgramFiles(x86)} "Microsoft SDKs\Azure\CLI2\wbin")
        )
    }
    foreach ($dir in $extraPaths) {
        if ($dir -and (Test-Path -LiteralPath $dir) -and $env:PATH -notlike "*$dir*") {
            $env:PATH = "$dir;$env:PATH"
        }
    }
}

function Ensure-AzureSignTool {
    Initialize-SigningToolPath
    $toolExe = Join-SigningPath $env:USERPROFILE ".dotnet\tools\azuresigntool.exe"
    if ($toolExe -and (Test-Path -LiteralPath $toolExe)) {
        return $toolExe
    }
    $tool = Get-Command azuresigntool -ErrorAction SilentlyContinue
    if ($tool) {
        return $tool.Source
    }
    $dotnet = Get-Command dotnet -ErrorAction SilentlyContinue
    if ($dotnet) {
        $dotnet = $dotnet.Source
    } else {
        $dotnetPath = Join-SigningPath $env:ProgramFiles "dotnet\dotnet.exe"
        if ($dotnetPath -and (Test-Path -LiteralPath $dotnetPath)) {
            $dotnet = $dotnetPath
        }
    }
    if (-not $dotnet) {
        throw @"
AzureSignTool is not installed and dotnet SDK was not found.
Install once from an interactive shell:
  dotnet tool install --global AzureSignTool
"@
    }
    Write-Host "Installing AzureSignTool..."
    & $dotnet tool install --global AzureSignTool | Out-Null
    Initialize-SigningToolPath
    if ($toolExe -and (Test-Path -LiteralPath $toolExe)) {
        return $toolExe
    }
    $tool = Get-Command azuresigntool -ErrorAction SilentlyContinue
    if (-not $tool) {
        throw "AzureSignTool is not available after install."
    }
    return $tool.Source
}

function Find-SignToolExe {
    Initialize-SigningEnvironment
    $tool = Get-Command signtool -ErrorAction SilentlyContinue
    if ($tool) {
        return $tool.Source
    }
    $kitsRoot = Join-SigningPath ${env:ProgramFiles(x86)} "Windows Kits\10\bin"
    if ($kitsRoot -and (Test-Path -LiteralPath $kitsRoot)) {
        $candidate = Get-ChildItem -Path $kitsRoot -Filter signtool.exe -Recurse -ErrorAction SilentlyContinue |
            Where-Object { $_.FullName -match '\\x64\\' } |
            Sort-Object FullName -Descending |
            Select-Object -First 1
        if ($candidate) {
            return $candidate.FullName
        }
    }
    return $null
}

function Get-KeyVaultAccessToken {
    Initialize-SigningToolPath
    $token = $env:AZURE_KV_ACCESS_TOKEN
    if ($token) {
        return $token
    }
    $az = Get-Command az -ErrorAction SilentlyContinue
    if ($az) {
        $token = az account get-access-token --resource https://vault.azure.net --query accessToken -o tsv 2>$null
        if ($LASTEXITCODE -eq 0 -and $token) {
            $token = $token.Trim()
            Write-Host "::add-mask::$token"
            return $token
        }
    }
    throw @"
Azure Key Vault signing credentials are not available.
Set one of:
  - AZURE_KV_ACCESS_TOKEN
  - az login (Azure CLI session)
"@
}

$files = @()
$useFileList = $false

if ($FileList) {
    $FileList = $FileList.Trim().Trim('"')
    if (-not (Test-Path -LiteralPath $FileList)) {
        throw "File list not found: $FileList"
    }
    $files = Get-Content -LiteralPath $FileList |
        ForEach-Object { $_.Trim().Trim('"') } |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
    if ($files.Count -eq 0) {
        Write-Host "FileList is empty: $FileList. Nothing to sign."
        exit 0
    }
    foreach ($file in $files) {
        if (-not (Test-Path -LiteralPath $file)) {
            throw "File to sign not found: $file (from $FileList)"
        }
    }
    $useFileList = $true
} elseif ($FileToSign) {
    $FileToSign = $FileToSign.Trim().Trim('"')
    if (-not (Test-Path -LiteralPath $FileToSign)) {
        throw "File to sign not found: $FileToSign"
    }
    $files = @($FileToSign)
} else {
    throw "File to sign not specified. Pass -FileToSign, -FileList, or set NVDA_SIGN_FILE."
}

$keyVaultUri = if ($env:AZURE_KEY_VAULT_URI) { $env:AZURE_KEY_VAULT_URI } else { "https://shuaruta-codesign-kv.vault.azure.net/" }
$certName = if ($env:CERT_NAME) { $env:CERT_NAME } else { "shuaruta-codesign" }
$timestampUrl = if ($env:TIMESTAMP_URL) { $env:TIMESTAMP_URL } elseif ($env:TIMESERVER) { $env:TIMESERVER } else { "http://timestamp.digicert.com" }

$azureSignTool = Ensure-AzureSignTool
$accessToken = Get-KeyVaultAccessToken

$signArgs = @(
    "sign",
    "-kvu", $keyVaultUri,
    "-kvc", $certName,
    "-kva", $accessToken,
    "-tr", $timestampUrl,
    "-fd", "sha256",
    "-v"
)

if ($useFileList) {
    $signArgs += @("-s", "-ifl", $FileList)
} else {
    $signArgs += $FileToSign
}

& $azureSignTool @signArgs
if ($LASTEXITCODE -ne 0) {
    $targetDesc = if ($useFileList) { "FileList: $FileList" } else { $FileToSign }
    throw "AzureSignTool failed for $targetDesc (exit $LASTEXITCODE)"
}

$signtool = Find-SignToolExe
if ($signtool) {
    # Verify in chunks of up to 50 files to avoid command line length limits
    $batchSize = 50
    for ($i = 0; $i -lt $files.Count; $i += $batchSize) {
        $chunk = $files[$i..([Math]::Min($i + $batchSize - 1, $files.Count - 1))]
        & $signtool verify /pa @chunk
        if ($LASTEXITCODE -ne 0) {
            throw "signtool verify failed in batch starting at index $i"
        }
    }
} else {
    foreach ($file in $files) {
        $sig = Get-AuthenticodeSignature -LiteralPath $file
        if ($sig.Status -ne "Valid") {
            throw "Signature verification failed for ${file}: $($sig.Status)"
        }
    }
}
