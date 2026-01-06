# Analyze diff files for potential regression risks
# Usage: .\jptools\analyzeRegressionRisks.ps1

param(
    [string]$DiffDir = "projectDocs/jp/compare-with-2025/generated",
    [string]$OutputFile = "projectDocs/jp/compare-with-2025/regression-risks.md"
)

$ErrorActionPreference = "Continue"

Write-Host "Analyzing diff files for regression risks..." -ForegroundColor Cyan

# Patterns that might indicate regression risks
$riskPatterns = @{
    "JP固有機能の削除" = @(
        "jtalk",
        "mecab",
        "haruka",
        "日本語",
        "japanese",
        "jp",
        "JP"
    )
    "エラーハンドリングの削除" = @(
        "except",
        "try:",
        "catch",
        "Error",
        "Exception"
    )
    "関数・メソッドの削除" = @(
        "^-def ",
        "^-    def ",
        "^-class ",
        "^-    class "
    )
    "重要な条件分岐の削除" = @(
        "^-if ",
        "^-    if ",
        "^-elif ",
        "^-    elif ",
        "^-else:",
        "^-    else:"
    )
    "設定値の変更" = @(
        "^-.*=.*",
        "^-.*:.*"
    )
    "import文の削除" = @(
        "^-import ",
        "^-from .* import"
    )
}

$regressionRisks = @{
    "JP固有機能の削除" = @()
    "エラーハンドリングの削除" = @()
    "関数・メソッドの削除" = @()
    "重要な条件分岐の削除" = @()
    "設定値の変更" = @()
    "import文の削除" = @()
}

# Get all diff files
$diffFiles = Get-ChildItem -Path $DiffDir -Filter "*.md" | Where-Object { $_.Name -notlike "*regression*" }

Write-Host "Found $($diffFiles.Count) diff files to analyze" -ForegroundColor Gray

foreach ($diffFile in $diffFiles) {
    $content = Get-Content -Path $diffFile.FullName -Raw -Encoding UTF8
    $fileName = $diffFile.BaseName -replace '\.md$', ''
    
    # Check each risk pattern
    foreach ($category in $riskPatterns.Keys) {
        $patterns = $riskPatterns[$category]
        
        foreach ($pattern in $patterns) {
            # Look for deletions (lines starting with -)
            if ($category -match "削除") {
                # Check for deleted lines matching the pattern
                $matches = [regex]::Matches($content, "(?m)^-$pattern", [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
                if ($matches.Count -gt 0) {
                    # Check if there's no corresponding addition
                    $hasAddition = $content -match "(?m)^\+.*$pattern"
                    if (-not $hasAddition) {
                        $regressionRisks[$category] += [PSCustomObject]@{
                            File = $fileName
                            Pattern = $pattern
                            Count = $matches.Count
                            DiffFile = $diffFile.Name
                        }
                        break  # Only report once per file per category
                    }
                }
            } else {
                # For other patterns, just check if they appear in deleted lines
                $deletedLines = [regex]::Matches($content, "(?m)^-$pattern", [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
                if ($deletedLines.Count -gt 0) {
                    $regressionRisks[$category] += [PSCustomObject]@{
                        File = $fileName
                        Pattern = $pattern
                        Count = $deletedLines.Count
                        DiffFile = $diffFile.Name
                    }
                    break
                }
            }
        }
    }
}

# Generate report
$reportContent = @"
# リグレッションリスク分析レポート

**生成日時**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

このレポートは、2025.3.x jp (alphajp-251219) と現在の alphajp ブランチの差分を分析し、リグレッションが疑われる変更を特定したものです。

## 分析結果サマリー

"@

$totalRisks = 0
foreach ($category in $regressionRisks.Keys) {
    $count = $regressionRisks[$category].Count
    $totalRisks += $count
    if ($count -gt 0) {
        $reportContent += "`n- **$category**: $count ファイル"
    }
}

$reportContent += "`n`n**合計**: $totalRisks ファイルにリスクが検出されました`n"

# Detailed findings
foreach ($category in $regressionRisks.Keys) {
    $risks = $regressionRisks[$category]
    if ($risks.Count -gt 0) {
        $reportContent += "`n## $category`n`n"
        
        # Group by file
        $grouped = $risks | Group-Object -Property File
        
        foreach ($group in $grouped) {
            $file = $group.Name
            $items = $group.Group
            
            # Check if this is a JP-specific file
            $isJpSpecific = $file -like "*jptools*" -or $file -like "*miscDepsJp*" -or $file -like "*jtalk*" -or $file -like "*mecab*" -or $file -like "*haruka*"
            $priority = if ($isJpSpecific) { "🔴 **高優先度**" } else { "🟡 中優先度" }
            
            $reportContent += "### ``$file`` $priority`n`n"
            $reportContent += "- **検出パターン**: $($items[0].Pattern)`n"
            $reportContent += "- **差分ファイル**: [``$($items[0].DiffFile)``](./generated/$($items[0].DiffFile))`n"
            $reportContent += "- **検出数**: $($items[0].Count) 箇所`n`n"
        }
    }
}

# Add recommendations
$reportContent += @"

## 推奨される確認事項

1. **JP固有コードの削除**: `jptools/`, `miscDepsJp/`, `source/synthDrivers/jtalk/` などのJP固有コードで機能が削除されていないか確認
2. **エラーハンドリング**: エラーハンドリングが削除されていないか、適切に移行されているか確認
3. **関数・メソッドの削除**: 重要な関数やメソッドが削除されていないか確認
4. **条件分岐の削除**: 重要な条件分岐（特に日本語関連）が削除されていないか確認
5. **設定値の変更**: 設定値が意図せず変更されていないか確認

## 次のステップ

1. 高優先度（🔴）のファイルから順に確認
2. 各差分ファイルを開いて、実際の変更内容を確認
3. リグレッションが確認された場合は、`important-changes.md` に詳細を記載

"@

# Save report
$reportContent | Out-File -FilePath $OutputFile -Encoding UTF8

Write-Host "`nRegression risk analysis complete!" -ForegroundColor Green
Write-Host "Report saved to: $OutputFile" -ForegroundColor Cyan
Write-Host "`nSummary:" -ForegroundColor Yellow
foreach ($category in $regressionRisks.Keys) {
    $count = $regressionRisks[$category].Count
    if ($count -gt 0) {
        Write-Host "  $category : $count files" -ForegroundColor Gray
    }
}
