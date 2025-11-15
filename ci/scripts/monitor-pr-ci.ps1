# Monitor PR CI status and provide advice on failures
# Usage: .\ci\scripts\monitor-pr-ci.ps1 -PrNumber 573 [-Watch]

param(
    [Parameter(Mandatory=$true)]
    [int]$PrNumber,
    
    [switch]$Watch
)

$ErrorActionPreference = "Stop"

function Get-PrCiStatus {
    param([int]$Number)
    
    Write-Host "`n=== PR #$Number CI Status ===" -ForegroundColor Cyan
    
    # Get PR info
    $pr = gh pr view $Number --json number,title,state,statusCheckRollup,url,mergeable,mergeStateStatus,headRefName,baseRefName
    if (-not $pr) {
        Write-Host "Error: Could not fetch PR #$Number" -ForegroundColor Red
        return $null
    }
    
    $prObj = $pr | ConvertFrom-Json
    Write-Host "Title: $($prObj.title)" -ForegroundColor Yellow
    Write-Host "State: $($prObj.state)" -ForegroundColor $(if ($prObj.state -eq "OPEN") { "Green" } else { "Gray" })
    Write-Host "Branch: $($prObj.headRefName) -> $($prObj.baseRefName)" -ForegroundColor Gray
    $mergeStatus = if ($prObj.mergeStateStatus) { $prObj.mergeStateStatus } else { "unknown" }
    Write-Host "Mergeable: $($prObj.mergeable) ($mergeStatus)" -ForegroundColor $(if ($prObj.mergeable -and $mergeStatus -eq "CLEAN") { "Green" } else { "Yellow" })
    Write-Host "URL: $($prObj.url)" -ForegroundColor Gray
    
    # Get check status
    Write-Host "`n--- CI Checks ---" -ForegroundColor Cyan
    $checks = gh pr checks $Number
    if ($checks) {
        $checkLines = $checks -split "`n" | Where-Object { $_ -match '\S' }
        $failed = @()
        $inProgress = @()
        $passed = @()
        $skipped = @()
        
        foreach ($line in $checkLines) {
            if ($line -match '^([^\t]+)\t+(\w+)\t+(\d+[smh]?)\t+(.+)$') {
                $name = $matches[1].Trim()
                $state = $matches[2].Trim()
                $duration = $matches[3].Trim()
                $url = $matches[4].Trim()
                
                $checkObj = @{
                    name = $name
                    state = $state
                    duration = $duration
                    url = $url
                }
                
                if ($state -eq "pending" -or $state -eq "in_progress") {
                    $inProgress += $checkObj
                    Write-Host "  [$state] $name" -ForegroundColor Yellow
                } elseif ($state -eq "pass" -or $state -eq "success") {
                    $passed += $checkObj
                    Write-Host "  [PASS] $name ($duration)" -ForegroundColor Green
                } elseif ($state -eq "fail" -or $state -eq "failure") {
                    $failed += $checkObj
                    Write-Host "  [FAIL] $name ($duration)" -ForegroundColor Red
                    if ($url) {
                        Write-Host "    URL: $url" -ForegroundColor Gray
                    }
                } elseif ($state -eq "skip" -or $state -eq "skipped") {
                    $skipped += $checkObj
                    Write-Host "  [SKIP] $name" -ForegroundColor Gray
                } else {
                    Write-Host "  [$state] $name" -ForegroundColor Yellow
                }
            }
        }
        
        Write-Host "`nSummary:" -ForegroundColor Cyan
        Write-Host "  Passed: $($passed.Count)" -ForegroundColor Green
        Write-Host "  Failed: $($failed.Count)" -ForegroundColor $(if ($failed.Count -gt 0) { "Red" } else { "Gray" })
        Write-Host "  In Progress: $($inProgress.Count)" -ForegroundColor $(if ($inProgress.Count -gt 0) { "Yellow" } else { "Gray" })
        Write-Host "  Skipped: $($skipped.Count)" -ForegroundColor Gray
        
        # Analyze failures and provide advice
        if ($failed.Count -gt 0) {
            Write-Host "`n=== Failure Analysis ===" -ForegroundColor Red
            foreach ($fail in $failed) {
                Write-Host "`n[$($fail.name)]" -ForegroundColor Red
                
                    # Get run details
                    if ($fail.url) {
                        $urlParts = $fail.url -split '/'
                        $runId = $urlParts[-2]
                        $jobId = $urlParts[-1]
                    
                    Write-Host "  Analyzing logs..." -ForegroundColor Yellow
                    $logOutput = gh run view $runId --log --job $jobId 2>&1 | Select-String -Pattern "error|Error|ERROR|fail|Fail|FAIL|fatal|Fatal|FATAL" -Context 1,1 | Select-Object -First 20
                    
                    if ($logOutput) {
                        Write-Host "  Key errors found:" -ForegroundColor Yellow
                        foreach ($line in $logOutput) {
                            Write-Host "    $line" -ForegroundColor Gray
                        }
                    }
                    
                    # Provide specific advice based on error patterns
                    if ($fail.name -like "*Build NVDA*" -or $fail.name -like "*Build*") {
                        Write-Host "`n  💡 Advice for build failures:" -ForegroundColor Cyan
                        Write-Host "    - Check for architecture mismatches (x86 vs x64)" -ForegroundColor White
                        Write-Host "    - Verify MSVC environment is correctly configured" -ForegroundColor White
                        Write-Host "    - Ensure all dependencies are built for the correct architecture" -ForegroundColor White
                        Write-Host "    - For JTalk builds, check MACHINE parameter matches TARGET_ARCH" -ForegroundColor White
                        
                        # Check for specific JTalk build errors
                        if ($logOutput -match "libopenjtalk|jtalkPrep|MACHINE|LNK1112") {
                            Write-Host "`n  🔧 JTalk Build Issue Detected:" -ForegroundColor Yellow
                            Write-Host "    The error 'LNK1112: module machine type conflicts' indicates:" -ForegroundColor White
                            Write-Host "    1. Previous build artifacts may be left in the build directory" -ForegroundColor White
                            Write-Host "    2. Solution: Clean the build directory before building" -ForegroundColor White
                            Write-Host "       - In CI: Ensure build directory is cleaned between runs" -ForegroundColor White
                            Write-Host "       - Locally: Run 'scons -c' or delete miscDepsJp/include/python-jtalk/lib/*.obj" -ForegroundColor White
                            Write-Host "    3. Verify vcvarsall.bat is called with correct architecture (x64 for x64 builds)" -ForegroundColor White
                            Write-Host "    4. Check that jptools/scons_jp.py passes MACHINE=x64 for x64 builds" -ForegroundColor White
                        }
                    } elseif ($fail.name -like "*test*" -or $fail.name -like "*Test*" -or $fail.name -like "*all tests*") {
                        Write-Host "`n  💡 Advice for test failures:" -ForegroundColor Cyan
                        Write-Host "    - Review test output for specific assertion failures" -ForegroundColor White
                        Write-Host "    - Check if tests are environment-dependent" -ForegroundColor White
                        Write-Host "    - Verify test data and fixtures are up to date" -ForegroundColor White
                        
                        # If "all tests pass" failed, check if it's due to buildNVDA failure
                        if ($fail.name -like "*all tests*" -and $logOutput -match "buildNVDA.*failure") {
                            Write-Host "`n  ⚠️  Root Cause: buildNVDA job failed" -ForegroundColor Yellow
                            Write-Host "    This check aggregates results from multiple jobs." -ForegroundColor White
                            Write-Host "    Check the 'Build NVDA' job logs for the actual build error." -ForegroundColor White
                            Write-Host "    Common issues:" -ForegroundColor White
                            Write-Host "    - JTalk build architecture mismatch (x86 vs x64)" -ForegroundColor White
                            Write-Host "    - Missing or incorrect MSVC environment setup" -ForegroundColor White
                            Write-Host "    - Previous build artifacts not cleaned" -ForegroundColor White
                        }
                    } elseif ($fail.name -like "*type*" -or $fail.name -like "*Type*" -or $fail.name -like "*pyright*") {
                        Write-Host "`n  💡 Advice for type check failures:" -ForegroundColor Cyan
                        Write-Host "    - Review type errors in the logs" -ForegroundColor White
                        Write-Host "    - Run type check locally: ci\scripts\tests\typeCheck.ps1" -ForegroundColor White
                        Write-Host "    - Check for missing type stubs or incorrect annotations" -ForegroundColor White
                    }
                }
            }
        }
        
        return @{
            Pr = $prObj
            Checks = $checkObj
            Failed = $failed
            InProgress = $inProgress
            Passed = $passed
            Skipped = $skipped
        }
    }
    
    return @{
        Pr = $prObj
        Checks = @()
        Failed = @()
        InProgress = @()
        Passed = @()
        Skipped = @()
    }
}

