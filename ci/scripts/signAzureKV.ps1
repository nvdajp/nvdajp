# Signs a single file with AzureSignTool + Azure Key Vault (GlobalSign HSM).
# Invoked from SCons signExecAzureKv or jptools/buildSynthDriverHost32.ps1.
#
# Authentication (first match wins):
#   1. AZURE_KV_ACCESS_TOKEN  - pre-issued token (GitHub Actions OIDC)
#   2. az account get-access-token  - local `az login` session
#   3. AZURE_CLIENT_SECRET + AZURE_CLIENT_ID + AZURE_TENANT_ID
#
# Key Vault settings (defaults match shuaruta/code-signing):
#   AZURE_KEY_VAULT_URI, CERT_NAME (certificate name in Key Vault)

# A part of NVDA Japanese fork (nvdajp)
# SPDX-License-Identifier: GPL-2.0-or-later

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$FileToSign = $env:NVDA_SIGN_FILE
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
    if ($env:AZURE_KV_ACCESS_TOKEN) {
        return $env:AZURE_KV_ACCESS_TOKEN
    }
    $az = Get-Command az -ErrorAction SilentlyContinue
    if ($az) {
        try {
            $token = & $az.Source account get-access-token --resource https://vault.azure.net --query accessToken -o tsv 2>$null
            if ($LASTEXITCODE -eq 0 -and $token) {
                if ($env:GITHUB_ACTIONS -eq "true") {
                    Write-Host "::add-mask::$token"
                }
                return $token.Trim()
            }
        } catch {
            Write-Warning "az account get-access-token failed: $_"
        }
    }
    throw @"
Azure Key Vault signing credentials are not available.
Set one of:
  - AZURE_KV_ACCESS_TOKEN
  - az login (Azure CLI session)
"@
}

if (-not $FileToSign) {
    throw "File to sign not specified. Pass -FileToSign or set NVDA_SIGN_FILE."
}

$FileToSign = $FileToSign.Trim().Trim('"')

if (-not (Test-Path -LiteralPath $FileToSign)) {
    throw "File to sign not found: $FileToSign"
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
    "-tr", $timestampUrl,
    "-fd", "sha256",
    "-v"
)
if ($accessToken) {
    $signArgs += @("-kva", $accessToken)
} else {
    $signArgs += @(
        "-kvi", $env:AZURE_CLIENT_ID,
        "-kvs", $env:AZURE_CLIENT_SECRET,
        "-kvt", $env:AZURE_TENANT_ID
    )
}
$signArgs += $FileToSign

& $azureSignTool @signArgs
if ($LASTEXITCODE -ne 0) {
    throw "AzureSignTool failed for $FileToSign (exit $LASTEXITCODE)"
}

$signtool = Find-SignToolExe
if ($signtool) {
    & $signtool verify /pa $FileToSign
    if ($LASTEXITCODE -ne 0) {
        throw "signtool verify failed for $FileToSign"
    }
} else {
    $sig = Get-AuthenticodeSignature -LiteralPath $FileToSign
    if ($sig.Status -ne "Valid") {
        throw "Signature verification failed for ${FileToSign}: $($sig.Status)"
    }
}
