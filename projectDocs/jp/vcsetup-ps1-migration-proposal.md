# vcsetup.cmd → vcsetup.ps1 移行案

## 概要

`jptools/vcsetup.cmd`をPowerShellスクリプト（`jptools/vcsetup.ps1`）に移行する案を検討します。

## 移行の利点

### 1. Python依存の扱いやすさ

* **現状**: バッチスクリプトから`python find_vcvars.py`を呼び出す必要がある
* **移行後**: PowerShellから直接`vs_utils.py`をインポート可能








  ```powershell
  # PowerShellから直接Pythonモジュールを使用
* $vsUtilsPath = Join-Path $PSScriptRoot "vs_utils.py"
* # または、Pythonスクリプトを呼び出す（より簡単）
* $vcvarsPath = python "$PSScriptRoot\find_vcvars.py" $arch
* ```
*
*## 2. エラーハンドリングの強化
*

* **現状**: バッチスクリプトのエラーハンドリングは限定的

* **移行後**: PowerShellの`try-catch`、詳細なエラーメッセージ、ログ出力が可能

*

*## 3. 環境変数の設定

*

* **現状**: `call "%FOUND%"`でvcvarsを実行し、環境変数を設定

* **移行後**: PowerShellで環境変数を直接設定・管理可能
*
* ```powershell
* # vcvarsの出力をキャプチャして環境変数を設定
* $envOutput = cmd /c "`"$vcvarsPath`" $arch >nul 2>&1 && set"
* foreach ($line in $envOutput) {
*     if ($line -match '^([^=]+)=(.*)$') {
*         [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
*     }
* }
* ```
*
*## 4. 既存のPowerShellスクリプトとの一貫性
*
* `runJpSmokeTests.ps1`は既にPowerShellで実装されている
* `checkJtalkArch.ps1`もPowerShellで実装されている
* 同じ言語で統一することで、保守性が向上

### 5. バッチスクリプトの複雑さの回避

**問題例**: `enabledelayedexpansion`問題（2025年12月30日修正）

`certBuild2023.cmd`が`setlocal enabledelayedexpansion`を使用しているため、`vcsetup.cmd`内の`if "%VCVARS_EXIT%" neq "0" (...)`構文で変数展開タイミングの問題が発生。`VCVARS_EXIT`=0でも条件が真と評価され、誤って終了コード1を返していた。

**修正**: `if`文を`goto`ベースの条件分岐に変更する必要があった。

```batch
rem 修正前（問題のあるコード）
if "%VCVARS_EXIT%" neq "0" (
  echo [ERROR] ...
  exit /b 1
)

rem 修正後（gotoベースの条件分岐）
if "%VCVARS_EXIT%" equ "0" goto :vcvars_exit_ok
echo [ERROR] ...
exit /b 1
:vcvars_exit_ok
```

**PowerShell移行の利点**: PowerShellでは`if`文の`()`ブロック内でも変数展開が正しく動作し、このような問題が発生しない。

```powershell

# PowerShellでは自然に動作
if ($VCVARS_EXIT -ne 0) {

    Write-Error "Failed to execute vcvars script: $FOUND (exit code: $VCVARS_EXIT)"
    exit 1


}
```




**関連ドキュメント**: `projectDocs/jp/vcsetup-responsibilities.md`の「既知の問題と修正履歴」セクション




## 呼び出し元への影響





### 1. `certBuild2023.cmd`（バッチスクリプト）






**現状**:


```batch



call jptools\vcsetup.cmd %BUILD_ARCH%

```





**移行後（オプション1: ラッパーを残す）**:

```batch
rem vcsetup.cmdはvcsetup.ps1を呼び出すラッパーとして残す


*
*
powershell -ExecutionPolicy Bypass -NoProfile -File jptools\vcsetup.ps1 %BUILD_ARCH%
```

**移行後（オプション2: 直接呼び出し）**:


*
*
*``batch
*owershell -ExecutionPolicy Bypass -NoProfile -File jptools\vcsetup.ps1 %BUILD_ARCH%
if errorlevel 1 goto onerror
```
*
*
*
*
**推奨**: オプション1（後方互換性のため）
*
### 2. `nonCertBuild.py`（Pythonスクリプト）

**現状**:
*
*
*
*``python
*nvmap = _capture_env_via_cmd(f'call "{vcsetup}" >nul', cwd=repo_root)
```


**移行後**:
*
*
*``python
* PowerShellスクリプトを呼び出して環境変数をキャプチャ
*nvmap = _capture_env_via_cmd(
    f'powershell -ExecutionPolicy Bypass -NoProfile -File "{vcsetup}" >nul',
    cwd=repo_root

*
*
*``
*
**注意**: `nonCertBuild.py`は環境変数をキャプチャする必要があるため、PowerShellスクリプトも環境変数を設定する必要がある
*
### 3. `miscDepsJp/include/python-jtalk/vcsetup.cmd`（ラッパー）

*
**現状**:
*
*``batch
*all "%~dp0..\..\..\jptools\vcsetup.cmd" x86
*``
*
**移行後**: 変更不要（`vcsetup.cmd`がラッパーとして残る場合）

*
*## 4. その他の呼び出し元
*
* `miscDepsJp/jptools/clean.cmd`
* `miscDepsJp/jptools/build-and-test.cmd`
*
*れらは`miscDepsJp/include/python-jtalk/vcsetup.cmd`経由で呼び出されるため、影響なし

## 実装案
*
*
*## 案1: 完全移行（`vcsetup.cmd`を削除）
*
**メリット**:
* シンプルな実装
* メンテナンス対象が1つに減る

**デメリット**:
*
* すべての呼び出し元を更新する必要がある
* 後方互換性がない
*
**推奨度**: ⭐⭐（後方互換性の問題）
*
*## 案2: 段階的移行（`vcsetup.cmd`をラッパーとして残す）

**メリット**:
*
* 後方互換性を維持
* 既存の呼び出し元を変更する必要がない
* 段階的に移行可能
*
**デメリット**:
* `vcsetup.cmd`と`vcsetup.ps1`の2つのファイルを維持する必要がある

**実装**:
*
*``batch
@echo off
rem Wrapper for vcsetup.ps1 (backward compatibility)
*em Usage: vcsetup.cmd [x64|x86]
*
set "ARCH=%~1"
if "%ARCH%"=="" set "ARCH=x86"

*owershell -ExecutionPolicy Bypass -NoProfile -File "%~dp0vcsetup.ps1" %ARCH%
*xit /b %ERRORLEVEL%
```

**推奨度**: ⭐⭐⭐⭐⭐（推奨）
*
### 案3: ハイブリッド（`vcsetup.cmd`と`vcsetup.ps1`を並行運用）

**メリット**:
* 呼び出し元が選択可能
* 段階的な移行が可能

**デメリット**:
* 2つの実装を維持する必要がある
* 重複コードのリスク

**推奨度**: ⭐⭐⭐（中程度）

## 実装例（案2: ラッパー方式）

### `jptools/vcsetup.ps1`（新規作成）

```powershell
<#
.SYNOPSIS
    Setup MSVC build environment persistently.

.DESCRIPTION
    Sets up Visual Studio MSVC build environment for x86 or x64 architecture.
    This script replaces vcsetup.cmd with improved error handling and Python integration.

.PARAMETER Architecture
    Target architecture: x86 or x64. Defaults to x86.

.EXAMPLE
    .\vcsetup.ps1 x86
    Sets up x86 MSVC environment.

.EXAMPLE
    .\vcsetup.ps1 x64
    Sets up x64 MSVC environment.
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet("x86", "x64")]
    [string]$Architecture = "x86"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

# Fast path for x86: check if MSVC tools are already available
if ($Architecture -eq "x86") {
    try {
        $null = Get-Command cl -ErrorAction Stop
        $null = Get-Command nmake -ErrorAction Stop
        Write-Host "[vcsetup] MSVC tools already available, skipping setup"
        # Set CL environment variable for x86 builds
        if (-not $env:CL) {
            $env:CL = "/arch:IA32"
        } elseif ($env:CL -notmatch "/arch:IA32") {
            $env:CL = "$env:CL /arch:IA32"
        }
        exit 0
    } catch {
        # Tools not available, continue with setup
    }
}

# Find vcvars script using Python (shared logic with scons_jp.py)
$vcvarsPath = $null
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

# Fallback to direct search if Python failed
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

if (-not $vcvarsPath -or -not (Test-Path $vcvarsPath)) {
    Write-Error "Could not locate Visual Studio 2022 vcvars script for $Architecture"
    exit 1
}

# Execute vcvars script and capture environment variables
Write-Host "[vcsetup] Using: $vcvarsPath"
try {
    # Run vcvars and capture environment variables
    $envOutput = cmd /c "`"$vcvarsPath`" $Architecture >nul 2>&1 && set"

    # Parse and set environment variables
    $envVarsSet = 0
    foreach ($line in $envOutput) {
   *    if ($line -match '^([^=]+)=(.*)$') {
   *        $key = $matches[1]
   *        $value = $matches[2]
            [System.Environment]::SetEnvironmentVariable($key, $value, 'Process')
            $envVarsSet++
        }
    }

    if ($envVarsSet -eq 0) {
   *    Write-Warning "No environment variables were set by vcvars script"
   *} else {
   *    Write-Host "[vcsetup] Set $envVarsSet environment variables"

    }

    # Verify nmake is available
    try {
        $null = Get-Command nmake -ErrorAction Stop
        Write-Host "[vcsetup] nmake is now available"
   *} catch {
   *    Write-Warning "nmake is still not available after vcvars execution"
   *}



    # Set CL environment variable for x86 builds
    if ($Architecture -eq "x86") {
        if (-not $env:CL) {
            $env:CL = "/arch:IA32"
            Write-Host "[vcsetup] Set CL=/arch:IA32"
   *    } elseif ($env:CL -notmatch "/arch:IA32") {
   *        $env:CL = "$env:CL /arch:IA32"
   *        Write-Host "[vcsetup] Appended /arch:IA32 to CL=$env:CL"

        }

    }

    Write-Host "[vcsetup] MSVC environment setup completed"
    exit 0

} c*tch {

   *Write-Error "Failed to execute vcvars script: $_"
   *exit 1

}

