# vcsetup.cmd → vcsetup.ps1 移行案の品質保証評価

## 品質保証原則（roadmap.mdより）

1. **小さなPR単位で進める**: 各PRで必ず全テストが通過することを確認
2. **段階的な検証を必須とする**: 各段階でビルド・型チェック・単体テスト・システムテストを通過確認
3. **完了の定義を明確化**: テストが全て通過し、CIが安定して緑になるまで「完了」としない
4. **問題が発生したら即座に停止**: テスト失敗や不安定な動作が見られたら、次の段階に進まずに問題を解決
5. **開発環境の事前整備を優先**: ローカルで頻繁に実行できる環境を事前に整備

## 重要な論点: 本家との差分

### 本家のMSVC環境設定方法

**本家（nvaccess/beta）のアプローチ**:
- SConsがMSVCを自動検出（`sconstruct`で`env = Environment(tools=['default', 'msvc'])`）
- CIでは`ilammy/msvc-dev-cmd@v1`を使用してMSVC環境を設定
- `nonCertBuild.py`では`vswhere`を使用してMSVC環境を設定（本家のアプローチに近い）
- **`vcsetup.cmd`のようなスクリプトは存在しない**

**本家がSConsだけでMSVCを使える理由**:
- SConsのMSVCツールチェーンが自動的にVisual Studioを検出
- `cl.exe`や`link.exe`などのコンパイラツールを自動的に見つける
- ただし、`nmake`が必要な場合は明示的な環境設定が必要

### 日本語版で`vcsetup.cmd`が必要な理由

**日本語版独自の要件**:
1. **`nmake`が必要**: `jtalkPrep`で`nmake`を使用して`libopenjtalk.dll`をビルド
2. **バッチスクリプトからの呼び出し**: `certBuild2023.cmd`（バッチスクリプト）からMSVC環境を設定する必要がある
3. **x86/x64の切り替え**: `BUILD_ARCH`に応じてMSVC環境を切り替える必要がある

**`vcsetup.cmd`が存在する理由**:
- `certBuild2023.cmd`（バッチスクリプト）からMSVC環境を設定するため
- `nmake`を利用可能にするため（SConsのMSVCツールチェーンだけでは不十分）
- x86/x64の切り替えをサポートするため

### 本家との差分への影響

**現状（vcsetup.cmd）**:
- 日本語版独自のスクリプト（本家には存在しない）
- バッチスクリプト + Python依存の複雑な実装

**移行後（vcsetup.ps1）**:
- 日本語版独自のスクリプト（本家には存在しない）← **変わらない**
- PowerShellスクリプト + Python依存の実装

**評価**:
- **本家との差分は変わらない**: `vcsetup.cmd`も`vcsetup.ps1`も日本語版独自のスクリプト
- **実装の複雑さ**: PowerShellの方が可読性が高く、保守しやすい
- **本家との整合性**: `nonCertBuild.py`は既に`vswhere`を使用（本家のアプローチに近い）

### 本家のアプローチを参考にできるか？

**検討事項**:
1. **`nonCertBuild.py`のアプローチ**: `vswhere`を使用してMSVC環境を設定（本家のアプローチに近い）
2. **`certBuild2023.cmd`の制約**: バッチスクリプトから`vswhere`を呼び出す必要がある
3. **`vcsetup.cmd`の役割**: バッチスクリプトからMSVC環境を設定するためのラッパー

**結論**:
- `vcsetup.cmd`（または`vcsetup.ps1`）は日本語版独自の要件のため、本家には存在しない
- 本家のアプローチ（`vswhere`）を参考にできるが、バッチスクリプトからの呼び出しという制約がある
- PowerShellへの移行は、本家との差分を増やすものではなく、実装の改善である

## 評価項目

### 1. テスト可能性

#### 現状（vcsetup.cmd）

**問題点**:
- バッチスクリプトのテストが困難
- 環境変数の設定を検証する方法が限定的
- エラーケースのテストが難しい

