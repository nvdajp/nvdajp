<#
.SYNOPSIS
    JP PATCHマーカーがない差分を分析し、本家版の変更を適用する候補をリストアップします。

.DESCRIPTION
    projectDocs/jp/compare-with-beta/generated/ 内のMarkdownファイルを解析して：
    1. JP PATCHマーカーがない差分を特定
    2. 本家版の変更を適用する候補を優先順位付きでリストアップ
    3. ユーザーが確認できるレポートを生成

.PARAMETER GeneratedDir
    生成されたMarkdownファイルがあるディレクトリ
    デフォルト: projectDocs/jp/compare-with-beta/generated

.PARAMETER OutputFile
    出力レポートファイル
    デフォルト: projectDocs/jp/compare-with-beta/diff-minimization-candidates.md

.PARAMETER SourceBetaPath
    本家版betaのパス（実際のファイルを確認する場合）
    デフォルト: F:\nvda\gh\beta

.EXAMPLE
    .\jptools\analyzeDiffMinimization.ps1
    デフォルト設定で分析を実行

.EXAMPLE
    .\jptools\analyzeDiffMinimization.ps1 -OutputFile "my-report.md"
    カスタム出力ファイルを指定
#>
[CmdletBinding()]
param(
    [string]$GeneratedDir = "projectDocs/jp/compare-with-beta/generated",
    [string]$OutputFile = "projectDocs/jp/compare-with-beta/diff-minimization-candidates.md",
    [string]$SourceBetaPath = "F:\nvda\gh\beta"
)

$ErrorActionPreference = "Stop"

# リポジトリルートを取得
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

$generatedPath = Join-Path $repoRoot $GeneratedDir
if (-not (Test-Path $generatedPath)) {
    Write-Error "Generated directory not found: $generatedPath"
    exit 1
}

Write-Host "分析を開始します..." -ForegroundColor Cyan
Write-Host "  生成ファイルディレクトリ: $generatedPath" -ForegroundColor Gray
Write-Host ""

# 生成されたMarkdownファイルを取得
$mdFiles = Get-ChildItem -Path $generatedPath -Filter "*.md" | Sort-Object Name

$candidates = @()
$hasJpPatch = @()
$unknown = @()

foreach ($mdFile in $mdFiles) {
    $content = Get-Content $mdFile.FullName -Raw -Encoding UTF8

    # ファイルパスを抽出（最初の行から）
    $filePath = $null
    if ($content -match '`([^`]+)`') {
        $filePath = $matches[1]
    }

    if (-not $filePath) {
        continue
    }

    # 実際のファイルが存在するか確認
    $actualPath = Join-Path $repoRoot $filePath
    if (-not (Test-Path $actualPath)) {
        Write-Warning "ファイルが見つかりません: $filePath"
        continue
    }

    # 実際のファイルにJP PATCHマーカーがあるか確認
    $fileContent = Get-Content $actualPath -Raw -Encoding UTF8
    $hasJpMarker = $fileContent -match '(?i)(BEGIN JP PATCH|END JP PATCH|# nvdajp)'

    # diffセクションを抽出
    $diffMatch = $content -match '(?s)```diff\s+(.*?)\s+```'
    if (-not $diffMatch) {
        continue
    }

    $diffContent = $matches[1]

    # 差分の行数をカウント（追加/削除）
    $addedLines = ([regex]::Matches($diffContent, '^\+(?!\+)')).Count
    $removedLines = ([regex]::Matches($diffContent, '^-(?!-)')).Count

    # 差分の種類を判定
    $diffType = "unknown"
    if ($diffContent -match 'screenCurtain') {
        $diffType = "screenCurtain_merge_missing"
    }
    elseif ($diffContent -match 'import\s+winreg|RegDeleteTree') {
        $diffType = "registry_refactor"
    }
    elseif ($diffContent -match 'copyright.*2025') {
        $diffType = "copyright_update"
    }
    elseif ($diffContent -match 'log\.debug.*MathPlayer|log\.debug.*math presentation') {
        $diffType = "log_message_update"
    }
    elseif ($addedLines -gt 0 -and $removedLines -gt 0) {
        $diffType = "code_change"
    }
    elseif ($removedLines -gt 0) {
        $diffType = "code_removal"
    }
    elseif ($addedLines -gt 0) {
        $diffType = "code_addition"
    }

    $candidate = [PSCustomObject]@{
        File = $filePath
        HasJpMarker = $hasJpMarker
        AddedLines = $addedLines
        RemovedLines = $removedLines
        DiffType = $diffType
        Priority = 0
        Reason = ""
        DiffPreview = ""
    }

    # 優先順位を決定
    if (-not $hasJpMarker) {
        # JP PATCHマーカーがない = 本家版の変更を適用する候補
        switch ($diffType) {
            "screenCurtain_merge_missing" {
                $candidate.Priority = 1
                $candidate.Reason = "明らかなマージ漏れ: screenCurtain統合"
            }
            "registry_refactor" {
                $candidate.Priority = 2
                $candidate.Reason = "明らかなマージ漏れ: registry.pyのリファクタリング"
            }
            "copyright_update" {
                $candidate.Priority = 5
                $candidate.Reason = "Copyright更新（低優先度）"
            }
            "log_message_update" {
                $candidate.Priority = 4
                $candidate.Reason = "ログメッセージの更新"
            }
            "code_change" {
                $candidate.Priority = 3
                $candidate.Reason = "コード変更（要確認）"
            }
            default {
                $candidate.Priority = 6
                $candidate.Reason = "その他の変更（要確認）"
            }
        }

        # 差分のプレビューを生成（最初の50行）
        $diffLines = $diffContent -split "`n"
        $previewLines = $diffLines | Select-Object -First 50
        $candidate.DiffPreview = ($previewLines -join "`n")
        if ($diffLines.Count -gt 50) {
            $candidate.DiffPreview += "`n... (残り $($diffLines.Count - 50) 行)"
        }

        $candidates += $candidate
    }
    else {
        $hasJpPatch += $candidate
    }
}

