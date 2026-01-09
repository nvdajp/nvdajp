# projectDocs/jp ディレクトリ構造の整理案

**作成日**: 2026-01-09

## 現状

- **Markdownファイル数**: 60個
- **サブディレクトリ**: `compare-with-2025/`, `compare-with-beta/`
- **問題点**: ファイルが多すぎて、必要な情報を見つけにくい

## 整理方針

### カテゴリ分け

#### 1. **現在の状況・まとめ系**（ルートに残す）
- `README.md` - ドキュメントハブ（最重要）
- `roadmap.md` - ロードマップ
- `line-endings-summary.md` - 改行コード対応のまとめ
- `pyright-enablement-summary.md` - pyright対応のまとめ

#### 2. **過去の作業記録**（`archive/`に移動候補）
- `merge-*` - マージ関連の過去の記録
  - `merge-plan-beta-2025-11.md`
  - `merge-issues-beta-2025-11.md`
  - `merge-conflicts-detailed-2025-11.md`
  - `merge-decision-analysis.md`
  - `merge-readiness-checklist-260102.md`
  - `merge-rehearsal-*.md` (3ファイル)
- `period2-*` - 期間2の作業記録
  - `period2-qa-evaluation.md`
  - `period2-implementation-strategy.md`
  - `period2-scope-separation-plan.md`
- `pr608-vs-pr609-explanation.md` - PR説明
- `task3b4-*` - タスク3b.4の作業記録（完了済み）
  - `task3b4-commits-to-merge.md`
  - `task3b4-implementation-plan.md`
- `stage3b-*` - ステージ3bの作業記録（完了済み）
  - `stage3b-qa-checklist.md`
  - `stage3b-x64-migration-plan.md`
- `migration-review-2025.3jp-to-260102.md` - 移行レビュー

#### 3. **技術的な詳細**（ルートに残す、参照が多い）
- `braille-*` - 点字関連
  - `braille-ja-jp-comp6.md`
  - `braille-routing-analysis.md`
  - `braille-tables-relationship.md`
- `japanese-input-method-implementation.md` - IME実装
- `miscdepsjp-overlay-strategy.md` - miscDepsJp戦略
- `code-signing-dependencies.md` - コード署名依存関係
- `build-architecture-environment-variables.md` - ビルド環境変数
- `vendor-submodules.md` - ベンダーツリー
- `vswhere-implementation-status.md` - vswhere実装状況
- `po-merge-procedure.md` - POファイルマージ手順
- `po-file-status.md` - POファイル状況
- `waic-tests.md` - WAICテスト
- `chrome-system-test-japanese-environment.md` - Chrome system test
- その他の技術ドキュメント

#### 4. **トラブルシューティング**（`troubleshooting/`に移動候補）
- `troubleshooting_runjp_smoke_tests.md`
- `x64-jp-smoke-crash-investigation.md`
- `build_file_lock_troubleshooting.md`
- `local_verification_*` - ローカル検証関連
  - `local_verification_build_dependencies.md`
  - `local_verification_jtalk_runner_fix.md`

#### 5. **評価・分析**（`evaluation/`に移動候補）
- `certBuild2023_evaluation.md`
- `vcsetup-ps1-qa-evaluation.md`
- `vcsetup-ps1-migration-proposal.md`
- `vcsetup-responsibilities.md`
- `vcsetup-vswhere-dependency-analysis.md`
- `scons-jp-vswhere-dependency-analysis.md`
- `skip-test-decision-analysis.md`
- `test-routing-skip-justification.md`
- `test-routing-failures.md`
- `jpSmokeTest-error-patterns.md`

#### 6. **計画・提案**（`plans/`に移動候補、または削除候補）
- `ja-rokutenkanji-table-fix-plan.md` - **完了済み**（liblouis 3.36更新完了、コミット `e5a9b2e`）→ **削除候補**
- `todo_build_script_redundancy_and_logging.md` - TODO（優先度低、実装済みの可能性）→ **削除候補またはarchive/に移動**
- `talk-outline-nvdajp-development-2025-12.md` - 過去のイベント資料（2025年12月）→ **削除候補またはarchive/に移動**

#### 7. **比較結果**（既にサブディレクトリ、そのまま）
- `compare-with-2025/`
- `compare-with-beta/`

#### 8. **その他**（ルートに残す）
- `readmejp.md` - ユーザー向けドキュメント（大きい）
- `changes-nvdajp.md` - 変更履歴
- `tab_character_analysis.md` - タブ文字分析
- `nvdahighlighter-fix.md` - NVDAHighlighter修正
- `espeak-parallel-build-fix.md` - eSpeak並列ビルド修正
- `coderabbit-independent-setup.md` - CodeRabbit設定

