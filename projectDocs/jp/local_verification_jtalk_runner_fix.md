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
uv pip install --system scons
```

または、仮想環境を使用する場合：

```powershell
uv pip install scons
```

**注**: `unittest` は Python 標準ライブラリのため、追加のインストールは不要です。

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
.\jptools\runJpSmokeTests.ps1 -SkipInstall -SkipOverlay -TestFilter "JtalkTests"
```

### すべての準備を自動実行

```powershell
.\jptools\runJpSmokeTests.ps1
```

### 準備済みの場合はスキップ

```powershell
.\jptools\runJpSmokeTests.ps1 -SkipInstall -SkipOverlay
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
test_jtalk (miscDepsJp.jptools.test.JtalkTests) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.67s

OK
```

## トラブルシューティング

### DLLのビルドに失敗する場合

- MSVC環境が正しく設定されているか確認
- `projectDocs/dev/createDevEnvironment.md` を参照
- Visual Studio 2022 の Developer Command Prompt が利用可能か確認

### unittest について

`unittest` は Python 標準ライブラリのため、追加のインストールは不要です。Python 3.11 以降で利用可能です。

### テストが失敗する場合

- `miscDepsJp/jptools/__h2output.txt` を確認
- エラーメッセージでパスを確認
- PYTHONPATH が絶対パスで設定されているか確認

## x64 環境での検証

x64 環境での smoke テストは、`checkJtalkArch.ps1` を使用します：

```powershell
# x64 DLL をビルドして smoke テストを実行
.\jptools\checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests
```

このスクリプトは：
- `.venv-x64` を使用して x86 の `.venv` と分離（競合回避）
- `uv` で Python 3.13 x64 を自動インストール・使用
- x64 DLL が正しくビルド・配置されることを確認（dumpbin で検証）
- x64 Python で smoke テストを実行

**注意**: `scons.bat`は常にx86 Python 3.13で実行されますが、`TARGET_ARCH=x64`によりx64 DLLがビルドされます。

### x64 環境での準備手順

1. **x64 DLL のビルド**
   ```powershell
   # TARGET_ARCH=x64 で x64 DLL をビルド
   $env:TARGET_ARCH = 'x64'
   .\scons.bat jtalkSync
   ```

2. **x64 DLL の検証**
   ```powershell
   # dumpbin で x64 DLL のアーキテクチャを確認
   .\jptools\checkJtalkArch.ps1 -Architecture x64
   ```

3. **x64 smoke テストの実行**
   ```powershell
   # x64 DLL をビルドして smoke テストを実行
   .\jptools\checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests
   ```

### x64 環境での注意点

- x64 環境では、x64 用の DLL（`libopenjtalk.dll`、`libmecab.dll`）が必要
- x64 Python で x64 DLL を読み込む必要がある（x86 Python では `OSError: [WinError 193]` が発生）
- `.venv-x64` を使用して x86 の `.venv` と分離することで、リソース競合を回避

### x64 環境でのトラブルシューティング

x64 環境での問題については、`projectDocs/jp/troubleshooting_runjp_smoke_tests.md` の「問題: x64 環境での `access violation` エラー」セクションを参照してください。

## 関連ドキュメント

- `projectDocs/jp/troubleshooting_runjp_smoke_tests.md` - トラブルシューティング情報（x86/x64）
- `jptools/runJpSmokeTests.ps1` - スクリプトの実装（x86 用）
- `jptools/checkJtalkArch.ps1` - x86/x64 の DLL 検証・smoke テストスクリプト
- `miscDepsJp/include/python-jtalk/jtalkRunner.py` - `repo_root` 計算ロジック
- `projectDocs/jp/roadmap.md` - x64 対応の詳細な進捗状況
