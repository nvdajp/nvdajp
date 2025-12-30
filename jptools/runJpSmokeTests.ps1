<#
.SYNOPSIS
    Runs the JP braille / JTalk smoke tests locally with the same steps as CI.

.DESCRIPTION
    1. Optionally installs the minimal tooling (uv pip install scons).
    2. Optionally runs "scons.bat jtalkSync" to prepare JTalk assets (DLLs and dictionaries).
    3. Sets PYTHONPATH so that python-jtalk + source/synthDrivers/jtalk are importable.
    4. Invokes "uv run python -m unittest miscDepsJp.jptools.test" (or specific test classes/methods).

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

# Set UV_PYTHON_PREFERENCE to ensure uv uses managed Python
# This ensures consistent behavior between local and CI environments
if (-not $env:UV_PYTHON_PREFERENCE) {
    $env:UV_PYTHON_PREFERENCE = "managed"
    Write-Host "Set UV_PYTHON_PREFERENCE=managed"
}

# Setup log file for all output
$logFile = Join-Path $repoRoot "jpSmokeTests.log"
# Start transcript to capture all output to log file
Start-Transcript -Path $logFile -Append | Out-Null
Write-Host "REPO_ROOT set to $repoRoot"
Write-Host "Log file: $logFile"

# Determine build architecture from BUILD_ARCH environment variable
# BUILD_ARCH is JP-specific for smoke test environment switching
# TARGET_ARCH is SCons environment variable and should not be used as OS environment variable
$buildArch = if ($env:BUILD_ARCH) { $env:BUILD_ARCH } else { "x86" }
Write-Host "Build architecture: $buildArch"

# For x64 builds, use x64 Python and separate venv (.venv-x64)
# For x86 builds, use x86 Python and default venv (.venv)
if ($buildArch -eq "x64") {
    Write-Host "x64 build detected: using x64 Python and .venv-x64"
    # Ensure x64 Python 3.13 is available
    Write-Host "Ensuring Python 3.13 x64 is available..."
    & uv python install 3.13
    if (-not $?) {
        Write-Error "uv python install failed"
        Stop-Transcript | Out-Null
        exit 1
    }
    # Use separate venv for x64 to avoid conflicts with x86 .venv
    $venvX64 = Join-Path $repoRoot ".venv-x64"
    $pythonExe = Join-Path $venvX64 "Scripts\python.exe"
    if (-not (Test-Path $pythonExe)) {
        Write-Host "Creating x64 virtual environment..."
        & uv venv $venvX64 --python 3.13
        if (-not $?) {
            Write-Error "Failed to create x64 virtual environment"
            Stop-Transcript | Out-Null
            exit 1
        }
        $pythonExe = Join-Path $venvX64 "Scripts\python.exe"
    }
} else {
    # x86 build: use default .venv
    $pythonExe = Join-Path $repoRoot ".venv\Scripts\python.exe"
    if (-not (Test-Path $pythonExe)) {
        $pythonExe = "python"
    }
}
Write-Host "Using Python: $pythonExe"

function Test-UnittestAvailable {
    # unittest is part of the Python standard library, so it's always available.
    # Compatibility shim: this function is retained for older scripts/CI jobs that still
    # invoke Test-UnittestAvailable, but it is effectively a no-op and always returns $true.
    # TODO: Remove this function once all external callers have been updated to stop using it.
    return $true
}

