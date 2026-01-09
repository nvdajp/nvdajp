# ビルドアーキテクチャ環境変数の方針

## 概要

日本語版NVDAのビルドシステムでは、`BUILD_ARCH`と`TARGET_ARCH`という2つの環境変数を使用して、ビルドツールのアーキテクチャとビルドされるバイナリのアーキテクチャを制御します。

**重要な注意**: これらの環境変数は**日本語版独自の追加**です。本家（nvaccess/beta）ブランチでは使用されていません。

- **`BUILD_ARCH`**: 完全に日本語版独自のOS環境変数
- **`TARGET_ARCH`**: SCons環境変数としてのみ使用（本家から継承）

## 環境変数の定義

### `BUILD_ARCH`（OS環境変数）

- **用途**: 主にsmoke testの環境（Pythonアーキテクチャ）を切り替えるためのOS環境変数。また、MSVC環境の設定にも使用される。
- **使用箇所**:
  - `jptools/certBuild2023.cmd`: `vcsetup.cmd`に渡してMSVC環境を設定
  - `jptools/runJpSmokeTests.ps1`: Pythonアーキテクチャの選択に使用
  - `jptools/checkJtalkArch.ps1`: ビルドアーキテクチャの指定に使用
  - `jptools/scons_jp.py`: SCons環境変数`TARGET_ARCH`の設定に使用
- **値**: `x64`（x86 はサポートされていません）
- **デフォルト**: `x64`

### `TARGET_ARCH`（SCons環境変数）

- **用途**: SConsでビルドされるバイナリ（DLL、EXEなど）のターゲットアーキテクチャを指定
- **性質**: SCons環境変数としてのみ使用。OS環境変数として設定することはしない。
- **設定方法**: `jptools/scons_jp.py`の`register_jp_builders`関数で、`BUILD_ARCH`環境変数の値に基づいて自動設定される。
- **使用箇所**:
  - `jptools/scons_jp.py`: `BUILD_ARCH`環境変数を読み取り、SCons環境変数`TARGET_ARCH`に設定
  - `nvdaHelper/archBuild_sconscript`: NVDAHelperのビルドアーキテクチャを決定（SCons環境変数から読み取り、本家から）
  - `sconstruct`: 環境変数`env32`、`env64`、`envArm64`の選択に使用（本家から）
- **値**: `x64`（`x86_64`）、`arm64`など（x86 はサポートされていません）
- **デフォルト**: `x64`

## 重要な原則

### 原則1: `scons.bat`は常にx64 Python 3.13で実行される

- `scons.bat`は`ensureuv.ps1`経由で実行され、常にx64 Python 3.13を使用します
- これは`.venv`がx64 Python 3.13で作成されるためです
- **x86 ビルドはサポートされていません**

### 原則2: `BUILD_ARCH`でビルドされるDLLのアーキテクチャが決まる

- `scons.bat jtalkSync`を実行する際、`BUILD_ARCH`環境変数が設定されていると、その値に応じてDLLがビルドされます（x64 のみサポート）
- `jptools/scons_jp.py`は`BUILD_ARCH`環境変数を読み取り、SCons環境変数`TARGET_ARCH`に設定します
- `TARGET_ARCH`はSCons環境変数としてのみ使用され、OS環境変数として設定することはありません
- **x86 ビルドはサポートされていません**

### 原則3: `TARGET_ARCH`はSCons環境変数としてのみ使用

- `TARGET_ARCH`はSCons環境変数としてのみ使用します
- OS環境変数として`TARGET_ARCH`を設定することはしません
- 日本語版独自の用途には`BUILD_ARCH`を使用します

## 実装方針

### `certBuild2023.cmd`での処理

```cmd
rem Build architecture (default to x86)
rem BUILD_ARCH is JP-specific environment variable for smoke test environment switching and MSVC setup
rem TARGET_ARCH is SCons environment variable and should not be set as OS environment variable
if not defined BUILD_ARCH set BUILD_ARCH=x86
echo BUILD_ARCH is %BUILD_ARCH%
```

