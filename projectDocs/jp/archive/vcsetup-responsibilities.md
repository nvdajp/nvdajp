# vcsetup.cmd の責務整理

## 概要

`jptools/vcsetup.cmd`は、Visual Studio MSVCビルド環境を設定するためのバッチスクリプトです。このドキュメントでは、`vcsetup.cmd`の責務を明確に定義し、整理します。

## 現在の責務

### 1. Visual Studio vcvarsスクリプトの検索

- **責務**: Visual Studio 2022の`vcvars32.bat`または`vcvars64.bat`を検索する
- **実装**（2025年12月30日更新）:
  - まず`jptools/find_vcvars.py`（`vs_utils.py`を使用）で検索
    - `vs_utils.py`は`vswhere`を使用してVisual Studio 2022を優先検索
    - Visual Studio 2022が見つからない場合のみ、すべてのバージョンを検索
  - Pythonが失敗した場合、直接パス検索（BuildTools, Community, Professional, Enterpriseの順）
- **現在の状態**: 
  - ✅ `vswhere`サポートが追加され、Visual Studio 2022が優先的に使用される
  - ✅ Visual Studio 2025がインストールされていても、Visual Studio 2022が使用される
  - ⚠️ Python依存がある（`find_vcvars.py`が失敗した場合のフォールバックが必要）

### 2. MSVC環境変数の設定

- **責務**: vcvarsスクリプトを実行して、MSVCビルドツール（`cl`, `nmake`, `link`など）をPATHに追加する
- **実装**: `call "%FOUND%" >nul 2>&1`でvcvarsスクリプトを実行
- **問題点**:
  - エラー時の詳細情報が不足（`>nul 2>&1`で出力を抑制）
  - vcvars実行失敗時の診断情報がない

### 3. アーキテクチャの選択と最適化

- **責務**: x86またはx64のMSVC環境を選択し、必要に応じて最適化する
- **実装**:
  - x64ビルド: 常にvcvarsを実行（fast-pathなし）
  - x86ビルド: fast-pathで`cl`と`nmake`が既に利用可能かチェック
- **問題点**:
  - fast-pathロジックが複雑（x86/x64で異なる動作）
  - `cl`と`nmake`の存在確認がfast-path内に混在

### 4. x86ビルド用のCL環境変数設定

- **責務**: x86ビルドの場合、`CL`環境変数に`/arch:IA32`を設定する
- **実装**: `SET CL=/arch:IA32`
- **問題点**: 
  - 既存の`CL`環境変数の値を上書きする可能性がある

## 責務の整理案

### 提案1: 単一責任の原則に基づく分離

`vcsetup.cmd`の責務を以下のように分離します：

#### 責務1: vcvarsスクリプトの検索と実行（コア責務）

```batch
@echo off
rem Core responsibility: Find and execute Visual Studio vcvars script
rem Usage: vcsetup.cmd [x64|x86]
rem Defaults to x86.

set "ARCH=%~1"
if "%ARCH%"=="" set "ARCH=x86"

rem Find vcvars script
call jptools\find_vcvars.cmd %ARCH%
if errorlevel 1 (
  echo [ERROR] Could not locate Visual Studio vcvars script for %ARCH%>&2
  exit /b 1
)

rem Execute vcvars script
call "%VCVARS_PATH%"
if errorlevel 1 (
  echo [ERROR] Failed to execute vcvars script: "%VCVARS_PATH%" >&2
  exit /b 1
)

exit /b 0
```

#### 責務2: fast-path最適化（別スクリプトまたはオプション）

```batch
@echo off
rem Optional optimization: Skip vcvars if MSVC tools are already available
rem Usage: vcsetup-fastpath.cmd [x64|x86]

set "ARCH=%~1"
if "%ARCH%"=="" set "ARCH=x86"

rem For x64, always set up environment
if /I "%ARCH%"=="x64" (
  call jptools\vcsetup.cmd x64
  exit /b %ERRORLEVEL%
)

rem For x86, check if tools are already available
cl >nul 2>&1
if errorlevel 1 goto :setup
nmake /? >nul 2>&1
if errorlevel 1 goto :setup

rem Tools are available, skip setup
exit /b 0

:setup
call jptools\vcsetup.cmd x86
exit /b %ERRORLEVEL%
```

#### 責務3: CL環境変数の設定（別スクリプトまたはオプション）

