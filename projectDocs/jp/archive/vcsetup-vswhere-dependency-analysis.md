# vcsetup の vswhere 依存に関する分析

## 質問

`vcsetup.cmd`（または`vcsetup.ps1`）も`vswhere`に依存すべきか？

## 現状の分析

### 1. 現在の実装

#### `nonCertBuild.py`（Pythonスクリプト）

```python
def _ensure_nmake_env() -> None:
    """Order of attempts:
    1) If 'cl' seems callable, do nothing.
    2) Use vswhere to locate Visual Studio and call vcvars32/VsDevCmd, import env.
    3) Fallback to JP's jptools/vcsetup.cmd and import env.
    """
```

**アプローチ**:
- **ステップ2**: `vswhere.exe`を使用してVisual Studioを検出（本家のアプローチ）
- **ステップ3**: フォールバックとして`vcsetup.cmd`を使用

#### `vcsetup.cmd`（バッチスクリプト）

```batch
rem Use shared Python module for VS path detection (jptools/vs_utils.py)
rem This ensures consistency with scons_jp.py and runJpSmokeTests.ps1
set "FOUND="
for /f "delims=" %%P in ('python "%~dp0find_vcvars.py" %ARCH% 2^>nul') do (
  set "FOUND=%%P"
)

if not defined FOUND (
  rem Fallback to direct search if Python call fails
  ...
)
```

**アプローチ**:
- `vs_utils.py`（`find_vcvars.py`経由）を使用
- `vs_utils.py`は**直接パス検索**（`vswhere`を使用しない）
- フォールバックとして直接パス検索

#### `vs_utils.py`（Pythonモジュール）

```python
def find_vcvars(arch: Literal["x86", "x64"] = "x86") -> str | None:
    """Find vcvars32.bat or vcvars64.bat in Visual Studio 2022 install locations.
    
    Search order: BuildTools, Community, Professional, Enterprise.
    """
    script_name = "vcvars32.bat" if arch == "x86" else "vcvars64.bat"
    
    for edition in VS2022_EDITIONS:
        path = VS2022_BASE_PATH / edition / "VC" / "Auxiliary" / "Build" / script_name
        if path.exists():
            return str(path)
    return None
```

**アプローチ**:
- **直接パス検索**: `C:\Program Files\Microsoft Visual Studio\2022\{edition}\VC\Auxiliary\Build\vcvars32.bat`
- `vswhere`を使用しない

### 2. `vswhere`の可用性

**`vswhere.exe`の場所**:
- `C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe`
- Visual Studioインストーラーに含まれる

**可用性**:
- ✅ Visual Studioがインストールされている環境では利用可能
- ❌ Visual Studioがインストールされていない環境では存在しない可能性がある
- ✅ CI環境（GitHub Actions）では通常利用可能（Visual Studioがインストールされているため）

## 検討事項

### 1. `nonCertBuild.py`との一貫性

**現状**:
- `nonCertBuild.py`: `vswhere`を使用（本家のアプローチ）
- `vcsetup.cmd`: `vs_utils.py`を使用（直接パス検索）

**問題点**:
- 異なる検出方法を使用している
- `nonCertBuild.py`は`vswhere`を優先し、`vcsetup.cmd`をフォールバックとして使用
- `vcsetup.cmd`は`vswhere`を使用しない

**一貫性の観点**:
- `vcsetup.cmd`も`vswhere`を使用することで、`nonCertBuild.py`との一貫性が向上する
- 同じ検出ロジックを使用することで、保守性が向上する

### 2. 本家のアプローチとの整合性

**本家のアプローチ**:
- `vswhere`を使用してVisual Studioを検出（推測）
- Microsoftが推奨する標準的な方法

**日本語版のアプローチ**:
- `nonCertBuild.py`: `vswhere`を使用（本家と同じ）
- `vcsetup.cmd`: 直接パス検索（本家と異なる）

**整合性の観点**:
- `vcsetup.cmd`も`vswhere`を使用することで、本家のアプローチに近づく
- ただし、`vcsetup.cmd`は日本語版独自のスクリプトのため、本家には存在しない

### 3. `vswhere`の利点と欠点

#### 利点

1. **柔軟性**:
   - Enterprise、Professional、BuildToolsなど、様々なVisual Studioエディションに対応
   - Visual Studioのバージョン（2019、2022など）にも対応可能

