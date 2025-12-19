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

# Disable PowerShell debug mode to prevent hanging in CI
Set-PSDebug -Off
$DebugPreference = 'SilentlyContinue'

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
    $isX64 = $machineLine -match '\b8664\b'
    $isX86 = $machineLine -match '\b14C\b'
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
        if (-not $?) {
            Write-Error "scons failed"
            exit 1
        }
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
                # Use uv to run pytest with Python 3.11 x64.
                # Use separate venv (.venv-x64) to avoid conflicts with x86 .venv.
                $venvX64 = "$repoRoot\.venv-x64"
                $env:PYTHONPATH = "$repoRoot\source\synthDrivers\jtalk;$repoRoot\miscDepsJp\include\python-jtalk"
                
                # Ensure JTalk dictionaries are present (required for smoke tests)
                $jtalkSource = Join-Path $repoRoot "source\synthDrivers\jtalk"
                $charBin = Join-Path $jtalkSource "dic\char.bin"
                if (-not (Test-Path $charBin)) {
                    Write-Host "JTalk dictionaries not found under $jtalkSource; running scons jtalkSync..." -ForegroundColor Yellow
                    & "$repoRoot\scons.bat" jtalkSync
                    if ($LastExitCode -ne 0) {
                        Write-Error "Failed to run scons jtalkSync with exit code $LastExitCode"
                        exit $LastExitCode
                    }
                }
                
                # Ensure x64 Python is available (uv will skip if already installed)
                Write-Host "Ensuring Python 3.11 x64 is available..."
                & uv python install 3.11
                if (-not $?) {
                    Write-Error "uv python install failed"
                    exit 1
                }
                
                # Create venv if it doesn't exist or is incomplete
                $venvPython = "$venvX64\Scripts\python.exe"
                $venvNeedsRecreate = $false
                if (-not (Test-Path $venvPython)) {
                    $venvNeedsRecreate = $true
                } elseif (-not (Test-Path "$venvX64\pyvenv.cfg")) {
                    # Incomplete venv (missing pyvenv.cfg), remove and recreate
                    Write-Host "Incomplete venv detected, removing and recreating..."
                    Remove-Item -Recurse -Force $venvX64 -ErrorAction SilentlyContinue
                    Start-Sleep -Seconds 1
                    $venvNeedsRecreate = $true
                }
                
                if ($venvNeedsRecreate) {
                    Write-Host "Creating x64 virtual environment with Python 3.11.14..."
                    # Use UV_PYTHON_PREFERENCE=only-managed to prefer uv-managed Python (x64)
                    # This prevents uv from using the x86 Python from PATH
                    $oldPreference = $env:UV_PYTHON_PREFERENCE
                    $env:UV_PYTHON_PREFERENCE = "only-managed"
                    try {
                        # Use Python 3.11.14 explicitly to match GitHub Actions environment
                        # Use --clear flag to replace existing directory if it exists
                        & uv venv --python 3.11.14 --clear $venvX64
                    } finally {
                        $env:UV_PYTHON_PREFERENCE = $oldPreference
                    }
                    if (-not $?) {
                        Write-Error "uv venv failed"
                        exit 1
                    }
                    
                    # Verify venv Python is x64
                    $venvPython = "$venvX64\Scripts\python.exe"
                    $pythonArch = & $venvPython -c "import platform; print(platform.architecture()[0])"
                    if ($pythonArch -ne "64bit") {
                        Write-Error "ERROR: venv Python is not x64 ($pythonArch). Ensure x64 Python is installed: uv python install 3.11"
                        exit 1
                    }
                    
                    # Install pytest in the venv
                    Write-Host "Installing pytest in x64 venv..."
                    & uv pip install --python $venvPython pytest
                    if (-not $?) {
                        Write-Error "uv pip install pytest failed"
                        exit 1
                    }
                }
                
                # Run pytest in the x64 venv with timeout to prevent hang on access violation
                # Set PYTHONUTF8=1 to enable UTF-8 mode for console output (handles Unicode characters)
                # Set code page to 932 (Japanese Shift-JIS) to match local environment behavior
                # This ensures consistent behavior for ctypes string handling and MeCab internal processing
                $env:PYTHONUTF8 = "1"
                # Set code page in the process that will run pytest
                # Note: Start-Process creates a new process, so we need to set code page via cmd /c
                # Create a temporary batch file to ensure chcp 932 is executed before python
                # This is more reliable than using && or & in cmd /c
                $batchFile = Join-Path $env:TEMP "run_pytest_x64_$(Get-Date -Format 'yyyyMMddHHmmss').bat"
                $batchContent = @"
@echo off
chcp 932 >nul 2>&1
cd /d "$repoRoot"
"$venvX64\Scripts\python.exe" -m pytest -q miscDepsJp/jptools/test.py -k "JpBrailleTests or JtalkTests"
exit /b %ERRORLEVEL%
"@
                try {
                    $batchContent | Out-File -FilePath $batchFile -Encoding ASCII -NoNewline
                    $process = Start-Process -FilePath $batchFile -PassThru -NoNewWindow -Wait:$false -UseNewEnvironment:$false -WorkingDirectory $repoRoot
                } finally {
                    # Clean up batch file after process completes
                    # Wait for process to finish first, then clean up
                    $process | Wait-Process -Timeout 120 -ErrorAction SilentlyContinue
                    if (-not $process.HasExited) {
                        Write-Warning "pytest timed out after 120 seconds, forcing termination"
                        $process | Stop-Process -Force -ErrorAction SilentlyContinue
                        Write-Error "jp smoke tests timed out"
                        exit 1
                    }
                    # Clean up batch file after process exits
                    Start-Sleep -Milliseconds 500
                    if (Test-Path $batchFile) {
                        Remove-Item $batchFile -Force -ErrorAction SilentlyContinue
                    }
                }
                $process | Wait-Process -Timeout 120 -ErrorAction SilentlyContinue
                if (-not $process.HasExited) {
                    Write-Warning "pytest timed out after 120 seconds, forcing termination"
                    $process | Stop-Process -Force -ErrorAction SilentlyContinue
                    Write-Error "jp smoke tests timed out"
                    exit 1
                }
                if ($process.ExitCode -ne 0) {
                    Write-Error "jp smoke tests failed (exit code: $($process.ExitCode))"
                    exit 1
                }
            } else {
                & pwsh -NoLogo -File "jptools/runJpSmokeTests.ps1" -SkipOverlay
                if (-not $?) {
                    Write-Error "jp smoke tests failed"
                    exit 1
                }
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
