<#
.SYNOPSIS
    Verifies that the MeCab dictionary includes custom entries (一人→ヒトリ, etc.).

.DESCRIPTION
    Runs a quick sanity check that translator2 produces expected output for
    custom-dictionary entries. Use after jtalkSync to catch CI cache pollution
    or incorrect dictionary builds before running full smoke tests.

    Can be run locally or in CI (e.g. after buildNVDA's Prepare JTalk step).

.EXAMPLE
    .\jptools\verifyJtalkDictionary.ps1
    Run after: scons jtalkSync

.EXAMPLE
    # CI (buildNVDA) で jtalkSync 直後に実行する場合
    chcp 932 >nul 2>&1 && powershell -ExecutionPolicy Bypass -File jptools/verifyJtalkDictionary.ps1
#>
$ErrorActionPreference = 'Stop'

$isCI = $env:GITHUB_ACTIONS -eq "true"
if ($isCI) {
    $repoRoot = (Resolve-Path .).Path
} else {
    $repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}
Set-Location $repoRoot

$jtalkSource = Join-Path $repoRoot "source\synthDrivers\jtalk"
$jptoolsDir = Join-Path $repoRoot "miscDepsJp\jptools"
$env:PYTHONPATH = "$jtalkSource;$jptoolsDir"
# CI uses cp1252; ensure Python stdout/stderr use UTF-8 to avoid UnicodeEncodeError on Japanese
$env:PYTHONUTF8 = "1"

# Prefer .venv Python if it exists (same as runJpSmokeTests)
$pythonExe = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python"
}

$verifyScript = Join-Path $jptoolsDir "verify_dic.py"
if (-not (Test-Path $verifyScript)) {
    Write-Error "verify_dic.py not found at $verifyScript"
    exit 1
}

Write-Host "Verifying JTalk dictionary (一人→ヒトリ, etc.)..."
& $pythonExe $verifyScript
exit $LASTEXITCODE
