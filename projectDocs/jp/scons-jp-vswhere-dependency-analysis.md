# scons_jp.py の vswhere 依存に関する分析

## 質問

`scons_jp.py`も`vswhere`に依存すべきか？

## 現状の分析

### 1. `scons_jp.py`の現在の実装

#### Visual Studio検出の実装

```python
def _find_vcvarsall() -> str | None:
    """Find vcvarsall.bat in common Visual Studio install locations.
    Returns absolute path if found, None otherwise.
    Currently supports Visual Studio 2022 only.
    Search order: BuildTools, Community, Professional, Enterprise.

    Note: This function delegates to jptools.vs_utils.find_vcvarsall() for shared logic.
    """
    return find_vcvarsall()
```

**アプローチ**:

1. **`jtalkPrep`**: `libopenjtalk.dll`のビルド時に`nmake`が必要な場合
2. **`jtalkSync`**: `libmecab.dll`のビルド時に`nmake`が必要な場合
3. **`jtalkSync`**: 辞書のビルド時に`nmake`が必要な場合

**使用パターン**:
cmd_script = f'call "{vcvarsall}" {nmake_machine} && nmake /f all.mak MACHINE={nmake_machine}'








```

### 2. 他のスクリプトとの比較

#### `nonCertBuild.py`（Pythonスクリプト）

```python
def _ensure_nmake_env() -> None:
    """Order of attempts:
*   1) If 'cl' seems callable, do nothing.
*   2) Use vswhere to locate Visual Studio and call vcvars32/VsDevCmd, import env.
*   3) Fallback to JP's jptools/vcsetup.cmd and import env.
*   """
*``
*
**アプローチ**:
* **ステップ2**: `vswhere`を使用（本家のアプローチ）
* **ステップ3**: フォールバックとして`vcsetup.cmd`を使用
*
*### `vcsetup.cmd`（バッチスクリプト）
*
**アプローチ**:
* `vs_utils.py`を使用（直接パス検索、`vswhere`を使用しない）
*
*### `runJpSmokeTests.ps1`（PowerShellスクリプト）
*
**アプローチ**:
* 直接パス検索（`vswhere`を使用しない）
*
*## 3. 一貫性の問題
*
**現状**:
* `nonCertBuild.py`: `vswhere`を使用（本家のアプローチ）
* `scons_jp.py`: `vs_utils.py`を使用（直接パス検索、`vswhere`を使用しない）
* `vcsetup.cmd`: `vs_utils.py`を使用（直接パス検索、`vswhere`を使用しない）
* `runJpSmokeTests.ps1`: 直接パス検索（`vswhere`を使用しない）
*
**問題点**:
* 異なる検出方法を使用している
* `nonCertBuild.py`だけが`vswhere`を使用している
* 他のスクリプトは直接パス検索を使用している
*
*# 検討事項
*
*## 1. `nonCertBuild.py`との一貫性
*
**現状**:
* `nonCertBuild.py`: `vswhere`を使用
* `scons_jp.py`: 直接パス検索を使用
*
**一貫性の観点**:
* `scons_jp.py`も`vswhere`を使用することで、`nonCertBuild.py`との一貫性が向上する
* 同じ検出ロジックを使用することで、保守性が向上する
*
*## 2. 本家のアプローチとの整合性
*
**本家のアプローチ**:
* `vswhere`を使用してVisual Studioを検出（推測）
*
**日本語版のアプローチ**:
* `nonCertBuild.py`: `vswhere`を使用（本家と同じ）
* `scons_jp.py`: 直接パス検索（本家と異なる）
*
**整合性の観点**:
* `scons_jp.py`も`vswhere`を使用することで、本家のアプローチに近づく
*
*## 3. `vs_utils.py`の役割
*
**現状**:
* `vs_utils.py`は直接パス検索のみを実装
* `scons_jp.py`と`vcsetup.cmd`の両方で使用されている
*
**改善案**:
* `vs_utils.py`に`vswhere`サポートを追加
* `find_vcvarsall()`と`find_vcvars()`を修正し、`vswhere`を優先、直接パス検索をフォールバックとする
* これにより、`scons_jp.py`と`vcsetup.cmd`の両方が自動的に`vswhere`を使用するようになる
*
*## 4. 実装の複雑さ
*
**現状**:
* `scons_jp.py`は`vs_utils.find_vcvarsall()`を呼び出すだけ（シンプル）
*
**`vswhere`を追加した場合**:
* `vs_utils.py`の実装が複雑になる

* ただし、`scons_jp.py`のコードは変更不要（`vs_utils.py`の内部実装の変更のみ）



## 推奨アプローチ
*
*
*
*## 案1: `vs_utils.py`に`vswhere`サポートを追加（推奨）
*
*
*
**実装**:
*
*. `vs_utils.py`に`find_vcvarsall_with_vswhere()`関数を追加
*. `find_vcvarsall()`関数を修正し、`vswhere`を優先、直接パス検索をフォールバックとする
*. `find_vcvars()`関数も同様に修正
*
**利点**:
* `scons_jp.py`のコード変更が不要（`vs_utils.py`の内部実装の変更のみ）

* `vcsetup.cmd`も自動的に`vswhere`を使用するようになる
* すべてのスクリプトが同じ検出ロジックを使用（一貫性）

* `nonCertBuild.py`との一貫性が向上する
* 本家のアプローチに近づく