# Main monitoring loop
$status = Get-PrCiStatus -Number $PrNumber

if ($Watch) {
    Write-Host "`n=== Watching for changes (Ctrl+C to stop) ===" -ForegroundColor Cyan
    $lastState = $status
    
    while ($true) {
        Start-Sleep -Seconds 30
        $currentState = Get-PrCiStatus -Number $PrNumber
        
        # Check for changes
        $changed = $false
        if ($currentState.Failed.Count -ne $lastState.Failed.Count) {
            $changed = $true
            Write-Host "`n⚠️  Failure count changed!" -ForegroundColor Yellow
        }
        if ($currentState.InProgress.Count -ne $lastState.InProgress.Count) {
            $changed = $true
        }
        
        if ($changed) {
            Write-Host "`n🔄 Status changed - refreshing..." -ForegroundColor Cyan
        }
        
        $lastState = $currentState
    }
} else {
    # Single check
    if ($status.Failed.Count -gt 0) {
        Write-Host "`n❌ PR has $($status.Failed.Count) failing check(s)" -ForegroundColor Red
        exit 1
    } elseif ($status.InProgress.Count -gt 0) {
        Write-Host "`n⏳ PR has $($status.InProgress.Count) check(s) in progress" -ForegroundColor Yellow
        exit 0
    } else {
        Write-Host "`n✅ All checks passed!" -ForegroundColor Green
        exit 0
    }
}

