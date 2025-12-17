# Check and (optionally) build JTalk payload for a given architecture.
# Usage:
#   pwsh -File jptools/checkJtalkArch.ps1 -Architecture x64
# Options:
#   -Architecture x86|x64 (default x64)
#   -SkipBuild (do not run scons, just check binaries)

param(
    [ValidateSet('x86', 'x64')]
    [string]$Architecture = 'x64',
    [switch]$SkipBuild,
    [switch]$RunSmokeTests
)

$ErrorActionPreference = 'Stop'

function Invoke-DumpbinMachine {
    param(
        [string]$Path,
        [string]$ArchForVcvars
    )
    if (-not (Test-Path $Path)) {
        Write-Host "MISS: $Path"
        return $false
    }
    $dumpbin = 'dumpbin'
    $result = $null
    $dumpbinOk = $true
    try {
        $result = & $dumpbin /headers $Path 2>$null
        if (-not $?) { $dumpbinOk = $false }
    } catch {
        $dumpbinOk = $false
    }
    if (-not $dumpbinOk) {
        # Fallback: run dumpbin via vcvarsall.bat (VS2022 Community)
        $vcvarsall = 'C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat'
        if (-not (Test-Path $vcvarsall)) {
            Write-Host "ERROR: dumpbin not found and vcvarsall.bat missing at expected path."
            return $false
        }
        $cmd = "call `"$vcvarsall`" $ArchForVcvars && dumpbin /headers `"$Path`""
        $result = cmd.exe /c $cmd 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: dumpbin via vcvarsall failed. Open VS Dev Cmd or adjust PATH."
            return $false
        }
    }
    $machineLine = $result | Where-Object { $_ -match 'machine' } | Select-Object -First 1
    if (-not $machineLine) {
        Write-Host "WARN: machine line not found in dumpbin output for $Path"
        return $false
    }
    $isX64 = $machineLine -match '8664'
    $isX86 = $machineLine -match '14C'
    $archText = if ($isX64) { 'x64 (8664)' } elseif ($isX86) { 'x86 (14C)' } else { $machineLine.Trim() }
    $status = if (($ArchForVcvars -eq 'x64' -and $isX64) -or ($ArchForVcvars -eq 'x86' -and $isX86)) { 'OK' } else { 'NG' }
    Write-Host "$($status): $Path -> $archText"
    return $status -eq 'OK'
}

$repoRoot = Split-Path -Parent $PSScriptRoot
if (-not $SkipBuild) {
    Write-Host "Building jtalkSync for $Architecture ..."
    Push-Location $repoRoot
    $oldArch = $env:TARGET_ARCH
    try {
        $env:TARGET_ARCH = $Architecture
        & "$repoRoot\scons.bat" "jtalkSync"
        if (-not $?) { throw "scons failed" }
    } finally {
        $env:TARGET_ARCH = $oldArch
        Pop-Location
    }
}

$payloadDir = Join-Path $repoRoot "source\synthDrivers\jtalk"
$dlls = @(
    (Join-Path $payloadDir "libopenjtalk.dll"),
    (Join-Path $payloadDir "libmecab.dll")
)

$allOk = $true
foreach ($dll in $dlls) {
    $ok = Invoke-DumpbinMachine -Path $dll -ArchForVcvars $Architecture
    if (-not $ok) { $allOk = $false }
}

if ($allOk) {
    Write-Host "Done: payload binaries match $Architecture" -ForegroundColor Green
    if ($RunSmokeTests) {
        Write-Host "Running jp smoke tests for $Architecture ..."
        Push-Location $repoRoot
        $oldArch = $env:TARGET_ARCH
        try {
            $env:TARGET_ARCH = $Architecture
            & pwsh -NoLogo -File "jptools/runJpSmokeTests.ps1" -SkipOverlay
            if (-not $?) { throw "jp smoke tests failed" }
        } finally {
            $env:TARGET_ARCH = $oldArch
            Pop-Location
        }
    }
    exit 0
}
Write-Host "Done: mismatches detected" -ForegroundColor Yellow
exit 1
