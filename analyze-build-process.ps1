# PowerShellスクリプト: miscDepsJpビルドプロセスの分析
# このスクリプトは、miscDepsJpのビルドプロセスを分析し、改善可能な箇所を特定します。
# フェーズ3（ビルドプロセスの改善）の準備として使用します。

# エラー発生時に停止
$ErrorActionPreference = "Stop"

# 作業ディレクトリの確認
$currentDir = Get-Location
Write-Host "現在の作業ディレクトリ: $currentDir" -ForegroundColor Cyan
Write-Host "このスクリプトは、nvdajpリポジトリのルートディレクトリで実行する必要があります。" -ForegroundColor Yellow
$confirmation = Read-Host "続行しますか？ (y/n)"
if ($confirmation -ne "y") {
    Write-Host "スクリプトを終了します。" -ForegroundColor Red
    exit
}

# 分析結果の出力先
$outputDir = "build-analysis_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $outputDir | Out-Null
Write-Host "分析結果を $outputDir に出力します。" -ForegroundColor Green

# ビルドスクリプトの収集
Write-Host "ビルドスクリプトを収集しています..." -ForegroundColor Cyan
$buildScripts = @(
    "jptools\setupMiscDepsJp.cmd",
    "jptools\cleanMiscDepsJp.cmd",
    "miscDepsJp\include\jtalk\all-build.cmd",
    "miscDepsJp\include\jtalk\all-install.cmd",
    "miscDepsJp\include\jtalk\all-clean.cmd",
    "miscDepsJp\include\python-jtalk\build.cmd",
    "miscDepsJp\include\python-jtalk\all.mak",
    "miscDepsJp\include\python-jtalk\hts.mak",
    "miscDepsJp\include\python-jtalk\lib\Makefile.mak"
)

# ビルドスクリプトの内容を収集
$buildScriptContents = @{}
foreach ($script in $buildScripts) {
    if (Test-Path $script) {
        $content = Get-Content -Path $script -Raw
        $buildScriptContents[$script] = $content
        Write-Host "スクリプト $script を収集しました。" -ForegroundColor Green
    } else {
        Write-Host "スクリプト $script が見つかりません。" -ForegroundColor Yellow
    }
}

# ビルドスクリプトの内容を出力
$buildScriptContents | ConvertTo-Json -Depth 10 | Out-File -FilePath "$outputDir\build-scripts.json"

# ファイルコピー操作の分析
Write-Host "ファイルコピー操作を分析しています..." -ForegroundColor Cyan
$copyOperations = @()

foreach ($script in $buildScripts) {
    if (-not $buildScriptContents.ContainsKey($script)) {
        continue
    }
    
    $content = $buildScriptContents[$script]
    
    # Windowsのcopyコマンドを検出
    $copyMatches = [regex]::Matches($content, "copy\s+([^\r\n]+)")
    foreach ($match in $copyMatches) {
        $copyOperation = $match.Groups[1].Value.Trim()
        $copyOperations += @{
            "Script" = $script
            "Operation" = "copy"
            "Command" = $copyOperation
        }
    }
    
    # PowerShellのCopy-Itemを検出
    $copyItemMatches = [regex]::Matches($content, "Copy-Item\s+([^\r\n]+)")
    foreach ($match in $copyItemMatches) {
        $copyOperation = $match.Groups[1].Value.Trim()
        $copyOperations += @{
            "Script" = $script
            "Operation" = "Copy-Item"
            "Command" = $copyOperation
        }
    }
}

# ファイルコピー操作を出力
$copyOperations | ConvertTo-Json -Depth 10 | Out-File -FilePath "$outputDir\copy-operations.json"
Write-Host "ファイルコピー操作を $($copyOperations.Count) 件検出しました。" -ForegroundColor Green

# パッチ適用操作の分析
Write-Host "パッチ適用操作を分析しています..." -ForegroundColor Cyan
$patchOperations = @()

foreach ($script in $buildScripts) {
    if (-not $buildScriptContents.ContainsKey($script)) {
        continue
    }
    
    $content = $buildScriptContents[$script]
    
    # patchコマンドを検出
    $patchMatches = [regex]::Matches($content, "patch\s+([^\r\n]+)")
    foreach ($match in $patchMatches) {
        $patchOperation = $match.Groups[1].Value.Trim()
        $patchOperations += @{
            "Script" = $script
            "Operation" = "patch"
            "Command" = $patchOperation
        }
    }
}

# パッチ適用操作を出力
$patchOperations | ConvertTo-Json -Depth 10 | Out-File -FilePath "$outputDir\patch-operations.json"
Write-Host "パッチ適用操作を $($patchOperations.Count) 件検出しました。" -ForegroundColor Green

# ビルド依存関係の分析
Write-Host "ビルド依存関係を分析しています..." -ForegroundColor Cyan
$buildDependencies = @{}

