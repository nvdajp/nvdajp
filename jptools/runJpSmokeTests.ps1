<#
.SYNOPSIS
    Runs the JP braille / JTalk smoke tests locally with the same steps as CI.

.DESCRIPTION
    1. Optionally installs the minimal tooling (uv pip install scons pytest).
    2. Optionally runs "scons.bat miscdepsjp" to prepare the overlay.
    3. Sets PYTHONPATH so that python-jtalk + source/synthDrivers/jtalk are importable.
    4. Invokes "uv run pytest miscDepsJp/jptools/test.py -k 'JpBrailleTests or JtalkTests'".

    Use -SkipInstall or -SkipOverlay if you already prepared the environment.
    Use -TestFilter to run specific tests (e.g., "JpBrailleTests.test_pass2" or "JtalkTests").
    Use -TestIndices to run specific test cases by index (e.g., "11" or "11,12,13").
    Use -Architecture to specify target architecture (x86 or x64, default: x86).
    Use -Parallel to run tests for both x86 and x64 architectures in parallel (requires -SkipOverlay).
    
    In CI environments (detected via GITHUB_ACTIONS environment variable), additional CI-specific
    processing is performed (cache checking, GitHub Actions step summary, etc.).

.EXAMPLE
    .\runJpSmokeTests.ps1 -SkipInstall -SkipOverlay -TestFilter "JpBrailleTests.test_pass2"
    Runs only the pass2 test (MeCab-related test) for x86 architecture.

.EXAMPLE
    .\runJpSmokeTests.ps1 -SkipInstall -TestFilter "test_pass2_tab_characters"
    Runs only test cases containing tab characters (useful for debugging tab character issues).

.EXAMPLE
    .\runJpSmokeTests.ps1 -SkipInstall -TestFilter "test_pass2_no_tab_characters"
    Runs only test cases NOT containing tab characters (useful for testing without tab character issues).

.EXAMPLE
    .\runJpSmokeTests.ps1 -SkipInstall -TestFilter "test_pass2_by_index" -TestIndices "11"
    Runs only test case at index 11 (0-based).

.EXAMPLE
    .\runJpSmokeTests.ps1 -SkipInstall -SkipOverlay -Architecture x64 -TestFilter "JtalkTests"
    Runs JtalkTests for x64 architecture (requires x64 DLLs to be built separately).

