[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$InputPath,

    [Parameter(Position = 1)]
    [string]$OutputPath = "",

    [int]$KeepFirst = 20,

    [switch]$NoSummary
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $InputPath)) {
    throw "Input file not found: $InputPath"
}

if (-not $OutputPath) {
    $baseName = [IO.Path]::GetFileNameWithoutExtension($InputPath)
    $OutputPath = Join-Path -Path (Get-Location) -ChildPath ($baseName + ".filtered.log")
}

$mecabContextIdRegex = [regex]::new('^context_id\.cpp\(\d+\)\s+\[[^\]]+\]\s+cannot find (LEFT|RIGHT)-ID\b', 'Compiled')

$suppressedCounts = @{
    mecabContextId = 0
}

$keptCounts = @{
    mecabContextId = 0
}

$outLines = New-Object System.Collections.Generic.List[string]

Get-Content -LiteralPath $InputPath -ReadCount 2000 | ForEach-Object {
    foreach ($line in $_) {
        if ($mecabContextIdRegex.IsMatch($line)) {
            $suppressedCounts.mecabContextId++
            if ($keptCounts.mecabContextId -lt $KeepFirst) {
                $keptCounts.mecabContextId++
                $outLines.Add($line)
            }
            continue
        }
        $outLines.Add($line)
    }
}

if (-not $NoSummary) {
    $outLines.Add("")
    $outLines.Add("---- filter summary ----")
    $outLines.Add(("Input:  {0}" -f (Resolve-Path -LiteralPath $InputPath)))
    $outLines.Add(("Output: {0}" -f (Resolve-Path -LiteralPath $OutputPath -ErrorAction SilentlyContinue)))
    $outLines.Add(("Suppressed mecab context_id warnings: {0} (kept first {1})" -f $suppressedCounts.mecabContextId, $KeepFirst))
}

$outLines | Set-Content -LiteralPath $OutputPath -Encoding UTF8
Write-Host ("Wrote filtered log: {0}" -f $OutputPath)
