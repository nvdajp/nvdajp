# runJpSmokeTests.ps1 のトラブルシューティング

## テストフレームワークについて

JP smoke tests は Python 標準ライブラリの `unittest` を使用しています。`pytest` などの追加の依存関係は不要です。

### テストの実行方法

```powershell
# すべての準備を自動実行
.\jptools\runJpSmokeTests.ps1

# 準備済みの場合はスキップ
.\jptools\runJpSmokeTests.ps1 -SkipInstall -SkipOverlay

# 特定のテストクラスのみ実行
.\jptools\runJpSmokeTests.ps1 -SkipInstall -SkipOverlay -TestFilter "JtalkTests"
```

### CI での動作

GitHub Actions の CI ワークフロー（`.github/workflows/testAndPublish.yml`）では、以下の手順で実行されています：

```yaml
- name: Run JP smoke tests
  shell: pwsh
  run: jptools/runJpSmokeTests.ps1 -SkipInstall -SkipOverlay
```

`unittest` は Python 標準ライブラリのため、追加のインストールは不要です。

## 問題: CI環境で `jtalkRunner.py` の `__file__` 解決が失敗する

### エラーメッセージ

```
OSError: DLL directory does not exist: D:\a\miscDepsJp\source\synthDrivers\jtalk
FAILED miscDepsJp.jptools.test.JtalkTests.test_jtalk - OSError: DLL directory does not exist: D:\a\miscDepsJp\source\synthDrivers\jtalk
```

### 原因

`jptools/runJpSmokeTests.ps1` で PYTHONPATH を相対パスで設定していたため、CI環境で `jtalkRunner.py` の `__file__` 解決が正しく動作していませんでした。

**技術的な詳細:**


`jptools/runJpSmokeTests.ps1` で PYTHONPATH を絶対パスに変更：

```powershell
$pythonJtalk = Join-Path $repoRoot "miscDepsJp\include\python-jtalk"
$jtalkOverlay = Join-Path $repoRoot "miscDepsJp\source\synthDrivers\jtalk"
$env:PYTHONPATH = "$pythonJtalk;$jtalkOverlay"
```

#### 修正 2: `jtalkRunner.py` の `repo_root` 計算ロジックを改善

`miscDepsJp/include/python-jtalk/jtalkRunner.py` で、PYTHONPATH 環境変数からリポジトリルートを推論する方法を優先：

```python
# Fallback 1: Try to get repo root from PYTHONPATH environment variable
if repo_root is None:
    pythonpath = os.environ.get('PYTHONPATH', '')
    if pythonpath:
        for path in pythonpath.split(os.pathsep):
            if path and os.path.isdir(path):
                # Check if this path contains miscDepsJp/include/python-jtalk
                if path.endswith("miscDepsJp/include/python-jtalk") or path.endswith("miscDepsJp\\include\\python-jtalk"):
                    # Go up two levels: miscDepsJp/include/python-jtalk -> miscDepsJp -> repo root
                    candidate = os.path.dirname(os.path.dirname(path))
                    if os.path.exists(os.path.join(candidate, "miscDepsJp")):
                        repo_root = os.path.dirname(candidate)
                        break

# Fallback 2: Use __file__-based calculation (depends on miscDepsJp folder structure)
if repo_root is None or not os.path.exists(os.path.join(repo_root, "miscDepsJp")):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # script_dir -> miscDepsJp/include/python-jtalk
    # ../.. -> miscDepsJp
    # ../.. -> repo root
    repo_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
```

**注意**: 現在の実装では `miscDepsJp/include/python-jtalk` パスのみを処理しています。`miscDepsJp/source/synthDrivers/jtalk` パスのケースは実装されていません。

### 検証方法

ローカル環境での詳細な検証手順は、`projectDocs/jp/local_verification_jtalk_runner_fix.md` を参照してください。

簡単な検証：

```powershell
# ローカル環境でPYTHONPATHを設定してテスト
$repoRoot = (Resolve-Path .).Path
$pythonJtalk = Join-Path $repoRoot "miscDepsJp\include\python-jtalk"
$jtalkOverlay = Join-Path $repoRoot "miscDepsJp\source\synthDrivers\jtalk"
$env:PYTHONPATH = "$pythonJtalk;$jtalkOverlay"
python -c "import sys; sys.path.insert(0, r'$pythonJtalk'); import jtalkRunner; print('Success')"
```

## 問題: x64 環境での `access violation` エラー

### エラーメッセージ

```
Windows fatal exception: access violation reading 0x00000000BAAF17C0
```

または

```

OverflowError: int too long to convert

```

### 原因

* 64 のみを実行し、x86 の CI に影響を与えない

 checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests` を使用

 jptools/checkJtalkArch.ps1`- x86/x64 の DLL 検証・smoke テストスクリプト
 source/synthDrivers/jtalk/mecab.py` - MeCab DLL の `ctypes` インターフェース

* .github/workflows/checkJtalkArch-x64.yml` - x64 専用の CI workflow
*

 ons launcher`を実行せずに、`runnvda.bat` を使って MeCab のデバッグを行うこともできます。

 e source/synthDrivers/jtalkmecab.py

*

*\scons.bat jtalSync
* 3. NVDA を起動してテト


*## ログの確認

*

*eCab のログは `source/synthDrivers/jtalk/mecab_debug.log` にのみ保存されます（コンソールには出力されません）。これは `mecabRunner.py` と `jtalkRunner.py` の `__print` 関数がログファイルにのみ書き込むように実装されているためです。
* scons jtalkSync` は JTalk DLL と辞書ファイルを準備します（必要に応じて実行）
* overlay 処理は廃止済みのため、`scons miscdepsjp` は不要です

* `jptools/runJpSmokeTests.ps1` - スクリプトの実装（x86 用）
* `pyproject.toml` - 依存関係の定義
* `.github/workflows/testAndPublish.yml` - CI での実行方法（x86）