.EXAMPLE
    .\runJpSmokeTests.ps1 -SkipInstall -SkipOverlay -Parallel -TestFilter "JtalkTests"
    Runs JtalkTests for both x86 and x64 architectures in parallel (requires both architectures' DLLs to be built separately).
#>
[CmdletBinding()]
param(
    [switch]$SkipInstall,
    [switch]$SkipOverlay,
    [string]$TestFilter = "JpBrailleTests or JtalkTests",
    [int]$MaxTests = 0,
    [string]$TestIndices = "",
    [ValidateSet("x86", "x64")]
    [string]$Architecture = "x86",
    [switch]$Parallel
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Allow JP_TARGET_ARCH environment variable to override default architecture when not explicitly specified
if (-not $PSBoundParameters.ContainsKey("Architecture")) {
    if ($env:JP_TARGET_ARCH) {
        $Architecture = $env:JP_TARGET_ARCH
        Write-Host "JP_TARGET_ARCH detected; using Architecture=$Architecture" -ForegroundColor Cyan
    }
}

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

function Resolve-JtalkPaths {
    param(
        [Parameter(Mandatory = $true)][ValidateSet("x86", "x64")]$Arch
    )
    $pythonBase = Join-Path $repoRoot "miscDepsJp\include\python-jtalk"
    $overlayBase = Join-Path $repoRoot "miscDepsJp\source\synthDrivers\jtalk"

    $archPython = Join-Path $pythonBase $Arch
    $archOverlay = Join-Path $overlayBase $Arch

    if (Test-Path $archPython) {
        $pythonPath = $archPython
    } else {
        $pythonPath = $pythonBase
    }

    if (Test-Path $archOverlay) {
        $overlayPath = $archOverlay
    } else {
        $overlayPath = $overlayBase
    }

    [PSCustomObject]@{
        PythonPath = $pythonPath
        OverlayPath = $overlayPath
    }
}

function Invoke-JpSmoke {
    param(
        [Parameter(Mandatory = $true)][ValidateSet("x86", "x64")]$Arch
    )

    $sconsArch = if ($Arch -eq "x64") { "x86_64" } else { "x86" }
    Write-Host "Using architecture: $Arch (TARGET_ARCH=$sconsArch)" -ForegroundColor Cyan
    $prevJpTargetArch = $env:JP_TARGET_ARCH
    $env:JP_TARGET_ARCH = $Arch
    $prevTargetArch = $env:TARGET_ARCH
    $env:TARGET_ARCH = $sconsArch

    $ensureDeps = $true
    if ($SkipInstall) {
        Write-Host "SkipInstall requested, checking if pytest is available..." -ForegroundColor Cyan
        uv run python -c "import pytest" *> $null
        if ($LastExitCode -eq 0) {
            $ensureDeps = $false
            Write-Host "pytest already available; skipping install." -ForegroundColor Green
        } else {
            Write-Host "pytest not found; installing minimal deps (scons, pytest) despite -SkipInstall." -ForegroundColor Yellow
        }
    }

    if ($ensureDeps) {
        Write-Host "Installing uv dependencies (scons, pytest)..." -ForegroundColor Cyan
        uv pip install scons pytest
        if ($LastExitCode -ne 0) {
            Write-Error "Failed to install dependencies with exit code $LastExitCode"
            $env:TARGET_ARCH = $prevTargetArch
            exit $LastExitCode
        }
    }

    if (-not $SkipOverlay) {
        # In CI, check cache first to avoid unnecessary builds
        if ($isCI) {
            $dllPath = Join-Path $repoRoot "miscDepsJp\source\synthDrivers\jtalk\libopenjtalk.dll"
            if (Test-Path $dllPath) {
                Write-Host "JTalk DLL found in cache, skipping jtalkPrep" -ForegroundColor Green
            } else {
                Write-Host "JTalk DLL not found in cache, running jtalkPrep..." -ForegroundColor Yellow
                & "$repoRoot\scons.bat" jtalkPrep
                if ($LastExitCode -ne 0) {
                    Write-Error "Failed to run scons jtalkPrep with exit code $LastExitCode"
                    $env:TARGET_ARCH = $prevTargetArch
                    exit $LastExitCode
                }
            }
        } else {
            Write-Host "Preparing JTalk DLL via scons jtalkPrep..." -ForegroundColor Cyan
            & "$repoRoot\scons.bat" jtalkPrep
            if ($LastExitCode -ne 0) {
                Write-Error "Failed to run scons jtalkPrep with exit code $LastExitCode"
                $env:TARGET_ARCH = $prevTargetArch
                exit $LastExitCode
            }
        }
        Write-Host "Preparing miscDeps overlay via scons..." -ForegroundColor Cyan
        & "$repoRoot\scons.bat" miscdepsjp
        if ($LastExitCode -ne 0) {
            Write-Error "Failed to run scons miscdepsjp with exit code $LastExitCode"
            $env:TARGET_ARCH = $prevTargetArch
            exit $LastExitCode
        }
    }

    $paths = Resolve-JtalkPaths -Arch $Arch
    $env:PYTHONPATH = "$($paths.PythonPath);$($paths.OverlayPath)"
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
    uv run pytest miscDepsJp/jptools/test.py -k "$pytestFilter"
    $testExitCode = $LastExitCode

    # CI-specific post-processing
    if ($isCI -and $testExitCode -ne 0) {
        Write-Output "FAIL: JP smoke tests. See test results for more information." >> $env:GITHUB_STEP_SUMMARY
        Write-Output "testFailExitCode=$testExitCode" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
    }

    $env:TARGET_ARCH = $prevTargetArch
    $env:JP_TARGET_ARCH = $prevJpTargetArch
    return $testExitCode
}

$scriptPath = $MyInvocation.MyCommand.Path

if ($Parallel) {
    if (-not $SkipOverlay) {
        Write-Error "-Parallel は現状 -SkipOverlay と併用してください。アーキ別の成果物分離が整うまで並行ビルドは安全ではありません。"
        exit 1
    }
    Write-Host "`n=== 並行実行モード: x86/x64 の両方でテストを実行します ===" -ForegroundColor Cyan
    $jobs = @()
    $jobArchMap = @{}
    foreach ($arch in @("x86", "x64")) {
        Write-Host "`n[並行実行] $arch アーキテクチャのジョブを開始..." -ForegroundColor Cyan
        $job = Start-Job -ScriptBlock {
            param(
                $scriptPath,
                $archValue,
                $testFilterValue,
                $maxTestsValue,
                $testIndicesValue,
                $skipInstallValue
            )
            $psArgs = @(
                "-NoLogo", "-NoProfile",
                "-File", $scriptPath,
                "-Architecture", $archValue,
                "-SkipOverlay"
            )
            if ($skipInstallValue) { $psArgs += "-SkipInstall" }
            if ($testFilterValue) { $psArgs += @("-TestFilter", $testFilterValue) }
            if ($maxTestsValue -gt 0) { $psArgs += @("-MaxTests", $maxTestsValue) }
            if ($testIndicesValue -ne "") { $psArgs += @("-TestIndices", $testIndicesValue) }
            
            # 出力をキャプチャするために一時ファイルを使用
            $tempOut = [System.IO.Path]::GetTempFileName()
            $tempErr = [System.IO.Path]::GetTempFileName()
            
            try {
                $proc = Start-Process pwsh -ArgumentList $psArgs -PassThru -Wait -WindowStyle Hidden -RedirectStandardOutput $tempOut -RedirectStandardError $tempErr
                $output = Get-Content $tempOut -Raw -ErrorAction SilentlyContinue
                $errorOutput = Get-Content $tempErr -Raw -ErrorAction SilentlyContinue
                return @{
                    ExitCode = $proc.ExitCode
                    Output = $output
                    Error = $errorOutput
                }
            } finally {
                Remove-Item $tempOut -ErrorAction SilentlyContinue
                Remove-Item $tempErr -ErrorAction SilentlyContinue
            }
        } -ArgumentList $scriptPath, $arch, $TestFilter, $MaxTests, $TestIndices, $SkipInstall
        $jobs += $job
        $jobArchMap[$job.Id] = $arch
    }
    
    Write-Host "`n[並行実行] すべてのジョブの完了を待機中..." -ForegroundColor Cyan
    $results = @{}
    $failed = $false
    
    while ($jobs.Count -gt 0) {
        $completed = $jobs | Where-Object { $_.State -eq "Completed" -or $_.State -eq "Failed" }
        foreach ($job in $completed) {
            $arch = $jobArchMap[$job.Id]
            Write-Host "`n[並行実行] $arch アーキテクチャの結果を受信中..." -ForegroundColor Cyan
            $result = Receive-Job -Job $job -ErrorAction SilentlyContinue
            
            if ($result -is [hashtable]) {
                $results[$arch] = $result
                Write-Host "`n--- $arch アーキテクチャの出力 ---" -ForegroundColor Yellow
                if ($result.Output) {
                    Write-Host $result.Output
                }
                if ($result.Error) {
                    Write-Host $result.Error -ForegroundColor Red
                }
                Write-Host "--- $arch アーキテクチャの終了コード: $($result.ExitCode) ---" -ForegroundColor $(if ($result.ExitCode -eq 0) { "Green" } else { "Red" })
                
                if ($result.ExitCode -ne 0) {
                    Write-Error "[並行実行] $arch アーキテクチャのテストが失敗しました (終了コード: $($result.ExitCode))"
                    $failed = $true
                }
            } else {
                # フォールバック: 古い形式の結果
                $code = $result
                $results[$arch] = @{ ExitCode = $code }
                Write-Host "--- $arch アーキテクチャの終了コード: $code ---" -ForegroundColor $(if ($code -eq 0) { "Green" } else { "Red" })
                if ($code -ne 0) {
                    Write-Error "[並行実行] $arch アーキテクチャのテストが失敗しました (終了コード: $code)"
                    $failed = $true
                }
            }
            
            Remove-Job -Job $job
            $jobs = $jobs | Where-Object { $_.Id -ne $job.Id }
        }
        
        if ($jobs.Count -gt 0) {
            Start-Sleep -Milliseconds 500
        }
    }
    
    Write-Host "`n=== 並行実行の結果サマリー ===" -ForegroundColor Cyan
    foreach ($arch in @("x86", "x64")) {
        if ($results.ContainsKey($arch)) {
            $status = if ($results[$arch].ExitCode -eq 0) { "✓ 成功" } else { "✗ 失敗" }
            $color = if ($results[$arch].ExitCode -eq 0) { "Green" } else { "Red" }
            Write-Host "  $arch : $status (終了コード: $($results[$arch].ExitCode))" -ForegroundColor $color
        } else {
            Write-Host "  $arch : ? 結果不明" -ForegroundColor Yellow
        }
    }
    
    if ($failed) {
        Write-Host "`n[並行実行] 1つ以上のアーキテクチャでテストが失敗しました。" -ForegroundColor Red
        exit 1
    } else {
        Write-Host "`n[並行実行] すべてのアーキテクチャでテストが成功しました。" -ForegroundColor Green
        exit 0
    }
}

$result = Invoke-JpSmoke -Arch $Architecture
exit $result