2. **標準的な方法**:
   - Microsoftが推奨するVisual Studio検出方法
   - 本家のアプローチと同じ

3. **CI環境での動作**:
   - GitHub ActionsなどのCI環境でも動作する
   - Visual Studioがインストールされている環境では`vswhere`が利用可能

4. **将来の拡張性**:
   - Visual Studio 2025など、将来のバージョンにも対応可能

#### 欠点

1. **依存関係**:
   - Visual Studioインストーラーに依存する
   - Visual Studioがインストールされていない環境では存在しない可能性がある

2. **実装の複雑さ**:
   - `vswhere`の呼び出しと結果の解析が必要
   - エラーハンドリングが複雑になる可能性がある

3. **パフォーマンス**:
   - `vswhere`の実行には時間がかかる可能性がある
   - 直接パス検索の方が高速な場合がある

### 4. 直接パス検索の利点と欠点

#### 利点

1. **シンプル**:
   - 実装が簡単
   - 追加の依存関係が不要

2. **高速**:
   - ファイルシステムの直接検索のため、高速

3. **確実性**:
   - Visual Studioがインストールされている限り、動作する

#### 欠点

1. **柔軟性の欠如**:
   - Visual Studio 2022のみサポート（ハードコード）
   - エディションの検索順序が固定

2. **将来の拡張性**:
   - Visual Studio 2025など、将来のバージョンに対応するにはコード変更が必要

3. **本家との差異**:
   - 本家のアプローチ（`vswhere`）と異なる

## 推奨アプローチ

### 案1: `vswhere`を優先し、直接パス検索をフォールバックとする（推奨）

**実装**:
1. まず`vswhere`を使用してVisual Studioを検出
2. `vswhere`が失敗した場合、直接パス検索にフォールバック

**利点**:
- `nonCertBuild.py`との一貫性が向上する
- 本家のアプローチに近づく
- 柔軟性が向上する（様々なVisual Studioエディションに対応）
- フォールバックにより、`vswhere`が存在しない環境でも動作する

**欠点**:
- 実装が複雑になる
- `vswhere`の呼び出しと結果の解析が必要

**評価**: ⭐⭐⭐⭐⭐（推奨）

### 案2: 直接パス検索を維持（現状維持）

**実装**:
- 現在の実装を維持（`vs_utils.py`を使用）

**利点**:
- 実装がシンプル
- 追加の依存関係が不要

**欠点**:
- `nonCertBuild.py`との一貫性が低い
- 本家のアプローチと異なる
- 柔軟性が低い（Visual Studio 2022のみサポート）

**評価**: ⭐⭐⭐（中程度）

### 案3: `vswhere`のみを使用（フォールバックなし）

**実装**:
- `vswhere`のみを使用し、フォールバックなし

**利点**:
- `nonCertBuild.py`との完全な一貫性
- 本家のアプローチと同じ

**欠点**:
- `vswhere`が存在しない環境では動作しない
- リスクが高い

**評価**: ⭐⭐（非推奨）

## 推奨される実装（案1）

### `vs_utils.py`の拡張

```python
def find_vcvars_with_vswhere(arch: Literal["x86", "x64"] = "x86") -> str | None:
    """Find vcvars script using vswhere (preferred method).
    
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
    """Find vcvars32.bat or vcvars64.bat in Visual Studio 2022 install locations.
    
    First tries vswhere (preferred), then falls back to direct path search.
    
    Args:
        arch: Target architecture ("x86" or "x64"). Defaults to "x86".
        
    Returns:
        Absolute path to vcvars script if found, None otherwise.
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

### `vcsetup.ps1`の実装

```powershell
# Try vswhere first (preferred method, consistent with nonCertBuild.py)
$vcvarsPath = $null
$vswhere = "C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe"
if (Test-Path $vswhere) {
    try {
        $scriptName = if ($Architecture -eq "x64") { "vcvars64.bat" } else { "vcvars32.bat" }
        $pattern = "VC\Auxiliary\Build\$scriptName"
        
        $result = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -find $pattern -format value 2>&1
        if ($result -and (Test-Path $result)) {
            $vcvarsPath = $result
            Write-Host "[vcsetup] Found vcvars via vswhere: $vcvarsPath"
        }
    } catch {
        Write-Warning "vswhere search failed: $_"
    }
}

