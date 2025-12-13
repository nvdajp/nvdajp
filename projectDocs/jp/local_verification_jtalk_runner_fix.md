# ローカル検証: jtalkRunner.py の __file__ 解決問題の修正検証

## 概要

このドキュメントは、CI環境で発生していた `jtalkRunner.py` の `__file__` 解決問題の修正をローカル環境で検証する手順を説明します。

## 問題の背景

この検証は、CI環境で発生していた `jtalkRunner.py` の `__file__` 解決問題の修正を確認するためのものです。

**詳細な問題の説明と解決策は `projectDocs/jp/troubleshooting_runjp_smoke_tests.md` の「問題: CI環境で `jtalkRunner.py` の `__file__` 解決が失敗する」セクションを参照してください。**

### 修正内容の要約

1. `jptools/runJpSmokeTests.ps1`: PYTHONPATH を絶対パスに変更
2. `miscDepsJp/include/python-jtalk/jtalkRunner.py`: PYTHONPATH から `repo_root` を推論する方法を優先

## 現在の状況
- ✅ `uv` は利用可能
- ✅ `scons.bat` はリポジトリ内に存在
- ❌ DLL (`libopenjtalk.dll`) が存在しない（初回のみ）

## 準備手順

### 1. 依存関係のインストール

```powershell
# リポジトリルートで実行
uv pip install --system scons pytest
```

または、仮想環境を使用する場合：

```powershell
uv pip install scons pytest
```

### 2. JTalk DLLのビルド

```powershell
# リポジトリルートで実行
.\scons.bat jtalkPrep
```

これにより、`miscDepsJp\source\synthDrivers\jtalk\libopenjtalk.dll` が生成されます。

### 3. miscDeps overlayの準備

```powershell
# リポジトリルートで実行
.\scons.bat miscdepsjp
```

これにより、JTalk関連のファイルがコピーされます。

### 4. 検証: DLLの存在確認

```powershell
Test-Path "miscDepsJp\source\synthDrivers\jtalk\libopenjtalk.dll"
# True が返れば準備完了
```

## 検証実行

準備が完了したら、以下のコマンドで修正を検証します：

### 推奨: JTalkテストのみ実行（修正の検証）

```powershell
.\jptools\runJpSmokeTests.ps1 -SkipInstall -SkipJtalkSync -TestFilter "JtalkTests"
```

### すべての準備を自動実行

```powershell
.\jptools\runJpSmokeTests.ps1
```

### 準備済みの場合はスキップ

```powershell
.\jptools\runJpSmokeTests.ps1 -SkipInstall -SkipJtalkSync
```

## 検証内容

修正の検証では、以下を確認します：

1. **PYTHONPATHが絶対パスで設定されているか**
   ```powershell
   # 実行中に表示される PYTHONPATH を確認
   # 例: PYTHONPATH set to F:\nvda\gh\alphajp-251207\miscDepsJp\include\python-jtalk;F:\nvda\gh\alphajp-251207\miscDepsJp\source\synthDrivers\jtalk
   ```
   - ✅ 絶対パス（`F:\nvda\gh\...` など）が表示されればOK
   - ❌ 相対パス（`miscDepsJp\...` など）が表示されればNG

2. **`jtalkRunner.py`の`repo_root`計算が正しいか**
   - テストが成功すれば、`repo_root`が正しく計算されている
   - 失敗した場合は、エラーメッセージでパスを確認
   - エラー例: `OSError: DLL directory does not exist: D:\a\miscDepsJp\source\synthDrivers\jtalk`（間違ったパス）

3. **DLLが正しいパスから読み込まれているか**
   - テストが成功すれば、DLLが正しく読み込まれている
   - 失敗した場合は、エラーメッセージでパスを確認

## 期待される結果

検証が成功すると、以下のような出力が表示されます：

```
PYTHONPATH set to F:\nvda\gh\alphajp-251207\miscDepsJp\include\python-jtalk;F:\nvda\gh\alphajp-251207\miscDepsJp\source\synthDrivers\jtalk
Running JP braille/JTalk smoke tests (filter: JtalkTests)...
============================= test session starts =============================
...
miscDepsJp\jptools\test.py .                                             [100%]
================= 1 passed, 4 deselected, 6 warnings in 0.67s =================
```

## トラブルシューティング

### DLLのビルドに失敗する場合

- MSVC環境が正しく設定されているか確認
- `projectDocs/dev/createDevEnvironment.md` を参照
- Visual Studio 2022 の Developer Command Prompt が利用可能か確認

### pytest が見つからない場合

仮想環境が作成されている場合は、仮想環境内にインストール：

```powershell
uv pip install pytest
```

### テストが失敗する場合

- `miscDepsJp/jptools/__h2output.txt` を確認
- エラーメッセージでパスを確認
- PYTHONPATH が絶対パスで設定されているか確認

## 関連ドキュメント

- `projectDocs/jp/troubleshooting_runjp_smoke_tests.md` - トラブルシューティング情報
- `jptools/runJpSmokeTests.ps1` - スクリプトの実装
- `miscDepsJp/include/python-jtalk/jtalkRunner.py` - `repo_root` 計算ロジック
