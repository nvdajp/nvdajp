<#
.SYNOPSIS
    Runs the JP braille / JTalk smoke tests locally with the same steps as CI.

.DESCRIPTION
    1. Optionally installs the minimal tooling (uv pip install scons pytest).
    2. Optionally runs "scons.bat jtalkSync" to prepare JTalk assets (DLLs and dictionaries).
    3. Sets PYTHONPATH so that python-jtalk + source/synthDrivers/jtalk are importable.
    4. Invokes "uv run python -m pytest miscDepsJp/jptools/test.py -k 'JpBrailleTests or JtalkTests'".

    Use -SkipInstall or -SkipOverlay if you already prepared the environment.
    Use -TestFilter to run specific tests (e.g., "JpBrailleTests.test_pass2" or "JtalkTests").
    Use -TestIndices to run specific test cases by index (e.g., "11" or "11,12,13").
    
    In CI environments (detected via GITHUB_ACTIONS environment variable), additional CI-specific
    processing is performed (cache checking, GitHub Actions step summary, etc.).

.EXAMPLE
    .\runJpSmokeTests.ps1 -SkipInstall -SkipOverlay -TestFilter "JpBrailleTests.test_pass2"
    Runs only the pass2 test (MeCab-related test).

.EXAMPLE
    .\runJpSmokeTests.ps1 -SkipInstall -TestFilter "test_pass2_tab_characters"
    Runs only test cases containing tab characters (useful for debugging tab character issues).

.EXAMPLE
    .\runJpSmokeTests.ps1 -SkipInstall -TestFilter "test_pass2_no_tab_characters"
    Runs only test cases NOT containing tab characters (useful for testing without tab character issues).

.EXAMPLE
    .\runJpSmokeTests.ps1 -SkipInstall -TestFilter "test_pass2_by_index" -TestIndices "11"
    Runs only test case at index 11 (0-based).
#>
[CmdletBinding()]
param(
    [switch]$SkipInstall,
    [switch]$SkipOverlay,
    [string]$TestFilter = "JpBrailleTests or JtalkTests",
    [int]$MaxTests = 0,
    [string]$TestIndices = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Detect CI environment
$isCI = $env:GITHUB_ACTIONS -eq "true"

# Determine repo root
if ($isCI) {
    # In CI, we're already in the repo root
    $repoRoot = (Resolve-Path .).Path
} else {
    # In local environment, calculate from script location
    $repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}
Set-Location $repoRoot

# Set REPO_ROOT environment variable for long-term maintainability
# This allows scripts to get repo root without depending on miscDepsJp folder structure
$env:REPO_ROOT = $repoRoot
Write-Host "REPO_ROOT set to $repoRoot" -ForegroundColor Cyan

$pythonExe = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python"
}

function Test-PytestPresent {
    # Use uv run to check pytest, since we use uv run to execute tests
    # This ensures we check the same environment that will be used for testing
    try {
        uv run python -m pytest --version 2>&1 | Out-Null
        return $LastExitCode -eq 0
    } catch {
        return $false
    }
}

function Install-Packages {
    param(
        [string[]]$Packages
    )
    Write-Host "Installing dependencies: $($Packages -join ', ')" -ForegroundColor Cyan
    $installOk = $false
    try {
        uv pip install @Packages
        if ($LastExitCode -eq 0) { $installOk = $true }
    } catch {
        Write-Warning "uv is not available; falling back to python -m pip"
    }
    if (-not $installOk) {
        & $pythonExe -m pip install @Packages
    }
    if ($LastExitCode -ne 0) {
        Write-Error "Failed to install dependencies with exit code $LastExitCode"
        exit $LastExitCode
    }
}

function Ensure-JtalkDic {
    param(
        [string]$RepoRoot,
        [string]$JtalkSource
    )
    $charBin = Join-Path $JtalkSource "dic\char.bin"
    if (-not (Test-Path $charBin)) {
        Write-Host "JTalk dictionaries not found under $JtalkSource; running scons jtalkSync..." -ForegroundColor Yellow
        & "$RepoRoot\scons.bat" jtalkSync
        if ($LastExitCode -ne 0) {
            Write-Error "Failed to run scons jtalkSync with exit code $LastExitCode"
            exit $LastExitCode
        }
    }
}

