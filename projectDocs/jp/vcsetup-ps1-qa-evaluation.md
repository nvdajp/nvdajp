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

* **標準的な方法**: Microsoftが推奨するVisual Studio検出方法
*et*ocal enableextensions enabledelayedexpansion
* 歴*的な理由（既存のビルドスクリプト）
###* 3. PowerShellへの移行が`nonCertBuild.py`との一貫性をどう向上させるか
***

*
*
*em This ensures consistency with scons_jp.py and runJpSmokeTests.ps1
*
*
**移行後（vcsetup.ps1）**:
*   $vcvarsPath = python $findVcvarsScript $Architecture 2>&1 | Where-Object { $_ -and $_ -notmatch "^\s*$" } | Select-Object -First 1
*   if ($vcvarsPath -and (Test-Path $vcvarsPath)) {
*   $vcvarsPath = $null

*
* ロ*出力が改善（`Write-Host`）
* 可*性が向上（PowerShellの構文）
*

* Pythonスクリプト: `vswhere`を使用（推測）
**

* CI: `ilammy/msvc-dev-cmd@v1`を使用（本家と同じ）
**P*werShellへの移行後**:
* CI: `ilammy/msvc-dev-cmd@v1`を使用（本家と同じ）← **変わらない**
* P*thonスクリプト（`nonCertBuild.py`）: `vswhere`を使用（本家と同じ）← **変わらない**
* バ*チスクリプト（`certBuild2023.cmd`）: `vcsetup.ps1`を使用（日本語版独自）← **実装が改善**
*

* `*onCertBuild.py`との一貫性が向上する（同じアプローチを使用可能）
* 実*の改善により、保守性が向上する
*

###*5. `vswhere`への依存に関する検討
*

**現***:

* `*onCertBuild.py`: `vswhere`を使用（本家のアプローチ）
* `*csetup.cmd`: `vs_utils.py`を使用（直接パス検索、`vswhere`を使用しない）
* `vs_utils.py`: 直接パス検索のみ（`vswhere`を使用しない）
*
*
1. **`nonCertBuild.py`との一貫性**:
   * `nonCertBuild.py`は`vswhere`を優先し、`vcsetup.cmd`をフォールバックとして使用

   * `vcsetup.cmd`も`vswhere`を使用することで、一貫性が向上する
   * `vcsetup.cmd`も`vswhere`を使用することで、本家のアプローチに近づく
*
*
*
3. **`vswhere`の可用性**:
   * ✅ Visual Studioがインストールされている環境では利用可能


**推奨アプローチ**: `vswhere`を優先し、直接パス検索をフォールバックとする

*
**理由**:
*
1. **`nonCertBuild.py`との一貫性**: 同じ検出方法（`vswhere`）を使用

3. **柔軟性**: 様々なVisual Studioエディションに対応
4. **将来の拡張性**: Visual Studio 2025など、将来のバージョンにも対応可能
5. **フォールバック**: `vswhere`が存在しない環境でも動作する

**実装方針**:
*
*. `vs_utils.py`に`find_vcvars_with_vswhere()`関数を追加
*. `find_vcvars()`関数を修正し、`vswhere`を優先、直接パス検索をフォールバックとする
3. `vcsetup.ps1`で`vswhere`を優先し、Python検索、直接パス検索の順でフォールバック


詳細は`projectDocs/jp/vcsetup-vswhere-dependency-analysis.md`を参照。

### 推奨される移行計画

1. **フェーズ1**: `vcsetup.ps1`の作成と単体テスト（PR #1）
*. **フェーズ2**: `vcsetup.cmd`をラッパーに変更（PR #2）
*. **フェーズ3**: CIでの検証と安定化（PR #2の続き）
*
各フェーズで、品質保証原則に基づいて段階的に検証し、問題が発生した場合は即座に停止して対応する。


### 次のステップ（将来の作業）

⏳ **未実装**

**現在の状態**:
* ✅ `vswhere`リファクタリングは完了（`vs_utils.py`に`vswhere`サポート追加）
* ✅ Visual Studio 2022が優先的に使用される
* ⏳ `vcsetup.ps1`への移行は未実装

**実装計画**（将来の作業）:

1. `vcsetup.ps1`の実装と単体テストの作成
2. ローカル環境での動作確認
3. PR #1の作成とレビュー
4. CIでの検証

詳細は`projectDocs/jp/vcsetup-ps1-migration-proposal.md`を参照。