**テスト方法**:
- 手動テスト: `certBuild2023.cmd`からの呼び出しを確認
- 間接的な検証: ビルドが成功するかどうかで判断

#### 移行後（vcsetup.ps1）

**利点**:
- PowerShellスクリプトのテストが容易（Pesterなど）
- 関数単位でのテストが可能
- モックを使用した単体テストが可能

**テスト方法**:
```powershell
# Pesterを使用したテスト例
Describe "vcsetup.ps1" {
    It "should find vcvars32.bat for x86" {
        # テスト実装
    }

    It "should set CL environment variable for x86" {
        # テスト実装
    }

    It "should handle Python failure gracefully" {
        # テスト実装
    }
}
```

**評価**: ⭐⭐⭐⭐⭐（大幅に改善）

### 2. 段階的な検証の容易さ

#### 現状（vcsetup.cmd）

**問題点**:
- 変更の影響範囲が広い（すべての呼び出し元に影響）
- 段階的な検証が困難（バッチスクリプトの特性上）

#### 移行後（vcsetup.ps1 + ラッパー）

**利点**:
- ラッパー方式により、段階的な移行が可能
- `vcsetup.cmd`を残すことで、既存の呼び出し元への影響を最小化
- 新しい実装（`vcsetup.ps1`）を独立してテスト可能

**検証手順**:
1. `vcsetup.ps1`を作成し、単体テストを実装
2. `vcsetup.cmd`をラッパーに変更し、`vcsetup.ps1`を呼び出す
3. 既存の呼び出し元（`certBuild2023.cmd`など）で動作確認
4. CIで全テストが通過することを確認
5. 問題がなければ、ラッパーを維持して完了

**評価**: ⭐⭐⭐⭐（段階的検証が容易）

### 3. リスク管理

#### 現状（vcsetup.cmd）

**リスク**:
- Python依存の追加により、複雑性が増加
- エラーハンドリングが不十分
- 環境変数の設定が不透明

#### 移行後（vcsetup.ps1）

**リスク**:
- PowerShell実行ポリシーの問題（`-ExecutionPolicy Bypass`で回避可能）
- 環境変数の継承（バッチスクリプトから呼び出した場合）
- 既存の動作との差異

**リスク軽減策**:
1. **ラッパー方式**: `vcsetup.cmd`を残すことで、既存の動作を維持
2. **段階的な移行**: 小さなPR単位で進める
3. **包括的なテスト**: すべての呼び出し元で動作確認
4. **ロールバック計画**: 問題が発生した場合、`vcsetup.cmd`を元の実装に戻す

**評価**: ⭐⭐⭐（リスクは管理可能）

### 4. 保守性

#### 現状（vcsetup.cmd）

**問題点**:
- バッチスクリプトの可読性が低い
- Python依存の扱いが複雑（`for /f`ループでPython呼び出し）
- エラーハンドリングが限定的

#### 移行後（vcsetup.ps1）

**利点**:
- PowerShellの可読性が高い
- エラーハンドリングが強化可能（`try-catch`）
- 既存のPowerShellスクリプト（`runJpSmokeTests.ps1`など）との一貫性

**評価**: ⭐⭐⭐⭐（保守性が向上）

### 5. 開発環境での検証

#### 現状（vcsetup.cmd）

**検証方法**:
- 手動で`certBuild2023.cmd`を実行
- ビルドが成功するかどうかで判断

#### 移行後（vcsetup.ps1）

**検証方法**:
- PowerShellスクリプトを直接実行してテスト可能
- 単体テスト（Pester）を実行可能
- デバッグが容易（`Set-PSDebug -Trace 1`など）

**評価**: ⭐⭐⭐⭐（開発環境での検証が容易）

### 6. CI/CDでの検証

#### 現状（vcsetup.cmd）

**検証**:
- CIでビルドが成功するかどうかで間接的に検証
- エラーが発生した場合、原因の特定が困難