```

### `jptools/vcsetup.cmd`（ラッパーとして残す）

```batch
*ec*o off
*
*em*Wrapper for vcsetup.ps1 (backward compatibility)
rem*This script delegates to vcsetup.ps1 to maintain compatibility with existing callers.


rem Usage: vcsetup.cmd [x64|x86]

rem Defaults to x86.

set "ARCH=%~1"
if "%ARCH%"=="" set "ARCH=x86"

*ow*rshell -ExecutionPolicy Bypass -NoProfile -File "%~dp0vcsetup.ps1" %ARCH%
*
*xi* /b %ERRORLEVEL%
```*




## 移行手順

1. **`vcsetup.ps1`を作成**: 上記の実装例をベースに作成
2. **`vcsetup.cmd`をラッパーに変更**: 既存の実装をラッパーに置き換え
3. **テスト**:
*  * `certBuild2023.cmd`からの呼び出し
*
*  * `nonCertBuild.py`からの呼び出し
   * `miscDepsJp`からの呼び出し


4. **ドキュメント更新**: `vcsetup-responsibilities.md`を更新


## 注意事項

### 1. 環境変数の継承

*owerShellスクリプトから設定した環境変数は、呼び出し元のバッチスクリプトに継承される必要がある。
*
*
**確認方法**:


```batch