- `BUILD_ARCH`のみを設定（デフォルト`x86`）
- `TARGET_ARCH`は設定しません（SCons環境変数としてのみ使用）

### `jptools/scons_jp.py`での処理

```python
# Use BUILD_ARCH (JP-specific) to set TARGET_ARCH (SCons environment variable).
# BUILD_ARCH is an OS environment variable for JP-specific purposes (mainly smoke test environment switching).
# TARGET_ARCH is a SCons environment variable and should only be set via SCons, not OS environment.
# Note: x86 builds are no longer supported
build_arch = str(os.environ.get("BUILD_ARCH", "")).lower()
if build_arch in ("x64", "x86_64"):
    env["TARGET_ARCH"] = "x64"
elif build_arch == "x86":
    env["TARGET_ARCH"] = "x86"  # Deprecated: x86 builds are no longer supported
else:
    # Fallback to existing SCons TARGET_ARCH (defaults to x64)
    env["TARGET_ARCH"] = str(env.get("TARGET_ARCH", "x64")).lower()
```

- `BUILD_ARCH`環境変数を読み取り、SCons環境変数`TARGET_ARCH`に設定
- `BUILD_ARCH`が設定されていない場合、SCons環境の`TARGET_ARCH`（デフォルト`x64`）を使用
- **x86 ビルドはサポートされていません**

### `jptools/runJpSmokeTests.ps1`での処理

```powershell
# Use x64 Python 3.13 and .venv for smoke tests
# Note: x86 builds are no longer supported
# Ensure x64 Python 3.13 is available
& uv python install 3.13
# Use .venv (x64 Python 3.13)
$venvPath = Join-Path $repoRoot ".venv"
$pythonExe = Join-Path $venvPath "Scripts\python.exe"
```

- x64 Python 3.13と`.venv`を使用してsmoke testを実行
- **x86 ビルドはサポートされていません**

## 各シナリオでの動作

### シナリオ1: `scons launcher`の実行

#### シナリオ1-1: `certBuild2023.cmd`から呼ばれる場合

```cmd
set BUILD_ARCH=x64
call jptools\certBuild2023.cmd
```

動作:

1. `certBuild2023.cmd`内で`BUILD_ARCH`が設定される（デフォルト`x64`）
2. `vcsetup.cmd %BUILD_ARCH%`でMSVC環境を設定
3. `scons.bat launcher`が実行される
4. `jptools/scons_jp.py`の`register_jp_builders`が呼ばれ、`BUILD_ARCH`環境変数を読み取ってSCons環境変数`TARGET_ARCH`に設定
5. 依存関係として`jtalkSync`が実行される
   - `jtalkSync`はSCons環境変数`TARGET_ARCH`を読み取ってDLLをビルド
   - `scons.bat`は常にx64 Python 3.13で実行される（`.venv`はx64 Python 3.13を使用）

環境変数の値:

- `BUILD_ARCH`: `x64`（OS環境変数、設定された値）
- `TARGET_ARCH`: SCons環境変数として`x64`（`jptools/scons_jp.py`で設定）
- Python: x64 Python 3.13（`.venv`）

#### シナリオ1-2: 直接実行する場合

```cmd
call scons.bat launcher
```

動作:

1. `BUILD_ARCH`が設定されていない場合、デフォルト`x64`が使われる
2. `jptools/scons_jp.py`の`register_jp_builders`が呼ばれ、`BUILD_ARCH`が未設定の場合はSCons環境変数`TARGET_ARCH`（デフォルト`x64`）を使用
3. `jtalkSync`はSCons環境変数`TARGET_ARCH`を読み取ってDLLをビルド

環境変数の値:

- `BUILD_ARCH`: 未設定（デフォルト`x64`として扱われる）
- `TARGET_ARCH`: SCons環境変数としてデフォルト`x64`
- Python: x64 Python 3.13（`.venv`）

**注意**: x86 ビルドはサポートされていません。

### シナリオ2: `jp smoke test x64`の実行

#### シナリオ2-1: `certBuild2023.cmd`から呼ばれる場合