```batch
@echo off
rem Set CL environment variable for x86 builds
rem Usage: vcsetup-cl.cmd [x64|x86]

set "ARCH=%~1"
if "%ARCH%"=="" set "ARCH=x86"

if /I "%ARCH%"=="x86" (
  rem Append /arch:IA32 to existing CL, or set it if not defined
  if defined CL (
    set "CL=%CL% /arch:IA32"
  ) else (
    set "CL=/arch:IA32"
  )
)
```

### 提案2: 現在の実装を改善（段階的アプローチ）

現在の`vcsetup.cmd`を維持しつつ、以下の改善を行います：

#### 改善1: エラーハンドリングの強化

```batch
rem Execute vcvars script with error output
call "%FOUND%" 2>&1 | findstr /V "^$" > "%TEMP%\vcvars_output.txt"
set "VCVARS_EXIT=%ERRORLEVEL%"
if "%VCVARS_EXIT%" neq "0" (
  echo [ERROR] Failed to execute vcvars script: "%FOUND%" >&2
  echo [ERROR] Output: >&2
  type "%TEMP%\vcvars_output.txt" >&2
  exit /b 1
)
```

#### 改善2: fast-pathロジックの明確化

```batch
rem Fast path optimization (x86 only)
if /I "%ARCH%"=="x86" (
  rem Check if MSVC tools are already available
  cl >nul 2>&1
  if "%ERRORLEVEL%" neq "9009" (
    nmake /? >nul 2>&1
    if "%ERRORLEVEL%" neq "9009" (
      rem Both cl and nmake are available, skip setup
      echo [vcsetup] MSVC tools already available, skipping setup
      goto :set_cl_arch
    )
  )
)
```

#### 改善3: CL環境変数の安全な設定

```batch
:set_cl_arch
if defined SET_CL_ARCH (
  rem Append /arch:IA32 to existing CL, or set it if not defined
  if defined CL (
    echo [vcsetup] Appending /arch:IA32 to existing CL=%CL%
    set "CL=%CL% /arch:IA32"
  ) else (
    echo [vcsetup] Setting CL=/arch:IA32
    set "CL=/arch:IA32"
  )
)
```

## Python依存について

### 導入の経緯

コミット`53fcb90b9`（2025-12-28）で、`vcsetup.cmd`にPython依存（`find_vcvars.py`）が導入されました。

**導入理由**（コメントより）:
- `scons_jp.py`と`runJpSmokeTests.ps1`との一貫性を保つため
- `vs_utils.py`で共通ロジックを共有するため

### 方針の評価

#### 利点

1. **コードの重複回避**: `vs_utils.py`でVisual Studio検索ロジックを一元管理
2. **一貫性**: Pythonスクリプト（`scons_jp.py`, `runJpSmokeTests.ps1`）と同じ検索ロジックを使用
3. **保守性**: Visual Studio検索ロジックの変更が1箇所で済む

#### 問題点

1. **依存関係の複雑化**: バッチスクリプトがPythonに依存する（通常は不要）
2. **起動オーバーヘッド**: Pythonプロセスの起動が必要（フォールバックで緩和）
3. **環境依存**: Pythonが利用できない環境ではフォールバックが必要（既に実装済み）

### 推奨アプローチ

**現状維持（提案2の改善）**を推奨します。理由：

1. **実用性**: フォールバックが実装されており、Pythonが利用できない環境でも動作する
2. **一貫性**: Pythonスクリプトとの一貫性が保たれている
3. **保守性**: 共通ロジックの一元管理により、保守が容易

**ただし、以下の改善を推奨**：

1. **エラーハンドリングの強化**: Python呼び出し失敗時の詳細情報
2. **ドキュメントの明確化**: Python依存の理由とフォールバックの動作を明記
3. **テスト**: Pythonが利用できない環境での動作確認

### 代替案（将来の検討）

もしPython依存を完全に排除したい場合：

1. **純粋なバッチスクリプト**: `vcsetup.cmd`を純粋なバッチスクリプトとして実装
2. **Pythonスクリプトからの呼び出し**: `scons_jp.py`や`runJpSmokeTests.ps1`から`vcsetup.cmd`を呼び出す際に、Pythonで検索したパスを環境変数として渡す
3. **共通ライブラリ**: Visual Studio検索ロジックを別の形式（例: PowerShellモジュール）で共有