*
**欠点**:
*
* `vs_utils.py`の実装が複雑になる
* `vswhere`の呼び出しと結果の解析が必要
*
*
**評価**: ⭐⭐⭐⭐⭐（推奨）
*
*
*## 案2: `scons_jp.py`に直接`vswhere`サポートを追加
*
*
**実装**:
*
*. `scons_jp.py`の`_find_vcvarsall()`関数を修正し、`vswhere`を優先、`vs_utils.find_vcvarsall()`をフォールバックとする
*
**利点**:
* `scons_jp.py`だけが`vswhere`を使用する
* `vs_utils.py`の変更が不要
*
**欠点**:
* `vcsetup.cmd`は依然として直接パス検索を使用（一貫性が低い）
* コードの重複（`nonCertBuild.py`と`scons_jp.py`で`vswhere`ロジックが重複）
*
**評価**: ⭐⭐⭐（中程度）
*
*## 案3: 現状維持（直接パス検索のみ）
*
**実装**:
* 現在の実装を維持
*
**利点**:
* 実装がシンプル
* 追加の依存関係が不要
*
**欠点**:
* `nonCertBuild.py`との一貫性が低い
* 本家のアプローチと異なる
* 柔軟性が低い（Visual Studio 2022のみサポート）

**評価**: ⭐⭐⭐（中程度）

## 推奨される実装（案1）

### `vs_utils.py`の拡張

```python
import subprocess
from pathlib import Path
from typing import Literal

def find_vcvarsall_with_vswhere() -> str | None:
    """Find vcvarsall.bat using vswhere (preferred method).

    Returns:
        Absolute path to vcvarsall.bat if found, None otherwise.
    """
    vswhere = Path(r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe")
    if not vswhere.exists():
        return None

    pattern = r"VC\Auxiliary\Build\vcvarsall.bat"

    try:
        result = subprocess.check_output(
            [
                str(vswhere),
                "-latest",
                "-products", "*",
                "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
                "-find", pattern,
                "-format", "value",
            ],
            text=True,
            errors="ignore",
        ).strip()

        if result and Path(result).exists():
            return result
    except Exception:
        pass

    return None


def find_vcvarsall() -> str | None:
    """Find vcvarsall.bat in Visual Studio install locations.

    First tries vswhere (preferred), then falls back to direct path search.

    Returns:
        Absolute path to vcvarsall.bat if found, None otherwise.

    Search order: BuildTools, Community, Professional, Enterprise.
    """
    # Try vswhere first (preferred method, consistent with nonCertBuild.py)
    result = find_vcvarsall_with_vswhere()
    if result:
        return result

    # Fallback to direct path search (for environments without vswhere)
    for edition in VS2022_EDITIONS:
        path = VS2022_BASE_PATH / edition / "VC" / "Auxiliary" / "Build" / "vcvarsall.bat"
        if path.exists():
            return str(path)
    return None


def find_vcvars_with_vswhere(arch: Literal["x86", "x64"] = "x86") -> str | None:
    """Find vcvars script using vswhere (preferred method).

    Args:
        arch: Target architecture ("x86" or "x64"). Defaults to "x86".

    Returns:
        Absolute path to vcvars script if found, None otherwise.
    """
    vswhere = Path(r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe")
    if not vswhere.exists():
        return None

    script_name = "vcvars32.bat" if arch == "x86" else "vcvars64.bat"
    pattern = rf"VC\Auxiliary\Build\{script_name}"

    try:
        result = subprocess.check_output(
            [
                str(vswhere),
                "-latest",
                "-products", "*",
                "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
                "-find", pattern,
                "-format", "value",
            ],
            text=True,
            errors="ignore",
        ).strip()

        if result and Path(result).exists():
            return result
    except Exception:
        pass

    return None


def find_vcvars(arch: Literal["x86", "x64"] = "x86") -> str | None:
    """Find vcvars32.bat or vcvars64.bat in Visual Studio install locations.

    First tries vswhere (preferred), then falls back to direct path search.

    Args:
        arch: Target architecture ("x86" or "x64"). Defaults to "x86".

    Returns:
        Absolute path to vcvars script if found, None otherwise.

    Search order: BuildTools, Community, Professional, Enterprise.
    """
    # Try vswhere first (preferred method, consistent with nonCertBuild.py)
    result = find_vcvars_with_vswhere(arch)
    if result:

        return result

    # Fallback to direct path search (for environments without vswhere)

    script_name = "vcvars32.bat" if arch == "x86" else "vcvars64.bat"

    for edition in VS2022_EDITIONS:

        path = VS2022_BASE_PATH / edition / "VC" / "Auxiliary" / "Build" / script_name
        if path.exists():
            return str(path)


    return None
```

### `scons_jp.py`の変更

*

**変更不要**: `scons_jp.py`は`vs_utils.find_vcvarsall()`を呼び出すだけなので、`vs_utils.py`の内部実装の変更により自動的に`vswhere`を使用するようになる。
*
*

*

*. **本家のアプローチに近い**: Microsoftが推奨する標準的な方法

5. **柔軟性と将来の拡張性**: 様々なVisual Studioエディションに対応、将来のバージョンにも対応可能
*. **フォールバック**: `vswhere`が存在しない環境でも動作（直接パス検索にフォールバック）

*

*# 実装状況（2025年12月30日）

* **実装完了**
*

**実装内容**:
*. ✅ Visual Studio 2022を優先的に使用（`-version [17.0,18.0)`）

* ✅ x86 JP smoke tests成功

* `e625d3c8b`: "Add vswhere support to vs_utils.py for stable Visual Studio detection"
