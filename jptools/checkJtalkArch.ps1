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
        # Fallback: run dumpbin via vcvarsall.bat
        # Try multiple Visual Studio installation paths (Community, Enterprise, Professional, BuildTools)
        $vcvarsallPaths = @(
            'C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat',
            'C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvarsall.bat',
            'C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvarsall.bat',
            'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat'
        )
        # Also try VSINSTALLDIR environment variable if set
        if ($env:VSINSTALLDIR) {
            $vcvarsallFromEnv = Join-Path $env:VSINSTALLDIR "VC\Auxiliary\Build\vcvarsall.bat"
            if (Test-Path $vcvarsallFromEnv) {
                $vcvarsallPaths = @($vcvarsallFromEnv) + $vcvarsallPaths
            }
        }
        $vcvarsall = $null
        foreach ($p in $vcvarsallPaths) {
            if (Test-Path $p) {
                $vcvarsall = $p
                break
            }
        }
        if (-not $vcvarsall) {
            Write-Host "ERROR: dumpbin not found and vcvarsall.bat not found in common paths."
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
            if ($Architecture -eq 'x64') {
                # Use uv to run pytest with Python 3.11 x64 (uv will install if needed).
                # Use separate venv (.venv-x64) to avoid conflicts with x86 .venv.
                # Ensure PYTHONPATH is set for JTalk modules.
                $venvX64 = "$repoRoot\.venv-x64"
                $env:PYTHONPATH = "$repoRoot\source\synthDrivers\jtalk;$repoRoot\miscDepsJp\include\python-jtalk"
                # Create venv if it doesn't exist
                if (-not (Test-Path "$venvX64\Scripts\python.exe")) {
                    & uv venv --python 3.11 $venvX64
                    if (-not $?) { throw "uv venv failed" }
                    # Install pytest in the venv using uv pip
                    & uv pip install --python "$venvX64\Scripts\python.exe" pytest
                    if (-not $?) { throw "uv pip install pytest failed" }
                }
                # Run pytest in the x64 venv
                & "$venvX64\Scripts\python.exe" -m pytest -q miscDepsJp/jptools/test.py -k "JpBrailleTests or JtalkTests"
                if (-not $?) { throw "jp smoke tests failed" }
            } else {
                & pwsh -NoLogo -File "jptools/runJpSmokeTests.ps1" -SkipOverlay
                if (-not $?) { throw "jp smoke tests failed" }
            }
        } finally {
            $env:TARGET_ARCH = $oldArch
            Pop-Location
        }
    }
    exit 0
}
Write-Host "Done: mismatches detected" -ForegroundColor Yellow
exit 1
