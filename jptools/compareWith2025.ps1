# Compare current repository with 2025.3.x jp (alphajp-251219 PR #600)
# Usage: .\jptools\compareWith2025.ps1 [-Directory <path>] [-FileType <extensions>] [-Output <format>]

param(
    [string]$Source2025Path = "F:\nvda\gh\alphajp-251219",
    [string]$Directory = "",
    [string[]]$FileType = @(),
    [ValidateSet("list", "diff", "vscode", "git", "markdown")]
    [string]$Output = "list",
    [string]$OutputDir = "projectDocs/jp/compare-with-2025",
    [switch]$IgnoreWhitespace = $false,
    [switch]$ShowStats = $false
)

$ErrorActionPreference = "Stop"

# Check if source 2025.3.x jp exists
if (-not (Test-Path $Source2025Path)) {
    Write-Host "Error: $Source2025Path does not exist" -ForegroundColor Red
    exit 1
}

# Get current repository root
$CurrentRoot = (Get-Location).Path
if (-not (Test-Path "$CurrentRoot\.git")) {
    Write-Host "Error: Not in a Git repository" -ForegroundColor Red
    exit 1
}

Write-Host "Comparing:" -ForegroundColor Cyan
Write-Host "  Current: $CurrentRoot" -ForegroundColor Gray
Write-Host "  Source 2025.3.x jp: $Source2025Path" -ForegroundColor Gray
Write-Host ""

# Get all files in current directory (excluding .git, node_modules, etc.)
$currentFiles = Get-ChildItem -Path $CurrentRoot -Recurse -File `
    | Where-Object { 
        $_.FullName -notlike "*\.git\*" -and
        $_.FullName -notlike "*\node_modules\*" -and
        $_.FullName -notlike "*\__pycache__\*" -and
        $_.FullName -notlike "*\.venv\*" -and
        $_.FullName -notlike "*\build\*" -and
        $_.FullName -notlike "*\dist\*"
    }

# Filter by directory and file type
if ($Directory -ne "") {
    $currentFiles = $currentFiles | Where-Object { $_.FullName -like "*$Directory*" }
}
if ($FileType.Count -gt 0) {
    $currentFiles = $currentFiles | Where-Object { $_.Extension -in $FileType }
}

# Compare files
$changedFiles = @()
$addedFiles = @()
$removedFiles = @()
$identicalFiles = 0

foreach ($file in $currentFiles) {
    $relativePath = $file.FullName.Substring($CurrentRoot.Length + 1)
    $source2025File = Join-Path $Source2025Path $relativePath
    
    if (Test-Path $source2025File) {
        # Compare file content
        $currentHash = (Get-FileHash $file.FullName -Algorithm SHA256).Hash
        $source2025Hash = (Get-FileHash $source2025File -Algorithm SHA256).Hash
        
        if ($currentHash -ne $source2025Hash) {
            $changedFiles += [PSCustomObject]@{
                Path = $relativePath
                Current = $file.FullName
                Source2025 = $source2025File
            }
        } else {
            $identicalFiles++
        }
    } else {
        $addedFiles += $relativePath
    }
}

# Check for removed files
$source2025Files = Get-ChildItem -Path $Source2025Path -Recurse -File `
    | Where-Object { 
        $_.FullName -notlike "*\.git\*" -and
        $_.FullName -notlike "*\node_modules\*" -and
        $_.FullName -notlike "*\__pycache__\*" -and
        $_.FullName -notlike "*\.venv\*" -and
        $_.FullName -notlike "*\build\*" -and
        $_.FullName -notlike "*\dist\*"
    }

if ($Directory -ne "") {
    $source2025Files = $source2025Files | Where-Object { $_.FullName -like "*$Directory*" }
}
if ($FileType.Count -gt 0) {
    $source2025Files = $source2025Files | Where-Object { $_.Extension -in $FileType }
}

foreach ($file in $source2025Files) {
    $relativePath = $file.FullName.Substring($Source2025Path.Length + 1)
    $currentFile = Join-Path $CurrentRoot $relativePath
    
    if (-not (Test-Path $currentFile)) {
        $removedFiles += $relativePath
    }
}

# Output results
Write-Host "=== Comparison Results ===" -ForegroundColor Cyan
Write-Host "Changed files: $($changedFiles.Count)" -ForegroundColor Yellow
Write-Host "Added files: $($addedFiles.Count)" -ForegroundColor Green
Write-Host "Removed files: $($removedFiles.Count)" -ForegroundColor Red
Write-Host "Identical files: $identicalFiles" -ForegroundColor Gray
Write-Host ""

