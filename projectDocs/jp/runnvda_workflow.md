# runnvda.bat を使った試行錯誤ワークフロー

`scons launcher` を実行せずに、`runnvda.bat` を使って MeCab のデバッグを行う方法。

## このブランチの対象

* **アーキテクチャ**: x86（32bit）
* **Python バージョン**: 3.11
* **ビルド環境**: Windows 10/11

## 前提条件

* 多くの日本語版固有ファイルは `source/` に直接配置されています
* `source/synthDrivers/jtalk/mecab.py` を直接編集します

## ワークフロー

### 1. mecab.py を編集

```powershell
# source/synthDrivers/jtalk/mecab.py を直接編集
code source/synthDrivers/jtalk/mecab.py
```

### 2. runnvda.bat でテスト

```powershell
# NVDA を起動してテスト
.\runnvda.bat
```

### 3. ログを確認

NVDA のログは通常 `%APPDATA%\nvda\nvda.log` に出力されます。

## 注意事項

* `source/synthDrivers/jtalk/mecab.py` を直接編集します（Git 管理も `source/` 配下で行われます）
* `source/synthDrivers/jtalk/libopenjtalk.dll` や `libmecab.dll` が必要な場合は、`scons jtalkSync` を実行してください

## runJpSmokeTests.ps1 を使ったテスト

`runnvda.bat` の代わりに、`runJpSmokeTests.ps1` を使って MeCab の動作をテストすることもできます。

### 基本的な使い方

```powershell
# すべてのテストを実行（依存関係とJTalk資産を自動準備）
.\jptools\runJpSmokeTests.ps1

# 依存関係が既にインストールされている場合
.\jptools\runJpSmokeTests.ps1 -SkipInstall

# 依存関係とJTalk資産が既に準備されている場合
.\jptools\runJpSmokeTests.ps1 -SkipInstall -SkipJtalkSync

# 特定のテストのみ実行（例: test_pass2）
.\jptools\runJpSmokeTests.ps1 -SkipInstall -SkipJtalkSync -TestFilter "test_pass2"
```

### 詳細情報

**詳細な使い方、オプションの説明、トラブルシューティングについては、`projectDocs/jp/troubleshooting_runjp_smoke_tests.md` を参照してください。**

このドキュメントには以下の情報が含まれています：

* オプションの詳細な説明（`-SkipInstall`, `-SkipJtalkSync`, `-TestFilter`, `-MaxTests` など）
* テストケース数の段階的な増やし方
* ログファイルの確認方法
* よくあるエラーとその解決策
* CI環境での注意事項