```cmd
set BUILD_ARCH=x64
call jptools\certBuild2023.cmd
```

動作:

1. `certBuild2023.cmd`内で`BUILD_ARCH=x64`が設定される
2. `runJpSmokeTests.ps1`が実行される
3. `runJpSmokeTests.ps1`は`BUILD_ARCH`を読み取る
4. x64なので、x64 Python 3.13と`.venv`を使用してsmoke testを実行

環境変数の値:

- `BUILD_ARCH`: `x64`（OS環境変数）
- `TARGET_ARCH`: SCons環境変数として`x64`（`jptools/scons_jp.py`で設定）
- Python: x64 Python 3.13（`.venv`）

#### シナリオ2-2: `checkJtalkArch.ps1`から呼ばれる場合（CIや手動実行）

```powershell
.\jptools\checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests
```

動作:

1. `checkJtalkArch.ps1`内で`BUILD_ARCH=x64`が設定される
2. `scons.bat jtalkSync`が実行される（x64 DLLをビルド）
   - `jptools/scons_jp.py`の`register_jp_builders`が`BUILD_ARCH`を読み取り、SCons環境変数`TARGET_ARCH`に設定
3. `runJpSmokeTests.ps1`が実行される
4. `runJpSmokeTests.ps1`は`BUILD_ARCH`を読み取る
5. x64なので、x64 Python 3.13と`.venv`を使用してsmoke testを実行

環境変数の値:

- `BUILD_ARCH`: `x64`（OS環境変数、`checkJtalkArch.ps1`で設定）
- `TARGET_ARCH`: SCons環境変数として`x64`（`jptools/scons_jp.py`で設定）
- Python: x64 Python 3.13（`.venv`）

#### シナリオ2-3: 直接実行する場合

```powershell
$env:BUILD_ARCH = "x64"
.\jptools\runJpSmokeTests.ps1
```

動作:

1. `BUILD_ARCH=x64`がOS環境変数として設定される
2. `runJpSmokeTests.ps1`は`BUILD_ARCH`を読み取る
3. x64なので、x64 Python 3.13と`.venv`を使用してsmoke testを実行

環境変数の値:

- `BUILD_ARCH`: `x64`（OS環境変数、手動設定）
- `TARGET_ARCH`: SCons環境変数として`x64`（`jptools/scons_jp.py`で設定）
- Python: x64 Python 3.13（`.venv`）

### 手動で`jtalkSync`を実行する場合

```cmd
set BUILD_ARCH=x64
call scons.bat jtalkSync
```

動作:

1. `BUILD_ARCH`環境変数を設定してから`scons.bat jtalkSync`を実行
2. `jptools/scons_jp.py`の`register_jp_builders`が`BUILD_ARCH`を読み取り、SCons環境変数`TARGET_ARCH`に設定
3. `jtalkSync`はSCons環境変数`TARGET_ARCH`を読み取ってDLLをビルド

環境変数の値:

- `BUILD_ARCH`: `x64`（OS環境変数、手動設定）
- `TARGET_ARCH`: SCons環境変数として`x64`（`jptools/scons_jp.py`で設定）
- Python: x64 Python 3.13（`.venv`）

### `jtalkSync`のクリーン処理（`scons -c jtalkSync`）

`jtalkSync`のクリーン処理は、x86/x64切り替え時に古いファイルが残らないよう、以下のファイルを確実に削除します（2025-12-30 改善）:

- **オブジェクトファイル**: `miscDepsJp/include/python-jtalk/libopenjtalk/mecab/src/*.obj`（`glob`で動的検索）
- **ライブラリファイル**: `miscDepsJp/include/python-jtalk/libopenjtalk/mecab/src/*.lib`（`glob`で動的検索）
- **実行ファイル**: `miscDepsJp/include/python-jtalk/libopenjtalk/mecab/src/*.exe`（`glob`で動的検索）
- **Stampファイル**:
  - `miscDepsJp/_state/prep/jtalkSync.x64.stamp`（x64 のみ）
  - `miscDepsJp/_state/prep/jtalkPrep.x64.stamp`（x64 のみ）