#### 移行後（vcsetup.ps1）

**検証**:
- CIでPowerShellスクリプトのテストを実行可能
- エラーメッセージが詳細で、原因の特定が容易
- ログ出力が改善され、デバッグが容易

**評価**: ⭐⭐⭐⭐（CI/CDでの検証が改善）

## 品質保証チェックリスト

### 移行前の準備

- [ ] `vcsetup.ps1`の実装
- [ ] `vcsetup.ps1`の単体テスト（Pester）の実装
- [ ] `vcsetup.cmd`ラッパーの実装
- [ ] ローカル環境での動作確認
  - [ ] `certBuild2023.cmd`からの呼び出し
  - [ ] `nonCertBuild.py`からの呼び出し
  - [ ] `miscDepsJp`からの呼び出し

### 段階的な検証

#### ステップ1: `vcsetup.ps1`の作成とテスト

- [ ] `vcsetup.ps1`を作成
- [ ] 単体テストを実装
- [ ] ローカル環境で単体テストを実行
- [ ] すべてのテストが通過することを確認

#### ステップ2: ラッパーの実装

- [ ] `vcsetup.cmd`をラッパーに変更
- [ ] ローカル環境で動作確認
  - [ ] `certBuild2023.cmd`からの呼び出し
  - [ ] 環境変数が正しく設定されることを確認
  - [ ] `nmake`が利用可能になることを確認

#### ステップ3: 既存の呼び出し元での検証

- [ ] `certBuild2023.cmd`からの呼び出し
  - [ ] x86ビルドが成功することを確認
  - [ ] x64ビルドが成功することを確認
- [ ] `nonCertBuild.py`からの呼び出し
  - [ ] 環境変数が正しくキャプチャされることを確認
- [ ] `miscDepsJp`からの呼び出し
  - [ ] すべての呼び出し元で動作することを確認

#### ステップ4: CIでの検証

- [ ] PRを作成
- [ ] CIで全テストが通過することを確認
  - [ ] 型チェック: `ci/scripts/tests/typeCheck.ps1`
  - [ ] ビルドテスト: `certBuild2023.cmd`
  - [ ] 単体テスト: `rununittests.bat`
  - [ ] システムテスト: `runJpSmokeTests.ps1`
- [ ] CIが安定して緑になることを確認

#### ステップ5: 問題発生時の対応

- [ ] 問題が発生した場合のロールバック計画を準備
- [ ] `vcsetup.cmd`を元の実装に戻す手順を文書化

## 推奨される移行戦略

### フェーズ1: 準備（PR #1）

1. `vcsetup.ps1`を作成
2. 単体テスト（Pester）を実装
3. ローカル環境でテストを実行
4. すべてのテストが通過することを確認

**完了条件**:
- `vcsetup.ps1`が完成
- 単体テストがすべて通過
- ドキュメントが更新されている

### フェーズ2: ラッパーの実装（PR #2）

1. `vcsetup.cmd`をラッパーに変更
2. ローカル環境で動作確認
3. 既存の呼び出し元で動作確認

**完了条件**:
- `vcsetup.cmd`が`vcsetup.ps1`を呼び出す
- すべての呼び出し元で動作する
- 環境変数が正しく設定される

### フェーズ3: CIでの検証（PR #2の続き）

1. CIで全テストが通過することを確認
2. CIが安定して緑になることを確認
3. 問題がなければ完了

**完了条件**:
- CIで全テストが通過
- CIが安定して緑になる
- 問題が発生した場合、ロールバック可能

## 品質保証上の懸念事項と対策

### 懸念1: 環境変数の継承

**懸念**: PowerShellスクリプトから設定した環境変数が、呼び出し元のバッチスクリプトに継承されない可能性

**対策**:
- `[System.Environment]::SetEnvironmentVariable($key, $value, 'Process')`を使用
- テストで環境変数の継承を確認
- `nonCertBuild.py`の`_capture_env_via_cmd`で検証

