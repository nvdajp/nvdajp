# システムテスト CI 復帰の提案

## 概要

2026-07-30 に実施したシステムテストの包括的調査に基づき、CI ワークフローへのシステムテスト段階的復帰を提案します。

## 調査の背景

- **調査期間**: 約 40 分
- **テスト対象**: 16 種類のシステムテストタグ
- **ビルド環境**: Azure Key Vault 署名付きビルド（37 ファイル署名済み）
- **調査スクリプト**: `jptools/surveySystemTests.ps1`

## 主要な発見

### テスト安定性ランキング

| 順位 | テストタグ | 成功率 | テスト数 | 推奨 |
|-----|-----------|--------|---------|------|
| 1 | `chrome` | **90%** | 55/61 | ✅ CI 復帰可能 |
| 2 | `startupShutdown` | 73% | 8/11 | ⚠️ 要調査 |
| 3 | `symbols` | 60% | 6/10 | ⚠️ 設定修正必要 |
| 4 | `NVDA` | 36% | 8/22 | ❌ ローカル限定 |
| 5 | `restarts_on_crash` | 33% | 1/3 | ❌ ローカル限定 |
| 6 | `vscode` | 0% | 0/1 | ❌ 環境依存 |
| 7 | `installer` | 0% | 0/2 | 🔧 パラメータ修正必要 |

### chrome テストの詳細

**成功理由**:
- 基本的な Web アクセシビリティ機能を網羅
- テスト環境が安定
- 失敗の多くはタイムアウト（一時的な問題）

**失敗ケース** (6 件中):
- スピーチタイムアウト（2 件）
- ウィンドウ検出失敗（1 件）
- その他（3 件）

## 提案：段階的復帰アプローチ

### Phase 1: 即座に CI 復帰（本 PR）

**対象**: `chrome` タグのみ

**実装内容**:
- `.github/workflows/testAndPublish.yml` で `chrome` タグを有効化
- 既存の除外リストから `chrome` を削除

**期待される効果**:
- ✅ ブラウザーアクセシビリティの回帰検出能力向上
- ✅ 実ユーザー環境に近いテストカバレッジ
- ✅ CI 実行時間は +5〜10 分程度（許容範囲）

**リスク管理**:
- 偽陽性率 10% 未満を目標
- 失敗時は再実行で対応
- 2 週間のモニタリング期間を設ける

### Phase 2: 調査・改善（2026-08 中旬目標）

**対象**: `startupShutdown` タグ

**必要な対応**:
- UIAHandler クラッシュ処理の安定性向上
- テスト環境の最適化
- タイムアウト設定の調整

### Phase 3: 設定修正（2026-08 下旬目標）

**対象**: `installer`, `symbols` タグ

**必要な対応**:
- `installer`: `--installDir` パラメータ追加
- `symbols`: 除外/包含設定の差異を調査

### 継続的ローカル限定

**対象**: `vscode`, `restarts_on_crash`, 一部 `chrome_*` 詳細タグ

**理由**:
- 特殊環境が必要
- 不安定性が高すぎる
- 実行時間が長すぎる

## 変更ファイル

### `.github/workflows/testAndPublish.yml`

```diff
  systemTests:
    runs-on: windows-2022
    steps:
      - name: Run system tests
        run: |
          .\jptools\runSystemTests.ps1 `
-           --exclude chrome `
            --exclude symbols `
            --exclude vscode `
            --exclude restarts_on_crash
```

## 成功基準

- [ ] `chrome` テストが CI で安定実行（成功率 90% 維持）
- [ ] 偽陽性率 10% 未満
- [ ] CI 実行時間 +15 分以内
- [ ] 回帰バグ検出能力の向上

## モニタリング計画

1. **最初の 2 週間**: 毎日 CI 結果を確認
2. **メトリクス収集**:
   - テスト成功率
   - 平均実行時間
   - 偽陽性率
3. **必要に応じて**: 除外設定を見直し

## 参考資料

- [システムテスト CI 復帰計画書](projectDocs/jp/system-tests-ci-restoration-plan.md)
- 調査結果サマリー: `testOutput/test_survey_results.csv`
- 詳細結果: `testOutput/test_survey_detailed.csv`
- 個別テストログ: `testOutput/survey_<tag>/`

## 関連 Issue

- #539 (ワークフロー整合性)
- 本調査で判明した問題のトラッキング用 Issue（必要に応じて作成）

## 結論

`chrome` テストの CI 復帰は、リスクが低く、効果が明確です。段階的アプローチにより、CI の信頼性を維持しながら、テストカバレッジを向上できます。
