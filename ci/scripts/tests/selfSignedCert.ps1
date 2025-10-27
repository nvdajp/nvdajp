param(
    [ValidateSet('create','cleanup')]
    [string]$Mode = 'create',
    [string]$PfxPath = "$PWD/selfsigned.pfx",
    [string]$Subject = 'CN=NVDA-JP CI SelfSigned',
    [string]$Thumbprint = ''
)

$ErrorActionPreference = 'Stop'

if ($Mode -eq 'create') {
    # Create a self-signed code-signing certificate in CurrentUser store and trust it (Root).
    $cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject $Subject -CertStoreLocation 'Cert:\\CurrentUser\\My' -KeyExportPolicy Exportable

    # Trust the certificate by adding to CurrentUser Root store
    $rootStore = New-Object System.Security.Cryptography.X509Certificates.X509Store('Root','CurrentUser')
    $rootStore.Open([System.Security.Cryptography.X509Certificates.OpenFlags]::ReadWrite)
    try { $rootStore.Add($cert) } finally { $rootStore.Close() }

    # Export to PFX (no password for CI use)
    $secPwd = ConvertTo-SecureString -String '' -AsPlainText -Force
    $abs = (Resolve-Path $PfxPath).Path
    Export-PfxCertificate -Cert "Cert:\\CurrentUser\\My\\$($cert.Thumbprint)" -FilePath $abs -Password $secPwd | Out-Null

    # Expose outputs to subsequent steps
    "SELF_SIGNED_PFX=$abs" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
    "SELF_SIGNED_THUMBPRINT=$($cert.Thumbprint)" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
    Write-Output "Created self-signed certificate: $($cert.Thumbprint) -> $abs"
    exit 0
}

if ($Mode -eq 'cleanup') {
    if (-not $Thumbprint) {
        $Thumbprint = $env:SELF_SIGNED_THUMBPRINT
    }
    if (-not $Thumbprint) { exit 0 }

    foreach ($storeName in @('My','Root')) {
        $store = New-Object System.Security.Cryptography.X509Certificates.X509Store($storeName,'CurrentUser')
        $store.Open([System.Security.Cryptography.X509Certificates.OpenFlags]::ReadWrite)
        try {
            $toRemove = $store.Certificates | Where-Object { $_.Thumbprint -replace ' ', '' -eq ($Thumbprint -replace ' ', '') }
            if ($toRemove) { $store.Remove($toRemove) }
        } finally { $store.Close() }
    }
    Write-Output "Removed self-signed certificate: $Thumbprint"
    exit 0
}

Write-Error "Unknown Mode: $Mode"
exit 1

