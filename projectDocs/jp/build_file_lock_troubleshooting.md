# ビルド時のファイルロックエラー対処法

## 症状

ビルド中に以下のようなエラーが発生する：

```
scons: *** [source\lib64\IAccessible2proxy.dll] アクセスが拒否されました。
scons: building terminated because of errors.
```

## 原因

`source\lib64\` ディレクトリ内の DLL ファイルが別のプロセスによってロックされている。

## 対処法

### 1. 実行中の NVDA を終了

NVDA が実行中の場合、DLL ファイルがロックされる可能性があります。

```powershell
# NVDA プロセスを確認
Get-Process | Where-Object { $_.ProcessName -like "*nvda*" }

# NVDA を終了（必要に応じて）
Stop-Process -Name "nvda" -Force -ErrorAction SilentlyContinue
```

### 2. 以前のビルドプロセスを確認・終了

SCons やビルドツールのプロセスが残っている可能性があります。

```powershell
# Python/SCons プロセスを確認
Get-Process | Where-Object { $_.ProcessName -like "*python*" -or $_.ProcessName -like "*scons*" }

# 必要に応じて終了
Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue
```

### 3. ファイルエクスプローラーを閉じる

`source\lib64\` ディレクトリを開いているファイルエクスプローラーウィンドウを閉じる。

### 4. ウイルス対策ソフトを一時的に無効化

リアルタイムスキャンがファイルをロックしている可能性があります（ビルド完了後に再有効化）。

### 5. ファイルを手動で削除して再ビルド

```powershell
# ロックされているファイルを削除（プロセス終了後）
Remove-Item "source\lib64\IAccessible2proxy.dll" -Force -ErrorAction SilentlyContinue
Remove-Item "source\lib64\ISimpleDOM.dll" -Force -ErrorAction SilentlyContinue

# クリーンビルド
.\scons.bat -c
.\scons.bat source dist launcher --all-cores
```

### 6. プロセスエクスプローラーでロックを確認

[Process Explorer](https://docs.microsoft.com/en-us/sysinternals/downloads/process-explorer) を使用して、どのプロセスがファイルをロックしているか確認：

1. Process Explorer を起動
2. `Ctrl+F` でファイル検索
3. `IAccessible2proxy.dll` を検索
4. ロックしているプロセスを確認・終了

## 予防策

### ビルド前にクリーンアップ

```powershell
# ビルド前に実行中のプロセスを確認
Get-Process | Where-Object { $_.ProcessName -like "*nvda*" -or $_.ProcessName -like "*python*" }

# クリーンビルドを実行
.\scons.bat -c
```

### ビルドスクリプトに追加

`certBuild2025.ps1` などのビルドスクリプトの冒頭に以下を追加：

```powershell
# 実行中の NVDA を確認
$nvdaProcess = Get-Process -Name "nvda" -ErrorAction SilentlyContinue
if ($nvdaProcess) {
    Write-Warning "NVDA is running. Please close it before building."
    exit 1
}
```

## 関連ドキュメント

* `projectDocs/jp/local_verification_build_dependencies.md`: ビルド検証手順
* `projectDocs/jp/code-signing-dependencies.md`: ビルド依存関係の詳細