# Fallback to Python-based search (vs_utils.py)
if (-not $vcvarsPath) {
    try {
        $findVcvarsScript = Join-Path $scriptRoot "find_vcvars.py"
        $vcvarsPath = python $findVcvarsScript $Architecture 2>&1 | Where-Object { $_ -and $_ -notmatch "^\s*$" } | Select-Object -First 1
        if ($vcvarsPath -and (Test-Path $vcvarsPath)) {
            Write-Host "[vcsetup] Found vcvars via Python: $vcvarsPath"
        } else {
            $vcvarsPath = $null
        }
    } catch {
        Write-Warning "Python-based vcvars search failed: $_"
        $vcvarsPath = $null
    }
}

# Fallback to direct path search (for environments without vswhere or Python)
if (-not $vcvarsPath) {
    Write-Host "[vcsetup] Falling back to direct search..."
    $scriptName = if ($Architecture -eq "x64") { "vcvars64.bat" } else { "vcvars32.bat" }
    $editions = @("BuildTools", "Community", "Professional", "Enterprise")
    
    foreach ($edition in $editions) {
        $candidate = "C:\Program Files\Microsoft Visual Studio\2022\$edition\VC\Auxiliary\Build\$scriptName"
        if (Test-Path $candidate) {
            $vcvarsPath = $candidate
            Write-Host "[vcsetup] Found vcvars via direct search: $vcvarsPath"
            break
        }
    }
}
```

## 結論

**推奨**: 案1（`vswhere`を優先し、直接パス検索をフォールバックとする）

**理由**:
1. **`nonCertBuild.py`との一貫性**: 同じ検出方法（`vswhere`）を使用
2. **本家のアプローチに近い**: Microsoftが推奨する標準的な方法
3. **柔軟性**: 様々なVisual Studioエディションに対応
4. **将来の拡張性**: Visual Studio 2025など、将来のバージョンにも対応可能
5. **フォールバック**: `vswhere`が存在しない環境でも動作する

**実装方針**:
1. `vs_utils.py`に`find_vcvars_with_vswhere()`と`find_vcvarsall_with_vswhere()`関数を追加
2. `find_vcvars()`と`find_vcvarsall()`関数を修正し、`vswhere`を優先、直接パス検索をフォールバックとする
3. `scons_jp.py`のコード変更は不要（`vs_utils.py`の内部実装の変更により自動的に`vswhere`を使用）
4. `vcsetup.ps1`で`vswhere`を優先し、Python検索、直接パス検索の順でフォールバック

**影響範囲**:
- `vs_utils.py`: `vswhere`サポートを追加
- `scons_jp.py`: コード変更不要（`vs_utils.py`の内部実装の変更により自動的に`vswhere`を使用）
- `vcsetup.cmd` / `vcsetup.ps1`: `vs_utils.py`を使用しているため、自動的に`vswhere`を使用
- `find_vcvars.py`: `vs_utils.py`を使用しているため、自動的に`vswhere`を使用

## 実装状況（2025年12月30日）

✅ **実装完了**

**実装内容**:
1. ✅ `vs_utils.py`に`find_vcvars_with_vswhere()`と`find_vcvarsall_with_vswhere()`関数を追加
2. ✅ `find_vcvars()`と`find_vcvarsall()`関数を修正し、`vswhere`を優先、直接パス検索をフォールバックとする
3. ✅ Visual Studio 2022を優先的に使用（`-version [17.0,18.0)`）
4. ✅ `vcsetup.cmd`は`vs_utils.py`を使用しているため、自動的に`vswhere`を使用

**検証結果**:
- ✅ x86 JP smoke tests成功
- ✅ `certBuild2025`が実行可能
- ✅ Visual Studio 2022が優先的に検出される

**コミット**:
- `e625d3c8b`: "Add vswhere support to vs_utils.py for stable Visual Studio detection"
- `a9c1c471d`: "Prioritize Visual Studio 2022 over Visual Studio 2025 in vs_utils.py"

**今後の作業**:
- [ ] `vcsetup.ps1`の実装（`projectDocs/jp/vcsetup-ps1-migration-proposal.md`参照）

詳細は`projectDocs/jp/vswhere-implementation-status.md`を参照。