switch ($Output) {
    "list" {
        if ($changedFiles.Count -gt 0) {
            Write-Host "=== Changed Files ===" -ForegroundColor Yellow
            $changedFiles | ForEach-Object { Write-Host "  $($_.Path)" -ForegroundColor Gray }
            Write-Host ""
        }
        
        if ($addedFiles.Count -gt 0) {
            Write-Host "=== Added Files ===" -ForegroundColor Green
            $addedFiles | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
            Write-Host ""
        }
        
        if ($removedFiles.Count -gt 0) {
            Write-Host "=== Removed Files ===" -ForegroundColor Red
            $removedFiles | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
            Write-Host ""
        }
        
        # Save to file
        $outputFile = "compare-with-2025-$(Get-Date -Format 'yyyyMMdd-HHmmss').txt"
        $changedFiles | ForEach-Object { $_.Path } | Out-File -FilePath $outputFile -Encoding UTF8
        Write-Host "Changed files list saved to: $outputFile" -ForegroundColor Cyan
    }
    
    "diff" {
        if ($changedFiles.Count -gt 0) {
            Write-Host "=== Generating diffs ===" -ForegroundColor Cyan
            $diffOptions = ""
            if ($IgnoreWhitespace) {
                $diffOptions = "-w"
            }
            
            foreach ($file in $changedFiles) {
                Write-Host "`n--- $($file.Path) ---" -ForegroundColor Yellow
                git diff --no-index $diffOptions $file.Source2025 $file.Current 2>&1 | Select-Object -First 100
                if ($changedFiles.Count -gt 10 -and $changedFiles.IndexOf($file) -ge 9) {
                    Write-Host "`n... (showing first 10 files, use -Output list to see all)" -ForegroundColor Gray
                    break
                }
            }
        }
    }
    
    "vscode" {
        if ($changedFiles.Count -gt 0) {
            Write-Host "=== Opening in VS Code ===" -ForegroundColor Cyan
            $firstFile = $changedFiles[0]
            code --diff $firstFile.Source2025 $firstFile.Current
            
            if ($changedFiles.Count -gt 1) {
                Write-Host "`nTo compare other files, use:" -ForegroundColor Gray
                Write-Host "  code --diff <source-2025-file> <current-file>" -ForegroundColor Gray
                Write-Host "`nOr use the list output to see all changed files." -ForegroundColor Gray
            }
        }
    }
    
    "git" {
        if ($changedFiles.Count -gt 0) {
            Write-Host "=== Git diff commands ===" -ForegroundColor Cyan
            Write-Host "`nTo compare files using git diff --no-index:" -ForegroundColor Gray
            $changedFiles | Select-Object -First 20 | ForEach-Object {
                Write-Host "  git diff --no-index `"$($_.Source2025)`" `"$($_.Current)`"" -ForegroundColor White
            }
            if ($changedFiles.Count -gt 20) {
                Write-Host "  ... ($($changedFiles.Count - 20) more files)" -ForegroundColor Gray
            }
        }
    }
    
    "markdown" {
        Write-Host "=== Generating Markdown reports ===" -ForegroundColor Cyan
        
        # Create output directory
        $outputDirPath = Join-Path $CurrentRoot $OutputDir
        if (-not (Test-Path $outputDirPath)) {
            New-Item -ItemType Directory -Path $outputDirPath -Force | Out-Null
        }
        $generatedDir = Join-Path $outputDirPath "generated"
        if (-not (Test-Path $generatedDir)) {
            New-Item -ItemType Directory -Path $generatedDir -Force | Out-Null
        }
        
        # Get current branch name
        $currentBranch = git branch --show-current 2>$null
        if (-not $currentBranch) {
            $currentBranch = "unknown"
        }
        
        # Determine source description based on path
        $sourceDescription = if ($Source2025Path -like "*alphajp-251219*") {
            "2025.3.x jp (alphajp-251219 PR #600) - x86 Python 3.11 の最後の状態"
        } elseif ($Source2025Path -like "*\beta*" -or $Source2025Path -like "*beta*") {
            "nvaccess/beta ($Source2025Path)"
        } else {
            $Source2025Path
        }
        
        # Generate summary.md
        $summaryContent = @"
# 比較結果サマリー

**生成日時**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## 比較対象

- **ベース**: $sourceDescription
- **比較先**: 現在の $currentBranch ブランチ（x64 Python 3.13）

## 統計情報

- **変更されたファイル**: $($changedFiles.Count)
- **追加されたファイル**: $($addedFiles.Count)
- **削除されたファイル**: $($removedFiles.Count)
- **同一ファイル**: $identicalFiles
- **変更率**: $([math]::Round(($changedFiles.Count / ($changedFiles.Count + $identicalFiles)) * 100, 2))%

## カテゴリ別の変更

詳細は [file-list.md](./file-list.md) を参照してください。

"@
        $summaryContent | Out-File -FilePath (Join-Path $outputDirPath "summary.md") -Encoding UTF8
        
        # Categorize files
        $categories = @{
            "JP固有コード" = @()
            "ソースコード" = @()
            "設定ファイル" = @()
            "翻訳ファイル" = @()
            "ビルドシステム" = @()
            "CI/ワークフロー" = @()
            "ドキュメント" = @()
            "その他" = @()
        }
        
        foreach ($file in $changedFiles) {
            $path = $file.Path
            if ($path -like "*source/synthDrivers/jtalk*" -or $path -like "*source/synthDrivers/haruka*" -or $path -like "*miscDepsJp*" -or $path -like "*jptools*") {
                $categories["JP固有コード"] += $file
            } elseif ($path -like "*source/*" -or $path -like "*nvdaHelper/*") {
                $categories["ソースコード"] += $file
            } elseif ($path -like "*.po" -or $path -like "*locale/*") {
                $categories["翻訳ファイル"] += $file
            } elseif ($path -like "*sconscript*" -or $path -like "*sconstruct*" -or $path -like "*pyproject.toml*") {
                $categories["ビルドシステム"] += $file
            } elseif ($path -like "*\.github/*" -or $path -like "*ci/*") {
                $categories["CI/ワークフロー"] += $file
            } elseif ($path -like "*projectDocs/*" -or $path -like "*.md" -or $path -like "*readme*") {
                $categories["ドキュメント"] += $file
            } elseif ($path -like "*.json" -or $path -like "*.yaml" -or $path -like "*.yml" -or $path -like "*.toml" -or $path -like "*.ini") {
                $categories["設定ファイル"] += $file
            } else {
                $categories["その他"] += $file
            }
        }
        
        # Generate file-list.md
        $fileListContent = @"
# 変更されたファイル一覧

**生成日時**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## カテゴリ別ファイル一覧

"@
        
        foreach ($category in $categories.Keys | Sort-Object) {
            $files = $categories[$category]
            if ($files.Count -gt 0) {
                $fileListContent += "`n### $category ($($files.Count) ファイル)`n`n"
                foreach ($file in $files | Sort-Object Path) {
                    $fileListContent += "- ``$($file.Path)```n"
                }
            }
        }
        
        if ($addedFiles.Count -gt 0) {
            $fileListContent += "`n## 追加されたファイル ($($addedFiles.Count) ファイル)`n`n"
            foreach ($file in $addedFiles | Sort-Object) {
                $fileListContent += "- ``$file```n"
            }
        }
        
        if ($removedFiles.Count -gt 0) {
            $fileListContent += "`n## 削除されたファイル ($($removedFiles.Count) ファイル)`n`n"
            foreach ($file in $removedFiles | Sort-Object) {
                $fileListContent += "- ``$file```n"
            }
        }
        
        $fileListContent | Out-File -FilePath (Join-Path $outputDirPath "file-list.md") -Encoding UTF8
        
        # Generate important-changes.md (JP固有コードのみ)
        $importantContent = @"
# 重要な変更の詳細

**生成日時**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

このファイルには、JP固有コードや重要な設定ファイルの変更が記載されています。

## JP固有コードの変更

"@
        
        $jpFiles = $categories["JP固有コード"]
        if ($jpFiles.Count -gt 0) {
            foreach ($file in $jpFiles | Sort-Object Path) {
                $importantContent += "`n### ``$($file.Path)```n`n"
                
                # Check if this is a Python file and has a generated diff
                $safePath = $file.Path -replace '[\\/:*?"<>|]', '_'
                $generatedDiffFile = Join-Path $generatedDir "$safePath.md"
                
                if ($file.Path -like "*.py" -and (Test-Path $generatedDiffFile)) {
                    # Python file with generated diff - add link to generated file
                    $importantContent += "- **差分ファイル**: [``$safePath.md``](./generated/$safePath.md)`n"
                } else {
                    # Non-Python file or no generated diff - show git diff command
                    $importantContent += "- **差分を確認**: ``git diff --no-index `"$($file.Source2025)`" `"$($file.Current)`"``"
                }
                $importantContent += "`n`n"
            }
        } else {
            $importantContent += "`nJP固有コードの変更はありません。`n"
        }
        
        $importantContent | Out-File -FilePath (Join-Path $outputDirPath "important-changes.md") -Encoding UTF8
        
        # Generate diff files for Python files in generated/ folder
        Write-Host "Generating diff files for Python files..." -ForegroundColor Cyan
        # Always use -w to ignore whitespace differences (indentation changes)
        $diffOptions = "-w"
        
        $pythonFiles = $changedFiles | Where-Object { $_.Path -like "*.py" }
        $generatedCount = 0
        
        foreach ($file in $pythonFiles) {
            try {
                # Use git diff with proper encoding handling
                $diffCmd = "git -c core.quotepath=false diff --no-index"
                if ($diffOptions) {
                    $diffCmd += " $diffOptions"
                }
                $diffCmd += " `"$($file.Source2025)`" `"$($file.Current)`""
                
                # Capture output with proper encoding
                $processInfo = New-Object System.Diagnostics.ProcessStartInfo
                $processInfo.FileName = "git"
                $processInfo.Arguments = "-c core.quotepath=false diff --no-index $diffOptions `"$($file.Source2025)`" `"$($file.Current)`""
                $processInfo.UseShellExecute = $false
                $processInfo.RedirectStandardOutput = $true
                $processInfo.RedirectStandardError = $true
                $processInfo.StandardOutputEncoding = [System.Text.Encoding]::UTF8
                $processInfo.StandardErrorEncoding = [System.Text.Encoding]::UTF8
                $processInfo.CreateNoWindow = $true
                
                $process = New-Object System.Diagnostics.Process
                $process.StartInfo = $processInfo
                $process.Start() | Out-Null
                $diffOutput = $process.StandardOutput.ReadToEnd()
                $errorOutput = $process.StandardError.ReadToEnd()
                $process.WaitForExit()
                $exitCode = $process.ExitCode
                
                # git diff returns 0 (no diff) or 1 (diff found), both are valid
                # Exit code 129+ indicates an error
                if ($exitCode -le 1) {
                    # Skip if diff is empty (only whitespace differences)
                    $diffOutputTrimmed = $diffOutput.Trim()
                    if ([string]::IsNullOrWhiteSpace($diffOutputTrimmed)) {
                        # Only whitespace differences, skip this file
                        continue
                    }
                    
                    $safePath = $file.Path -replace '[\\/:*?"<>|]', '_'
                    $diffFile = Join-Path $generatedDir "$safePath.md"
                    
                    # Format as Markdown code block for better readability
                    $diffContent = @"
# Diff for: ``$($file.Path)``

**Source 2025.3.x jp**: ``$($file.Source2025)``  
**Current**: ``$($file.Current)``

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

``````diff
$diffOutput
``````
"@
                    # Use UTF-8 with BOM for better compatibility
                    $utf8WithBom = New-Object System.Text.UTF8Encoding $true
                    [System.IO.File]::WriteAllText($diffFile, $diffContent, $utf8WithBom)
                    $generatedCount++
                } else {
                    Write-Host "  Warning: git diff failed (exit code $exitCode) for $($file.Path)" -ForegroundColor Yellow
                    if ($errorOutput) {
                        Write-Host "    Error: $errorOutput" -ForegroundColor Yellow
                    }
                }
            } catch {
                Write-Host "  Warning: Failed to generate diff for $($file.Path): $_" -ForegroundColor Yellow
            }
        }
        
        Write-Host "Markdown reports generated in: $outputDirPath" -ForegroundColor Green
        Write-Host "  - summary.md" -ForegroundColor Gray
        Write-Host "  - file-list.md" -ForegroundColor Gray
        Write-Host "  - important-changes.md" -ForegroundColor Gray
        Write-Host "  - generated/ ($generatedCount Python diff files)" -ForegroundColor Gray
    }
}

if ($ShowStats) {
    Write-Host "`n=== Statistics ===" -ForegroundColor Cyan
    Write-Host "Total files compared: $($changedFiles.Count + $identicalFiles + $addedFiles.Count)" -ForegroundColor Gray
    Write-Host "Change rate: $([math]::Round(($changedFiles.Count / ($changedFiles.Count + $identicalFiles)) * 100, 2))%" -ForegroundColor Gray
}
