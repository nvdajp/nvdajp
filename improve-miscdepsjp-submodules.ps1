# PowerShellスクリプト: miscDepsJpサブモジュール構造の改善
# このスクリプトは、miscDepsJpのサブモジュール構造を改善するためのフェーズ2の作業を自動化します。
# 注意: このスクリプトを実行する前に、必ずリポジトリのバックアップを作成してください。

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

# バックアップの作成
Write-Host "バックアップを作成しています..." -ForegroundColor Cyan
$backupDir = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $backupDir | Out-Null
Copy-Item -Path ".git" -Destination "$backupDir\.git" -Recurse
Copy-Item -Path ".gitmodules" -Destination "$backupDir\.gitmodules"
Copy-Item -Path "miscDepsJp" -Destination "$backupDir\miscDepsJp" -Recurse
Write-Host "バックアップを $backupDir に作成しました。" -ForegroundColor Green

# 新しいブランチの作成
Write-Host "新しいブランチを作成しています..." -ForegroundColor Cyan
git checkout -b improve-miscdepsjp-submodules
Write-Host "ブランチ 'improve-miscdepsjp-submodules' を作成しました。" -ForegroundColor Green

# miscDepsJpサブモジュールのコミットハッシュの記録
Write-Host "miscDepsJpサブモジュールのコミットハッシュを記録しています..." -ForegroundColor Cyan
Push-Location miscDepsJp
$miscDepsJpCommit = git rev-parse HEAD
$miscDepsJpCommit | Out-File -FilePath "..\miscDepsJp-commit.txt"
Pop-Location
Write-Host "miscDepsJpのコミットハッシュ: $miscDepsJpCommit" -ForegroundColor Green

# 各サブモジュールのコミットハッシュの記録
Write-Host "各サブモジュールのコミットハッシュを記録しています..." -ForegroundColor Cyan

# libopenjtalk
try {
    Push-Location miscDepsJp\include\libopenjtalk
    $libopenjtalkCommit = git rev-parse HEAD
    $libopenjtalkCommit | Out-File -FilePath "..\..\..\libopenjtalk-commit.txt"
    Pop-Location
    Write-Host "libopenjtalkのコミットハッシュ: $libopenjtalkCommit" -ForegroundColor Green
} catch {
    Write-Host "libopenjtalkのコミットハッシュの取得に失敗しました: $_" -ForegroundColor Red
    Write-Host "手動でコミットハッシュを確認し、libopenjtalk-commit.txtに保存してください。" -ForegroundColor Yellow
}

# htsengineapi
try {
    Push-Location miscDepsJp\include\htsengineapi
    $htsengineapiCommit = git rev-parse HEAD
    $htsengineapiCommit | Out-File -FilePath "..\..\..\htsengineapi-commit.txt"
    Pop-Location
    Write-Host "htsengineapiのコミットハッシュ: $htsengineapiCommit" -ForegroundColor Green
} catch {
    Write-Host "htsengineapiのコミットハッシュの取得に失敗しました: $_" -ForegroundColor Red
    Write-Host "手動でコミットハッシュを確認し、htsengineapi-commit.txtに保存してください。" -ForegroundColor Yellow
}

# python-jtalk
try {
    Push-Location miscDepsJp\include\python-jtalk
    $pythonJtalkCommit = git rev-parse HEAD
    $pythonJtalkCommit | Out-File -FilePath "..\..\..\python-jtalk-commit.txt"
    Pop-Location
    Write-Host "python-jtalkのコミットハッシュ: $pythonJtalkCommit" -ForegroundColor Green
} catch {
    Write-Host "python-jtalkのコミットハッシュの取得に失敗しました: $_" -ForegroundColor Red
    Write-Host "手動でコミットハッシュを確認し、python-jtalk-commit.txtに保存してください。" -ForegroundColor Yellow
}

# libkuraji
try {
    Push-Location miscDepsJp\include\libkuraji
    $libkurajiCommit = git rev-parse HEAD
    $libkurajiCommit | Out-File -FilePath "..\..\..\libkuraji-commit.txt"
    Pop-Location
    Write-Host "libkurajiのコミットハッシュ: $libkurajiCommit" -ForegroundColor Green
} catch {
    Write-Host "libkurajiのコミットハッシュの取得に失敗しました: $_" -ForegroundColor Red
    Write-Host "手動でコミットハッシュを確認し、libkuraji-commit.txtに保存してください。" -ForegroundColor Yellow
}

# 一時ディレクトリの作成とmiscDepsJpの内容のコピー
Write-Host "miscDepsJpの内容を一時ディレクトリにコピーしています..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path "temp-miscdepsjp" | Out-Null
Copy-Item -Path "miscDepsJp\*" -Destination "temp-miscdepsjp" -Recurse -Force

# miscDepsJpサブモジュールの削除
Write-Host "miscDepsJpサブモジュールを削除しています..." -ForegroundColor Cyan
git submodule deinit -f miscDepsJp
git rm --cached miscDepsJp
if (Test-Path ".git\modules\miscDepsJp") {
    Remove-Item -Path ".git\modules\miscDepsJp" -Recurse -Force
}

# miscDepsJpディレクトリの作成と内容のコピー
Write-Host "miscDepsJpディレクトリを作成し、内容をコピーしています..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path "miscDepsJp" | Out-Null
Copy-Item -Path "temp-miscdepsjp\*" -Destination "miscDepsJp" -Recurse -Force

