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

#### 4. **過去の作業記録・分析・トラブルシューティング**（`archive/`に統合）
- マージ関連: `merge-*.md`
- 期間2関連: `period2-*.md`
- タスク関連: `task3b4-*.md`、`stage3b-*.md`
- トラブルシューティング: `troubleshooting_*.md`、`build_file_lock_troubleshooting.md`、`local_verification_*.md`
- 評価・分析: `vcsetup-*.md`、`scons-jp-vswhere-dependency-analysis.md`、`skip-test-decision-analysis.md`、`test-routing-*.md`、`jpSmokeTest-error-patterns.md`
- その他: `pr608-vs-pr609-explanation.md`、`migration-review-*.md`

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
├── archive/                     # 過去の作業記録など
│   ├── merge-*.md
│   ├── period2-*.md
│   ├── pr608-vs-pr609-explanation.md
│   ├── task3b4-*.md
│   ├── stage3b-*.md
│   └── migration-review-*.md
│   ├── troubleshooting_*.md
│   ├── build_file_lock_troubleshooting.md
│   └── local_verification_*.md
│   ├── vcsetup-*.md
│   ├── scons-jp-vswhere-dependency-analysis.md
│   ├── skip-test-decision-analysis.md
│   ├── test-routing-*.md
│   └── jpSmokeTest-error-patterns.md
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

### フェーズ1: `archive/`ディレクトリの作成とREADME更新
1. `archive/`ディレクトリを作成
2. README.mdに新しい構造を説明するセクションを追加

### フェーズ2: 過去の作業記録・分析・トラブルシューティングの移動
1. `archive/`に以下を移動:
   - マージ関連: `merge-*.md`
   - 期間2関連: `period2-*.md`
   - タスク関連: `task3b4-*.md`、`stage3b-*.md`
   - トラブルシューティング: `troubleshooting_*.md`、`build_file_lock_troubleshooting.md`、`local_verification_*.md`
   - 評価・分析: `vcsetup-*.md`、`scons-jp-vswhere-dependency-analysis.md`、`skip-test-decision-analysis.md`、`test-routing-*.md`、`jpSmokeTest-error-patterns.md`
   - その他: `pr608-vs-pr609-explanation.md`、`migration-review-*.md`
2. 参照を更新（特に`troubleshooting_runjp_smoke_tests.md`など、現在も参照されているファイル）

## 注意事項

1. **参照の更新**: ファイルを`archive/`に移動する場合、すべての参照を更新する必要があります
2. **段階的な実施**: 一度にすべてを移動せず、段階的に実施することを推奨します
3. **README.mdの更新**: 移動後、README.mdのリンクを更新する必要があります
4. **現在も参照されているファイル**: `troubleshooting_runjp_smoke_tests.md`など、現在も参照されているファイルを移動する場合は、参照元を更新してください