# 優先順位でソート
$candidates = $candidates | Sort-Object Priority, File

Write-Host "分析完了:" -ForegroundColor Green
Write-Host "  JP PATCHマーカーがない差分: $($candidates.Count) ファイル" -ForegroundColor Yellow
Write-Host "  JP PATCHマーカーがある差分: $($hasJpPatch.Count) ファイル" -ForegroundColor Cyan
Write-Host ""

# レポートを生成
$outputPath = Join-Path $repoRoot $OutputFile
$report = @"
# 差分最小化候補リスト

**生成日時**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## 概要

このレポートは、`projectDocs/jp/compare-with-beta/generated/` 内のMarkdownファイルを解析して、
JP PATCHマーカーがない差分を特定し、本家版の変更を適用する候補をリストアップしたものです。

### 統計

- **JP PATCHマーカーがない差分**: $($candidates.Count) ファイル
- **JP PATCHマーカーがある差分**: $($hasJpPatch.Count) ファイル（保持すべきJP固有の変更）

## 優先順位の説明

1. **優先度1**: 明らかなマージ漏れ（例: screenCurtain統合）
2. **優先度2**: 明らかなマージ漏れ（例: registry.pyのリファクタリング）
3. **優先度3**: コード変更（要確認）
4. **優先度4**: ログメッセージの更新
5. **優先度5**: Copyright更新（低優先度）
6. **優先度6**: その他の変更（要確認）

## 適用候補（優先順位順）

"@

foreach ($candidate in $candidates) {
    $priorityBadge = switch ($candidate.Priority) {
        1 { "🔴 **最優先**" }
        2 { "🟠 **高優先度**" }
        3 { "🟡 **中優先度**" }
        4 { "🔵 **低優先度**" }
        5 { "⚪ **低優先度**" }
        default { "⚫ **要確認**" }
    }

    $filePathEscaped = $candidate.File -replace '`', '``'
    $report += "`n"
    $report += "### ${priorityBadge}: ``${filePathEscaped}```n"
    $report += "`n"
    $report += "- **優先度**: $($candidate.Priority)`n"
    $report += "- **理由**: $($candidate.Reason)`n"
    $report += "- **追加行数**: $($candidate.AddedLines)`n"
    $report += "- **削除行数**: $($candidate.RemovedLines)`n"
    $report += "- **変更タイプ**: $($candidate.DiffType)`n"
    $report += "`n"
    $report += "#### 差分プレビュー`n"
    $report += "`n"
    $report += "``````diff`n"
    $report += "$($candidate.DiffPreview)`n"
    $report += "```````n"
    $report += "`n"
    $report += "#### 確認事項`n"
    $report += "`n"
    $report += "- [ ] 本家版の変更内容を確認`n"
    $report += "- [ ] JP固有の機能に影響がないか確認`n"
    $report += "- [ ] ビルド・型チェック・テストを実行`n"
    $report += "- [ ] 問題なければ本家版の変更を適用`n"
    $report += "`n"
    $report += "---`n"
}

$report += @"

## 注意事項

1. **各変更を小さな単位で適用**: 一度に複数のファイルを変更しない
2. **各変更後に検証**: ビルド・型チェック・単体テストを実行
3. **問題があれば即座にロールバック**: Gitで簡単に戻せるように、各変更を個別のコミットにする
4. **JP PATCHマーカーがある差分は保持**: これらはJP固有の変更なので、本家版の変更を適用しない

## 次のステップ

1. 優先度1-2のファイルから順に確認・適用
2. 各ファイルについて：
   - 本家版のファイルを確認: ``$SourceBetaPath\$($candidate.File)``
   - 現在のファイルを確認: ``source\$($candidate.File)``
   - 差分を確認: projectDocs/jp/compare-with-beta/generated/source_$($candidate.File.Replace('\', '_').Replace('/', '_').Replace('.', '_')).md
   - 本家版の変更を適用
   - ビルド・型チェック・テストを実行
   - 問題なければコミット

## 参考

- 元の比較結果: ``projectDocs/jp/compare-with-beta/summary.md``
- ファイル一覧: ``projectDocs/jp/compare-with-beta/file-list.md``
"@

# レポートを保存
$report | Out-File -FilePath $outputPath -Encoding UTF8 -NoNewline

Write-Host "レポートを生成しました:" -ForegroundColor Green
Write-Host "  $outputPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "次のステップ:" -ForegroundColor Yellow
Write-Host "  1. レポートを確認: Get-Content `"$outputPath`" | less" -ForegroundColor Gray
Write-Host "  2. 優先度1-2のファイルから順に確認・適用" -ForegroundColor Gray
Write-Host "  3. 各変更後にビルド・型チェック・テストを実行" -ForegroundColor Gray