# setupMiscDepsJp.cmdの依存関係を分析
if ($buildScriptContents.ContainsKey("jptools\setupMiscDepsJp.cmd")) {
    $content = $buildScriptContents["jptools\setupMiscDepsJp.cmd"]
    $callMatches = [regex]::Matches($content, "call\s+([^\r\n]+)")
    $dependencies = @()
    foreach ($match in $callMatches) {
        $dependency = $match.Groups[1].Value.Trim()
        $dependencies += $dependency
    }
    $buildDependencies["jptools\setupMiscDepsJp.cmd"] = $dependencies
}

# all-build.cmdの依存関係を分析
if ($buildScriptContents.ContainsKey("miscDepsJp\include\jtalk\all-build.cmd")) {
    $content = $buildScriptContents["miscDepsJp\include\jtalk\all-build.cmd"]
    $callMatches = [regex]::Matches($content, "call\s+([^\r\n]+)")
    $dependencies = @()
    foreach ($match in $callMatches) {
        $dependency = $match.Groups[1].Value.Trim()
        $dependencies += $dependency
    }
    $buildDependencies["miscDepsJp\include\jtalk\all-build.cmd"] = $dependencies
}

# all.makの依存関係を分析
if ($buildScriptContents.ContainsKey("miscDepsJp\include\python-jtalk\all.mak")) {
    $content = $buildScriptContents["miscDepsJp\include\python-jtalk\all.mak"]
    $nmakeMatches = [regex]::Matches($content, "nmake\s+/f\s+([^\s\r\n]+)")
    $dependencies = @()
    foreach ($match in $nmakeMatches) {
        $dependency = $match.Groups[1].Value.Trim()
        $dependencies += $dependency
    }
    $buildDependencies["miscDepsJp\include\python-jtalk\all.mak"] = $dependencies
}

# ビルド依存関係を出力
$buildDependencies | ConvertTo-Json -Depth 10 | Out-File -FilePath "$outputDir\build-dependencies.json"
Write-Host "ビルド依存関係を分析しました。" -ForegroundColor Green

