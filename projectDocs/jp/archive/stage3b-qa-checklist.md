# ステージ3b: x64 Python 3.13移行 - 品質保証チェックリスト

## 品質保証の原則（参照: `roadmap.md`）

* **小さなPR単位で進める**: 各PRで必ず全テストが通過することを確認
* **段階的な検証を必須とする**: 各段階でビルド・型チェック・単体テスト・システムテストを通過確認
* **完了の定義を明確化**: テストが全て通過し、CIが安定して緑になるまで「完了」としない
* **問題が発生したら即座に停止**: テスト失敗や不安定な動作が見られたら、次の段階に進まずに問題を解決

## 前提条件の確認

### ✅ 完了済み

* ✅ **ステージ3a完了**: x86 Python 3.13対応完了
  * コミット: `625691b11a` - "x86 + Python 3.13 (#607)"
  * **重要**: PR #607が安全な状態でマージされたものがbetajpブランチであり、これが作業の起点
  * ローカル検証完了（型チェック、ビルド、JP smoke test x86/x64、ランチャービルド）
  * CI状態: PR #607で`allTestsPass`が通過し、安全な状態でマージ済み ✅

* ✅ **マージリハーサル完了**: x64移行コミット（`58dd14767`）のマージリハーサル実施
  * 255ファイルのコンフリクトを確認
  * 記録: `projectDocs/jp/merge-rehearsal-x64-2025-12-30.md`

* ✅ **x64検証環境整備完了**
  * ローカル環境: `checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests` ✅
  * CI環境: `.github/workflows/checkJtalkArch-x64.yml` ✅

### ⚠️ 確認が必要な項目

#### 1. ローカル環境での検証確認（最優先）✅ 完了（2025-12-30）

**確認項目**:
- [x] 現在のブランチ（betajp-251231）でローカル検証が可能か ✅
- [x] 型チェック: `ci/scripts/tests/typeCheck.ps1` が成功するか ✅
- [x] ビルド: `.\scons.bat source --all-cores` が成功するか ✅
- [x] JP smoke test (x86): `jptools/checkJtalkArch.ps1 -Architecture x86 -RunSmokeTests` が成功するか ✅
- [x] JP smoke test (x64): `jptools/checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests` が成功するか ✅

**検証結果**:
- **型チェック**: ✅ 成功（仮想環境作成完了）
- **ビルド**: ✅ 成功（jtalkSync、jtalkPrep ビルド成功）
- **JP smoke test (x86)**: ✅ 成功（2 tests passed (JpBrailleTests), 1 test passed (JtalkTests)）
- **JP smoke test (x64)**: ✅ 成功（x64 DLL ビルド成功、3 tests passed）

**理由**: 品質保証原則「段階的な検証を必須とする」に従い、各段階で検証を実施する必要がある。

#### 2. マージ戦略の検討

**現状**:
- 255ファイルのコンフリクトが確認された
- これは「小さなPR単位」の原則に反する可能性がある

**検討課題**:

**オプションA: 一度にマージ（推奨アプローチ）**
- 利点: x86を完全に捨てられる、依存関係の複雑化を抑制
- リスク: 255ファイルのコンフリクトを一度に解決する必要がある
- 検証: 各作業段階（1-6）で段階的に検証を実施

**オプションB: 段階的にマージ**
- 利点: 変更量を分割してリスクを低減
- リスク: x86/x64の両方をサポートする複雑さが残る、作業量が増える

**推奨**: オプションAを採用し、作業段階1-6に従って段階的に検証を実施する

#### 4. 作業段階ごとの検証計画

**作業段階 1: 基盤整備**
- [ ] サブモジュールとロックファイルの解決後、型チェックを実施
- [ ] `uv.lock` の再生成後、依存関係の整合性を確認

**作業段階 2: ビルドシステム**
- [ ] ビルドシステムの更新後、`scons source --all-cores` でビルドを確認
- [ ] JP固有のビルドシステム（`jtalkSync`、`jtalkPrep`）がx64で動作するか確認

**作業段階 3: CI/ワークフロー**
- [ ] `testAndPublish.yml` の更新後、ローカルで構文チェックを実施
- [ ] PRを作成してCIを実行し、`allTestsPass` が緑になることを確認

**作業段階 4: ソースコード**
- [ ] ソースコードの更新後、型チェックを実施
- [ ] JP固有コードの動作確認

**作業段階 5: テスト**
- [ ] テストファイルの更新後、ローカルでテストを実行
- [ ] JP固有テストの動作確認

**作業段階 6: 検証と完了確認**
- [ ] 型チェック: `ci/scripts/tests/typeCheck.ps1` ✅
- [ ] ビルド: `scons source --all-cores` ✅
- [ ] JP smoke tests (x64): `jptools/checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests` ✅
- [ ] ランチャービルド: `scons launcher --all-cores` ✅
- [ ] CI検証: PRを作成してCIを実行、`allTestsPass` が緑になることを確認 ✅

## 作業を進める前の最終確認

### ✅ 必須条件

- [x] **ベースコミットのCI状態が緑**: PR #607で`allTestsPass`が通過し、安全な状態でマージ済み ✅
- [x] **ローカル環境での検証が可能**: 現在のブランチで検証環境が整備されている ✅（2025-12-30完了）
- [x] **マージ戦略が決定**: オプションA（一度にマージ）を採用することを決定 ✅

### ⚠️ リスク要因

1. **255ファイルのコンフリクト**: 一度に解決する必要がある
   - **対策**: 作業段階1-6に従って段階的に解決し、各段階で検証を実施

2. **x64環境での検証**: ローカル環境とCI環境の両方で検証が必要
   - **対策**: 既にx64検証環境が整備済み ✅

3. **x86コードの削除**: x86関連のコードを削除する際の見落とし
   - **対策**: 段階的に確認し、各段階で検証を実施

## 推奨される次のステップ

### ステップ1: ローカル環境での検証（最優先）✅ 完了（2025-12-30）

**前提**: PR #607が安全な状態でマージされており、ベースコミット `625691b11a` は既に検証済み ✅

```powershell
# 型チェック
ci/scripts/tests/typeCheck.ps1

# ビルド
.\scons.bat source --all-cores

# JP smoke test (x86)
jptools/checkJtalkArch.ps1 -Architecture x86 -RunSmokeTests

# JP smoke test (x64)
jptools/checkJtalkArch.ps1 -Architecture x64 -RunSmokeTests
```

**完了条件**: すべての検証が成功することを確認 ✅

**検証結果**:
- ✅ 型チェック: 成功
- ✅ ビルド: 成功
- ✅ JP smoke test (x86): 成功（2 tests passed (JpBrailleTests), 1 test passed (JtalkTests)）
- ✅ JP smoke test (x64): 成功（x64 DLL ビルド成功、3 tests passed）

### ステップ2: マージ実施の開始

**条件**: ステップ1が完了していること

**作業内容**: タスク 3b.3（x64対応の実施）を開始
- 作業段階1-6に従って段階的に解決
- 各段階で検証を実施
- 問題が発生したら即座に停止して修正

## 参照

- **ロードマップ**: `projectDocs/jp/roadmap.md`
- **詳細計画**: `projectDocs/jp/stage3b-x64-migration-plan.md`
- **マージリハーサル記録**: `projectDocs/jp/merge-rehearsal-x64-2025-12-30.md`
- **品質保証原則**: `projectDocs/jp/roadmap.md` の「品質保証の原則」セクション
