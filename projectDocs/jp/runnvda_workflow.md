# runnvda.bat を使った試行錯誤ワークフロー

`scons launcher` を実行せずに、`runnvda.bat` を使って MeCab のデバッグを行う方法。

## このブランチの対象

* **アーキテクチャ**: x86（32bit）
* **Python バージョン**: 3.11
* **ビルド環境**: Windows 10/11

## 前提条件

- `miscDepsJp/include/python-jtalk/mecab.py` を編集
- `source/synthDrivers/jtalk/mecab.py` に変更を反映する必要がある

## ワークフロー

### 1. mecab.py を編集

```powershell
# miscDepsJp/include/python-jtalk/mecab.py を編集
code miscDepsJp/include/python-jtalk/mecab.py
```

### 2. overlay を実行して source にコピー

```powershell
# scons miscdepsjp を実行
# これにより以下が実行される:
# - miscDepsJp/source から source への overlay コピー
# - miscDepsJp/include/python-jtalk から source/synthDrivers/jtalk へのコピー
#   (jtalkCore.py, mecab.py, text2mecab.py)
uv run scons miscdepsjp
```

### 3. runnvda.bat でテスト

```powershell
# NVDA を起動してテスト
.\runnvda.bat
```

### 4. ログを確認

NVDA のログは通常 `%APPDATA%\nvda\nvda.log` に出力されます。

## 注意事項

- `mecab.py` を編集したら、必ず `scons miscdepsjp` を実行して `source/synthDrivers/jtalk/mecab.py` を更新する必要があります
- `scons miscdepsjp` は `jtalkPrep` に依存しているため、`libopenjtalk.dll` が `miscDepsJp/source/synthDrivers/jtalk/libopenjtalk.dll` に存在する必要があります
- `scons miscdepsjp` は比較的高速に実行されます（Python ファイルのコピーのみ）

## 高速化のヒント

`mecab.py` の変更が小さい場合、直接 `source/synthDrivers/jtalk/mecab.py` を編集して `runnvda.bat` でテストすることも可能ですが、最終的には `miscDepsJp/include/python-jtalk/mecab.py` に反映する必要があります。

## runJpSmokeTests.ps1 を使ったテスト

`runnvda.bat` の代わりに、`runJpSmokeTests.ps1` を使って MeCab の動作をテストすることもできます。

**詳細なトラブルシューティング情報は `projectDocs/jp/troubleshooting_runjp_smoke_tests.md` を参照してください。**

### 基本的な使い方

```powershell
# すべてのテストを実行（依存関係とoverlayを自動実行）
.\jptools\runJpSmokeTests.ps1

# 依存関係が既にインストールされている場合
.\jptools\runJpSmokeTests.ps1 -SkipInstall

# 依存関係とoverlayが既に準備されている場合
.\jptools\runJpSmokeTests.ps1 -SkipInstall -SkipJtalkSync

# 特定のテストのみ実行（例: test_pass2）
.\jptools\runJpSmokeTests.ps1 -SkipInstall -SkipJtalkSync -TestFilter "test_pass2"

# テストケース数を制限して実行（例: 10件まで）
.\jptools\runJpSmokeTests.ps1 -SkipInstall -SkipJtalkSync -TestFilter "test_pass2" -MaxTests 10
```

### テストケース数の段階的な増やし方

MeCab のアクセス違反が特定のテストケース数で発生する場合、段階的にテストケース数を増やして失敗する閾値を特定できます：

```powershell
# 1件のテストケースで実行
.\jptools\runJpSmokeTests.ps1 -SkipInstall -TestFilter "test_pass2" -MaxTests 1

# 5件のテストケースで実行
.\jptools\runJpSmokeTests.ps1 -SkipInstall -TestFilter "test_pass2" -MaxTests 5

# 10件のテストケースで実行
.\jptools\runJpSmokeTests.ps1 -SkipInstall -TestFilter "test_pass2" -MaxTests 10

# 11件のテストケースで実行（失敗する可能性がある）
.\jptools\runJpSmokeTests.ps1 -SkipInstall -TestFilter "test_pass2" -MaxTests 11
```

### ログファイルの確認

テスト実行後、`miscDepsJp/jptools/__h2output.txt` に詳細なログが出力されます：

```powershell
# ログファイルの最後の30行を確認
Get-Content miscDepsJp\jptools\__h2output.txt | Select-Object -Last 30

# テストケース番号を検索
Get-Content miscDepsJp\jptools\__h2output.txt | Select-String "Test \d+:"
```

### オプションの説明

- `-SkipInstall`: `uv pip install scons pytest` をスキップします（依存関係が既にインストールされている場合に使用）
- `-SkipJtalkSync`: `scons jtalkSync` の実行をスキップします（JTalk資産が既に準備されている場合に使用）
  - **注意**: `-SkipJtalkSync` を指定すると、`libopenjtalk.dll` や `mecab-dict-index.exe` が見つからないエラーが発生する可能性があります
- `-TestFilter`: 実行するテストをフィルタリングします（例: `"JtalkTests"`, `"test_pass2"`）
- `-MaxTests`: `pass2` 関数に渡され、テストケースの実行数を制限します

### 注意事項

- `-SkipInstall` を指定しても、`-SkipJtalkSync` を指定しない限り、`scons jtalkSync` は自動的に実行されます
- Windows fatal exception が発生した場合、`__h2output.txt` にログが書き込まれない可能性があります（ログが書き込まれる前にクラッシュするため）

### トラブルシューティング

- `pytest` モジュールが見つからないエラー: `projectDocs/jp/troubleshooting_runjp_smoke_tests.md` を参照
- CI環境での `__file__` 解決エラー: `projectDocs/jp/troubleshooting_runjp_smoke_tests.md` を参照
- ローカル環境での検証手順: `projectDocs/jp/local_verification_jtalk_runner_fix.md` を参照