### 懸念2: PowerShell実行ポリシー

**懸念**: PowerShell実行ポリシーにより、スクリプトが実行できない可能性

**対策**:
- `-ExecutionPolicy Bypass`を使用
- CI環境での実行ポリシーを確認
- ドキュメントに実行ポリシーの要件を明記

### 懸念3: エラーコードの返却

**懸念**: PowerShellスクリプトのエラーコードが、呼び出し元のバッチスクリプトに正しく返されない可能性

**対策**:
- `exit`コマンドで明示的にエラーコードを返す
- テストでエラーコードの返却を確認
- `certBuild2023.cmd`の`if errorlevel 1`で検証

### 懸念4: 既存の動作との差異

**懸念**: PowerShellスクリプトの動作が、既存のバッチスクリプトと異なる可能性

**対策**:
- 既存の動作を詳細に分析
- テストで既存の動作を再現
- 段階的な移行により、問題を早期に発見

## 結論

### 品質保証の観点からの評価

**総合評価**: ⭐⭐⭐⭐（推奨）

**理由**:
1. **テスト可能性**: PowerShellスクリプトのテストが容易（Pesterなど）
2. **段階的な検証**: ラッパー方式により、段階的な移行が可能
3. **リスク管理**: ラッパー方式により、既存の動作を維持しながら移行可能
4. **保守性**: PowerShellの可読性が高く、エラーハンドリングが強化可能
5. **開発環境での検証**: ローカル環境での検証が容易
6. **本家との差分**: 本家との差分は変わらない（`vcsetup.cmd`も`vcsetup.ps1`も日本語版独自）

### 本家との差分に関する結論

**重要な認識**:
- `vcsetup.cmd`（または`vcsetup.ps1`）は日本語版独自の要件のため、本家には存在しない
- 本家はSConsだけでMSVCを使えるが、日本語版では`nmake`が必要なため、明示的な環境設定が必要
- PowerShellへの移行は、本家との差分を増やすものではなく、実装の改善である

**本家のアプローチとの関係**:

#### 1. `nonCertBuild.py`が`vswhere`を使用している理由と方法

**`nonCertBuild.py`のアプローチ**（本家のアプローチに近い）:

```python
def _ensure_nmake_env() -> None:
    """Ensure MSVC build tools (cl/nmake) are on PATH for this process.
    Order of attempts:
    1) If 'cl' seems callable, do nothing.
    2) Use vswhere to locate Visual Studio and call vcvars32/VsDevCmd, import env.
    3) Fallback to JP's jptools/vcsetup.cmd and import env.
    """
```

**ステップ1: Fast path**
- `cl`が既にPATHにある場合は何もしない（既にMSVC環境が設定されている）

**ステップ2: vswhereを使用**（本家のアプローチ）
- `vswhere.exe`を使用してVisual Studioのインストールパスを検出
- `vswhere -find`で`vcvars32.bat`、`vcvarsall.bat`、`VsDevCmd.bat`を検索
- 見つかったスクリプトを実行し、環境変数をキャプチャして`os.environ`に設定

**ステップ3: フォールバック**
- `vswhere`が失敗した場合、`vcsetup.cmd`をフォールバックとして使用

**なぜ`vswhere`を使用するのか**:
- **本家のアプローチに近い**: 本家も`vswhere`を使用してVisual Studioを検出
- **柔軟性**: Enterprise、Professional、BuildToolsなど、様々なVisual Studioエディションに対応
- **CI環境での動作**: GitHub ActionsなどのCI環境でも動作する
- **標準的な方法**: Microsoftが推奨するVisual Studio検出方法

#### 2. `certBuild2023.cmd`がバッチスクリプトであることの制約

**`certBuild2023.cmd`の構造**:

```batch
setlocal enableextensions enabledelayedexpansion
set SCONSOPTIONS=%*
...
call jptools\vcsetup.cmd %BUILD_ARCH%
@if not "%ERRORLEVEL%"=="0" goto onerror
...
call scons.bat launcher %SCONSARGS%
```

