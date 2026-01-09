# Script to record merge conflicts when merging nvaccess/beta
# This script should be run after attempting a merge with nvaccess/beta
# Usage: .\ci\scripts\tests\recordMergeConflicts.ps1

param(
    [string]$OutputFile = "projectDocs/jp/archive/merge-conflicts-detailed-2025-11.md",
    [string]$BaseBranch = "betajp",
    [string]$MergeBranch = "nvaccess/beta"
)

$ErrorActionPreference = "Continue"

Write-Host "Recording merge conflicts for $MergeBranch into $BaseBranch" -ForegroundColor Cyan

# Get list of conflicted files
$conflictedFiles = git diff --name-only --diff-filter=U
if (-not $conflictedFiles) {
    Write-Host "No conflicts found. Checking if merge is in progress..." -ForegroundColor Yellow
    $mergeInProgress = git merge HEAD 2>&1 | Select-String -Pattern "merge in progress"
    if (-not $mergeInProgress) {
        Write-Host "No merge in progress. Please run merge first." -ForegroundColor Red
        exit 1
    }
}

# Get conflict markers
$conflictPattern = '^<<<<<<< |^=======|^>>>>>>> '

$mergeBranchCommit = git rev-parse --short $MergeBranch
$mergeBranchCommitLong = git rev-parse $MergeBranch
$mergeBranchCommitMsg = git log -1 --format="%s" $MergeBranch
$baseBranchCommit = git rev-parse --short $BaseBranch
$baseBranchCommitLong = git rev-parse $BaseBranch
$baseBranchCommitMsg = git log -1 --format="%s" $BaseBranch

$output = @"
# nvaccess beta マージコンフリクト詳細記録（2025-11）

このファイルは、nvaccess/beta を日本語版にマージする際に発生したコンフリクトの詳細を記録したものです。

## メタ情報

- **マージ元**: $MergeBranch
- **マージ先（ベース）**: $BaseBranch
- **記録日時**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
- **上流コミット**: $mergeBranchCommit ($mergeBranchCommitMsg)
- **上流コミット（完全）**: $mergeBranchCommitLong
- **ベースコミット**: $baseBranchCommit ($baseBranchCommitMsg)
- **ベースコミット（完全）**: $baseBranchCommitLong

## コンフリクトファイル一覧

"@

$fileCount = 0
foreach ($file in $conflictedFiles) {
    $fileCount++
    Write-Host "Processing: $file ($fileCount / $($conflictedFiles.Count))" -ForegroundColor Gray
    
    if (-not (Test-Path $file)) {
        $output += "### $fileCount. $file`n`n**状態**: ファイルが見つかりません（削除/移動の可能性）`n`n"
        continue
    }
    
    # Check if it's a directory (submodule)
    if (Test-Path $file -PathType Container) {
        $output += "### $fileCount. $file`n`n**状態**: サブモジュール（ディレクトリ）`n`n"
        $output += "**解決方法**: `git add $file` でサブモジュールの状態を確定`n`n"
        $output += "---`n`n"
        continue
    }
    
    # Get conflict markers in file
    $content = Get-Content $file -Raw
    $conflictMarkers = [regex]::Matches($content, $conflictPattern, [System.Text.RegularExpressions.RegexOptions]::Multiline)
    
    if ($conflictMarkers.Count -eq 0) {
        $output += "### $fileCount. $file`n`n**状態**: コンフリクトマーカーが見つかりません（未解決または自動マージ済み）`n`n"
        continue
    }
    
    # Count conflicts (each conflict has 3 markers: <<<<<<, =======, >>>>>>>)
    $conflictCount = [Math]::Floor($conflictMarkers.Count / 3)
    
    # Get line numbers of conflict markers
    $lineNumbers = @()
    $lineNum = 1
    foreach ($line in (Get-Content $file)) {
        if ($line -match '^<<<<<<< ') {
            $lineNumbers += $lineNum
        }
        $lineNum++
    }
    
    $output += "### $fileCount. $file`n`n"
    $output += "**コンフリクト数**: $conflictCount`n`n"
    $output += "**コンフリクト開始行**: $($lineNumbers -join ', ')`n`n"
    
    # Show sample conflict (first one)
    if ($lineNumbers.Count -gt 0) {
        $firstConflictLine = $lineNumbers[0]
        $startLine = [Math]::Max(1, $firstConflictLine - 5)
        $endLine = [Math]::Min((Get-Content $file).Count, $firstConflictLine + 50)
        
        $output += "**最初のコンフリクト周辺（行 $startLine - $endLine）**:`n`n"
        $output += "````````n"
        $lines = Get-Content $file
        for ($i = $startLine - 1; $i -lt $endLine; $i++) {
            $lineNum = $i + 1
            $line = $lines[$i]
            $marker = ""
            if ($line -match '^<<<<<<< ') {
                $marker = " <- JP側"
            } elseif ($line -match '^=======') {
                $marker = " <- 分岐点"
            } elseif ($line -match '^>>>>>>> ') {
                $marker = " <- 上流側"
            }
            $output += "$lineNum`:$line$marker`n"
        }
        $output += "````````n`n"
    }
    
    $output += "---`n`n"
}

$output += @"

## 解決方針メモ

各ファイルの解決方針は `projectDocs/jp/archive/merge-issues-beta-2025-11.md` を参照してください。

## 次のステップ

1. 各コンフリクトを projectDocs/jp/archive/merge-issues-beta-2025-11.md の解決方針に従って解決
2. uv.lock はコンフリクト解決後に 'uv lock --upgrade' で再生成
3. source/locale/ja/LC_MESSAGES/nvda.po は msgmerge で上流 pot に追随
4. 解決後、ビルドとテストを実行して確認

"@

# Write output
$output | Out-File -FilePath $OutputFile -Encoding UTF8
Write-Host "`n詳細記録を $OutputFile に保存しました。" -ForegroundColor Green
Write-Host "コンフリクトファイル数: $fileCount" -ForegroundColor Green

