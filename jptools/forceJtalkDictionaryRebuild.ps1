<#
.SYNOPSIS
    Forces a clean JTalk / MeCab dictionary rebuild (CI-aligned).

.DESCRIPTION
    Matches testAndPublish.yml "Force JTalk dictionary rebuild" + "Prepare JTalk":
    - Removes source\synthDrivers\jtalk\dic
    - Removes miscDepsJp\_state\prep\jtalkSync.*.stamp
    - Runs scons jtalkPrep jtalkSync under CP932

    Use before JP smoke tests in local cert builds so custom dictionary entries
    (一人→ヒトリ, 二百十日, etc.) are always included.

.EXAMPLE
    chcp 932 >nul 2>&1 && powershell -ExecutionPolicy Bypass -File jptools\forceJtalkDictionaryRebuild.ps1
#>
[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

$null = cmd /c "chcp 932 >nul 2>&1"
try {
    $chcpLine = (cmd /c chcp 2>&1 | Out-String).Trim()
    Write-Host "Console code page: $chcpLine"
} catch {
    Write-Warning "Could not read chcp output: $_"
}

$dicDir = Join-Path $repoRoot "source\synthDrivers\jtalk\dic"
if (Test-Path $dicDir) {
    Remove-Item -Path $dicDir -Recurse -Force
    Write-Host "Removed $dicDir to force fresh dictionary build"
}

$stampDir = Join-Path $repoRoot "miscDepsJp\_state\prep"
if (Test-Path $stampDir) {
    Get-ChildItem $stampDir -Filter "jtalkSync.*.stamp" -ErrorAction SilentlyContinue |
        Remove-Item -Force
    Write-Host "Removed jtalkSync stamp files to force SCons rebuild"
}

$sconsArgs = @("jtalkPrep", "jtalkSync")
if ($env:SCONSOPTIONS) {
    $sconsArgs += ($env:SCONSOPTIONS -split '\s+' | Where-Object { $_ })
}

Write-Host "Running: scons.bat $($sconsArgs -join ' ')"
& "$repoRoot\scons.bat" @sconsArgs
exit $LASTEXITCODE