# 一時ディレクトリの削除
Write-Host "一時ディレクトリを削除しています..." -ForegroundColor Cyan
Remove-Item -Path "temp-miscdepsjp" -Recurse -Force

# .gitmodulesファイルのバックアップと編集
Write-Host ".gitmodulesファイルをバックアップし、編集しています..." -ForegroundColor Cyan
Copy-Item -Path ".gitmodules" -Destination ".gitmodules.bak"

# .gitmodulesファイルの内容を読み込む
$gitmodules = Get-Content -Path ".gitmodules" -Raw

# miscDepsJpエントリを削除
$gitmodules = $gitmodules -replace '\[submodule "miscDepsJp"\][^\[]*', ''

# 新しいサブモジュールエントリを追加
$newEntries = @"

[submodule "miscDepsJp/include/libopenjtalk"]
	path = miscDepsJp/include/libopenjtalk
	url = https://github.com/nishimotz/libopenjtalk.git
[submodule "miscDepsJp/include/htsengineapi"]
	path = miscDepsJp/include/htsengineapi
	url = https://github.com/nishimotz/htsengineapi.git
[submodule "miscDepsJp/include/python-jtalk"]
	path = miscDepsJp/include/python-jtalk
	url = https://github.com/nvdajp/python-jtalk.git
[submodule "miscDepsJp/include/libkuraji"]
	path = miscDepsJp/include/libkuraji
	url = https://github.com/nishimotz/libkuraji.git
"@

$gitmodules = $gitmodules + $newEntries

# 更新した内容を.gitmodulesファイルに書き込む
$gitmodules | Set-Content -Path ".gitmodules"

# 不要なファイルの削除
Write-Host "不要なファイルを削除しています..." -ForegroundColor Cyan
if (Test-Path "miscDepsJp\.gitmodules") {
    Remove-Item -Path "miscDepsJp\.gitmodules" -Force
}
if (Test-Path "miscDepsJp\appveyor.yml") {
    Remove-Item -Path "miscDepsJp\appveyor.yml" -Force
}

# サブモジュールの初期化
Write-Host "サブモジュールを初期化しています..." -ForegroundColor Cyan
git submodule init

# 各サブモジュールを特定のコミットでチェックアウト
Write-Host "各サブモジュールを特定のコミットでチェックアウトしています..." -ForegroundColor Cyan

# libopenjtalk
Write-Host "libopenjtalkをチェックアウトしています..." -ForegroundColor Cyan
git submodule update --init miscDepsJp/include/libopenjtalk
Push-Location miscDepsJp\include\libopenjtalk
$libopenjtalkCommit = Get-Content -Path "..\..\..\libopenjtalk-commit.txt"
git checkout $libopenjtalkCommit
Pop-Location
Write-Host "libopenjtalkをコミット $libopenjtalkCommit でチェックアウトしました。" -ForegroundColor Green

# htsengineapi
Write-Host "htsengineapiをチェックアウトしています..." -ForegroundColor Cyan
git submodule update --init miscDepsJp/include/htsengineapi
Push-Location miscDepsJp\include\htsengineapi
$htsengineapiCommit = Get-Content -Path "..\..\..\htsengineapi-commit.txt"
git checkout $htsengineapiCommit
Pop-Location
Write-Host "htsengineapiをコミット $htsengineapiCommit でチェックアウトしました。" -ForegroundColor Green

# python-jtalk
Write-Host "python-jtalkをチェックアウトしています..." -ForegroundColor Cyan
git submodule update --init miscDepsJp/include/python-jtalk
Push-Location miscDepsJp\include\python-jtalk
$pythonJtalkCommit = Get-Content -Path "..\..\..\python-jtalk-commit.txt"
git checkout $pythonJtalkCommit
Pop-Location
Write-Host "python-jtalkをコミット $pythonJtalkCommit でチェックアウトしました。" -ForegroundColor Green

# libkuraji
Write-Host "libkurajiをチェックアウトしています..." -ForegroundColor Cyan
git submodule update --init miscDepsJp/include/libkuraji
Push-Location miscDepsJp\include\libkuraji
$libkurajiCommit = Get-Content -Path "..\..\..\libkuraji-commit.txt"
git checkout $libkurajiCommit
Pop-Location
Write-Host "libkurajiをコミット $libkurajiCommit でチェックアウトしました。" -ForegroundColor Green

# 一時ファイルの削除
Write-Host "一時ファイルを削除しています..." -ForegroundColor Cyan
Remove-Item -Path "libopenjtalk-commit.txt", "htsengineapi-commit.txt", "python-jtalk-commit.txt", "libkuraji-commit.txt", "miscDepsJp-commit.txt"

# 変更のコミット
Write-Host "変更をコミットしています..." -ForegroundColor Cyan
git add .gitmodules
git add miscDepsJp
git commit -m "Refactor: Convert nested submodules to direct submodules"
Write-Host "変更をコミットしました。" -ForegroundColor Green

# 検証手順の表示
Write-Host "以下のコマンドを実行して、変更を検証してください:" -ForegroundColor Yellow
Write-Host "jptools\devbuild2024.cmd" -ForegroundColor Cyan
Write-Host "runnvda.bat" -ForegroundColor Cyan

Write-Host "スクリプトが完了しました。" -ForegroundColor Green
Write-Host "問題が発生した場合は、$backupDir からリポジトリを復元できます。" -ForegroundColor Yellow