function Initialize-MsvcEnvironment {
    <#
    .SYNOPSIS
        Initializes MSVC environment variables (PATH, INCLUDE, LIB, etc.) for x86 builds.
        This ensures tools like dumpbin, cl, nmake are available in the current PowerShell session.
    #>
    # Check if cl is already available (fast path)
    try {
        $null = Get-Command cl -ErrorAction Stop
        Write-Host "MSVC environment already configured (cl is available)" -ForegroundColor Green
        return
    } catch {
        # cl not found, need to set up environment
    }

    # Try to find vcvarsall.bat in common Visual Studio locations
    # Currently supports Visual Studio 2022 only
    $vcvarsallPaths = @(
        # VS 2022 (Program Files, 64-bit installer)
        "C:\Program Files\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvarsall.bat",
        "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat",
        "C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvarsall.bat",
        "C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvarsall.bat"
    )

    $vcvarsall = $null
    foreach ($path in $vcvarsallPaths) {
        if (Test-Path $path) {
            $vcvarsall = $path
            break
        }
    }

    if (-not $vcvarsall) {
        Write-Warning "vcvarsall.bat not found in common locations. MSVC tools (dumpbin, cl, nmake) may not be available."
        Write-Warning "You may need to manually run 'vcvarsall.bat x86' in a Developer Command Prompt."
        return
    }

    Write-Host "Setting up MSVC environment for x86 using: $vcvarsall" -ForegroundColor Cyan
    
    # Run vcvarsall.bat x86 and capture environment variables
    $envOutput = cmd /c "`"$vcvarsall`" x86 >nul 2>&1 && set"
    
    # Parse environment variables and set them in current PowerShell session
    $envVarsSet = 0
    foreach ($line in $envOutput) {
        if ($line -match '^([^=]+)=(.*)$') {
            $key = $matches[1]
            $value = $matches[2]
            [System.Environment]::SetEnvironmentVariable($key, $value, 'Process')
            $envVarsSet++
        }
    }

    if ($envVarsSet -gt 0) {
        Write-Host "MSVC environment configured ($envVarsSet environment variables set)" -ForegroundColor Green
        
        # Verify dumpbin is available
        try {
            $null = Get-Command dumpbin -ErrorAction Stop
            Write-Host "dumpbin is now available" -ForegroundColor Green
        } catch {
            Write-Warning "dumpbin is still not available after MSVC environment setup"
        }
    } else {
        Write-Warning "Failed to set MSVC environment variables"
    }
}

$packages = @("pytest")
if (-not $SkipInstall) {
    # Always refresh scons/pytest when not skipping install
    $packages = @("scons", "pytest")
}

$needsInstall = (-not $SkipInstall) -or (-not (Test-PytestPresent))
if ($needsInstall) {
    if ($SkipInstall -and (-not (Test-PytestPresent))) {
        Write-Host "pytest not found; installing despite -SkipInstall" -ForegroundColor Yellow
    }
    Install-Packages -Packages $packages
    if (-not (Test-PytestPresent)) {
        Write-Error "pytest is still missing after installation"
        exit 1
    }
}

# Initialize MSVC environment for local runs (needed for dumpbin, cl, nmake)
# CI environments already have MSVC environment set up via ilammy/msvc-dev-cmd@v1
if (-not $isCI) {
    Initialize-MsvcEnvironment
}

if (-not $SkipOverlay) {
    # In CI, check cache first to avoid unnecessary builds
    if ($isCI) {
        $dllPath = Join-Path $repoRoot "source\synthDrivers\jtalk\libopenjtalk.dll"
        if (Test-Path $dllPath) {
            Write-Host "JTalk DLL found in cache, skipping jtalkSync" -ForegroundColor Green
        } else {
            Write-Host "JTalk DLL not found in cache, running jtalkSync..." -ForegroundColor Yellow
            & "$repoRoot\scons.bat" jtalkSync
            if ($LastExitCode -ne 0) {
                Write-Error "Failed to run scons jtalkSync with exit code $LastExitCode"
                exit $LastExitCode
            }
        }
    } else {
        Write-Host "Preparing JTalk assets via scons jtalkSync..." -ForegroundColor Cyan
        & "$repoRoot\scons.bat" jtalkSync
        if ($LastExitCode -ne 0) {
            Write-Error "Failed to run scons jtalkSync with exit code $LastExitCode"
            exit $LastExitCode
        }
    }
}

$jtalkSource = Join-Path $repoRoot "source\synthDrivers\jtalk"
# Ensure dictionaries are present in source/ even when overlay is skipped
Ensure-JtalkDic -RepoRoot $repoRoot -JtalkSource $jtalkSource

# jtalkRunner.py is still in miscDepsJp/include/python-jtalk, so add it to PYTHONPATH
$pythonJtalk = Join-Path $repoRoot "miscDepsJp\include\python-jtalk"
$env:PYTHONPATH = "$jtalkSource;$pythonJtalk"
Write-Host "PYTHONPATH set to $($env:PYTHONPATH)" -ForegroundColor Cyan

# Set max tests environment variable if specified
if ($MaxTests -gt 0) {
    $env:JP_SMOKE_MAX_TESTS = $MaxTests.ToString()
    Write-Host "Limiting tests to $MaxTests" -ForegroundColor Cyan
}

# Set test indices environment variable if specified
if ($TestIndices -ne "") {
    $env:JP_SMOKE_TEST_INDICES = $TestIndices
    Write-Host "Running tests at indices: $TestIndices" -ForegroundColor Cyan
}

Write-Host "Running JP braille/JTalk smoke tests (filter: $TestFilter)..." -ForegroundColor Cyan
# pytest -k option uses expression matching, so we need to handle different formats
# Examples:
#   "test_pass2" -> matches any test_pass2
#   "JpBrailleTests and test_pass2" -> matches test_pass2 in JpBrailleTests
#   "JpBrailleTests" -> matches all tests in JpBrailleTests
if ($TestFilter -match "\.test_") {
    # If filter contains ".test_", split into class and method
    $parts = $TestFilter -split "\.test_"
    if ($parts.Length -eq 2) {
        $className = $parts[0]
        $methodName = "test_" + $parts[1]
        $pytestFilter = "$className and $methodName"
    } else {
        $pytestFilter = $TestFilter
    }
} else {
    $pytestFilter = $TestFilter
}

# Run tests
uv run python -m pytest miscDepsJp/jptools/test.py -k "$pytestFilter"
$testExitCode = $LastExitCode

# CI-specific post-processing
if ($isCI -and $testExitCode -ne 0) {
    Write-Output "FAIL: JP smoke tests. See test results for more information." >> $env:GITHUB_STEP_SUMMARY
    Write-Output "testFailExitCode=$testExitCode" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
}

exit $testExitCode