call jptools\vcsetup.cmd x86
echo PATH=%PATH%
nmake /?
```

*## 2. エラーハンドリング
*
*
バッチスクリプトからの呼び出しで、エラーコードが正しく返されることを確認する。


**確認方法**:

```batch
call jptools\vcsetup.cmd x86
if errorlevel 1 (
    echo Error occurred
    exit /b 1
*
*
*``

### 3. PowerShell実行ポリシー


`-ExecutionPolicy Bypass`を使用することで、実行ポリシーの問題を回避する。

## まとめ

**推奨**: 案2（ラッパー方式）で段階的に移行

**理由**:
*
*. 後方互換性を維持
2. 既存の呼び出し元を変更する必要がない
3. PowerShellの利点（エラーハンドリング、Python統合）を活用できる

4. 段階的な移行が可能

## 実装状況

⏳ **未実装（将来の作業）**

**現在の状態**:
* ✅ `vswhere`リファクタリングは完了（`vs_utils.py`に`vswhere`サポート追加）
* ✅ Visual Studio 2022が優先的に使用される
* ⏳ `vcsetup.ps1`への移行は未実装

**次のステップ**（将来の作業）:

1. `vcsetup.ps1`の実装とテスト
2. `vcsetup.cmd`をラッパーに変更
3. 既存の呼び出し元での動作確認
4. ドキュメント更新

詳細は`projectDocs/jp/vcsetup-ps1-qa-evaluation.md`を参照。