function Install-Packages {
    param(
        [string[]]$Packages,
        [string]$VenvPath = ""
    )
    Write-Host "Installing dependencies: $($Packages -join ', ')"
    $installOk = $false
    try {
        if ($VenvPath) {
            # Use specific venv for installation
            & uv pip install --python $pythonExe @Packages
        } else {
            & uv pip install @Packages
        }
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
        Write-Host "JTalk dictionaries not found under $JtalkSource; running scons jtalkSync..."
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
        Initializes MSVC environment variables (PATH, INCLUDE, LIB, etc.) for the specified architecture.
        This ensures tools like dumpbin, cl, nmake are available in the current PowerShell session.
        Currently supports Visual Studio 2022 only.
    #>
    param(
        [string]$Architecture = "x86"
    )
    
    # For x64 builds, always set up environment to ensure x64 tools are used
    # For x86 builds, check if cl is already available (fast path)
    if ($Architecture -eq "x86") {
        try {
            $null = Get-Command cl -ErrorAction Stop
            Write-Host "MSVC environment already configured (cl is available)"
            return
        } catch {
            # cl not found, need to set up environment
        }
    }

    # VS 2022: Search in BuildTools, Community, Professional, Enterprise order
    # Note: This logic is shared with jptools/scons_jp.py via jptools/vs_utils.py
    # For consistency, we use the same search order here
    $editions = @("BuildTools", "Community", "Professional", "Enterprise")
    $vcvarsall = $null
    
    foreach ($edition in $editions) {
        $path = "C:\Program Files\Microsoft Visual Studio\2022\$edition\VC\Auxiliary\Build\vcvarsall.bat"
        if (Test-Path $path) {
            $vcvarsall = $path
            break
        }
    }

    if (-not $vcvarsall) {
        Write-Warning "Visual Studio 2022 vcvarsall.bat not found. MSVC tools (dumpbin, cl, nmake) may not be available."
        Write-Warning "You may need to manually run 'vcvarsall.bat $Architecture' in a Developer Command Prompt."
        return
    }

    Write-Host "Setting up MSVC environment for $Architecture using: $vcvarsall"
    
    # Run vcvarsall.bat with the specified architecture and capture environment variables
    $envOutput = cmd /c "`"$vcvarsall`" $Architecture >nul 2>&1 && set"
    
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
        Write-Host "MSVC environment configured ($envVarsSet environment variables set)"
        
        # Verify dumpbin is available
        try {
            $null = Get-Command dumpbin -ErrorAction Stop
            Write-Host "dumpbin is now available"
        } catch {
            Write-Warning "dumpbin is still not available after MSVC environment setup"
        }
    } else {
        Write-Warning "Failed to set MSVC environment variables"
    }
}

$packages = @()
if (-not $SkipInstall) {
    # Always refresh scons when not skipping install
    $packages = @("scons")
}

if (-not $SkipInstall) {
    $venvPath = if ($buildArch -eq "x64") { Join-Path $repoRoot ".venv-x64" } else { Join-Path $repoRoot ".venv" }
    Install-Packages -Packages $packages -VenvPath $venvPath
}

# Initialize MSVC environment for local runs (needed for dumpbin, cl, nmake)
# CI environments already have MSVC environment set up via ilammy/msvc-dev-cmd@v1
if (-not $isCI) {
    Initialize-MsvcEnvironment -Architecture $buildArch
}

if (-not $SkipOverlay) {
    # In CI, check cache first to avoid unnecessary builds
    if ($isCI) {
        $dllPath = Join-Path $repoRoot "source\synthDrivers\jtalk\libopenjtalk.dll"
        if (Test-Path $dllPath) {
            Write-Host "JTalk DLL found in cache, skipping jtalkSync"
        } else {
            Write-Host "JTalk DLL not found in cache, running jtalkSync..."
            & "$repoRoot\scons.bat" jtalkSync
            if ($LastExitCode -ne 0) {
                Write-Error "Failed to run scons jtalkSync with exit code $LastExitCode"
                exit $LastExitCode
            }
        }
    } else {
        Write-Host "Preparing JTalk assets via scons jtalkSync..."
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
# Also add miscDepsJp/jptools so test.py can import jpBrailleRunner, etc.
$pythonJtalk = Join-Path $repoRoot "miscDepsJp\include\python-jtalk"
$jptoolsDir = Join-Path $repoRoot "miscDepsJp\jptools"
$env:PYTHONPATH = "$jtalkSource;$pythonJtalk;$jptoolsDir"
Write-Host "PYTHONPATH set to $($env:PYTHONPATH)"

# Set max tests environment variable if specified
if ($MaxTests -gt 0) {
    $env:JP_SMOKE_MAX_TESTS = $MaxTests.ToString()
    Write-Host "Limiting tests to $MaxTests"
}

# Set test indices environment variable if specified
if ($TestIndices -ne "") {
    $env:JP_SMOKE_TEST_INDICES = $TestIndices
    Write-Host "Running tests at indices: $TestIndices"
}

Write-Host "Running JP braille/JTalk smoke tests (filter: $TestFilter)..."
# unittest can run test.py directly with module path notation
# Examples:
#   "JpBrailleTests" -> miscDepsJp.jptools.test.JpBrailleTests
#   "JpBrailleTests.test_pass2" -> miscDepsJp.jptools.test.JpBrailleTests.test_pass2
#   "JpBrailleTests or JtalkTests" -> run both classes separately
# Default: run JpBrailleTests and JtalkTests
$testModule = "miscDepsJp.jptools.test"
$unittestArgs = @()

if ($TestFilter -and $TestFilter -ne "JpBrailleTests or JtalkTests") {
    # Convert filter to unittest module path format
    if ($TestFilter -match "\.test_") {
        # Specific test method: "JpBrailleTests.test_pass2"
        $unittestArgs = @("$testModule.$TestFilter")
    } elseif ($TestFilter -match " or ") {
        # Multiple classes: "JpBrailleTests or JtalkTests"
        $classes = $TestFilter -split " or " | ForEach-Object { $_.Trim() }
        $unittestArgs = $classes | ForEach-Object { "$testModule.$_" }
    } else {
        # Single class: "JpBrailleTests"
        $unittestArgs = @("$testModule.$TestFilter")
    }
} else {
    # Default: run JpBrailleTests and JtalkTests
    $unittestArgs = @("$testModule.JpBrailleTests", "$testModule.JtalkTests")
}

# Run tests
$testExitCode = 0
if ($unittestArgs.Count -eq 1) {
    & uv run --python $pythonExe python -m unittest $unittestArgs[0] -v
    $testExitCode = $LastExitCode
} else {
    # Multiple test classes: run each separately and combine exit codes
    $allPassed = $true
    foreach ($testArg in $unittestArgs) {
        & uv run --python $pythonExe python -m unittest $testArg -v
        if ($LastExitCode -ne 0) {
            $allPassed = $false
        }
    }
    if (-not $allPassed) {
        $testExitCode = 1
    } else {
        $testExitCode = 0
    }
}

# CI-specific post-processing
if ($isCI -and $testExitCode -ne 0) {
    Write-Output "FAIL: JP smoke tests. See test results for more information." >> $env:GITHUB_STEP_SUMMARY
    Write-Output "testFailExitCode=$testExitCode" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
}

# Stop transcript before exiting
Stop-Transcript | Out-Null

exit $testExitCode