**バッチスクリプトの制約**:

1. **Pythonの直接実行が困難**:
   - `vswhere`を直接呼び出すことは可能だが、環境変数のキャプチャが複雑
   - `for /f`ループでPythonスクリプトを呼び出す必要がある（現在の`vcsetup.cmd`の方法）

2. **環境変数の継承**:
   - バッチスクリプト内で設定した環境変数は、同じプロセス内でのみ有効
   - `call`コマンドで別のバッチスクリプトを実行すると、環境変数が継承される

3. **エラーハンドリングの限界**:
   - `if errorlevel`によるエラーチェックは限定的
   - 詳細なエラーメッセージの取得が困難

4. **Pythonスクリプトとの統合**:
   - `nonCertBuild.py`のように`subprocess`を使用して環境変数をキャプチャできない
   - バッチスクリプトからPythonスクリプトを呼び出す必要がある

**なぜ`certBuild2023.cmd`はバッチスクリプトなのか**:
- 歴史的な理由（既存のビルドスクリプト）
- シンプルな実行（ダブルクリックで実行可能）
- Windows標準のバッチスクリプトで、追加の依存関係が不要

#### 3. PowerShellへの移行が`nonCertBuild.py`との一貫性をどう向上させるか

**現状の問題点**:

1. **異なる実装方法**:
   - `nonCertBuild.py`: Pythonで`vswhere`を使用（本家のアプローチ）
   - `vcsetup.cmd`: バッチスクリプト + Python依存（日本語版独自）

2. **コードの重複**:
   - `nonCertBuild.py`と`vcsetup.cmd`で、Visual Studio検索ロジックが重複
   - `vs_utils.py`で共通化されているが、バッチスクリプトからの呼び出しが複雑

3. **保守性の問題**:
   - バッチスクリプトの可読性が低い
   - エラーハンドリングが限定的

**PowerShellへの移行による改善**:

1. **実装方法の統一**:
   - `nonCertBuild.py`: Pythonで`vswhere`を使用
   - `vcsetup.ps1`: PowerShellで`vswhere`または`vs_utils.py`を使用
   - 両方とも同じアプローチ（`vswhere`または`vs_utils.py`）を使用可能

2. **コードの共通化**:
   - `vcsetup.ps1`から`vs_utils.py`を直接使用可能（または`find_vcvars.py`を呼び出し）
   - `nonCertBuild.py`と同じ検索ロジックを使用可能

3. **保守性の向上**:
   - PowerShellの可読性が高い
   - エラーハンドリングが強化可能
   - テストが容易（Pesterなど）

**具体的な改善例**:

**現状（vcsetup.cmd）**:
```batch
rem Use shared Python module for VS path detection (jptools/vs_utils.py)
rem This ensures consistency with scons_jp.py and runJpSmokeTests.ps1
set "FOUND="
for /f "delims=" %%P in ('python "%~dp0find_vcvars.py" %ARCH% 2^>nul') do (
  set "FOUND=%%P"
)
```

**移行後（vcsetup.ps1）**:
```powershell
# Use shared Python module for VS path detection (jptools/vs_utils.py)
# This ensures consistency with scons_jp.py and runJpSmokeTests.ps1
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
```

**改善点**:
- エラーハンドリングが強化（`try-catch`）
- ログ出力が改善（`Write-Host`）
- 可読性が向上（PowerShellの構文）

#### 4. 本家のアプローチとの整合性

**本家のアプローチ**:
- CI: `ilammy/msvc-dev-cmd@v1`を使用
- Pythonスクリプト: `vswhere`を使用（推測）

**日本語版のアプローチ**:
- CI: `ilammy/msvc-dev-cmd@v1`を使用（本家と同じ）
- Pythonスクリプト（`nonCertBuild.py`）: `vswhere`を使用（本家と同じ）
- バッチスクリプト（`certBuild2023.cmd`）: `vcsetup.cmd`を使用（日本語版独自）

