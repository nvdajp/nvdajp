# システムテスト CI 復帰計画

## 概要

2026-07-30 に実施したシステムテスト調査の結果に基づき、CI ワークフローへのシステムテスト段階的復帰を提案する。

## 調査結果

### 実施した調査

- **調査期間**: 約 40 分
- **テストタグ数**: 16 種類
- **ビルド**: Azure Key Vault 署名付きビルド（37 ファイル署名）

### テスト別安定性

| テストタグ | 成功率 | 推奨カテゴリ | 備考 |
|-----------|--------|-------------|------|
| `chrome` | 90% (55/61) | **CI 復帰可能** | 最も安定、タイムアウト調整で改善 |
| `startupShutdown` | 73% (8/11) | 要調査 | UIAHandler クラッシュ処理に不安定性 |
| `symbols` | 60% (6/10) | 要調査 | 設定の問題（除外時は成功） |
| `NVDA` | 36% (8/22) | ローカル限定 | 記号発音テストが失敗 |
| `restarts_on_crash` | 33% (1/3) | ローカル限定 | 不安定すぎる |
| `vscode` | 0% (0/1) | ローカル限定 | VS Code 環境が必要 |
| `installer` | 0% (0/2) | 設定修正必要 | `--installDir` パラメータ不足 |

## 段階的復帰プラン

### Phase 1: 即座に CI 復帰（本 PR）

**対象**: `chrome` タグ

**理由**:
- 90% の安定性
- ブラウザー関連の基本的なアクセシビリティ機能をカバー
- 失敗は主にタイムアウト（一時的な問題の可能性）

**実装内容**:
1. `.github/workflows/testAndPublish.yml` のシステムテストジョブで `chrome` タグを復活
2. タイムアウト設定の調整（必要に応じて）
3. 失敗時のフォールバック動作を確認

**期待される影響**:
- CI 実行時間：+5〜10 分程度
- フラットフォームカバレッジ：向上
- 回帰検出能力：向上

### Phase 2: 調査・修正後に CI 復帰

**対象**: `startupShutdown` タグ

**課題**:
- UIAHandler クラッシュ処理の不安定性
- テスト環境依存の問題

**必要な調査**:
1. クラッシュダンプの分析
2. テスト環境の安定性向上
3. タイムアウト設定の最適化

**目標時期**: 2026-08 中旬

### Phase 3: 設定修正・環境整備

**対象**: `installer`, `symbols` タグ

**必要な対応**:
- `installer`: `--installDir` パラメータの追加
- `symbols`: 除外設定と包含設定の差異を調査

**目標時期**: 2026-08 下旬

### 継続的にローカル限定

**対象**: `vscode`, `restarts_on_crash`, 一部の `chrome_*` 詳細タグ

**理由**:
- 特殊な環境が必要（VS Code）
- 不安定性が高すぎる
- 実行時間が長すぎる

## 実装詳細（Phase 1）

### 変更ファイル

1. `.github/workflows/testAndPublish.yml`
   - システムテストジョブで `chrome` タグを有効化
   - 既存の除外設定を修正

2. `ci/scripts/beforeTests.ps1`（必要に応じて）
   - Chrome テスト実行前の環境セットアップ

### 予想される CI 変更

```yaml
# 変更前（現状）
- name: Run system tests
  run: |
    .\jptools\runSystemTests.ps1 `
      --exclude chrome `
      --exclude symbols `
      --exclude vscode `
      --exclude restarts_on_crash

# 変更後（Phase 1）
- name: Run system tests
  run: |
    .\jptools\runSystemTests.ps1 `
      --exclude symbols `
      --exclude vscode `
      --exclude restarts_on_crash
```

## リスク管理

### 想定されるリスク

1. **CI フラットフォームの増加**
   - 対策：90% の安定性だが、稀な失敗は許容
   - 再実行機能を活用

2. **CI 実行時間の増加**
   - 予想：+5〜10 分
   - 許容範囲内と判断

3. **ビルド遅延**
   - 対策：並列実行の検討（将来）

### モニタリング計画

- 最初の 2 週間は CI 結果を毎日確認
- フラットフォーム率を追跡
- 必要に応じて除外設定を見直し

## 成功基準

- [ ] `chrome` タグのテストが CI で安定して実行される
- [ ] 偽陽性（フラットフォーム）率が 10% 未満
- [ ] CI 実行時間が許容範囲内（+15 分以内）
- [ ] 回帰バグの検出能力が向上

## 次のステップ

1. [x] システムテスト調査の実施
2. [ ] 本 PR の作成とレビュー
3. [ ] `betajp` へのマージ
4. [ ] 2 週間のモニタリング
5. [ ] Phase 2 の検討開始

## 参考資料

- 調査結果サマリー: `testOutput\test_survey_results.csv`
- 詳細結果: `testOutput\test_survey_detailed.csv`
- 個別テストログ: `testOutput\survey_<tag>\`