**重要**: クリーン処理はアーキテクチャ指定不要です。`scons -c jtalkSync`を実行すると、x64のstampファイルと、`mecab/src`ディレクトリ内のすべてのビルド成果物（`.obj`、`.lib`、`.exe`）が削除されます。**注意**: x86 ビルドはサポートされていません。

## まとめ表

| シナリオ | `BUILD_ARCH` | `TARGET_ARCH` | Python | venv | DLLアーキテクチャ |
| -------- | ------------ | ------------- | ------ | ---- | ---------------- |
| `scons launcher`（`certBuild2023.cmd`経由、x86） | `x86`（OS環境変数） | `x86`（SCons環境変数） | x86 3.13 | `.venv` | x86 |
| `scons launcher`（`certBuild2023.cmd`経由、x64） | `x64`（OS環境変数） | `x64`（SCons環境変数） | x86 3.13 | `.venv` | x64 |
| `scons launcher`（直接実行） | 未設定（デフォルト`x86`） | `x86`（SCons環境変数、デフォルト） | x86 3.13 | `.venv` | x86 |
| `jp smoke test x86`（`certBuild2023.cmd`経由） | `x86`（OS環境変数） | `x86`（SCons環境変数） | x86 3.13 | `.venv` | x86 |
| `jp smoke test x86`（直接実行） | 未設定（デフォルト`x86`） | `x86`（SCons環境変数、デフォルト） | x86 3.13 | `.venv` | x86 |
| `jp smoke test x64`（`certBuild2023.cmd`経由） | `x64`（OS環境変数） | `x64`（SCons環境変数） | x64 3.13 | `.venv` | x64 |
| `jp smoke test x64`（`checkJtalkArch.ps1`経由） | `x64`（OS環境変数） | `x64`（SCons環境変数） | x64 3.13 | `.venv` | x64 |
| `jp smoke test x64`（直接実行） | `x64`（OS環境変数、手動設定） | `x64`（SCons環境変数） | x64 3.13 | `.venv` | x64 |
| `scons jtalkSync`（手動実行、x64） | `x64`（OS環境変数、手動設定） | `x64`（SCons環境変数） | x86 3.13 | `.venv` | x64 |

## 禁止事項

### ❌ やってはいけないこと

1. **`TARGET_ARCH`をOS環境変数として設定する**
   - `TARGET_ARCH`はSCons環境変数としてのみ使用すべきです
   - OS環境変数として設定することは混乱を招くため、避けるべきです
   - 代わりに`BUILD_ARCH`を使用してください

2. **`scons.bat`をx86 Pythonで実行しようとする**
   - `scons.bat`は常にx64 Python 3.13で実行されます（`.venv`はx64 Python 3.13を使用）
   - x86 ビルドはサポートされていません

## 関連ドキュメント

- `projectDocs/jp/troubleshooting_runjp_smoke_tests.md`: smoke test実行時のトラブルシューティング
- 注: `certBuild2023.cmd`の詳細な評価は`certBuild2025.ps1`の説明に統合されています（`certBuild2025.ps1`は`certBuild2023.cmd`をラップしています）
- `projectDocs/jp/roadmap.md`: 長期的な開発計画

## 変更履歴

- 2025-12-30: 初版作成。`BUILD_ARCH`と`TARGET_ARCH`の関係と使用方法を明記
- 2025-12-30: リファクタリング完了。`TARGET_ARCH`をOS環境変数として使用することを廃止し、SCons環境変数としてのみ使用するように変更。`BUILD_ARCH`をOS環境変数として使用し、`jptools/scons_jp.py`でSCons環境変数`TARGET_ARCH`に設定する方式に統一。
- 2025-12-30: `jtalkSync`のクリーン処理を改善。`scons -c jtalkSync`で`mecab/src`ディレクトリ内の`*.obj`、`*.lib`、`*.exe`ファイルと、x64のstampファイルが確実に削除されるよう改善。
- 2026-01-02: x86 ビルドサポートを削除。`.venv-x64` を `.venv` に統一。x64 のみをサポート。
