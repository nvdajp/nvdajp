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
- `jptools/runJpSmokeTests.ps1` で `$env:PYTHONPATH = "miscDepsJp\include\python-jtalk;miscDepsJp\source\synthDrivers\jtalk"` のように相対パスを設定
- CI環境では、作業ディレクトリがリポジトリルートと異なる場合がある
- `jtalkRunner.py` が `__file__` からリポジトリルートを計算する際、`__file__` が `D:\a\miscDepsJp\include\python-jtalk\jtalkRunner.py` として解決されていた（正しくは `D:\a\nvdajp\nvdajp\miscDepsJp\include\python-jtalk\jtalkRunner.py`）
- その結果、`repo_root` が `D:\a\miscDepsJp` として計算され、正しいパス `D:\a\nvdajp\nvdajp\miscDepsJp\source\synthDrivers\jtalk` を見つけられなかった

### 解決策

#### 修正 1: PYTHONPATH を絶対パスに変更

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

x64 環境で MeCab DLL を呼び出す際、`ctypes` のポインタ型指定が不足していたため、64ビットポインタ（8バイト）が32ビット整数（4バイト）として扱われていました。

**技術的な詳細:**
- x64 ではポインタが 8 バイトだが、`ctypes` のデフォルト型（`c_int` は 4 バイト）では正しく読み取れない
- `mecab_new` の `restype` が明示的に設定されていなかったため、デフォルトの `c_int` が使用されていた
- `mecab_strerror` と `mecab_sparse_tonode` の `argtypes` が明示的に設定されていなかった

### 解決策

`source/synthDrivers/jtalk/mecab.py` で以下の修正を実施：

1. **`mecab_new` の `restype` を `c_void_p` に設定**
   ```python
   libmc.mecab_new.restype = c_void_p  # x64 requires explicit pointer type (8 bytes)
   ```

2. **`mecab_strerror` と `mecab_sparse_tonode` の `argtypes` を明示的に設定**
   ```python
   libmc.mecab_strerror.argtypes = [c_void_p]
   libmc.mecab_sparse_tonode.argtypes = [c_void_p, c_char_p]
   ```

3. **NULL ポインタチェックを追加**
   ```python
   if not mecab:
       logwrite_("mecab_new failed.")
       return
   ```

### x64 環境での smoke テスト実行

x64 環境での smoke テストは、専用のスクリプト `checkJtalkArch.ps1` を使用します：

```powershell
# x64 DLL をビルドして smoke テストを実行
.\jptools\checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests
```

このスクリプトは：
- `.venv-x64` を使用して x86 の `.venv` と分離（競合回避）
- `uv` で Python 3.13 x64 を自動インストール・使用
- x64 DLL が正しくビルド・配置されることを確認
- x64 Python で smoke テストを実行（unittest を使用）

### CI での x64 検証

x64 専用の GitHub Actions workflow（`.github/workflows/checkJtalkArch-x64.yml`）が作成されています：

- `testAndPublish.yml` とは別の独立した workflow
- x64 のみを実行し、x86 の CI に影響を与えない
- `checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests` を使用

### 関連ドキュメント

- `jptools/checkJtalkArch.ps1` - x86/x64 の DLL 検証・smoke テストスクリプト
- `source/synthDrivers/jtalk/mecab.py` - MeCab DLL の `ctypes` インターフェース
- `projectDocs/jp/roadmap.md` - x64 対応の詳細な進捗状況
- `.github/workflows/checkJtalkArch-x64.yml` - x64 専用の CI workflow

## runnvda.bat を使ったテスト

`scons launcher` を実行せずに、`runnvda.bat` を使って MeCab のデバッグを行うこともできます。

### 基本的な使い方

```powershell
# 1. mecab.py を編集（直接 source/synthDrivers/jtalk/mecab.py を編集）
code source/synthDrivers/jtalk/mecab.py

# 2. JTalk DLL と辞書を準備（必要に応じて）
.\scons.bat jtalkSync

# 3. NVDA を起動してテスト
.\runnvda.bat
```

### ログの確認

NVDA のログは通常 `%APPDATA%\nvda\nvda.log` に出力されます。

### 注意事項

- `mecab.py` は `source/synthDrivers/jtalk/mecab.py` に直接配置されているため、直接編集できます
- `scons jtalkSync` は JTalk DLL と辞書ファイルを準備します（必要に応じて実行）
- overlay 処理は廃止済みのため、`scons miscdepsjp` は不要です

## 関連ドキュメント

- `jptools/runJpSmokeTests.ps1` - スクリプトの実装（x86 用）
- `jptools/checkJtalkArch.ps1` - x86/x64 の DLL 検証・smoke テストスクリプト
- `miscDepsJp/include/python-jtalk/jtalkRunner.py` - `repo_root` 計算ロジック
- `projectDocs/jp/local_verification_jtalk_runner_fix.md` - ローカル環境での検証手順
- `projectDocs/jp/roadmap.md` - x64 対応の詳細な進捗状況
- `pyproject.toml` - 依存関係の定義
- `.github/workflows/testAndPublish.yml` - CI での実行方法（x86）
- `.github/workflows/checkJtalkArch-x64.yml` - CI での実行方法（x64）