## 推奨される整理構造

```
projectDocs/jp/
├── README.md                    # ドキュメントハブ（最重要）
├── roadmap.md                   # ロードマップ
├── line-endings-summary.md      # 改行コード対応のまとめ
├── pyright-enablement-summary.md # pyright対応のまとめ
│
├── archive/                     # 過去の作業記録
│   ├── merge-*.md
│   ├── period2-*.md
│   ├── pr608-vs-pr609-explanation.md
│   ├── task3b4-*.md
│   ├── stage3b-*.md
│   └── migration-review-*.md
│
├── troubleshooting/             # トラブルシューティング
│   ├── troubleshooting_*.md
│   ├── x64-jp-smoke-crash-investigation.md
│   ├── build_file_lock_troubleshooting.md
│   └── local_verification_*.md
│
├── evaluation/                  # 評価・分析
│   ├── certBuild2023_evaluation.md
│   ├── vcsetup-*.md
│   ├── scons-jp-vswhere-dependency-analysis.md
│   ├── skip-test-decision-analysis.md
│   ├── test-routing-*.md
│   └── jpSmokeTest-error-patterns.md
│
├── plans/                       # 計画・提案（削除済み）
│   └── （完了済み・不要な計画ファイルは削除済み）
│
├── compare-with-2025/          # 比較結果（既存）
├── compare-with-beta/          # 比較結果（既存）
│
└── [技術的な詳細ドキュメント]  # ルートに残す（参照が多い）
    ├── braille-*.md
    ├── japanese-input-method-implementation.md
    ├── miscdepsjp-overlay-strategy.md
    ├── code-signing-dependencies.md
    ├── build-architecture-environment-variables.md
    ├── vendor-submodules.md
    ├── vswhere-implementation-status.md
    ├── po-*.md
    ├── waic-tests.md
    ├── chrome-system-test-japanese-environment.md
    ├── readmejp.md
    ├── changes-nvdajp.md
    └── その他
```

## 整理のメリット

1. **可読性の向上**: カテゴリごとに整理され、必要な情報を見つけやすい
2. **保守性の向上**: 過去の作業記録と現在の情報を分離
3. **参照の明確化**: README.mdから主要なドキュメントへのリンクを整理

## 注意事項

1. **参照の更新**: ファイルを移動する場合、すべての参照を更新する必要がある
2. **段階的な実施**: 一度にすべてを移動せず、段階的に実施することを推奨
3. **README.mdの更新**: 移動後、README.mdのリンクを更新する必要がある

## 実施手順（推奨）

### フェーズ1: サブディレクトリの作成とREADME更新
1. `archive/`、`troubleshooting/`、`evaluation/`、`plans/`ディレクトリを作成
2. README.mdに新しい構造を説明するセクションを追加

### フェーズ2: 過去の作業記録の移動
1. `archive/`に過去の作業記録を移動
2. 参照を更新

### フェーズ3: トラブルシューティングの移動
1. `troubleshooting/`にトラブルシューティング関連を移動
2. 参照を更新

### フェーズ4: 評価・分析の移動
1. `evaluation/`に評価・分析関連を移動
2. 参照を更新

### フェーズ5: 計画・提案の整理
1. 完了済み・不要な計画ファイルを削除
   - `ja-rokutenkanji-table-fix-plan.md` - 完了済み（liblouis 3.36更新完了）
   - `talk-outline-nvdajp-development-2025-12.md` - 過去のイベント資料
2. 残りの計画ファイルを`archive/`に移動または削除
   - `todo_build_script_redundancy_and_logging.md` - TODO（優先度低、実装済みの可能性）

## 代替案: 最小限の整理

すべてを移動するのが大変な場合は、以下の最小限の整理も検討できます：

1. **完了済み・不要なファイルを削除**
   - `ja-rokutenkanji-table-fix-plan.md` - 完了済み（liblouis 3.36更新完了）
   - `talk-outline-nvdajp-development-2025-12.md` - 過去のイベント資料
   - `todo_build_script_redundancy_and_logging.md` - TODO（優先度低、実装済みの可能性）
   - これだけで約3ファイルが削除される

2. **過去の作業記録のみ`archive/`に移動**
   - `merge-*`、`period2-*`、`pr608-*`、`task3b4-*`、`stage3b-*`、`migration-review-*`
   - これだけで約15ファイルが整理される

3. **README.mdの改善**
   - カテゴリごとのセクションを追加
   - 主要なドキュメントへのリンクを整理
