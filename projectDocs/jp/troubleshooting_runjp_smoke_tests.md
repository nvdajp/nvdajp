# runJpSmokeTests.ps1 のトラブルシューティング

## 問題: `pytest` モジュールが見つからない

### エラーメッセージ

```powershell
.\jptools\runJpSmokeTests.ps1 -SkipInstall
F:\nvda\gh\betajp\.venv\Scripts\python.exe: No module named pytest
```

### 原因

`-SkipInstall` フラグを使用すると、スクリプトは `uv pip install scons pytest` をスキップします。しかし、`pytest` は `pyproject.toml` の依存関係グループに定義されていないため、`uv run python -m pytest` を実行しても `pytest` が見つかりません。

**技術的な詳細:**
- `uv run` は `pyproject.toml` の依存関係を解決してからコマンドを実行します
- `pytest` が `pyproject.toml` の依存関係グループ（`unit-tests` など）に定義されていない場合、`uv run` は `pytest` を利用できません
- `uv pip install` は現在の仮想環境（`.venv`）に直接パッケージをインストールしますが、`-SkipInstall` を使用するとこのステップがスキップされます

### 解決策

#### 方法 1: `-SkipInstall` フラグを外す（推奨）

依存関係をインストールしてからテストを実行します：

```powershell
.\jptools\runJpSmokeTests.ps1
```

これにより、スクリプトは自動的に `uv pip install scons pytest` を実行します。

#### 方法 2: 手動で `pytest` をインストール

`-SkipInstall` を使いたい場合は、事前に手動でインストールします：

```powershell
uv pip install pytest
.\jptools\runJpSmokeTests.ps1 -SkipInstall
```

#### 方法 3: `pyproject.toml` に `pytest` を追加（長期的な解決策）

`pytest` を `pyproject.toml` の `unit-tests` 依存関係グループに追加することで、`uv sync --group unit-tests` や `uv run --group unit-tests` で `pytest` が利用可能になります。

```toml
[dependency-groups]
unit-tests = [
	# Creating XML unit test reports
	"unittest-xml-reporting==3.2.0",
	# Feed parameters to tests neatly
	"parameterized==0.9.0",
	# Testing framework for JP smoke tests
	"pytest",
]
```

その後、依存関係を同期します：

```powershell
uv sync --group unit-tests
.\jptools\runJpSmokeTests.ps1 -SkipInstall
```

### CI での動作

GitHub Actions の CI ワークフロー（`.github/workflows/testAndPublish.yml`）では、以下の手順で実行されています：

```yaml
- name: Install tools for JP overlay
  shell: pwsh
  run: uv pip install scons pytest
- name: Run JP braille/JTalk smoke tests
  shell: pwsh
  run: uv run python -m pytest test.py -k "JpBrailleTests or JtalkTests"
```

CI では `uv pip install` で直接インストールしてから `uv run` で実行しているため、問題は発生しません。

### 推奨される運用方法

1. **初回実行時**: `-SkipInstall` を付けずに実行して、依存関係をインストール
2. **2回目以降**: 依存関係が既にインストールされていることを確認した上で `-SkipInstall` を使用
3. **依存関係が不明な場合**: `-SkipInstall` を外して実行（依存関係のインストールは比較的高速）

## 問題: CI環境で `jtalkRunner.py` の `__file__` 解決が失敗する

### エラーメッセージ

```
OSError: DLL directory does not exist: D:\a\miscDepsJp\source\synthDrivers\jtalk
FAILED miscDepsJp/jptools/test.py::JtalkTests::test_jtalk - OSError: DLL directory does not exist: D:\a\miscDepsJp\source\synthDrivers\jtalk
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

### 関連ドキュメント

- `jptools/runJpSmokeTests.ps1` - スクリプトの実装
- `miscDepsJp/include/python-jtalk/jtalkRunner.py` - `repo_root` 計算ロジック
- `projectDocs/jp/runnvda_workflow.md` - `runJpSmokeTests.ps1` の基本的な使い方
- `projectDocs/jp/local_verification_jtalk_runner_fix.md` - ローカル環境での検証手順
- `pyproject.toml` - 依存関係の定義
- `.github/workflows/testAndPublish.yml` - CI での実行方法
