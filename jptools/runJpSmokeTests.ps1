<#
.SYNOPSIS
    Runs the JP braille / JTalk smoke tests locally with the same steps as CI.

.DESCRIPTION
    1. Optionally installs the minimal tooling (uv pip install scons pytest).
    2. Optionally runs "scons.bat jtalkSync" to prepare JTalk assets (DLLs and dictionaries).
    3. Sets PYTHONPATH so that python-jtalk + source/synthDrivers/jtalk are importable.
    4. Invokes "uv run python -m pytest miscDepsJp/jptools/test.py -k 'JpBrailleTests or JtalkTests'".

    Use -SkipInstall or -SkipJtalkSync if you already prepared the environment.
    Use -TestFilter to run specific tests (e.g., "JpBrailleTests.test_pass2" or "JtalkTests").
    Use -TestIndices to run specific test cases by index (e.g., "11" or "11,12,13").
    
    In CI environments (detected via GITHUB_ACTIONS environment variable), additional CI-specific
    processing is performed (cache checking, GitHub Actions step summary, etc.).

.EXAMPLE
    .\runJpSmokeTests.ps1 -SkipInstall -SkipJtalkSync -TestFilter "JpBrailleTests.test_pass2"
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
    [switch]$SkipJtalkSync,
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

function Ensure-MecabDictIndex {
    param(
        [string]$RepoRoot
    )
    # Check if mecab-dict-index.exe exists in the build output location
    # (built by scons jtalkSync)
    $mecabDictIndex = Join-Path $RepoRoot "miscDepsJp\include\python-jtalk\libopenjtalk\mecab\src\mecab-dict-index.exe"
    # Rebuild mecab-dict-index.exe when sources are newer (e.g. utils.h JP PATCH changes)
    $mecabUtilsH = Join-Path $RepoRoot "miscDepsJp\include\python-jtalk\libopenjtalk\mecab\src\utils.h"
    $mecabSrcDir = Split-Path -Parent $mecabDictIndex
    $mecabUtilsObj = Join-Path $mecabSrcDir "utils.obj"
    
    $needsRebuild = $false
    if (Test-Path $mecabDictIndex) {
        if (Test-Path $mecabUtilsH) {
            $exeTime = (Get-Item $mecabDictIndex).LastWriteTimeUtc
            $hdrTime = (Get-Item $mecabUtilsH).LastWriteTimeUtc
            if ($hdrTime -gt $exeTime) {
                $needsRebuild = $true
            }
            # Header-only changes may not trigger a rebuild if object files are already present.
            # Detect stale objects too (utils.obj is built from code that includes utils.h).
            if ((-not $needsRebuild) -and (Test-Path $mecabUtilsObj)) {
                $objTime = (Get-Item $mecabUtilsObj).LastWriteTimeUtc
                if ($hdrTime -gt $objTime) {
                    $needsRebuild = $true
                }
            }
        }
    }

    if ((-not (Test-Path $mecabDictIndex)) -or $needsRebuild) {
        if ($needsRebuild) {
            Write-Host "mecab-dict-index.exe is older than utils.h; forcing rebuild..." -ForegroundColor Yellow
            # Makefile.mak may not track header dependencies reliably on some setups.
            # Force rebuild by removing object files so nmake must recompile.
            Remove-Item -Force -ErrorAction SilentlyContinue (Join-Path $mecabSrcDir "*.obj")
            Remove-Item -Force -ErrorAction SilentlyContinue (Join-Path $mecabSrcDir "*_dll.obj")
            Remove-Item -Force -ErrorAction SilentlyContinue $mecabDictIndex
        } else {
            Write-Host "mecab-dict-index.exe not found; running scons jtalkSync to build it..." -ForegroundColor Yellow
        }
        & "$RepoRoot\scons.bat" jtalkSync
        if ($LastExitCode -ne 0) {
            Write-Error "Failed to run scons jtalkSync with exit code $LastExitCode"
            exit $LastExitCode
        }
        # Verify it was built
        if (-not (Test-Path $mecabDictIndex)) {
            Write-Warning "mecab-dict-index.exe still not found after jtalkSync. User dictionary tests may fail."
        }
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

if (-not $SkipJtalkSync) {
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
# Ensure mecab-dict-index.exe is available for user dictionary tests
Ensure-MecabDictIndex -RepoRoot $repoRoot

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
