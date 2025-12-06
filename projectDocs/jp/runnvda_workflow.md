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

### 基本的な使い方

```powershell
# すべてのテストを実行
.\jptools\runJpSmokeTests.ps1 -SkipInstall

# 特定のテストのみ実行（例: test_pass2）
.\jptools\runJpSmokeTests.ps1 -SkipInstall -TestFilter "test_pass2"

# テストケース数を制限して実行（例: 10件まで）
.\jptools\runJpSmokeTests.ps1 -SkipInstall -TestFilter "test_pass2" -MaxTests 10
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

### 注意事項

- `-SkipInstall` オプションを指定すると、`scons miscdepsjp` が自動的に実行されます（overlay が実行されます）
- `-SkipOverlay` オプションを指定すると overlay がスキップされますが、`libopenjtalk.dll` が見つからないエラーが発生する可能性があります
- `-MaxTests` オプションは `pass2` 関数に渡され、テストケースの実行数を制限します
- Windows fatal exception が発生した場合、`__h2output.txt` にログが書き込まれない可能性があります（ログが書き込まれる前にクラッシュするため）

### トラブルシューティング

`pytest` モジュールが見つからないエラーが発生した場合、`projectDocs/jp/troubleshooting_runjp_smoke_tests.md` を参照してください。