# ビルドプロセスの図式化（DOT形式）
Write-Host "ビルドプロセスを図式化しています..." -ForegroundColor Cyan
$dotGraph = @"
digraph BuildProcess {
  rankdir=LR;
  node [shape=box, style=filled, fillcolor=lightblue];

  // Main build script
  setupMiscDepsJp [label="jptools\\setupMiscDepsJp.cmd"];

  // Build scripts
  allBuild [label="miscDepsJp\\include\\jtalk\\all-build.cmd"];
  allInstall [label="miscDepsJp\\include\\jtalk\\all-install.cmd"];
  allClean [label="miscDepsJp\\include\\jtalk\\all-clean.cmd"];
  pythonJtalkBuild [label="miscDepsJp\\include\\python-jtalk\\build.cmd"];
  
  // Dependencies
  setupMiscDepsJp -> allBuild;
  setupMiscDepsJp -> allInstall;
  setupMiscDepsJp -> allClean;
  allBuild -> pythonJtalkBuild;
  
  // Copy operations
  node [shape=ellipse, style=filled, fillcolor=lightgreen];
"@

# コピー操作をグラフに追加
$copyNodeId = 0
foreach ($copyOp in $copyOperations) {
    $copyNodeId++
    $dotGraph += "`n  copy$copyNodeId [label=`"Copy: $($copyOp.Command)`"];"
    $scriptName = $copyOp.Script -replace "\\", "\\\\"
    $dotGraph += "`n  `"$scriptName`" -> copy$copyNodeId;"
}

# パッチ操作をグラフに追加
$patchNodeId = 0
foreach ($patchOp in $patchOperations) {
    $patchNodeId++
    $dotGraph += "`n  patch$patchNodeId [label=`"Patch: $($patchOp.Command)`", fillcolor=lightyellow];"
    $scriptName = $patchOp.Script -replace "\\", "\\\\"
    $dotGraph += "`n  `"$scriptName`" -> patch$patchNodeId;"
}

$dotGraph += "`n}"

# DOTグラフを出力
$dotGraph | Out-File -FilePath "$outputDir\build-process.dot"
Write-Host "ビルドプロセスの図式化を $outputDir\build-process.dot に出力しました。" -ForegroundColor Green

# 改善提案の生成
Write-Host "改善提案を生成しています..." -ForegroundColor Cyan
$improvements = @"
# miscDepsJpビルドプロセスの改善提案

## 分析結果

### ファイルコピー操作

ファイルコピー操作が $($copyOperations.Count) 件検出されました。これらの操作は、同じファイルが複数の場所に存在することを意味し、一貫性の維持が難しくなる原因となっています。

### パッチ適用操作

パッチ適用操作が $($patchOperations.Count) 件検出されました。これらの操作は、サブモジュールのファイルを直接修正するのではなく、コピーしてからパッチを適用しています。これにより、サブモジュールの更新時に問題が発生する可能性があります。

## 改善提案

### 1. ファイルコピーの最小化

現在のビルドプロセスでは、サブモジュール間でファイルがコピーされています。これを改善するために、以下の方法を検討します：

1. **直接参照の使用**:
   - python-jtalk内からlibopenjtalkとhtsengineapiを直接参照するように修正
   - 相対パスを使用して、コピーではなく元のファイルを参照

2. **シンボリックリンクの使用**:
   - 必要な場合は、ファイルをコピーする代わりにシンボリックリンクを作成
   - これにより、ファイルの一貫性を維持しながら、複数の場所からアクセス可能に

### 2. パッチ適用プロセスの改善

現在のパッチ適用プロセスでは、サブモジュールからファイルをコピーしてからパッチを適用しています。これを改善するために、以下の方法を検討します：

1. **フォークリポジトリの使用**:
   - 必要な修正を含むフォークリポジトリを作成
   - サブモジュールとして、修正済みのフォークリポジトリを参照

2. **ビルド時のパッチ適用**:
   - 元のファイルを直接修正せず、ビルド時にパッチを適用
   - ビルド結果のみを使用し、元のファイルは変更しない

### 3. ビルドスクリプトの簡素化

現在のビルドスクリプトは複雑で、多くの依存関係があります。これを改善するために、以下の方法を検討します：

1. **統一されたビルドシステムの使用**:
   - 複数のMakefileやバッチファイルを統合
   - 依存関係を明示的に定義し、並列ビルドを可能に

2. **ビルド設定の集中管理**:
   - 共通の設定を一箇所で管理
   - 環境変数を使用して、各ビルドスクリプトに設定を渡す

## 実装計画

上記の改善提案を実装するための計画を以下に示します：

1. **フェーズ3.1: ビルドスクリプトの分析と設計**
   - 現在のビルドプロセスの詳細な依存関係図を作成
   - 改善案の詳細設計

2. **フェーズ3.2: ファイルコピーの最小化**
   - python-jtalk/all.makの修正
   - 直接参照を使用するように変更

3. **フェーズ3.3: パッチ適用プロセスの改善**
   - ビルド時のパッチ適用方法の実装
   - パッチファイルの整理と管理

4. **フェーズ3.4: ビルドスクリプトの簡素化**
   - 統一されたビルドシステムの設計と実装
   - 依存関係の明示的な定義

各フェーズの実装後には、ビルドテストと機能テストを行い、問題がないことを確認します。
"@

# 改善提案を出力
$improvements | Out-File -FilePath "$outputDir\improvement-proposals.md"
Write-Host "改善提案を $outputDir\improvement-proposals.md に出力しました。" -ForegroundColor Green

# 重複ファイルの分析
Write-Host "重複ファイルを分析しています..." -ForegroundColor Cyan

# python-jtalk/libopenjtalkとlibopenjtalkの比較
$pythonJtalkLibopenjtalkDir = "miscDepsJp\include\python-jtalk\libopenjtalk"
$libopenjtalkDir = "miscDepsJp\include\libopenjtalk"

if (Test-Path $pythonJtalkLibopenjtalkDir -PathType Container -and Test-Path $libopenjtalkDir -PathType Container) {
    $duplicateFiles = @()
    
    $pythonJtalkLibopenjtalkFiles = Get-ChildItem -Path $pythonJtalkLibopenjtalkDir -Recurse -File | Select-Object -ExpandProperty FullName
    $libopenjtalkFiles = Get-ChildItem -Path $libopenjtalkDir -Recurse -File | Select-Object -ExpandProperty FullName
    
    foreach ($file1 in $pythonJtalkLibopenjtalkFiles) {
        $relativePath = $file1.Substring($pythonJtalkLibopenjtalkDir.Length)
        $file2 = Join-Path -Path $libopenjtalkDir -ChildPath $relativePath
        
        if (Test-Path $file2 -PathType Leaf) {
            $hash1 = Get-FileHash -Path $file1 -Algorithm MD5
            $hash2 = Get-FileHash -Path $file2 -Algorithm MD5
            
            $isDuplicate = $hash1.Hash -eq $hash2.Hash
            $duplicateFiles += @{
                "File1" = $file1
                "File2" = $file2
                "IsDuplicate" = $isDuplicate
                "Hash1" = $hash1.Hash
                "Hash2" = $hash2.Hash
            }
        }
    }
    
    # 重複ファイルを出力
    $duplicateFiles | ConvertTo-Json -Depth 10 | Out-File -FilePath "$outputDir\duplicate-files.json"
    $duplicateCount = ($duplicateFiles | Where-Object { $_.IsDuplicate -eq $true }).Count
    Write-Host "重複ファイルを $duplicateCount 件検出しました。" -ForegroundColor Green
} else {
    Write-Host "python-jtalk/libopenjtalkまたはlibopenjtalkディレクトリが見つかりません。" -ForegroundColor Yellow
}

Write-Host "分析が完了しました。結果は $outputDir ディレクトリに出力されています。" -ForegroundColor Green
Write-Host "この分析結果を基に、フェーズ3（ビルドプロセスの改善）の実装を検討してください。" -ForegroundColor Yellow