**PowerShellへの移行後**:
- CI: `ilammy/msvc-dev-cmd@v1`を使用（本家と同じ）← **変わらない**
- Pythonスクリプト（`nonCertBuild.py`）: `vswhere`を使用（本家と同じ）← **変わらない**
- バッチスクリプト（`certBuild2023.cmd`）: `vcsetup.ps1`を使用（日本語版独自）← **実装が改善**

**結論**:
- PowerShellへの移行は、本家との差分を増やすものではない
- `nonCertBuild.py`との一貫性が向上する（同じアプローチを使用可能）
- 実装の改善により、保守性が向上する

### 5. `vswhere`への依存に関する検討

**重要な質問**: `vcsetup.cmd`（または`vcsetup.ps1`）も`vswhere`に依存すべきか？

**現状**:
- `nonCertBuild.py`: `vswhere`を使用（本家のアプローチ）
- `vcsetup.cmd`: `vs_utils.py`を使用（直接パス検索、`vswhere`を使用しない）
- `vs_utils.py`: 直接パス検索のみ（`vswhere`を使用しない）

**検討事項**:

1. **`nonCertBuild.py`との一貫性**:
   - `nonCertBuild.py`は`vswhere`を優先し、`vcsetup.cmd`をフォールバックとして使用
   - `vcsetup.cmd`も`vswhere`を使用することで、一貫性が向上する

2. **本家のアプローチとの整合性**:
   - 本家は`vswhere`を使用（推測）
   - `vcsetup.cmd`も`vswhere`を使用することで、本家のアプローチに近づく

3. **`vswhere`の可用性**:
   - ✅ Visual Studioがインストールされている環境では利用可能
   - ✅ CI環境（GitHub Actions）では通常利用可能
   - ❌ Visual Studioがインストールされていない環境では存在しない可能性がある

**推奨アプローチ**: `vswhere`を優先し、直接パス検索をフォールバックとする

**理由**:
1. **`nonCertBuild.py`との一貫性**: 同じ検出方法（`vswhere`）を使用
2. **本家のアプローチに近い**: Microsoftが推奨する標準的な方法
3. **柔軟性**: 様々なVisual Studioエディションに対応
4. **将来の拡張性**: Visual Studio 2025など、将来のバージョンにも対応可能
5. **フォールバック**: `vswhere`が存在しない環境でも動作する

**実装方針**:
1. `vs_utils.py`に`find_vcvars_with_vswhere()`関数を追加
2. `find_vcvars()`関数を修正し、`vswhere`を優先、直接パス検索をフォールバックとする
3. `vcsetup.ps1`で`vswhere`を優先し、Python検索、直接パス検索の順でフォールバック

詳細は`projectDocs/jp/vcsetup-vswhere-dependency-analysis.md`を参照。

### 推奨される移行計画

1. **フェーズ1**: `vcsetup.ps1`の作成と単体テスト（PR #1）
2. **フェーズ2**: `vcsetup.cmd`をラッパーに変更（PR #2）
3. **フェーズ3**: CIでの検証と安定化（PR #2の続き）

各フェーズで、品質保証原則に基づいて段階的に検証し、問題が発生した場合は即座に停止して対応する。

### 次のステップ（将来の作業）

⏳ **未実装**

**現在の状態**:
- ✅ `vswhere`リファクタリングは完了（`vs_utils.py`に`vswhere`サポート追加）
- ✅ Visual Studio 2022が優先的に使用される
- ⏳ `vcsetup.ps1`への移行は未実装

**実装計画**（将来の作業）:
1. `vcsetup.ps1`の実装と単体テストの作成
2. ローカル環境での動作確認
3. PR #1の作成とレビュー
4. CIでの検証

詳細は`projectDocs/jp/vcsetup-ps1-migration-proposal.md`を参照。
