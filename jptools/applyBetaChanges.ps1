<#
.SYNOPSIS
    本家版betaの変更を適用します（確認付き）。

.DESCRIPTION
    指定されたファイルに本家版betaの変更を適用します。
    各ファイルについて、適用前に差分を表示して確認を求めます。

.PARAMETER Files
    適用するファイルのパス（配列）。相対パスまたは絶対パス。

.PARAMETER SourceBetaPath
    本家版betaのパス
    デフォルト: F:\nvda\gh\beta

.PARAMETER DryRun
    実際には適用せず、差分のみを表示します。

.PARAMETER SkipConfirmation
    確認をスキップして自動的に適用します（注意: 使用時は十分に確認してください）。

.EXAMPLE
    .\jptools\applyBetaChanges.ps1 -Files @("source\core.py", "source\config\__init__.py")
    指定されたファイルに本家版の変更を適用（確認付き）

.EXAMPLE
    .\jptools\applyBetaChanges.ps1 -Files @("source\core.py") -DryRun
    差分のみを表示（実際には適用しない）

.EXAMPLE
    # 優先度1のファイルを一括適用
    $files = @(
        "source\config\__init__.py",
        "source\config\profileUpgradeSteps.py",
        "source\core.py",
        "source\gui\blockAction.py",
        "source\vision\visionHandler.py",
        "source\visionEnhancementProviders\_exampleProvider_autoGui.py",
        "source\winVersion.py"
    )
    .\jptools\applyBetaChanges.ps1 -Files $files
#>
[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory=$true)]
    [string[]]$Files,

    [string]$SourceBetaPath = "F:\nvda\gh\beta",

    [switch]$DryRun,

    [switch]$SkipConfirmation
)

$ErrorActionPreference = "Stop"

# リポジトリルートを取得
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

if (-not (Test-Path $SourceBetaPath)) {
    Write-Error "本家版betaのパスが見つかりません: $SourceBetaPath"
    exit 1
}

Write-Host "本家版betaの変更を適用します" -ForegroundColor Cyan
Write-Host "  本家版beta: $SourceBetaPath" -ForegroundColor Gray
Write-Host "  対象ファイル数: $($Files.Count)" -ForegroundColor Gray
if ($DryRun) {
    Write-Host "  [DRY RUN] 実際には適用しません" -ForegroundColor Yellow
}
Write-Host ""

$appliedFiles = @()
$skippedFiles = @()
$errorFiles = @()

foreach ($file in $Files) {
    $currentPath = Join-Path $repoRoot $file
    $betaPath = Join-Path $SourceBetaPath $file

    Write-Host "処理中: $file" -ForegroundColor Cyan

    # ファイルの存在確認
    if (-not (Test-Path $currentPath)) {
        Write-Warning "  現在のファイルが見つかりません: $currentPath"
        $errorFiles += $file
        continue
    }

    if (-not (Test-Path $betaPath)) {
        Write-Warning "  本家版のファイルが見つかりません: $betaPath"
        $errorFiles += $file
        continue
    }

    # ファイルの内容を比較
    $currentContent = Get-Content $currentPath -Raw -Encoding UTF8
    $betaContent = Get-Content $betaPath -Raw -Encoding UTF8

    if ($currentContent -eq $betaContent) {
        Write-Host "  差分なし（既に同じ内容）" -ForegroundColor Green
        $appliedFiles += $file
        continue
    }

    # 差分を取得（簡易版）
    try {
        $diff = git diff --no-index -- "$currentPath" "$betaPath" 2>&1 | Out-String
        if ($LASTEXITCODE -ne 0 -and $diff -notmatch "differ" -and $diff -notmatch "Binary") {
            # git diffが使えない場合は、ファイルサイズと行数を比較
            $currentLines = (Get-Content $currentPath).Count
            $betaLines = (Get-Content $betaPath).Count
            $diff = "ファイルサイズの違い: 現在=$currentLines行, 本家版=$betaLines行`n(詳細な差分は表示できません)"
        }
    }
    catch {
        # git diffが使えない場合は、ファイルサイズと行数を比較
        $currentLines = (Get-Content $currentPath).Count
        $betaLines = (Get-Content $betaPath).Count
        $diff = "ファイルサイズの違い: 現在=$currentLines行, 本家版=$betaLines行`n(詳細な差分は表示できません)"
    }

    # 差分を表示
    Write-Host "  差分:" -ForegroundColor Yellow
    $diffLines = $diff -split "`n"
    $previewLines = $diffLines | Select-Object -First 30
    Write-Host ($previewLines -join "`n")
    if ($diffLines.Count -gt 30) {
        Write-Host "  ... (残り $($diffLines.Count - 30) 行)" -ForegroundColor Gray
    }
    Write-Host ""

    if ($DryRun) {
        Write-Host "  [DRY RUN] 適用をスキップ" -ForegroundColor Yellow
        continue
    }

    # 確認
    if (-not $SkipConfirmation) {
        $response = Read-Host "  この変更を適用しますか? (Y/N)"
        if ($response -ne "Y" -and $response -ne "y") {
            Write-Host "  適用をスキップしました" -ForegroundColor Yellow
            $skippedFiles += $file
            continue
        }
    }

    # バックアップを作成（念のため）
    $backupPath = "$currentPath.backup"
    Copy-Item -Path $currentPath -Destination $backupPath -Force

    try {
        # 本家版のファイルをコピー
        Copy-Item -Path $betaPath -Destination $currentPath -Force

        Write-Host "  適用完了" -ForegroundColor Green
        Write-Host "  バックアップ: $backupPath" -ForegroundColor Gray
        $appliedFiles += $file
    }
    catch {
        Write-Error "  適用に失敗しました: $_"
        # バックアップから復元
        if (Test-Path $backupPath) {
            Copy-Item -Path $backupPath -Destination $currentPath -Force
            Write-Host "  バックアップから復元しました" -ForegroundColor Yellow
        }
        $errorFiles += $file
    }

    Write-Host ""
}

# 結果サマリー
Write-Host "`n結果サマリー:" -ForegroundColor Cyan
Write-Host "  適用済み: $($appliedFiles.Count) ファイル" -ForegroundColor Green
if ($appliedFiles.Count -gt 0) {
    foreach ($f in $appliedFiles) {
        Write-Host "    - $f" -ForegroundColor Gray
    }
}

if ($skippedFiles.Count -gt 0) {
    Write-Host "  スキップ: $($skippedFiles.Count) ファイル" -ForegroundColor Yellow
    foreach ($f in $skippedFiles) {
        Write-Host "    - $f" -ForegroundColor Gray
    }
}

if ($errorFiles.Count -gt 0) {
    Write-Host "  エラー: $($errorFiles.Count) ファイル" -ForegroundColor Red
    foreach ($f in $errorFiles) {
        Write-Host "    - $f" -ForegroundColor Gray
    }
}

Write-Host "`n次のステップ:" -ForegroundColor Yellow
Write-Host "  1. ビルド・型チェック・テストを実行" -ForegroundColor Gray
Write-Host "  2. 問題なければコミット" -ForegroundColor Gray
Write-Host "  3. 問題があればバックアップから復元: Copy-Item `"<file>.backup`" `"<file>`"" -ForegroundColor Gray
