<#
.SYNOPSIS
    Verifies that the MeCab dictionary includes custom entries (一人→ヒトリ, etc.).

.DESCRIPTION
    Runs a quick sanity check that translator2 produces expected output for
    custom-dictionary entries. Use after jtalkSync to catch cache pollution
    or incorrect dictionary builds before running full smoke tests.

    - CI (GITHUB_ACTIONS): the workflow passes -Strict, because the dictionary
      build is not reproducible and basic cases pass even against a broken
      sys.dic (entries present but unreachable via the index). Without -Strict
      the GHA default is basic.
    - Local / certBuild: strict cases by default (二百十日, ごめんください, etc.).

.PARAMETER Strict
    Force strict verification (basic + extended custom-dic cases).

.PARAMETER Basic
    Force basic verification only (same as CI).

.EXAMPLE
    .\jptools\verifyJtalkDictionary.ps1
    Local default: strict verification after scons jtalkSync.

.EXAMPLE
    .\jptools\verifyJtalkDictionary.ps1 -Basic
    CI-equivalent sanity check only.
#>
[CmdletBinding()]
param(
    [switch]$Strict,
    [switch]$Basic
)

$ErrorActionPreference = 'Stop'

if ($Strict -and $Basic) {
    Write-Error "Use -Strict or -Basic, not both."
    exit 1
}

$isCI = $env:GITHUB_ACTIONS -eq "true"
if ($isCI) {
    $repoRoot = (Resolve-Path .).Path
} else {
    $repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}
Set-Location $repoRoot

if ($Strict) {
    $env:JP_VERIFY_DIC_MODE = "strict"
} elseif ($Basic) {
    $env:JP_VERIFY_DIC_MODE = "basic"
} else {
    Remove-Item Env:JP_VERIFY_DIC_MODE -ErrorAction SilentlyContinue
}

$jtalkSource = Join-Path $repoRoot "source\synthDrivers\jtalk"
$jptoolsDir = Join-Path $repoRoot "miscDepsJp\jptools"
$env:PYTHONPATH = "$jtalkSource;$jptoolsDir"
$env:PYTHONUTF8 = "1"

# Local certBuild: chcp 932 may help MeCab on Japanese Windows. Skip on GHA.
if (-not $isCI) {
    $null = cmd /c "chcp 932 >nul 2>&1"
}

$pythonExe = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python"
}

$verifyScript = Join-Path $jptoolsDir "verify_dic.py"
if (-not (Test-Path $verifyScript)) {
    Write-Error "verify_dic.py not found at $verifyScript"
    exit 1
}

$modeHint = if ($env:JP_VERIFY_DIC_MODE) { $env:JP_VERIFY_DIC_MODE } elseif ($isCI) { "basic (CI default)" } else { "strict (local default)" }
Write-Host "Verifying JTalk dictionary (mode: $modeHint)..."
& $pythonExe $verifyScript
exit $LASTEXITCODE
