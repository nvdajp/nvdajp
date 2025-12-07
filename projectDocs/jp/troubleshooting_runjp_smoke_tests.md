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

### 関連ドキュメント

- `jptools/runJpSmokeTests.ps1` - スクリプトの実装
- `projectDocs/jp/runnvda_workflow.md` - ワークフローの説明
- `pyproject.toml` - 依存関係の定義
- `.github/workflows/testAndPublish.yml` - CI での実行方法