ただし、現時点では**現状維持が最適**と判断します。

## 推奨アプローチ

**提案2（段階的アプローチ）**を推奨します。理由：

1. **後方互換性**: 既存の呼び出し元（`certBuild2023.cmd`, `nonCertBuild.py`など）への影響が最小限
2. **実装の簡潔性**: 単一スクリプトで責務を管理しやすい
3. **段階的改善**: 問題が発生した場合、部分的に改善できる
4. **Python依存**: 既に実装されており、フォールバックにより実用上の問題はない

## 改善後の責務定義

### 主要責務

1. **Visual Studio vcvarsスクリプトの検索と実行**
   - `find_vcvars.py`を使用してvcvarsスクリプトを検索
   - フォールバックとして直接パス検索
   - vcvarsスクリプトを実行してMSVC環境変数を設定

2. **アーキテクチャに応じた最適化**
   - x64ビルド: 常にvcvarsを実行（x86ツールの混入を防止）
   - x86ビルド: fast-pathで既存ツールをチェック（パフォーマンス向上）

3. **x86ビルド用のCL環境変数設定**
   - x86ビルドの場合、`CL`環境変数に`/arch:IA32`を追加

### 非責務（他のスクリプトに委譲すべき）

1. **MSVCツールの存在確認**: `certBuild2023.cmd`で`nmake /?`を実行して確認
2. **Visual Studioバージョンの確認**: `check_vs_version.cmd`で確認
3. **環境変数の検証**: 呼び出し元で検証

## 既知の問題と修正履歴

### enabledelayedexpansion問題の修正（2025年12月30日）

**問題**: `certBuild2023.cmd`が`setlocal enabledelayedexpansion`を使用しているため、`vcsetup.cmd`内の`if "%VCVARS_EXIT%" neq "0" (...)`構文で変数展開タイミングの問題が発生。`VCVARS_EXIT`=0でも条件が真と評価され、`vcsetup.cmd`が誤って終了コード1を返していた。

**修正**: `if ... (...)`構文を`if ... goto :label`構文に変更し、`()`ブロックを使用しないことで`enabledelayedexpansion`の影響を回避。

```batch
rem 修正前（問題のあるコード）
if "%VCVARS_EXIT%" neq "0" (
  echo [ERROR] Failed to execute vcvars script: "%FOUND%" (exit code: %VCVARS_EXIT%) >&2
  exit /b 1
)

rem 修正後（gotoベースの条件分岐）
if "%VCVARS_EXIT%" equ "0" goto :vcvars_exit_ok
echo [ERROR] Failed to execute vcvars script: "%FOUND%" (exit code: %VCVARS_EXIT%) >&2
exit /b 1
:vcvars_exit_ok
```

**教訓**: バッチスクリプトで`setlocal enabledelayedexpansion`が有効な親プロセスから呼び出される場合、`if`文の`()`ブロック内での変数展開タイミングに注意が必要。`goto`ベースの条件分岐を使用することで、この問題を回避できる。

**関連コミット**: `2051a0c3d` - "クリーンアップ: デバッグログを削除"（2025年12月30日）

## 実装チェックリスト

- [x] enabledelayedexpansion問題の修正（2025年12月30日完了）
- [ ] エラーハンドリングの強化（vcvars実行失敗時の詳細出力）
- [ ] fast-pathロジックの明確化（コメントの追加）
- [ ] CL環境変数の安全な設定（既存値の保持）
- [ ] Visual Studio 2022以外のバージョン対応（将来の拡張性）
- [ ] テストケースの追加（x86/x64、fast-path、エラーケース）

## 関連ドキュメント

- `projectDocs/jp/build-architecture-environment-variables.md`: `BUILD_ARCH`と`TARGET_ARCH`の関係
- `projectDocs/jp/vswhere-implementation-status.md`: `vswhere`実装状況のまとめ（実装済み）
- `projectDocs/jp/vcsetup-ps1-migration-proposal.md`: PowerShell移行案（将来の作業）
- `projectDocs/jp/vcsetup-ps1-qa-evaluation.md`: PowerShell移行の品質保証評価（将来の作業）
- `jptools/find_vcvars.py`: vcvarsスクリプト検索の実装
- `jptools/vs_utils.py`: Visual Studio検索のユーティリティ（`vswhere`サポート追加済み）
